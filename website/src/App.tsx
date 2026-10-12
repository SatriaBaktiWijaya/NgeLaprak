import React, { useEffect, useRef } from 'react'
import gsap from 'gsap'
import { Navbar } from './components/Navbar'
import { ShaderBackground } from './components/ShaderBackground'
import { Hero } from './components/Hero'
import { PipelineVisualizer } from './components/PipelineVisualizer'
import { IdeGallery } from './components/IdeGallery'
import { BeforeAfter } from './components/BeforeAfter'
import { FeaturesBento } from './components/FeaturesBento'
import { SampleViewer } from './components/SampleViewer'
import { InstallGuide } from './components/InstallGuide'
import { Footer } from './components/Footer'

export const App: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Subtle initial reveal animation with GSAP
    const ctx = gsap.context(() => {
      gsap.from('.animate-fade-in', {
        opacity: 0,
        y: 20,
        duration: 0.8,
        stagger: 0.15,
        ease: 'power2.out'
      })
    }, containerRef)

    return () => ctx.revert()
  }, [])

  return (
    <div ref={containerRef} className="min-h-screen bg-[#08090E] text-[#F8FAFC] selection:bg-indigo-500/30 selection:text-white relative">
      {/* Dynamic Background Shader & Glowing Canvas */}
      <ShaderBackground />

      {/* Floating Pill Navbar */}
      <Navbar />

      {/* Main Sections */}
      <main className="relative z-10">
        <Hero />
        <PipelineVisualizer />
        <IdeGallery />
        <BeforeAfter />
        <FeaturesBento />
        <SampleViewer />
        <InstallGuide />
      </main>

      {/* Footer */}
      <Footer />
    </div>
  )
}

export default App
