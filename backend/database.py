import os, sqlite3
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.environ.get("DATA_DIR", BASE / "database"))
DATA_DIR.mkdir(parents=True, exist_ok=True)
DATABASE = DATA_DIR / "resume_system.db"

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as c:
        c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, password TEXT NOT NULL, role TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        c.execute("CREATE TABLE IF NOT EXISTS resumes (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, filename TEXT NOT NULL, candidate_name TEXT, email TEXT, text TEXT NOT NULL, skills TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        c.execute("CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY AUTOINCREMENT, recruiter_id INTEGER, title TEXT NOT NULL, company TEXT NOT NULL, description TEXT NOT NULL, skills TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        c.execute("CREATE TABLE IF NOT EXISTS recommendations (id INTEGER PRIMARY KEY AUTOINCREMENT, resume_id INTEGER NOT NULL, job_id INTEGER NOT NULL, score REAL NOT NULL, matched_skills TEXT, missing_skills TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        if c.execute("SELECT COUNT(*) FROM jobs").fetchone()[0] == 0:
            c.executemany("INSERT INTO jobs(title,company,description,skills) VALUES(?,?,?,?)", [
                ("Python Developer","DemoTech","Python Flask REST API SQL Git problem solving",""),
                ("Data Analyst","InsightWorks","Python SQL Excel pandas numpy data analysis data visualization",""),
                ("Frontend Developer","WebNova","HTML CSS JavaScript React Git responsive web development","")
            ])
