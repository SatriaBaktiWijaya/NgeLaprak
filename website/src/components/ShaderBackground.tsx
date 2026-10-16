import React from 'react'

export const ShaderBackground: React.FC = () => {
  return (
    <div className="fixed inset-0 pointer-events-none overflow-hidden select-none z-0">
      {/* Supaste-inspired Cosmic Glow Aura (Using GPU-friendly native radial gradients with zero blur filters) */}
      <div
        className="absolute -top-40 left-1/2 -translate-x-1/2 w-[1000px] h-[550px] rounded-full pointer-events-none"
        style={{
          background: 'radial-gradient(ellipse at center, rgba(99, 102, 241, 0.16) 0%, rgba(124, 58, 237, 0.08) 40%, transparent 70%)'
        }}
      />
      <div
        className="absolute top-[20%] left-1/2 -translate-x-1/2 w-[600px] h-[350px] rounded-full pointer-events-none"
        style={{
          background: 'radial-gradient(ellipse at center, rgba(79, 70, 229, 0.12) 0%, transparent 70%)'
        }}
      />
      <div
        className="absolute top-[45%] -left-40 w-[600px] h-[600px] rounded-full pointer-events-none"
        style={{
          background: 'radial-gradient(circle at center, rgba(49, 46, 129, 0.12) 0%, transparent 70%)'
        }}
      />
      <div
        className="absolute top-[60%] -right-40 w-[600px] h-[600px] rounded-full pointer-events-none"
        style={{
          background: 'radial-gradient(circle at center, rgba(88, 28, 135, 0.10) 0%, transparent 70%)'
        }}
      />

      {/* Subtle modern tech grid overlay */}
      <div
        className="absolute inset-0 opacity-[0.03] pointer-events-none"
        style={{
          backgroundImage: `radial-gradient(rgba(255, 255, 255, 0.4) 1px, transparent 1px)`,
          backgroundSize: '32px 32px'
        }}
      />

      {/* Vignette */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-[#08090E]/60 to-[#08090E] pointer-events-none" />
    </div>
  )
}
