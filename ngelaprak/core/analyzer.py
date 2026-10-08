import os
import re
import docx
import pypdf

def extract_text_from_pdf(pdf_path):
    text_pages = []
    reader = pypdf.PdfReader(pdf_path)
    for page in reader.pages:
        text_pages.append(page.extract_text() or "")
    return "\n".join(text_pages)

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

def analyze_modul(modul_path):
    """
    Extracts structured info from a lab module file (PDF or DOCX).
    Returns dict: title, tujuan, tools, dasar_teori, tasks
    """
    if modul_path.lower().endswith(".pdf"):
        raw_text = extract_text_from_pdf(modul_path)
    elif modul_path.lower().endswith(".docx"):
        raw_text = extract_text_from_docx(modul_path)
    else:
        with open(modul_path, "r", encoding="utf-8", errors="ignore") as f:
            raw_text = f.read()

    info = {
        "title": "",
        "tujuan": [],
        "tools": "",
        "dasar_teori": "",
        "raw_text_length": len(raw_text)
    }

    # Extract title
    match_title = re.search(r"Modul\s+\d+[:\s]+([^\n\r]+)", raw_text, re.IGNORECASE)
    if match_title:
        info["title"] = match_title.group(0).strip()

    # Extract Tujuan
    match_tujuan = re.search(r"Tujuan\s+Praktikum[:\s]*(.*?)(?=(?:dasar\s+teori|alat|tool|\d+\.\d+|$))", raw_text, re.IGNORECASE | re.DOTALL)
    if match_tujuan:
        lines = [l.strip() for l in match_tujuan.group(1).splitlines() if l.strip()]
        info["tujuan"] = [l for l in lines if re.match(r"^\d+[\.\)]", l) or len(l) > 10]

    return info

def analyze_template_docx(template_path):
    """
    Extracts cover metadata, typography, and logo from an existing student laprak template.
    """
    doc = docx.Document(template_path)
    meta = {
        "paragraphs": len(doc.paragraphs),
        "student_name": "",
        "student_nim": "",
        "asisten": [],
        "prodi": "",
        "fakultas": "",
        "kampus": "",
        "tahun": "2026",
        "has_logo": False,
        "margins": {}
    }

    if doc.sections:
        s = doc.sections[0]
        meta["margins"] = {
            "top": s.top_margin.pt,
            "bottom": s.bottom_margin.pt,
            "left": s.left_margin.pt,
            "right": s.right_margin.pt
        }

    for p in doc.paragraphs[:30]:
        t = p.text.strip()
        if not t: continue
        if "Nama :" in t or "Nama:" in t:
            meta["student_name"] = t
        elif "NIM" in t:
            meta["student_nim"] = t
        elif "Asisten" in t:
            pass
        elif "PROGRAM STUDI" in t:
            meta["prodi"] = t
        elif "FAKULTAS" in t:
            meta["fakultas"] = t
        elif "UNIVERSITAS" in t or "UNIVERSITY" in t:
            meta["kampus"] = t

    # Check for embedded images (logo)
    for rel in doc.part.related_parts.values():
        if "image" in rel.content_type:
            meta["has_logo"] = True
            break

    return meta
