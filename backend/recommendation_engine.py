from backend.matching_engine import calculate_match
def recommend_jobs(resume_text,jobs):
    out=[]
    for job in jobs:
        out.append({"job_id":job["id"],"title":job["title"],"company":job["company"],**calculate_match(resume_text,job["description"])})
    return sorted(out,key=lambda x:x["score"],reverse=True)
