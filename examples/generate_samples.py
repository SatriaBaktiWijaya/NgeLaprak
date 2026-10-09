import os
import sys
from PIL import Image, ImageDraw, ImageFont

# Add repo to sys.path
REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, REPO_DIR)

from ngelaprak.renderers import (
    render_netbeans_code,
    render_codeblocks_code,
    render_terminal_output,
    frame_windows_gui
)
from ngelaprak.core import LaprakDocxBuilder, export_docx_to_pdf

EXAMPLES_DIR = os.path.join(REPO_DIR, "examples")
TEMPLATE_PATH = os.path.join(REPO_DIR, "ngelaprak", "templates", "template_kampus.docx")

def create_mock_swing_gui(out_path):
    w, h = 640, 420
    img = Image.new("RGBA", (w, h), (240, 240, 240, 255))
    draw = ImageDraw.Draw(img)

    try:
        font_main = ImageFont.truetype("segoeui.ttf", 12)
        font_bold = ImageFont.truetype("segouib.ttf", 13)
        font_header = ImageFont.truetype("segouib.ttf", 15)
    except Exception:
        font_main = ImageFont.load_default()
        font_bold = ImageFont.load_default()
        font_header = ImageFont.load_default()

    # Header banner
    draw.text((20, 16), "SISTEM MANAJEMEN PENJUALAN TOKO BUKU", fill=(20, 40, 90, 255), font=font_header)
    draw.line([(20, 44), (w - 20, 44)], fill=(200, 200, 200, 255), width=1)

    # Form Fields
    labels = ["Kode Buku :", "Judul Buku :", "Kategori :", "Harga (Rp) :", "Stok :"]
    values = ["BK-003", "Struktur Data & Algoritma", "Komputer & Teknologi", "85000", "15"]

    start_y = 60
    for i, (lbl, val) in enumerate(zip(labels, values)):
        y = start_y + (i * 32)
        draw.text((24, y + 4), lbl, fill=(30, 30, 30, 255), font=font_main)
        # Input box
        draw.rectangle([(130, y), (380, y + 24)], fill=(255, 255, 255, 255), outline=(170, 170, 170, 255))
        draw.text((138, y + 4), val, fill=(40, 40, 40, 255), font=font_main)

    # Buttons
    buttons = [("Simpan", (410, 60), (100, 28), (0, 120, 215)), 
               ("Update", (410, 96), (100, 28), (40, 167, 69)),
               ("Hapus", (410, 132), (100, 28), (220, 53, 69)),
               ("Reset", (410, 168), (100, 28), (108, 117, 125))]

    for label, (bx, by), (bw, bh), col in buttons:
        draw.rectangle([(bx, by), (bx + bw, by + bh)], fill=col, outline=(col[0]-20, col[1]-20, col[2]-20, 255))
        draw.text((bx + 26, by + 6), label, fill=(255, 255, 255, 255), font=font_bold)

    # Table section
    table_y = 230
    draw.text((24, table_y - 20), "Daftar Inventaris Buku (Database MySQL Connected):", fill=(50, 50, 50, 255), font=font_bold)

    # Table Header
    draw.rectangle([(20, table_y), (w - 20, table_y + 24)], fill=(225, 230, 240, 255), outline=(180, 180, 180, 255))
    cols = [(28, "No"), (60, "Kode"), (150, "Judul Buku"), (360, "Kategori"), (480, "Harga"), (560, "Stok")]
    for cx, ctitle in cols:
        draw.text((cx, table_y + 4), ctitle, fill=(30, 30, 30, 255), font=font_bold)

    # Table Rows
    rows = [
        ("1", "BK-001", "Pemrograman Java Lanjut", "Informatika", "Rp 95.000", "10"),
        ("2", "BK-002", "Basis Data Relasional", "Sistem Info", "Rp 78.000", "22"),
        ("3", "BK-003", "Struktur Data & Algoritma", "Informatika", "Rp 85.000", "15")
    ]
    for r_idx, row in enumerate(rows):
        ry = table_y + 24 + (r_idx * 24)
        bg_col = (255, 255, 255, 255) if r_idx % 2 == 0 else (248, 248, 248, 255)
        draw.rectangle([(20, ry), (w - 20, ry + 24)], fill=bg_col, outline=(210, 210, 210, 255))
        for col_idx, (cx, _) in enumerate(cols):
            draw.text((cx, ry + 4), row[col_idx], fill=(40, 40, 40, 255), font=font_main)

    # Status Bar
    draw.rectangle([(0, h - 24), (w, h)], fill=(230, 230, 230, 255), outline=(200, 200, 200, 255))
    draw.text((12, h - 19), "[STATUS] Connected to jdbc:mysql://localhost:3306/db_toko | Total Records: 3", fill=(70, 70, 70, 255), font=font_main)

    img.save(out_path)
    return out_path


