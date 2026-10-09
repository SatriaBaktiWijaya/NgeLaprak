import os
import re
import shutil
import docx
import pypdf

def extract_text_from_pdf(pdf_path, max_pages=None):
    text_pages = []
    try:
        reader = pypdf.PdfReader(pdf_path)
        pages = reader.pages if max_pages is None else reader.pages[:max_pages]
        for page in pages:
            text_pages.append(page.extract_text() or "")
    except Exception:
        pass
    return "\n".join(text_pages)

def extract_text_from_docx(docx_path):
    try:
        doc = docx.Document(docx_path)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    except Exception:
        return ""

def extract_text_from_file(file_path, max_chars=10000):
    if not os.path.exists(file_path):
        return ""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path, max_pages=5)[:max_chars]
    elif ext == ".docx":
        return extract_text_from_docx(file_path)[:max_chars]
    else:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()[:max_chars]
        except Exception:
            return ""

def parse_pascal_case(s):
    """Converts PascalCase or camelCase to words (e.g. SatriaBaktiWijaya -> Satria Bakti Wijaya)"""
    return re.sub(r'([a-z])([A-Z])', r'\1 \2', s).strip()

def classify_file(filename, file_path=None):
    """
    Categorizes a file into:
    - 'modul'     : Lab guides, modules, jobsheets
    - 'tp'        : Pre-lab questions / Tugas Pendahuluan
    - 'laprak'    : Past lab reports, report templates
    - 'code'      : Source code (*.cpp, *.java, *.py, *.sql, etc.)
    - 'screenshot': Images / screenshots (*.png, *.jpg, etc.)
    - 'ignore'    : Repo meta files (.git, package.json, etc.)
    - 'misc'      : Other files
    """
    fn = filename.lower()
    ext = os.path.splitext(fn)[1]

    # Ignore meta files and build directories
    if fn in ['.git', '.gitignore', '.gitattributes', 'package.json', 'package-lock.json',
              'readme.md', 'license', 'install.ps1', 'install.sh', '.env', 'yarn.lock']:
        return 'ignore'

    # Check images / screenshots
    if ext in ['.png', '.jpg', '.jpeg', '.bmp', '.webp', '.gif', '.svg']:
        return 'screenshot'

    # Check source code & project files
    if ext in ['.cpp', '.c', '.h', '.hpp', '.java', '.py', '.sql', '.html', '.css',
               '.js', '.ts', '.php', '.cs', '.go', '.rs', '.cbp', '.vcxproj', '.xml']:
        if fn != 'pom.xml': # regular code or project
            return 'code'
        return 'code'

    # Check for TP (Tugas Pendahuluan / Pre-lab)
    if re.search(r'\btp\b|tugas[\s_-]*pendahuluan|prelab', fn):
        return 'tp'

    # Check for Laprak / Template / Past reports
    # Matches laprak, laporan, template, contoh, or course code patterns like STRUKTUR-DATA_MOD-2_...
    if re.search(r'laprak|laporan|template|contoh|[a-z0-9_\-]+_mod[-_]?\d+_', fn):
        return 'laprak'

    # Check for Modul
    if re.search(r'modul|module|materi|jobsheet|panduan|labguide', fn):
        return 'modul'

    # Deep check inside PDF / DOCX if name is ambiguous
    if ext in ['.pdf', '.docx'] and file_path and os.path.exists(file_path):
        preview = extract_text_from_file(file_path, max_chars=1500).lower()
        if 'laporan praktikum' in preview or 'nama (nim)' in preview or 'asisten praktikum' in preview:
            return 'laprak'
        if 'tugas pendahuluan' in preview:
            return 'tp'
        if 'modul' in preview or 'tujuan praktikum' in preview:
            return 'modul'

    return 'misc'

def analyze_modul(modul_path):
    """
    Extracts structured info from a lab module file (PDF or DOCX).
    Returns dict: title, tujuan, tools, dasar_teori, tasks
    """
    raw_text = extract_text_from_file(modul_path, max_chars=30000)

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

