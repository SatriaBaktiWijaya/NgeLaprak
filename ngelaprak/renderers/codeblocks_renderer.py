import os
import io
import zipfile
import ctypes
from ctypes import wintypes
import xml.etree.ElementTree as ET
import random
import wx
import wx.stc as stc
import wx.aui as aui
from PIL import Image

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    pass

CODEBLOCKS_SHARE_DIR = r"C:\Program Files\CodeBlocks\share\CodeBlocks"
CODEBLOCKS_LEXER_XML = os.path.join(CODEBLOCKS_SHARE_DIR, "lexers", "lexer_cpp.xml")
CODEBLOCKS_RES_ZIP = os.path.join(CODEBLOCKS_SHARE_DIR, "resources.zip")
CODEBLOCKS_COMPILER_ZIP = os.path.join(CODEBLOCKS_SHARE_DIR, "compiler.zip")

FALLBACK_STYLES = [
    {"indices": [0, 11], "fg": (0, 0, 0), "bg": (255, 255, 255), "bold": False, "italics": False, "underlined": False},
    {"indices": [1, 2, 23], "fg": (152, 152, 217), "bg": None, "bold": False, "italics": False, "underlined": False},
    {"indices": [3, 15, 24], "fg": (128, 128, 255), "bg": None, "bold": True, "italics": False, "underlined": False},
    {"indices": [17], "fg": (0, 128, 128), "bg": None, "bold": False, "italics": False, "underlined": False},
    {"indices": [4], "fg": (240, 0, 240), "bg": None, "bold": False, "italics": False, "underlined": False},
    {"indices": [5], "fg": (0, 0, 160), "bg": None, "bold": True, "italics": False, "underlined": False},
    {"indices": [16], "fg": (0, 160, 0), "bg": None, "bold": True, "italics": False, "underlined": False},
    {"indices": [19], "fg": (190, 0, 190), "bg": None, "bold": True, "italics": False, "underlined": False},
    {"indices": [6, 12, 20], "fg": (0, 0, 255), "bg": None, "bold": False, "italics": False, "underlined": False},
    {"indices": [7], "fg": (224, 160, 0), "bg": None, "bold": False, "italics": False, "underlined": False},
    {"indices": [9], "fg": (0, 160, 0), "bg": None, "bold": False, "italics": False, "underlined": False},
    {"indices": [10], "fg": (255, 0, 0), "bg": None, "bold": False, "italics": False, "underlined": False},
]

FALLBACK_KEYWORDS = {
    0: "alignas alignof asm auto bool break case catch char char16_t char32_t class const const_cast constexpr continue decltype default delete do double dynamic_cast else enum explicit export extern false final float for friend goto if inline int long mutable namespace new noexcept nullptr operator override private protected public register reinterpret_cast return short signed sizeof static static_assert static_cast struct switch template this thread_local throw true try typedef typeid typename union unsigned using virtual void volatile wchar_t while size_t time_t",
    1: "std vector string cout cin endl cerr pair make_pair map set list queue stack deque empty size begin end push_back pop_back clear length c_str substr find getline iostream fstream sstream algorithm cmath cstdio cstdlib cstring iomanip",
}


def _parse_cb_lexer_xml(xml_path=CODEBLOCKS_LEXER_XML):
    if not os.path.exists(xml_path):
        return FALLBACK_STYLES, FALLBACK_KEYWORDS
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        lexer = root.find("Lexer")
        styles = []
        for st in lexer.findall("Style"):
            idx_str = st.attrib.get("index", "")
            indices = [int(x) for x in idx_str.split(",") if x.strip().lstrip("-").isdigit()]
            fg = st.attrib.get("fg")
            bg = st.attrib.get("bg")
            styles.append({
                "indices": indices,
                "fg": tuple(int(c) for c in fg.split(",")) if fg else None,
                "bg": tuple(int(c) for c in bg.split(",")) if bg else None,
                "bold": st.attrib.get("bold") == "1",
                "italics": st.attrib.get("italics") == "1",
                "underlined": st.attrib.get("underlined") == "1",
            })
        keywords = {}
        kw_node = lexer.find("Keywords")
        if kw_node is not None:
            for s in kw_node.findall("Set"):
                idx = int(s.attrib["index"])
                val = " ".join(s.attrib.get("value", "").split())
                keywords[idx] = val
        return styles, keywords
    except Exception:
        return FALLBACK_STYLES, FALLBACK_KEYWORDS