def generate_adpl_sample():
    print("=== Generating Sample 1: ADPL / PBO (Java Swing & NetBeans) ===")
    out_dir = os.path.join(EXAMPLES_DIR, "adpl_modul4_sample")
    shots_dir = os.path.join(out_dir, "screenshots")
    os.makedirs(shots_dir, exist_ok=True)

    # 1. Render Java Code in NetBeans
    code_koneksi = """package com.toko.database;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class KoneksiDB {
    private static Connection conn;
    private static final String url = "jdbc:mysql://localhost:3306/db_toko";
    private static final String user = "root";
    private static final String pass = "";

    public static Connection getConnection() {
        if (conn == null) {
            try {
                conn = DriverManager.getConnection(url, user, pass);
                System.out.println("Koneksi Database Berhasil!");
            } catch (SQLException e) {
                System.err.println("Gagal koneksi: " + e.getMessage());
            }
        }
        return conn;
    }
}"""
    shot_koneksi = os.path.join(shots_dir, "1_KoneksiDB_NetBeans.png")
    render_netbeans_code("KoneksiDB.java", code_koneksi, start_line=1, out_path=shot_koneksi)

    code_form = """package com.toko.view;

import com.toko.database.KoneksiDB;
import java.sql.*;
import javax.swing.table.DefaultTableModel;

public class KasirForm extends javax.swing.JFrame {
    private DefaultTableModel tableModel;

    public KasirForm() {
        initComponents();
        loadDataBuku();
    }

    private void loadDataBuku() {
        tableModel = (DefaultTableModel) tableBuku.getModel();
        tableModel.setRowCount(0);
        try {
            Connection conn = KoneksiDB.getConnection();
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("SELECT * FROM buku");
            while (rs.next()) {
                tableModel.addRow(new Object[]{
                    rs.getString("kode"),
                    rs.getString("judul"),
                    rs.getString("kategori"),
                    rs.getInt("harga"),
                    rs.getInt("stok")
                });
            }
        } catch (SQLException ex) {
            System.err.println("Error load data: " + ex.getMessage());
        }
    }
}"""
    shot_form = os.path.join(shots_dir, "2_KasirForm_NetBeans.png")
    render_netbeans_code("KasirForm.java", code_form, start_line=1, out_path=shot_form)

    # 2. Render Mock GUI Window Framed
    raw_gui = os.path.join(shots_dir, "raw_gui.png")
    create_mock_swing_gui(raw_gui)
    shot_framed_gui = os.path.join(shots_dir, "3_Kasir_Swing_GUI.png")
    frame_windows_gui(raw_gui, title_text="Form Kasir Toko Buku - Java Swing", out_path=shot_framed_gui, app_icon="java")
    if os.path.exists(raw_gui):
        os.remove(raw_gui)

    # 3. Render MySQL Terminal Output
    sql_lines = [
        "mysql> USE db_toko;",
        "Database changed",
        "mysql> SELECT kode, judul, harga, stok FROM buku;",
        "+---------+---------------------------+-------+------+",
        "| kode    | judul                     | harga | stok |",
        "+---------+---------------------------+-------+------+",
        "| BK-001  | Pemrograman Java Lanjut   | 95000 |   10 |",
        "| BK-002  | Basis Data Relasional     | 78000 |   22 |",
        "| BK-003  | Struktur Data & Algoritma | 85000 |   15 |",
        "+---------+---------------------------+-------+------+",
        "3 rows in set (0.01 sec)",
        "",
        "mysql> "
    ]
    shot_term = os.path.join(shots_dir, "4_MySQL_Terminal.png")
    render_terminal_output("MySQL 8.0 Command Line Client", sql_lines, out_path=shot_term)

    # 4. Assemble Word Document
    docx_out = os.path.join(out_dir, "LAPRAK_SAMPLE_ADPL_MODUL4.docx")
    builder = LaprakDocxBuilder(template_path=TEMPLATE_PATH)
    builder.set_cover_title("PERTEMUAN 4", "MODUL 4: GUI JAVA SWING & DATABASE JDBC")
    builder.clear_guided_section(keep_until_p_index=35)

    builder.add_code_item(
        "1.) KoneksiDB.java",
        [shot_koneksi],
        "Class KoneksiDB bertugas buat ngebangun koneksi aplikasi Java ke database MySQL pake driver JDBC. Di sini dipake variabel statis conn biar koneksinya cuma dibuat sekali (pola singleton sederhana) terus bisa dipake ulang di seluruh class view dan controller.",
        img_width=None
    )

    builder.add_code_item(
        "2.) KasirForm.java",
        [shot_form],
        "Class ini turunan dari JFrame yang nampilin form transaksi kasir. Method loadDataBuku() ngejalanin query SELECT * FROM buku ke database lewat KoneksiDB, terus hasilnya dimasukin baris demi baris ke DefaultTableModel biar otomatis muncul di tabel GUI.",
        img_width=None
    )

    builder.add_output_section([shot_framed_gui, shot_term])
    builder.save(docx_out)
    print(f"[OK] Word document created: {docx_out}")

    # 5. Export to PDF
    pdf_out = os.path.join(out_dir, "LAPRAK_SAMPLE_ADPL_MODUL4.pdf")
    export_docx_to_pdf(docx_out, pdf_out)
    print(f"[OK] PDF document exported: {pdf_out}")


