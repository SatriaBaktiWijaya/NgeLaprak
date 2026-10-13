import React, { useState } from 'react'
import { Terminal, Copy, Check, Sparkles, FileCode, FileText, ArrowRight, ShieldCheck, Code2, Download, Eye, School, TerminalSquare } from 'lucide-react'
import { Dithering } from '@paper-design/shaders-react'

export const Hero: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'npx' | 'powershell' | 'bash'>('npx')
  const [simulatorTab, setSimulatorTab] = useState<'pipeline' | 'cli' | 'cover'>('pipeline')
  const [copied, setCopied] = useState(false)

  const commands = {
    npx: 'npx skills add ngelaprak',
    powershell: 'irm https://raw.githubusercontent.com/khilma-ainunnajah/NgeLaprak/main/install.ps1 | iex',
    bash: 'curl -fsSL https://raw.githubusercontent.com/khilma-ainunnajah/NgeLaprak/main/install.sh | bash'
  }

  const handleCopy = () => {
    navigator.clipboard.writeText(commands[activeTab])
    setCopied(true)
    setTimeout(() => setCopied(false), 2200)
  }

  return (
    <section className="relative pt-32 pb-20 md:pt-40 md:pb-28 overflow-hidden">
      {/* Dynamic Dithering Shader Background */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none select-none z-0">
        <Dithering
          width="100%"
          height="100%"
          colorBack="#090a0f"
          colorFront="#6366f1"
          shape="sphere"
          type="4x4"
          size={2}
          speed={0.75}
          scale={0.75}
          className="w-full h-full opacity-35 md:opacity-45"
        />
        {/* Soft radial vignette so text is crystal clear while dither sphere glows around it */}
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(9,10,15,0.25)_0%,transparent_50%,#090A0F_85%)]" />
        <div className="absolute inset-0 bg-gradient-to-b from-[#090A0F]/70 via-transparent to-[#090A0F]" />
      </div>

      {/* Background Telkom University Logo & Ambient Crimson Glow */}
      <div className="absolute top-[37%] left-1/2 -translate-x-1/2 -translate-y-1/2 pointer-events-none select-none z-0 flex items-center justify-center">
        {/* Subtle Telkom red ambient aura */}
        <div className="absolute w-[360px] h-[360px] sm:w-[480px] sm:h-[480px] bg-[#EE2E24]/[0.08] blur-[100px] rounded-full pointer-events-none" />
        <img
          src="/images/logo_telkom.png"
          alt="Telkom University Logo Background"
          className="w-[240px] sm:w-[340px] md:w-[420px] object-contain opacity-[0.11] mix-blend-screen filter drop-shadow-[0_0_60px_rgba(238,46,36,0.22)]"
        />
      </div>

      <div className="max-w-5xl mx-auto px-4 sm:px-6 relative z-10 text-center">
        {/* Subtle Category Pill */}
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/[0.04] border border-white/10 text-slate-300 text-xs font-medium mb-6 backdrop-blur-xl shadow-lg">
          <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
          <span>Universal Agent Skill v1.3</span>
          <span className="w-1 h-1 rounded-full bg-slate-600" />
          <span className="text-indigo-300 font-mono">Multi-Campus & CLI Simulator</span>
        </div>

        {/* Display Headline with Tight Tracking */}
        <h1 className="text-4xl sm:text-6xl md:text-7xl font-extrabold tracking-[-0.035em] text-white mb-6 leading-[1.05] font-sans max-w-4xl mx-auto drop-shadow-[0_4px_24px_rgba(0,0,0,0.8)]">
          Ubah 3 Berkas.{' '}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-slate-100 via-indigo-200 to-indigo-400">
            Laporan Lab Sempurna.
          </span>
        </h1>

        {/* Minimal High-Contrast Subtitle */}
        <p className="text-sm sm:text-base md:text-lg text-slate-200/90 max-w-2xl mx-auto mb-9 leading-relaxed font-normal drop-shadow-[0_2px_12px_rgba(0,0,0,0.9)]">
          Skill AI Agent yang otomatis merapikan folder, membuat kodingan resmi IDE (NetBeans/Code::Blocks), render screenshot konsol interaktif, dan menyusun dokumen Word & PDF siap kumpul.
        </p>

        {/* Command Terminal Bar */}
        <div className="max-w-md mx-auto mb-10">
          <div className="rounded-full bg-[#0D101D] border border-white/15 p-1.5 shadow-2xl shadow-black/80 backdrop-blur-xl flex items-center justify-between gap-2">
            <div className="flex items-center gap-2 pl-3.5 pr-2 font-mono text-xs text-slate-200 overflow-x-auto scrollbar-none">
              <span className="text-indigo-400 font-bold select-none">$</span>
              <span className="whitespace-nowrap font-medium tracking-wide">{commands[activeTab]}</span>
            </div>

            <button
              onClick={handleCopy}
              className={`flex items-center gap-1.5 px-4 py-2 rounded-full text-xs font-semibold shrink-0 transition-all duration-200 ${
                copied
                  ? 'bg-emerald-500 text-white shadow-md shadow-emerald-500/30'
                  : 'bg-white text-slate-950 hover:bg-slate-100 shadow-md active:scale-95'
              }`}
              title="Salin ke clipboard"
            >
              {copied ? (
                <>
                  <Check className="w-3.5 h-3.5" />
                  <span>Tersalin!</span>
                </>
              ) : (
                <>
                  <Copy className="w-3.5 h-3.5 text-slate-800" />
                  <span>Copy</span>
                </>
              )}
            </button>
          </div>

          {/* Quick tab switcher */}
          <div className="flex items-center justify-center gap-3 mt-3 text-[11px] text-slate-400 font-mono">
            <span>Tab:</span>
            <button
              onClick={() => setActiveTab('npx')}
              className={`hover:text-slate-200 transition-colors ${activeTab === 'npx' ? 'text-indigo-400 font-bold underline' : ''}`}
            >
              npx
            </button>
            <span>•</span>
            <button
              onClick={() => setActiveTab('powershell')}
              className={`hover:text-slate-200 transition-colors ${activeTab === 'powershell' ? 'text-indigo-400 font-bold underline' : ''}`}
            >
              powershell
            </button>
            <span>•</span>
            <button
              onClick={() => setActiveTab('bash')}
              className={`hover:text-slate-200 transition-colors ${activeTab === 'bash' ? 'text-indigo-400 font-bold underline' : ''}`}
            >
              bash
            </button>
            <span className="hidden sm:inline">•</span>
            <span className="hidden sm:inline text-slate-500">Antigravity / Cursor / Claude Code</span>
          </div>
        </div>

        {/* Floating Centerpiece Preview Frame */}
        <div className="max-w-4xl mx-auto rounded-3xl bg-[#0D101D]/90 border border-white/10 p-4 sm:p-6 shadow-2xl backdrop-blur-2xl text-left relative overflow-hidden group">
          {/* Subtle glow border aura */}
          <div className="absolute -top-24 left-1/2 -translate-x-1/2 w-96 h-48 bg-indigo-500/15 rounded-full blur-3xl pointer-events-none" />

          {/* Window Header with Simulator Mode Switcher */}
          <div className="flex flex-wrap items-center justify-between gap-3 pb-4 mb-4 border-b border-white/8 text-xs font-mono">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-[#FF5F56]" />
              <div className="w-3 h-3 rounded-full bg-[#FFBD2E]" />
              <div className="w-3 h-3 rounded-full bg-[#27C93F]" />
              <span className="text-slate-400 ml-2 font-medium">NgeLaprak Workflow Simulator</span>
            </div>

            {/* Sub-tabs */}
            <div className="flex items-center gap-1.5 p-1 rounded-xl bg-black/40 border border-white/5">
              <button
                onClick={() => setSimulatorTab('pipeline')}
                className={`px-2.5 py-1 rounded-lg text-[11px] transition-colors ${
                  simulatorTab === 'pipeline' ? 'bg-indigo-600 text-white font-medium' : 'text-slate-400 hover:text-white'
                }`}
              >
                Alur 3-Berkas
              </button>
              <button
                onClick={() => setSimulatorTab('cli')}
                className={`px-2.5 py-1 rounded-lg text-[11px] transition-colors ${
                  simulatorTab === 'cli' ? 'bg-indigo-600 text-white font-medium' : 'text-slate-400 hover:text-white'
                }`}
              >
                CLI Simulator
              </button>
              <button
                onClick={() => setSimulatorTab('cover')}
                className={`px-2.5 py-1 rounded-lg text-[11px] transition-colors ${
                  simulatorTab === 'cover' ? 'bg-indigo-600 text-white font-medium' : 'text-slate-400 hover:text-white'
                }`}
              >
                Multi-Kampus
              </button>
            </div>
          </div>

          {/* TAB 1: Pipeline Flow */}
          {simulatorTab === 'pipeline' && (
            <div className="grid grid-cols-1 md:grid-cols-12 gap-3 items-center">
              {/* Inputs Column (5 cols) */}
              <div className="md:col-span-5 space-y-2">
                <span className="text-[10px] font-mono uppercase tracking-wider text-slate-400 block px-1">
                  Berkas Input Praktikum
                </span>

                <div className="p-2.5 rounded-xl bg-black/40 border border-white/8 flex items-center gap-3">
                  <div className="w-7 h-7 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center shrink-0">
                    <FileCode className="w-4 h-4" />
                  </div>
                  <div className="min-w-0 flex-1">
                    <div className="text-xs font-bold text-white truncate">1. Source Code</div>
                    <div className="text-[10px] font-mono text-slate-400 truncate">Stack.cpp / Main.java (atau dibuatkan)</div>
                  </div>
                  <span className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-indigo-500/20 text-indigo-300">Auto-Detect</span>
                </div>

                <div className="p-2.5 rounded-xl bg-black/40 border border-white/8 flex items-center gap-3">
                  <div className="w-7 h-7 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center shrink-0">
                    <FileText className="w-4 h-4" />
                  </div>
                  <div className="min-w-0 flex-1">
                    <div className="text-xs font-bold text-white truncate">2. Modul Praktikum</div>
                    <div className="text-[10px] font-mono text-slate-400 truncate">Modul_03_Strukdat.pdf</div>
                  </div>
                  <span className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-indigo-500/20 text-indigo-300">Wajib</span>
                </div>

                <div className="p-2.5 rounded-xl bg-black/40 border border-white/8 flex items-center gap-3">
                  <div className="w-7 h-7 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center shrink-0">
                    <FileText className="w-4 h-4" />
                  </div>
                  <div className="min-w-0 flex-1">
                    <div className="text-xs font-bold text-white truncate">3. Template Word / PDF</div>
                    <div className="text-[10px] font-mono text-slate-400 truncate">Template_Laprak_UI_UGM_ITS.docx</div>
                  </div>
                  <span className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-slate-500/20 text-slate-300">Opsional</span>
                </div>
              </div>

              {/* Middle Engine (2 cols) */}
              <div className="md:col-span-2 flex flex-col items-center justify-center py-2 text-center">
                <div className="w-10 h-10 rounded-full bg-indigo-600 flex items-center justify-center text-white shadow-lg shadow-indigo-500/30 my-1">
                  <Sparkles className="w-5 h-5" />
                </div>
                <span className="text-[10px] font-mono text-indigo-300 mt-1">Autonomous</span>
                <span className="text-[9px] font-mono text-slate-400">~15-30 detik</span>
              </div>

              {/* Outputs Column (5 cols) */}
              <div className="md:col-span-5 space-y-2">
                <span className="text-[10px] font-mono uppercase tracking-wider text-slate-400 block px-1">
                  Hasil Siap Kumpul
                </span>

                {/* PDF Result */}
                <div className="p-3 rounded-xl bg-black/40 border border-white/10 flex items-center justify-between gap-3">
                  <div className="flex items-center gap-2.5 min-w-0">
                    <div className="w-7 h-7 rounded-lg bg-rose-500/20 text-rose-400 flex items-center justify-center shrink-0">
                      <FileText className="w-4 h-4" />
                    </div>
                    <div className="min-w-0">
                      <div className="text-xs font-bold text-white truncate">Laporan_Praktikum.pdf</div>
                      <div className="text-[10px] text-slate-400">Margin 4-4-3-3 & Cover Resmi</div>
                    </div>
                  </div>
                  <a
                    href="/samples/strukdat/LAPRAK_SAMPLE_STRUKDAT_MODUL3.pdf"
                    download
                    className="p-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-white shrink-0 transition-colors"
                    title="Unduh PDF"
                  >
                    <Download className="w-3.5 h-3.5" />
                  </a>
                </div>

                {/* Word Result */}
                <div className="p-3 rounded-xl bg-black/40 border border-white/10 flex items-center justify-between gap-3">
                  <div className="flex items-center gap-2.5 min-w-0">
                    <div className="w-7 h-7 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center shrink-0">
                      <FileText className="w-4 h-4" />
                    </div>
                    <div className="min-w-0">
                      <div className="text-xs font-bold text-white truncate">Laporan_Praktikum.docx</div>
                      <div className="text-[10px] text-slate-400">100% Editable & Times New Roman</div>
                    </div>
                  </div>
                  <a
                    href="/samples/strukdat/LAPRAK_SAMPLE_STRUKDAT_MODUL3.docx"
                    download
                    className="p-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-white shrink-0 transition-colors"
                    title="Unduh DOCX"
                  >
                    <Download className="w-3.5 h-3.5" />
                  </a>
                </div>

                <a
                  href="#samples"
                  className="flex items-center justify-center gap-1.5 py-1.5 text-center text-xs text-indigo-300 hover:text-white transition-colors font-mono"
                >
                  <Eye className="w-3.5 h-3.5" />
                  <span>Inspeksi Dokumen Lengkap</span>
                </a>
              </div>
            </div>
          )}

          {/* TAB 2: CLI Interactive Simulation */}
          {simulatorTab === 'cli' && (
            <div className="rounded-xl bg-[#08090E] border border-white/5 p-4 font-mono text-xs text-slate-300 space-y-1.5 shadow-inner leading-relaxed">
              <div className="text-indigo-400">PS D:\COOLYEAH\Semester 3\StrukturData&gt; .\main.exe</div>
              <div className="text-amber-300 font-bold">=== PROGRAM SIMULASI ABSTRACT DATA TYPE (STACK) ===</div>
              <div className="text-slate-400">Praktikan : Satria Bakti Wijaya (109092500017)</div>
              <div>Pilih Menu [1. Push, 2. Pop, 3. Peek, 4. Display, 5. Exit]: <span className="bg-white/20 text-white font-bold px-1 rounded">1</span></div>
              <div>&gt;&gt; Masukkan elemen nilai: <span className="bg-white/20 text-white font-bold px-1 rounded">10</span></div>
              <div className="text-emerald-400">[OK] Nilai 10 berhasil didorong ke Stack (Top sekarang: 0)</div>
              <div>Pilih Menu [1. Push, 2. Pop, 3. Peek, 4. Display, 5. Exit]: <span className="bg-white/20 text-white font-bold px-1 rounded">1</span></div>
              <div>&gt;&gt; Masukkan elemen nilai: <span className="bg-white/20 text-white font-bold px-1 rounded">25</span></div>
              <div className="text-emerald-400">[OK] Nilai 25 berhasil didorong ke Stack (Top sekarang: 1)</div>
              <div className="text-slate-500 pt-1 text-[11px]">------------------------------------------------------------------------</div>
              <div className="text-slate-500 text-[11px]">Process returned 0 (0x0)   execution time : 0.042 s</div>
            </div>
          )}

          {/* TAB 3: Multi-Campus Adaptive Cover */}
          {simulatorTab === 'cover' && (
            <div className="p-4 rounded-xl bg-black/40 border border-white/5 space-y-3">
              <div className="flex items-center gap-2 text-xs font-semibold text-white">
                <School className="w-4 h-4 text-indigo-400" />
                <span>Agnostik Kampus & Auto-Extraction Logo PDF</span>
              </div>
              <p className="text-xs text-slate-400 leading-relaxed">
                Mendeteksi universitas (UI, UGM, ITB, ITS, Telkom, Undip, dll.), fakultas, program studi, serta format nomor mahasiswa (NIM, NPM, NRP). Jika template hanya berupa PDF, logo cover otomatis diekstrak dan disematkan ke Word baru.
              </p>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-1 font-mono text-[11px]">
                <div className="p-2 rounded bg-white/5 border border-white/5 text-center text-slate-300">ITS (NRP)</div>
                <div className="p-2 rounded bg-white/5 border border-white/5 text-center text-slate-300">UGM / UI (NIM)</div>
                <div className="p-2 rounded bg-white/5 border border-white/5 text-center text-slate-300">UPN (NPM)</div>
                <div className="p-2 rounded bg-white/5 border border-white/5 text-center text-indigo-300">Auto Logo PDF</div>
              </div>
            </div>
          )}
        </div>
      </div>
    </section>
  )
}
