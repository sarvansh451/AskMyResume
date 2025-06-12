import streamlit as st
import pdfplumber
import re
from openai import OpenAI
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Initialize Groq-compatible OpenAI client
client = OpenAI(
    api_key=st.secrets["groq"]["api_key"],
    base_url="https://api.groq.com/openai/v1"
)

MODEL_ID = "llama3-70b-8192"  # Supported model on Groq

def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    return full_text

def extract_skills(text, skills_list):
    text_lower = text.lower()
    return [skill for skill in skills_list if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text_lower)]

def generate_questions(skills, num_questions):
    skills = skills or ["software development"]
    prompt = (
        f"Generate {num_questions} direct technical interview questions for a candidate skilled in: "
        f"{', '.join(skills)}.\n"
        "Only list the questions, numbered, with no explanations, no introductions, and no commentary.\n"
        "Example:\n"
        "1. What is polymorphism in object-oriented programming?\n"
        "2. How does a REST API work?\n\n"
        "Questions:\n"
    )

    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "You are an expert interview question generator."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=800,
    )

    text = response.choices[0].message.content.strip()
    lines = text.split("\n")
    questions = [line.strip() for line in lines if re.match(r"^\d+\.\s", line) or "?" in line]
    return questions[:num_questions] 

def generate_summary(text):
    prompt = (
        "Summarize the following resume text in 3-4 sentences, highlighting technical skills, experience, and role preferences.\n\n"
        f"Resume Text:\n{text}\n"
    )
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "You are a professional resume summarizer."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.5,
        max_tokens=300,
    )
    return response.choices[0].message.content.strip()

def extract_soft_skills(text):
    prompt = (
        "Extract and list the top soft skills mentioned or implied in the following resume text:\n\n"
        f"{text}\n"
        "\nList them as a comma-separated list."
    )
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "You are an expert at identifying soft skills in resumes."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.5,
        max_tokens=150,
    )
    return response.choices[0].message.content.strip()

def show_wordcloud(skills):
    if not skills:
        return
    wordcloud_text = " ".join(skills)
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(wordcloud_text)

    st.subheader("📊 Skill WordCloud")
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

def main():
    st.set_page_config(page_title="Skill-based Interview Q Generator", page_icon="🧠")
    st.title("🧠 Skill-based Resume Interview Question Generator")

    num_questions = st.slider("Number of questions:", 1, 10, 5)
    uploaded = st.file_uploader("Upload your PDF resume", type="pdf")
    if not uploaded:
        return

    with st.spinner("Extracting text from resume..."):
        resume_text = extract_text_from_pdf(uploaded)

    if not resume_text.strip():
        st.error("No text found in PDF.")
        return
    st.success("Resume text extracted!")

    # Summary Section
    with st.spinner("Generating resume summary..."):
        summary = generate_summary(resume_text)
    st.subheader("📝 Resume Summary:")
    st.markdown(summary)

    # Extract Common Technical Skills
    common_skills = [
        "machine learning", "sql", "java", "python", "data structures",
        "c++", "javascript", "deep learning", "nlp", "react",
        "aws", "docker", "kubernetes", "git", "html", "css"
    ]
    skills = extract_skills(resume_text, common_skills)

    if skills:
        st.write(f"**✅ Extracted Skills:** {', '.join(skills)}")
    else:
        st.info("⚠️ No predefined skills found; using general software development.")

    show_wordcloud(skills)

    # Soft Skills
    with st.spinner("Extracting soft skills..."):
        soft_skills = extract_soft_skills(resume_text)
    st.subheader("💡 Soft Skills:")
    st.markdown(soft_skills)

    # Interview Questions
    with st.spinner(f"Generating {num_questions} interview questions..."):
        questions = generate_questions(skills, num_questions)

    st.subheader("📝 Generated Interview Questions:")
    for i, q in enumerate(questions, 1):
        st.markdown(f"* {q}")

    questions_text = "\n".join([f"{q}" for q in questions])
    st.subheader("📄 Download or Copy Questions")

    st.download_button(
        label="📥 Download as .txt",
        data=questions_text,
        file_name="interview_questions.txt",
        mime="text/plain"
    )

    st.code(questions_text, language="markdown")

if __name__ == "__main__":
    main()
