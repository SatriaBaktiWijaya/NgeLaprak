import React from 'react'
import { Sparkles, ArrowUp, Coffee } from 'lucide-react'
import { NgeLaprakLogo } from './NgeLaprakLogo'

const GithubIcon: React.FC<{ className?: string }> = ({ className = "w-4 h-4" }) => (
  <svg className={className} viewBox="0 0 24 24" fill="currentColor">
    <path fillRule="evenodd" clipRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" />
  </svg>
)

export const Footer: React.FC = () => {
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return (
    <footer className="border-t border-white/5 bg-[#07080C] py-12 text-slate-400 text-xs sm:text-sm relative">
      <div className="max-w-6xl mx-auto px-4 sm:px-6">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6 pb-8 border-b border-white/5">
          {/* Logo */}
          <div className="flex items-center gap-2.5">
            <NgeLaprakLogo size={28} className="rounded-xl shadow-md shadow-indigo-600/30" />
            <span className="font-bold text-white text-base font-sans">
              Nge<span className="text-indigo-400">Laprak</span>
            </span>
          </div>

          {/* Quick links */}
          <div className="flex flex-wrap items-center gap-6 text-xs font-medium text-slate-400">
            <a href="#tutorial" className="hover:text-white transition-colors">
              Tutorial
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
            <a
              href="https://saweria.co/satriabaktiwijaya"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1.5 text-amber-400/90 hover:text-amber-300 transition-colors"
            >
              <Coffee className="w-3.5 h-3.5 text-amber-400" />
              <span>Saweria</span>
            </a>
            <a
              href="https://github.com/SatriaBaktiWijaya/NgeLaprak"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1.5 hover:text-white transition-colors"
            >
              <GithubIcon className="w-3.5 h-3.5" />
              <span>GitHub</span>
            </a>
          </div>

          {/* Back to top */}
          <button
            onClick={scrollToTop}
            className="p-2.5 rounded-xl bg-white/5 hover:bg-white/10 text-slate-400 hover:text-white transition-all active:scale-[0.98] cursor-pointer"
            title="Kembali ke atas"
          >
            <ArrowUp className="w-4 h-4" />
          </button>
        </div>

        {/* Bottom Bar */}
        <div className="pt-6 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-slate-500">
          <div>Dibuat untuk mahasiswa sains komputer &amp; informatika. MIT License.</div>
          <div className="font-mono text-[11px] text-slate-600">NetBeans • Code::Blocks • VS Code • DBeaver</div>
        </div>
      </div>
    </footer>
  )
}
