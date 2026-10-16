import React from 'react'

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
 * 100% Mobile & WebKit Safe Dithering / Tech Dot Background.
 * 
 * Uses pure CSS radial-gradient tiling instead of SVG userSpaceOnUse patterns or WebGL contexts.
 * This completely prevents iOS WebKit GPU process buffer allocation failures (OOM crashes)
 * on tall sections (Hero, Bento, IDE Gallery) in mobile Safari and In-App browsers (Instagram, etc.)
 * while preserving the signature dark tech dot-matrix and ambient aesthetic.
 */
export const SafeImageDithering: React.FC<SafeImageDitheringProps> = ({
  image,
  colorBack = '#090A0F',
  colorFront = '#6366F1',
  className = 'w-full h-full',
  size = 2
}) => {
  // Spacing in pixels for the CSS dot pattern (clean & performant)
  const spacing = Math.max(12, Math.round(size * 7))

  return (
    <div className={`relative overflow-hidden pointer-events-none select-none ${className}`}>
      {/* Background Image (Desaturated & Ambient) */}
      {image && (
        <img
          src={image}
          alt=""
          className="w-full h-full object-cover opacity-25 transition-opacity duration-500"
          loading="lazy"
          decoding="async"
        />
      )}

      {/* Subtle Color Wash Overlay (Zero mix-blend-mode to avoid GPU layer crashes) */}
      <div
        className="absolute inset-0 pointer-events-none opacity-40"
        style={{
          background: `radial-gradient(circle at center, ${colorFront} 0%, transparent 75%)`
        }}
      />

      {/* Lightweight CSS Dot-Matrix Pattern (Zero SVG DOM nodes, 100% crash-free) */}
      <div
        className="absolute inset-0 pointer-events-none opacity-35"
        style={{
          backgroundImage: `radial-gradient(circle, ${colorFront} 1.25px, transparent 1.25px)`,
          backgroundSize: `${spacing}px ${spacing}px`,
          backgroundPosition: 'center center'
        }}
      />

      {/* Soft Ambient Vignette */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          background: `radial-gradient(ellipse at center, transparent 30%, ${colorBack} 90%)`
        }}
      />
    </div>
  )
}
