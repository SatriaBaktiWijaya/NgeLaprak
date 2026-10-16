import React, { Component, useState, useEffect, type ErrorInfo, type ReactNode } from 'react'
import { ImageDithering } from '@paper-design/shaders-react'

// Detect WebGL2 support safely in browser
export function isWebGL2Supported(): boolean {
  if (typeof window === 'undefined') return false
  try {
    const canvas = document.createElement('canvas')
    const gl = canvas.getContext('webgl2')
    return Boolean(gl)
  } catch {
    return false
  }
}

interface ErrorBoundaryProps {
  children: ReactNode
  fallback: ReactNode
}

interface ErrorBoundaryState {
  hasError: boolean
}

class WebGLErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(): ErrorBoundaryState {
    return { hasError: true }
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Silently suppress WebGL unsupported errors and switch to fallback
    console.warn('WebGL2 not available for shader, switched to CSS fallback:', error.message)
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback
    }
    return this.props.children
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

export const SafeImageDithering: React.FC<SafeImageDitheringProps> = ({
  image,
  className = 'w-full h-full',
  type = '8x8',
  size = 2,
  ...props
}) => {
  const [canRenderWebGL, setCanRenderWebGL] = useState(false)
  const [hasChecked, setHasChecked] = useState(false)

  useEffect(() => {
    setCanRenderWebGL(isWebGL2Supported())
    setHasChecked(true)
  }, [])

  // Universal CSS Dither / Tech Dot fallback (looks great without any GPU/WebGL requirements)
  const fallback = (
    <div className={`relative overflow-hidden pointer-events-none select-none ${className}`}>
      {image && (
        <img
          src={image}
          alt=""
          className="w-full h-full object-cover filter contrast-125 brightness-75 grayscale opacity-30"
          loading="lazy"
        />
      )}
      <div
        className="absolute inset-0 opacity-25 pointer-events-none"
        style={{
          backgroundImage: 'radial-gradient(rgba(99, 102, 241, 0.7) 1px, transparent 1px)',
          backgroundSize: '10px 10px'
        }}
      />
    </div>
  )

  if (!hasChecked || !canRenderWebGL) {
    return fallback
  }

  return (
    <WebGLErrorBoundary fallback={fallback}>
      <ImageDithering
        image={image}
        className={className}
        type={type}
        size={size}
        {...props}
      />
    </WebGLErrorBoundary>
  )
}
