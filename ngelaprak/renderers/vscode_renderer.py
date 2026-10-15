import os
import subprocess
import html
import re
import random
from PIL import Image, ImageChops

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

PYTHON_KEYWORDS = {
    "def", "class", "import", "from", "as", "with", "async", "await", "lambda",
    "pass", "global", "nonlocal", "del", "assert", "yield"
}
CONTROL_FLOW_KEYWORDS = {
    "if", "else", "elif", "for", "while", "return", "try", "except", "finally",
    "raise", "break", "continue", "in", "is", "not", "and", "or", "throw", "catch"
}
CONSTANTS = {"True", "False", "None", "self", "cls", "null", "undefined", "this"}
COMMON_FUNCS = {"print", "len", "range", "str", "int", "float", "list", "dict", "set", "tuple", "open", "type", "input", "append", "get"}

def highlight_vscode_line(line_text, is_dark=True):
    if not line_text.strip():
        return "&nbsp;"
        
    esc = html.escape(line_text)
    
    # Check comment (# for python, // for c/java/js)
    stripped = esc.strip()
    comment_char = None
    if stripped.startswith("#"):
        comment_char = "#"
    elif stripped.startswith("//"):
        comment_char = "//"
        
    if comment_char:
        c_idx = esc.find(comment_char)
        pre = esc[:c_idx].replace(" ", "&nbsp;").replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
        comment = f'<span class="vsc-comment">{esc[c_idx:]}</span>'
        return pre + comment

    # Tokenize strings, numbers, words, and symbols
    token_pattern = r'(&quot;.*?&quot;|\'.*?\'|\b\d+\b|\b\w+\b|[^\w\s])'
    tokens = re.split(token_pattern, esc)
    out = []
    
    for i, tok in enumerate(tokens):
        if not tok:
            continue
        # String literal
        if (tok.startswith('&quot;') and tok.endswith('&quot;')) or (tok.startswith("'") and tok.endswith("'")):
            out.append(f'<span class="vsc-string">{tok}</span>')
        # Number literal
        elif tok.isdigit():
            out.append(f'<span class="vsc-number">{tok}</span>')
        # Control flow keywords (magenta)
        elif tok in CONTROL_FLOW_KEYWORDS:
            out.append(f'<span class="vsc-control">{tok}</span>')
        # Standard keywords (blue)
        elif tok in PYTHON_KEYWORDS:
            out.append(f'<span class="vsc-keyword">{tok}</span>')
        # Constants / Builtins
        elif tok in CONSTANTS:
            out.append(f'<span class="vsc-constant">{tok}</span>')
        # Functions / Method calls
        elif tok in COMMON_FUNCS or (i + 1 < len(tokens) and tokens[i + 1] == "("):
            out.append(f'<span class="vsc-func">{tok}</span>')
        else:
            out.append(tok)
            
    return "".join(out).replace(" ", "&nbsp;").replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")

