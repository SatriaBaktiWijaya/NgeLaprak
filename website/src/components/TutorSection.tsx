import React, { useState } from 'react'
import { Sparkles, Terminal, Copy, Check, Download } from 'lucide-react'

/* ─────────────────────────────────────────────────────
   SVG Illustration 1 — Folder Workspace (Minimalist & Expressive)
   Clean 3D folder with sleek floating colored document cards
   ───────────────────────────────────────────────────── */
const FolderIllustration: React.FC = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 400 240"
    role="img"
    aria-labelledby="folder-title folder-desc"
    className="w-full h-full"
  >
    <title id="folder-title">Folder Konteks Praktikum</title>
    <desc id="folder-desc">Ilustrasi folder workspace dengan lembaran dokumen bahan praktikum yang melayang masuk.</desc>
    <defs>
      <filter id="folderGlow" x="-30%" y="-30%" width="160%" height="160%">
        <feGaussianBlur stdDeviation="8" result="blur" />
        <feMerge>
          <feMergeNode in="blur" />
          <feMergeNode in="SourceGraphic" />
        </feMerge>
      </filter>
      <filter id="docShadow" x="-20%" y="-20%" width="140%" height="140%">
        <feDropShadow dx="0" dy="4" stdDeviation="5" floodColor="#000" floodOpacity="0.5" />
      </filter>
      <linearGradient id="folderFront" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stopColor="#4338ca" />
        <stop offset="100%" stopColor="#312e81" />
      </linearGradient>
      <linearGradient id="cardPink" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor="#f43f5e" />
        <stop offset="100%" stopColor="#be123c" />
      </linearGradient>
      <linearGradient id="cardBlue" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor="#3b82f6" />
        <stop offset="100%" stopColor="#1d4ed8" />
      </linearGradient>
      <linearGradient id="cardEmerald" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor="#10b981" />
        <stop offset="100%" stopColor="#047857" />
      </linearGradient>
      <radialGradient id="folderAura" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stopColor="#6366f1" stopOpacity="0.35" />
        <stop offset="100%" stopColor="#6366f1" stopOpacity="0" />
      </radialGradient>
    </defs>

    <style>{`
      @keyframes floatCard1 { 0%,100% { transform: translate(0, 0) rotate(-4deg); } 50% { transform: translate(-3px, -10px) rotate(-6deg); } }
      @keyframes floatCard2 { 0%,100% { transform: translate(0, 0) rotate(0deg); } 50% { transform: translate(0, -12px) rotate(1deg); } }
      @keyframes floatCard3 { 0%,100% { transform: translate(0, 0) rotate(5deg); } 50% { transform: translate(3px, -9px) rotate(7deg); } }
      @keyframes auraPulse { 0%,100% { opacity: 0.4; transform: scale(0.95); } 50% { opacity: 0.8; transform: scale(1.08); } }
      @keyframes streamDot { 0% { opacity: 0.1; transform: translateY(0); } 50% { opacity: 0.9; } 100% { opacity: 0.1; transform: translateY(12px); } }
      .float-card-1 { animation: floatCard1 3.4s ease-in-out infinite; transform-origin: 120px 80px; }
      .float-card-2 { animation: floatCard2 3.8s ease-in-out infinite 0.3s; transform-origin: 200px 70px; }
      .float-card-3 { animation: floatCard3 3.1s ease-in-out infinite 0.6s; transform-origin: 280px 80px; }
      .aura-bg { animation: auraPulse 4s ease-in-out infinite; transform-origin: 200px 140px; }
      .stream-1 { animation: streamDot 2s ease-in-out infinite; }
      .stream-2 { animation: streamDot 2.3s ease-in-out infinite 0.4s; }
      .stream-3 { animation: streamDot 1.9s ease-in-out infinite 0.8s; }
    `}</style>

    {/* Ambient Glow */}
    <circle className="aura-bg" cx="200" cy="140" r="100" fill="url(#folderAura)" />

    {/* Background Grid Pattern */}
    <g opacity="0.08">
      {Array.from({ length: 9 }).map((_, r) =>
        Array.from({ length: 15 }).map((_, c) => (
          <circle key={`fg-${r}-${c}`} cx={30 + c * 24} cy={24 + r * 24} r="1" fill="#818cf8" />
        ))
      )}
    </g>

    {/* ── Floating Document Cards (No cluttered text, pure sleek geometry) ── */}
    {/* Card 1 — Modul (Rose) */}
    <g className="float-card-1" filter="url(#docShadow)">
      <rect x="85" y="32" width="72" height="92" rx="10" fill="#131422" stroke="#f43f5e" strokeWidth="2" />
      {/* Colored Header bar */}
      <rect x="85" y="32" width="72" height="20" rx="10" fill="url(#cardPink)" />
      <rect x="85" y="44" width="72" height="8" fill="url(#cardPink)" />
      {/* Decorative fold corner */}
      <path d="M145,32 L157,44 L145,44 Z" fill="#fda4af" opacity="0.8" />
      {/* Skeleton lines */}
      <rect x="96" y="62" width="50" height="3.5" rx="1.75" fill="#f43f5e" opacity="0.6" />
      <rect x="96" y="72" width="40" height="3.5" rx="1.75" fill="#f43f5e" opacity="0.4" />
      <rect x="96" y="82" width="46" height="3.5" rx="1.75" fill="#f43f5e" opacity="0.3" />
      <rect x="96" y="94" width="32" height="12" rx="4" fill="#f43f5e" opacity="0.2" />
    </g>

    {/* Card 2 — Template (Blue) */}
    <g className="float-card-2" filter="url(#docShadow)">
      <rect x="164" y="20" width="72" height="92" rx="10" fill="#111827" stroke="#3b82f6" strokeWidth="2" />
      {/* Colored Header bar */}
      <rect x="164" y="20" width="72" height="20" rx="10" fill="url(#cardBlue)" />
      <rect x="164" y="32" width="72" height="8" fill="url(#cardBlue)" />
      {/* Decorative fold corner */}
      <path d="M224,20 L236,32 L224,32 Z" fill="#93c5fd" opacity="0.8" />
      {/* Skeleton lines */}
      <rect x="175" y="50" width="50" height="3.5" rx="1.75" fill="#3b82f6" opacity="0.6" />
      <rect x="175" y="60" width="38" height="3.5" rx="1.75" fill="#3b82f6" opacity="0.45" />
      <rect x="175" y="70" width="46" height="3.5" rx="1.75" fill="#3b82f6" opacity="0.35" />
      <rect x="175" y="80" width="42" height="3.5" rx="1.75" fill="#3b82f6" opacity="0.25" />
      <rect x="175" y="92" width="50" height="10" rx="3" fill="#3b82f6" opacity="0.18" />
    </g>

    {/* Card 3 — Source & TP (Emerald) */}
    <g className="float-card-3" filter="url(#docShadow)">
      <rect x="243" y="32" width="72" height="92" rx="10" fill="#061c16" stroke="#10b981" strokeWidth="2" />
      {/* Colored Header bar */}
      <rect x="243" y="32" width="72" height="20" rx="10" fill="url(#cardEmerald)" />
      <rect x="243" y="44" width="72" height="8" fill="url(#cardEmerald)" />
      {/* Decorative fold corner */}
      <path d="M303,32 L315,44 L303,44 Z" fill="#6ee7b7" opacity="0.8" />
      {/* Skeleton lines */}
      <rect x="254" y="62" width="42" height="3.5" rx="1.75" fill="#10b981" opacity="0.6" />
      <rect x="254" y="72" width="50" height="3.5" rx="1.75" fill="#10b981" opacity="0.45" />
      <rect x="254" y="82" width="36" height="3.5" rx="1.75" fill="#10b981" opacity="0.35" />
      <rect x="254" y="94" width="50" height="12" rx="4" fill="#10b981" opacity="0.2" />
    </g>

    {/* Downward stream motion dashes */}
    <g opacity="0.6">
      <line className="stream-1" x1="121" y1="126" x2="121" y2="140" stroke="#f43f5e" strokeWidth="2.5" strokeDasharray="3 3" />
      <line className="stream-2" x1="200" y1="114" x2="200" y2="135" stroke="#3b82f6" strokeWidth="2.5" strokeDasharray="3 3" />
      <line className="stream-3" x1="279" y1="126" x2="279" y2="140" stroke="#10b981" strokeWidth="2.5" strokeDasharray="3 3" />
    </g>

    {/* ── Folder Main Structure ── */}
    <g filter="url(#folderGlow)">
      {/* Folder Back Tab */}
      <path
        d="M90,126 L90,114 Q90,106 98,106 L154,106 Q162,106 168,114 L178,126 Z"
        fill="#1e1b4b"
        stroke="#4f46e5"
        strokeWidth="2"
      />
      {/* Folder Back Base */}
      <rect x="90" y="122" width="220" height="98" rx="14" fill="#1e1b4b" stroke="#4f46e5" strokeWidth="2" />

      {/* Folder Front Flap (Open 3D perspective) */}
      <path
        d="M82,138 Q82,128 92,128 L308,128 Q318,128 318,138 L318,214 Q318,224 308,224 L92,224 Q82,224 82,214 Z"
        fill="url(#folderFront)"
        stroke="#818cf8"
        strokeWidth="2.5"
      />

      {/* Glossy highlight line on folder rim */}
      <line x1="96" y1="133" x2="304" y2="133" stroke="#a5b4fc" strokeWidth="2" strokeLinecap="round" opacity="0.7" />

      {/* Folder interior pocket decorative details */}
      <rect x="110" y="160" width="180" height="4" rx="2" fill="#6366f1" opacity="0.4" />
      <rect x="110" y="172" width="140" height="4" rx="2" fill="#6366f1" opacity="0.25" />
      <rect x="110" y="184" width="160" height="4" rx="2" fill="#6366f1" opacity="0.15" />
    </g>
  </svg>
)

