import os
import sys
import subprocess

def export_docx_to_pdf(docx_path, pdf_path=None):
    """
    Exports a .docx document to .pdf using native Microsoft Word COM (on Windows)
    or LibreOffice (on Linux/macOS).
    """
    docx_path = os.path.abspath(docx_path)
    if pdf_path is None:
        pdf_path = os.path.splitext(docx_path)[0] + ".pdf"
    else:
        pdf_path = os.path.abspath(pdf_path)

    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

    # 1. Try docx2pdf if installed (uses native COM directly in python)
    try:
        from docx2pdf import convert
        convert(docx_path, pdf_path)
        if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
            return pdf_path
    except Exception as e:
        pass

    # 2. Try Windows Word COM via PowerShell
    if sys.platform == "win32":
        ps_cmd = f"""
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {{
    $doc = $word.Documents.Open('{docx_path}')
    $doc.SaveAs([ref]'{pdf_path}', [ref]17)
    $doc.Close()
}} finally {{
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
}}
"""
        try:
            res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True)
            if res.returncode == 0 and os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
                return pdf_path
        except Exception as e:
            print(f"[Warning] PowerShell Word COM failed: {e}")

    # 3. Try LibreOffice headless
    try:
        cmd = ["soffice", "--headless", "--convert-to", "pdf", docx_path, "--outdir", os.path.dirname(pdf_path)]
        subprocess.run(cmd, capture_output=True)
        if os.path.exists(pdf_path):
            return pdf_path
    except Exception:
        pass

    raise RuntimeError("Failed to export PDF: No compatible Word COM, docx2pdf, or LibreOffice found.")
