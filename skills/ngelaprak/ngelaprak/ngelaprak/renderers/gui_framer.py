import os
from PIL import Image, ImageDraw, ImageFont

TEMPLATES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "templates"))
JAVA_ICON_PATH = os.path.join(TEMPLATES_DIR, "java_cup_icon.png")

def frame_windows_gui(content_img_path, title_text="Application", out_path="framed_gui.png", app_icon="java"):
    """
    Frames a GUI screenshot with authentic Windows 11 window borders,
    rounded header, real Java coffee cup icon, and native window controls.
    """
    content = Image.open(content_img_path).convert("RGBA")
    w, h = content.size
    
    title_h = 32
    border = 1
    total_w = w + (border * 2)
    total_h = h + title_h + border
    
    frame = Image.new("RGBA", (total_w, total_h), (255, 255, 255, 0))
    draw = ImageDraw.Draw(frame)
    
    # Title bar
    draw.rectangle([0, 0, total_w, title_h], fill=(243, 243, 243, 255))
    draw.rectangle([0, 0, total_w - 1, total_h - 1], outline=(180, 180, 180, 255), width=1)
    
    # App icon
    if app_icon == "java" and os.path.exists(JAVA_ICON_PATH):
        try:
            cup = Image.open(JAVA_ICON_PATH).convert("RGBA")
            frame.paste(cup, (8, 6), cup)
        except Exception:
            draw.rounded_rectangle([8, 8, 24, 24], radius=3, fill=(220, 60, 60, 255))
    else:
        draw.rounded_rectangle([8, 8, 24, 24], radius=3, fill=(50, 120, 220, 255))
        
    # Title text
    try:
        font_title = ImageFont.truetype("segoeui.ttf", 12)
        font_btn = ImageFont.truetype("segoeui.ttf", 11)
    except Exception:
        font_title = ImageFont.load_default()
        font_btn = ImageFont.load_default()
        
    draw.text((34, 7), title_text, fill=(30, 30, 30, 255), font=font_title)
    
    # Window controls (crisp vector shapes: Minimize, Maximize, and Close X)
    draw.line([(total_w - 97, 16), (total_w - 87, 16)], fill=(70, 70, 70, 255), width=1)
    draw.rectangle([(total_w - 63, 11), (total_w - 53, 21)], outline=(70, 70, 70, 255), width=1)
    draw.line([(total_w - 29, 11), (total_w - 19, 21)], fill=(70, 70, 70, 255), width=1)
    draw.line([(total_w - 19, 11), (total_w - 29, 21)], fill=(70, 70, 70, 255), width=1)
    
    # Paste GUI body
    frame.paste(content, (border, title_h), content)
    
    final_img = Image.new("RGB", (total_w, total_h), (255, 255, 255))
    final_img.paste(frame, (0, 0), frame)
    final_img.save(out_path)
    return out_path
