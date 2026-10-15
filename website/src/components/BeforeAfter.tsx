import React from 'react'
import { XCircle, CheckCircle2, Sparkles, X, Check } from 'lucide-react'

/* ─────────────────────────────────────────────────────
   SVG Illustration 1 — Manual Chaos (Format Manual)
   Crooked document, broken margin, error badges, 03:00 AM clock
   ───────────────────────────────────────────────────── */
const ManualChaosIllustration: React.FC = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 400 220"
    role="img"
    aria-labelledby="manual-title manual-desc"
    className="w-full h-full"
  >
    <title id="manual-title">Kekacauan Format Manual</title>
    <desc id="manual-desc">Ilustrasi dokumen praktikum manual yang miring, margin rusak, dan begadang larut malam.</desc>
    <defs>
      <filter id="redAura" x="-25%" y="-25%" width="150%" height="150%">
        <feGaussianBlur stdDeviation="8" result="blur" />
        <feMerge>
          <feMergeNode in="blur" />
          <feMergeNode in="SourceGraphic" />
        </feMerge>
      </filter>
      <radialGradient id="roseGlow" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stopColor="#f43f5e" stopOpacity="0.3" />
        <stop offset="100%" stopColor="#f43f5e" stopOpacity="0" />
      </radialGradient>
      <linearGradient id="brokenPaper" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stopColor="#1a0a0e" />
        <stop offset="100%" stopColor="#0f0508" />
      </linearGradient>
    </defs>

    <style>{`
      @keyframes floatBroken { 0%,100% { transform: translateY(0) rotate(-3.5deg); } 50% { transform: translateY(-5px) rotate(-2deg); } }
      @keyframes warnPulse { 0%,100% { transform: scale(1); opacity: 0.8; } 50% { transform: scale(1.1); opacity: 1; } }
      @keyframes jitter { 0%,100% { opacity: 0.3; } 50% { opacity: 0.7; } }
      .broken-doc { animation: floatBroken 4s ease-in-out infinite; transform-origin: 190px 110px; }
      .warn-badge { animation: warnPulse 2.2s ease-in-out infinite; transform-origin: 290px 45px; }
      .clock-pulse { animation: warnPulse 3s ease-in-out infinite; transform-origin: 90px 50px; }
    `}</style>

    {/* Background ambient red glow */}
    <circle cx="200" cy="110" r="95" fill="url(#roseGlow)" />

    {/* Background Grid Pattern */}
    <g opacity="0.06">
      {Array.from({ length: 9 }).map((_, r) =>
        Array.from({ length: 15 }).map((_, c) => (
          <circle key={`mg-${r}-${c}`} cx={30 + c * 24} cy={22 + r * 24} r="1" fill="#f43f5e" />
        ))
      )}
    </g>

    {/* ── Night Begadang Clock Widget (Left) ── */}
    <g className="clock-pulse">
      <circle cx="85" cy="55" r="24" fill="#18080c" stroke="#f43f5e" strokeWidth="2" strokeDasharray="3 3" />
      {/* Clock hands showing 03:15 AM */}
      <circle cx="85" cy="55" r="2.5" fill="#f43f5e" />
      <line x1="85" y1="55" x2="85" y2="40" stroke="#f43f5e" strokeWidth="2" strokeLinecap="round" />
      <line x1="85" y1="55" x2="98" y2="55" stroke="#f43f5e" strokeWidth="2" strokeLinecap="round" />
      <text x="85" y="92" textAnchor="middle" fontFamily="monospace" fontSize="9" fontWeight="bold" fill="#fda4af">
        03:30 AM
      </text>
    </g>

    {/* ── Main Crooked / Broken Document ── */}
    <g className="broken-doc" filter="url(#redAura)">
      {/* Crooked Sheet */}
      <rect
        x="130"
        y="26"
        width="145"
        height="170"
        rx="10"
        fill="url(#brokenPaper)"
        stroke="#f43f5e"
        strokeWidth="2"
        strokeDasharray="6 3"
      />

      {/* Misaligned Header Bar */}
      <path d="M135,32 L265,37 L263,55 L135,50 Z" fill="#4c0519" opacity="0.7" />
      <line x1="145" y1="44" x2="235" y2="48" stroke="#f43f5e" strokeWidth="3" strokeLinecap="round" />

      {/* Crooked text lines (misaligned margins) */}
      <line x1="142" y1="66" x2="255" y2="69" stroke="#fda4af" strokeWidth="2" strokeLinecap="round" opacity="0.6" />
      <line x1="152" y1="76" x2="248" y2="78" stroke="#fda4af" strokeWidth="2" strokeLinecap="round" opacity="0.4" />
      <line x1="140" y1="86" x2="260" y2="88" stroke="#fda4af" strokeWidth="2" strokeLinecap="round" opacity="0.5" />

      {/* Crooked Screenshot Box with jagged crack */}
      <rect
        x="142"
        y="98"
        width="120"
        height="50"
        rx="6"
        fill="#26040c"
        stroke="#e11d48"
        strokeWidth="1.5"
      />
      {/* Red error jagged crack in screenshot */}
      <path
        d="M148,124 L175,116 L195,132 L225,112 L254,128"
        fill="none"
        stroke="#f43f5e"
        strokeWidth="2"
        strokeLinecap="round"
      />
      <text x="202" y="141" textAnchor="middle" fontFamily="monospace" fontSize="7.5" fill="#fca5a5">
        [Screenshot Rusak / Blur]
      </text>

      {/* More jagged paragraph lines */}
      <line x1="150" y1="160" x2="258" y2="162" stroke="#fda4af" strokeWidth="2" strokeLinecap="round" opacity="0.4" />
      <line x1="144" y1="170" x2="230" y2="171" stroke="#fda4af" strokeWidth="2" strokeLinecap="round" opacity="0.3" />

      {/* Red margin error guide lines */}
      <line x1="130" y1="26" x2="130" y2="196" stroke="#ef4444" strokeWidth="1" strokeDasharray="2 2" opacity="0.7" />
    </g>

    {/* ── Floating Warning Alert Badge (Right) ── */}
    <g className="warn-badge">
      <circle cx="295" cy="50" r="18" fill="#4c0519" stroke="#f43f5e" strokeWidth="2" />
      <text x="295" y="56" textAnchor="middle" fontFamily="Arial, sans-serif" fontSize="16" fontWeight="bold" fill="#ffffff">
        !
      </text>
      <rect x="268" y="76" width="54" height="15" rx="7.5" fill="#7f1d1d" opacity="0.7" />
      <text x="295" y="87" textAnchor="middle" fontFamily="monospace" fontSize="7.5" fontWeight="bold" fill="#fca5a5">
        REVISI
      </text>
    </g>

    {/* Floating stress particles */}
    <circle cx="115" cy="155" r="2.5" fill="#f43f5e" opacity="0.6" />
    <circle cx="310" cy="130" r="2" fill="#fda4af" opacity="0.5" />
    <circle cx="280" cy="175" r="3" fill="#f43f5e" opacity="0.4" />
  </svg>
)

