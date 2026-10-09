import os
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="NgeLaprak CLI - Lab Report Assistant")
    subparsers = parser.add_subparsers(dest="command")

    # Command: init
    parser_init = subparsers.add_parser("init", help="Inisialisasi struktur folder laporan praktikum")
    parser_init.add_argument("--path", default=".", help="Direktori target")

    # Command: render
    parser_render = subparsers.add_parser("render", help="Render screenshot kode IDE otentik")
    parser_render.add_argument("--ide", choices=["netbeans", "codeblocks", "vscode"], default="netbeans", help="Target IDE")
    parser_render.add_argument("--file", required=True, help="File kode sumber")
    parser_render.add_argument("--out", default="screenshot.png", help="Path output gambar")
    parser_render.add_argument("--start", type=int, default=1, help="Baris awal")
    parser_render.add_argument("--end", type=int, default=None, help="Baris akhir")

    # Command: export-pdf
    parser_pdf = subparsers.add_parser("export-pdf", help="Ekspor berkas DOCX ke PDF")
    parser_pdf.add_argument("--docx", required=True, help="Path berkas .docx")
    parser_pdf.add_argument("--pdf", default=None, help="Path berkas .pdf output")

    args = parser.parse_args()

    if args.command == "init":
        target = os.path.abspath(args.path)
        os.makedirs(os.path.join(target, "Modul"), exist_ok=True)
        os.makedirs(os.path.join(target, "Laprak", "screenshots"), exist_ok=True)
        os.makedirs(os.path.join(target, "Code"), exist_ok=True)
        print(f"[NgeLaprak] Struktur direktori berhasil dibuat di: {target}")
        print("  - Modul/      : Taruh berkas panduan modul PDF/Word")
        print("  - Laprak/     : Tempat berkas template dan output (.docx, .pdf)")
        print("  - Code/       : Tempat berkas projek/kodingan praktikum")

    elif args.command == "render":
        from ngelaprak.renderers import render_netbeans_code, render_codeblocks_code, render_vscode_code
        with open(args.file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        fname = os.path.basename(args.file)
        if args.ide == "netbeans":
            render_netbeans_code(fname, content, start_line=args.start, end_line=args.end, out_path=args.out)
        elif args.ide == "codeblocks":
            render_codeblocks_code(content, start_line=args.start, end_line=args.end, out_path=args.out)
        elif args.ide == "vscode":
            render_vscode_code(content, start_line=args.start, end_line=args.end, out_path=args.out)
        print(f"[NgeLaprak] Screenshot {args.ide} berhasil disimpan ke: {args.out}")

    elif args.command == "export-pdf":
        from ngelaprak.core import export_docx_to_pdf
        pdf_out = export_docx_to_pdf(args.docx, args.pdf)
        print(f"[NgeLaprak] Berhasil diekspor ke PDF: {pdf_out}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
