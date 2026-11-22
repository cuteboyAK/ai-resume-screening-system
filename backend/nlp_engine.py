import re
SKILLS = {"python","java","javascript","typescript","c","c++","c#","sql","mysql","postgresql","mongodb","oracle","html","css","bootstrap","react","angular","vue","node.js","flask","fastapi","django","machine learning","deep learning","artificial intelligence","nlp","natural language processing","computer vision","tensorflow","pytorch","scikit-learn","pandas","numpy","opencv","git","github","docker","aws","azure","gcp","rest api","data analysis","data visualization","power bi","tableau","excel","communication","leadership","problem solving","teamwork","project management","linux","cybersecurity","networking","android","kotlin","figma"}
def normalize_text(text):
    return re.sub(r"[^a-z0-9+#.\\- ]"," ",re.sub(r"\\s+"," ",(text or "").lower())).strip()
def extract_skills(text):
    t=normalize_text(text); found=set()
    for s in sorted(SKILLS,key=len,reverse=True):
        if re.search(r"(?<![a-z0-9])"+re.escape(s)+r"(?![a-z0-9])",t): found.add(s)
    return sorted(found)
def skills_text(skills): return ", ".join(skills)
