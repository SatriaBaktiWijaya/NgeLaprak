import React from 'react'
import { FolderGit2, ShieldCheck, Camera, FileCheck2, Cpu, Sparkles, Check, Code, Layers } from 'lucide-react'

export const FeaturesBento: React.FC = () => {
  return (
    <section id="features" className="py-24 relative overflow-hidden bg-[#08090E]">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 relative z-10">
        {/* Header */}
        <div className="text-center max-w-2xl mx-auto mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-semibold mb-3">
            <Layers className="w-3.5 h-3.5" />
            <span>Fitur Unggulan</span>
          </div>
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-white tracking-tight mb-4 font-sans">
            Dibangun Spesifik Untuk{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400">
              Praktikum Informatika
            </span>
          </h2>
          <p className="text-slate-400 text-sm sm:text-base leading-relaxed">
            Bukan sekadar AI text generator biasa, melainkan autonomous agent yang memahami lingkungan IDE dan standar lab kampus.
          </p>
        </div>

        {/* Bento Grid */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-5">
          {/* Card 1: Autonomous Scaffold (Col 7) */}
          <div className="md:col-span-7 rounded-3xl bg-[#0F1221] border border-white/8 hover:border-indigo-500/40 p-6 sm:p-8 relative overflow-hidden transition-all duration-300 group shadow-xl">
            <div className="absolute top-0 right-0 w-64 h-64 bg-indigo-600/10 rounded-full blur-3xl pointer-events-none group-hover:bg-indigo-600/20 transition-colors" />

            <div className="w-12 h-12 rounded-2xl bg-indigo-500/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400 mb-6 group-hover:scale-105 transition-transform">
              <FolderGit2 className="w-6 h-6" />
            </div>

            <div className="flex items-center gap-2 mb-2">
              <span className="text-[11px] font-mono uppercase tracking-wider text-indigo-400 font-semibold">
                Project Architecture
              </span>
            </div>
            <h3 className="text-xl sm:text-2xl font-bold text-white mb-3">
              Autonomous Scaffold Standar Industri
            </h3>
            <p className="text-slate-400 text-sm leading-relaxed mb-6">
              Otomatis menyusun struktur folder project Java (Apache NetBeans Maven / Gradle) dan C++ (Modular include/src) agar kode langsung bisa dibuka dan di-build dosen tanpa missing classpath.
            </p>

            {/* Micro visual: Directory Tree */}
            <div className="rounded-xl bg-[#08090F] border border-white/5 p-4 font-mono text-xs text-slate-300 space-y-1.5 shadow-inner">
              <div className="text-indigo-400">📁 praktikum-strukdat/</div>
              <div className="pl-4 text-slate-400">├── 📁 src/main/java/com/kampus/</div>
              <div className="pl-8 text-emerald-400">├── Main.java</div>
              <div className="pl-8 text-emerald-400">└── StackGraph.java</div>
              <div className="pl-4 text-slate-400">├── 📁 screenshots/ (auto-generated)</div>
              <div className="pl-4 text-slate-400">└── 📄 pom.xml / CMakeLists.txt</div>
            </div>
          </div>

          {/* Card 2: Anti-Plagiat Engine (Col 5) */}
          <div className="md:col-span-5 rounded-3xl bg-[#0F1221] border border-white/8 hover:border-purple-500/40 p-6 sm:p-8 relative overflow-hidden transition-all duration-300 group shadow-xl flex flex-col justify-between">
            <div className="absolute top-0 right-0 w-52 h-52 bg-purple-600/10 rounded-full blur-3xl pointer-events-none group-hover:bg-purple-600/20 transition-colors" />

            <div>
              <div className="w-12 h-12 rounded-2xl bg-purple-500/20 border border-purple-500/30 flex items-center justify-center text-purple-400 mb-6 group-hover:scale-105 transition-transform">
                <ShieldCheck className="w-6 h-6" />
              </div>

              <span className="text-[11px] font-mono uppercase tracking-wider text-purple-400 font-semibold mb-2 block">
                Originality & Voice
              </span>
              <h3 className="text-xl sm:text-2xl font-bold text-white mb-3">
                Anti-Plagiat & Student Voice
              </h3>
              <p className="text-slate-400 text-sm leading-relaxed mb-6">
                Menghasilkan pembahasan kode dengan gaya tulisan alami mahasiswa yang kritis dan mendalam, bukan frasa kaku template generator.
              </p>
            </div>

            <div className="p-3.5 rounded-xl bg-purple-950/20 border border-purple-500/20 text-xs text-purple-200">
              <div className="flex items-center gap-2 font-semibold mb-1">
                <Check className="w-4 h-4 text-emerald-400" />
                <span>Simulasi Turnitin Passing Rate 98%</span>
              </div>
              <span className="text-[11px] text-purple-300/80">
                Variasi diksi dan alur logika dinamis per mahasiswa.
              </span>
            </div>
          </div>

          {/* Card 3: Real IDE Screenshot Engine (Col 5) */}
          <div className="md:col-span-5 rounded-3xl bg-[#0F1221] border border-white/8 hover:border-cyan-500/40 p-6 sm:p-8 relative overflow-hidden transition-all duration-300 group shadow-xl flex flex-col justify-between">
            <div className="absolute top-0 right-0 w-52 h-52 bg-cyan-600/10 rounded-full blur-3xl pointer-events-none group-hover:bg-cyan-600/20 transition-colors" />

            <div>
              <div className="w-12 h-12 rounded-2xl bg-cyan-500/20 border border-cyan-500/30 flex items-center justify-center text-cyan-400 mb-6 group-hover:scale-105 transition-transform">
                <Camera className="w-6 h-6" />
              </div>

              <span className="text-[11px] font-mono uppercase tracking-wider text-cyan-400 font-semibold mb-2 block">
                Native Capture
              </span>
              <h3 className="text-xl sm:text-2xl font-bold text-white mb-3">
                Pixel-Perfect IDE Renderer
              </h3>
              <p className="text-slate-400 text-sm leading-relaxed mb-6">
                Rendering otomatis tangkapan layar editor sintaks berwarna tajam dengan frame window macOS/Linux tanpa perlu screenshot manual.
              </p>
            </div>

            <div className="flex items-center gap-2 text-xs font-mono text-cyan-300 bg-cyan-950/30 p-3 rounded-xl border border-cyan-500/20">
              <Sparkles className="w-4 h-4 text-cyan-400 shrink-0" />
              <span>Dukungan NetBeans, Code::Blocks, VS Code, DBeaver</span>
            </div>
          </div>

          {/* Card 4: Dual Output .docx & .pdf (Col 7) */}
          <div className="md:col-span-7 rounded-3xl bg-[#0F1221] border border-white/8 hover:border-emerald-500/40 p-6 sm:p-8 relative overflow-hidden transition-all duration-300 group shadow-xl">
            <div className="absolute top-0 right-0 w-64 h-64 bg-emerald-600/10 rounded-full blur-3xl pointer-events-none group-hover:bg-emerald-600/20 transition-colors" />

            <div className="w-12 h-12 rounded-2xl bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400 mb-6 group-hover:scale-105 transition-transform">
              <FileCheck2 className="w-6 h-6" />
            </div>

            <div className="flex items-center gap-2 mb-2">
              <span className="text-[11px] font-mono uppercase tracking-wider text-emerald-400 font-semibold">
                Multi-Format Compilation
              </span>
            </div>
            <h3 className="text-xl sm:text-2xl font-bold text-white mb-3">
              Dual Output Word (.docx) & PDF (.pdf)
            </h3>
            <p className="text-slate-400 text-sm leading-relaxed mb-6">
              Dua berkas matang sekaligus: Word untuk kamu yang ingin menyunting nama kelompok atau logo lab, dan PDF siap unggah dengan vector clarity yang rapi.
            </p>

            {/* Checklist tags */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs text-slate-300 font-mono">
              <div className="flex items-center gap-2 p-2.5 rounded-lg bg-black/30 border border-white/5">
                <Check className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                <span>Margin 4-4-3-3 Presisi</span>
              </div>
              <div className="flex items-center gap-2 p-2.5 rounded-lg bg-black/30 border border-white/5">
                <Check className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                <span>Nomor Romawi & Arab</span>
              </div>
              <div className="flex items-center gap-2 p-2.5 rounded-lg bg-black/30 border border-white/5">
                <Check className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                <span>Daftar Isi Otomatis</span>
              </div>
              <div className="flex items-center gap-2 p-2.5 rounded-lg bg-black/30 border border-white/5">
                <Check className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                <span>Tabel & Gambar Bernomor</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
