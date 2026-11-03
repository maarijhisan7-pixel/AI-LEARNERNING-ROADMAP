import streamlit as st
from google import genai
from pypdf import PdfReader
from docx import Document

st.set_page_config(page_title="ATS Resume Analyzer", page_icon="📄")
st.title("📄 ATS Resume Analyzer")
st.write("Upload your resume and get an AI-powered ATS score and improvement suggestions.")

# Read Gemini API key from Streamlit secrets
api_key = st.secrets.get("GEMINI_API_KEY", "")

# Upload resume
file = st.file_uploader("Upload your resume", type=["pdf", "docx", "txt"])

# Optional job description
job_description = st.text_area("Paste the job description (optional)")

if st.button("Analyze Resume"):
    if not file:
        st.warning("Please upload your resume first.")
    elif not api_key:
        st.error("Gemini API key is missing. Add it to .streamlit/secrets.toml.")
    else:
        try:
            # Extract text from the uploaded file
            if file.name.endswith(".pdf"):
                reader = PdfReader(file)
                resume_text = "\n".join(
                    page.extract_text() or "" for page in reader.pages
                )
            elif file.name.endswith(".docx"):
                document = Document(file)
                resume_text = "\n".join(p.text for p in document.paragraphs)
            else:
                resume_text = file.getvalue().decode("utf-8", errors="ignore")

            if not resume_text.strip():
                st.error("No text found. Please upload a readable, text-based resume.")
            else:
                # Send resume to Gemini
                client = genai.Client(api_key=api_key)

                prompt = f"""
                You are an ATS resume reviewer.

                Analyze this resume and provide:
                1. An estimated ATS score out of 100.
                2. Resume strengths.
                3. Resume weaknesses.
                4. Missing keywords, if a job description is provided.
                5. Clear suggestions to improve the resume.

                Do not invent qualifications or experience.
                Explain that the score is only an estimate, not an official ATS result.

                JOB DESCRIPTION:
                {job_description if job_description else "Not provided"}

                RESUME:
                {resume_text[:30000]}
                """

                with st.spinner("Gemini is analyzing your resume..."):
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt
                    )

                st.subheader("Resume Analysis")
                st.markdown(response.text)

        except Exception as error:
            st.error(f"Something went wrong: {error}")
