import os
import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from io import BytesIO
import requests
import zipfile
import tempfile
import shutil

# Load OpenAI API Key securely
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("\U0001F6D1 Missing OpenAI API Key! Set it as an environment variable.")
    st.stop()

# Initialize OpenAI model
llm = ChatOpenAI(
    model_name="gpt-4o",
    openai_api_key=openai_api_key,
    temperature=0.1,
    max_retries=3
)

# Function to clone and analyze GitHub repo
def analyze_github_repo(repo_url):
    api_url = repo_url.replace("github.com", "api.github.com/repos") + "/zipball/main"
    temp_dir = tempfile.mkdtemp()

    try:
        response = requests.get(api_url)
        if response.status_code != 200:
            st.error("❌ Failed to download repository archive.")
            return None

        # Extract repository files
        zip_path = os.path.join(temp_dir, "repo.zip")
        with open(zip_path, "wb") as f:
            f.write(response.content)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Analyze files to detect tech stack and dependencies
        detected_info = ""
        tech_stack = []
        dependencies = []

        for root, _, files in os.walk(temp_dir):
            if "requirements.txt" in files:
                tech_stack.append("Python")
                dependencies.append("requirements.txt")
            if "package.json" in files:
                tech_stack.append("Node.js")
                dependencies.append("package.json")
            if "pom.xml" in files:
                tech_stack.append("Java (Maven)")
                dependencies.append("pom.xml")
            if "build.gradle" in files:
                tech_stack.append("Java (Gradle)")
                dependencies.append("build.gradle")
            if any(f.endswith(".csproj") for f in files):
                tech_stack.append(".NET")
                dependencies.append(".csproj")

        detected_info += f"**Tech Stack:** {', '.join(set(tech_stack))}\n"
        detected_info += f"**Dependencies:** {', '.join(set(dependencies))}\n"

        if not detected_info.strip():
            detected_info = "Unable to detect dependencies. Please provide details manually."

        shutil.rmtree(temp_dir)  # Clean up
        return detected_info.strip()

    except Exception as e:
        st.error(f"❌ Error analyzing GitHub repo: {str(e)}")
        return None

# Function to generate Dockerfile based on detected info
def generate_dockerfile(codebase_description):
    prompt = f"""
    Generate a Dockerfile based on the following application details:

    {codebase_description}

    Ensure the Dockerfile follows best practices such as:
    - Using lightweight base images (e.g., `python:3.12-slim`, `node:20-alpine`).
    - Minimizing the number of layers.
    - Ensuring efficient caching.
    - Implementing proper `.dockerignore` file recommendations.
    - Securing the container by limiting root permissions.

    Output only the Dockerfile content.
    """

    try:
        response = llm.invoke(prompt)
        return response.content.strip() if hasattr(response, 'content') else str(response).strip() if response else "❌ No response received!"
    except Exception as e:
        st.error(f"❌ Error generating Dockerfile: {str(e)}")
        return None

# Function to refine Dockerfile based on user feedback
def refine_dockerfile(feedback, dockerfile_code):
    prompt = f"""
    Refine the following Dockerfile based on this user feedback:

    Feedback: {feedback}

    Dockerfile:
    {dockerfile_code}

    Ensure improvements include security, caching, efficiency, and best practices.
    Output only the updated Dockerfile content.
    """
    try:
        response = llm.invoke(prompt)
        return response.content.strip() if hasattr(response, 'content') else str(response).strip() if response else "❌ No response received!"
    except Exception as e:
        st.error(f"❌ Error refining Dockerfile: {str(e)}")
        return None

# Function to provide file download option
def get_download_link(content, file_name):
    file_bytes = BytesIO(content.encode('utf-8'))
    return st.download_button(label="📥 Download Dockerfile", data=file_bytes, file_name=file_name, mime="text/plain")

# Streamlit UI
st.set_page_config(layout="wide")
st.title("🐳 AI-Powered Dockerfile Generator")

# Sidebar for codebase details
st.sidebar.header("🗂️ Application Details")
input_type = st.sidebar.radio("Input Type", ["GitHub Repository URL", "Manual Description"])

if input_type == "GitHub Repository URL":
    repo_url = st.sidebar.text_input("🔗 Enter GitHub Repo URL")
    if st.sidebar.button("Analyze Repo"):
        detected_info = analyze_github_repo(repo_url)
        if detected_info:
            st.markdown("### 🔎 Detected Information")
            st.markdown(detected_info)
            st.session_state.detected_info = detected_info

if input_type == "Manual Description":
    codebase_description = st.sidebar.text_area("📋 Describe your application (framework, dependencies, etc.)", height=200)
    st.session_state.detected_info = codebase_description

# Generate Dockerfile
if st.sidebar.button("Generate Dockerfile"):
    dockerfile_code = generate_dockerfile(st.session_state.detected_info)
    if dockerfile_code:
        st.session_state.dockerfile_code = dockerfile_code
        st.success("✅ Dockerfile generated successfully!")
        st.code(dockerfile_code, language="dockerfile", line_numbers=True)
        get_download_link(dockerfile_code, "Dockerfile")

# Refinement section
st.subheader("🔄 Refine Dockerfile Using Natural Language Suggestions")
refine_feedback = st.text_area("✍️ Provide feedback to refine the Dockerfile:", height=150)
if st.button("Refine Dockerfile"):
    if "dockerfile_code" not in st.session_state or not st.session_state.dockerfile_code:
        st.warning("⚠️ Generate a Dockerfile first before refining.")
    elif not refine_feedback.strip():
        st.warning("⚠️ Please provide feedback before refining.")
    else:
        refined_dockerfile = refine_dockerfile(refine_feedback, st.session_state.dockerfile_code)
        if refined_dockerfile:
            st.session_state.dockerfile_code = refined_dockerfile
            st.success("✅ Dockerfile refined successfully!")
            st.code(refined_dockerfile, language="dockerfile", line_numbers=True)
            get_download_link(refined_dockerfile, "Dockerfile")
