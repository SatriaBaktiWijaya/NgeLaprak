import os
import sys
import argparse

# Ensure ngelaprak package root is in sys.path
_parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _parent not in sys.path:
    sys.path.insert(0, _parent)

def format_context_summary(ctx):
    out = []
    out.append("============================================================")
    out.append("   Konteks Terdeteksi Otomatis (Smart Context Inference)")
    out.append("============================================================")
    out.append(f"  * Mata Kuliah   : {ctx.get('course_name')}")
    out.append(f"  * Modul Target  : {ctx.get('target_module_title')}")
    if ctx.get('student_name') or ctx.get('student_nim'):
        out.append(f"  * Mahasiswa     : {ctx.get('student_name')} ({ctx.get('student_nim')})")
    if ctx.get('asisten'):
        out.append(f"  * Asisten Lab   : {', '.join(ctx.get('asisten')[:2])}")
    out.append(f"  * Bahasa / IDE  : {ctx.get('language')} -> {ctx.get('recommended_ide')}")
    if ctx.get('suggested_filename'):
        out.append(f"  * Target File   : {ctx.get('suggested_filename')}")
    
    code_status = "Sudah ada kodingan" if ctx.get('has_code') else "Belum ada kodingan (siap dibuat di folder Code/)"
    out.append(f"  * Status Kode   : {code_status}")
    out.append("============================================================")
    return "\n".join(out)

def main():
    parser = argparse.ArgumentParser(description="NgeLaprak CLI - Lab Report Assistant")
    subparsers = parser.add_subparsers(dest="command")

    # Command: init
    parser_init = subparsers.add_parser("init", help="Inisialisasi struktur folder laporan praktikum")
    parser_init.add_argument("--path", default=".", help="Direktori target")
    parser_init.add_argument("--organize", action="store_true", help="Otomatis rapikan file yang tercecer di root")

    # Command: organize
    parser_organize = subparsers.add_parser("organize", help="Auto-scaffold dan rapikan file ke Modul/, Laprak/, dan Code/")
    parser_organize.add_argument("--path", default=".", help="Direktori target")
    parser_organize.add_argument("--dry-run", action="store_true", help="Simulasi pemindahan tanpa mengubah berkas")

    # Command: analyze
    parser_analyze = subparsers.add_parser("analyze", help="Analisis dan deteksi konteks otomatis dari folder kerja")
    parser_analyze.add_argument("--path", default=".", help="Direktori target")

    # Command: render
    parser_render = subparsers.add_parser("render", help="Render screenshot kode IDE otentik")
    parser_render.add_argument("--ide", choices=["netbeans", "codeblocks", "vscode", "database"], default="netbeans", help="Target IDE")
    parser_render.add_argument("--file", required=True, help="File kode sumber")
    parser_render.add_argument("--out", default="screenshot.png", help="Path output gambar")
    parser_render.add_argument("--start", type=int, default=1, help="Baris awal")
    parser_render.add_argument("--end", type=int, default=None, help="Baris akhir")

    # Command: export-pdf
    parser_pdf = subparsers.add_parser("export-pdf", help="Ekspor berkas DOCX ke PDF")
    parser_pdf.add_argument("--docx", required=True, help="Path berkas .docx")
    parser_pdf.add_argument("--pdf", default=None, help="Path berkas .pdf output")

    args = parser.parse_args()

    if args.command in ["init", "organize"]:
        from ngelaprak.core import organize_workspace
        target = os.path.abspath(args.path)

        if args.command == "organize" or getattr(args, "organize", False):
            dry_run = getattr(args, "dry_run", False)
            res = organize_workspace(target, dry_run=dry_run)
            
            if dry_run:
                print(f"[NgeLaprak SIMULASI] Memeriksa direktori: {target}")
            else:
                print(f"[NgeLaprak] Merapikan struktur direktori di: {target}")

            if res["created_dirs"]:
                print(f"[+] Folder dibuat: {', '.join(os.path.basename(d) for d in res['created_dirs'])}")

            if res["moved_files"]:
                print("[*] Berkas dipindahkan ke folder masing-masing:")
                for m in res["moved_files"]:
                    dest_rel = os.path.relpath(m["destination"], target)
                    print(f"    -> {m['filename']} => {dest_rel}")
            else:
                print("[*] Berkas sudah berada di folder yang sesuai.")

            print()
            print(format_context_summary(res["context"]))
        else:
            os.makedirs(os.path.join(target, "Modul"), exist_ok=True)
            os.makedirs(os.path.join(target, "Laprak", "screenshots"), exist_ok=True)
            os.makedirs(os.path.join(target, "Code"), exist_ok=True)
            print(f"[NgeLaprak] Struktur direktori berhasil dibuat di: {target}")
            print("  - Modul/      : Taruh berkas panduan modul PDF/Word & TP")
            print("  - Laprak/     : Tempat berkas template dan output (.docx, .pdf)")
            print("  - Code/       : Tempat berkas projek/kodingan praktikum")
            print("  (Tips: Jalankan 'ngelaprak organize' untuk merapikan file otomatis)")

    elif args.command == "analyze":
        from ngelaprak.core import infer_workspace_context
        target = os.path.abspath(args.path)
        ctx = infer_workspace_context(target)
        print(format_context_summary(ctx))

    elif args.command == "render":
        from ngelaprak.renderers import render_netbeans_code, render_codeblocks_code, render_vscode_code, render_database_view
        with open(args.file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        fname = os.path.basename(args.file)
        if args.ide == "netbeans":
            render_netbeans_code(fname, content, start_line=args.start, end_line=args.end, out_path=args.out)
        elif args.ide == "codeblocks":
            render_codeblocks_code(content, start_line=args.start, end_line=args.end, out_path=args.out)
        elif args.ide == "vscode":
            render_vscode_code(content, start_line=args.start, end_line=args.end, out_path=args.out)
        elif args.ide == "database":
            render_database_view(query=content, out_path=args.out)
        print(f"[NgeLaprak] Screenshot {args.ide} berhasil disimpan ke: {args.out}")

    elif args.command == "export-pdf":
        from ngelaprak.core import export_docx_to_pdf
        pdf_out = export_docx_to_pdf(args.docx, args.pdf)
        print(f"[NgeLaprak] Berhasil diekspor ke PDF: {pdf_out}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