/* ─────────────────────────────────────────────────────
   SVG Illustration 2 — Automated Perfection (Dengan NgeLaprak)
   Perfect 4-4-3-3 margins, embedded IDE screenshot, verified checkmark, 30s fast streak
   ───────────────────────────────────────────────────── */
const AutomatedPerfectionIllustration: React.FC = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 400 220"
    role="img"
    aria-labelledby="auto-title auto-desc"
    className="w-full h-full"
  >
    <title id="auto-title">Presisi Otomatis NgeLaprak</title>
    <desc id="auto-desc">Ilustrasi laporan praktikum yang terstruktur presisi, margin baku 4-4-3-3, dan selesai cepat.</desc>
    <defs>
      <filter id="emeraldAura" x="-25%" y="-25%" width="150%" height="150%">
        <feGaussianBlur stdDeviation="8" result="blur" />
        <feMerge>
          <feMergeNode in="blur" />
          <feMergeNode in="SourceGraphic" />
        </feMerge>
      </filter>
      <radialGradient id="greenGlow" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stopColor="#10b981" stopOpacity="0.35" />
        <stop offset="100%" stopColor="#10b981" stopOpacity="0" />
      </radialGradient>
      <linearGradient id="perfectPaper" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor="#0b1b15" />
        <stop offset="100%" stopColor="#05100c" />
      </linearGradient>
    </defs>

    <style>{`
      @keyframes smoothLevitate { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-6px); } }
      @keyframes checkPulse { 0%,100% { transform: scale(1); } 50% { transform: scale(1.12); } }
      @keyframes speedFlash { 0%,100% { opacity: 0.4; } 50% { opacity: 0.9; } }
      .perfect-doc { animation: smoothLevitate 4s ease-in-out infinite; }
      .check-badge { animation: checkPulse 2.4s ease-in-out infinite; transform-origin: 295px 50px; }
      .speed-streak { animation: speedFlash 2s ease-in-out infinite; }
    `}</style>

    {/* Background ambient emerald glow */}
    <circle cx="200" cy="110" r="95" fill="url(#greenGlow)" />

    {/* Background Grid Pattern */}
    <g opacity="0.06">
      {Array.from({ length: 9 }).map((_, r) =>
        Array.from({ length: 15 }).map((_, c) => (
          <circle key={`ag-${r}-${c}`} cx={30 + c * 24} cy={22 + r * 24} r="1" fill="#10b981" />
        ))
      )}
    </g>

    {/* ── Speed 30s Badge (Left) ── */}
    <g className="speed-streak">
      <rect x="62" y="42" width="48" height="48" rx="14" fill="#064e3b" stroke="#10b981" strokeWidth="2" opacity="0.9" />
      <text x="86" y="66" textAnchor="middle" fontFamily="Arial, sans-serif" fontSize="16" fontWeight="900" fill="#34d399">
        ⚡
      </text>
      <text x="86" y="81" textAnchor="middle" fontFamily="monospace" fontSize="8.5" fontWeight="bold" fill="#a7f3d0">
        ~30s
      </text>
    </g>

    {/* ── Main Perfect Document Sheet ── */}
    <g className="perfect-doc" filter="url(#emeraldAura)">
      {/* Pristine Document Base */}
      <rect
        x="130"
        y="24"
        width="145"
        height="174"
        rx="12"
        fill="url(#perfectPaper)"
        stroke="#10b981"
        strokeWidth="2"
      />

      {/* 4-4-3-3 Margin Guide Corner Marks */}
      <path d="M136,36 L136,30 L142,30" fill="none" stroke="#34d399" strokeWidth="1.5" opacity="0.8" />
      <path d="M269,36 L269,30 L263,30" fill="none" stroke="#34d399" strokeWidth="1.5" opacity="0.8" />
      <path d="M136,186 L136,192 L142,192" fill="none" stroke="#34d399" strokeWidth="1.5" opacity="0.8" />
      <path d="M269,186 L269,192 L263,192" fill="none" stroke="#34d399" strokeWidth="1.5" opacity="0.8" />

      {/* Clean Header Bar */}
      <rect x="130" y="24" width="145" height="30" rx="12" fill="#047857" opacity="0.75" />
      <rect x="130" y="44" width="145" height="10" fill="#047857" opacity="0.75" />
      <rect x="152" y="36" width="100" height="6" rx="3" fill="#a7f3d0" />

      {/* Regular paragraph skeleton lines */}
      <rect x="145" y="64" width="115" height="3.5" rx="1.75" fill="#10b981" opacity="0.6" />
      <rect x="145" y="73" width="95" height="3.5" rx="1.75" fill="#10b981" opacity="0.4" />
      <rect x="145" y="82" width="105" height="3.5" rx="1.75" fill="#10b981" opacity="0.3" />

      {/* Embedded Pixel-Perfect IDE Frame */}
      <rect
        x="142"
        y="94"
        width="120"
        height="56"
        rx="6"
        fill="#022c22"
        stroke="#059669"
        strokeWidth="1.5"
      />
      {/* IDE mini titlebar dots */}
      <circle cx="150" cy="102" r="2" fill="#ef4444" />
      <circle cx="156" cy="102" r="2" fill="#f59e0b" />
      <circle cx="162" cy="102" r="2" fill="#10b981" />
      <line x1="142" y1="108" x2="262" y2="108" stroke="#065f46" strokeWidth="1" />
      {/* Syntax code lines */}
      <rect x="150" y="115" width="45" height="3" rx="1.5" fill="#34d399" opacity="0.8" />
      <rect x="160" y="122" width="60" height="3" rx="1.5" fill="#6ee7b7" opacity="0.6" />
      <rect x="150" y="129" width="35" height="3" rx="1.5" fill="#34d399" opacity="0.7" />
      <rect x="150" y="138" width="80" height="6" rx="2" fill="#047857" opacity="0.7" />

      {/* More paragraph skeleton lines */}
      <rect x="145" y="159" width="115" height="3.5" rx="1.75" fill="#10b981" opacity="0.5" />
      <rect x="145" y="168" width="80" height="3.5" rx="1.75" fill="#10b981" opacity="0.35" />
    </g>

    {/* ── Verified Checkmark Badge (Right) ── */}
    <g className="check-badge">
      <circle cx="295" cy="50" r="18" fill="#064e3b" stroke="#34d399" strokeWidth="2.5" />
      <path
        d="M287,50 L293,56 L305,42"
        stroke="#ffffff"
        strokeWidth="3"
        fill="none"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <rect x="268" y="76" width="54" height="15" rx="7.5" fill="#065f46" opacity="0.8" />
      <text x="295" y="87" textAnchor="middle" fontFamily="monospace" fontSize="7.5" fontWeight="bold" fill="#6ee7b7">
        ACC LAB
      </text>
    </g>

    {/* Sparkle celebration particles */}
    <circle cx="115" cy="155" r="2.5" fill="#34d399" opacity="0.7" />
    <circle cx="310" cy="130" r="2" fill="#6ee7b7" opacity="0.6" />
    <circle cx="280" cy="175" r="3" fill="#10b981" opacity="0.5" />
  </svg>
)

