import os
import subprocess
import html
import re
from PIL import Image, ImageChops

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def render_vscode_code(code_text, language="python", theme="dark", start_line=1, end_line=None, out_path="vscode_shot.png"):
    """
    Renders an authentic VS Code editor snippet (Dark+ or Light+).
    """
    all_lines = code_text.splitlines()
    if end_line is None or end_line > len(all_lines):
        end_line = len(all_lines)
        
    slice_lines = all_lines[start_line - 1 : end_line]
    num_lines = len(slice_lines)
    
    is_dark = (theme == "dark")
    bg_color = "#1e1e1e" if is_dark else "#ffffff"
    text_color = "#d4d4d4" if is_dark else "#000000"
    gutter_color = "#858585" if is_dark else "#237893"
    kw_color = "#569cd6" if is_dark else "#0000ff"
    str_color = "#ce9178" if is_dark else "#a31515"
    comment_color = "#6a9955" if is_dark else "#008000"
    
    gutter_html = "".join(f'<div class="vsc-gutter-row">{start_line + i}</div>' for i in range(num_lines))
    
    code_lines_html = []
    for l in slice_lines:
        if not l.strip():
            code_lines_html.append('<div class="vsc-code-row">&nbsp;</div>')
            continue
        esc = html.escape(l)
        # basic syntax
        tokens = re.split(r'(&quot;.*?&quot;|\'.*?\'|\b\w+\b|[^\w\s])', esc)
        out = []
        for tok in tokens:
            if not tok: continue
            if (tok.startswith('&quot;') and tok.endswith('&quot;')) or (tok.startswith("'") and tok.endswith("'")):
                out.append(f'<span style="color:{str_color};">{tok}</span>')
            elif tok in {"def", "class", "import", "from", "return", "if", "else", "elif", "for", "while", "in", "as", "with", "True", "False", "None", "self"}:
                out.append(f'<span style="color:{kw_color}; font-weight:500;">{tok}</span>')
            else:
                out.append(tok)
        code_lines_html.append(f'<div class="vsc-code-row">{"".join(out).replace(" ", "&nbsp;").replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")}</div>')
        
    code_html = "".join(code_lines_html)
    temp_html = os.path.abspath(out_path + ".temp.html")
    
    html_doc = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {{
    margin: 0;
    padding: 0;
    background: {bg_color};
    font-family: 'Consolas', 'Courier New', monospace;
    display: inline-block;
}}
.vsc-editor {{
    display: flex;
    background: {bg_color};
    font-size: 13.5px;
    line-height: 20px;
    padding: 4px 0;
    user-select: none;
}}
.vsc-gutter {{
    background: {bg_color};
    padding: 0 10px 0 16px;
    text-align: right;
    color: {gutter_color};
    user-select: none;
}}
.vsc-gutter-row {{
    height: 20px;
    font-size: 12px;
}}
.vsc-code-area {{
    background: {bg_color};
    padding-left: 12px;
    padding-right: 32px;
    color: {text_color};
    white-space: nowrap;
}}
.vsc-code-row {{
    height: 20px;
}}
</style>
</head>
<body>
<div class="vsc-editor">
    <div class="vsc-gutter">{gutter_html}</div>
    <div class="vsc-code-area">{code_html}</div>
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
        
    if os.path.exists(out_path):
        im = Image.open(out_path)
        bg = Image.new(im.mode, im.size, (30, 30, 30) if is_dark else (255, 255, 255))
        diff = ImageChops.difference(im, bg)
        bbox = diff.getbbox()
        if bbox:
            crop_box = (
                max(0, bbox[0] - 2),
                max(0, bbox[1] - 2),
                min(im.width, bbox[2] + 4),
                min(im.height, bbox[3] + 4)
            )
            im = im.crop(crop_box)
            im.save(out_path)
            
    return out_path
