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
python3 -m pip install --upgrade wxPython --quiet || echo -e "\033[0;33m[!] wxPython gagal dipasang otomatis (opsional untuk Code::Blocks native di Linux).\033[0m"
echo -e "\033[0;32m[✓] Dependensi Python siap!\033[0m"

# 3. Detect Agent Skills Root
TARGET_DIR="$HOME/.gemini/config/skills/ngelaprak"
mkdir -p "$TARGET_DIR"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

cp "$SCRIPT_DIR/SKILL.md" "$TARGET_DIR/SKILL.md"
rm -rf "$TARGET_DIR/ngelaprak"
cp -r "$SCRIPT_DIR/ngelaprak" "$TARGET_DIR/ngelaprak"
find "$TARGET_DIR/ngelaprak" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

echo -e "\033[0;32m[✓] Skill 'ngelaprak' berhasil dipasang ke Global: $TARGET_DIR\033[0m"

# 4. Install/Update Local Project Skill (.agents/skills/ngelaprak)
LOCAL_DIR="$SCRIPT_DIR/.agents/skills/ngelaprak"
if [ "$SCRIPT_DIR" != "$HOME" ] && [[ "$SCRIPT_DIR" != "$HOME/.gemini"* ]]; then
    mkdir -p "$LOCAL_DIR"
    cp "$SCRIPT_DIR/SKILL.md" "$LOCAL_DIR/SKILL.md"
    rm -rf "$LOCAL_DIR/ngelaprak"
    cp -r "$SCRIPT_DIR/ngelaprak" "$LOCAL_DIR/ngelaprak"
    find "$LOCAL_DIR/ngelaprak" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    echo -e "\033[0;32m[✓] Skill 'ngelaprak' berhasil dipasang ke Proyek Lokal: $LOCAL_DIR\033[0m"
fi

echo -e "\033[0;36mAI Agent siap menyusun laporan praktikum otomatis!\033[0m"
