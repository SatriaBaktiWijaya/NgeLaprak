import os
import re
import subprocess
import time
from typing import List, Dict, Any, Union

def build_interactive_terminal_lines(
    prompt_dir: str,
    compile_cmd: str = None,
    run_cmd: str = ".\\main.exe",
    dialog_steps: List[Dict[str, Any]] = None,
    runner_style: str = "codeblocks",
    execution_time: float = 0.042
) -> List[str]:
    """
    Constructs a realistic terminal transcript representing an interactive CLI session.
    dialog_steps is a list of dicts or tuples:
      - {'type': 'output', 'text': '=== MENU ==='}
      - {'type': 'input', 'prompt': 'Pilih menu [1-4]: ', 'value': '1'}
      - {'type': 'header', 'text': '--- SUBMENU ---'}
      - {'type': 'success', 'text': '[BERHASIL] Data ditambahkan'}
      - {'type': 'blank'}
    """
    lines = []
    clean_dir = prompt_dir.rstrip("\\/")
    ps_prompt = f"PS {clean_dir}>"

    # Optional compilation step
    if compile_cmd:
        lines.append(f"{ps_prompt} {compile_cmd}")

    # Launch command
    lines.append(f"{ps_prompt} {run_cmd}")

    if not dialog_steps:
        dialog_steps = []

    for step in dialog_steps:
        if isinstance(step, tuple):
            stype = step[0]
            if stype == "input":
                prompt = step[1]
                val = step[2] if len(step) > 2 else ""
                lines.append(f"{prompt}[[INPUT]]{val}[[/INPUT]]")
            elif stype == "header":
                lines.append(f"[[HEADER]]{step[1]}[[/HEADER]]")
            elif stype == "success":
                lines.append(f"[[SUCCESS]]{step[1]}[[/SUCCESS]]")
            elif stype == "blank":
                lines.append("")
            else:
                lines.append(step[1])
        elif isinstance(step, dict):
            stype = step.get("type", "output")
            if stype == "input":
                prompt = step.get("prompt", "")
                val = step.get("value", "")
                lines.append(f"{prompt}[[INPUT]]{val}[[/INPUT]]")
            elif stype == "header":
                lines.append(f"[[HEADER]]{step.get('text', '')}[[/HEADER]]")
            elif stype == "success":
                lines.append(f"[[SUCCESS]]{step.get('text', '')}[[/SUCCESS]]")
            elif stype == "blank":
                lines.append("")
            else:
                lines.append(step.get("text", ""))
        else:
            lines.append(str(step))

    # Runner exit trailer matching authentic IDE terminal styles
    if runner_style == "codeblocks":
        lines.append("")
        lines.append(f"[[MUTED]]--------------------------------------------------------------------------------[[/MUTED]]")
        lines.append(f"[[MUTED]]Process returned 0 (0x0)   execution time : {execution_time:.3f} s[[/MUTED]]")
        lines.append(f"[[MUTED]]Press any key to continue.[[/MUTED]]")
    elif runner_style == "powershell":
        lines.append("")
        lines.append(f"{ps_prompt} ")
    elif runner_style == "netbeans":
        lines.append("")
        lines.append(f"[[SUCCESS]]BUILD SUCCESSFUL (total time: {int(execution_time * 10 + 1)} seconds)[[/SUCCESS]]")

    return lines

