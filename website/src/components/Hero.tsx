import React, { useState } from 'react'
import { Terminal, Copy, Check, Sparkles, FileCode, FileText, ArrowRight, ShieldCheck, Code2, Download, Eye } from 'lucide-react'

export const Hero: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'npx' | 'powershell' | 'bash'>('npx')
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
      <div className="max-w-5xl mx-auto px-4 sm:px-6 relative z-10 text-center">
        {/* Supaste-style Category Pill */}
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/[0.04] border border-white/10 text-slate-300 text-xs font-medium mb-6 backdrop-blur-xl shadow-lg">
          <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
          <span>Universal Agent Skill v1.2</span>
          <span className="w-1 h-1 rounded-full bg-slate-600" />
          <span className="text-indigo-300 font-mono">NetBeans & C++ Ready</span>
        </div>

        {/* Supaste-inspired Display Headline */}
        <h1 className="text-4xl sm:text-6xl md:text-7xl font-extrabold tracking-tight text-white mb-6 leading-[1.08] font-sans max-w-4xl mx-auto">
          Ubah 3 Berkas.{' '}
          <span className="italic font-serif font-normal text-transparent bg-clip-text bg-gradient-to-r from-indigo-300 via-purple-300 to-pink-300 block sm:inline">
            Jadi Laporan Sempurna.
          </span>
        </h1>

        {/* Minimal Subtitle */}
        <p className="text-sm sm:text-base md:text-lg text-slate-400 max-w-2xl mx-auto mb-9 leading-relaxed font-normal">
          Otomatisasi pembuatan Laporan Praktikum (.docx & .pdf) lengkap dengan screenshot IDE autentik, penjelasan alami mahasiswa, dan struktur project standar industri.
        </p>

        {/* Supaste-style Central Action Terminal Pill */}
        <div className="max-w-md mx-auto mb-10">
          <div className="rounded-full bg-[#0D1020]/90 border border-white/15 p-1.5 shadow-2xl shadow-indigo-950/60 backdrop-blur-xl flex items-center justify-between gap-2">
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

          {/* Quick tab switcher & compatibility note */}
          <div className="flex items-center justify-center gap-3 mt-3 text-[11px] text-slate-500 font-mono">
            <span>Tab:</span>
            <button
              onClick={() => setActiveTab('npx')}
              className={`hover:text-slate-300 transition-colors ${activeTab === 'npx' ? 'text-indigo-400 font-bold underline' : ''}`}
            >
              npx
            </button>
            <span>•</span>
            <button
              onClick={() => setActiveTab('powershell')}
              className={`hover:text-slate-300 transition-colors ${activeTab === 'powershell' ? 'text-indigo-400 font-bold underline' : ''}`}
            >
              powershell
            </button>
            <span>•</span>
            <button
              onClick={() => setActiveTab('bash')}
              className={`hover:text-slate-300 transition-colors ${activeTab === 'bash' ? 'text-indigo-400 font-bold underline' : ''}`}
            >
              bash
            </button>
            <span className="hidden sm:inline">•</span>
            <span className="hidden sm:inline text-slate-500">Cursor / Claude / Gemini CLI</span>
          </div>
        </div>

        {/* Centerpiece: Floating Supaste-style Dynamic Preview Frame */}
        <div className="max-w-4xl mx-auto rounded-3xl bg-[#0D1020]/80 border border-white/10 p-4 sm:p-6 shadow-2xl backdrop-blur-2xl text-left relative overflow-hidden group">
          {/* Subtle glow border aura */}
          <div className="absolute -top-24 left-1/2 -translate-x-1/2 w-96 h-48 bg-indigo-500/20 rounded-full blur-3xl pointer-events-none" />

          {/* Window Header */}
          <div className="flex items-center justify-between pb-4 mb-4 border-b border-white/8 text-xs font-mono">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-[#FF5F56]" />
              <div className="w-3 h-3 rounded-full bg-[#FFBD2E]" />
              <div className="w-3 h-3 rounded-full bg-[#27C93F]" />
              <span className="text-slate-400 ml-2 font-medium">NgeLaprak Workflow Live Simulator</span>
            </div>
            <div className="flex items-center gap-2 text-emerald-400 text-[11px]">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              <span>Ready for Output</span>
            </div>
          </div>

          {/* Interactive Flow Grid */}
          <div className="grid grid-cols-1 md:grid-cols-12 gap-3 items-center">
            {/* Inputs Column (5 cols) */}
            <div className="md:col-span-5 space-y-2">
              <span className="text-[10px] font-mono uppercase tracking-wider text-slate-500 block px-1">
                3 Berkas Input
              </span>

              <div className="p-2.5 rounded-xl bg-black/40 border border-white/8 flex items-center gap-3">
                <div className="w-7 h-7 rounded-lg bg-blue-500/20 text-blue-400 flex items-center justify-center shrink-0">
                  <FileCode className="w-4 h-4" />
                </div>
                <div className="min-w-0 flex-1">
                  <div className="text-xs font-bold text-white truncate">1. Source Code</div>
                  <div className="text-[10px] font-mono text-slate-400 truncate">Stack.cpp / Main.java</div>
                </div>
                <span className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-indigo-500/20 text-indigo-300">Wajib</span>
              </div>

              <div className="p-2.5 rounded-xl bg-black/40 border border-white/8 flex items-center gap-3">
                <div className="w-7 h-7 rounded-lg bg-purple-500/20 text-purple-400 flex items-center justify-center shrink-0">
                  <FileText className="w-4 h-4" />
                </div>
                <div className="min-w-0 flex-1">
                  <div className="text-xs font-bold text-white truncate">2. Modul Praktikum</div>
                  <div className="text-[10px] font-mono text-slate-400 truncate">Modul_03_Strukdat.pdf</div>
                </div>
                <span className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-purple-500/20 text-purple-300">Wajib</span>
              </div>

              <div className="p-2.5 rounded-xl bg-black/40 border border-white/8 flex items-center gap-3">
                <div className="w-7 h-7 rounded-lg bg-amber-500/20 text-amber-400 flex items-center justify-center shrink-0">
                  <FileText className="w-4 h-4" />
                </div>
                <div className="min-w-0 flex-1">
                  <div className="text-xs font-bold text-white truncate">3. Template Word</div>
                  <div className="text-[10px] font-mono text-slate-400 truncate">Template_Lab_SI.docx</div>
                </div>
                <span className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300">Opsional</span>
              </div>
            </div>

            {/* Middle Arrow / Engine (2 cols) */}
            <div className="md:col-span-2 flex flex-col items-center justify-center py-2 text-center">
              <div className="w-10 h-10 rounded-full bg-gradient-to-r from-indigo-500 to-purple-600 flex items-center justify-center text-white shadow-lg shadow-indigo-500/30 my-1">
                <Sparkles className="w-5 h-5" />
              </div>
              <span className="text-[10px] font-mono text-indigo-300 mt-1">Autonomous</span>
              <span className="text-[9px] font-mono text-slate-500">~15-30 detik</span>
            </div>

            {/* Outputs Column (5 cols) */}
            <div className="md:col-span-5 space-y-2">
              <span className="text-[10px] font-mono uppercase tracking-wider text-slate-500 block px-1">
                Hasil Siap Kumpul
              </span>

              {/* PDF Result */}
              <div className="p-3 rounded-xl bg-red-950/20 border border-red-500/30 flex items-center justify-between gap-3">
                <div className="flex items-center gap-2.5 min-w-0">
                  <div className="w-7 h-7 rounded-lg bg-red-500/20 text-red-400 flex items-center justify-center shrink-0">
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
                  className="p-1.5 rounded-lg bg-red-600 hover:bg-red-500 text-white shrink-0 transition-colors"
                  title="Unduh PDF"
                >
                  <Download className="w-3.5 h-3.5" />
                </a>
              </div>

              {/* Word Result */}
              <div className="p-3 rounded-xl bg-blue-950/20 border border-blue-500/30 flex items-center justify-between gap-3">
                <div className="flex items-center gap-2.5 min-w-0">
                  <div className="w-7 h-7 rounded-lg bg-blue-500/20 text-blue-400 flex items-center justify-center shrink-0">
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
                  className="p-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white shrink-0 transition-colors"
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
        </div>
      </div>
    </section>
  )
}