/* ─────────────────────────────────────────────────────
   SVG Illustration 2 — AI Terminal / Chat Prompt (Minimalist & Expressive)
   Clean terminal window with prompt line, typing wave, and glowing agent status
   ───────────────────────────────────────────────────── */
const TerminalIllustration: React.FC = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 400 240"
    role="img"
    aria-labelledby="terminal-title terminal-desc"
    className="w-full h-full"
  >
    <title id="terminal-title">Prompt AI Coding Agent</title>
    <desc id="terminal-desc">Ilustrasi jendela terminal AI Agent yang siap mengeksekusi prompt pengerjaan laprak.</desc>
    <defs>
      <filter id="termAura" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur stdDeviation="8" result="blur" />
        <feMerge>
          <feMergeNode in="blur" />
          <feMergeNode in="SourceGraphic" />
        </feMerge>
      </filter>
      <linearGradient id="termBg" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor="#0e0f1e" />
        <stop offset="100%" stopColor="#080814" />
      </linearGradient>
      <linearGradient id="termHeader" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stopColor="#1e1b4b" />
        <stop offset="100%" stopColor="#17153a" />
      </linearGradient>
      <radialGradient id="termPulse" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stopColor="#818cf8" stopOpacity="0.4" />
        <stop offset="100%" stopColor="#818cf8" stopOpacity="0" />
      </radialGradient>
    </defs>

    <style>{`
      @keyframes blinkCursor { 0%,100% { opacity: 1; } 50% { opacity: 0; } }
      @keyframes soundBar1 { 0%,100% { height: 8px; y: 176px; } 50% { height: 26px; y: 158px; } }
      @keyframes soundBar2 { 0%,100% { height: 18px; y: 166px; } 50% { height: 8px; y: 176px; } }
      @keyframes soundBar3 { 0%,100% { height: 12px; y: 172px; } 50% { height: 32px; y: 152px; } }
      @keyframes soundBar4 { 0%,100% { height: 24px; y: 160px; } 50% { height: 12px; y: 172px; } }
      @keyframes pulseGlow { 0%,100% { opacity: 0.3; transform: scale(0.96); } 50% { opacity: 0.7; transform: scale(1.05); } }
      .cursor { animation: blinkCursor 0.9s step-end infinite; }
      .bar-1 { animation: soundBar1 1.2s ease-in-out infinite; }
      .bar-2 { animation: soundBar2 1.4s ease-in-out infinite 0.2s; }
      .bar-3 { animation: soundBar3 1.1s ease-in-out infinite 0.4s; }
      .bar-4 { animation: soundBar4 1.3s ease-in-out infinite 0.6s; }
      .term-pulse { animation: pulseGlow 3.5s ease-in-out infinite; transform-origin: 200px 120px; }
    `}</style>

    {/* Ambient Glow */}
    <circle className="term-pulse" cx="200" cy="120" r="110" fill="url(#termPulse)" />

    {/* Background Grid Pattern */}
    <g opacity="0.08">
      {Array.from({ length: 9 }).map((_, r) =>
        Array.from({ length: 15 }).map((_, c) => (
          <circle key={`tg-${r}-${c}`} cx={30 + c * 24} cy={24 + r * 24} r="1" fill="#6366f1" />
        ))
      )}
    </g>

    {/* ── Main Terminal Frame ── */}
    <g filter="url(#termAura)">
      {/* Outer Window Box */}
      <rect x="40" y="22" width="320" height="196" rx="14" fill="url(#termBg)" stroke="#3730a3" strokeWidth="2" />

      {/* Title Bar */}
      <rect x="40" y="22" width="320" height="34" rx="14" fill="url(#termHeader)" />
      <rect x="40" y="44" width="320" height="12" fill="url(#termHeader)" />

      {/* Window Controls (Traffic lights) */}
      <circle cx="62" cy="39" r="4.5" fill="#ef4444" opacity="0.9" />
      <circle cx="77" cy="39" r="4.5" fill="#f59e0b" opacity="0.9" />
      <circle cx="92" cy="39" r="4.5" fill="#10b981" opacity="0.9" />

      {/* Terminal Title Pill */}
      <rect x="150" y="31" width="100" height="16" rx="8" fill="#312e81" opacity="0.6" />
      <circle cx="162" cy="39" r="3" fill="#818cf8" />
      <rect x="172" y="37" width="64" height="4" rx="2" fill="#a5b4fc" opacity="0.8" />

      {/* ── Terminal Body Content ── */}
      {/* Line 1: Command prompt */}
      <text x="60" y="84" fontFamily="monospace" fontSize="13" fontWeight="bold" fill="#818cf8">&gt;</text>
      <text x="78" y="84" fontFamily="monospace" fontSize="12" fontWeight="600" fill="#e0e7ff">npx skills add ngelaprak</text>

      {/* Line 2: Status check */}
      <circle cx="64" cy="107" r="4" fill="#10b981" />
      <rect x="78" y="104" width="140" height="6" rx="3" fill="#34d399" opacity="0.75" />

      {/* Line 3: AI execution prompt line */}
      <text x="60" y="134" fontFamily="monospace" fontSize="13" fontWeight="bold" fill="#818cf8">&gt;</text>
      <rect x="78" y="126" width="180" height="10" rx="4" fill="#6366f1" opacity="0.4" />
      {/* Blinking cursor */}
      <rect className="cursor" x="264" y="123" width="8" height="16" rx="2" fill="#a5b4fc" />

      {/* ── Interactive Wave / Processing Box ── */}
      <rect x="58" y="152" width="284" height="50" rx="10" fill="#1e1b4b" opacity="0.5" stroke="#4f46e5" strokeWidth="1" />

      {/* Soundwave/Processing bars */}
      <g fill="#818cf8">
        <rect className="bar-1" x="80" y="168" width="4.5" height="18" rx="2.25" opacity="0.9" />
        <rect className="bar-2" x="90" y="168" width="4.5" height="18" rx="2.25" opacity="0.8" />
        <rect className="bar-3" x="100" y="168" width="4.5" height="18" rx="2.25" opacity="0.9" />
        <rect className="bar-4" x="110" y="168" width="4.5" height="18" rx="2.25" opacity="0.7" />
        <rect className="bar-2" x="120" y="168" width="4.5" height="18" rx="2.25" opacity="0.85" />
      </g>

      {/* AI Processing Badge on Right */}
      <rect x="230" y="166" width="96" height="22" rx="11" fill="#4338ca" opacity="0.5" stroke="#6366f1" strokeWidth="1" />
      <circle cx="244" cy="177" r="3.5" fill="#34d399">
        <animate attributeName="opacity" values="0.4;1;0.4" dur="1.5s" repeatCount="indefinite" />
      </circle>
      <rect x="254" y="174" width="60" height="5" rx="2.5" fill="#c7d2fe" />
    </g>
  </svg>
)

