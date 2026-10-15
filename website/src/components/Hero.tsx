import React, { useState } from 'react'
import { Terminal, Copy, Check, Sparkles, FileCode, FileText, ArrowRight, Download, Eye, BookOpen, LayoutTemplate } from 'lucide-react'
import { ImageDithering } from '@paper-design/shaders-react'

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
      {/* Dynamic Image Dithering Shader Background with Telkom University Purwokerto photo */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none select-none z-0">
        <ImageDithering
          width="100%"
          height="100%"
          image="/images/OIP.webp"
          colorBack="#090a0f"
          colorFront="#6366f1"
          colorHighlight="#818cf8"
          originalColors={false}
          inverted={false}
          type="8x8"
          size={2}
          colorSteps={2}
          fit="cover"
          className="w-full h-full opacity-30 md:opacity-40"
        />
        {/* Soft radial vignette & vertical gradient overlay to guarantee text legibility */}
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(9,10,15,0.3)_0%,transparent_50%,#090A0F_85%)]" />
        <div className="absolute inset-0 bg-gradient-to-b from-[#090A0F]/75 via-transparent to-[#090A0F]" />
      </div>

      <div className="max-w-5xl mx-auto px-4 sm:px-6 relative z-10 text-center">
        {/* Subtle Category Pill */}
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/[0.04] border border-white/10 text-slate-300 text-xs font-medium mb-6 backdrop-blur-xl shadow-lg">
          <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
          <span>Universal Agent Skill v1.3</span>
          <span className="w-1 h-1 rounded-full bg-slate-600" />
          <span className="text-indigo-300 font-mono">Alur Otomatis 2-Berkas</span>
        </div>

        {/* Display Headline with Tight Tracking */}
        <h1 className="text-4xl sm:text-6xl md:text-7xl font-extrabold tracking-[-0.035em] text-white mb-6 leading-[1.05] font-sans max-w-4xl mx-auto drop-shadow-[0_4px_24px_rgba(0,0,0,0.8)]">
          Kasih 2 Berkas,{' '}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-slate-100 via-indigo-200 to-indigo-400">
            Laprak Selesai.
          </span>
        </h1>

        {/* Minimal High-Contrast Subtitle */}
        <p className="text-sm sm:text-base md:text-lg text-slate-200/90 max-w-2xl mx-auto mb-9 leading-relaxed font-normal drop-shadow-[0_2px_12px_rgba(0,0,0,0.9)]">
          Cukup sediakan Modul Praktikum dan Template dokumen kampus. AI Agent merapikan struktur kodingan, render screenshot IDE resmi, dan menyusun dokumen Word & PDF siap kumpul.
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
                  : 'bg-white text-slate-950 hover:bg-slate-100 shadow-md active:scale-95 cursor-pointer'
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

          {/* Quick tab switcher (Antigravity/Cursor/Claude Code text removed to prevent redundancy) */}
          <div className="flex items-center justify-center gap-3 mt-3 text-[11px] text-slate-400 font-mono">
            <span>Tab:</span>
            <button
              onClick={() => setActiveTab('npx')}
              className={`hover:text-slate-200 transition-colors cursor-pointer ${activeTab === 'npx' ? 'text-indigo-400 font-bold underline' : ''}`}
            >
              npx
            </button>
            <span>•</span>
            <button
              onClick={() => setActiveTab('powershell')}
              className={`hover:text-slate-200 transition-colors cursor-pointer ${activeTab === 'powershell' ? 'text-indigo-400 font-bold underline' : ''}`}
            >
              powershell
            </button>
            <span>•</span>
            <button
              onClick={() => setActiveTab('bash')}
              className={`hover:text-slate-200 transition-colors cursor-pointer ${activeTab === 'bash' ? 'text-indigo-400 font-bold underline' : ''}`}
            >
              bash
            </button>
          </div>
        </div>

        {/* Floating Centerpiece Preview Frame: Minimalist Visual File-Flow Diagram */}
        <div className="max-w-4xl mx-auto rounded-3xl bg-[#0D101D]/90 border border-white/10 p-5 sm:p-7 shadow-2xl backdrop-blur-2xl text-left relative overflow-hidden group">
          {/* Subtle glow border aura */}
          <div className="absolute -top-24 left-1/2 -translate-x-1/2 w-96 h-48 bg-indigo-500/15 rounded-full blur-3xl pointer-events-none" />

          {/* Window Header */}
          <div className="flex items-center justify-between pb-4 mb-6 border-b border-white/8 text-xs font-mono">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-[#FF5F56]" />
              <div className="w-3 h-3 rounded-full bg-[#FFBD2E]" />
              <div className="w-3 h-3 rounded-full bg-[#27C93F]" />
              <span className="text-slate-400 ml-2 font-medium">Alur Eksekusi Berkas Otomatis</span>
            </div>

            <div className="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-[11px]">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
              <span>100% Otomatis</span>
            </div>
          </div>

          {/* Visual 3-Stage Flow: 2 Input Files -> Connected Engine -> 2 Output Documents */}
          <div className="grid grid-cols-1 md:grid-cols-11 gap-4 items-center py-2">
            
            {/* STAGE 1: 2 Input Files (Left - 4 cols) */}
            <div className="md:col-span-4 space-y-3">
              <div className="text-[10px] font-mono uppercase tracking-wider text-slate-400 px-1 flex items-center justify-between">
                <span>Input Berkas</span>
                <span className="text-indigo-400 font-medium">2 File</span>
              </div>

              {/* Input 1: Modul Praktikum */}
              <div className="p-3.5 rounded-2xl bg-[#121526]/80 border border-indigo-500/20 hover:border-indigo-500/40 transition-all duration-300 flex items-center gap-3.5 shadow-lg group/item">
                <div className="w-10 h-10 rounded-xl bg-indigo-500/15 border border-indigo-500/30 text-indigo-400 flex items-center justify-center shrink-0 group-hover/item:scale-105 transition-transform">
                  <BookOpen className="w-5 h-5 text-indigo-300" />
                </div>
                <div className="min-w-0 flex-1">
                  <div className="text-xs sm:text-sm font-bold text-white tracking-tight">Modul Praktikum</div>
                  <div className="text-[10px] font-mono text-indigo-300/80">.pdf / .txt</div>
                </div>
                <span className="text-[9px] font-mono px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                  Wajib
                </span>
              </div>

              {/* Input 2: Template Word / PDF */}
              <div className="p-3.5 rounded-2xl bg-[#121526]/80 border border-indigo-500/20 hover:border-indigo-500/40 transition-all duration-300 flex items-center gap-3.5 shadow-lg group/item">
                <div className="w-10 h-10 rounded-xl bg-purple-500/15 border border-purple-500/30 text-purple-400 flex items-center justify-center shrink-0 group-hover/item:scale-105 transition-transform">
                  <LayoutTemplate className="w-5 h-5 text-purple-300" />
                </div>
                <div className="min-w-0 flex-1">
                  <div className="text-xs sm:text-sm font-bold text-white tracking-tight">Template Word / PDF</div>
                  <div className="text-[10px] font-mono text-purple-300/80">.docx / .pdf</div>
                </div>
                <span className="text-[9px] font-mono px-2 py-0.5 rounded-full bg-slate-500/20 text-slate-300 border border-slate-500/30">
                  Opsional
                </span>
              </div>
            </div>

            {/* STAGE 2: Center Connecting Engine (Center - 3 cols) */}
            <div className="md:col-span-3 flex flex-col items-center justify-center py-4 md:py-0 relative">
              {/* Connector lines on Desktop */}
              <div className="hidden md:block absolute inset-0 pointer-events-none">
                <svg className="w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none">
                  {/* Left-to-center line */}
                  <line x1="0" y1="50" x2="35" y2="50" stroke="#6366F1" strokeWidth="2" strokeDasharray="3 3" opacity="0.6" className="animate-pulse" />
                  {/* Center-to-right line */}
                  <line x1="65" y1="50" x2="100" y2="50" stroke="#6366F1" strokeWidth="2" strokeDasharray="3 3" opacity="0.6" className="animate-pulse" />
                </svg>
              </div>

              {/* Center Logo Emblem */}
              <div className="relative group/logo">
                <div className="w-16 h-16 sm:w-18 sm:h-18 rounded-2xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-purple-500 p-0.5 shadow-[0_0_40px_rgba(99,102,241,0.5)] transition-transform duration-300 group-hover/logo:scale-105">
                  <div className="w-full h-full rounded-[14px] bg-[#0A0D18] flex flex-col items-center justify-center relative overflow-hidden">
                    <Sparkles className="w-7 h-7 text-indigo-400 animate-pulse" />
                    <span className="text-[9px] font-mono font-bold tracking-wider text-white mt-1">NgeLaprak</span>
                  </div>
                </div>
                {/* Floating autonomous badge */}
                <span className="absolute -bottom-2.5 left-1/2 -translate-x-1/2 text-[9px] font-mono px-2 py-0.5 rounded-full bg-indigo-500 text-white font-semibold shadow-md whitespace-nowrap">
                  ~15 Detik
                </span>
              </div>
            </div>

            {/* STAGE 3: 2 Output Documents (Right - 4 cols) */}
            <div className="md:col-span-4 space-y-3">
              <div className="text-[10px] font-mono uppercase tracking-wider text-slate-400 px-1 flex items-center justify-between">
                <span>Hasil Jadi</span>
                <span className="text-emerald-400 font-medium">Siap Kumpul</span>
              </div>

              {/* Output 1: Laporan Praktikum (.docx) */}
              <div className="p-3.5 rounded-2xl bg-[#121526]/80 border border-blue-500/25 hover:border-blue-500/50 transition-all duration-300 flex items-center justify-between gap-3 shadow-lg group/item">
                <div className="flex items-center gap-3.5 min-w-0">
                  <div className="w-10 h-10 rounded-xl bg-blue-500/15 border border-blue-500/30 text-blue-400 flex items-center justify-center shrink-0 group-hover/item:scale-105 transition-transform">
                    {/* Microsoft Word Style Badge */}
                    <span className="font-extrabold text-sm font-mono text-blue-400">W</span>
                  </div>
                  <div className="min-w-0">
                    <div className="text-xs sm:text-sm font-bold text-white tracking-tight truncate">
                      Laporan Praktikum
                    </div>
                    <div className="text-[10px] font-mono text-blue-300/80">.docx • Editable</div>
                  </div>
                </div>
                <a
                  href="/samples/strukdat/LAPRAK_SAMPLE_STRUKDAT_MODUL3.docx"
                  download
                  className="p-2 rounded-xl bg-white/10 hover:bg-white/20 text-white shrink-0 transition-colors cursor-pointer"
                  title="Unduh DOCX"
                >
                  <Download className="w-4 h-4" />
                </a>
              </div>

              {/* Output 2: Laporan Praktikum (.pdf) */}
              <div className="p-3.5 rounded-2xl bg-[#121526]/80 border border-rose-500/25 hover:border-rose-500/50 transition-all duration-300 flex items-center justify-between gap-3 shadow-lg group/item">
                <div className="flex items-center gap-3.5 min-w-0">
                  <div className="w-10 h-10 rounded-xl bg-rose-500/15 border border-rose-500/30 text-rose-400 flex items-center justify-center shrink-0 group-hover/item:scale-105 transition-transform">
                    {/* PDF Style Badge */}
                    <span className="font-extrabold text-xs font-mono text-rose-400">PDF</span>
                  </div>
                  <div className="min-w-0">
                    <div className="text-xs sm:text-sm font-bold text-white tracking-tight truncate">
                      Laporan Praktikum
                    </div>
                    <div className="text-[10px] font-mono text-rose-300/80">.pdf • Format Resmi</div>
                  </div>
                </div>
                <a
                  href="/samples/strukdat/LAPRAK_SAMPLE_STRUKDAT_MODUL3.pdf"
                  download
                  className="p-2 rounded-xl bg-white/10 hover:bg-white/20 text-white shrink-0 transition-colors cursor-pointer"
                  title="Unduh PDF"
                >
                  <Download className="w-4 h-4" />
                </a>
              </div>
            </div>

          </div>

          {/* Quick Footer Action inside Window */}
          <div className="pt-4 mt-3 border-t border-white/5 flex items-center justify-center">
            <a
              href="#samples"
              className="flex items-center gap-1.5 text-xs text-indigo-300 hover:text-white transition-colors font-mono cursor-pointer"
            >
              <Eye className="w-3.5 h-3.5" />
              <span>Inspeksi Dokumen Hasil Lengkap</span>
            </a>
          </div>
        </div>
      </div>
    </section>
  )
}
