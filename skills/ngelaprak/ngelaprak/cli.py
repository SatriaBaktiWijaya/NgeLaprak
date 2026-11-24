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
    if ctx.get('kampus'):
        out.append(f"  * Kampus/Univ   : {ctx.get('kampus')}")
    if ctx.get('prodi') or ctx.get('fakultas'):
        prodi_txt = ctx.get('prodi', '')
        fak_txt = f" ({ctx.get('fakultas')})" if ctx.get('fakultas') else ""
        out.append(f"  * Prodi/Fakultas: {prodi_txt}{fak_txt}")
    if ctx.get('asisten'):
        out.append(f"  * Asisten Lab   : {', '.join(ctx.get('asisten')[:2])}")
    out.append(f"  * Bahasa / IDE  : {ctx.get('language')} -> {ctx.get('recommended_ide')}")
    if ctx.get('suggested_filename'):
        out.append(f"  * Target File   : {ctx.get('suggested_filename')}")
    
    code_status = "Sudah ada kodingan" if ctx.get('has_code') else "Belum ada kodingan (siap dibuat di folder Code/)"
    out.append(f"  * Status Kode   : {code_status}")

    tr = ctx.get("trap_report") or {}
    if tr.get("total_stripped_traps") or tr.get("total_semantic_warnings") or tr.get("image_heavy_files"):
        out.append("------------------------------------------------------------")
        out.append(f"  [ANTI-TRAP] Risk Level: {str(tr.get('risk_level', 'none')).upper()}")
        if tr.get("total_stripped_traps"):
            out.append(f"  * Hidden Trap Dibuang  : {tr.get('total_stripped_traps')} temuan")
        if tr.get("total_semantic_warnings"):
            out.append(f"  * Peringatan Semantik  : {tr.get('total_semantic_warnings')} (WAJIB konfirmasi user)")
        if tr.get("forbidden_identifiers"):
            out.append(f"  * Forbidden Identifiers: {', '.join(tr['forbidden_identifiers'])}")
        if tr.get("image_heavy_files"):
            out.append(f"  * Dokumen Scan/Gambar  : {', '.join(tr['image_heavy_files'])} (terapkan protokol visual anti-trap)")
        for finding in tr.get("files_with_findings", [])[:5]:
            out.append(
                f"    - {finding['file']} [{finding['risk_level']}] "
                f"(stripped={finding['stripped_count']}, warnings={finding['semantic_warning_count']})"
            )

    out.append("============================================================")
    return "\n".join(out)