def extract_metadata_from_pdf(pdf_path):
    """
    Extracts cover metadata, student identity, course, and assistants from a past PDF report.
    """
    meta = {
        "student_name": "",
        "student_nim": "",
        "course": "",
        "module_number": None,
        "asisten": [],
        "prodi": "",
        "fakultas": "",
        "kampus": "",
        "tahun": "2026"
    }
    
    fname = os.path.basename(pdf_path)
    # Check NIM and Name in filename
    m_nim_fn = re.search(r'(\d{8,14})', fname)
    if m_nim_fn:
        meta["student_nim"] = m_nim_fn.group(1)
        m_name_fn = re.search(r'\d{8,14}_([A-Za-z]+)', fname)
        if m_name_fn:
            meta["student_name"] = parse_pascal_case(m_name_fn.group(1))

    # Check course in filename
    m_course_fn = re.search(r'^([A-Za-z0-9_\-]+?)_MOD[-_]?(\d+)', fname, re.IGNORECASE)
    if m_course_fn:
        meta["course"] = m_course_fn.group(1).replace('-', ' ').title()
        meta["module_number"] = int(m_course_fn.group(2))

    text = extract_text_from_pdf(pdf_path, max_pages=3)
    if not text:
        return meta

    # Name from text
    m_name = re.search(r'Nama\s*:\s*([^\n\r]+)', text)
    if m_name:
        meta["student_name"] = m_name.group(1).strip()

    # NIM from text
    m_nim = re.search(r'(?:NIM|Nama\s*\(NIM\))\s*:\s*(\d{8,14})', text)
    if m_nim:
        meta["student_nim"] = m_nim.group(1).strip()

    # Course from text if empty
    if not meta["course"]:
        m_c = re.search(r'(STRUKTUR\s+DATA|ANALISIS\s+DAN\s+PERANCANGAN\s+PERANGKAT\s+LUNAK|ADPL|PEMROGRAMAN\s+BERORIENTASI\s+OBJEK|PBO|BASIS\s+DATA|JARINGAN\s+KOMPUTER)', text, re.IGNORECASE)
        if m_c:
            meta["course"] = m_c.group(1).title()

    # Asisten
    m_asisten = re.search(r'Asisten\s+Praktikum\s*:\s*(.*?)(?=(?:Laboratorium|Program|Fakultas|\n\n\n|$))', text, re.IGNORECASE | re.DOTALL)
    if m_asisten:
        lines = [l.strip() for l in m_asisten.group(1).splitlines() if l.strip()]
        meta["asisten"] = lines

    # Institution info
    for line in text.splitlines()[:50]:
        l = line.strip()
        if "PROGRAM STUDI" in l.upper():
            meta["prodi"] = l
        elif "FAKULTAS" in l.upper():
            meta["fakultas"] = l
        elif "UNIVERSITAS" in l.upper() or "TELKOM UNIVERSITY" in l.upper():
            meta["kampus"] = l
        elif re.match(r'^(202[4-9])$', l):
            meta["tahun"] = l

    return meta