/* ─────────────────────────────────────────────────────
   SVG Illustration 3 — Finished Report Document (Minimalist & Expressive)
   Clean verified document with Word & PDF companion badges
   ───────────────────────────────────────────────────── */
const ReportIllustration: React.FC = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 400 240"
    role="img"
    aria-labelledby="report-title report-desc"
    className="w-full h-full"
  >
    <title id="report-title">Laporan Praktikum Selesai</title>
    <desc id="report-desc">Ilustrasi laporan praktikum yang telah selesai dan siap diedit dalam format DOCX dan PDF.</desc>
    <defs>
      <filter id="reportAura" x="-25%" y="-25%" width="150%" height="150%">
        <feGaussianBlur stdDeviation="8" result="blur" />
        <feMerge>
          <feMergeNode in="blur" />
          <feMergeNode in="SourceGraphic" />
        </feMerge>
      </filter>
      <filter id="badgeShadow" x="-20%" y="-20%" width="140%" height="140%">
        <feDropShadow dx="0" dy="4" stdDeviation="5" floodColor="#000" floodOpacity="0.55" />
      </filter>
      <linearGradient id="docPaper" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor="#0c1e19" />
        <stop offset="100%" stopColor="#061310" />
      </linearGradient>
      <linearGradient id="wordGrad" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stopColor="#2563eb" />
        <stop offset="100%" stopColor="#1e40af" />
      </linearGradient>
      <linearGradient id="pdfGrad" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stopColor="#dc2626" />
        <stop offset="100%" stopColor="#991b1b" />
      </linearGradient>
      <radialGradient id="emeraldAura" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stopColor="#10b981" stopOpacity="0.4" />
        <stop offset="100%" stopColor="#10b981" stopOpacity="0" />
      </radialGradient>
    </defs>

    <style>{`
      @keyframes docBob { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-7px); } }
      @keyframes checkPulse { 0%,100% { transform: scale(1); } 50% { transform: scale(1.1); } }
      @keyframes auraBreath { 0%,100% { opacity: 0.35; transform: scale(0.96); } 50% { opacity: 0.75; transform: scale(1.06); } }
      .doc-card { animation: docBob 4s ease-in-out infinite; }
      .check-seal { animation: checkPulse 2.4s ease-in-out infinite; transform-origin: 200px 24px; }
      .aura-emerald { animation: auraBreath 3.5s ease-in-out infinite; transform-origin: 200px 125px; }
    `}</style>

    {/* Ambient Glow */}
    <circle className="aura-emerald" cx="200" cy="125" r="105" fill="url(#emeraldAura)" />

    {/* Background Grid Pattern */}
    <g opacity="0.08">
      {Array.from({ length: 9 }).map((_, r) =>
        Array.from({ length: 15 }).map((_, c) => (
          <circle key={`rg-${r}-${c}`} cx={30 + c * 24} cy={24 + r * 24} r="1" fill="#10b981" />
        ))
      )}
    </g>

    {/* ── Main Report Document Sheet ── */}
    <g className="doc-card" filter="url(#reportAura)">
      {/* Paper Sheet */}
      <rect x="120" y="32" width="160" height="186" rx="14" fill="url(#docPaper)" stroke="#10b981" strokeWidth="2" />

      {/* Header Accent Bar */}
      <rect x="120" y="32" width="160" height="34" rx="14" fill="#064e3b" opacity="0.75" />
      <rect x="120" y="54" width="160" height="12" fill="#064e3b" opacity="0.75" />
      {/* Title skeleton bar */}
      <rect x="145" y="44" width="110" height="7" rx="3.5" fill="#6ee7b7" />

      {/* Abstract Content Lines (Clean paragraph simulation) */}
      <rect x="138" y="78" width="124" height="4" rx="2" fill="#10b981" opacity="0.5" />
      <rect x="138" y="88" width="98" height="4" rx="2" fill="#10b981" opacity="0.35" />
      <rect x="138" y="98" width="114" height="4" rx="2" fill="#10b981" opacity="0.25" />

      {/* Code/Graph Block */}
      <rect x="138" y="112" width="124" height="36" rx="8" fill="#022c22" stroke="#065f46" strokeWidth="1" />
      <rect x="150" y="122" width="60" height="3.5" rx="1.75" fill="#34d399" opacity="0.75" />
      <rect x="160" y="130" width="80" height="3.5" rx="1.75" fill="#34d399" opacity="0.5" />
      <rect x="150" y="138" width="40" height="3.5" rx="1.75" fill="#34d399" opacity="0.65" />

      {/* IDE Screenshot / Chart Mockup Block */}
      <rect x="138" y="156" width="124" height="34" rx="8" fill="#022c22" stroke="#065f46" strokeWidth="1" opacity="0.8" />
      <circle cx="152" cy="173" r="5" fill="#10b981" opacity="0.6" />
      <rect x="164" y="171" width="76" height="4" rx="2" fill="#34d399" opacity="0.5" />
    </g>

    {/* ── DOCX Badge (Left) ── */}
    <g filter="url(#badgeShadow)">
      <rect x="42" y="78" width="64" height="76" rx="12" fill="url(#wordGrad)" stroke="#60a5fa" strokeWidth="2" />
      <text x="74" y="124" textAnchor="middle" fontFamily="Arial, Helvetica, sans-serif" fontSize="26" fontWeight="900" fill="#ffffff">
        W
      </text>
      <rect x="52" y="136" width="44" height="4" rx="2" fill="#93c5fd" opacity="0.8" />
    </g>

    {/* ── PDF Badge (Right) ── */}
    <g filter="url(#badgeShadow)">
      <rect x="294" y="78" width="64" height="76" rx="12" fill="url(#pdfGrad)" stroke="#f87171" strokeWidth="2" />
      <text x="326" y="122" textAnchor="middle" fontFamily="Arial, Helvetica, sans-serif" fontSize="18" fontWeight="900" fill="#ffffff">
        PDF
      </text>
      <rect x="304" y="136" width="44" height="4" rx="2" fill="#fca5a5" opacity="0.8" />
    </g>

    {/* ── Floating Verified Checkmark Seal ── */}
    <g className="check-seal" filter="url(#reportAura)">
      <circle cx="200" cy="24" r="16" fill="#047857" stroke="#34d399" strokeWidth="2.5" />
      <path
        d="M192,24 L197,29 L209,17"
        stroke="#ffffff"
        strokeWidth="3"
        fill="none"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </g>

    {/* Connecting subtle dashed light rays */}
    <g opacity="0.35">
      <line x1="106" y1="116" x2="120" y2="116" stroke="#3b82f6" strokeWidth="2" strokeDasharray="3 3" />
      <line x1="280" y1="116" x2="294" y2="116" stroke="#ef4444" strokeWidth="2" strokeDasharray="3 3" />
    </g>
  </svg>
)

