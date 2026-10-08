import os
import subprocess
import html
from PIL import Image, ImageChops

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def render_terminal_output(title_text, lines, out_path="terminal_shot.png", mode="windows_terminal"):
    """
    Renders an authentic Windows Terminal or CMD/MySQL client window.
    """
    body_content = "<br>".join(html.escape(l).replace(" ", "&nbsp;") if l else "&nbsp;" for l in lines)
    disp_title = html.escape(title_text)
    temp_html = os.path.abspath(out_path + ".temp.html")
    
    html_doc = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {{ margin: 0; padding: 0; background: #ffffff; font-family: 'Consolas', monospace; display: inline-block; }}
.terminal-window {{
    background: #0c0c0c;
    border: 1px solid #333333;
    border-radius: 6px;
    overflow: hidden;
    box-shadow: 0 4px 14px rgba(0,0,0,0.25);
}}
.tabbar {{
    background: #1f1f1f;
    border-bottom: 1px solid #2d2d2d;
    display: flex;
    align-items: center;
    padding-left: 8px;
    height: 32px;
}}
.tab {{
    background: #0c0c0c;
    border: 1px solid #333333;
    border-bottom: none;
    padding: 5px 14px;
    font-size: 12.5px;
    color: #ffffff;
    display: flex;
    align-items: center;
    gap: 8px;
    border-radius: 4px 4px 0 0;
}}
.win-controls {{
    margin-left: auto;
    padding-right: 12px;
    display: flex;
    gap: 14px;
    color: #888888;
    font-size: 11px;
}}
.terminal-body {{
    background: #0c0c0c;
    color: #cccccc;
    font-size: 13.5px;
    line-height: 20px;
    padding: 12px 18px;
    white-space: nowrap;
}}
</style>
</head>
<body>
<div class="terminal-window">
    <div class="tabbar">
        <div class="tab">
            <span>&gt;</span>
            <span>{disp_title}</span>
            <span style="color:#888; font-size:10px;">✕</span>
        </div>
        <div class="win-controls">
            <span>—</span>
            <span>▢</span>
            <span>✕</span>
        </div>
    </div>
    <div class="terminal-body">{body_content}</div>
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
        "--window-size=1200,800",
        f"file:///{temp_html.replace(os.sep, '/')}"
    ]
    subprocess.run(cmd, capture_output=True)
    
    if os.path.exists(temp_html):
        try: os.remove(temp_html)
        except: pass
        
    if os.path.exists(out_path):
        im = Image.open(out_path)
        bg = Image.new(im.mode, im.size, (255, 255, 255))
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
