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
    "new", "delete", "nullptr", "NULL", "const", "static", "inline"
}

def highlight_codeblocks_cpp(line_text):
    if not line_text.strip():
        return "&nbsp;"
        
    esc = html.escape(line_text)
    
    # Preprocessor
    stripped = esc.strip()
    if stripped.startswith("#include") or stripped.startswith("#define") or stripped.startswith("#ifndef") or stripped.startswith("#endif"):
        return f'<span class="cb-prep">{esc}</span>'.replace(" ", "&nbsp;").replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
        
    # Comments
    if stripped.startswith("//"):
        c_idx = esc.find("//")
        pre = esc[:c_idx].replace(" ", "&nbsp;").replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
        comment = f'<span class="cb-comment">{esc[c_idx:]}</span>'
        return pre + comment
        
    tokens = re.split(r'(&quot;.*?&quot;|\b\w+\b|[^\w\s])', esc)
    out = []
    for tok in tokens:
        if not tok:
            continue
        if tok.startswith('&quot;') and tok.endswith('&quot;'):
            out.append(f'<span class="cb-string">{tok}</span>')
        elif tok in CPP_KEYWORDS:
            out.append(f'<span class="cb-kw">{tok}</span>')
        else:
            out.append(tok)
            
    return "".join(out).replace(" ", "&nbsp;").replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")

def render_codeblocks_code(code_text, start_line=1, end_line=None, out_path="codeblocks_shot.png", with_cursor=True, author_tag=None):
    """
    Renders an authentic Code::Blocks editor snippet (C/C++).
    Includes optional blinking cursor, author header, and anti-plagiarism dimension jitter.
    """
    if author_tag and start_line == 1 and not code_text.strip().startswith("//"):
        code_text = f"// @author {author_tag}\n" + code_text

    all_lines = code_text.splitlines()
    if end_line is None or end_line > len(all_lines):
        end_line = len(all_lines)
        
    slice_lines = all_lines[start_line - 1 : end_line]
    num_lines = len(slice_lines)
    
    gutter_html = "".join(f'<div class="cb-gutter-row">{start_line + i}</div>' for i in range(num_lines))
    code_rows = []
    for i, line in enumerate(slice_lines):
        highlighted = highlight_codeblocks_cpp(line)
        cursor_elem = '<span class="cb-cursor"></span>' if (i == num_lines - 1 and with_cursor) else ''
        code_rows.append(f'<div class="cb-code-row">{highlighted}{cursor_elem}</div>')
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
    line-height: 19px;
    padding: 2px 0;
    user-select: none;
}}
.cb-gutter {{
    background: #f0f0f0;
    border-right: 1px solid #d0d0d0;
    padding: 0 8px;
    text-align: right;
    color: #444444;
    user-select: none;
}}
.cb-gutter-row {{
    height: 19px;
    font-size: 12px;
}}
.cb-code-area {{
    background: #ffffff;
    padding-left: 8px;
    padding-right: 28px;
    color: #000000;
    white-space: nowrap;
}}
.cb-code-row {{
    height: 19px;
}}
.cb-kw {{ color: #0000a0; font-weight: bold; }}
.cb-prep {{ color: #008000; font-weight: normal; }}
.cb-string {{ color: #a00000; }}
.cb-comment {{ color: #008000; font-style: italic; }}
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
