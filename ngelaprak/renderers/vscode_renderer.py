import os
import subprocess
import html
import re
import random
from PIL import Image, ImageChops

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

PYTHON_CONTROL_KEYWORDS = {
    "import", "from", "as", "with", "try", "except", "finally", "raise",
    "return", "if", "else", "elif", "for", "while", "pass", "break",
    "continue", "in", "is", "not", "and", "or", "global", "nonlocal",
    "del", "assert", "yield"
}
PYTHON_DEF_KEYWORDS = {"def", "class", "lambda", "async", "await"}
PYTHON_CONSTANTS = {"True", "False", "None"}
PYTHON_SELF = {"self", "cls"}
PYTHON_TYPES = {
    "int", "str", "float", "bool", "list", "dict", "tuple", "set", "bytes",
    "object", "type", "List", "Dict", "Tuple", "Set", "Optional", "Union", "Any",
    "Exception", "BaseException", "ValueError", "TypeError", "KeyError",
    "ZeroDivisionError", "FileNotFoundError", "IndexError", "AttributeError",
    "os", "sys", "re", "shutil", "docx", "pypdf", "json", "math", "random",
    "subprocess", "html", "PIL", "Image", "ImageChops", "PdfReader", "Document",
    "DataProcessor"
}
PYTHON_FUNCS = {
    "print", "len", "range", "open", "sum", "min", "max", "input",
    "append", "extend", "insert", "remove", "pop", "clear", "index",
    "count", "sort", "reverse", "join", "split", "strip", "lstrip", "rstrip",
    "replace", "lower", "upper", "startswith", "endswith", "format",
    "find", "items", "keys", "values", "get", "update", "read", "write",
    "close", "exists", "splitext", "basename", "dirname", "abspath"
}

