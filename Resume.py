import streamlit as st
from PyPDF2 import PdfReader

st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 ATS Resume Analyzer")

skills_db = [
    "python","java","c++","sql","html",
    "css","javascript","git","github",
    "machine learning","data analysis",
    "react","nodejs","mongodb"
]

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

if uploaded_file:

    pdf = PdfReader(uploaded_file)

    text = ""

    for page in pdf.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text.lower()

    found_skills = []

    for skill in skills_db:
        if skill in text:
            found_skills.append(skill)

    score = min(len(found_skills) * 7, 70)

    if "project" in text:
        score += 10

    if "internship" in text:
        score += 10

    if "certification" in text:
        score += 10

    score = min(score,100)

    st.subheader("ATS Score")
    st.progress(score/100)
    st.metric("Score",f"{score}/100")

    col1,col2 = st.columns(2)

    with col1:
        st.subheader("Detected Skills")
        st.success(found_skills)

    with col2:
        missing = [
            skill
            for skill in skills_db
            if skill not in found_skills
        ]

        st.subheader("Missing Skills")
        st.error(missing)

    st.subheader("Strengths")

    strengths = []

    if len(found_skills) >= 5:
        strengths.append(
            "Good technical skill set"
        )

    if "project" in text:
        strengths.append(
            "Projects section found"
        )

    if "internship" in text:
        strengths.append(
            "Internship experience found"
        )

    if strengths:
        for s in strengths:
            st.write("✅",s)

    st.subheader("Weaknesses")

    weaknesses = []

    if len(found_skills) < 5:
        weaknesses.append(
            "Add more technical skills"
        )

    if "project" not in text:
        weaknesses.append(
            "Projects section missing"
        )

    if "internship" not in text:
        weaknesses.append(
            "Internship experience missing"
        )

    if "certification" not in text:
        weaknesses.append(
            "Certifications missing"
        )

    for w in weaknesses:
        st.write("❌",w)

    st.subheader("Final Verdict")

    if score >= 80:
        st.success(
            "Excellent Resume"
        )

    elif score >= 60:
        st.warning(
            "Good Resume but needs improvement"
        )

    else:
        st.error(
            "Resume needs major improvement"
        )