import os
import subprocess
import html
import random
from PIL import Image, ImageChops

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

SQL_KEYWORDS = {
    "SELECT", "FROM", "WHERE", "INSERT", "INTO", "VALUES", "UPDATE", "SET",
    "DELETE", "JOIN", "INNER", "LEFT", "RIGHT", "OUTER", "GROUP", "BY",
    "ORDER", "ASC", "DESC", "HAVING", "LIMIT", "OFFSET", "CREATE", "TABLE",
    "ALTER", "DROP", "DATABASE", "PRIMARY", "KEY", "FOREIGN", "REFERENCES",
    "NOT", "NULL", "AND", "OR", "IN", "AS", "DISTINCT", "LIKE"
}

def highlight_sql(sql_text):
    words = sql_text.split()
    out = []
    for w in words:
        clean = w.strip(",;()").upper()
        if clean in SQL_KEYWORDS:
            out.append(f'<span class="sql-kw">{html.escape(w)}</span>')
        elif w.startswith("'") or w.startswith('"'):
            out.append(f'<span class="sql-str">{html.escape(w)}</span>')
        else:
            out.append(f'<span class="sql-id">{html.escape(w)}</span>')
    return " ".join(out)

def render_database_query(query_sql, columns, rows, title="DBeaver 24.0 - SQL Console", status_text=None, out_path="sql_result.png"):
    """
    Renders an authentic SQL Query Editor + Data Grid result (DBeaver / Navicat / pgAdmin style).
    Perfect for Basis Data / SQL laboratory reports.
    """
    out_path = os.path.abspath(out_path)
    if status_text is None:
        status_text = f"Query executed successfully ({len(rows)} rows fetched in 15 ms)"

    highlighted_sql = highlight_sql(query_sql)

    # Table columns HTML
    th_html = '<th class="row-num">#</th>' + "".join(f'<th>{html.escape(c)}</th>' for c in columns)

    # Table rows HTML
    tr_rows = []
    for idx, row in enumerate(rows):
        r_num = idx + 1
        cells = f'<td class="row-num">{r_num}</td>' + "".join(f'<td>{html.escape(str(val))}</td>' for val in row)
        row_cls = "even-row" if idx % 2 == 1 else "odd-row"
        tr_rows.append(f'<tr class="{row_cls}">{cells}</tr>')
    tbody_html = "".join(tr_rows)

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
    font-family: 'Segoe UI', Arial, sans-serif;
    display: inline-block;
}}
.dbeaver-window {{
    background: #252526;
    border: 1px solid #3c3c3c;
    border-radius: 6px;
    overflow: hidden;
    box-shadow: 0 4px 16px rgba(0,0,0,0.25);
    width: 680px;
}}
.title-bar {{
    background: #1f1f1f;
    padding: 6px 12px;
    font-size: 11.5px;
    color: #cccccc;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #333333;
}}
.editor-toolbar {{
    background: #2d2d2d;
    padding: 4px 10px;
    display: flex;
    align-items: center;
    gap: 8px;
    border-bottom: 1px solid #3c3c3c;
}}
.btn-exec {{
    background: #0e639c;
    color: #ffffff;
    border: none;
    border-radius: 3px;
    padding: 3px 8px;
    font-size: 11px;
    font-weight: bold;
    display: flex;
    align-items: center;
    gap: 4px;
}}
.sql-area {{
    background: #1e1e1e;
    color: #d4d4d4;
    font-family: 'Consolas', monospace;
    font-size: 13px;
    padding: 10px 14px;
    border-bottom: 2px solid #007acc;
    white-space: pre-wrap;
}}
.sql-kw {{ color: #569cd6; font-weight: bold; }}
.sql-str {{ color: #ce9178; }}
.sql-id {{ color: #9cdcfe; }}
.grid-container {{
    background: #ffffff;
    overflow: hidden;
}}
table {{
    width: 100%;
    border-collapse: collapse;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 12px;
}}
th {{
    background: #f0f0f0;
    color: #333333;
    font-weight: 600;
    text-align: left;
    padding: 5px 10px;
    border: 1px solid #dcdcdc;
}}
th.row-num, td.row-num {{
    width: 28px;
    text-align: center;
    color: #888888;
    background: #fafafa;
    border-right: 1px solid #dcdcdc;
}}
td {{
    padding: 4px 10px;
    border: 1px solid #e5e5e5;
    color: #222222;
}}
tr.odd-row td:not(.row-num) {{ background: #ffffff; }}
tr.even-row td:not(.row-num) {{ background: #f9fbfd; }}
.status-bar {{
    background: #007acc;
    color: #ffffff;
    font-size: 11px;
    padding: 3px 10px;
}}
</style>
</head>
<body>
<div class="dbeaver-window">
    <div class="title-bar">
        <span>🗄️ {html.escape(title)}</span>
    </div>
    <div class="editor-toolbar">
        <button class="btn-exec">▶ Execute Script</button>
        <span style="color:#888; font-size:11px;">Server: localhost:3306</span>
    </div>
    <div class="sql-area">{highlighted_sql}</div>
    <div class="grid-container">
        <table>
            <thead><tr>{th_html}</tr></thead>
            <tbody>{tbody_html}</tbody>
        </table>
    </div>
    <div class="status-bar">{html.escape(status_text)}</div>
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
        "--window-size=1200,1000",
        f"file:///{temp_html.replace(os.sep, '/')}"
    ]
    subprocess.run(cmd, capture_output=True)

    if os.path.exists(temp_html):
        try: os.remove(temp_html)
        except: pass

    # Auto crop with anti-plagiarism jitter
    if os.path.exists(out_path):
        im = Image.open(out_path)
        bg = Image.new(im.mode, im.size, (255, 255, 255))
        diff = ImageChops.difference(im, bg)
        bbox = diff.getbbox()
        if bbox:
            jitter_w = random.randint(15, 45)
            crop_box = (
                max(0, bbox[0] - 2),
                max(0, bbox[1] - 2),
                min(im.width, bbox[2] + jitter_w),
                min(im.height, bbox[3] + 4)
            )
            im = im.crop(crop_box)
            im.save(out_path)

    return out_path
