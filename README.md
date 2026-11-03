# ATS Resume Analyzer

A simple AI-powered resume analyzer using Streamlit and Gemini Flash.

## Features
- Upload PDF, DOCX, or TXT resume.
- Get estimated ATS score.
- Identify resume weaknesses.
- Get improvement suggestions.
- Compare resume with job description.

## Installation

pip install -r requirements.txt

## API Key

Create a Gemini API key:
https://aistudio.google.com/apikey

Create .streamlit/secrets.toml:

GEMINI_API_KEY = "your-api-key"

## Run Application

streamlit run app.py

## Deployment

1. Push code to GitHub.
2. Open Streamlit Community Cloud.
3. Connect your GitHub repository.
4. Select app.py.
5. Add GEMINI_API_KEY in Secrets.
6. Click Deploy.