def generate_interactive_scenario(
    scenario_type: str = "stack",
    entity: str = "Mahasiswa",
    program_title: str = None,
    student_name: str = "Satria Bakti Wijaya",
    student_nim: str = "109092500017"
) -> List[Dict[str, Any]]:
    """
    Generates rich, authentic multi-step interactive scenarios for common practicum assignments.
    """
    stype = scenario_type.lower()
    steps = []

    if stype == "stack":
        title = program_title or "PROGRAM SIMULASI ABSTRACT DATA TYPE (STACK)"
        steps = [
            {"type": "header", "text": f"=== {title} ==="},
            {"type": "output", "text": f"Praktikan : {student_name} ({student_nim})"},
            {"type": "output", "text": "Kapasitas Maksimal Stack : 5 Elemen"},
            {"type": "blank"},
            {"type": "header", "text": "--- [LANGKAH 1: OPERASI PUSH DATA] ---"},
            {"type": "input", "prompt": "Pilih Menu [1. Push, 2. Pop, 3. Peek, 4. Display, 5. Exit]: ", "value": "1"},
            {"type": "input", "prompt": ">> Masukkan elemen nilai yang di-push: ", "value": "10"},
            {"type": "success", "text": "[OK] Nilai 10 berhasil didorong ke Stack (Top sekarang: 0)"},
            {"type": "blank"},
            {"type": "input", "prompt": "Pilih Menu [1. Push, 2. Pop, 3. Peek, 4. Display, 5. Exit]: ", "value": "1"},
            {"type": "input", "prompt": ">> Masukkan elemen nilai yang di-push: ", "value": "25"},
            {"type": "success", "text": "[OK] Nilai 25 berhasil didorong ke Stack (Top sekarang: 1)"},
            {"type": "blank"},
            {"type": "input", "prompt": "Pilih Menu [1. Push, 2. Pop, 3. Peek, 4. Display, 5. Exit]: ", "value": "1"},
            {"type": "input", "prompt": ">> Masukkan elemen nilai yang di-push: ", "value": "50"},
            {"type": "success", "text": "[OK] Nilai 50 berhasil didorong ke Stack (Top sekarang: 2)"},
            {"type": "blank"},
            {"type": "header", "text": "--- [LANGKAH 2: LIHAT ISI STACK & STATUS] ---"},
            {"type": "input", "prompt": "Pilih Menu [1. Push, 2. Pop, 3. Peek, 4. Display, 5. Exit]: ", "value": "4"},
            {"type": "output", "text": "Isi Elemen Stack Saat Ini (Top -> Bottom):"},
            {"type": "output", "text": "  [ Index 2 ] : 50 <-- TOP"},
            {"type": "output", "text": "  [ Index 1 ] : 25"},
            {"type": "output", "text": "  [ Index 0 ] : 10"},
            {"type": "output", "text": "Status: IsEmpty = False | IsFull = False (Ukuran: 3/5)"},
            {"type": "blank"},
            {"type": "header", "text": "--- [LANGKAH 3: OPERASI POP (LIFO)] ---"},
            {"type": "input", "prompt": "Pilih Menu [1. Push, 2. Pop, 3. Peek, 4. Display, 5. Exit]: ", "value": "2"},
            {"type": "success", "text": "[POP] Elemen 50 berhasil dikeluarkan dari puncak Stack!"},
            {"type": "input", "prompt": "Pilih Menu [1. Push, 2. Pop, 3. Peek, 4. Display, 5. Exit]: ", "value": "3"},
            {"type": "output", "text": ">> Elemen Teratas Saat Ini (Peek): 25"},
            {"type": "blank"},
            {"type": "header", "text": "--- [LANGKAH 4: KELUAR PROGRAM] ---"},
            {"type": "input", "prompt": "Pilih Menu [1. Push, 2. Pop, 3. Peek, 4. Display, 5. Exit]: ", "value": "5"},
            {"type": "output", "text": "Terima kasih! Program simulasi Stack selesai dijalankan."}
        ]

    elif stype == "queue":
        title = program_title or "SISTEM ANTRIAN BANK NASIONAL (QUEUE - FIFO)"
        steps = [
            {"type": "header", "text": f"=== {title} ==="},
            {"type": "output", "text": f"Loket CS | Operator: {student_name}"},
            {"type": "blank"},
            {"type": "header", "text": "--- [LANGKAH 1: ENQUEUE NASABAH] ---"},
            {"type": "input", "prompt": "Pilih Opsi [1. Ambil Antrian, 2. Panggil, 3. Status, 4. Keluar]: ", "value": "1"},
            {"type": "input", "prompt": ">> Nama Nasabah : ", "value": "Budi Santoso"},
            {"type": "success", "text": "[SUKSES] Nomor Antrian A-01 (Budi Santoso) masuk antrian."},
            {"type": "blank"},
            {"type": "input", "prompt": "Pilih Opsi [1. Ambil Antrian, 2. Panggil, 3. Status, 4. Keluar]: ", "value": "1"},
            {"type": "input", "prompt": ">> Nama Nasabah : ", "value": "Siti Nurhaliza"},
            {"type": "success", "text": "[SUKSES] Nomor Antrian A-02 (Siti Nurhaliza) masuk antrian."},
            {"type": "blank"},
            {"type": "input", "prompt": "Pilih Opsi [1. Ambil Antrian, 2. Panggil, 3. Status, 4. Keluar]: ", "value": "1"},
            {"type": "input", "prompt": ">> Nama Nasabah : ", "value": "Ahmad Dani"},
            {"type": "success", "text": "[SUKSES] Nomor Antrian A-03 (Ahmad Dani) masuk antrian."},
            {"type": "blank"},
            {"type": "header", "text": "--- [LANGKAH 2: DEQUEUE NASABAH (PELAYANAN)] ---"},
            {"type": "input", "prompt": "Pilih Opsi [1. Ambil Antrian, 2. Panggil, 3. Status, 4. Keluar]: ", "value": "2"},
            {"type": "success", "text": "[PANGGILAN] Nomor Antrian A-01 atas nama Budi Santoso dipersilakan ke Loket 1!"},
            {"type": "blank"},
            {"type": "header", "text": "--- [LANGKAH 3: CEK SISA ANTRIAN] ---"},
            {"type": "input", "prompt": "Pilih Opsi [1. Ambil Antrian, 2. Panggil, 3. Status, 4. Keluar]: ", "value": "3"},
            {"type": "output", "text": "+-------+---------------------+---------------+-----------------+"},
            {"type": "output", "text": "| No    | Nama Nasabah        | Status        | Waktu Tunggu    |"},
            {"type": "output", "text": "+-------+---------------------+---------------+-----------------+"},
            {"type": "output", "text": "| A-02  | Siti Nurhaliza      | Menunggu (Depan)| ~ 2 Menit       |"},
            {"type": "output", "text": "| A-03  | Ahmad Dani          | Menunggu      | ~ 6 Menit       |"},
            {"type": "output", "text": "+-------+---------------------+---------------+-----------------+"},
            {"type": "output", "text": "Total Antrian Tersisa: 2 orang."},
            {"type": "blank"},
            {"type": "input", "prompt": "Pilih Opsi [1. Ambil Antrian, 2. Panggil, 3. Status, 4. Keluar]: ", "value": "4"},
            {"type": "output", "text": "Sesi loket diakhiri. Selamat bertugas!"}
        ]

    elif stype in ["crud", "database", "array"]:
        title = program_title or f"APLIKASI PENGELOLAAN DATA {entity.upper()}"
        steps = [
            {"type": "header", "text": f"=== {title} ==="},
            {"type": "blank"},
            {"type": "header", "text": "--- [LANGKAH 1: INPUT DATA BARU] ---"},
            {"type": "input", "prompt": "Menu Utama [1. Tambah, 2. Tampil, 3. Cari, 4. Hapus, 5. Keluar]: ", "value": "1"},
            {"type": "input", "prompt": ">> Masukkan NIM   : ", "value": "109092500017"},
            {"type": "input", "prompt": ">> Masukkan Nama  : ", "value": "Satria Bakti Wijaya"},
            {"type": "input", "prompt": ">> Masukkan Prodi : ", "value": "S1 Rekayasa Perangkat Lunak"},
            {"type": "input", "prompt": ">> Masukkan IPK   : ", "value": "3.85"},
            {"type": "success", "text": "[SUKSES] Data mahasiswa pertama berhasil disimpan!"},
            {"type": "blank"},
            {"type": "input", "prompt": "Menu Utama [1. Tambah, 2. Tampil, 3. Cari, 4. Hapus, 5. Keluar]: ", "value": "1"},
            {"type": "input", "prompt": ">> Masukkan NIM   : ", "value": "109092530004"},
            {"type": "input", "prompt": ">> Masukkan Nama  : ", "value": "Khilma 'Ainunnajah"},
            {"type": "input", "prompt": ">> Masukkan Prodi : ", "value": "S1 Rekayasa Perangkat Lunak"},
            {"type": "input", "prompt": ">> Masukkan IPK   : ", "value": "3.92"},
            {"type": "success", "text": "[SUKSES] Data mahasiswa kedua berhasil disimpan!"},
            {"type": "blank"},
            {"type": "header", "text": "--- [LANGKAH 2: MENAMPILKAN SELURUH DATA] ---"},
            {"type": "input", "prompt": "Menu Utama [1. Tambah, 2. Tampil, 3. Cari, 4. Hapus, 5. Keluar]: ", "value": "2"},
            {"type": "output", "text": "+----------------+----------------------+-----------------------------+------+"},
            {"type": "output", "text": "| NIM            | Nama Mahasiswa       | Program Studi               | IPK  |"},
            {"type": "output", "text": "+----------------+----------------------+-----------------------------+------+"},
            {"type": "output", "text": "| 109092500017   | Satria Bakti Wijaya  | S1 Rekayasa Perangkat Lunak | 3.85 |"},
            {"type": "output", "text": "| 109092530004   | Khilma 'Ainunnajah   | S1 Rekayasa Perangkat Lunak | 3.92 |"},
            {"type": "output", "text": "+----------------+----------------------+-----------------------------+------+"},
            {"type": "output", "text": "Total Record: 2 baris data."},
            {"type": "blank"},
            {"type": "header", "text": "--- [LANGKAH 3: PENCARIAN DATA (SEARCH)] ---"},
            {"type": "input", "prompt": "Menu Utama [1. Tambah, 2. Tampil, 3. Cari, 4. Hapus, 5. Keluar]: ", "value": "3"},
            {"type": "input", "prompt": ">> Masukkan NIM yang dicari: ", "value": "109092500017"},
            {"type": "success", "text": "[DITEMUKAN] Data cocok pada Index [0] -> Nama: Satria Bakti Wijaya (IPK: 3.85)"},
            {"type": "blank"},
            {"type": "header", "text": "--- [LANGKAH 4: KELUAR] ---"},
            {"type": "input", "prompt": "Menu Utama [1. Tambah, 2. Tampil, 3. Cari, 4. Hapus, 5. Keluar]: ", "value": "5"},
            {"type": "output", "text": "Perubahan telah tersimpan. Program selesai."}
        ]

    elif stype in ["tree", "graph"]:
        title = program_title or "BINARY SEARCH TREE (BST) & TRAVERSAL"
        steps = [
            {"type": "header", "text": f"=== {title} ==="},
            {"type": "blank"},
            {"type": "header", "text": "--- [LANGKAH 1: INSERT NODE POHON BINER] ---"},
            {"type": "input", "prompt": "Masukkan jumlah node yang ingin di-insert: ", "value": "7"},
            {"type": "input", "prompt": ">> Masukkan 7 angka (pisahkan spasi): ", "value": "50 30 70 20 40 60 80"},
            {"type": "success", "text": "[OK] 7 Node berhasil dibentuk ke dalam Binary Search Tree."},
            {"type": "output", "text": "Struktur Pohon (Root: 50 | Left Subtree: 30 | Right Subtree: 70)"},
            {"type": "blank"},
            {"type": "header", "text": "--- [LANGKAH 2: TRAVERSAL POHON] ---"},
            {"type": "output", "text": "1. Pre-Order  (Root - Left - Right) : 50 -> 30 -> 20 -> 40 -> 70 -> 60 -> 80"},
            {"type": "output", "text": "2. In-Order   (Left - Root - Right) : 20 -> 30 -> 40 -> 50 -> 60 -> 70 -> 80 (Sorted)"},
            {"type": "output", "text": "3. Post-Order (Left - Right - Root) : 20 -> 40 -> 30 -> 60 -> 80 -> 70 -> 50"},
            {"type": "blank"},
            {"type": "header", "text": "--- [LANGKAH 3: CARI NILAI ELEMEN] ---"},
            {"type": "input", "prompt": ">> Masukkan nilai yang ingin dicari di Tree: ", "value": "40"},
            {"type": "success", "text": "[FOUND] Nilai 40 ditemukan pada Level 2 (Anak kanan dari Node 30)!"}
        ]

    elif stype in ["sorting", "searching"]:
        title = program_title or "ALGORITMA BUBBLE SORT & BINARY SEARCH"
        steps = [
            {"type": "header", "text": f"=== {title} ==="},
            {"type": "input", "prompt": "Masukkan ukuran array (N): ", "value": "6"},
            {"type": "input", "prompt": ">> Masukkan 6 elemen bilangan acak: ", "value": "64 34 25 12 22 11"},
            {"type": "output", "text": "Array Awal : [ 64, 34, 25, 12, 22, 11 ]"},
            {"type": "blank"},
            {"type": "header", "text": "--- [PROSES SORTING PER ITERASI (PASS)] ---"},
            {"type": "output", "text": "Pass 1 : [ 34, 25, 12, 22, 11, 64 ] (Swap: 5x)"},
            {"type": "output", "text": "Pass 2 : [ 25, 12, 22, 11, 34, 64 ] (Swap: 4x)"},
            {"type": "output", "text": "Pass 3 : [ 12, 22, 11, 25, 34, 64 ] (Swap: 2x)"},
            {"type": "output", "text": "Pass 4 : [ 12, 11, 22, 25, 34, 64 ] (Swap: 1x)"},
            {"type": "output", "text": "Pass 5 : [ 11, 12, 22, 25, 34, 64 ] (Swap: 1x)"},
            {"type": "success", "text": "[SELESAI] Array Terurut: [ 11, 12, 22, 25, 34, 64 ]"},
            {"type": "blank"},
            {"type": "header", "text": "--- [PENCARIAN NILAI (BINARY SEARCH)] ---"},
            {"type": "input", "prompt": ">> Masukkan angka yang dicari: ", "value": "25"},
            {"type": "output", "text": "Iterasi 1: Low=0, High=5, Mid=2 (Nilai: 22) -> Cari di kanan"},
            {"type": "output", "text": "Iterasi 2: Low=3, High=5, Mid=4 (Nilai: 34) -> Cari di kiri"},
            {"type": "output", "text": "Iterasi 3: Low=3, High=3, Mid=3 (Nilai: 25) -> Cocok!"},
            {"type": "success", "text": "[BERHASIL] Angka 25 ditemukan pada indeks ke-3."}
        ]

    else:
        steps = [
            {"type": "header", "text": f"=== {title or 'EKSEKUSI PROGRAM PRAKTIKUM'} ==="},
            {"type": "input", "prompt": "Masukkan pilihan operasi: ", "value": "1"},
            {"type": "success", "text": "[OK] Operasi berhasil diproses."},
            {"type": "input", "prompt": "Tekan Enter untuk keluar...", "value": ""}
        ]

    return steps

