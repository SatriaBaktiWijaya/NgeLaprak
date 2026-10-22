import os
import subprocess
import html
import re
from PIL import Image, ImageChops

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

JAVA_KEYWORDS = {
    "package", "import", "public", "private", "protected", "class", "interface",
    "static", "final", "void", "new", "return", "try", "catch", "throw", "throws",
    "int", "double", "float", "boolean", "char", "long", "short", "byte",
    "if", "else", "while", "for", "switch", "case", "break", "default", "continue",
    "this", "super", "extends", "implements", "null", "true", "false"
}

JAVA_COMMON_TYPES = {
    "String", "Object", "System", "List", "ArrayList", "Map", "HashMap",
    "Set", "HashSet", "Integer", "Double", "Boolean", "Character", "Scanner",
    "Math", "Exception", "Throwable", "Override", "Deprecated"
}

def highlight_netbeans_java(line_text, is_active=False):
    if not line_text.strip():
        return "&nbsp;"
        
    esc = html.escape(line_text)
    stripped = esc.strip()
    
    # 1. Javadoc / Multi-line Comment
    if stripped.startswith("/**") or stripped.startswith("/*") or stripped.startswith("*"):
        c_idx = -1
        for marker in ["/**", "/*", "*"]:
            idx = esc.find(marker)
            if idx != -1 and (c_idx == -1 or idx < c_idx):
                c_idx = idx
        if c_idx != -1 and esc[:c_idx].strip() == "":
            pre = esc[:c_idx].replace(" ", "&nbsp;").replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
            comment = f'<span class="nb-javadoc">{esc[c_idx:]}</span>'
            return pre + comment

    # 2. Single-line Comment
    if stripped.startswith("//"):
        c_idx = esc.find("//")
        pre = esc[:c_idx].replace(" ", "&nbsp;").replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
        comment = f'<span class="nb-comment">{esc[c_idx:]}</span>'
        return pre + comment

    # 3. Class declaration: highlight class name bold
    class_match = re.search(r'\bclass\s+([A-Za-z0-9_]+)', esc)
    class_name = class_match.group(1) if class_match else None

    # Tokenize strings, annotations, identifiers, words, symbols
    tokens = re.split(r'(&quot;.*?&quot;|\'.*?\'|@[A-Za-z0-9_]+|\b\w+\b|[^\w\s])', esc)
    out = []
    
    for i, tok in enumerate(tokens):
        if not tok:
            continue
        # String literal (NetBeans: Green #008000)
        if tok.startswith('&quot;') and tok.endswith('&quot;'):
            out.append(f'<span class="nb-string">{tok}</span>')
        # Char literal (NetBeans: Green #008000)
        elif tok.startswith("'") and tok.endswith("'"):
            out.append(f'<span class="nb-string">{tok}</span>')
        # Annotation (NetBeans: Dark Grey #404040)
        elif tok.startswith("@"):
            out.append(f'<span class="nb-ann">{tok}</span>')
        # Class declaration name (NetBeans: Bold Black)
        elif class_name and tok == class_name:
            out.append(f'<span class="nb-class-decl">{tok}</span>')
        # Keywords (NetBeans: Blue #0000e6)
        elif tok in JAVA_KEYWORDS:
            out.append(f'<span class="nb-kw">{tok}</span>')
        # Fields: accessed via 'this.field' or declared as private/static/final field
        elif (i >= 2 and tokens[i - 1] == "." and tokens[i - 2] == "this") or (
            tok.isupper() and len(tok) > 2 and "_" in tok
        ) or (
            any(f in esc for f in ["private ", "protected "]) and not "(" in esc and tok not in JAVA_KEYWORDS and tok not in JAVA_COMMON_TYPES
        ):
            out.append(f'<span class="nb-field">{tok}</span>')
        else:
            out.append(tok)
            
    res = "".join(out).replace(" ", "&nbsp;").replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
    return res

