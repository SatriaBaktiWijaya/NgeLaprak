import os
import subprocess
import html
import re
from PIL import Image, ImageChops

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

CPP_KEYWORDS = {
    "int", "float", "double", "char", "bool", "void", "long", "short",
    "struct", "class", "public", "private", "protected", "virtual",
    "return", "using", "namespace", "include", "typedef", "sizeof",
    "if", "else", "for", "while", "do", "switch", "case", "break", "continue",
    "new", "delete", "nullptr", "NULL", "const", "static", "inline", "size_t",
    "true", "false"
}

CPP_STD_IDENTIFIERS = {
    "std", "vector", "string", "cout", "cin", "endl", "cerr", "pair",
    "make_pair", "map", "set", "list", "queue", "stack", "deque",
    "empty", "size", "begin", "end", "push_back", "pop_back", "clear",
    "length", "c_str", "substr", "find", "getline"
}

CPP_OPERATORS = {
    "&lt;&lt;", "&gt;&gt;", "&lt;=", "&gt;=", "==", "!=", "++", "--",
    "+=", "-=", "*=", "/=", "&amp;&amp;", "||",
    "=", "+", "-", "*", "/", "&lt;", "&gt;", "!", "&amp;", "|", "%"
}

def highlight_codeblocks_cpp(line_text):
    if not line_text.strip():
        return "&nbsp;"
        
    esc = html.escape(line_text)
    stripped = esc.strip()
    
    def safe_space(s):
        return s.replace(" ", "&nbsp;").replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
    
    # 1. Comments (Code::Blocks default: slate periwinkle blue #8890b0)
    if stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*"):
        c_idx = -1
        for marker in ["//", "/*", "*"]:
            idx = esc.find(marker)
            if idx != -1 and (c_idx == -1 or idx < c_idx):
                c_idx = idx
        if c_idx != -1 and esc[:c_idx].strip() == "":
            pre = safe_space(esc[:c_idx])
            comment = f'<span class="cb-comment">{safe_space(esc[c_idx:])}</span>'
            return pre + comment

    # 2. Preprocessor Directives (#include, #define, etc.)
    if stripped.startswith("#"):
        # For #define, highlight macro name green and numbers magenta
        if stripped.startswith("#define"):
            parts = re.split(r'(\b\d+(?:\.\d+)?\b)', esc)
            out = []
            for p in parts:
                if re.match(r'^\d+(?:\.\d+)?$', p):
                    out.append(f'<span class="cb-num">{safe_space(p)}</span>')
                else:
                    out.append(f'<span class="cb-prep">{safe_space(p)}</span>')
            return "".join(out)
        return f'<span class="cb-prep">{safe_space(esc)}</span>'
        
    # 3. Tokenize strings, numbers, operators, words
    token_pattern = r'(&quot;.*?&quot;|\'.*?\'|\b\d+(?:\.\d+)?\b|&lt;&lt;|&gt;&gt;|&lt;=|&gt;=|==|!=|\+\+|--|\+=|-=|\*=|/=|&amp;&amp;|\|\||\b\w+\b|[^\w\s])'
    tokens = re.split(token_pattern, esc)
    out = []
    
    for tok in tokens:
        if not tok:
            continue
        # String literal (Code::Blocks: Blue #0000ff)
        if tok.startswith('&quot;') and tok.endswith('&quot;'):
            out.append(f'<span class="cb-string">{safe_space(tok)}</span>')
        # Char literal (Code::Blocks: Blue #0000ff)
        elif tok.startswith("'") and tok.endswith("'"):
            out.append(f'<span class="cb-string">{safe_space(tok)}</span>')
        # Numbers / floats (Code::Blocks: Magenta #f000f0)
        elif re.match(r'^\d+(?:\.\d+)?$', tok):
            out.append(f'<span class="cb-num">{safe_space(tok)}</span>')
        # Keywords (Code::Blocks: Bold Dark Blue #0000a0)
        elif tok in CPP_KEYWORDS:
            out.append(f'<span class="cb-kw">{safe_space(tok)}</span>')
        # Standard library types & functions (Code::Blocks: Bold Green #00a000)
        elif tok in CPP_STD_IDENTIFIERS:
            out.append(f'<span class="cb-std">{safe_space(tok)}</span>')
        # Operators (Code::Blocks: Red #ff0000)
        elif tok in CPP_OPERATORS:
            out.append(f'<span class="cb-op">{safe_space(tok)}</span>')
        else:
            out.append(safe_space(tok))
            
    return "".join(out)

