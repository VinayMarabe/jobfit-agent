import os
import streamlit as st
from google import genai
from pypdf import PdfReader

st.set_page_config(page_title="JobFit Agent", page_icon="🎯", layout="wide")

st.title("🎯 JobFit Agent")
st.caption("An LLM-powered assistant that compares a resume with a job description and suggests concrete improvements.")

with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input(
        "Gemini API key",
        type="password",
        help="Your key is used only for this session. Do not paste it into source code or commit it to GitHub."
    )
    st.caption("Get a key from Google AI Studio. Keep it private.")

left, right = st.columns(2)
with left:
    st.subheader("1. Your resume")
    resume_file = st.file_uploader("Upload a PDF resume", type=["pdf"])
    resume_text_manual = st.text_area("Or paste resume text", height=180, placeholder="Paste your resume text here…")
with right:
    st.subheader("2. Target role")
    job_title = st.text_input("Job title", placeholder="e.g. Junior Data Scientist")
    job_description = st.text_area("Job description", height=230, placeholder="Paste the full job description here…")

def extract_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    return "\n".join(page.extract_text() or "" for page in reader.pages).strip()

if st.button("Analyze my fit", type="primary", use_container_width=True):
    resume_text = resume_text_manual.strip()
    if not resume_text and resume_file is not None:
        try:
            resume_text = extract_pdf(resume_file)
        except Exception as exc:
            st.error(f"Could not read that PDF: {exc}")
            st.stop()

    if not api_key.strip():
        st.error("Enter your Gemini API key in the sidebar.")
    elif not resume_text:
        st.error("Upload a readable PDF or paste your resume text.")
    elif not job_description.strip():
        st.error("Paste the job description.")
    else:
        with st.spinner("Reviewing the resume against the role…"):
            try:
                client = genai.Client(api_key=api_key.strip())
                prompt = f"""
You are JobFit Agent, a careful career-support assistant. Compare the resume with the job description.
Do not invent experience, credentials, metrics, or skills. Clearly distinguish evidence from suggestions.
Return Markdown with these sections:
1. Overall fit (score out of 100, clearly labelled as an approximate heuristic, not a hiring prediction)
2. Strong matches (quote or point to resume evidence)
3. Important gaps (only based on the supplied job description)
4. Five prioritized resume improvements (truthful and specific)
5. Suggested ATS keywords, separated into already supported and only add if genuinely true
6. Three likely interview questions based on the gaps
7. A concise 3-sentence application pitch based only on evidence in the resume

Target role: {job_title or "Not specified"}

RESUME:
{resume_text[:18000]}

JOB DESCRIPTION:
{job_description[:12000]}
"""
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                st.subheader("Your JobFit report")
                st.markdown(response.text or "The model returned an empty response.")
                st.download_button(
                    "Download report as Markdown",
                    data=(response.text or "").encode("utf-8"),
                    file_name="jobfit_report.md",
                    mime="text/markdown"
                )
                st.info("Privacy note: the resume and job description are sent to the Gemini API for analysis. Avoid uploading information you do not want processed by the provider.")
            except Exception as exc:
                st.error(f"Analysis failed: {exc}")
                st.caption("Check that your API key is valid and that the selected model is available to your account.")

st.divider()
st.caption("Built as a practical LLM application demo. The fit score is an approximate aid, not a guarantee of interview or hiring outcomes.")