def _load_wx_bitmap_from_zip(zip_path, entry_name):
    if not os.path.exists(zip_path):
        return None
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            if entry_name in zf.namelist():
                data = zf.read(entry_name)
                wx_img = wx.Image(io.BytesIO(data), wx.BITMAP_TYPE_PNG)
                if wx_img.IsOk():
                    return wx.Bitmap(wx_img)
    except Exception:
        pass
    return None


def _capture_hwnd_bitmap(hwnd, include_nonclient=False):
    rect = wintypes.RECT()
    if include_nonclient:
        ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
    else:
        ctypes.windll.user32.GetClientRect(hwnd, ctypes.byref(rect))
    w = max(1, rect.right - rect.left)
    h = max(1, rect.bottom - rect.top)

    hwndDC = ctypes.windll.user32.GetWindowDC(hwnd) if include_nonclient else ctypes.windll.user32.GetDC(hwnd)
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
    img = Image.frombuffer("RGBA", (w, h), buf, "raw", "BGRA", 0, 1).convert("RGB")

    ctypes.windll.gdi32.DeleteObject(saveBitMap)
    ctypes.windll.gdi32.DeleteDC(mfcDC)
    ctypes.windll.user32.ReleaseDC(hwnd, hwndDC)
    return img


def _configure_scintilla_editor(ed, full_slice_text, start_line, end_line, with_cursor, show_vscroll=False, caret_line=None):
    ed.SetLexer(stc.STC_LEX_CPP)
    font = wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Courier New")
    ed.StyleSetFont(stc.STC_STYLE_DEFAULT, font)
    ed.StyleClearAll()

    styles, keywords = _parse_cb_lexer_xml(CODEBLOCKS_LEXER_XML)
    for st in styles:
        for idx in st["indices"]:
            if idx < 0:
                continue
            ed.StyleSetFont(idx, font)
            if st["fg"]:
                ed.StyleSetForeground(idx, wx.Colour(*st["fg"]))
            if st["bg"]:
                ed.StyleSetBackground(idx, wx.Colour(*st["bg"]))
            ed.StyleSetBold(idx, st["bold"])
            ed.StyleSetItalic(idx, st["italics"])
            ed.StyleSetUnderline(idx, st["underlined"])

    for kw_idx, kw_val in keywords.items():
        ed.SetKeyWords(kw_idx, kw_val)

    ed.SetProperty("fold", "1")
    ed.SetProperty("fold.compact", "0")
    ed.SetProperty("fold.comment", "1")
    ed.SetProperty("fold.preprocessor", "1")

    ed.SetMarginType(0, stc.STC_MARGIN_NUMBER)
    ed.SetMarginWidth(0, ed.TextWidth(stc.STC_STYLE_LINENUMBER, f"_{max(99, end_line)}"))
    ed.StyleSetFont(stc.STC_STYLE_LINENUMBER, font)
    ed.StyleSetForeground(stc.STC_STYLE_LINENUMBER, wx.Colour(100, 100, 100))
    ed.StyleSetBackground(stc.STC_STYLE_LINENUMBER, wx.Colour(240, 240, 240))

    ed.SetMarginType(1, stc.STC_MARGIN_SYMBOL)
    ed.SetMarginWidth(1, 0)

    ed.SetMarginType(2, stc.STC_MARGIN_SYMBOL)
    ed.SetMarginWidth(2, 4)
    ed.SetMarginMask(2, 1 << 24)
    ed.MarkerDefine(24, stc.STC_MARK_FULLRECT, wx.Colour(0, 224, 0), wx.Colour(0, 224, 0))

    ed.SetMarginType(3, stc.STC_MARGIN_SYMBOL)
    ed.SetMarginMask(3, stc.STC_MASK_FOLDERS)
    ed.SetMarginWidth(3, 16)
    ed.SetFoldMarginColour(True, wx.Colour(240, 240, 240))
    ed.SetFoldMarginHiColour(True, wx.Colour(240, 240, 240))

    fg_fold = wx.Colour(255, 255, 255)
    bg_fold = wx.Colour(128, 128, 128)
    ed.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_BOXMINUS, fg_fold, bg_fold)
    ed.MarkerDefine(stc.STC_MARKNUM_FOLDER, stc.STC_MARK_BOXPLUS, fg_fold, bg_fold)
    ed.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_VLINE, fg_fold, bg_fold)
    ed.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, stc.STC_MARK_LCORNER, fg_fold, bg_fold)
    ed.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, stc.STC_MARK_BOXPLUSCONNECTED, fg_fold, bg_fold)
    ed.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_BOXMINUSCONNECTED, fg_fold, bg_fold)
    ed.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNER, fg_fold, bg_fold)

    ed.SetIndentationGuides(stc.STC_IV_LOOKBOTH)
    ed.SetUseHorizontalScrollBar(False)
    ed.SetUseVerticalScrollBar(show_vscroll)
    ed.SetCaretPeriod(0)
    ed.SetCaretWidth(1 if with_cursor else 0)

    ed.SetText(full_slice_text)
    ed.Colourise(0, -1)

    for ln in range(end_line):
        ed.MarkerAdd(ln, 24)

    target_ln = (caret_line - 1) if caret_line is not None else (end_line - 1)
    target_ln = max(0, min(end_line - 1, target_ln))
    target_pos = ed.GetLineEndPosition(target_ln)
    ed.SetCurrentPos(target_pos)
    ed.SetSelection(target_pos, target_pos)

    if start_line > 1:
        ed.SetFirstVisibleLine(start_line - 1)
    else:
        ed.SetFirstVisibleLine(0)