def generate_strukdat_sample():
    print("\n=== Generating Sample 2: Struktur Data (C++ & Code::Blocks) ===")
    out_dir = os.path.join(EXAMPLES_DIR, "strukdat_modul3_sample")
    shots_dir = os.path.join(out_dir, "screenshots")
    os.makedirs(shots_dir, exist_ok=True)

    # 1. Render C++ Code in Code::Blocks
    code_stack_h = """#ifndef STACK_H
#define STACK_H

#define MAX_STACK 10

struct Stack {
    int data[MAX_STACK];
    int top;
};

void createStack(Stack &S);
bool isEmpty(Stack S);
bool isFull(Stack S);
void push(Stack &S, int nilai);
int pop(Stack &S);
void printStack(Stack S);

#endif"""
    shot_stack_h = os.path.join(shots_dir, "1_Stack_h_CodeBlocks.png")
    render_codeblocks_code(code_stack_h, start_line=1, out_path=shot_stack_h)

    code_main_cpp = """#include <iostream>
#include "Stack.h"
using namespace std;

void createStack(Stack &S) {
    S.top = -1;
}

bool isEmpty(Stack S) {
    return S.top == -1;
}

bool isFull(Stack S) {
    return S.top == MAX_STACK - 1;
}

void push(Stack &S, int nilai) {
    if (!isFull(S)) {
        S.top++;
        S.data[S.top] = nilai;
        cout << "Berhasil push nilai: " << nilai << endl;
    } else {
        cout << "Stack penuh!" << endl;
    }
}

int main() {
    Stack S;
    createStack(S);
    push(S, 10);
    push(S, 25);
    push(S, 50);
    return 0;
}"""
    shot_main_cpp = os.path.join(shots_dir, "2_main_cpp_CodeBlocks.png")
    render_codeblocks_code(code_main_cpp, start_line=1, out_path=shot_main_cpp)

    # 2. Terminal Output
    term_lines = [
        "PS D:\\COOLYEAH\\Semester 3\\StrukturData> g++ main.cpp -o main.exe",
        "PS D:\\COOLYEAH\\Semester 3\\StrukturData> .\\main.exe",
        "Berhasil push nilai: 10",
        "Berhasil push nilai: 25",
        "Berhasil push nilai: 50",
        "",
        "Process returned 0 (0x0)   execution time : 0.042 s",
        "Press any key to continue."
    ]
    shot_term = os.path.join(shots_dir, "3_Console_Output.png")
    render_terminal_output("Windows PowerShell - g++ compiler", term_lines, out_path=shot_term)

    # 3. Assemble Word Document
    docx_out = os.path.join(out_dir, "LAPRAK_SAMPLE_STRUKDAT_MODUL3.docx")
    builder = LaprakDocxBuilder(template_path=TEMPLATE_PATH)
    builder.set_cover_title("PERTEMUAN 3", "MODUL 3: ABSTRACT DATA TYPE (ADT) & STACK")
    builder.clear_guided_section(keep_until_p_index=35)

    builder.add_code_item(
        "1.) Stack.h",
        [shot_stack_h],
        "File header Stack.h berisi definisi struct Stack dengan kapasitas maksimal 10 elemen integer. Pointer top diinisialisasi untuk nandain posisi elemen paling atas sesuai prinsip LIFO (Last In First Out).",
        img_width=None
    )

    builder.add_code_item(
        "2.) main.cpp",
        [shot_main_cpp],
        "Fungsi utama menginisialisasi stack lewat createStack(S) dengan ngeset top ke -1. Kemudian dilakukan pemanggilan operasi push() buat nambahin angka 10, 25, dan 50 ke tumpukan data.",
        img_width=None
    )

    builder.add_output_section([shot_term])
    builder.save(docx_out)
    print(f"[OK] Word document created: {docx_out}")

    # 4. Export to PDF
    pdf_out = os.path.join(out_dir, "LAPRAK_SAMPLE_STRUKDAT_MODUL3.pdf")
    export_docx_to_pdf(docx_out, pdf_out)
    print(f"[OK] PDF document exported: {pdf_out}")


if __name__ == "__main__":
    generate_adpl_sample()
    generate_strukdat_sample()
    print("\n[SUCCESS] Semua sample laprak (.docx & .pdf) berhasil dibuat!")