def render_vscode_code(
    code_text,
    filename="main.py",
    language="python",
    theme="dark",
    start_line=1,
    end_line=None,
    out_path="vscode_shot.png",
    author_tag=None,
    show_tab=True
):
    """
    Renders an authentic Visual Studio Code editor snippet.
    Default: VS Code Dark+ / Dark Modern theme with:
    - Dark editor background (#1e1e1e)
    - Active file tab with language icon & close button
    - Optional breadcrumb navigation
    - Line number gutter with accurate styling
    - Rich syntax highlighting matching VS Code default tokens
    - Anti-plagiarism dimension jitter
    """
    out_path = os.path.abspath(out_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    # Author tag injection for anti-plagiarism
    if author_tag and start_line == 1:
        comment_prefix = "#" if language == "python" or filename.endswith(".py") else "//"
        if not code_text.strip().startswith(comment_prefix):
            code_text = f"{comment_prefix} @author {author_tag}\n" + code_text

    all_lines = code_text.splitlines()
    if end_line is None or end_line > len(all_lines):
        end_line = len(all_lines)
        
    slice_lines = all_lines[start_line - 1 : end_line]
    num_lines = len(slice_lines)
    
    is_dark = (theme.lower() == "dark")
    bg_color = "#1e1e1e" if is_dark else "#ffffff"
    header_bg = "#181818" if is_dark else "#f3f3f3"
    tab_active_bg = "#1e1e1e" if is_dark else "#ffffff"
    tab_border_top = "#0078d4" if is_dark else "#005fb8"
    tab_text = "#ffffff" if is_dark else "#333333"
    breadcrumb_bg = "#1e1e1e" if is_dark else "#ffffff"
    breadcrumb_text = "#8c8c8c" if is_dark else "#616161"
    border_color = "#2b2b2b" if is_dark else "#e5e5e5"
    text_color = "#d4d4d4" if is_dark else "#000000"
    gutter_color = "#858585" if is_dark else "#237893"
    
    # Syntax colors
    kw_color = "#569cd6" if is_dark else "#0000ff"
    ctrl_color = "#c586c0" if is_dark else "#af00db"
    str_color = "#ce9178" if is_dark else "#a31515"
    num_color = "#b5cea8" if is_dark else "#098658"
    func_color = "#dcdcaa" if is_dark else "#795e26"
    comment_color = "#6a9955" if is_dark else "#008000"
    const_color = "#569cd6" if is_dark else "#0000ff"
    
    gutter_html = "".join(f'<div class="vsc-gutter-row">{start_line + i}</div>' for i in range(num_lines))
    
    code_lines_html = []
    for l in slice_lines:
        line_hl = highlight_vscode_line(l, is_dark=is_dark)
        code_lines_html.append(f'<div class="vsc-code-row">{line_hl}</div>')
        
    code_html = "".join(code_lines_html)
    temp_html = os.path.abspath(out_path + ".temp.html")
    
    clean_filename = os.path.basename(filename) if filename else "main.py"
    file_ext = os.path.splitext(clean_filename)[1].lower()
    
    # File icon color indicator
    if file_ext in [".py"]:
        icon_svg = '<svg width="14" height="14" viewBox="0 0 24 24" fill="#3776ab"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14h2v2h-2v-2zm0-10h2v8h-2V6z"/></svg>'
    elif file_ext in [".js", ".ts", ".jsx", ".tsx"]:
        icon_svg = '<svg width="14" height="14" viewBox="0 0 24 24" fill="#f7df1e"><rect width="24" height="24" rx="3"/><text x="4" y="18" font-size="14" font-weight="bold" fill="#000">JS</text></svg>'
    elif file_ext in [".cpp", ".c", ".h"]:
        icon_svg = '<svg width="14" height="14" viewBox="0 0 24 24" fill="#00599c"><rect width="24" height="24" rx="3"/><text x="3" y="17" font-size="12" font-weight="bold" fill="#fff">C++</text></svg>'
    else:
        icon_svg = '<svg width="14" height="14" viewBox="0 0 24 24" fill="#757575"><path d="M14 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>'

    tab_header_html = ""
    if show_tab:
        tab_header_html = f"""
<div class="vsc-titlebar">
    <div class="vsc-tabs">
        <div class="vsc-tab active">
            <span class="vsc-tab-icon">{icon_svg}</span>
            <span class="vsc-tab-title">{html.escape(clean_filename)}</span>
            <span class="vsc-tab-close">&times;</span>
        </div>
    </div>
</div>
<div class="vsc-breadcrumb">
    <span>src</span> &gt; <span class="vsc-bc-active">{html.escape(clean_filename)}</span>
</div>
"""

    html_doc = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {{
    margin: 0;
    padding: 0;
    background: {bg_color};
    font-family: 'Consolas', 'Courier New', 'Segoe UI', monospace;
    display: inline-block;
}}
.vsc-window {{
    background: {bg_color};
    border-radius: 6px;
    overflow: hidden;
    box-shadow: 0 4px 14px rgba(0,0,0,0.4);
    border: 1px solid {border_color};
    min-width: 580px;
}}
.vsc-titlebar {{
    background: {header_bg};
    display: flex;
    align-items: center;
    border-bottom: 1px solid {border_color};
    padding: 0;
    height: 35px;
}}
.vsc-tabs {{
    display: flex;
    height: 100%;
}}
.vsc-tab {{
    display: flex;
    align-items: center;
    gap: 7px;
    padding: 0 14px;
    font-size: 12px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: #969696;
    border-right: 1px solid {border_color};
    cursor: default;
}}
.vsc-tab.active {{
    background: {tab_active_bg};
    color: {tab_text};
    border-top: 2px solid {tab_border_top};
    margin-top: -1px;
}}
.vsc-tab-close {{
    font-size: 14px;
    color: #858585;
    margin-left: 4px;
}}
.vsc-breadcrumb {{
    background: {breadcrumb_bg};
    padding: 4px 16px;
    font-size: 11px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: {breadcrumb_text};
    border-bottom: 1px solid {border_color};
    display: flex;
    align-items: center;
    gap: 6px;
}}
.vsc-bc-active {{
    color: {text_color};
    font-weight: 500;
}}
.vsc-editor {{
    display: flex;
    background: {bg_color};
    font-size: 13.5px;
    line-height: 20px;
    padding: 6px 0;
    user-select: none;
}}
.vsc-gutter {{
    background: {bg_color};
    padding: 0 12px 0 16px;
    text-align: right;
    color: {gutter_color};
    user-select: none;
    min-width: 38px;
}}
.vsc-gutter-row {{
    height: 20px;
    font-size: 12px;
    font-family: 'Consolas', 'Courier New', monospace;
}}
.vsc-code-area {{
    background: {bg_color};
    padding-left: 14px;
    padding-right: 36px;
    color: {text_color};
    white-space: nowrap;
    font-family: 'Consolas', 'Courier New', monospace;
}}
.vsc-code-row {{
    height: 20px;
}}
.vsc-keyword {{ color: {kw_color}; font-weight: 500; }}
.vsc-control {{ color: {ctrl_color}; font-weight: 500; }}
.vsc-string {{ color: {str_color}; }}
.vsc-number {{ color: {num_color}; }}
.vsc-func {{ color: {func_color}; }}
.vsc-comment {{ color: {comment_color}; font-style: italic; }}
.vsc-constant {{ color: {const_color}; }}
</style>
</head>
<body>
<div class="vsc-window">
    {tab_header_html}
    <div class="vsc-editor">
        <div class="vsc-gutter">{gutter_html}</div>
        <div class="vsc-code-area">{code_html}</div>
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
        
    if os.path.exists(out_path):
        im = Image.open(out_path)
        bg = Image.new(im.mode, im.size, (30, 30, 30) if is_dark else (255, 255, 255))
        diff = ImageChops.difference(im, bg)
        bbox = diff.getbbox()
        if bbox:
            # Jitter for anti-plagiarism dimension uniqueness
            jitter_w = random.randint(2, 8)
            jitter_h = random.randint(2, 6)
            crop_box = (
                max(0, bbox[0] - 2),
                max(0, bbox[1] - 2),
                min(im.width, bbox[2] + jitter_w),
                min(im.height, bbox[3] + jitter_h)
            )
            im = im.crop(crop_box)
            im.save(out_path)
            
    return out_path
