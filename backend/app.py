import os, uuid
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from backend.database import get_connection, init_db
from backend.resume_parser import extract_text, extract_email, extract_name
from backend.nlp_engine import extract_skills, skills_text
from backend.recommendation_engine import recommend_jobs

BASE=Path(__file__).resolve().parent.parent
FRONT=BASE/"frontend"
UPLOAD=Path(os.environ.get("DATA_DIR",BASE/"uploads"))/"uploads"
UPLOAD.mkdir(parents=True,exist_ok=True)
app=Flask(__name__); CORS(app); app.config["MAX_CONTENT_LENGTH"]=10*1024*1024

@app.get("/")
def home(): return send_from_directory(FRONT,"index.html")
@app.get("/<path:filename>")
def static_files(filename): return send_from_directory(FRONT,filename)
@app.get("/api/health")
def health(): return jsonify({"status":"running","service":"AI Resume Screening API"})

@app.post("/api/register")
def register():
    d=request.get_json(silent=True) or {}; name=str(d.get("name","")).strip(); email=str(d.get("email","")).strip().lower(); password=str(d.get("password","")); role=d.get("role","candidate")
    if not name or not email or not password or role not in ("candidate","recruiter"): return jsonify({"error":"Enter all fields and select a valid role."}),400
    try:
        with get_connection() as c: uid=c.execute("INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)",(name,email,password,role)).lastrowid
        return jsonify({"message":"Registration successful","user_id":uid})
    except Exception: return jsonify({"error":"Email already registered or invalid data."}),400

@app.post("/api/login")
def login():
    d=request.get_json(silent=True) or {}
    with get_connection() as c: u=c.execute("SELECT id,name,email,role FROM users WHERE email=? AND password=?",(str(d.get("email","")).lower(),str(d.get("password","")))).fetchone()
    if not u: return jsonify({"error":"Invalid email or password."}),401
    return jsonify({"message":"Login successful","user":dict(u)})

@app.post("/api/resumes")
def upload_resume():
    f=request.files.get("resume")
    if not f or not f.filename: return jsonify({"error":"Choose a PDF or DOCX resume."}),400
    name=secure_filename(f.filename)
    if "." not in name or name.rsplit(".",1)[1].lower() not in {"pdf","docx"}: return jsonify({"error":"Only PDF and DOCX files are supported."}),400
    path=UPLOAD/(uuid.uuid4().hex+"_"+name); f.save(path)
    try:
        text=extract_text(path)
        if not text.strip(): raise ValueError("No readable text found. Scanned PDFs require OCR.")
        skills=extract_skills(text); candidate=extract_name(text); email=extract_email(text); uid=request.form.get("user_id",type=int)
        with get_connection() as c: rid=c.execute("INSERT INTO resumes(user_id,filename,candidate_name,email,text,skills) VALUES(?,?,?,?,?,?)",(uid,name,candidate,email,text,skills_text(skills))).lastrowid
        return jsonify({"message":"Resume analyzed","resume_id":rid,"candidate_name":candidate,"email":email,"skills":skills})
    except Exception as e:
        path.unlink(missing_ok=True); return jsonify({"error":str(e)}),400

@app.post("/api/jobs")
def create_job():
    d=request.get_json(silent=True) or {}; title=str(d.get("title","")).strip(); company=str(d.get("company","")).strip(); desc=str(d.get("description","")).strip()
    if not title or not company or not desc: return jsonify({"error":"Title, company and description are required."}),400
    skills=extract_skills(desc)
    with get_connection() as c: jid=c.execute("INSERT INTO jobs(title,company,description,skills) VALUES(?,?,?,?)",(title,company,desc,skills_text(skills))).lastrowid
    return jsonify({"message":"Job created","job_id":jid,"skills":skills})

@app.get("/api/jobs")
def jobs():
    with get_connection() as c: rows=c.execute("SELECT id,title,company,description,skills,created_at FROM jobs ORDER BY id DESC").fetchall()
    return jsonify([dict(x) for x in rows])

@app.get("/api/recommend/<int:rid>")
def recommendations(rid):
    with get_connection() as c:
        resume=c.execute("SELECT * FROM resumes WHERE id=?",(rid,)).fetchone(); jobs=c.execute("SELECT * FROM jobs ORDER BY id DESC").fetchall()
    if not resume: return jsonify({"error":"Resume not found."}),404
    results=recommend_jobs(resume["text"],jobs)
    with get_connection() as c:
        for r in results: c.execute("INSERT INTO recommendations(resume_id,job_id,score,matched_skills,missing_skills) VALUES(?,?,?,?,?)",(rid,r["job_id"],r["score"],", ".join(r["matched_skills"]),", ".join(r["missing_skills"])))
    return jsonify({"resume_id":rid,"recommendations":results})

@app.get("/api/resumes")
def resumes():
    with get_connection() as c: rows=c.execute("SELECT id,user_id,filename,candidate_name,email,skills,created_at FROM resumes ORDER BY id DESC").fetchall()
    return jsonify([dict(x) for x in rows])
@app.get("/api/candidates")
def candidates():
    with get_connection() as c: rows=c.execute("SELECT id,candidate_name,email,skills,created_at FROM resumes ORDER BY id DESC").fetchall()
    return jsonify([dict(x) for x in rows])

with app.app_context(): init_db()
if __name__=="__main__": app.run(host="0.0.0.0",port=int(os.environ.get("PORT",5000)),debug=False)
