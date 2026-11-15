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


def _load_wx_bitmap(zip_filename, entry_name, fallback_art=None, size=(20, 20)):
    zip_path = os.path.join(CODEBLOCKS_SHARE_DIR, zip_filename)
    if os.path.exists(zip_path):
        try:
            with zipfile.ZipFile(zip_path, "r") as zf:
                if entry_name in zf.namelist():
                    data = zf.read(entry_name)
                    img = wx.Image(io.BytesIO(data), wx.BITMAP_TYPE_PNG)
                    if img.IsOk():
                        if size and (img.GetWidth() != size[0] or img.GetHeight() != size[1]):
                            img.Rescale(size[0], size[1], wx.IMAGE_QUALITY_HIGH)
                        return wx.Bitmap(img)
        except Exception:
            pass
    if fallback_art:
        bmp = wx.ArtProvider.GetBitmap(fallback_art, wx.ART_TOOLBAR, size)
        if bmp.IsOk():
            return bmp
    bmp = wx.Bitmap(size[0], size[1])
    dc = wx.MemoryDC(bmp)
    dc.SetBackground(wx.Brush(wx.Colour(240, 240, 240)))
    dc.Clear()
    dc.SelectObject(wx.NullBitmap)
    return bmp


def _load_wx_bitmap_from_zip(zip_path, entry_name):
    """Backwards-compatible zip loader."""
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


def _configure_scintilla_editor(
    ed,
    full_slice_text,
    start_line,
    end_line,
    with_cursor,
    show_vscroll=False,
    caret_line=1,
    caret_col=1,
    show_changebar=False,
):
    ed.SetLexer(stc.STC_LEX_CPP)
    font = wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Courier New")
    ed.StyleSetFont(stc.STC_STYLE_DEFAULT, font)
    ed.StyleClearAll()

    # Font quality for subpixel LCD ClearType
    try:
        ed.SetFontQuality(stc.STC_EFF_QUALITY_LCD_OPTIMIZED)
    except Exception:
        pass

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

    # Margin 0: Line Numbers
    ed.SetMarginType(0, stc.STC_MARGIN_NUMBER)
    ed.SetMarginWidth(0, ed.TextWidth(stc.STC_STYLE_LINENUMBER, f"_{max(99, end_line)}"))
    ed.StyleSetFont(stc.STC_STYLE_LINENUMBER, font)
    ed.StyleSetForeground(stc.STC_STYLE_LINENUMBER, wx.Colour(128, 128, 128))
    ed.StyleSetBackground(stc.STC_STYLE_LINENUMBER, wx.Colour(240, 240, 240))

    # Margin 1: Symbol Margin
    ed.SetMarginType(1, stc.STC_MARGIN_SYMBOL)
    ed.SetMarginWidth(1, 0)

    # Margin 2: Changebar (Disabled by default for clean margin; active when show_changebar=True)
    ed.SetMarginType(2, stc.STC_MARGIN_SYMBOL)
    if show_changebar:
        ed.SetMarginWidth(2, 4)
        ed.SetMarginMask(2, 1 << 24)
        ed.MarkerDefine(24, stc.STC_MARK_FULLRECT, wx.Colour(0, 224, 0), wx.Colour(0, 224, 0))
    else:
        ed.SetMarginWidth(2, 0)

    # Margin 3: Square Box Fold Margin & Fold Guide Lines
    ed.SetMarginType(3, stc.STC_MARGIN_SYMBOL)
    ed.SetMarginMask(3, stc.STC_MASK_FOLDERS)
    ed.SetMarginWidth(3, 16)
    ed.SetMarginSensitive(3, True)
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

    # Caret properties: sharp solid 1px vertical black caret
    ed.SetCaretPeriod(0)
    ed.SetCaretWidth(1 if with_cursor else 0)
    ed.SetCaretForeground(wx.Colour(0, 0, 0))

    ed.SetText(full_slice_text)
    ed.Colourise(0, -1)

    if show_changebar:
        for ln in range(end_line):
            ed.MarkerAdd(ln, 24)

    # Calculate caret position matching caret_line / caret_col
    all_lines = full_slice_text.splitlines() or [""]
    c_line = max(1, min(len(all_lines), caret_line if caret_line is not None else 1))
    target_ln = c_line - 1
    line_start = ed.PositionFromLine(target_ln)
    line_end = ed.GetLineEndPosition(target_ln)
    c_col = max(1, caret_col if caret_col is not None else 1)
    target_pos = min(line_end, line_start + (c_col - 1))
    ed.SetCurrentPos(target_pos)
    ed.SetSelection(target_pos, target_pos)

    if start_line > 1:
        ed.SetFirstVisibleLine(start_line - 1)
    else:
        ed.SetFirstVisibleLine(0)

    return target_pos


