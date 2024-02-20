import streamlit as st
import re
from pdfminer.high_level import extract_text
from PyPDF2 import PdfReader
from pathlib import Path
import spacy
from spacy.matcher import Matcher

def extract_text_from_pdf(uploaded_file):
    text = ""
    try:
        with uploaded_file as file:
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
    except Exception as e:
        st.error("Error occurred while processing the PDF file.")
        st.stop()
    return text

def extract_contact_number_from_resume(text):
    contact_number = None
    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    match = re.search(pattern, text)
    if match:
        contact_number = match.group()
    return contact_number

def extract_email_from_resume(text):
    email = None
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    match = re.search(pattern, text)
    if match:
        email = match.group()
    return email

def extract_skills_from_resume(text, skills_list):
    skills = []
    for skill in skills_list:
        pattern = r"\b{}\b".format(re.escape(skill))
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            skills.append(skill)
    return skills

def extract_education_from_resume(text):
    education = []
    education_keywords = ['BE CSE', 'Bsc', 'B. Pharmacy', 'B Pharmacy', 'Msc', 'M. Pharmacy', 'Ph.D', 'Bachelor', 'Master','B.E.CSE','B.S.Computer Science']
    for keyword in education_keywords:
        pattern = r"(?i)\b{}\b".format(re.escape(keyword))
        match = re.search(pattern, text)
        if match:
            education.append(match.group())
    return education

def extract_name(resume_text):
    nlp = spacy.load('en_core_web_sm')
    matcher = Matcher(nlp.vocab)
    patterns = [
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}],  
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}],  
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}]  
    ]
    for pattern in patterns:
        matcher.add('NAME', patterns=[pattern])
    doc = nlp(resume_text)
    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        return span.text
    return None

def extract_information_from_resume(resume_text):
    name = extract_name(resume_text)
    if name:
        st.sidebar.markdown(f"**Name:** {name}")

    contact_number = extract_contact_number_from_resume(resume_text)
    if contact_number:
        st.sidebar.markdown(f"**Contact Number:** {contact_number}")

    email = extract_email_from_resume(resume_text)
    if email:
        st.sidebar.markdown(f"**Email:** {email}")

    skills_list = ['Python', 'Data Analysis', 'Machine Learning', 'Communication','Artificial Intelligence','Data Analysis','PowerBI','SQL','C']
    extracted_skills = extract_skills_from_resume(resume_text, skills_list)
    if extracted_skills:
        st.sidebar.markdown(f"**Skills:**")
        for skill in extracted_skills:
            st.sidebar.markdown(f"- {skill}")

    extracted_education = extract_education_from_resume(resume_text)
    if extracted_education:
        st.sidebar.markdown(f"**Education:**")
        for education in extracted_education:
            st.sidebar.markdown(f"- {education}")

def main():
    st.title('Resume Parser')
    st.markdown("---")
    st.write("Upload a resume in PDF format:")
    uploaded_file = st.file_uploader("", type=["pdf"])

    if uploaded_file is not None:
        resume_text = extract_text_from_pdf(uploaded_file)
        extract_information_from_resume(resume_text)

        # Apply CSS for the box outline
        st.sidebar.markdown(
            """
            <style>
                .reportview-container .sidebar .sidebar-content {
                    border-color: #1abc9c;
                    border-width: 2px;
                    border-radius: 5px;
                }
            </style>
            """,
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()

