"""
1-to-1 Windows 11 PowerShell (Windows Terminal 1.25) Native Renderer.

Primary engine (Windows + wxPython): native Win32/wxPython frame captured via
GDI PrintWindow using authentic Windows 11 Segoe UI, Cascadia Mono, Campbell
color scheme (#0C0C0C / #CCCCCC), and official Windows Terminal profile icons.

Fallback engine (Linux/macOS or headless without wxPython): Pillow software
renderer reproducing the exact same layout, colors, and bundled icons.
"""

import ctypes
import os
import random
import re
import sys
from PIL import Image, ImageDraw, ImageFont

if sys.platform == "win32":
    from ctypes import wintypes

try:
    import wx

    HAS_WX = True
except (ImportError, ModuleNotFoundError):
    HAS_WX = False

if sys.platform == "win32":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        pass

TEMPLATES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "templates"))
PS_ICON_16 = os.path.join(TEMPLATES_DIR, "powershell_icon_16.png")
PS_ICON_32 = os.path.join(TEMPLATES_DIR, "powershell_icon_32.png")
CMD_ICON_16 = os.path.join(TEMPLATES_DIR, "cmd_icon_16.png")
CMD_ICON_32 = os.path.join(TEMPLATES_DIR, "cmd_icon_32.png")

_STYLE_TAGS = ("INPUT", "HEADER", "SUCCESS", "MUTED", "PROMPT")

# Official Windows Terminal 1.25 Dark Theme + Campbell Scheme colors
_COLOR_BG = (12, 12, 12)             # #0C0C0C terminalBackground
_COLOR_TABROW = (32, 32, 32)         # #202020 Win11 dark titlebar/tab strip
_COLOR_BORDER = (56, 56, 56)         # #383838 outer 1px window border
_COLOR_FG = (204, 204, 204)          # #CCCCCC Campbell foreground
_COLOR_CMD_YELLOW = (249, 241, 165)  # #F9F1A5 Campbell brightYellow (PSReadLine Command)
_COLOR_CURSOR = (255, 255, 255)      # #FFFFFF bar cursor
_COLOR_TEXT_WHITE = (255, 255, 255)
_COLOR_PILL_BG = (45, 45, 45)
_COLOR_PILL_DIV = (68, 68, 68)
_COLOR_SCROLL_THUMB = (92, 92, 92)


def strip_terminal_tokens(line):
    """Strips legacy NgeLaprak [[INPUT]]/[[HEADER]]/[[SUCCESS]]/[[MUTED]]/[[PROMPT]] tags."""
    s = "" if line is None else str(line)
    for tag in _STYLE_TAGS:
        s = re.sub(rf"\[\[{tag}\]\](.*?)\[\[/{tag}\]\]", r"\1", s)
    return s


def format_terminal_line(l):
    """Backward-compatible helper returning plain stripped text for a terminal line."""
    return strip_terminal_tokens(l)


def _split_ps_prompt_line(clean_line):
    """
    Splits a Windows PowerShell prompt line 'PS <dir>> <cmd> <args>' into
    native PSReadLine segments: command name in #F9F1A5, prompt and args in #CCCCCC.
    Returns None if the line is not a PS prompt line.
    """
    m = re.match(r"^(PS\s+[^>]+>\s*)(.*)$", clean_line)
    if not m:
        return None
    prompt_part, rest = m.group(1), m.group(2)
    if not rest:
        return [(prompt_part, _COLOR_FG)]
    m_cmd = re.match(r"^(\S+)(.*)$", rest)
    if not m_cmd:
        return [(clean_line, _COLOR_FG)]
    cmd_part, args_part = m_cmd.group(1), m_cmd.group(2)
    segs = [(prompt_part, _COLOR_FG), (cmd_part, _COLOR_CMD_YELLOW)]
    if args_part:
        segs.append((args_part, _COLOR_FG))
    return segs


