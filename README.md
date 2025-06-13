# AskMyResume
# 🧠 Resume Skill-Based Interview Question Generator

This Streamlit app automatically analyzes a PDF resume to:
- Extract technical and soft skills
- Generate tailored technical interview questions using LLaMA-3 via Groq API
- Summarize resume content
- Visualize skills with a word cloud

🔗 **[Try it Live on Streamlit](https://askmyresume-ckttmciaxa67zpjxedd7nq.streamlit.app/)** 

---

## 🚀 Features

- 📄 **PDF Resume Parsing:** Reads and extracts text from uploaded PDF resumes.
- 🧠 **AI-Powered Summary:** Summarizes resume into 3–4 meaningful sentences.
- 🛠️ **Skill Extraction:** Identifies popular technical skills (e.g., Python, SQL, AWS).
- 💡 **Soft Skill Detection:** Extracts soft skills using LLM analysis.
- 🎯 **Interview Questions:** Auto-generates technical interview questions based on extracted skills.
- ☁️ **Word Cloud Visualization:** Displays detected skills in a visual word cloud.
- 📥 **Download Questions:** Allows users to download questions as a `.txt` file.

---

## 📦 Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **Resume Parsing:** [pdfplumber](https://github.com/jsvine/pdfplumber)
- **AI Models:** [LLaMA-3](https://huggingface.co/meta-llama) via [Groq API](https://console.groq.com/)
- **Word Cloud Visualization:** [WordCloud](https://github.com/amueller/word_cloud), [Matplotlib](https://matplotlib.org/)

---

## 📁 Project Structure

```
resume-question-generator/
│
├── app.py                     # 🚀 Main Streamlit application
├── requirements.txt           # 📦 Required Python packages
├── README.md                  # 📘 This documentation file
│
├── .streamlit/                # 🔐 Secrets folder for API key
  └── secrets.toml           #     Groq API key stored securely here

 
```

