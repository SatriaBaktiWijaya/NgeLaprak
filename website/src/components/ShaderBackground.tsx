import React from 'react'

export const ShaderBackground: React.FC = () => {
  return (
    <div className="fixed inset-0 pointer-events-none overflow-hidden select-none z-0">
      {/* Supaste-inspired Cosmic Glow Aura */}
      <div className="absolute -top-40 left-1/2 -translate-x-1/2 w-[1000px] h-[550px] bg-gradient-to-b from-indigo-500/20 via-purple-600/10 to-transparent blur-[140px] rounded-full pointer-events-none" />
      <div className="absolute top-[20%] left-1/2 -translate-x-1/2 w-[600px] h-[300px] bg-indigo-600/15 blur-[100px] rounded-full pointer-events-none" />
      <div className="absolute top-[45%] -left-40 w-[600px] h-[600px] bg-indigo-900/10 blur-[130px] rounded-full pointer-events-none" />
      <div className="absolute top-[60%] -right-40 w-[600px] h-[600px] bg-purple-900/10 blur-[130px] rounded-full pointer-events-none" />

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