def _pick_icon_path(title_text, mode, size_px=16):
    low_title = (title_text or "").lower()
    low_mode = (mode or "powershell").lower()
    use_cmd = low_mode in ("cmd", "mysql") or any(
        k in low_title for k in ("mysql", "command prompt", "cmd.exe")
    )
    if use_cmd:
        cand = CMD_ICON_32 if size_px > 16 else CMD_ICON_16
        if os.path.exists(cand):
            return cand
    cand = PS_ICON_32 if size_px > 16 else PS_ICON_16
    if os.path.exists(cand):
        return cand
    return None


def _compute_jitter(clean_lines):
    rng = random.Random(abs(hash("\n".join(clean_lines))) % 100000)
    return rng.randint(16, 42), rng.randint(6, 16)


def _capture_hwnd_bitmap(hwnd):
    rect = wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
    w = max(1, rect.right - rect.left)
    h = max(1, rect.bottom - rect.top)

    hwndDC = ctypes.windll.user32.GetWindowDC(hwnd)
    mfcDC = ctypes.windll.gdi32.CreateCompatibleDC(hwndDC)
    saveBitMap = ctypes.windll.gdi32.CreateCompatibleBitmap(hwndDC, w, h)
    ctypes.windll.gdi32.SelectObject(mfcDC, saveBitMap)
    ctypes.windll.user32.PrintWindow(hwnd, mfcDC, 2)

    class BITMAPINFOHEADER(ctypes.Structure):
        _fields_ = [
            ("biSize", wintypes.DWORD),
            ("biWidth", wintypes.LONG),
            ("biHeight", wintypes.LONG),
            ("biPlanes", wintypes.WORD),
            ("biBitCount", wintypes.WORD),
            ("biCompression", wintypes.DWORD),
            ("biSizeImage", wintypes.DWORD),
            ("biXPelsPerMeter", wintypes.LONG),
            ("biYPelsPerMeter", wintypes.LONG),
            ("biClrUsed", wintypes.DWORD),
            ("biClrImportant", wintypes.DWORD),
        ]

    bmi = BITMAPINFOHEADER()
    bmi.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bmi.biWidth = w
    bmi.biHeight = -h
    bmi.biPlanes = 1
    bmi.biBitCount = 32
    bmi.biCompression = 0

    buf = ctypes.create_string_buffer(w * h * 4)
    ctypes.windll.gdi32.GetDIBits(mfcDC, saveBitMap, 0, h, buf, ctypes.byref(bmi), 0)

    ctypes.windll.gdi32.DeleteObject(saveBitMap)
    ctypes.windll.gdi32.DeleteDC(mfcDC)
    ctypes.windll.user32.ReleaseDC(hwnd, hwndDC)

    return Image.frombuffer("RGBA", (w, h), buf, "raw", "BGRA", 0, 1).convert("RGB")


