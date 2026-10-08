# ============================================================
# NgeLaprak Installer for Windows (PowerShell)
# ============================================================

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   NgeLaprak: Universal Laprak Skill Setup" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python terdeteksi: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Error "Python tidak ditemukan! Silakan instal Python 3.9+ terlebih dahulu."
    exit 1
}

# 2. Install Python Dependencies
Write-Host ""
Write-Host "[*] Memasang dependensi Python..." -ForegroundColor Yellow
python -m pip install --upgrade python-docx pypdf pdfplumber pillow --quiet
Write-Host "[OK] Dependensi Python siap!" -ForegroundColor Green

# 3. Detect Agent Skills Root
$userProfile = [System.Environment]::GetFolderPath('UserProfile')
$globalSkillDir = Join-Path $userProfile ".gemini\config\skills\ngelaprak"

Write-Host ""
Write-Host "[*] Mendaftarkan skill ke direktori AI Agent: $globalSkillDir" -ForegroundColor Yellow

if (!(Test-Path $globalSkillDir)) {
    New-Item -ItemType Directory -Path $globalSkillDir -Force | Out-Null
}

$currentDir = $PSScriptRoot
if ([string]::IsNullOrEmpty($currentDir)) {
    $currentDir = (Get-Location).Path
}

# Copy SKILL.md
Copy-Item -Path (Join-Path $currentDir "SKILL.md") -Destination (Join-Path $globalSkillDir "SKILL.md") -Force

# Copy ngelaprak python package
$targetPkgDir = Join-Path $globalSkillDir "ngelaprak"
if (Test-Path $targetPkgDir) {
    Remove-Item -Recurse -Force $targetPkgDir
}
Copy-Item -Path (Join-Path $currentDir "ngelaprak") -Destination $targetPkgDir -Recurse -Force

Write-Host "[OK] Skill 'ngelaprak' berhasil didaftarkan ke agent secara global!" -ForegroundColor Green
Write-Host ""
Write-Host "Sekarang AI Agent Anda sudah bisa otomatis mengerjakan laprak!" -ForegroundColor Cyan
