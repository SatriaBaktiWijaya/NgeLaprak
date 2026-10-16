import React, { useId } from 'react'

interface SafeImageDitheringProps {
  image: string
  colorBack?: string
  colorFront?: string
  colorHighlight?: string
  originalColors?: boolean
  inverted?: boolean
  type?: '8x8' | '4x4' | '2x2'
  size?: number
  colorSteps?: number
  fit?: 'cover' | 'contain'
  className?: string
  width?: string
  height?: string
}

/**
 * SafeImageDithering
 * A high-performance, 100% mobile-safe dithering background component.
 * Uses hardware-accelerated CSS and SVG pattern rendering instead of heavy WebGL contexts,
 * eliminating iOS WebKit/Safari memory crashes ("This webpage was reloaded because a problem occurred")
 * while maintaining the crisp retro-futuristic dot-matrix aesthetic.
 */
export const SafeImageDithering: React.FC<SafeImageDitheringProps> = ({
  image,
  colorBack = '#090a0f',
  colorFront = '#6366f1',
  colorHighlight = '#818cf8',
  className = 'w-full h-full',
  size = 2
}) => {
  const patternId = useId().replace(/:/g, '')
  const dotSize = Math.max(1.5, size * 1.5)
  const spacing = Math.max(6, size * 4.5)

  return (
    <div className={`relative overflow-hidden pointer-events-none select-none ${className}`}>
      {/* Background Image with high-contrast grayscale filter */}
      {image && (
        <img
          src={image}
          alt=""
          className="w-full h-full object-cover filter contrast-125 brightness-[0.65] grayscale-[0.8] transition-opacity duration-700"
          loading="lazy"
        />
      )}

      {/* Primary Color Tint Overlay (Mix Blend) */}
      <div
        className="absolute inset-0 mix-blend-color pointer-events-none opacity-60"
        style={{ backgroundColor: colorFront }}
      />

      {/* High-Performance SVG Tech Dot-Matrix Pattern */}
      <svg className="absolute inset-0 w-full h-full pointer-events-none opacity-45" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <pattern
            id={patternId}
            width={spacing}
            height={spacing}
            patternUnits="userSpaceOnUse"
          >
            {/* Center dot */}
            <circle cx={spacing / 2} cy={spacing / 2} r={dotSize / 2} fill={colorHighlight} opacity="0.75" />
            {/* Corner dots */}
            <circle cx="0" cy="0" r={dotSize / 3} fill={colorFront} opacity="0.5" />
            <circle cx={spacing} cy="0" r={dotSize / 3} fill={colorFront} opacity="0.5" />
            <circle cx="0" cy={spacing} r={dotSize / 3} fill={colorFront} opacity="0.5" />
            <circle cx={spacing} cy={spacing} r={dotSize / 3} fill={colorFront} opacity="0.5" />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill={`url(#${patternId})`} />
      </svg>

      {/* Smooth Ambient Vignette */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          background: `radial-gradient(circle at center, transparent 35%, ${colorBack} 95%)`
        }}
      />
    </div>
  )
}