def _build_full_codeblocks_frame(frame, full_slice_text, start_line, end_line, with_cursor, filename, project_name, extra_files=None, show_vscroll=False, caret_line=None):
    """Builds an authentic Code::Blocks 25.03 IDE frame using native wxWidgets & Code::Blocks assets."""
    cb_icon = _load_wx_bitmap_from_zip(CODEBLOCKS_RES_ZIP, "images/codeblocks.png")
    if cb_icon:
        icon = wx.Icon()
        icon.CopyFromBitmap(cb_icon)
        frame.SetIcon(icon)

    frame.SetTitle(f"{filename} [{project_name}] - Code::Blocks 25.03")

    # 1. Native Win32 MenuBar
    mb = wx.MenuBar()
    for label in ["&File", "&Edit", "&View", "&Search", "&Project", "&Build", "&Debug", "F&ortran", "&wxSmith", "&Tools", "&Plugins", "&Settings", "&Help"]:
        mb.Append(wx.Menu(), label)
    frame.SetMenuBar(mb)

    # 2. Native Win32 ToolBar with official Code::Blocks PNG icons
    tb = frame.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)
    tb.SetToolBitmapSize((20, 20))
    main_tools = [
        (CODEBLOCKS_RES_ZIP, "images/20x20/filenew.png", "New file"),
        (CODEBLOCKS_RES_ZIP, "images/20x20/fileopen.png", "Open"),
        (CODEBLOCKS_RES_ZIP, "images/20x20/filesave.png", "Save"),
        (CODEBLOCKS_RES_ZIP, "images/20x20/filesaveall.png", "Save everything"),
        None,
        (CODEBLOCKS_RES_ZIP, "images/20x20/undo.png", "Undo"),
        (CODEBLOCKS_RES_ZIP, "images/20x20/redo.png", "Redo"),
        None,
        (CODEBLOCKS_RES_ZIP, "images/20x20/editcut.png", "Cut"),
        (CODEBLOCKS_RES_ZIP, "images/20x20/editcopy.png", "Copy"),
        (CODEBLOCKS_RES_ZIP, "images/20x20/editpaste.png", "Paste"),
        None,
        (CODEBLOCKS_RES_ZIP, "images/20x20/filefind.png", "Find"),
        (CODEBLOCKS_RES_ZIP, "images/20x20/searchreplace.png", "Replace"),
        None,
        (CODEBLOCKS_COMPILER_ZIP, "images/20x20/compile.png", "Build"),
        (CODEBLOCKS_COMPILER_ZIP, "images/20x20/run.png", "Run"),
        (CODEBLOCKS_COMPILER_ZIP, "images/20x20/compilerun.png", "Build and run"),
        (CODEBLOCKS_COMPILER_ZIP, "images/20x20/rebuild.png", "Rebuild"),
        (CODEBLOCKS_COMPILER_ZIP, "images/20x20/stop.png", "Abort"),
    ]
    for item in main_tools:
        if item is None:
            tb.AddSeparator()
        else:
            bmp = _load_wx_bitmap_from_zip(item[0], item[1])
            if bmp:
                tb.AddTool(wx.ID_ANY, item[2], bmp, item[2])
    tb.Realize()

    # 3. Native wxAuiManager + Management Pane + Editor AuiNotebook
    mgr = aui.AuiManager(frame)

    mgmt_nb = aui.AuiNotebook(frame, style=aui.AUI_NB_TOP | aui.AUI_NB_TAB_MOVE)
    tree = wx.TreeCtrl(mgmt_nb, style=wx.TR_DEFAULT_STYLE | wx.TR_HAS_BUTTONS)
    il = wx.ImageList(16, 16)
    bmp_ws = _load_wx_bitmap_from_zip(CODEBLOCKS_RES_ZIP, "images/codeblocks.png")
    bmp_folder = _load_wx_bitmap_from_zip(CODEBLOCKS_RES_ZIP, "images/folder.png")
    bmp_src = _load_wx_bitmap_from_zip(CODEBLOCKS_RES_ZIP, "images/source.png")
    idx_ws = il.Add(bmp_ws.ConvertToImage().Rescale(16, 16).ConvertToBitmap()) if bmp_ws else -1
    idx_fld = il.Add(bmp_folder.ConvertToImage().Rescale(16, 16).ConvertToBitmap()) if bmp_folder else -1
    idx_src = il.Add(bmp_src.ConvertToImage().Rescale(16, 16).ConvertToBitmap()) if bmp_src else -1
    tree.AssignImageList(il)

    root_id = tree.AddRoot("Workspace", idx_ws)
    proj_id = tree.AppendItem(root_id, project_name, idx_ws)
    tree.SetItemBold(proj_id, True)
    files = list(extra_files) if extra_files else [filename]
    if filename not in files:
        files.append(filename)
    headers = [f for f in files if f.lower().endswith((".h", ".hpp"))]
    sources = [f for f in files if f not in headers]
    if sources:
        src_node = tree.AppendItem(proj_id, "Sources", idx_fld)
        for f in sources:
            item_id = tree.AppendItem(src_node, f, idx_src)
            if f == filename:
                tree.SelectItem(item_id)
    if headers:
        hdr_node = tree.AppendItem(proj_id, "Headers", idx_fld)
        for f in headers:
            item_id = tree.AppendItem(hdr_node, f, idx_src)
            if f == filename:
                tree.SelectItem(item_id)
    tree.ExpandAll()

    mgmt_nb.AddPage(tree, "Projects", True)
    mgmt_nb.AddPage(wx.Panel(mgmt_nb), "Symbols", False)
    mgmt_nb.AddPage(wx.Panel(mgmt_nb), "Files", False)

    ed_nb = aui.AuiNotebook(frame, style=aui.AUI_NB_TOP | aui.AUI_NB_CLOSE_ON_ACTIVE_TAB)
    ed = stc.StyledTextCtrl(ed_nb, style=wx.BORDER_NONE)
    _configure_scintilla_editor(ed, full_slice_text, start_line, end_line, with_cursor, show_vscroll=show_vscroll, caret_line=caret_line)
    ed_nb.AddPage(ed, filename, True)

    mgr.AddPane(
        mgmt_nb,
        aui.AuiPaneInfo().Name("Management").Caption("Management").Left().BestSize((235, -1)).MinSize((215, -1)).CloseButton(True),
    )
    mgr.AddPane(ed_nb, aui.AuiPaneInfo().Name("Editor").CenterPane())
    mgr.Update()

    # 4. Native Win32 StatusBar
    sb = frame.CreateStatusBar(5)
    sb.SetStatusWidths([-2, 135, 80, 125, 80])
    sb.SetStatusText(f"  {filename}", 0)
    sb.SetStatusText("Windows (CR+LF)", 1)
    sb.SetStatusText("UTF-8", 2)
    lines_arr = full_slice_text.splitlines()
    eff_ln = caret_line if caret_line is not None else end_line
    eff_idx = max(0, min(len(lines_arr) - 1, eff_ln - 1)) if lines_arr else 0
    last_line_len = len(lines_arr[eff_idx]) + 1 if lines_arr else 1
    sb.SetStatusText(f"Line {eff_ln}, Col {last_line_len}", 3)
    sb.SetStatusText("Insert", 4)

    return ed, mgr


