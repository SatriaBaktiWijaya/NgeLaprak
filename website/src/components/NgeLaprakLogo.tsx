import React from 'react'

interface NgeLaprakLogoProps {
  size?: number | string
  className?: string
  variant?: 'icon' | 'mark'
}

/**
 * Official NgeLaprak Brand Logo Component
 * Concept 1: The Code-Document 'N' with AI Quantum Spark
 */
export const NgeLaprakLogo: React.FC<NgeLaprakLogoProps> = ({
  size = 28,
  className = '',
  variant = 'icon'
}) => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 100 100"
      width={size}
      height={size}
      fill="none"
      role="img"
      aria-label="NgeLaprak Logo"
      className={`shrink-0 ${className}`}
    >
      <defs>
        <linearGradient id="nlLogoBg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#4f46e5" />
          <stop offset="50%" stopColor="#3730a3" />
          <stop offset="100%" stopColor="#1e1b4b" />
        </linearGradient>

        <linearGradient id="nlLogoBorder" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#a5b4fc" stopOpacity="0.8" />
          <stop offset="50%" stopColor="#6366f1" stopOpacity="0.3" />
          <stop offset="100%" stopColor="#312e81" stopOpacity="0.6" />
        </linearGradient>

        <linearGradient id="nlLogoBeam" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#38bdf8" />
          <stop offset="100%" stopColor="#6366f1" />
        </linearGradient>

        <filter id="nlLogoGlow" x="-30%" y="-30%" width="160%" height="160%">
          <feGaussianBlur stdDeviation="2.5" result="blur" />
          <feMerge>
            <feMergeNode in="blur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>

      {/* Squircle Base Frame */}
      <rect
        x="5"
        y="5"
        width="90"
        height="90"
        rx="24"
        fill="url(#nlLogoBg)"
        stroke="url(#nlLogoBorder)"
        strokeWidth="2.5"
      />

      {/* Document 4-4-3-3 Margin Corner Mark */}
      <path d="M16 26 L16 18 L24 18" stroke="#38bdf8" strokeWidth="2.5" strokeLinecap="round" opacity="0.8" />
      <path d="M84 74 L84 82 L76 82" stroke="#38bdf8" strokeWidth="2.5" strokeLinecap="round" opacity="0.8" />

      {/* The Iconic 'N' (Lettermark + Document Silhouette) */}
      <g>
        {/* Left Column (Document Spine) */}
        <rect x="22" y="24" width="13" height="52" rx="4.5" fill="#ffffff" />
        {/* Micro-dashes representing report binding / code lines */}
        <rect x="25.5" y="32" width="6" height="2" rx="1" fill="#4338ca" opacity="0.6" />
        <rect x="25.5" y="42" width="6" height="2" rx="1" fill="#4338ca" opacity="0.6" />
        <rect x="25.5" y="52" width="6" height="2" rx="1" fill="#4338ca" opacity="0.6" />
        <rect x="25.5" y="62" width="6" height="2" rx="1" fill="#4338ca" opacity="0.6" />

        {/* Right Column (Document Edge) */}
        <rect x="65" y="24" width="13" height="52" rx="4.5" fill="#ffffff" />

        {/* Dynamic Diagonal Code Chevron */}
        <path d="M26 26 L68 68 L74 68 L32 26 Z" fill="url(#nlLogoBeam)" />
      </g>

      {/* 4-Point AI Sparkle / Quantum Star */}
      <path
        d="M78 12 Q78 19 85 19 Q78 19 78 26 Q78 19 71 19 Q78 19 78 12 Z"
        fill="#38bdf8"
        filter="url(#nlLogoGlow)"
      />
      <circle cx="78" cy="19" r="1.5" fill="#ffffff" />
    </svg>
  )
}