def analyze_template_docx(template_path):
    """
    Extracts cover metadata, typography, and logo from an existing student laprak template.
    """
    meta = {
        "paragraphs": 0,
        "student_name": "",
        "student_nim": "",
        "course": "",
        "module_number": None,
        "asisten": [],
        "prodi": "",
        "fakultas": "",
        "kampus": "",
        "tahun": "2026",
        "has_logo": False,
        "margins": {}
    }

    try:
        doc = docx.Document(template_path)
    except Exception:
        fname = os.path.basename(template_path)
        m_nim = re.search(r'(\d{8,14})', fname)
        if m_nim:
            meta["student_nim"] = m_nim.group(1)
            m_name = re.search(r'\d{8,14}_([A-Za-z]+)', fname)
            if m_name:
                meta["student_name"] = parse_pascal_case(m_name.group(1))
        m_course = re.search(r'^([A-Za-z0-9_\-]+?)_MOD[-_]?(\d+)', fname, re.IGNORECASE)
        if m_course:
            meta["course"] = m_course.group(1).replace('-', ' ').title()
            meta["module_number"] = int(m_course.group(2))
        return meta

    meta["paragraphs"] = len(doc.paragraphs)

    if doc.sections:
        s = doc.sections[0]
        meta["margins"] = {
            "top": s.top_margin.pt,
            "bottom": s.bottom_margin.pt,
            "left": s.left_margin.pt,
            "right": s.right_margin.pt
        }

    for p in doc.paragraphs[:35]:
        t = p.text.strip()
        if not t: continue
        if "Nama :" in t or "Nama:" in t:
            meta["student_name"] = t.split(":", 1)[1].strip()
        elif "NIM" in t:
            m_nim = re.search(r'\d{8,14}', t)
            if m_nim:
                meta["student_nim"] = m_nim.group(0)
        elif "PROGRAM STUDI" in t.upper():
            meta["prodi"] = t
        elif "FAKULTAS" in t.upper():
            meta["fakultas"] = t
        elif "UNIVERSITAS" in t.upper() or "UNIVERSITY" in t.upper():
            meta["kampus"] = t
        elif re.match(r'^(202[4-9])$', t):
            meta["tahun"] = t

    # Check for embedded images (logo)
    for rel in doc.part.related_parts.values():
        if "image" in rel.content_type:
            meta["has_logo"] = True
            break

    # Fallback to filename hints if fields are still empty
    fname = os.path.basename(template_path)
    if not meta["student_nim"]:
        m_nim = re.search(r'(\d{8,14})', fname)
        if m_nim:
            meta["student_nim"] = m_nim.group(1)
    if not meta["student_name"]:
        m_name = re.search(r'\d{8,14}_([A-Za-z]+)', fname)
        if m_name:
            meta["student_name"] = parse_pascal_case(m_name.group(1))
    if not meta["course"]:
        m_course = re.search(r'^([A-Za-z0-9_\-]+?)_MOD[-_]?(\d+)', fname, re.IGNORECASE)
        if m_course:
            meta["course"] = m_course.group(1).replace('-', ' ').title()
            meta["module_number"] = int(m_course.group(2))

    return meta

