import React, { useEffect, useRef } from 'react'
import gsap from 'gsap'
import { Navbar } from './components/Navbar'
import { ShaderBackground } from './components/ShaderBackground'
import { Hero } from './components/Hero'
import { AgentEcosystem } from './components/AgentEcosystem'
import { TutorSection } from './components/TutorSection'
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
      const targets = containerRef.current?.querySelectorAll('.animate-fade-in')
      if (targets && targets.length > 0) {
        gsap.from(targets, {
          opacity: 0,
          y: 20,
          duration: 0.8,
          stagger: 0.15,
          ease: 'power2.out'
        })
      }
    }, containerRef)

    return () => ctx.revert()
  }, [])

  return (
    <div ref={containerRef} className="min-h-screen bg-[#090A0F] text-[#F8FAFC] selection:bg-indigo-500/30 selection:text-white relative">
      {/* Accessibility Skip Link */}
      <a
        href="#tutorial"
        className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-[100] focus:px-4 focus:py-2 focus:bg-white focus:text-black focus:font-semibold focus:rounded-full focus:shadow-2xl"
      >
        Lewati ke Konten Utama
      </a>

      {/* Subtle Noise Texture Overlay */}
      <div
        className="fixed inset-0 pointer-events-none z-40 opacity-[0.03] mix-blend-screen bg-[radial-gradient(#fff_1px,transparent_1px)] [background-size:20px_20px]"
        aria-hidden="true"
      />

      {/* Dynamic Background Shader & Glowing Canvas */}
      <ShaderBackground />

      {/* Floating Pill Navbar */}
      <Navbar />

      {/* Main Sections */}
      <main className="relative z-10">
        <Hero />
        <AgentEcosystem />
        <TutorSection />
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
