import React from 'react'
import {
  Users,
  Award,
  Sparkles,
  GitPullRequest,
  ExternalLink,
  Code2,
  Heart,
  Coffee,
  CheckCircle2,
  GitFork
} from 'lucide-react'

const GithubIcon: React.FC<{ className?: string }> = ({ className = 'w-4 h-4' }) => (
  <svg className={className} viewBox="0 0 24 24" fill="currentColor">
    <path
      fillRule="evenodd"
      clipRule="evenodd"
      d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"
    />
  </svg>
)

export const Contributors: React.FC = () => {
  return (
    <section id="contributors" className="py-20 md:py-28 relative overflow-hidden bg-[#090A0F] border-t border-white/5">
      {/* Background ambient lighting */}
      <div className="absolute top-1/3 left-1/4 w-[500px] h-[300px] bg-purple-500/10 blur-[130px] rounded-full pointer-events-none" />
      <div className="absolute bottom-10 right-1/4 w-[450px] h-[300px] bg-indigo-500/10 blur-[120px] rounded-full pointer-events-none" />

      <div className="max-w-6xl mx-auto px-4 sm:px-6 relative z-10">
        {/* Section Header */}
        <div className="text-center max-w-2xl mx-auto mb-16">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-400 text-xs font-mono uppercase tracking-wider mb-4 shadow-sm shadow-purple-950/40">
            <Users className="w-3.5 h-3.5" />
            <span>Kontributor Proyek</span>
          </div>
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-white tracking-[-0.035em] mb-4 font-sans [text-wrap:balance]">
            Orang di Balik <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-pink-400 to-indigo-400">NgeLaprak</span>
          </h2>
          <p className="text-slate-400 text-sm sm:text-base leading-relaxed [text-wrap:pretty]">
            Proyek open-source karya mahasiswa untuk mahasiswa. Dari arsitektur pipeline laporan otonom hingga rendering grafis IDE pixel-perfect.
          </p>
        </div>

        {/* Contributor Cards Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-12">
          {/* Spotlight Card: Alexander Frit (Alek) - Col 7 */}
          <div className="lg:col-span-7 rounded-3xl bg-gradient-to-b from-[#131525]/90 to-[#0D0F18]/90 border border-purple-500/30 hover:border-purple-400/50 p-6 sm:p-8 relative overflow-hidden transition-all duration-300 shadow-2xl shadow-purple-950/20 group flex flex-col justify-between">
            {/* Top decorative gradient bar */}
            <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-purple-500 via-pink-500 to-indigo-500" />

            <div>
              {/* Header with Avatar & Badge */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
                <div className="flex items-center gap-4">
                  <div className="relative">
                    <img
                      src="https://github.com/alexanderfrit.png"
                      alt="Alexander Frit"
                      onError={(e) => {
                        // Fallback jika avatar github offline
                        e.currentTarget.src = 'https://ui-avatars.com/api/?name=Alexander+Frit&background=6366f1&color=fff'
                      }}
                      className="w-16 h-16 rounded-2xl border-2 border-purple-500/40 shadow-lg shadow-purple-950/50 object-cover"
                    />
                    <div className="absolute -bottom-1 -right-1 p-1 rounded-lg bg-[#090A0F] border border-purple-500/40 text-purple-300">
                      <Sparkles className="w-3.5 h-3.5" />
                    </div>
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className="text-xl font-bold text-white tracking-tight">Alexander Frit</h3>
                      <span className="text-xs text-purple-300 font-mono">(Alek)</span>
                    </div>
                    <a
                      href="https://github.com/alexanderfrit"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 text-xs text-slate-400 hover:text-purple-300 font-mono transition-colors"
                    >
                      <GithubIcon className="w-3 h-3" />
                      <span>@alexanderfrit</span>
                      <ExternalLink className="w-2.5 h-2.5 opacity-60" />
                    </a>
                  </div>
                </div>

                <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-purple-500/15 border border-purple-500/30 text-purple-300 text-xs font-mono font-semibold self-start sm:self-auto shadow-sm">
                  <Award className="w-3.5 h-3.5 text-purple-400" />
                  <span>Core Contributor • PR #6</span>
                </div>
              </div>

              {/* Bio & Contribution details */}
              <p className="text-slate-300 text-sm leading-relaxed mb-5">
                Arsitek di balik perombakan grafis besar-besaran di <strong>PR #6 (feat: pixel-perfect renderers)</strong>. Menghapuskan dependency browser mock dengan mesin rendering native yang menghasilkan screenshot IDE resmi tanpa artefak web slop.
              </p>

              {/* Key Contributions List */}
              <div className="space-y-2.5 mb-6 text-xs text-slate-300">
                <div className="flex items-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-purple-400 shrink-0 mt-0.5" />
                  <span>
                    <strong>Apache NetBeans Native Engine:</strong> Mengintegrasikan <code className="text-purple-300 font-mono">javac</code> AST Compiler Tree API + FlatLaf Light + subpixel <code className="text-purple-300 font-mono">LCD_HRGB</code> antialiasing.
                  </span>
                </div>
                <div className="flex items-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-purple-400 shrink-0 mt-0.5" />
                  <span>
                    <strong>Code::Blocks wxScintilla Engine:</strong> Membangun adapter C++ styled text dengan <code className="text-purple-300 font-mono">lexer_cpp.xml</code> dan Win32 GDI font renderer otentik.
                  </span>
                </div>
                <div className="flex items-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-purple-400 shrink-0 mt-0.5" />
                  <span>
                    <strong>Dual Viewport System:</strong> Menciptakan arsitektur <code className="text-purple-300 font-mono">--view editor</code> (slice kode fokus) vs <code className="text-purple-300 font-mono">--view full</code> (jendela workspace lengkap).
                  </span>
                </div>
                <div className="flex items-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-purple-400 shrink-0 mt-0.5" />
                  <span>
                    <strong>Sample Dataset Regeneration:</strong> Meregenerasi seluruh dataset contoh ADPL dan Struktur Data modul kampus.
                  </span>
                </div>
              </div>
            </div>

            {/* Tags and Profile Button */}
            <div className="pt-4 border-t border-white/10 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div className="flex flex-wrap gap-1.5">
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-purple-500/10 text-purple-300 border border-purple-500/20">Java2D</span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-purple-500/10 text-purple-300 border border-purple-500/20">wxScintilla</span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-white/5 text-slate-300 border border-white/5">Win32 GDI</span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-white/5 text-slate-300 border border-white/5">PR #6</span>
              </div>
              <a
                href="https://github.com/alexanderfrit"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1.5 text-xs font-semibold text-purple-300 hover:text-white transition-colors"
              >
                <span>Lihat Profil GitHub</span>
                <ExternalLink className="w-3 h-3" />
              </a>
            </div>
          </div>

          {/* Card 2: Satria Bakti Wijaya (Creator & Lead) - Col 5 */}
          <div className="lg:col-span-5 rounded-3xl bg-[#0D0F18]/90 border border-white/10 hover:border-indigo-500/40 p-6 sm:p-8 relative overflow-hidden transition-all duration-300 shadow-xl shadow-black/40 group flex flex-col justify-between">
            {/* Top decorative gradient bar */}
            <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-indigo-500 to-teal-400" />

            <div>
              {/* Header with Avatar & Badge */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
                <div className="flex items-center gap-4">
                  <div className="relative">
                    <img
                      src="https://github.com/SatriaBaktiWijaya.png"
                      alt="Satria Bakti Wijaya"
                      onError={(e) => {
                        e.currentTarget.src = 'https://ui-avatars.com/api/?name=Satria+Bakti&background=4f46e5&color=fff'
                      }}
                      className="w-16 h-16 rounded-2xl border-2 border-indigo-500/40 shadow-lg shadow-indigo-950/50 object-cover"
                    />
                    <div className="absolute -bottom-1 -right-1 p-1 rounded-lg bg-[#090A0F] border border-indigo-500/40 text-indigo-300">
                      <Code2 className="w-3.5 h-3.5" />
                    </div>
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-white tracking-tight">Satria Bakti Wijaya</h3>
                    <a
                      href="https://github.com/SatriaBaktiWijaya"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 text-xs text-slate-400 hover:text-indigo-300 font-mono transition-colors"
                    >
                      <GithubIcon className="w-3 h-3" />
                      <span>@SatriaBaktiWijaya</span>
                      <ExternalLink className="w-2.5 h-2.5 opacity-60" />
                    </a>
                  </div>
                </div>

                <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-500/15 border border-indigo-500/30 text-indigo-300 text-xs font-mono font-semibold self-start sm:self-auto shadow-sm">
                  <span>Creator & Lead Maintainer</span>
                </div>
              </div>

              {/* Bio & Responsibilities */}
              <p className="text-slate-300 text-sm leading-relaxed mb-5">
                Penggagas dan arsitek inti framework <strong>NgeLaprak</strong>. Merancang pipeline otonom 2-berkas (Modul + Template) yang menyulap materi praktikum menjadi berkas DOCX & PDF resmi standar akademik.
              </p>

              {/* Responsibilities list */}
              <div className="space-y-2.5 mb-6 text-xs text-slate-300">
                <div className="flex items-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-indigo-400 shrink-0 mt-0.5" />
                  <span>
                    <strong>Framework Architecture:</strong> Sistem otomasi modular untuk agen AI (Claude Code, Antigravity, Cursor, Cline).
                  </span>
                </div>
                <div className="flex items-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-indigo-400 shrink-0 mt-0.5" />
                  <span>
                    <strong>Docx & PDF Compiler:</strong> Engine layout Word berpresisi tinggi dengan margin kampus dan tabel evaluasi.
                  </span>
                </div>
                <div className="flex items-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-indigo-400 shrink-0 mt-0.5" />
                  <span>
                    <strong>Interactive Showcase:</strong> Website dokumentasi dan ekosistem visual interaktif NgeLaprak.
                  </span>
                </div>
              </div>
            </div>

            {/* Links */}
            <div className="pt-4 border-t border-white/10 flex items-center justify-between gap-3">
              <a
                href="https://saweria.co/satriabaktiwijaya"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1.5 text-xs font-semibold text-amber-300 hover:text-amber-200 transition-colors"
              >
                <Coffee className="w-3.5 h-3.5 text-amber-400" />
                <span>Traktir Kopi di Saweria</span>
              </a>
              <a
                href="https://github.com/SatriaBaktiWijaya"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1.5 text-xs font-semibold text-indigo-300 hover:text-white transition-colors"
              >
                <span>GitHub Profile</span>
                <ExternalLink className="w-3 h-3" />
              </a>
            </div>
          </div>
        </div>

        {/* Open Source Call to Action Card */}
        <div className="rounded-2xl bg-[#0D0F18]/80 border border-white/10 p-6 sm:p-8 flex flex-col md:flex-row items-center justify-between gap-6 shadow-lg shadow-black/30">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center text-slate-300 shrink-0">
              <GitPullRequest className="w-6 h-6 text-indigo-400" />
            </div>
            <div>
              <h4 className="text-base sm:text-lg font-bold text-white mb-1">
                Ingin Menjadi Kontributor NgeLaprak?
              </h4>
              <p className="text-slate-400 text-xs sm:text-sm max-w-2xl leading-relaxed">
                Punya template kampusmu sendiri, ide renderer IDE baru (seperti Dev-C++, Eclipse, IntelliJ IDEA), atau optimasi format laporan? Kami sangat menyambut kontribusi kode, ide, maupun pelaporan bug.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3 shrink-0 w-full sm:w-auto">
            <a
              href="https://github.com/SatriaBaktiWijaya/NgeLaprak/issues"
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 sm:flex-none inline-flex items-center justify-center gap-2 px-4 py-2 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 text-xs font-semibold text-slate-300 hover:text-white transition-all active:scale-95"
            >
              <span>Laporkan Isu</span>
            </a>
            <a
              href="https://github.com/SatriaBaktiWijaya/NgeLaprak/pulls"
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 sm:flex-none inline-flex items-center justify-center gap-2 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 border border-indigo-400/30 text-xs font-semibold text-white shadow-md shadow-indigo-600/30 transition-all active:scale-95"
            >
              <GitFork className="w-3.5 h-3.5 text-indigo-200" />
              <span>Kirim Pull Request</span>
            </a>
          </div>
        </div>
      </div>
    </section>
  )
}