def infer_workspace_context(workspace_dir):
    """
    Autonomously investigates the workspace to deduce:
    - Course name (e.g. Struktur Data, ADPL, PBO)
    - Target module number & title (e.g. Modul 3: Abstract Data Type)
    - Student identity (Name, NIM, Kampus, Asisten)
    - Programming language & IDE styling (C++ Code::Blocks, Java NetBeans, SQL DBeaver, etc.)
    - Existing files categorized into Modul, Laprak, Code, Screenshots
    - Suggested output file name (e.g. STRUKTUR-DATA_MOD-3_109092500017_SatriaBaktiWijaya.docx)
    """
    workspace_dir = os.path.abspath(workspace_dir)

    categories = {
        "modul": [],
        "tp": [],
        "laprak": [],
        "code": [],
        "screenshot": [],
        "misc": []
    }
    loose_files = []

    # 1. Gather all files in workspace (root & immediate subfolders)
    for root, dirs, files in os.walk(workspace_dir):
        # Skip hidden folders and venv/node_modules
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'venv', '__pycache__']]
        for f in files:
            fp = os.path.join(root, f)
            cat = classify_file(f, fp)
            if cat in categories:
                categories[cat].append(fp)
            if root == workspace_dir and cat not in ['ignore', 'misc']:
                loose_files.append(fp)

    # 2. Deduce Target Module Number & Title
    target_module_number = None
    target_module_title = ""
    course_name = ""

    # Priority A: Check modul files
    for m_path in categories["modul"]:
        fn = os.path.basename(m_path)
        m_num = re.search(r'Modul\s*[-_]?\s*(\d+)', fn, re.IGNORECASE)
        if m_num:
            target_module_number = int(m_num.group(1))
            mod_info = analyze_modul(m_path)
            if mod_info.get("title"):
                target_module_title = mod_info["title"]
            break

    # Priority B: Check TP files if module number still unknown
    if target_module_number is None:
        for tp_path in categories["tp"]:
            fn = os.path.basename(tp_path)
            m_num = re.search(r'Modul\s*[-_]?\s*(\d+)', fn, re.IGNORECASE)
            if m_num:
                target_module_number = int(m_num.group(1))
                break

    # 3. Deduce Student Identity & Format from past Laprak / Template
    student_name = ""
    student_nim = ""
    asisten = []
    prodi = ""
    fakultas = ""
    kampus = ""
    reference_laprak_name = ""

    for l_path in categories["laprak"]:
        fn = os.path.basename(l_path)
        if fn.lower().endswith(".docx"):
            meta = analyze_template_docx(l_path)
            if meta.get("student_name") and not student_name:
                student_name = meta["student_name"]
            if meta.get("student_nim") and not student_nim:
                student_nim = meta["student_nim"]
            if meta.get("prodi"): prodi = meta["prodi"]
            if meta.get("fakultas"): fakultas = meta["fakultas"]
            if meta.get("kampus"): kampus = meta["kampus"]
            reference_laprak_name = fn
        elif fn.lower().endswith(".pdf"):
            meta = extract_metadata_from_pdf(l_path)
            if meta.get("student_name") and not student_name:
                student_name = meta["student_name"]
            if meta.get("student_nim") and not student_nim:
                student_nim = meta["student_nim"]
            if meta.get("course") and not course_name:
                course_name = meta["course"]
            if meta.get("asisten") and not asisten:
                asisten = meta["asisten"]
            if meta.get("prodi"): prodi = meta["prodi"]
            if meta.get("fakultas"): fakultas = meta["fakultas"]
            if meta.get("kampus"): kampus = meta["kampus"]
            reference_laprak_name = fn

    # Fallback course from modul / tp text if still empty
    if not course_name:
        for check_path in categories["modul"] + categories["tp"]:
            preview = extract_text_from_file(check_path, max_chars=2000)
            m_c = re.search(r'(STRUKTUR\s+DATA|ANALISIS\s+DAN\s+PERANCANGAN\s+PERANGKAT\s+LUNAK|ADPL|PEMROGRAMAN\s+BERORIENTASI\s+OBJEK|PBO|BASIS\s+DATA|JARINGAN\s+KOMPUTER)', preview, re.IGNORECASE)
            if m_c:
                course_name = m_c.group(1).title()
                break

    # 4. Deduce Programming Language & Preferred IDE
    language = "General / Text"
    recommended_ide = "vscode"

    # Check existing code files first
    code_exts = [os.path.splitext(cp)[1].lower() for cp in categories["code"]]
    if any(e in ['.cpp', '.c', '.h', '.hpp', '.cbp'] for e in code_exts):
        language = "C++"
        recommended_ide = "codeblocks"
    elif any(e == '.java' for e in code_exts):
        language = "Java"
        recommended_ide = "netbeans"
    elif any(e == '.sql' for e in code_exts):
        language = "SQL"
        recommended_ide = "database"
    elif any(e == '.py' for e in code_exts):
        language = "Python"
        recommended_ide = "vscode"
    elif any(e in ['.html', '.css', '.js', '.php'] for e in code_exts):
        language = "Web / PHP"
        recommended_ide = "vscode"
    else:
        # Infer from Modul & TP content
        combined_text = ""
        for p in categories["modul"] + categories["tp"]:
            combined_text += " " + extract_text_from_file(p, max_chars=10000).lower()

        if any(k in combined_text for k in ['c++', 'code::blocks', 'codeblocks', 'struct ', '#include <iostream>', 'cin >>', 'cout <<']):
            language = "C++"
            recommended_ide = "codeblocks"
        elif any(k in combined_text for k in ['netbeans', 'jframe', 'swing', 'public static void main', 'system.out.println', 'java ']):
            language = "Java"
            recommended_ide = "netbeans"
        elif any(k in combined_text for k in ['dbeaver', 'create table', 'select * from', 'insert into', 'sql ']):
            language = "SQL"
            recommended_ide = "database"
        elif any(k in combined_text for k in ['python', 'def ', 'pip install']):
            language = "Python"
            recommended_ide = "vscode"

    # 5. Formulate Suggested Target Laprak Filename
    suggested_filename = ""
    if reference_laprak_name and target_module_number is not None:
        # Pattern substitution: MOD-2 -> MOD-3
        base_name = os.path.splitext(reference_laprak_name)[0]
        ext = ".docx"
        new_base = re.sub(r'MOD[-_]?\d+', f'MOD-{target_module_number}', base_name, flags=re.IGNORECASE)
        suggested_filename = f"{new_base}{ext}"
    elif course_name and target_module_number and student_nim:
        clean_course = course_name.upper().replace(' ', '-')
        clean_name = student_name.replace(' ', '')
        suggested_filename = f"{clean_course}_MOD-{target_module_number}_{student_nim}_{clean_name}.docx"

    return {
        "workspace_dir": workspace_dir,
        "course_name": course_name or "Mata Kuliah Praktikum",
        "target_module_number": target_module_number,
        "target_module_title": target_module_title or (f"Modul {target_module_number}" if target_module_number else "Modul"),
        "student_name": student_name,
        "student_nim": student_nim,
        "asisten": asisten,
        "prodi": prodi,
        "fakultas": fakultas,
        "kampus": kampus,
        "language": language,
        "recommended_ide": recommended_ide,
        "suggested_filename": suggested_filename,
        "has_code": len(categories["code"]) > 0,
        "code_files_count": len(categories["code"]),
        "needs_scaffold": len(loose_files) > 0,
        "loose_files": loose_files,
        "categories": categories
    }

