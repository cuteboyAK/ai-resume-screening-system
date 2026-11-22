from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from backend.nlp_engine import normalize_text, extract_skills

def text_similarity(a,b):
    a,b=normalize_text(a),normalize_text(b)
    if not a or not b: return 0.0
    try:
        m=TfidfVectorizer(stop_words="english",ngram_range=(1,2)).fit_transform([a,b])
        return float(cosine_similarity(m[0:1],m[1:2])[0][0])
    except ValueError: return 0.0

def calculate_match(resume_text,job_text):
    rs=set(extract_skills(resume_text)); js=set(extract_skills(job_text))
    matched=sorted(rs & js); missing=sorted(js-rs)
    skill=len(matched)/len(js) if js else 0.0
    sim=text_similarity(resume_text,job_text)
    return {"score":round((.60*skill+.40*sim)*100,2),"skill_score":round(skill*100,2),"text_similarity":round(sim*100,2),"matched_skills":matched,"missing_skills":missing}