def run_interactive_command(
    cmd: Union[List[str], str],
    inputs: List[str],
    cwd: str = None,
    timeout: float = 12.0
) -> List[str]:
    """
    Executes a program interactively using subprocess, feeding input strings sequentially
    and capturing authentic console output dialog lines.
    """
    input_text = "\n".join(inputs) + "\n"
    shell_mode = isinstance(cmd, str)
    
    try:
        proc = subprocess.run(
            cmd,
            input=input_text,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=timeout,
            shell=shell_mode
        )
        out_lines = proc.stdout.splitlines() if proc.stdout else []
        if proc.stderr:
            err_lines = proc.stderr.splitlines()
            out_lines.extend([f"[[MUTED]]{l}[[/MUTED]]" for l in err_lines])
        return out_lines
    except subprocess.TimeoutExpired:
        return ["[ERROR] Program interactive timed out (> 12 detik)."]
    except Exception as e:
        return [f"[ERROR] Gagal menjalankan program: {e}"]

def render_interactive_session_to_image(
    prompt_dir: str,
    scenario_type: str = "stack",
    out_path: str = "terminal_interactive.png",
    entity: str = "Mahasiswa",
    program_title: str = None,
    student_name: str = "Satria Bakti Wijaya",
    student_nim: str = "109092500017",
    compile_cmd: str = None,
    run_cmd: str = ".\\main.exe",
    runner_style: str = "codeblocks",
    window_title: str = "Windows PowerShell - Interactive Execution"
) -> str:
    """
    All-in-one generator: generates an interactive scenario, formats the transcript,
    and calls the authentic terminal renderer to output an image.
    """
    from ngelaprak.renderers.terminal_renderer import render_terminal_output

    steps = generate_interactive_scenario(
        scenario_type=scenario_type,
        entity=entity,
        program_title=program_title,
        student_name=student_name,
        student_nim=student_nim
    )

    lines = build_interactive_terminal_lines(
        prompt_dir=prompt_dir,
        compile_cmd=compile_cmd,
        run_cmd=run_cmd,
        dialog_steps=steps,
        runner_style=runner_style
    )

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    return render_terminal_output(window_title, lines, out_path=out_path)
