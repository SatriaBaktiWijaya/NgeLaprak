import React, { useState, useEffect } from 'react'
import { Sparkles, Terminal, Menu, X, BookOpen } from 'lucide-react'

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
      setScrolled(window.scrollY > 20)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return (
    <>
      <header className="fixed top-4 left-1/2 -translate-x-1/2 z-50 w-[94%] max-w-4xl transition-all duration-300">
        <div
          className={`flex items-center justify-between px-4 sm:px-5 py-2.5 rounded-full border transition-all duration-300 ${
            scrolled
              ? 'bg-[#0A0D18]/95 backdrop-blur-2xl border-white/15 shadow-2xl shadow-black/80'
              : 'bg-[#0D1020]/90 backdrop-blur-xl border-white/10 shadow-xl shadow-black/50'
          }`}
        >
          {/* Brand Logo */}
          <a href="#" className="flex items-center gap-2.5 group">
            <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-md shadow-indigo-500/30 group-hover:scale-105 transition-transform">
              <Sparkles className="w-4 h-4 text-white" />
            </div>
            <div className="flex items-center gap-1.5">
              <span className="font-bold text-sm sm:text-base tracking-tight text-white font-sans">
                Nge<span className="text-indigo-400">Laprak</span>
              </span>
              <span className="text-[10px] font-mono font-semibold px-1.5 py-0.2 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                v1.2
              </span>
            </div>
          </a>

          {/* Desktop Links */}
          <nav className="hidden md:flex items-center gap-5 text-xs text-slate-300 font-medium">
            <a href="#pipeline" className="hover:text-white transition-colors">
              Alur 3-File
            </a>
            <a href="#gallery" className="hover:text-white transition-colors">
              Galeri IDE
            </a>
            <a href="#compare" className="hover:text-white transition-colors">
              Before/After
            </a>
            <a href="#features" className="hover:text-white transition-colors">
              Fitur
            </a>
            <a href="#samples" className="hover:text-white transition-colors">
              Hasil Dokumen
            </a>
            <a href="#install" className="hover:text-white transition-colors">
              Instalasi
            </a>
          </nav>

          {/* Right Action Buttons */}
          <div className="hidden sm:flex items-center gap-2">
            <a
              href="https://github.com/khilma-ainunnajah/NgeLaprak"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium text-slate-300 bg-white/5 hover:bg-white/10 hover:text-white border border-white/10 transition-all"
            >
              <GithubIcon className="w-3.5 h-3.5" />
              <span>GitHub</span>
            </a>
            <a
              href="#install"
              className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-full text-xs font-semibold text-white bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-400 hover:to-purple-500 shadow-md shadow-indigo-500/25 transition-all"
            >
              <Terminal className="w-3 h-3" />
              <span>Install Skill</span>
            </a>
          </div>

          {/* Mobile hamburger button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-1.5 text-slate-300 hover:text-white focus:outline-none"
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
              href="#pipeline"
              onClick={() => setMobileMenuOpen(false)}
              className="hover:text-indigo-400 transition-colors"
            >
              Alur 3-File
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
              href="#samples"
              onClick={() => setMobileMenuOpen(false)}
              className="hover:text-indigo-400 transition-colors"
            >
              Pratinjau Hasil
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
              href="https://github.com/khilma-ainunnajah/NgeLaprak"
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
              className="flex items-center gap-2 px-5 py-2.5 rounded-full bg-gradient-to-r from-indigo-500 to-purple-600 text-white text-xs font-bold shadow-lg"
            >
              <Terminal className="w-3.5 h-3.5" />
              <span>npx skills add ngelaprak</span>
            </a>
          </nav>
        </div>
      )}
    </>
  )
}
