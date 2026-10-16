import React, { useState } from 'react'
import { Terminal, Copy, Check, Sparkles, ExternalLink, Coffee, Heart } from 'lucide-react'
import { NgeLaprakLogo } from './NgeLaprakLogo'

/* ─────────────────────────────────────────────────────
   Animated Steaming Coffee Cup SVG Illustration
   Custom warm golden aesthetics for Saweria support
   ───────────────────────────────────────────────────── */
const CoffeeCupIllustration: React.FC = () => (
  <svg
    viewBox="0 0 120 110"
    className="w-20 h-20 mx-auto"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    role="img"
    aria-label="Cangkir Kopi Hangat"
  >
    <defs>
      <radialGradient id="coffeeGlow" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stopColor="#f59e0b" stopOpacity="0.45" />
        <stop offset="100%" stopColor="#f59e0b" stopOpacity="0" />
      </radialGradient>
    </defs>
    <style>{`
      @keyframes steamFloat1 {
        0% { transform: translateY(0); opacity: 0; }
        50% { opacity: 0.85; }
        100% { transform: translateY(-12px); opacity: 0; }
      }
      @keyframes steamFloat2 {
        0% { transform: translateY(0); opacity: 0; }
        50% { opacity: 0.85; }
        100% { transform: translateY(-16px); opacity: 0; }
      }
      .steam-1 { animation: steamFloat1 2.4s ease-in-out infinite; }
      .steam-2 { animation: steamFloat2 2.8s ease-in-out infinite 0.6s; }
      .steam-3 { animation: steamFloat1 2.2s ease-in-out infinite 1.2s; }
    `}</style>
    {/* Ambient Glow */}
    <circle cx="60" cy="60" r="42" fill="url(#coffeeGlow)" />
    {/* Steam Waves */}
    <path className="steam-1" d="M46 32 C44 24, 50 20, 48 12" stroke="#fbbf24" strokeWidth="2.5" strokeLinecap="round" opacity="0.8" />
    <path className="steam-2" d="M60 30 C58 20, 64 16, 62 8" stroke="#f59e0b" strokeWidth="2.5" strokeLinecap="round" opacity="0.9" />
    <path className="steam-3" d="M74 32 C72 24, 78 20, 76 12" stroke="#fbbf24" strokeWidth="2.5" strokeLinecap="round" opacity="0.8" />
    {/* Saucer Plate */}
    <ellipse cx="60" cy="88" rx="34" ry="6" fill="#2d1704" stroke="#fbbf24" strokeWidth="2" />
    {/* Cup Base */}
    <path d="M35 44 L41 78 C42 82, 78 82, 79 78 L85 44 Z" fill="#1c1106" stroke="#f59e0b" strokeWidth="2.5" strokeLinejoin="round" />
    {/* Cup Stripe */}
    <path d="M38 56 C49 60, 71 60, 82 56" stroke="#d97706" strokeWidth="2" opacity="0.7" />
    {/* Cup Handle */}
    <path d="M84 50 C94 50, 94 68, 82 70" fill="none" stroke="#f59e0b" strokeWidth="2.5" strokeLinecap="round" />
    {/* Heart on Cup */}
    <path d="M60 69 C60 69, 54 64.5, 54 61 C54 58.8, 55.8 57, 58 57 C59.2 57, 60 57.8, 60 57.8 C60 57.8, 60.8 57, 62 57 C64.2 57, 66 58.8, 66 61 C66 64.5, 60 69, 60 69 Z" fill="#f59e0b" />
  </svg>
)