def highlight_vscode_line(line_text, is_dark=True):
    if not line_text.strip():
        return "&nbsp;"
        
    esc = html.escape(line_text)
    stripped = esc.strip()
    
    # 1. Comments (# for Python, // for C/Java)
    comment_char = None
    if stripped.startswith("#"):
        comment_char = "#"
    elif stripped.startswith("//"):
        comment_char = "//"
        
    if comment_char:
        c_idx = esc.find(comment_char)
        if esc[:c_idx].strip() == "":
            pre = esc[:c_idx].replace(" ", "&nbsp;").replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
            comment = f'<span class="vsc-comment">{esc[c_idx:]}</span>'
            return pre + comment

    # 2. Decorators (@property, @staticmethod)
    if stripped.startswith("@"):
        return f'<span class="vsc-decorator">{esc}</span>'.replace(" ", "&nbsp;").replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")

    # 3. Tokenize strings, numbers, words, and symbols
    token_pattern = r'(&quot;.*?&quot;|\'.*?\'|\b\d+(?:\.\d+)?\b|\b\w+\b|[^\w\s])'
    tokens = re.split(token_pattern, esc)
    out = []
    
    for i, tok in enumerate(tokens):
        if not tok:
            continue
        # String literal (VS Code: Orange #ce9178)
        if (tok.startswith('&quot;') and tok.endswith('&quot;')) or (tok.startswith("'") and tok.endswith("'")):
            out.append(f'<span class="vsc-string">{tok}</span>')
        # Number literal (VS Code: Light Green #b5cea8)
        elif re.match(r'^\d+(?:\.\d+)?$', tok):
            out.append(f'<span class="vsc-number">{tok}</span>')
        # Control flow & imports (VS Code: Magenta #c586c0)
        elif tok in PYTHON_CONTROL_KEYWORDS:
            out.append(f'<span class="vsc-control">{tok}</span>')
        # Definition keywords (VS Code: Blue #569cd6)
        elif tok in PYTHON_DEF_KEYWORDS:
            out.append(f'<span class="vsc-keyword">{tok}</span>')
        # Constants True/False/None (VS Code: Blue #569cd6)
        elif tok in PYTHON_CONSTANTS or tok in PYTHON_SELF:
            out.append(f'<span class="vsc-constant">{tok}</span>')
        # Known Types, Modules, and Exceptions (VS Code: Teal #4ec9b0)
        elif tok in PYTHON_TYPES or (i > 0 and tokens[i-1] in ["class", ":", "-&gt;"]):
            out.append(f'<span class="vsc-type">{tok}</span>')
        # Function definitions or calls (VS Code: Yellow #dcdcaa)
        elif tok in PYTHON_FUNCS or (i + 1 < len(tokens) and tokens[i + 1] == "(") or (i > 1 and tokens[i-2] == "def"):
            out.append(f'<span class="vsc-func">{tok}</span>')
        # General variables / identifiers (VS Code: Light Blue #9cdcfe)
        elif re.match(r'^[a-zA-Z_]\w*$', tok):
            out.append(f'<span class="vsc-var">{tok}</span>')
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
    show_tab=True,
    active_line_offset=None,
    with_cursor=True
):
    """
    Renders an authentic Visual Studio Code editor snippet.
    Default: VS Code Dark+ / Dark Modern theme with:
    - Dark editor background (#1e1e1e)
    - Active file tab with language icon & close button
    - Breadcrumb navigation
    - Line number gutter with active line highlight (#ffffff)
    - Rich syntax highlighting matching VS Code default tokens:
      * Magenta control flow (#c586c0)
      * Blue definitions (#569cd6)
      * Teal types & modules (#4ec9b0)
      * Yellow functions & methods (#dcdcaa)
      * Light blue variables (#9cdcfe)
      * Orange strings (#ce9178)
      * Light green numbers (#b5cea8)
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
    
    if active_line_offset is None and num_lines > 0:
        active_line_offset = min(17, num_lines - 1) if num_lines > 17 else num_lines - 1
        
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
    type_color = "#4ec9b0" if is_dark else "#267f99"
    var_color = "#9cdcfe" if is_dark else "#001080"
    str_color = "#ce9178" if is_dark else "#a31515"
    num_color = "#b5cea8" if is_dark else "#098658"
    func_color = "#dcdcaa" if is_dark else "#795e26"
    comment_color = "#6a9955" if is_dark else "#008000"
    const_color = "#569cd6" if is_dark else "#0000ff"
    
    gutter_rows = []
    code_lines_html = []
    for i, l in enumerate(slice_lines):
        is_active = (i == active_line_offset)
        act_g_cls = " active" if is_active else ""
        act_c_cls = " active" if is_active else ""
        cursor_elem = '<span class="vsc-cursor"></span>' if (is_active and with_cursor) else ''
        
        gutter_rows.append(f'<div class="vsc-gutter-row{act_g_cls}">{start_line + i}</div>')
        line_hl = highlight_vscode_line(l, is_dark=is_dark)
        code_lines_html.append(f'<div class="vsc-code-row{act_c_cls}">{line_hl}{cursor_elem}</div>')
        
    gutter_html = "".join(gutter_rows)
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
.vsc-gutter-row.active {{
    color: #ffffff !important;
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
    box-sizing: border-box;
}}
.vsc-code-row.active {{
    background: {"#282828" if is_dark else "#f5f5f5"};
    outline: 1px solid {"#2d2d2d" if is_dark else "#e8e8e8"};
}}
.vsc-keyword {{ color: {kw_color}; font-weight: 500; }}
.vsc-control {{ color: {ctrl_color}; font-weight: 500; }}
.vsc-type {{ color: {type_color}; }}
.vsc-var {{ color: {var_color}; }}
.vsc-func {{ color: {func_color}; }}
.vsc-string {{ color: {str_color}; }}
.vsc-number {{ color: {num_color}; }}
.vsc-comment {{ color: {comment_color}; font-style: italic; }}
.vsc-constant {{ color: {const_color}; }}
.vsc-decorator {{ color: {func_color}; }}
.vsc-cursor {{
    display: inline-block;
    width: 1.5px;
    height: 16px;
    background: {"#aeafad" if is_dark else "#000000"};
    margin-left: 1px;
    vertical-align: middle;
}}
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