def render_codeblocks_code(
    code_text,
    start_line=1,
    end_line=None,
    out_path="codeblocks_shot.png",
    with_cursor=True,
    author_tag=None,
    view="editor",
    filename="main.cpp",
    project_name="ProjekPraktikum",
    extra_files=None,
):
    """
    Renders a 100% pixel-perfect Code::Blocks C/C++ screenshot using native wxScintilla + Win32 GDI
    and official Code::Blocks lexer_cpp.xml styles and folding markers.
    Supports view='editor' (cropped code + gutter) or view='full' (complete native wxWidgets Code::Blocks IDE window).
    """
    out_path = os.path.abspath(out_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    if author_tag and start_line == 1 and not code_text.strip().startswith("//"):
        code_text = f"// @author {author_tag}\n" + code_text

    all_lines = code_text.splitlines() or [""]
    if end_line is None or end_line > len(all_lines):
        end_line = len(all_lines)

    slice_lines = all_lines[start_line - 1 : end_line]
    if not slice_lines:
        slice_lines = [""]

    full_slice_text = "\n".join(all_lines[:end_line])
    visible_count = len(slice_lines)

    app = wx.GetApp() or wx.App(False)

    is_full = (view == "full")
    frame_style = (
        (wx.DEFAULT_FRAME_STYLE | wx.FRAME_NO_TASKBAR)
        if is_full
        else (wx.NO_BORDER | wx.FRAME_NO_TASKBAR)
    )
    frame = wx.Frame(None, pos=(80, 80), size=(1000, 700), style=frame_style)

    hwnd_frame = frame.GetHandle()
    GWL_EXSTYLE = -20
    WS_EX_LAYERED = 0x00080000
    WS_EX_NOACTIVATE = 0x08000000
    LWA_ALPHA = 0x00000002
    ex_style = ctypes.windll.user32.GetWindowLongW(hwnd_frame, GWL_EXSTYLE)
    ctypes.windll.user32.SetWindowLongW(hwnd_frame, GWL_EXSTYLE, ex_style | WS_EX_LAYERED | WS_EX_NOACTIVATE)
    ctypes.windll.user32.SetLayeredWindowAttributes(hwnd_frame, 0, 1, LWA_ALPHA)

    screen_w = ctypes.windll.user32.GetSystemMetrics(0)
    screen_h = ctypes.windll.user32.GetSystemMetrics(1)
    max_win_w = max(980, screen_w - 80)
    max_win_h = max(620, screen_h - 60)

    # Probe exact Scintilla metrics dynamically
    aui_mgr = None
    if is_full:
        ed, aui_mgr = _build_full_codeblocks_frame(
            frame, full_slice_text, start_line, end_line, with_cursor, filename, project_name, extra_files=extra_files
        )
        probe_h = max(14, ed.TextHeight(0))
        desired_h = probe_h * visible_count + 195 + random.randint(4, 12)
        if desired_h > max_win_h:
            ed.SetUseVerticalScrollBar(True)
            vis_fit = max(10, (max_win_h - 195) // probe_h)
            caret_ln = min(end_line, start_line + vis_fit - 1)
            tpos = ed.GetLineEndPosition(caret_ln - 1)
            ed.SetCurrentPos(tpos)
            ed.SetSelection(tpos, tpos)
            lines_arr = full_slice_text.splitlines()
            clen = len(lines_arr[caret_ln - 1]) + 1 if 0 <= caret_ln - 1 < len(lines_arr) else 1
            frame.GetStatusBar().SetStatusText(f"Line {caret_ln}, Col {clen}", 3)
    else:
        ed = stc.StyledTextCtrl(frame, size=(1000, 1000), style=wx.BORDER_NONE)
        _configure_scintilla_editor(ed, full_slice_text, start_line, end_line, with_cursor)

    line_h = ed.TextHeight(0)
    jitter_w = random.randint(24, 52)
    jitter_h = random.randint(8, 16)
    max_line_px = max((ed.TextWidth(0, l.replace("\t", "    ")) for l in slice_lines), default=200)

    if is_full:
        win_w = min(max_win_w, max(980, max_line_px + 380 + jitter_w))
        win_h = min(max_win_h, max(560, line_h * visible_count + 195 + jitter_h))
        frame.SetSize((win_w, win_h))
    else:
        total_h = line_h * visible_count + jitter_h
        max_w = max(360, max_line_px + 100 + jitter_w)
        frame.SetSize((max_w, total_h))
        ed.SetSize((max_w, total_h))

    frame.Show()

    def _on_timer():
        if start_line > 1:
            ed.SetFirstVisibleLine(start_line - 1)
        frame.Layout()
        ed.Refresh()
        ed.Update()
        if is_full:
            WM_NCACTIVATE = 0x0086
            ctypes.windll.user32.SendMessageW(frame.GetHandle(), WM_NCACTIVATE, 1, 0)
            frame.Refresh()
            frame.Update()
            img = _capture_hwnd_bitmap(frame.GetHandle(), include_nonclient=True)
            # Trim invisible 7px Windows 11 DWM drop-shadow margin on left/right/bottom
            if img.width > 20 and img.height > 20:
                img = img.crop((7, 0, img.width - 7, img.height - 7))
        else:
            img = _capture_hwnd_bitmap(ed.GetHandle(), include_nonclient=False)
        img.save(out_path)
        if aui_mgr is not None:
            aui_mgr.UnInit()
        frame.Destroy()

    wx.CallLater(140, _on_timer)
    app.MainLoop()
    return out_path
