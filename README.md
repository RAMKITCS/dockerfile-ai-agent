# 🐳 AI-Powered Dockerfile Generator

This project is an AI-driven Dockerfile generator built using **Streamlit**, **LangChain**, and **OpenAI's GPT-4o**. It can analyze a **GitHub Repository URL** or **manual descriptions** to automatically generate an optimized Dockerfile with best practices.

---

## 🚀 Features
✅ **Detects Tech Stack & Dependencies** from GitHub repositories or manual descriptions  
✅ Generates an optimized **Dockerfile** with caching, security, and efficiency best practices  
✅ Supports **Natural Language Refinements** to iteratively improve the generated Dockerfile  
✅ Provides a downloadable **Dockerfile** for easy integration into your project  

---

## 📋 Prerequisites
- Python 3.10 or higher
- An **OpenAI API Key** (set as an environment variable)
- Required Python Libraries:

```bash
pip install streamlit langchain_openai requests
```

---

## ⚙️ Setup Instructions

1. **Clone the Repository**
```bash
git clone https://github.com/your-username/dockerfile-generator.git
cd dockerfile-generator
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Set the OpenAI API Key**
```bash
export OPENAI_API_KEY=your-api-key-here
```
*(For Windows users using PowerShell)*:
```powershell
$env:OPENAI_API_KEY="your-api-key-here"
```

4. **Run the Streamlit Application**
```bash
streamlit run Dockerfile_agent.py
```

---

## 🖥️ How to Use

1. **Select Input Type:** Choose between `GitHub Repository URL` or `Manual Description`.
2. **Analyze Repo or Provide Description:**
   - For GitHub URL: Enter the repository link, then click **"Analyze Repo"**.
   - For Manual Description: Enter the details of your application like tech stack, dependencies, etc.
3. **Generate Dockerfile:** Click **"Generate Dockerfile"** to create a Dockerfile with best practices.
4. **Refine Dockerfile:** Provide suggestions to improve the Dockerfile using natural language and click **"Refine Dockerfile"**.
5. **Download the Dockerfile:** Click the download button to retrieve the generated file.

---

## 🛠️ Example Input for Manual Description
```text
Python 3.12 with Flask framework
Gunicorn as WSGI server
Uses Redis and MongoDB services
Includes a 'requirements.txt' for dependencies
```

---

## 📄 Sample Dockerfile Output
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]
```

---

## 🚧 Future Enhancements
✅ `.dockerignore` file auto-generation  
✅ Multi-stage build support for enhanced performance  
✅ Dynamic **Health Check** insertion for improved reliability  
✅ Intelligent security hardening strategies  

---

## 🧑‍💻 Contribution
Contributions are welcome! Feel free to open issues, submit feature requests, or create pull requests to improve the project.

---

## 🧩 License
This project is licensed under the **MIT License**.



