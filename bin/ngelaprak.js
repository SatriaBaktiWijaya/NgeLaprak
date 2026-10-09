#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const os = require('os');
const { spawn, execSync } = require('child_process');

const args = process.argv.slice(2);
const command = args[0];

function findPython() {
  const candidates = ['python', 'python3', 'py'];
  for (const cmd of candidates) {
    try {
      execSync(`${cmd} --version`, { stdio: 'ignore' });
      return cmd;
    } catch (e) {}
  }
  return 'python';
}

function copyDirRecursive(src, dest) {
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }
  const entries = fs.readdirSync(src, { withFileTypes: true });
  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDirRecursive(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

function installSkill() {
  console.log('\n==========================================');
  console.log('   NgeLaprak: Universal Laprak Skill Setup');
  console.log('==========================================\n');

  const pyCmd = findPython();
  console.log(`[OK] Python terdeteksi: ${pyCmd}`);

  console.log('[*] Memasang dependensi Python (python-docx, pillow)...');
  try {
    execSync(`${pyCmd} -m pip install python-docx pillow`, { stdio: 'inherit' });
    console.log('[OK] Dependensi Python siap!\n');
  } catch (err) {
    console.warn('[!] Gagal menjalankan pip otomatis, pastikan python-docx & pillow terpasang manual.');
  }

  // 1. Install to Antigravity / Gemini global config
  const geminiDir = path.join(os.homedir(), '.gemini', 'config', 'skills', 'ngelaprak');
  // 2. Install to current workspace .agents if in a project
  const localAgentDir = path.join(process.cwd(), '.agents', 'skills', 'ngelaprak');

  const rootDir = path.join(__dirname, '..');
  const skillMdSource = path.join(rootDir, 'SKILL.md');
  const pkgSource = path.join(rootDir, 'ngelaprak');

  try {
    // Copy to geminiDir
    fs.mkdirSync(geminiDir, { recursive: true });
    if (fs.existsSync(skillMdSource)) {
      fs.copyFileSync(skillMdSource, path.join(geminiDir, 'SKILL.md'));
    }
    if (fs.existsSync(pkgSource)) {
      copyDirRecursive(pkgSource, path.join(geminiDir, 'ngelaprak'));
    }
    console.log(`[OK] Skill terpasang di Global AI Agent: ${geminiDir}`);

    // If cwd is not homedir and not inside .gemini, also copy to local .agents/skills/ngelaprak
    if (process.cwd() !== os.homedir() && !process.cwd().startsWith(path.join(os.homedir(), '.gemini'))) {
      fs.mkdirSync(localAgentDir, { recursive: true });
      if (fs.existsSync(skillMdSource)) {
        fs.copyFileSync(skillMdSource, path.join(localAgentDir, 'SKILL.md'));
      }
      if (fs.existsSync(pkgSource)) {
        copyDirRecursive(pkgSource, path.join(localAgentDir, 'ngelaprak'));
      }
      console.log(`[OK] Skill terpasang di Proyek Lokal: ${localAgentDir}`);
    }

    console.log('\n[SELESAI] Sekarang AI Agent Anda sudah siap otomatis membuat laprak!\n');
  } catch (e) {
    console.error(`[ERROR] Gagal memasang skill: ${e.message}`);
    process.exit(1);
  }
}

if (command === 'install') {
  installSkill();
} else if (!command || command === '--help' || command === '-h') {
  console.log(`
=============================================================
  NgeLaprak CLI & Universal AI Agent Skill (by @SatriaBaktiWijaya)
=============================================================

CARA INSTALL KE AI AGENT:
  1. Via npx skills (Official Skills Package Manager):
     $ npx skills add SatriaBaktiWijaya/NgeLaprak
     $ npx skills add SatriaBaktiWijaya/NgeLaprak -g (Global)

  2. Via npx langsung:
     $ npx ngelaprak install

PERINTAH CLI:
  npx ngelaprak install          Pasang skill & dependensi Python ke sistem
  npx ngelaprak init             Buat struktur folder laprak (Modul/, Laprak/, Code/)
  npx ngelaprak render           Render screenshot IDE otentik
  npx ngelaprak export-pdf       Konversi Word (.docx) ke PDF (.pdf)

CONTOH PENGGUNAAN CHAT AI AGENT:
  Cukup katakan di prompt:
  "Tolong kerjakan laprak modul ini pake skill NgeLaprak. File modul ada
   di folder Modul/, template di Laprak/, dan kodinganku di Code/."
`);
} else {
  // Delegate to Python CLI
  const pyCmd = findPython();
  const pyScript = path.join(__dirname, '..', 'ngelaprak', 'cli.py');
  const py = spawn(pyCmd, [pyScript, ...args], { stdio: 'inherit' });
  py.on('close', (code) => {
    process.exit(code || 0);
  });
}