/* ═══════════════════════════════════════════════════════
   BeforeAfter Component with Expressive SVG Illustrations
   ═══════════════════════════════════════════════════════ */
export const BeforeAfter: React.FC = () => {
  const points = [
    {
      before: 'Screenshot buram, terpotong, atau foto kamera HP',
      after: 'Screenshot IDE autentik beresolusi tinggi tanpa watermark'
    },
    {
      before: 'Margin dan nomor halaman bergeser saat export ke PDF',
      after: 'Margin 4-4-3-3 baku, penomoran Romawi & Arab otomatis'
    },
    {
      before: 'Struktur kode berantakan tanpa package & config',
      after: 'Struktur proyek resmi Maven / CMake siap compile'
    },
    {
      before: 'Begadang 3–5 jam merapikan format laporan semalaman',
      after: 'Selesai otomatis dalam ~30 detik langsung siap kumpul'
    }
  ]

  return (
    <section id="compare" className="py-20 md:py-28 relative overflow-hidden bg-[#090A0F]">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 relative z-10">
        {/* Section Header */}
        <div className="text-center max-w-2xl mx-auto mb-14">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-mono uppercase tracking-wider mb-3">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Komparasi</span>
          </div>
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-white tracking-[-0.035em] mb-3 font-sans [text-wrap:balance]">
            Sebelum vs Sesudah <span className="text-indigo-400">NgeLaprak</span>
          </h2>
          <p className="text-slate-400 text-sm sm:text-base leading-relaxed [text-wrap:pretty]">
            Perbandingan pengerjaan laporan praktikum secara manual dan otomatis.
          </p>
        </div>

        {/* 2 Big Side-by-side Minimalist Cards with Expressive SVG Illustrations */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-stretch">
          {/* BEFORE CARD */}
          <div className="rounded-3xl bg-[#0D0F18] border border-rose-500/20 p-6 sm:p-8 relative overflow-hidden shadow-xl shadow-black/40 flex flex-col justify-between group">
            <div>
              <div className="flex items-center gap-3 mb-6 pb-4 border-b border-white/5">
                <div className="w-10 h-10 rounded-2xl bg-rose-500/10 border border-rose-500/20 flex items-center justify-center text-rose-400">
                  <XCircle className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-bold text-white text-lg tracking-tight">Format Manual</h3>
                  <span className="text-xs text-rose-400/80 font-mono">3–5 Jam Begadang</span>
                </div>
              </div>

              <div className="space-y-3 mb-6">
                {points.map((p, idx) => (
                  <div key={idx} className="p-3.5 rounded-xl bg-black/30 border border-rose-500/15 text-xs sm:text-sm text-slate-300 flex items-start gap-3">
                    <X className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
                    <span className="leading-relaxed">{p.before}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* SVG Illustration: Manual Chaos */}
            <div className="mt-auto pt-4">
              <div className="rounded-2xl overflow-hidden border border-rose-500/20 relative h-56 sm:h-60 bg-[#08090E] group-hover:border-rose-500/40 transition-colors shadow-inner flex items-center justify-center">
                <ManualChaosIllustration />
              </div>
            </div>
          </div>

          {/* AFTER CARD */}
          <div className="rounded-3xl bg-[#0D0F18] border border-indigo-500/40 p-6 sm:p-8 relative overflow-hidden shadow-2xl shadow-indigo-950/20 flex flex-col justify-between group">
            <div>
              <div className="flex items-center gap-3 mb-6 pb-4 border-b border-white/5">
                <div className="w-10 h-10 rounded-2xl bg-indigo-500/15 border border-indigo-500/30 flex items-center justify-center text-indigo-400 shadow-md">
                  <CheckCircle2 className="w-5 h-5 text-indigo-400" />
                </div>
                <div>
                  <h3 className="font-bold text-white text-lg tracking-tight">Dengan NgeLaprak</h3>
                  <span className="text-xs text-emerald-400 font-mono">~30 Detik Otomatis</span>
                </div>
              </div>

              <div className="space-y-3 mb-6">
                {points.map((p, idx) => (
                  <div key={idx} className="p-3.5 rounded-xl bg-black/30 border border-indigo-500/30 text-xs sm:text-sm text-slate-200 flex items-start gap-3">
                    <Check className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                    <span className="leading-relaxed">{p.after}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* SVG Illustration: Automated Perfection */}
            <div className="mt-auto pt-4">
              <div className="rounded-2xl overflow-hidden border border-emerald-500/20 relative h-56 sm:h-60 bg-[#08090E] group-hover:border-emerald-500/40 transition-colors shadow-inner flex items-center justify-center">
                <AutomatedPerfectionIllustration />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
