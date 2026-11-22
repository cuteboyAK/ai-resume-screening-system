# AI Resume Screening & Job Recommendation System

MCA project based on the supplied PDF: Flask REST backend, separate HTML/CSS/JavaScript frontend, SQLite, resume parsing and NLP matching.

## Features
- Candidate/recruiter registration
- PDF/DOCX resume text extraction
- Skill extraction using a built-in skills dictionary
- TF-IDF and cosine-similarity matching
- Ranked job recommendations and skill-gap analysis
- Job posting and recruiter candidate listing
- SQLite database with sample jobs

## Local run
Python 3.10+:
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Android: use GitHub/Render web interfaces for deployment; no local Python setup needed.
pip install -r requirements.txt
python -m backend.app
```
Open http://127.0.0.1:5000

## Render deployment
1. Upload the contents of this folder to a GitHub repository.
2. On Render choose New > Blueprint and connect the repository.
3. Render reads render.yaml; wait for deployment and open the generated onrender.com address.

The Flask app serves the frontend and API from one origin, so the frontend does not use localhost API addresses.

## Hosting/data warning
The SQLite file and uploaded resumes are stored in DATA_DIR (default: project/database). On hosts with an ephemeral filesystem, data may reset after restart/redeploy. For durable storage, attach a persistent disk and set DATA_DIR to its mount path, or use managed database/object storage. Free services may sleep when idle.

## Academic demo security note
This is not production-grade authentication. Passwords are stored as plain text and endpoints are not access-controlled. Use only dummy/test accounts and sample resumes; do not upload sensitive real personal data. Production use requires password hashing, sessions/tokens, authorization, and privacy/security controls.