def _build_full_codeblocks_frame(
    frame,
    full_slice_text,
    start_line,
    end_line,
    with_cursor,
    filename,
    project_name,
    extra_files=None,
    show_vscroll=False,
    caret_line=1,
    caret_col=1,
    show_bottom_dock=True,
    show_changebar=False,
):
    """Builds an authentic Code::Blocks 25.03 IDE frame matching 1:1 reference."""
    # 1. 3D Cube Icon & Window Title
    cb_icon = _load_wx_bitmap("resources.zip", "images/codeblocks.png", size=(16, 16))
    if cb_icon and cb_icon.IsOk():
        icon = wx.Icon()
        icon.CopyFromBitmap(cb_icon)
        frame.SetIcon(icon)

    frame.SetTitle(f"{filename} [{project_name}] - Code::Blocks 25.03")

    # 2. Exactly 15-Item MenuBar
    mb = wx.MenuBar()
    cb_menus = [
        "&File",
        "&Edit",
        "&View",
        "Sea&rch",
        "&Project",
        "&Build",
        "&Debug",
        "F&ortran",
        "&wxSmith",
        "&Tools",
        "Tools+",
        "P&lugins",
        "DoxyBlocks",
        "&Settings",
        "&Help",
    ]
    for label in cb_menus:
        mb.Append(wx.Menu(), label)
    frame.SetMenuBar(mb)

    # 3. Native wxAuiManager
    mgr = aui.AuiManager(frame)

    # 3.1 Row 0 Toolbars: Main Toolbar, Compiler Toolbar, Debugger Toolbar
    # --- Main Toolbar ---
    tb_main = aui.AuiToolBar(frame, -1, style=aui.AUI_TB_DEFAULT_STYLE | aui.AUI_TB_GRIPPER)
    tb_main.SetToolBitmapSize((20, 20))
    main_tools = [
        ("resources.zip", "images/20x20/filenew.png", "New file", wx.ART_NEW),
        ("resources.zip", "images/20x20/fileopen.png", "Open", wx.ART_FILE_OPEN),
        ("resources.zip", "images/20x20/filesave.png", "Save", wx.ART_FILE_SAVE),
        ("resources.zip", "images/20x20/filesaveall.png", "Save all", wx.ART_FILE_SAVE),
        ("resources.zip", "images/20x20/fileclose.png", "Close", wx.ART_QUIT),
        None,
        ("resources.zip", "images/20x20/undo.png", "Undo", wx.ART_UNDO),
        ("resources.zip", "images/20x20/redo.png", "Redo", wx.ART_REDO),
        None,
        ("resources.zip", "images/20x20/editcut.png", "Cut", wx.ART_CUT),
        ("resources.zip", "images/20x20/editcopy.png", "Copy", wx.ART_COPY),
        ("resources.zip", "images/20x20/editpaste.png", "Paste", wx.ART_PASTE),
        None,
        ("resources.zip", "images/20x20/filefind.png", "Find", wx.ART_FIND),
        ("resources.zip", "images/20x20/searchreplace.png", "Replace", wx.ART_FIND_AND_REPLACE),
    ]
    for item in main_tools:
        if item is None:
            tb_main.AddSeparator()
        else:
            bmp = _load_wx_bitmap(item[0], item[1], item[3])
            tb_main.AddTool(wx.ID_ANY, item[2], bmp, item[2])
    tb_main.Realize()

    # --- Compiler Toolbar ---
    tb_comp = aui.AuiToolBar(frame, -1, style=aui.AUI_TB_DEFAULT_STYLE | aui.AUI_TB_GRIPPER)
    tb_comp.SetToolBitmapSize((20, 20))
    comp_tools = [
        ("compiler.zip", "images/20x20/compile.png", "Build"),
        ("compiler.zip", "images/20x20/run.png", "Run"),
        ("compiler.zip", "images/20x20/compilerun.png", "Build and run"),
        ("compiler.zip", "images/20x20/rebuild.png", "Rebuild"),
        ("compiler.zip", "images/20x20/stop.png", "Abort"),
    ]
    for item in comp_tools:
        bmp = _load_wx_bitmap(item[0], item[1])
        tb_comp.AddTool(wx.ID_ANY, item[1], bmp, item[1])
    tb_comp.AddSeparator()
    combo_target = wx.ComboBox(tb_comp, -1, "Debug", choices=["Debug", "Release"], size=(80, -1), style=wx.CB_READONLY)
    tb_comp.AddControl(combo_target)
    tb_comp.Realize()

    # --- Debugger Toolbar ---
    tb_dbg = aui.AuiToolBar(frame, -1, style=aui.AUI_TB_DEFAULT_STYLE | aui.AUI_TB_GRIPPER)
    tb_dbg.SetToolBitmapSize((20, 20))
    dbg_tools = [
        ("resources.zip", "images/20x20/dbgrun.png", "Debug / Continue"),
        ("resources.zip", "images/20x20/dbgrunto.png", "Run to cursor"),
        ("resources.zip", "images/20x20/dbgnext.png", "Next step"),
        ("resources.zip", "images/20x20/dbgstep.png", "Step into"),
        ("resources.zip", "images/20x20/dbgstepout.png", "Step out"),
        ("resources.zip", "images/20x20/dbgnexti.png", "Next instruction"),
        ("resources.zip", "images/20x20/dbgstepi.png", "Step into instruction"),
        ("resources.zip", "images/20x20/dbgpause.png", "Break debugger"),
        ("resources.zip", "images/20x20/dbgstop.png", "Stop debugger"),
    ]
    for item in dbg_tools:
        bmp = _load_wx_bitmap(item[0], item[1])
        tb_dbg.AddTool(wx.ID_ANY, item[1], bmp, item[1])
    tb_dbg.Realize()

    # 3.2 Row 1 Toolbars: Code completion, BrowseTracker, DoxyBlocks, IncrementalSearch
    # --- Code Completion Toolbar ---
    tb_cc = aui.AuiToolBar(frame, -1, style=aui.AUI_TB_DEFAULT_STYLE | aui.AUI_TB_GRIPPER)
    tb_cc.SetToolBitmapSize((20, 20))
    combo_scope = wx.ComboBox(tb_cc, -1, "<global>", choices=["<global>"], size=(120, -1), style=wx.CB_READONLY)
    tb_cc.AddControl(combo_scope)
    combo_func = wx.ComboBox(tb_cc, -1, "", choices=["", "main() : int"], size=(150, -1), style=wx.CB_READONLY)
    tb_cc.AddControl(combo_func)
    tb_cc.Realize()

    # --- BrowseTracker Toolbar ---
    tb_bt = aui.AuiToolBar(frame, -1, style=aui.AUI_TB_DEFAULT_STYLE | aui.AUI_TB_GRIPPER)
    tb_bt.SetToolBitmapSize((20, 20))
    for img, tip in [
        ("prev.png", "Browse backward"),
        ("next.png", "Browse forward"),
        ("mark_prev.png", "Previous mark"),
        ("mark_next.png", "Next mark"),
        ("mark.png", "Set mark"),
        ("mark_clear.png", "Clear marks"),
    ]:
        bmp = _load_wx_bitmap("BrowseTracker.zip", f"images/20x20/{img}")
        tb_bt.AddTool(wx.ID_ANY, tip, bmp, tip)
    tb_bt.Realize()

    # --- DoxyBlocks Toolbar ---
    tb_doxy = aui.AuiToolBar(frame, -1, style=aui.AUI_TB_DEFAULT_STYLE | aui.AUI_TB_GRIPPER)
    tb_doxy.SetToolBitmapSize((20, 20))
    for img, tip in [
        ("comment_block.png", "DoxyBlocks comment block"),
        ("comment_line.png", "DoxyBlocks comment line"),
        ("extract.png", "Extract documentation"),
        ("html.png", "Run HTML"),
        ("chm.png", "Run CHM"),
    ]:
        bmp = _load_wx_bitmap("DoxyBlocks.zip", f"images/20x20/{img}")
        tb_doxy.AddTool(wx.ID_ANY, tip, bmp, tip)
    tb_doxy.Realize()

    # --- Incremental Search Toolbar ---
    tb_inc = aui.AuiToolBar(frame, -1, style=aui.AUI_TB_DEFAULT_STYLE | aui.AUI_TB_GRIPPER)
    tb_inc.SetToolBitmapSize((20, 20))
    txt_inc = wx.TextCtrl(tb_inc, -1, "", size=(110, -1))
    tb_inc.AddControl(txt_inc)
    for img, tip in [
        ("incsearchnext.png", "Next match"),
        ("incsearchprev.png", "Previous match"),
        ("incsearchhighlight.png", "Highlight occurrences"),
        ("incsearchcase.png", "Match case"),
    ]:
        bmp = _load_wx_bitmap("IncrementalSearch.zip", f"images/20x20/{img}")
        tb_inc.AddTool(wx.ID_ANY, tip, bmp, tip)
    tb_inc.Realize()

    # 3.3 Row 2 Toolbars: Editor tools, ThreadSearch / Zoom
    tb_edtools = aui.AuiToolBar(frame, -1, style=aui.AUI_TB_DEFAULT_STYLE | aui.AUI_TB_GRIPPER)
    tb_edtools.SetToolBitmapSize((20, 20))
    for img, tip in [
        ("bookmark_add.png", "Toggle bookmark"),
        ("findf.png", "Find in files"),
        ("searchreplacef.png", "Replace in files"),
        ("goto.png", "Goto line"),
        ("history_clear.png", "Clear history"),
        ("idea.png", "Tips"),
    ]:
        bmp = _load_wx_bitmap("resources.zip", f"images/20x20/{img}")
        tb_edtools.AddTool(wx.ID_ANY, tip, bmp, tip)
    tb_edtools.Realize()

    tb_ts = aui.AuiToolBar(frame, -1, style=aui.AUI_TB_DEFAULT_STYLE | aui.AUI_TB_GRIPPER)
    tb_ts.SetToolBitmapSize((20, 20))
    for img, tip in [
        ("folder.png", "Search in current directory"),
        ("openfiles.png", "Search in open files"),
        ("project.png", "Search in target project"),
        ("options.png", "Thread search options"),
    ]:
        bmp = _load_wx_bitmap("ThreadSearch.zip", f"images/20x20/{img}")
        tb_ts.AddTool(wx.ID_ANY, tip, bmp, tip)
    tb_ts.Realize()

    # Dock all toolbars into 3 rows
    mgr.AddPane(tb_main, aui.AuiPaneInfo().Name("MainTB").ToolbarPane().Top().Row(0).Position(0))
    mgr.AddPane(tb_comp, aui.AuiPaneInfo().Name("CompTB").ToolbarPane().Top().Row(0).Position(1))
    mgr.AddPane(tb_dbg, aui.AuiPaneInfo().Name("DbgTB").ToolbarPane().Top().Row(0).Position(2))

    mgr.AddPane(tb_cc, aui.AuiPaneInfo().Name("CcTB").ToolbarPane().Top().Row(1).Position(0))
    mgr.AddPane(tb_bt, aui.AuiPaneInfo().Name("BtTB").ToolbarPane().Top().Row(1).Position(1))
    mgr.AddPane(tb_doxy, aui.AuiPaneInfo().Name("DoxyTB").ToolbarPane().Top().Row(1).Position(2))
    mgr.AddPane(tb_inc, aui.AuiPaneInfo().Name("IncTB").ToolbarPane().Top().Row(1).Position(3))

    mgr.AddPane(tb_edtools, aui.AuiPaneInfo().Name("EdToolsTB").ToolbarPane().Top().Row(2).Position(0))
    mgr.AddPane(tb_ts, aui.AuiPaneInfo().Name("TsTB").ToolbarPane().Top().Row(2).Position(1))

    # 4. Management Pane (Left, ~200px)
    mgmt_nb = aui.AuiNotebook(frame, style=aui.AUI_NB_TOP | aui.AUI_NB_TAB_MOVE)
    tree = wx.TreeCtrl(mgmt_nb, style=wx.TR_DEFAULT_STYLE | wx.TR_HAS_BUTTONS | wx.TR_LINES_AT_ROOT)
    il = wx.ImageList(16, 16)
    bmp_ws = _load_wx_bitmap("resources.zip", "images/codeblocks.png", size=(16, 16))
    bmp_folder = _load_wx_bitmap("resources.zip", "images/folder.png", size=(16, 16))
    bmp_src = _load_wx_bitmap("resources.zip", "images/source.png", size=(16, 16))
    idx_ws = il.Add(bmp_ws) if bmp_ws else -1
    idx_fld = il.Add(bmp_folder) if bmp_folder else -1
    idx_src = il.Add(bmp_src) if bmp_src else -1
    tree.AssignImageList(il)

    root_id = tree.AddRoot("Workspace", idx_ws)
    proj_id = tree.AppendItem(root_id, project_name, idx_ws)
    tree.SetItemBold(proj_id, True)

    files = list(extra_files) if extra_files else [filename]
    if filename not in files:
        files.append(filename)
    headers = [f for f in files if f.lower().endswith((".h", ".hpp"))]
    sources = [f for f in files if f not in headers]

    target_item_id = None
    src_node = tree.AppendItem(proj_id, "Sources", idx_fld)
    for f in sources:
        item_id = tree.AppendItem(src_node, f, idx_src)
        if f == filename:
            target_item_id = item_id

    hdr_node = tree.AppendItem(proj_id, "Headers", idx_fld)
    for f in headers:
        item_id = tree.AppendItem(hdr_node, f, idx_src)
        if f == filename:
            target_item_id = item_id

    tree.ExpandAll()
    if target_item_id:
        tree.SelectItem(target_item_id)
        # Active blue highlight #0078D7 with white text
        tree.SetItemBackgroundColour(target_item_id, wx.Colour(0, 120, 215))
        tree.SetItemTextColour(target_item_id, wx.Colour(255, 255, 255))

    mgmt_nb.AddPage(tree, "Projects", True)
    mgmt_nb.AddPage(wx.Panel(mgmt_nb), "Symbols", False)

    mgr.AddPane(
        mgmt_nb,
        aui.AuiPaneInfo().Name("ManagementPane").Caption("Management").Left()
        .BestSize((200, -1)).MinSize((180, -1)).CloseButton(True),
    )

    # 5. Clean Editor Tab (NO icon on editor tab)
    ed_nb = aui.AuiNotebook(frame, style=aui.AUI_NB_TOP | aui.AUI_NB_CLOSE_ON_ACTIVE_TAB)
    ed = stc.StyledTextCtrl(ed_nb, style=wx.BORDER_NONE)
    target_pos = _configure_scintilla_editor(
        ed,
        full_slice_text,
        start_line,
        end_line,
        with_cursor,
        show_vscroll=show_vscroll,
        caret_line=caret_line,
        caret_col=caret_col,
        show_changebar=show_changebar,
    )
    # Plain text tab without icon
    ed_nb.AddPage(ed, filename, True)
    mgr.AddPane(ed_nb, aui.AuiPaneInfo().Name("Editor").CenterPane())

    # 6. Bottom Dock "Logs & others" (~140px)
    if show_bottom_dock:
        log_nb = aui.AuiNotebook(frame, style=aui.AUI_NB_TOP | aui.AUI_NB_TAB_MOVE)
        # ParseManager / ProjectManager realistic log
        log_txt = (
            f"Scanning for lexers in 'C:\\Program Files\\CodeBlocks/share/CodeBlocks/lexers'...\n"
            f"Found 43 lexers\n"
            f"Loading Lexer for C/C++...\n"
            f"ProjectManager: Loading project 'C:\\Projects\\{project_name}\\{project_name}.cbp'\n"
            f"ProjectManager: Project '{project_name}' loaded!\n"
            f"ParseManager: Parsing '{filename}'...\n"
            f"ParseManager: 1 file(s) parsed in 0.02s\n"
            f"ParseManager: Parsing project '{project_name}' done!\n"
        )
        log_ctrl = wx.TextCtrl(log_nb, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.BORDER_NONE)
        log_font = wx.Font(9, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Courier New")
        log_ctrl.SetFont(log_font)
        log_ctrl.SetValue(log_txt)
        log_ctrl.SetBackgroundColour(wx.Colour(255, 255, 255))
        log_ctrl.SetForegroundColour(wx.Colour(0, 0, 0))

        log_nb.AddPage(log_ctrl, "Code::Blocks", True)
        for tname in ["Search results", "Cccc", "Build log", "Build messages", "CppCheck / Vera++"]:
            log_nb.AddPage(wx.Panel(log_nb), tname, False)

        mgr.AddPane(
            log_nb,
            aui.AuiPaneInfo().Name("MessagesPane").Caption("Logs & others").Bottom()
            .BestSize((-1, 140)).MinSize((-1, 100)).CloseButton(True),
        )

    mgr.Update()

    # 8. 8-Pane Status Bar
    sb = frame.CreateStatusBar(8)
    # Field widths: Field 0 stretches (-1), rest are fixed
    sb.SetStatusWidths([-1, 70, 130, 110, 150, 60, 90, 70])
    sb_path = filename if os.path.isabs(filename) else f"C:\\Projects\\{project_name}\\{filename}"
    sb.SetStatusText(f"  {sb_path}", 0)
    sb.SetStatusText("C/C++", 1)
    sb.SetStatusText("Windows (CR+LF)", 2)
    sb.SetStatusText("WINDOWS-1252", 3)
    sb.SetStatusText(f"Line {caret_line}, Col {caret_col}, Pos {target_pos}", 4)
    sb.SetStatusText("Insert", 5)
    sb.SetStatusText("Read/Write", 6)
    sb.SetStatusText("default", 7)

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
    caret_line=1,
    caret_col=1,
    show_bottom_dock=True,
    show_changebar=False,
    scale=1.0,
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
    frame = wx.Frame(None, pos=(80, 80), size=(1024, 720), style=frame_style)

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
    max_win_w = max(1024, screen_w - 80)
    max_win_h = max(620, screen_h - 60)

    aui_mgr = None
    if is_full:
        ed, aui_mgr = _build_full_codeblocks_frame(
            frame,
            full_slice_text,
            start_line,
            end_line,
            with_cursor,
            filename,
            project_name,
            extra_files=extra_files,
            caret_line=caret_line,
            caret_col=caret_col,
            show_bottom_dock=show_bottom_dock,
            show_changebar=show_changebar,
        )
        probe_h = max(14, ed.TextHeight(0))
        dock_overhead = 350 if show_bottom_dock else 220
        desired_h = probe_h * visible_count + dock_overhead + random.randint(4, 12)
        if desired_h > max_win_h:
            ed.SetUseVerticalScrollBar(True)
    else:
        ed = stc.StyledTextCtrl(frame, size=(1000, 1000), style=wx.BORDER_NONE)
        _configure_scintilla_editor(
            ed,
            full_slice_text,
            start_line,
            end_line,
            with_cursor,
            caret_line=caret_line,
            caret_col=caret_col,
            show_changebar=show_changebar,
        )

    line_h = ed.TextHeight(0)
    rng = random.Random(abs(hash(code_text)) % 100000)
    jitter_w = rng.randint(24, 48)
    jitter_h = rng.randint(8, 16)
    max_line_px = max((ed.TextWidth(0, l.replace("\t", "    ")) for l in slice_lines), default=200)

    if is_full:
        win_w = min(max_win_w, max(1024, max_line_px + 380 + jitter_w))
        dock_overhead = 360 if show_bottom_dock else 220
        win_h = min(max_win_h, max(620 if show_bottom_dock else 480, line_h * visible_count + dock_overhead + jitter_h))
        frame.SetSize((win_w, win_h))
    else:
        total_h = line_h * visible_count + jitter_h
        max_w = max(360, max_line_px + 85 + jitter_w)
        frame.SetSize((max_w, total_h))
        ed.SetSize((max_w, total_h))

    frame.Show()

    def _on_timer():
        if start_line > 1:
            ed.SetFirstVisibleLine(start_line - 1)
        # Ensure Scintilla focus is set so the caret renders crisply
        WM_SETFOCUS = 0x0007
        ctypes.windll.user32.SendMessageW(ed.GetHandle(), WM_SETFOCUS, 0, 0)
        ed.SetFocus()
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

        # Apply scaling if requested
        if scale and scale != 1.0:
            new_w = max(1, int(img.width * scale))
            new_h = max(1, int(img.height * scale))
            img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

        img.save(out_path)
        if aui_mgr is not None:
            aui_mgr.UnInit()
        frame.Destroy()

    wx.CallLater(160, _on_timer)
    app.MainLoop()
    return out_path