def render_codeblocks_code(code_text, start_line=1, end_line=None, out_path="codeblocks_shot.png", with_cursor=True, author_tag=None):
    """
    Renders an authentic Code::Blocks editor snippet (C/C++).
    Faithfully replicates:
    - Slate periwinkle comments (#8890b0)
    - Bold navy keywords (#0000a0)
    - Bold green std identifiers (#00a000)
    - Bright blue string literals (#0000ff)
    - Magenta numbers & floats (#f000f0)
    - Red operators (#ff0000)
    - Green preprocessor (#00a000)
    - Signature lime-green modification bar (#00e000)
    - Fold box margin with connecting guide lines
    - Authentic Scintilla editor fonts and layout
    """
    out_path = os.path.abspath(out_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    if author_tag and start_line == 1 and not code_text.strip().startswith("//"):
        code_text = f"// @author {author_tag}\n" + code_text

    all_lines = code_text.splitlines()
    if end_line is None or end_line > len(all_lines):
        end_line = len(all_lines)
        
    slice_lines = all_lines[start_line - 1 : end_line]
    num_lines = len(slice_lines)
    
    gutter_rows = []
    code_rows = []
    
    for i, line in enumerate(slice_lines):
        ln = start_line + i
        raw = line.strip()
        has_fold = ("{" in raw or raw.startswith("/*") or raw.startswith("struct ") or raw.startswith("class ") or (("(" in raw and ")" in raw and "{" in raw)))
        fold_elem = '<span class="cb-fold-box">-</span>' if has_fold else '<span class="cb-fold-guide"></span>'
        
        gutter_rows.append(f'<div class="cb-gutter-row"><span class="cb-ln">{ln}</span><span class="cb-change-bar"></span><span class="cb-fold-cell">{fold_elem}</span></div>')
        
        highlighted = highlight_codeblocks_cpp(line)
        cursor_elem = '<span class="cb-cursor"></span>' if (i == num_lines - 1 and with_cursor) else ''
        code_rows.append(f'<div class="cb-code-row">{highlighted}{cursor_elem}</div>')
        
    gutter_html = "".join(gutter_rows)
    code_html = "".join(code_rows)

    temp_html = os.path.abspath(out_path + ".temp.html")
    
    html_doc = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {{
    margin: 0;
    padding: 0;
    background: #ffffff;
    font-family: 'Courier New', 'Consolas', monospace;
    display: inline-block;
}}
.cb-editor {{
    display: flex;
    background: #ffffff;
    font-size: 13.5px;
    line-height: 18px;
    padding: 2px 0;
    user-select: none;
}}
.cb-gutter {{
    background: #ffffff;
    display: flex;
    flex-direction: column;
    user-select: none;
}}
.cb-gutter-row {{
    height: 18px;
    display: flex;
    align-items: center;
}}
.cb-ln {{
    font-size: 12px;
    color: #2b2b2b;
    padding-left: 6px;
    padding-right: 6px;
    min-width: 24px;
    text-align: right;
    font-family: 'Consolas', 'Courier New', monospace;
}}
.cb-change-bar {{
    width: 4px;
    height: 18px;
    background: #00e000;
    display: inline-block;
}}
.cb-fold-cell {{
    width: 16px;
    height: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}}
.cb-fold-box {{
    width: 9px;
    height: 9px;
    border: 1px solid #7a7a7a;
    background: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 9px;
    line-height: 8px;
    color: #333333;
    font-family: monospace;
    z-index: 2;
}}
.cb-fold-guide {{
    width: 1px;
    height: 18px;
    background: #c8c8c8;
    display: block;
}}
.cb-code-area {{
    background: #ffffff;
    padding-left: 6px;
    padding-right: 32px;
    color: #000000;
    white-space: nowrap;
}}
.cb-code-row {{
    height: 18px;
}}
/* Syntax Tokens matching authentic Code::Blocks screenshot */
.cb-kw {{ color: #0000a0; font-weight: bold; }}
.cb-std {{ color: #00a000; font-weight: bold; }}
.cb-prep {{ color: #00a000; }}
.cb-string {{ color: #0000ff; }}
.cb-num {{ color: #f000f0; }}
.cb-op {{ color: #ff0000; }}
.cb-comment {{ color: #8890b0; }}
.cb-cursor {{
    display: inline-block;
    width: 1.5px;
    height: 15px;
    background: #000000;
    margin-left: 2px;
    vertical-align: middle;
}}
</style>
</head>
<body>
<div class="cb-editor">
    <div class="cb-gutter">{gutter_html}</div>
    <div class="cb-code-area">{code_html}</div>
</div>
</body>
</html>"""

    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_doc)
        
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--force-device-scale-factor=1.5",
        f"--screenshot={out_path}",
        "--window-size=1200,1600",
        f"file:///{temp_html.replace(os.sep, '/')}"
    ]
    subprocess.run(cmd, capture_output=True)
    
    if os.path.exists(temp_html):
        try: os.remove(temp_html)
        except: pass
        
    # Auto crop white margin with anti-plagiarism dimension jitter
    if os.path.exists(out_path):
        import random
        im = Image.open(out_path)
        bg = Image.new(im.mode, im.size, (255, 255, 255))
        diff = ImageChops.difference(im, bg)
        bbox = diff.getbbox()
        if bbox:
            jitter_w = random.randint(18, 55)
            jitter_h = random.randint(4, 18)
            crop_box = (
                max(0, bbox[0] - 2),
                max(0, bbox[1] - 2),
                min(im.width, bbox[2] + jitter_w),
                min(im.height, bbox[3] + jitter_h)
            )
            im = im.crop(crop_box)
            im.save(out_path)
            
    return out_path