def organize_workspace(workspace_dir, dry_run=False):
    """
    Autonomously scaffolds the workspace and organizes loose files in the root folder into:
    - Modul/               (Modul guides, TP)
    - Laprak/              (Reference reports, templates, and final reports)
    - Laprak/screenshots/  (Manual screenshots)
    - Code/                (Source code & implementation)
    
    Returns a dict with organized files and inferred workspace context.
    """
    workspace_dir = os.path.abspath(workspace_dir)

    modul_dir = os.path.join(workspace_dir, "Modul")
    laprak_dir = os.path.join(workspace_dir, "Laprak")
    ss_dir = os.path.join(laprak_dir, "screenshots")
    code_dir = os.path.join(workspace_dir, "Code")

    moved_files = []
    created_dirs = []

    # Get root entries
    entries = os.listdir(workspace_dir)
    loose_items = []
    for item in entries:
        fp = os.path.join(workspace_dir, item)
        if os.path.isfile(fp):
            cat = classify_file(item, fp)
            if cat not in ['ignore', 'misc']:
                loose_items.append((item, fp, cat))

    # If there are files to organize, ensure directories exist
    if loose_items and not dry_run:
        for d in [modul_dir, laprak_dir, ss_dir, code_dir]:
            if not os.path.exists(d):
                os.makedirs(d, exist_ok=True)
                created_dirs.append(d)

    # Move files to respective folders
    for item, fp, cat in loose_items:
        dest_folder = None
        if cat in ['modul', 'tp']:
            dest_folder = modul_dir
        elif cat == 'laprak':
            dest_folder = laprak_dir
        elif cat == 'code':
            dest_folder = code_dir
        elif cat == 'screenshot':
            dest_folder = ss_dir

        if dest_folder:
            dest_path = os.path.join(dest_folder, item)
            # Avoid overwriting identical file
            if not dry_run:
                if os.path.exists(dest_path):
                    base, ext = os.path.splitext(item)
                    dest_path = os.path.join(dest_folder, f"{base}_new{ext}")
                shutil.move(fp, dest_path)
            
            moved_files.append({
                "filename": item,
                "category": cat,
                "source": fp,
                "destination": dest_path
            })

    # Ensure Code/ and Laprak/screenshots/ exist even if no files were moved there
    if not dry_run and loose_items:
        os.makedirs(code_dir, exist_ok=True)
        os.makedirs(ss_dir, exist_ok=True)

    # Re-infer context after organizing
    context = infer_workspace_context(workspace_dir)

    return {
        "workspace_dir": workspace_dir,
        "scaffolded": len(moved_files) > 0,
        "created_dirs": created_dirs,
        "moved_files": moved_files,
        "context": context
    }