export const InstallGuide: React.FC = () => {
  const [copied, setCopied] = useState(false)
  const cmd = 'npx skills add SatriaBaktiWijaya/NgeLaprak'

  const handleCopy = () => {
    navigator.clipboard.writeText(cmd)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const agents = ['Antigravity', 'Cursor', 'Claude Code', 'VS Code', 'GitHub Copilot']

  return (
    <section id="install" className="py-20 md:py-28 relative overflow-hidden bg-[#090A0F]">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 relative z-10">
        {/* Side-by-Side Dual Card Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
          
          {/* LEFT: Main Install CTA Card (Col 7) */}
          <div className="lg:col-span-7 rounded-3xl bg-gradient-to-b from-[#111424] via-[#0D0F18] to-[#0A0B12] border border-indigo-500/30 p-5 sm:p-7 md:p-9 text-left relative overflow-hidden shadow-2xl shadow-indigo-950/30 flex flex-col justify-between">
            {/* Ambient Indigo Glow */}
            <div
              className="absolute top-0 right-0 w-80 h-80 rounded-full pointer-events-none"
              style={{
                background: 'radial-gradient(circle at top right, rgba(99, 102, 241, 0.15) 0%, transparent 70%)'
              }}
            />

            <div className="relative z-10">
              <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-mono uppercase tracking-wider mb-4">
                <NgeLaprakLogo size={14} className="rounded-sm" />
                <span>Instalasi Cepat</span>
              </div>

              <h2 className="text-2xl sm:text-3xl md:text-4xl font-extrabold text-white tracking-[-0.03em] mb-3 font-sans [text-wrap:balance]">
                Siap Selesaikan Laprak <span className="text-indigo-400">Tanpa Begadang?</span>
              </h2>

              <p className="text-slate-400 text-xs sm:text-sm leading-relaxed mb-6 [text-wrap:pretty]">
                Pasang skill NgeLaprak di terminal agen coding favorit kamu dan langsung mulai pengerjaan laporan praktikum hari ini.
              </p>
            </div>

            <div className="relative z-10 mt-auto">
              {/* Terminal Command Bar */}
              <div className="inline-flex items-center gap-2 p-1.5 sm:p-2 rounded-2xl bg-[#07080E] border border-white/10 w-full justify-between shadow-2xl mb-5">
                <div className="flex items-center gap-2 font-mono text-xs sm:text-sm text-slate-200 px-2 sm:px-3 truncate">
                  <span className="text-indigo-400 select-none font-bold">$</span>
                  <span className="select-all truncate">{cmd}</span>
                </div>
                <button
                  onClick={handleCopy}
                  className={`flex items-center gap-1.5 px-3.5 sm:px-4 py-2 sm:py-2.5 rounded-xl text-xs font-bold shrink-0 transition-all cursor-pointer ${
                    copied
                      ? 'bg-emerald-500 text-white shadow-md shadow-emerald-500/30'
                      : 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-md shadow-indigo-600/30 active:scale-[0.98]'
                  }`}
                >
                  {copied ? <Check className="w-3.5 h-3.5 text-white" /> : <Copy className="w-3.5 h-3.5" />}
                  <span>{copied ? 'Tersalin!' : 'Salin'}</span>
                </button>
              </div>

              {/* Supported Agents Pill Row */}
              <div className="flex flex-wrap items-center gap-1.5 text-xs text-slate-500 font-mono">
                <span className="text-slate-400 mr-1">Kompatibel:</span>
                {agents.map((agent, idx) => (
                  <span key={idx} className="px-2 py-0.5 rounded-lg bg-white/5 border border-white/5 text-slate-300 text-[11px]">
                    {agent}
                  </span>
                ))}
              </div>
            </div>
          </div>

          {/* RIGHT: Decorated Saweria / Buy Me a Coffee Card (Col 5) */}
          <div className="lg:col-span-5 rounded-3xl bg-gradient-to-b from-[#191307] via-[#100D06] to-[#0A0804] border border-amber-500/35 hover:border-amber-400/60 p-5 sm:p-7 md:p-9 text-center relative overflow-hidden shadow-2xl shadow-amber-950/30 flex flex-col justify-between transition-all duration-300 group">
            {/* Ambient Amber Glow */}
            <div
              className="absolute top-0 right-0 w-64 h-64 rounded-full pointer-events-none"
              style={{
                background: 'radial-gradient(circle at top right, rgba(245, 158, 11, 0.15) 0%, transparent 70%)'
              }}
            />
            <div
              className="absolute bottom-0 left-0 w-48 h-48 rounded-full pointer-events-none"
              style={{
                background: 'radial-gradient(circle at bottom left, rgba(249, 115, 22, 0.15) 0%, transparent 70%)'
              }}
            />

            <div className="relative z-10">
              <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-500/15 border border-amber-500/30 text-amber-300 text-xs font-mono uppercase tracking-wider mb-4">
                <Coffee className="w-3.5 h-3.5 text-amber-400" />
                <span>Traktir Kopi</span>
              </div>

              <h3 className="text-2xl sm:text-3xl font-extrabold text-white tracking-[-0.03em] mb-2 font-sans">
                Dukung <span className="text-amber-400">NgeLaprak</span>
              </h3>

              <p className="text-slate-400 text-xs sm:text-sm leading-relaxed mb-4 [text-wrap:pretty]">
                Dukungan secangkir kopi dari kamu membantu menjaga generator ini tetap aktif, gratis, dan terus diperbarui untuk seluruh mahasiswa.
              </p>

              {/* Animated Steaming Cup */}
              <div className="py-2">
                <CoffeeCupIllustration />
              </div>
            </div>

            <div className="relative z-10 mt-auto pt-4">
              <a
                href="https://saweria.co/satriabaktiwijaya"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center justify-center gap-2.5 w-full py-3.5 px-6 rounded-2xl bg-gradient-to-r from-amber-500 via-amber-400 to-orange-500 hover:from-amber-400 hover:to-orange-400 text-slate-950 font-extrabold text-xs sm:text-sm shadow-xl shadow-amber-500/20 hover:shadow-amber-500/35 active:scale-[0.98] transition-all duration-200 cursor-pointer group"
              >
                <Coffee className="w-4 h-4 text-slate-950 group-hover:rotate-12 transition-transform duration-200" />
                <span>Traktir Kopi di Saweria</span>
                <ExternalLink className="w-3.5 h-3.5 text-slate-950/80 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
              </a>

              <div className="text-[11px] font-mono text-amber-300/60 mt-3 text-center">
                Mendukung QRIS • GoPay • OVO • DANA • ShopeePay
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>
  )
}