def _render_terminal_wx(title_text, clean_lines, out_path, mode, show_cursor, psreadline, scale):
    app = wx.GetApp() or wx.App(False)
    jitter_w, jitter_h = _compute_jitter(clean_lines)

    font_ui = wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI")
    font_term = wx.Font(11, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Cascadia Mono")

    icon_path = _pick_icon_path(title_text, mode, size_px=16)
    icon_bmp = None
    if icon_path:
        im_ic = Image.open(icon_path).convert("RGBA").resize((16, 16), Image.Resampling.LANCZOS)
        icon_bmp = wx.Bitmap.FromBufferRGBA(16, 16, im_ic.tobytes())

    frame = wx.Frame(None, pos=(60, 60), style=wx.BORDER_NONE | wx.FRAME_NO_TASKBAR)
    hwnd_frame = frame.GetHandle()
    GWL_EXSTYLE = -20
    WS_EX_LAYERED = 0x00080000
    WS_EX_NOACTIVATE = 0x08000000
    LWA_ALPHA = 0x00000002
    ex_style = ctypes.windll.user32.GetWindowLongW(hwnd_frame, GWL_EXSTYLE)
    ctypes.windll.user32.SetWindowLongW(
        hwnd_frame, GWL_EXSTYLE, ex_style | WS_EX_LAYERED | WS_EX_NOACTIVATE
    )
    ctypes.windll.user32.SetLayeredWindowAttributes(hwnd_frame, 0, 1, LWA_ALPHA)

    panel = wx.Panel(frame, style=wx.BORDER_NONE)
    panel.SetBackgroundStyle(wx.BG_STYLE_PAINT)

    # Measure line extents accurately using a client DC
    probe_dc = wx.ClientDC(panel)
    probe_dc.SetFont(font_term)
    _, line_h = probe_dc.GetTextExtent("Mg")
    line_step = line_h + 2
    max_line_px = max((probe_dc.GetTextExtent(l)[0] for l in clean_lines), default=240)

    tabbar_h = 40
    pad_x = 9
    pad_y_top = 8
    total_w = max(620, max_line_px + pad_x * 2 + 16 + jitter_w)
    total_h = tabbar_h + max(140, len(clean_lines) * line_step + pad_y_top * 2 + jitter_h)

    def _on_paint(event):
        dc = wx.BufferedPaintDC(panel)
        gc = wx.GraphicsContext.Create(dc)
        w, h = panel.GetSize()

        # 1. Main viewport background + 1px dark window border
        dc.SetBrush(wx.Brush(wx.Colour(*_COLOR_BG)))
        dc.SetPen(wx.Pen(wx.Colour(*_COLOR_BORDER), 1))
        dc.DrawRectangle(0, 0, w, h)

        # 2. Top titlebar / tab strip (#202020)
        dc.SetBrush(wx.Brush(wx.Colour(*_COLOR_TABROW)))
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangle(1, 1, w - 2, tabbar_h)

        # 3. Seamless active tab (#0C0C0C) with rounded top corners
        tab_x, tab_y, tab_w = 8, 7, min(240, max(190, w - 220))
        if gc:
            path = gc.CreatePath()
            r = 6
            path.MoveToPoint(tab_x, tabbar_h + 1)
            path.AddLineToPoint(tab_x, tab_y + r)
            path.AddArcToPoint(tab_x, tab_y, tab_x + r, tab_y, r)
            path.AddLineToPoint(tab_x + tab_w - r, tab_y)
            path.AddArcToPoint(tab_x + tab_w, tab_y, tab_x + tab_w, tab_y + r, r)
            path.AddLineToPoint(tab_x + tab_w, tabbar_h + 1)
            path.CloseSubpath()
            gc.SetBrush(wx.Brush(wx.Colour(*_COLOR_BG)))
            gc.FillPath(path)

        # 4. Tab icon & title
        if icon_bmp:
            dc.DrawBitmap(icon_bmp, tab_x + 12, tab_y + 8, True)

        dc.SetFont(font_ui)
        dc.SetTextForeground(wx.Colour(*_COLOR_TEXT_WHITE))
        disp_title = title_text or "Windows PowerShell"
        max_tw = tab_w - 64
        while len(disp_title) > 6 and dc.GetTextExtent(disp_title)[0] > max_tw:
            disp_title = disp_title[:-4] + "..."
        _, th = dc.GetTextExtent(disp_title)
        dc.DrawText(disp_title, tab_x + 36, tab_y + (32 - th) // 2)

        # Tab close 'x'
        cx, cy = tab_x + tab_w - 18, tab_y + 16
        dc.SetPen(wx.Pen(wx.Colour(190, 190, 190), 1))
        dc.DrawLine(cx - 3, cy - 3, cx + 4, cy + 4)
        dc.DrawLine(cx - 3, cy + 3, cx + 4, cy - 4)

        # 5. Split '+' and 'v' new-tab pill button
        btn_x, btn_y = tab_x + tab_w + 6, tab_y + 4
        if gc:
            gc.SetBrush(wx.Brush(wx.Colour(*_COLOR_PILL_BG)))
            gc.SetPen(wx.TRANSPARENT_PEN)
            gc.DrawRoundedRectangle(btn_x, btn_y, 54, 24, 4)
        px, py = btn_x + 14, btn_y + 12
        dc.SetPen(wx.Pen(wx.Colour(220, 220, 220), 1))
        dc.DrawLine(px - 4, py, px + 5, py)
        dc.DrawLine(px, py - 4, px, py + 5)
        dc.SetPen(wx.Pen(wx.Colour(*_COLOR_PILL_DIV), 1))
        dc.DrawLine(btn_x + 29, btn_y + 4, btn_x + 29, btn_y + 20)
        vx, vy = btn_x + 41, btn_y + 11
        dc.SetPen(wx.Pen(wx.Colour(210, 210, 210), 1))
        dc.DrawLine(vx - 3, vy - 1, vx, vy + 2)
        dc.DrawLine(vx, vy + 2, vx + 4, vy - 2)

        # 6. Windows 11 Caption Controls (Minimize, Maximize, Close)
        cap_w = 46
        dc.SetPen(wx.Pen(wx.Colour(235, 235, 235), 1))
        mx, my = w - cap_w * 3 + cap_w // 2, tabbar_h // 2
        dc.DrawLine(mx - 5, my, mx + 6, my)
        rx, ry = w - cap_w * 2 + cap_w // 2, tabbar_h // 2
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRectangle(rx - 5, ry - 5, 10, 10)
        kx, ky = w - cap_w + cap_w // 2, tabbar_h // 2
        dc.DrawLine(kx - 5, ky - 5, kx + 6, ky + 6)
        dc.DrawLine(kx - 5, ky + 5, kx + 6, ky - 6)

        # 7. Terminal text lines
        dc.SetFont(font_term)
        y_start = tabbar_h + pad_y_top
        last_cursor_pos = None

        for idx, line in enumerate(clean_lines):
            y = y_start + idx * line_step
            x = pad_x
            segs = _split_ps_prompt_line(line) if psreadline else None
            if segs:
                for txt, col in segs:
                    dc.SetTextForeground(wx.Colour(*col))
                    dc.DrawText(txt, x, y)
                    x += dc.GetTextExtent(txt)[0]
            else:
                dc.SetTextForeground(wx.Colour(*_COLOR_FG))
                if line:
                    dc.DrawText(line, x, y)
                    x += dc.GetTextExtent(line)[0]
            if idx == len(clean_lines) - 1:
                last_cursor_pos = (x, y)

        # 8. Authentic Windows Terminal bar cursor '|'
        if show_cursor and last_cursor_pos is not None:
            cx_pos, cy_pos = last_cursor_pos
            dc.SetPen(wx.Pen(wx.Colour(*_COLOR_CURSOR), 2))
            dc.DrawLine(cx_pos + 1, cy_pos + 1, cx_pos + 1, cy_pos + line_h - 1)

        # 9. Subtle Windows 11 scrollbar thumb on right edge
        sb_h = h - tabbar_h - 12
        if sb_h > 50 and len(clean_lines) > 8 and gc:
            gc.SetBrush(wx.Brush(wx.Colour(*_COLOR_SCROLL_THUMB)))
            gc.SetPen(wx.TRANSPARENT_PEN)
            thumb_h = max(28, int(sb_h * 0.45))
            gc.DrawRoundedRectangle(w - 8, tabbar_h + 6 + (sb_h - thumb_h), 3, thumb_h, 1.5)

    panel.Bind(wx.EVT_PAINT, _on_paint)
    frame.SetSize((total_w, total_h))
    panel.SetSize((total_w, total_h))
    frame.Show()

    def _on_timer():
        frame.Refresh()
        frame.Update()
        img = _capture_hwnd_bitmap(frame.GetHandle())
        if scale and scale != 1.0:
            new_w = max(1, int(img.width * scale))
            new_h = max(1, int(img.height * scale))
            img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        img.save(out_path)
        frame.Destroy()

    wx.CallLater(120, _on_timer)
    app.MainLoop()
    return out_path


def _load_pil_font(candidates, size):
    for cand in candidates:
        try:
            return ImageFont.truetype(cand, size)
        except Exception:
            continue
    return ImageFont.load_default()


def _render_terminal_pillow(title_text, clean_lines, out_path, mode, show_cursor, psreadline, scale):
    """Cross-platform Pillow fallback renderer reproducing Windows 11 PowerShell UI."""
    jitter_w, jitter_h = _compute_jitter(clean_lines)

    font_ui = _load_pil_font(
        [
            r"C:\Windows\Fonts\segoeui.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "segoeui.ttf",
        ],
        12,
    )
    font_term = _load_pil_font(
        [
            r"C:\Windows\Fonts\CascadiaMono.ttf",
            r"C:\Windows\Fonts\consola.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
            "DejaVuSansMono.ttf",
        ],
        15,
    )

    probe_img = Image.new("RGB", (10, 10))
    probe_draw = ImageDraw.Draw(probe_img)
    bbox = probe_draw.textbbox((0, 0), "Mg", font=font_term)
    line_h = max(16, bbox[3] - bbox[1])
    line_step = line_h + 4
    max_line_px = max(
        (probe_draw.textlength(l, font=font_term) for l in clean_lines),
        default=240,
    )

    tabbar_h = 40
    pad_x = 10
    pad_y_top = 8
    total_w = max(620, int(max_line_px) + pad_x * 2 + 16 + jitter_w)
    total_h = tabbar_h + max(140, len(clean_lines) * line_step + pad_y_top * 2 + jitter_h)

    img = Image.new("RGB", (total_w, total_h), _COLOR_BG)
    draw = ImageDraw.Draw(img)

    # Top tab strip & border
    draw.rectangle([0, 0, total_w - 1, tabbar_h], fill=_COLOR_TABROW)
    draw.rectangle([0, 0, total_w - 1, total_h - 1], outline=_COLOR_BORDER, width=1)

    # Seamless active tab
    tab_x, tab_y, tab_w = 8, 7, min(240, max(190, total_w - 220))
    draw.rounded_rectangle([tab_x, tab_y, tab_x + tab_w, tabbar_h + 6], radius=6, fill=_COLOR_BG)

    icon_path = _pick_icon_path(title_text, mode, size_px=16)
    if icon_path:
        try:
            with Image.open(icon_path).convert("RGBA") as ic:
                ic = ic.resize((16, 16), Image.Resampling.LANCZOS)
                img.paste(ic, (tab_x + 12, tab_y + 8), ic)
        except Exception:
            pass

    disp_title = title_text or "Windows PowerShell"
    max_tw = tab_w - 64
    while len(disp_title) > 6 and draw.textlength(disp_title, font=font_ui) > max_tw:
        disp_title = disp_title[:-4] + "..."
    draw.text((tab_x + 36, tab_y + 8), disp_title, fill=_COLOR_TEXT_WHITE, font=font_ui)

    # Tab close 'x'
    cx, cy = tab_x + tab_w - 18, tab_y + 16
    draw.line([(cx - 3, cy - 3), (cx + 4, cy + 4)], fill=(190, 190, 190), width=1)
    draw.line([(cx - 3, cy + 3), (cx + 4, cy - 4)], fill=(190, 190, 190), width=1)

    # Split '+' and 'v' pill
    btn_x, btn_y = tab_x + tab_w + 6, tab_y + 4
    draw.rounded_rectangle([btn_x, btn_y, btn_x + 54, btn_y + 24], radius=4, fill=_COLOR_PILL_BG)
    px, py = btn_x + 14, btn_y + 12
    draw.line([(px - 4, py), (px + 5, py)], fill=(220, 220, 220), width=1)
    draw.line([(px, py - 4), (px, py + 5)], fill=(220, 220, 220), width=1)
    draw.line([(btn_x + 29, btn_y + 4), (btn_x + 29, btn_y + 20)], fill=_COLOR_PILL_DIV, width=1)
    vx, vy = btn_x + 41, btn_y + 11
    draw.line([(vx - 3, vy - 1), (vx, vy + 2), (vx + 4, vy - 2)], fill=(210, 210, 210), width=1)

    # Win11 caption controls
    cap_w = 46
    mx, my = total_w - cap_w * 3 + cap_w // 2, tabbar_h // 2
    draw.line([(mx - 5, my), (mx + 6, my)], fill=(235, 235, 235), width=1)
    rx, ry = total_w - cap_w * 2 + cap_w // 2, tabbar_h // 2
    draw.rectangle([rx - 5, ry - 5, rx + 5, ry + 5], outline=(235, 235, 235), width=1)
    kx, ky = total_w - cap_w + cap_w // 2, tabbar_h // 2
    draw.line([(kx - 5, ky - 5), (kx + 6, ky + 6)], fill=(235, 235, 235), width=1)
    draw.line([(kx - 5, ky + 5), (kx + 6, ky - 6)], fill=(235, 235, 235), width=1)

    # Terminal lines
    y_start = tabbar_h + pad_y_top
    last_cursor_pos = None
    for idx, line in enumerate(clean_lines):
        y = y_start + idx * line_step
        x = pad_x
        segs = _split_ps_prompt_line(line) if psreadline else None
        if segs:
            for txt, col in segs:
                draw.text((x, y), txt, fill=col, font=font_term)
                x += int(draw.textlength(txt, font=font_term))
        else:
            if line:
                draw.text((x, y), line, fill=_COLOR_FG, font=font_term)
                x += int(draw.textlength(line, font=font_term))
        if idx == len(clean_lines) - 1:
            last_cursor_pos = (x, y)

    if show_cursor and last_cursor_pos is not None:
        cx_pos, cy_pos = last_cursor_pos
        draw.line([(cx_pos + 1, cy_pos + 1), (cx_pos + 1, cy_pos + line_h - 1)], fill=_COLOR_CURSOR, width=2)

    sb_h = total_h - tabbar_h - 12
    if sb_h > 50 and len(clean_lines) > 8:
        thumb_h = max(28, int(sb_h * 0.45))
        draw.rounded_rectangle(
            [total_w - 8, tabbar_h + 6 + (sb_h - thumb_h), total_w - 5, tabbar_h + 6 + sb_h],
            radius=1,
            fill=_COLOR_SCROLL_THUMB,
        )

    if scale and scale != 1.0:
        new_w = max(1, int(img.width * scale))
        new_h = max(1, int(img.height * scale))
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    img.save(out_path)
    return out_path


def render_terminal_output(
    title_text="Windows PowerShell",
    lines=(),
    out_path="terminal_shot.png",
    mode="powershell",
    show_cursor=True,
    psreadline=True,
    scale=1.0,
    force_pillow=False,
):
    """
    Renders a 1-to-1 Windows 11 PowerShell (Windows Terminal) screenshot
    without artificial badge/color styles. Uses native Win32/wxPython GDI
    on Windows with automatic Pillow fallback on non-Windows/headless hosts.
    """
    out_path = os.path.abspath(out_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    clean_lines = [strip_terminal_tokens(l) for l in (lines or [])]
    if not clean_lines:
        clean_lines = [""]

    if HAS_WX and sys.platform == "win32" and not force_pillow:
        try:
            return _render_terminal_wx(
                title_text, clean_lines, out_path, mode, show_cursor, psreadline, scale
            )
        except Exception:
            pass

    return _render_terminal_pillow(
        title_text, clean_lines, out_path, mode, show_cursor, psreadline, scale
    )


__all__ = [
    "render_terminal_output",
    "format_terminal_line",
    "strip_terminal_tokens",
    "HAS_WX",
]