/* ═══════════════════════════════════════════════════════
   TutorSection — Clean Minimalist Component
   ═══════════════════════════════════════════════════════ */
export const TutorSection: React.FC = () => {
  const [copiedPrompt, setCopiedPrompt] = useState(false)

  const studentPrompt =
    'npx skills add ngelaprak && bantu aku selesaikan laporan praktikum ini sesuai modul dan template yang ada di workspace'

  const handleCopyPrompt = () => {
    navigator.clipboard.writeText(studentPrompt)
    setCopiedPrompt(true)
    setTimeout(() => setCopiedPrompt(false), 2200)
  }

  return (
    <section id="tutorial" className="py-20 md:py-28 relative overflow-hidden bg-[#090A0F]">
      {/* Background ambient lighting */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[750px] h-[350px] bg-indigo-600/[0.04] blur-[140px] rounded-full pointer-events-none" />

      <div className="max-w-6xl mx-auto px-4 sm:px-6 relative z-10">
        {/* Section Header */}
        <div className="text-center max-w-2xl mx-auto mb-14 md:mb-18">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-mono uppercase tracking-wider mb-3">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Tutorial Praktis</span>
          </div>
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-white tracking-[-0.035em] mb-4 font-sans [text-wrap:balance]">
            Cara Pakai Dalam <span className="text-indigo-400">3 Langkah Mudah</span>
          </h2>
          <p className="text-slate-400 text-sm sm:text-base leading-relaxed [text-wrap:pretty]">
            Panduan praktis mengerjakan tugas praktikum bersama AI Agent.
          </p>
        </div>

        {/* 3 Step Tutorial Cards — Clean & Minimalist */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 md:gap-7 items-stretch">
          
          {/* STEP 1: Taruh File Konteks Praktikum */}
          <div className="rounded-3xl bg-[#0D0F18] border border-white/8 hover:border-indigo-500/30 p-5 sm:p-6 transition-all duration-300 shadow-xl shadow-black/40 flex flex-col justify-between group">
            <div>
              {/* Step Header Badge */}
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-mono font-bold text-indigo-400 px-2.5 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20">
                  LANGKAH 01
                </span>
                <span className="text-2xl font-black font-mono text-slate-700 group-hover:text-indigo-400 transition-colors">
                  01
                </span>
              </div>

              <h3 className="text-lg sm:text-xl font-bold text-white mb-2 tracking-tight">
                Satukan Bahan Praktikum dalam Folder
              </h3>
            </div>

            {/* SVG Illustration */}
            <div className="mt-auto pt-4">
              <div className="rounded-2xl overflow-hidden border border-white/10 relative h-60 sm:h-64 bg-[#08090E] group-hover:border-indigo-500/40 transition-colors shadow-inner flex items-center justify-center">
                <FolderIllustration />
              </div>
            </div>
          </div>

          {/* STEP 2: Jalankan Prompt AI */}
          <div className="rounded-3xl bg-[#0D0F18] border border-white/8 hover:border-indigo-500/30 p-5 sm:p-6 transition-all duration-300 shadow-xl shadow-black/40 flex flex-col justify-between group">
            <div>
              {/* Step Header Badge */}
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-mono font-bold text-indigo-400 px-2.5 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20">
                  LANGKAH 02
                </span>
                <span className="text-2xl font-black font-mono text-slate-700 group-hover:text-indigo-400 transition-colors">
                  02
                </span>
              </div>

              <h3 className="text-lg sm:text-xl font-bold text-white mb-2 tracking-tight">
                Salin &amp; Jalankan Prompt ke AI
              </h3>
            </div>

            {/* SVG Illustration */}
            <div className="mt-auto pt-4">
              <div className="rounded-2xl overflow-hidden border border-white/10 relative h-60 sm:h-64 bg-[#08090E] group-hover:border-indigo-500/40 transition-colors shadow-inner flex items-center justify-center">
                <TerminalIllustration />
              </div>
            </div>
          </div>

          {/* STEP 3: Laprak Jadi dan Bisa Editable */}
          <div className="rounded-3xl bg-[#0D0F18] border border-white/8 hover:border-indigo-500/30 p-5 sm:p-6 transition-all duration-300 shadow-xl shadow-black/40 flex flex-col justify-between group">
            <div>
              {/* Step Header Badge */}
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-mono font-bold text-emerald-400 px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20">
                  LANGKAH 03
                </span>
                <span className="text-2xl font-black font-mono text-slate-700 group-hover:text-emerald-400 transition-colors">
                  03
                </span>
              </div>

              <h3 className="text-lg sm:text-xl font-bold text-white mb-2 tracking-tight">
                Laporan Selesai &amp; Bebas Diedit
              </h3>

              {/* Download Buttons for DOCX and PDF */}
              <div className="grid grid-cols-2 gap-2 mb-2">
                <a
                  href="/samples/strukdat/LAPRAK_SAMPLE_STRUKDAT_MODUL3.docx"
                  download
                  className="flex items-center justify-between p-2 rounded-xl bg-blue-500/10 border border-blue-500/25 hover:bg-blue-500/20 text-blue-200 transition-colors text-xs font-mono"
                  title="Unduh DOCX"
                >
                  <span className="font-bold flex items-center gap-1.5">
                    <span className="text-blue-400 font-extrabold">W</span> .docx
                  </span>
                  <Download className="w-3.5 h-3.5" />
                </a>

                <a
                  href="/samples/strukdat/LAPRAK_SAMPLE_STRUKDAT_MODUL3.pdf"
                  download
                  className="flex items-center justify-between p-2 rounded-xl bg-rose-500/10 border border-rose-500/25 hover:bg-rose-500/20 text-rose-200 transition-colors text-xs font-mono"
                  title="Unduh PDF"
                >
                  <span className="font-bold flex items-center gap-1.5">
                    <span className="text-rose-400 font-extrabold">PDF</span> .pdf
                  </span>
                  <Download className="w-3.5 h-3.5" />
                </a>
              </div>
            </div>

            {/* SVG Illustration */}
            <div className="mt-auto pt-4">
              <div className="rounded-2xl overflow-hidden border border-white/10 relative h-60 sm:h-64 bg-[#08090E] group-hover:border-emerald-500/40 transition-colors shadow-inner flex items-center justify-center">
                <ReportIllustration />
              </div>
            </div>
          </div>

        </div>

        {/* Dedicated Copy Prompt Banner Below the 3 Cards */}
        <div className="mt-8 rounded-3xl bg-gradient-to-r from-indigo-950/40 via-[#0D0F18] to-indigo-950/40 border border-indigo-500/25 p-5 sm:p-6 shadow-2xl relative overflow-hidden group">
          <div className="flex flex-col lg:flex-row items-stretch lg:items-center justify-between gap-4">
            <div className="flex items-center gap-3.5 shrink-0">
              <div className="w-11 h-11 rounded-2xl bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center shrink-0 shadow-inner">
                <Terminal className="w-5 h-5 text-indigo-400" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h4 className="text-sm sm:text-base font-bold text-white">Prompt Eksekusi AI Mahasiswa</h4>
                  <span className="text-[10px] font-mono font-medium px-2 py-0.5 rounded-full bg-indigo-500/15 border border-indigo-500/25 text-indigo-300">
                    1-Klik Salin
                  </span>
                </div>
                <p className="text-xs text-slate-400 mt-0.5">
                  Tempel langsung ke chat Antigravity, Cursor, Claude Code, Copilot, atau VS Code.
                </p>
              </div>
            </div>

            {/* Prompt Code Display & One-Click Copy Button */}
            <div className="flex-1 min-w-0 flex flex-col sm:flex-row items-stretch sm:items-center gap-2.5">
              <div className="flex-1 min-w-0 font-mono text-xs text-slate-200 bg-black/60 px-3.5 py-3 rounded-xl border border-white/10 select-all truncate">
                <span className="text-indigo-400 select-none mr-2 font-bold">$</span>
                {studentPrompt}
              </div>
              <button
                onClick={handleCopyPrompt}
                className={`shrink-0 flex items-center justify-center gap-2 py-3 px-5 rounded-xl text-xs font-semibold font-mono transition-all duration-200 cursor-pointer ${
                  copiedPrompt
                    ? 'bg-emerald-500 text-white shadow-lg shadow-emerald-500/30'
                    : 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg shadow-indigo-600/30 active:scale-[0.98]'
                }`}
                title="Salin Prompt"
              >
                {copiedPrompt ? (
                  <>
                    <Check className="w-4 h-4 text-white" />
                    <span>Prompt Tersalin!</span>
                  </>
                ) : (
                  <>
                    <Copy className="w-4 h-4" />
                    <span>Salin Prompt</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
