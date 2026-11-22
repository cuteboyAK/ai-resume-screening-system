import re
from pathlib import Path
from pypdf import PdfReader
from docx import Document

def extract_text(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        return "\\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages)
    if path.suffix.lower() == ".docx":
        return "\\n".join(p.text for p in Document(str(path)).paragraphs)
    raise ValueError("Only PDF and DOCX resumes are supported.")

def extract_email(text):
    m = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}", text)
    return m.group(0) if m else None

def extract_name(text):
    for line in [x.strip() for x in text.splitlines() if x.strip()][:10]:
        w = line.split()
        if "@" not in line and 2 <= len(w) <= 4 and all(re.match(r"^[A-Za-z.\\-]+$", x) for x in w):
            return line
    return None
