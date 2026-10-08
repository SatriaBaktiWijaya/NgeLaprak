#!/usr/bin/env bash
# ============================================================
# NgeLaprak Installer for Linux / macOS
# ============================================================

set -e

echo -e "\033[0;36m==========================================\033[0m"
echo -e "\033[0;36m   NgeLaprak: Universal Laprak Skill Setup\033[0m"
echo -e "\033[0;36m==========================================\033[0m"

# 1. Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "\033[0;31mPython 3 tidak ditemukan! Harap pasang Python 3 terlebih dahulu.\033[0m"
    exit 1
fi

echo -e "\033[0;32m[✓] Python 3 terdeteksi: $(python3 --version)\033[0m"

# 2. Install Dependencies
echo -e "\n\033[0;33m[*] Memasang dependensi Python...\033[0m"
python3 -m pip install --upgrade python-docx pypdf pdfplumber pillow --quiet
echo -e "\033[0;32m[✓] Dependensi Python siap!\033[0m"

# 3. Detect Agent Skills Root
TARGET_DIR="$HOME/.gemini/config/skills/ngelaprak"
mkdir -p "$TARGET_DIR"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

cp "$SCRIPT_DIR/SKILL.md" "$TARGET_DIR/SKILL.md"
rm -rf "$TARGET_DIR/ngelaprak"
cp -r "$SCRIPT_DIR/ngelaprak" "$TARGET_DIR/ngelaprak"

echo -e "\033[0;32m[✓] Skill 'ngelaprak' berhasil dipasang ke: $TARGET_DIR\033[0m"
echo -e "\033[0;36mAI Agent siap menyusun laporan praktikum otomatis!\033[0m"