def main():
    parser = argparse.ArgumentParser(description="NgeLaprak CLI - Lab Report Assistant")
    subparsers = parser.add_subparsers(dest="command")

    # Command: init
    parser_init = subparsers.add_parser("init", help="Inisialisasi struktur folder laporan praktikum")
    parser_init.add_argument("--path", default=".", help="Direktori target")
    parser_init.add_argument("--organize", action="store_true", help="Otomatis rapikan file yang tercecer di root")
    parser_init.add_argument("--lang", choices=["java", "cpp", "python", "sql"], default=None, help="Inisialisasi struktur proyek IDE resmi (NetBeans/CodeBlocks)")

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
    parser_render.add_argument("--theme", choices=["dark", "light"], default="dark", help="Tema editor (khusus VS Code: default dark)")
    parser_render.add_argument("--view", choices=["editor", "full"], default="editor", help="Tampilan: editor (potongan kode) atau full (jendela IDE penuh)")
    parser_render.add_argument("--project", default="ProjekPraktikum", help="Nama project untuk --view full")
    parser_render.add_argument("--filename", default=None, help="Override nama file di tab/explorer")
    parser_render.add_argument("--file", required=True, help="File kode sumber")
    parser_render.add_argument("--out", default="screenshot.png", help="Path output gambar")
    parser_render.add_argument("--start", type=int, default=1, help="Baris awal")
    parser_render.add_argument("--end", type=int, default=None, help="Baris akhir")
    parser_render.add_argument("--active-offset", type=int, default=None, help="Offset baris aktif relatif terhadap baris awal")
    parser_render.add_argument("--no-margin-guide", action="store_true", default=False, help="Sembunyikan garis panduan margin kolom 80")
    parser_render.add_argument("--no-cursor", action="store_true", default=False, help="Sembunyikan kursor/caret")
    parser_render.add_argument("--tag", default=None, help="Author tag untuk disisipkan jika start_line == 1")
    parser_render.add_argument("--extra-files", default=None, help="Daftar berkas ekstra dipisah koma (misal: a.java,b.java)")
    parser_render.add_argument("--sourcepath", default=None, help="Direktori root package source Java")
    parser_render.add_argument("--scale", type=float, default=1.0, help="Faktor skala raster (default: 1.0)")
    parser_render.add_argument("--caret", default=None, help="Posisi kursor dalam format 'LINE:COL' (misal: '1:1', '5:10')")
    parser_render.add_argument("--caret-line", type=int, default=1, help="Baris posisi kursor (default: 1)")
    parser_render.add_argument("--caret-col", type=int, default=1, help="Kolom posisi kursor (default: 1)")
    parser_render.add_argument("--hide-bottom-dock", action="store_true", default=False, help="Sembunyikan dock bawah (Output di NetBeans)")
    parser_render.add_argument("--hide-navigator", action="store_true", default=False, help="Sembunyikan panel Navigator di NetBeans")

    # Command: simulate-cli
    parser_sim = subparsers.add_parser("simulate-cli", help="Simulasi dan render screenshot terminal interaktif (multi-step input)")
    parser_sim.add_argument("--type", choices=["stack", "queue", "crud", "tree", "sorting"], default="stack", help="Jenis skenario simulasi praktikum")
    parser_sim.add_argument("--title", default=None, help="Judul program")
    parser_sim.add_argument("--name", default="Satria Bakti Wijaya", help="Nama mahasiswa")
    parser_sim.add_argument("--nim", default="109092500017", help="NIM mahasiswa")
    parser_sim.add_argument("--dir", default=r"D:\COOLYEAH\Semester 3\Praktikum", help="Prompt direktori terminal")
    parser_sim.add_argument("--runner-style", choices=["powershell", "codeblocks", "netbeans"], default="powershell", help="Gaya trailer sesi terminal (default: powershell)")
    parser_sim.add_argument("--scale", type=float, default=1.0, help="Faktor skala raster (default: 1.0)")
    parser_sim.add_argument("--out", default="screenshot_cli.png", help="Path gambar output")

    # Command: export-pdf
    parser_pdf = subparsers.add_parser("export-pdf", help="Ekspor berkas DOCX ke PDF")
    parser_pdf.add_argument("--docx", required=True, help="Path berkas .docx")
    parser_pdf.add_argument("--pdf", default=None, help="Path berkas .pdf output")

    # Command: sanitize
    parser_san = subparsers.add_parser(
        "sanitize",
        help="Sanitasi dokumen/gambar/kode terhadap hidden AI trap & prompt injection",
    )
    parser_san.add_argument("--file", required=True, help="Path berkas input (PDF/DOCX/PPTX/XLSX/HTML/MD/IPYNB/SVG/PNG/JPG/Code)")
    parser_san.add_argument("--out-clean", default=None, help="Simpan teks bersih hasil sanitasi ke berkas")
    parser_san.add_argument("--out-report", default=None, help="Simpan laporan lengkap sanitasi dalam format JSON")
    parser_san.add_argument("--out-image", default=None, help="Simpan gambar bersih (tanpa metadata & alpha-flattened)")
    parser_san.add_argument("--engine", choices=["auto", "pymupdf", "pdfplumber", "pypdf"], default="auto", help="Engine ekstraksi PDF (default: auto)")
    parser_san.add_argument("--json", action="store_true", dest="as_json", help="Cetak output laporan dalam format JSON")

    # Command: audit-code
    parser_audit = subparsers.add_parser(
        "audit-code",
        help="Audit direktori kode sumber terhadap kebocoran forbidden identifiers / trap watermark",
    )
    parser_audit.add_argument("--code-dir", required=True, help="Direktori (atau berkas) kode sumber untuk diaudit")
    parser_audit.add_argument("--report", default=None, help="Path berkas JSON laporan hasil 'ngelaprak sanitize --out-report'")
    parser_audit.add_argument("--source", action="append", default=None, help="Path dokumen sumber (PDF/DOCX/dll.) untuk mengekstrak forbidden identifiers otomatis")
    parser_audit.add_argument("--identifiers", default=None, help="Daftar identifier terlarang tambahan dipisah koma")
    parser_audit.add_argument("--json", action="store_true", dest="as_json", help="Cetak hasil audit dalam format JSON")

    args = parser.parse_args()

    if args.command in ["init", "organize"]:
        from ngelaprak.core import organize_workspace, auto_scaffold_code_directory
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

            if res.get("ide_scaffold") and res["ide_scaffold"]["type"] != "none":
                sc = res["ide_scaffold"]
                if sc["type"] == "java_netbeans":
                    print(f"[+] Proyek Apache NetBeans (Maven) siap di: Code/")
                    print(f"    -> File pom.xml & nbactions.xml terpasang")
                    print(f"    -> Package: {sc.get('package')} (Main Class: {sc.get('main_class')})")
                elif sc["type"] == "cpp_codeblocks":
                    print(f"[+] Proyek Code::Blocks (.cbp) siap di: Code/")
                    for cbp in sc.get("created_cbp", []):
                        print(f"    -> {os.path.relpath(cbp, target)}")

            print()
            print(format_context_summary(res["context"]))
        else:
            code_dir = os.path.join(target, "Code")
            os.makedirs(os.path.join(target, "Modul"), exist_ok=True)
            os.makedirs(os.path.join(target, "Laprak", "screenshots"), exist_ok=True)
            os.makedirs(code_dir, exist_ok=True)

            if getattr(args, "lang", None):
                sc = auto_scaffold_code_directory(code_dir, language=args.lang, project_name="ProjekPraktikum")
                if sc["type"] == "java_netbeans":
                    print(f"[NgeLaprak] Proyek Apache NetBeans Maven berhasil dibuat di: {code_dir}")
                elif sc["type"] == "cpp_codeblocks":
                    print(f"[NgeLaprak] Proyek Code::Blocks (.cbp) berhasil dibuat di: {code_dir}")

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
        from ngelaprak.renderers import render_netbeans_code, render_codeblocks_code, render_vscode_code, render_database_query
        abs_file = os.path.abspath(args.file)
        with open(abs_file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        fname = args.filename or os.path.basename(abs_file)
        file_dir = os.path.dirname(abs_file)

        if args.extra_files:
            if isinstance(args.extra_files, str):
                custom_extras = [f.strip() for f in args.extra_files.split(",") if f.strip()]
            else:
                custom_extras = list(args.extra_files)
            if fname not in custom_extras:
                custom_extras.insert(0, fname)
            extra_files = custom_extras
        else:
            exts = (".java",) if args.ide == "netbeans" else (".cpp", ".c", ".cc", ".h", ".hpp")
            siblings = sorted(n for n in os.listdir(file_dir) if n.lower().endswith(exts))[:8] if os.path.isdir(file_dir) else [fname]
            extra_files = [fname] + [s for s in siblings if s != fname]

        sourcepath = args.sourcepath
        if not sourcepath:
            norm_dir = file_dir.replace("\\", "/")
            marker = "/src/main/java"
            if marker in norm_dir:
                sourcepath = file_dir[: norm_dir.index(marker) + len(marker)]

        # Caret coordinates parsing
        caret_line = args.caret_line
        caret_col = args.caret_col
        if args.caret:
            try:
                caret_str = args.caret.strip()
                if ":" in caret_str:
                    parts = caret_str.split(":", 1)
                    caret_line = int(parts[0].strip())
                    caret_col = int(parts[1].strip())
                elif "," in caret_str:
                    parts = caret_str.split(",", 1)
                    caret_line = int(parts[0].strip())
                    caret_col = int(parts[1].strip())
                else:
                    caret_line = int(caret_str)
            except Exception as e:
                print(f"[!] Warning: Gagal mengurai format --caret '{args.caret}', menggunakan caret_line={caret_line}, caret_col={caret_col}: {e}")

        with_cursor = not getattr(args, "no_cursor", False)
        with_margin_guide = not getattr(args, "no_margin_guide", False)
        show_bottom_dock = not getattr(args, "hide_bottom_dock", False)
        show_navigator = not getattr(args, "hide_navigator", False)
        scale = float(getattr(args, "scale", 1.0))

        if args.ide == "netbeans":
            render_netbeans_code(
                fname,
                content,
                start_line=args.start,
                end_line=args.end,
                out_path=args.out,
                active_line_offset=args.active_offset,
                with_margin_guide=with_margin_guide,
                with_cursor=with_cursor,
                author_tag=args.tag,
                view=args.view,
                project_name=args.project,
                extra_files=extra_files,
                sourcepath=sourcepath,
                caret_line=caret_line,
                caret_col=caret_col,
                show_bottom_dock=show_bottom_dock,
                show_navigator=show_navigator,
                scale=scale,
            )
        elif args.ide == "codeblocks":
            render_codeblocks_code(
                content,
                start_line=args.start,
                end_line=args.end,
                out_path=args.out,
                with_cursor=with_cursor,
                author_tag=args.tag,
                view=args.view,
                filename=fname,
                project_name=args.project,
                extra_files=extra_files,
            )
        elif args.ide == "vscode":
            render_vscode_code(content, filename=fname, theme=args.theme, start_line=args.start, end_line=args.end, out_path=args.out)
        elif args.ide == "database":
            render_database_query(query_sql=content, columns=["id", "result"], rows=[[1, "Success"]], out_path=args.out)
        print(f"[NgeLaprak] Screenshot {args.ide} ({args.view}) berhasil disimpan ke: {args.out}")

    elif args.command == "simulate-cli":
        from ngelaprak.core.cli_simulator import render_interactive_session_to_image
        out_shot = render_interactive_session_to_image(
            prompt_dir=args.dir,
            scenario_type=args.type,
            out_path=args.out,
            program_title=args.title,
            student_name=args.name,
            student_nim=args.nim,
            runner_style=args.runner_style,
            scale=float(getattr(args, "scale", 1.0)),
        )
        print(f"[NgeLaprak] Screenshot CLI interaktif ({args.type}) berhasil disimpan ke: {out_shot}")

    elif args.command == "export-pdf":
        from ngelaprak.core import export_docx_to_pdf
        pdf_out = export_docx_to_pdf(args.docx, args.pdf)
        print(f"[NgeLaprak] Berhasil diekspor ke PDF: {pdf_out}")

    elif args.command == "sanitize":
        import json
        from ngelaprak.core import sanitize_document

        target_file = os.path.abspath(args.file)
        if not os.path.exists(target_file):
            print(f"[ANTI-TRAP] Error: Berkas tidak ditemukan: {target_file}", file=sys.stderr)
            sys.exit(2)

        rep = sanitize_document(
            target_file,
            engine=args.engine,
            out_image_path=args.out_image,
        )

        if args.out_clean:
            out_clean = os.path.abspath(args.out_clean)
            os.makedirs(os.path.dirname(out_clean), exist_ok=True)
            with open(out_clean, "w", encoding="utf-8") as f:
                f.write(rep.clean_text)

        if args.out_report:
            rep.save_json(args.out_report)

        if args.as_json:
            print(rep.to_json())
        else:
            print("============================================================")
            print("   [ANTI-TRAP] Laporan Sanitasi Dokumen / Gambar")
            print("============================================================")
            print(f"  * Berkas     : {target_file}")
            print(f"  * Tipe/Engine: {rep.file_type} ({rep.engine_used})")
            print(f"  * Risk Level : {rep.risk_level.upper()}")
            print(f"  * Trap Buang : {len(rep.stripped_traps)}")
            print(f"  * Peringatan : {len(rep.semantic_warnings)}")
            if rep.forbidden_identifiers:
                print(f"  * Forbidden  : {', '.join(rep.forbidden_identifiers)}")
            if rep.sanitized_image_path:
                print(f"  * Clean Image: {rep.sanitized_image_path}")
            if rep.stats.get("is_image_heavy_document"):
                print(f"  * [!] Halaman berbasis gambar/scan terdeteksi: {rep.stats.get('image_heavy_pages')}")
            if rep.stripped_traps:
                print("\n[Stripped Hidden Traps]:")
                for t in rep.stripped_traps:
                    print(f"  - [{t['reason']}] ({t['location']}): {t['text'][:160]}")
            if rep.semantic_warnings:
                print("\n[Semantic Warnings - WAJIB KONFIRMASI USER]:")
                for w in rep.semantic_warnings:
                    print(f"  - [{w['category']}/{w['pattern']}] ({w['location']}): {w['text'][:160]}")
            if rep.clean_text and not args.out_clean:
                print("\n[Clean Text]:")
                print(rep.clean_text)

    elif args.command == "audit-code":
        import json
        from ngelaprak.core import audit_code_for_traps

        extra_ids = (
            [s.strip() for s in args.identifiers.split(",") if s.strip()]
            if args.identifiers
            else None
        )
        res = audit_code_for_traps(
            code_dir=args.code_dir,
            forbidden_identifiers=extra_ids,
            report=args.report,
            source_files=args.source,
        )

        if args.as_json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            status_txt = "PASSED (BERSIH)" if res["passed"] else f"FAILED ({res['violation_count']} KEBOCORAN TRAP)"
            print("============================================================")
            print(f"   [ANTI-TRAP] Audit Kode Akhir: {status_txt}")
            print("============================================================")
            print(f"  * Direktori    : {res['code_dir']}")
            print(f"  * File Dipindai: {len(res['scanned_files'])}")
            print(f"  * Identifier   : {', '.join(res['checked_identifiers']) if res['checked_identifiers'] else '(none)'}")
            if res["violations"]:
                print("\n[Pelanggaran Terdeteksi]:")
                for v in res["violations"]:
                    print(f"  - {v['rel_path']}:{v['line']} [{v['reason']}:{v['identifier']}] -> {v['snippet']}")

        if not res["passed"]:
            sys.exit(1)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
