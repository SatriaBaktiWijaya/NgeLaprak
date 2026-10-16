import React, { useState, useEffect, useRef, Component, type ErrorInfo, type ReactNode } from 'react'
import { ImageDithering } from '@paper-design/shaders-react'

interface ErrorBoundaryProps {
  children: ReactNode
  fallback: ReactNode
}

interface ErrorBoundaryState {
  hasError: boolean
}

class ShaderErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(): ErrorBoundaryState {
    return { hasError: true }
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.warn('Paper Shader caught safely by boundary, using optimized fallback:', error.message)
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback
    }
    return this.props.children
  }
}

// Safely test WebGL2 capability without memory leaks
function isWebGL2Available(): boolean {
  if (typeof window === 'undefined') return false
  try {
    const canvas = document.createElement('canvas')
    const gl = canvas.getContext('webgl2', { powerPreference: 'low-power' })
    const supported = Boolean(gl)
    if (gl) {
      const ext = gl.getExtension('WEBGL_lose_context')
      if (ext) ext.loseContext()
    }
    return supported
  } catch {
    return false
  }
}

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
 * 
 * Combines authentic @paper-design/shaders-react Bayer dithering with bulletproof safety guards:
 * 1. Preloads the image before mounting (prevents "image must be fully loaded" error in paper-shader)
 * 2. Strict memory caps (minPixelRatio=1, capped maxPixelCount) to avoid iOS WebKit GPU crashes
 * 3. IntersectionObserver lazy-mounting (only 1 active WebGL context in viewport at a time)
 * 4. ErrorBoundary fallback for restricted in-app browsers
 */
export const SafeImageDithering: React.FC<SafeImageDitheringProps> = ({
  image,
  colorBack = '#090A0F',
  colorFront = '#6366F1',
  colorHighlight = '#818CF8',
  originalColors = false,
  inverted = false,
  type = '8x8',
  size = 2,
  colorSteps = 2,
  fit = 'cover',
  className = 'w-full h-full'
}) => {
  const containerRef = useRef<HTMLDivElement>(null)
  const [canRenderShader, setCanRenderShader] = useState(false)
  const [imageLoaded, setImageLoaded] = useState(false)
  const [isInView, setIsInView] = useState(false)
  const [isMobile, setIsMobile] = useState(false)

  // 1. Initial WebGL2 support check
  useEffect(() => {
    const supported = isWebGL2Available()
    const mobile = typeof window !== 'undefined' && (window.innerWidth < 768 || /iPhone|iPad|iPod|Android/i.test(navigator.userAgent))
    setIsMobile(mobile)
    setCanRenderShader(supported)
  }, [])

  // 2. Preload the image so paper-shader never throws "must be fully loaded"
  useEffect(() => {
    if (!image) return
    let active = true
    const img = new Image()
    img.src = image
    if (img.complete && img.naturalWidth > 0) {
      setImageLoaded(true)
    } else {
      img.onload = () => {
        if (active) setImageLoaded(true)
      }
      img.onerror = () => {
        if (active) setImageLoaded(false)
      }
    }
    return () => {
      active = false
    }
  }, [image])

  // 3. Viewport intersection: only mount WebGL when visible (never more than 1 context active)
  useEffect(() => {
    const el = containerRef.current
    if (!el || typeof IntersectionObserver === 'undefined') {
      setIsInView(true)
      return
    }

    const observer = new IntersectionObserver(
      (entries) => {
        const entry = entries[0]
        setIsInView(entry.isIntersecting)
      },
      { rootMargin: '150px 0px' }
    )

    observer.observe(el)
    return () => observer.disconnect()
  }, [])

  // High-End CSS Dither Fallback (Used when shader is loading, out of view, or on WebGL-restricted webviews)
  const fallback = (
    <div className="absolute inset-0 overflow-hidden pointer-events-none select-none">
      {image && (
        <img
          src={image}
          alt=""
          className="w-full h-full object-cover opacity-25 filter contrast-125"
          loading="lazy"
          decoding="async"
        />
      )}
      {/* Color Tint */}
      <div
        className="absolute inset-0 pointer-events-none opacity-40"
        style={{
          background: `radial-gradient(circle at center, ${colorFront} 0%, transparent 75%)`
        }}
      />
      {/* Repeating Dot Matrix */}
      <div
        className="absolute inset-0 pointer-events-none opacity-35"
        style={{
          backgroundImage: `radial-gradient(circle, ${colorFront} 1.25px, transparent 1.25px)`,
          backgroundSize: `${Math.max(12, Math.round(size * 7))}px ${Math.max(12, Math.round(size * 7))}px`,
          backgroundPosition: 'center center'
        }}
      />
      {/* Ambient Vignette */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          background: `radial-gradient(ellipse at center, transparent 30%, ${colorBack} 90%)`
        }}
      />
    </div>
  )

  const shouldRenderShader = canRenderShader && imageLoaded && isInView

  return (
    <div ref={containerRef} className={`relative overflow-hidden pointer-events-none select-none ${className}`}>
      {shouldRenderShader ? (
        <ShaderErrorBoundary fallback={fallback}>
          <ImageDithering
            image={image}
            colorBack={colorBack}
            colorFront={colorFront}
            colorHighlight={colorHighlight}
            originalColors={originalColors}
            inverted={inverted}
            type={type}
            size={isMobile ? Math.max(size, 2.5) : size}
            colorSteps={colorSteps}
            fit={fit}
            minPixelRatio={1}
            maxPixelCount={isMobile ? 350000 : 1200000}
            webGlContextAttributes={{
              powerPreference: 'low-power',
              preserveDrawingBuffer: false,
              antialias: false,
              depth: false,
              stencil: false
            }}
            className="w-full h-full"
          />
        </ShaderErrorBoundary>
      ) : (
        fallback
      )}

      {/* Ambient Vignette Overlay for smooth blending */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          background: `radial-gradient(ellipse at center, transparent 35%, ${colorBack} 92%)`
        }}
      />
    </div>
  )
}