def render_netbeans_code(filename, code_text, start_line=1, end_line=None, out_path="netbeans_shot.png", active_line_offset=None, with_margin_guide=True, with_cursor=True, author_tag=None):
    """
    Renders an authentic Apache NetBeans editor screenshot snippet.
    Matches NetBeans default Java editor:
    - Green strings (#008000)
    - Purple italic fields (#990066)
    - Blue keywords (#0000e6)
    - Bold class declarations
    - Pastel light yellow active line highlight (#fff9e6)
    - Faint pink vertical column guide line (#f3c2c2)
    - Gutter fold icons, override badge, and warning lightbulb hints
    - Blinking editor cursor on active line
    - Anti-plagiarism dimension jittering
    """
    if author_tag and start_line == 1 and not code_text.strip().startswith("//"):
        code_text = f"// @author {author_tag}\n" + code_text

    all_lines = code_text.splitlines()
    if end_line is None or end_line > len(all_lines):
        end_line = len(all_lines)
        
    slice_lines = all_lines[start_line - 1 : end_line]
    num_lines = len(slice_lines)
    
    if active_line_offset is None:
        active_line_offset = num_lines - 1

    gutter_html = ""
    code_html = ""
    
    for i, raw_line in enumerate(slice_lines):
        ln = start_line + i
        is_active = (i == active_line_offset)
        has_fold = "{" in raw_line
        has_hint = ("try" in raw_line or "catch" in raw_line or "printStackTrace" in raw_line or "import " in raw_line)
        has_override = ("@Override" in raw_line or (i > 0 and "@Override" in slice_lines[i-1]))
        
        # Gutter element
        if has_override:
            badge_icon = '<span class="nb-override"></span>'
        elif has_hint:
            badge_icon = '<span class="nb-bulb"></span>'
        else:
            badge_icon = '<span class="nb-nobulb"></span>'
            
        fold_icon = '<span class="nb-fold">-</span>' if has_fold else '<span class="nb-nofold"></span>'
        gutter_html += f'<div class="gutter-row"><span class="nb-ln">{ln}</span>{badge_icon}{fold_icon}</div>'
        
        # Code element
        highlighted = highlight_netbeans_java(raw_line, is_active)
        active_class = " active-line" if is_active else ""
        cursor_elem = '<span class="nb-cursor"></span>' if (is_active and with_cursor) else ''
        code_html += f'<div class="code-row{active_class}">{highlighted}{cursor_elem}</div>'

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
    font-family: 'Consolas', 'Courier New', monospace;
    display: inline-block;
}}
.netbeans-editor {{
    display: flex;
    position: relative;
    background: #ffffff;
    font-size: 13px;
    line-height: 19px;
    padding: 2px 0;
    user-select: none;
}}
.gutter {{
    background: #fbfbfb;
    border-right: 1px solid #e0e0e0;
    padding-right: 4px;
    text-align: right;
    min-width: 55px;
}}
.gutter-row {{
    height: 19px;
    display: flex;
    align-items: center;
    justify-content: flex-end;
}}
.nb-ln {{
    color: #555555;
    font-size: 11.5px;
    margin-right: 4px;
    min-width: 20px;
}}
.nb-bulb {{
    width: 12px;
    height: 12px;
    background: radial-gradient(circle, #ffe600 40%, #cca000 90%);
    border-radius: 50%;
    border: 1px solid #b38600;
    display: inline-block;
    margin-right: 2px;
}}
.nb-nobulb {{
    width: 12px;
    height: 12px;
    display: inline-block;
    margin-right: 2px;
}}
.nb-fold {{
    width: 9px;
    height: 9px;
    border: 1px solid #888888;
    background: #ffffff;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 9px;
    color: #444444;
    line-height: 7px;
    margin-right: 3px;
}}
.nb-nofold {{
    width: 9px;
    height: 9px;
    display: inline-block;
    margin-right: 3px;
}}
.code-area {{
    position: relative;
    background: #ffffff;
    padding-left: 10px;
    padding-right: 40px;
    color: #000000;
    white-space: nowrap;
}}
.code-row {{
    height: 19px;
    box-sizing: border-box;
}}
.active-line {{
    background: #fff9e6 !important;
    width: 100%;
}}
.margin-guide {{
    position: absolute;
    top: 0;
    bottom: 0;
    left: 650px;
    width: 1px;
    background: #f3c2c2;
    z-index: 10;
}}
.nb-override {{
    width: 12px;
    height: 12px;
    background: #4caf50;
    border-radius: 50%;
    border: 1px solid #2e7d32;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin-right: 2px;
    box-sizing: border-box;
}}
.nb-override::after {{
    content: '';
    width: 4px;
    height: 4px;
    background: #ffffff;
    border-radius: 50%;
    display: block;
}}
.nb-cursor {{
    display: inline-block;
    width: 1.5px;
    height: 15px;
    background: #000000;
    margin-left: 2px;
    vertical-align: middle;
}}
/* Syntax Highlighting */
.nb-kw {{ color: #0000e6; font-weight: normal; }}
.nb-string {{ color: #008000; }}
.nb-field {{ color: #990066; font-style: italic; }}
.nb-comment {{ color: #969696; font-style: italic; }}
.nb-javadoc {{ color: #707070; }}
.nb-ann {{ color: #404040; }}
.nb-class-decl {{ font-weight: bold; color: #000000; }}
</style>
</head>
<body>
<div class="netbeans-editor">
    <div class="gutter">{gutter_html}</div>
    <div class="code-area">
        {"<div class='margin-guide'></div>" if with_margin_guide else ""}
        {code_html}
    </div>
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
