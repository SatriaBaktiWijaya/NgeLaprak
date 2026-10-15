import React, { useState, useEffect } from 'react'
import { Sparkles, Terminal, Menu, X, BookOpen, Coffee } from 'lucide-react'
import { NgeLaprakLogo } from './NgeLaprakLogo'

const GithubIcon: React.FC<{ className?: string }> = ({ className = "w-4 h-4" }) => (
  <svg className={className} viewBox="0 0 24 24" fill="currentColor">
    <path fillRule="evenodd" clipRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" />
  </svg>
)

export const Navbar: React.FC = () => {
  const [scrolled, setScrolled] = useState(false)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 30)
    }
    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return (
    <>
      <header
        className={`fixed left-1/2 -translate-x-1/2 z-50 transition-all duration-300 ease-out ${
          scrolled
            ? 'top-2 sm:top-3 w-[90%] max-w-4xl'
            : 'top-4 sm:top-5 w-[94%] max-w-5xl'
        }`}
      >
        <div
          className={`flex items-center justify-between rounded-full border transition-all duration-300 shadow-[inset_0_1px_0_rgba(255,255,255,0.08)] ${
            scrolled
              ? 'bg-[#090A0F]/90 backdrop-blur-2xl border-white/15 shadow-2xl shadow-black/90 px-3.5 sm:px-4 py-1.5 sm:py-2'
              : 'bg-[#0D0E17]/80 backdrop-blur-xl border-white/8 shadow-xl shadow-black/50 px-4 sm:px-5 py-2.5 sm:py-3'
          }`}
        >
          {/* Brand Logo */}
          <a href="#" className="flex items-center gap-2 sm:gap-2.5 group focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 rounded-lg">
            <NgeLaprakLogo
              size={scrolled ? 24 : 28}
              className="group-hover:scale-105 active:scale-95 transition-all duration-300 shadow-md shadow-indigo-600/30 rounded-xl"
            />
            <div className="flex items-center gap-1.5 sm:gap-2">
              <span className={`font-bold tracking-tight text-white font-sans transition-all duration-300 ${
                scrolled ? 'text-xs sm:text-sm' : 'text-sm sm:text-base'
              }`}>
                Nge<span className="text-indigo-400">Laprak</span>
              </span>
              <span className={`font-mono font-semibold rounded-full bg-indigo-500/10 text-indigo-300 border border-indigo-500/25 tabular-nums transition-all duration-300 ${
                scrolled ? 'text-[9px] px-1.5 py-0' : 'text-[10px] px-1.5 py-0.5'
              }`}>
                v1.2
              </span>
            </div>
          </a>

          {/* Desktop Links */}
          <nav className={`hidden lg:flex items-center font-medium transition-all duration-300 ${
            scrolled ? 'gap-4 text-[11px] text-slate-300' : 'gap-5 text-xs text-slate-300'
          }`}>
            <a href="#tutorial" className="hover:text-white transition-colors focus-visible:outline-none focus-visible:text-white">
              Tutorial
            </a>
            <a href="#gallery" className="hover:text-white transition-colors focus-visible:outline-none focus-visible:text-white">
              Galeri IDE
            </a>
            <a href="#compare" className="hover:text-white transition-colors focus-visible:outline-none focus-visible:text-white">
              Before/After
            </a>
            <a href="#features" className="hover:text-white transition-colors focus-visible:outline-none focus-visible:text-white">
              Fitur
            </a>
            <a href="#install" className="hover:text-white transition-colors focus-visible:outline-none focus-visible:text-white">
              Instalasi
            </a>
          </nav>

          {/* Right Action Buttons */}
          <div className="hidden sm:flex items-center gap-1.5 sm:gap-2">
            <a
              href="https://saweria.co/satriabaktiwijaya"
              target="_blank"
              rel="noopener noreferrer"
              className={`flex items-center gap-1.5 rounded-full font-semibold text-amber-200 bg-amber-500/10 hover:bg-amber-500/20 hover:text-amber-100 border border-amber-500/30 hover:border-amber-400/50 shadow-sm shadow-amber-950/30 active:scale-[0.98] transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-amber-500 group ${
                scrolled ? 'px-2.5 py-1 text-[11px]' : 'px-3 py-1.5 text-xs'
              }`}
              title="Traktir Kopi di Saweria"
            >
              <Coffee className={`text-amber-400 group-hover:scale-110 transition-transform ${scrolled ? 'w-3 h-3' : 'w-3.5 h-3.5'}`} />
              <span>Traktir Kopi</span>
            </a>
            <a
              href="https://github.com/SatriaBaktiWijaya/NgeLaprak"
              target="_blank"
              rel="noopener noreferrer"
              className={`flex items-center gap-1.5 rounded-full font-medium text-slate-300 bg-white/5 hover:bg-white/10 hover:text-white border border-white/10 active:scale-[0.98] transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 ${
                scrolled ? 'px-2.5 py-1 text-[11px]' : 'px-3 py-1.5 text-xs'
              }`}
            >
              <GithubIcon className={scrolled ? 'w-3 h-3' : 'w-3.5 h-3.5'} />
              <span>GitHub</span>
            </a>
            <a
              href="#install"
              className={`flex items-center gap-1.5 rounded-full font-semibold text-white bg-indigo-600 hover:bg-indigo-500 border border-indigo-400/30 shadow-md shadow-indigo-600/30 active:scale-[0.98] transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 ${
                scrolled ? 'px-3 py-1 text-[11px]' : 'px-3.5 py-1.5 text-xs'
              }`}
            >
              <Terminal className={scrolled ? 'w-2.5 h-2.5 text-indigo-200' : 'w-3 h-3 text-indigo-200'} />
              <span>Install Skill</span>
            </a>
          </div>

          {/* Mobile hamburger button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-1.5 text-slate-300 hover:text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 rounded-md"
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </header>

      {/* Mobile Drawer Menu */}
      {mobileMenuOpen && (
        <div className="fixed inset-0 z-50 bg-[#08090E]/95 backdrop-blur-2xl flex flex-col justify-center items-center px-8 md:hidden">
          <button
            onClick={() => setMobileMenuOpen(false)}
            className="absolute top-6 right-6 p-2 text-slate-400 hover:text-white"
          >
            <X className="w-6 h-6" />
          </button>

          <nav className="flex flex-col items-center gap-6 text-base font-semibold text-slate-200">
            <a
              href="#tutorial"
              onClick={() => setMobileMenuOpen(false)}
              className="hover:text-indigo-400 transition-colors"
            >
              Tutorial
            </a>
            <a
              href="#gallery"
              onClick={() => setMobileMenuOpen(false)}
              className="hover:text-indigo-400 transition-colors"
            >
              Galeri IDE
            </a>
            <a
              href="#compare"
              onClick={() => setMobileMenuOpen(false)}
              className="hover:text-indigo-400 transition-colors"
            >
              Before & After
            </a>
            <a
              href="#features"
              onClick={() => setMobileMenuOpen(false)}
              className="hover:text-indigo-400 transition-colors"
            >
              Fitur Unggulan
            </a>
            <a
              href="#install"
              onClick={() => setMobileMenuOpen(false)}
              className="hover:text-indigo-400 transition-colors"
            >
              Instalasi CLI
            </a>

            <div className="w-32 h-px bg-white/10 my-2" />

            <a
              href="https://saweria.co/satriabaktiwijaya"
              target="_blank"
              rel="noopener noreferrer"
              onClick={() => setMobileMenuOpen(false)}
              className="flex items-center gap-2 px-5 py-2.5 rounded-full bg-amber-500/15 border border-amber-500/35 text-amber-200 text-xs font-bold shadow-md shadow-amber-950/30"
            >
              <Coffee className="w-4 h-4 text-amber-400" />
              <span>Traktir Kopi di Saweria</span>
            </a>
            <a
              href="https://github.com/SatriaBaktiWijaya/NgeLaprak"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 px-5 py-2 rounded-full bg-white/10 text-white text-xs"
            >
              <GithubIcon className="w-4 h-4" />
              <span>Buka di GitHub</span>
            </a>
            <a
              href="#install"
              onClick={() => setMobileMenuOpen(false)}
              className="flex items-center gap-2 px-5 py-2.5 rounded-full bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold shadow-lg shadow-indigo-600/30 active:scale-[0.98] transition-all"
            >
              <Terminal className="w-3.5 h-3.5 text-indigo-200" />
              <span>npx skills add SatriaBaktiWijaya/NgeLaprak</span>
            </a>
          </nav>
        </div>
      )}
    </>
  )
}
