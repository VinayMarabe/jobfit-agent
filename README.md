# JobFit Agent 🎯

A small LLM-powered career tool that compares a resume with a job description and generates an evidence-based fit report.

## Features
- PDF resume upload or pasted resume text
- Job description comparison
- Approximate fit score with an explicit caveat
- Evidence-backed strengths and gaps
- Prioritized resume improvements
- ATS keyword suggestions with a truthfulness check
- Interview questions and a concise application pitch
- Downloadable Markdown report

## Run locally

Requires Python 3.10+.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

Enter your Gemini API key in the app sidebar. Get a key from [Google AI Studio](https://aistudio.google.com/).

## Deploy free on Streamlit Community Cloud

1. Create a **public** GitHub repository named `jobfit-agent`.
2. Upload `app.py`, `requirements.txt`, `.gitignore`, and this README.
3. Visit [Streamlit Community Cloud](https://share.streamlit.io/) and sign in with GitHub.
4. Select **Create app**, choose your repository, branch `main`, and main file `app.py`.
5. Deploy. Streamlit will provide a public `streamlit.app` URL.
6. Open the app URL and enter your Gemini API key in the sidebar.

Do not commit API keys or resumes to GitHub. The app sends resume/job-description text to the Gemini API when the user clicks Analyze; disclose this to users.

## Limitations
The fit score is a heuristic, not a validated hiring prediction. The model can make mistakes, so verify every suggested claim and only include skills or experience that are true.
