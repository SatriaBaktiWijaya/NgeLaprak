import React, { useState } from 'react'
import {
  FolderGit2,
  Camera,
  Layers,
  GraduationCap,
  Image as ImageIcon,
  TerminalSquare,
  BookOpenCheck,
  Check
} from 'lucide-react'
import { ImageDithering } from '@paper-design/shaders-react'

export const FeaturesBento: React.FC = () => {
  const [activeCampus, setActiveCampus] = useState(0)

  const campusList = [
    { name: 'Universitas Indonesia', city: 'Depok' },
    { name: 'Institut Teknologi Bandung', city: 'Bandung' },
    { name: 'Universitas Gadjah Mada', city: 'Yogyakarta' },
    { name: 'Telkom University', city: 'Bandung & Purwokerto' }
  ]

  return (
    <section id="features" className="py-20 md:py-28 relative overflow-hidden bg-[#090A0F]">
      {/* Dynamic Image Dithering Shader Background with University Laboratory Photo */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none select-none z-0">
        <ImageDithering
          width="100%"
          height="100%"
          image="/images/campus_lab.jpg"
          colorBack="#090a0f"
          colorFront="#6366f1"
          colorHighlight="#818cf8"
          originalColors={false}
          inverted={false}
          type="8x8"
          size={2}
          colorSteps={2}
          fit="cover"
          className="w-full h-full opacity-25 md:opacity-35"
        />
        {/* Soft radial vignette & vertical gradient overlay to guarantee card legibility */}
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(9,10,15,0.4)_0%,transparent_60%,#090A0F_90%)]" />
        <div className="absolute inset-0 bg-gradient-to-b from-[#090A0F]/80 via-transparent to-[#090A0F]" />
      </div>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 relative z-10">
        {/* Section Header */}
        <div className="text-center max-w-2xl mx-auto mb-14">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-mono uppercase tracking-wider mb-3">
            <Layers className="w-3.5 h-3.5" />
            <span>Fitur Unggulan</span>
          </div>
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-white tracking-[-0.035em] mb-3 font-sans [text-wrap:balance]">
            Kemampuan Khusus <span className="text-indigo-400">Laboratorium Kampus</span>
          </h2>
          <p className="text-slate-400 text-sm sm:text-base leading-relaxed [text-wrap:pretty]">
            Compiler cerdas yang dirancang untuk standar laporan ilmiah dan format praktikum.
          </p>
        </div>

        {/* Bento Grid */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-5">
          {/* Card 1: Multi-Campus Adaptive Cover Engine (Col 7) */}
          <div className="md:col-span-7 rounded-3xl bg-[#0D0F18]/85 backdrop-blur-md border border-white/8 hover:border-indigo-500/30 p-6 sm:p-7 relative overflow-hidden transition-all duration-300 group shadow-xl shadow-black/40 flex flex-col justify-between">
            <div>
              <div className="w-10 h-10 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 mb-5">
                <GraduationCap className="w-5 h-5" />
              </div>

              <h3 className="text-xl sm:text-2xl font-bold text-white mb-2 tracking-tight">
                Adaptasi Cover Semua Kampus
              </h3>
              <p className="text-slate-400 text-sm leading-relaxed mb-5 [text-wrap:pretty]">
                Mendeteksi identitas universitas, fakultas, dan program studi dari modul/template, lalu menyusun halaman sampul resmi secara otomatis.
              </p>
            </div>

            {/* Clean Campus Selector */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 mt-auto">
              {campusList.map((campus, idx) => (
                <button
                  key={idx}
                  onClick={() => setActiveCampus(idx)}
                  className={`text-left p-2.5 rounded-xl border transition-all text-xs cursor-pointer ${
                    activeCampus === idx
                      ? 'bg-indigo-600/20 border-indigo-500/50 text-white font-semibold'
                      : 'bg-black/30 border-white/5 text-slate-400 hover:text-white'
                  }`}
                >
                  <div className="truncate text-white font-medium">{campus.name}</div>
                  <div className="text-[10px] text-slate-500 truncate">{campus.city}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Card 2: Auto PDF Logo Extraction (Col 5) */}
          <div className="md:col-span-5 rounded-3xl bg-[#0D0F18]/85 backdrop-blur-md border border-white/8 hover:border-indigo-500/30 p-6 sm:p-7 relative overflow-hidden transition-all duration-300 group shadow-xl shadow-black/40 flex flex-col justify-between">
            <div>
              <div className="w-10 h-10 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 mb-5">
                <ImageIcon className="w-5 h-5" />
              </div>

              <h3 className="text-xl sm:text-2xl font-bold text-white mb-2 tracking-tight">
                Ekstraksi Logo Kampus dari PDF
              </h3>
              <p className="text-slate-400 text-sm leading-relaxed mb-5 [text-wrap:pretty]">
                Mengekstrak logo resmi langsung dari modul referensi tanpa perlu mencari gambar terpisah di Google.
              </p>
            </div>

            <div className="p-3.5 rounded-xl bg-black/40 border border-white/5 text-xs text-slate-300 space-y-2 mt-auto font-mono">
              <div className="flex items-center gap-2 text-indigo-300">
                <Check className="w-4 h-4 text-emerald-400 shrink-0" />
                <span>Resolusi tinggi tanpa distorsi</span>
              </div>
              <div className="flex items-center gap-2 text-slate-400">
                <Check className="w-4 h-4 text-emerald-400 shrink-0" />
                <span>Otomatis di-embed ke Word & PDF</span>
              </div>
            </div>
          </div>

          {/* Card 3: Interactive CLI Runner (Col 5) */}
          <div className="md:col-span-5 rounded-3xl bg-[#0D0F18]/85 backdrop-blur-md border border-white/8 hover:border-indigo-500/30 p-6 sm:p-7 relative overflow-hidden transition-all duration-300 group shadow-xl shadow-black/40 flex flex-col justify-between">
            <div>
              <div className="w-10 h-10 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 mb-5">
                <TerminalSquare className="w-5 h-5" />
              </div>

              <h3 className="text-xl sm:text-2xl font-bold text-white mb-2 tracking-tight">
                Simulasi Input Console Interaktif
              </h3>
              <p className="text-slate-400 text-sm leading-relaxed mb-5 [text-wrap:pretty]">
                Mengeksekusi menu pilihan bertahap pada program tugas praktikum agar output terminal tampak natural.
              </p>
            </div>

            <div className="rounded-xl bg-[#08090F] border border-white/5 p-3 font-mono text-[11px] text-slate-300 space-y-1 mt-auto">
              <div className="text-slate-400">Pilih menu [1-4]: <span className="text-amber-400 font-bold">1</span></div>
              <div className="text-slate-400">Nilai data: <span className="text-amber-400 font-bold">42</span></div>
              <div className="text-emerald-400">[OK] Data berhasil ditambahkan!</div>
            </div>
          </div>

          {/* Card 4: Authentic IDE Renderers & Dual Output (Col 7) */}
          <div className="md:col-span-7 rounded-3xl bg-[#0D0F18]/85 backdrop-blur-md border border-white/8 hover:border-indigo-500/30 p-6 sm:p-7 relative overflow-hidden transition-all duration-300 group shadow-xl shadow-black/40 flex flex-col justify-between">
            <div>
              <div className="w-10 h-10 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 mb-5">
                <Camera className="w-5 h-5" />
              </div>

              <h3 className="text-xl sm:text-2xl font-bold text-white mb-2 tracking-tight">
                Struktur Proyek Resmi &amp; Dual Format
              </h3>
              <p className="text-slate-400 text-sm leading-relaxed mb-5 [text-wrap:pretty]">
                Menghasilkan repositori rapi (NetBeans Maven / C++ CMake) serta 2 dokumen siap pakai: Word (.docx) yang bisa diedit dan PDF (.pdf) standar margin 4-4-3-3.
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 mt-auto font-mono text-xs">
              <div className="p-3 rounded-xl bg-black/40 border border-white/5 text-slate-300">
                <div className="text-indigo-400 font-semibold mb-1 flex items-center gap-1.5">
                  <FolderGit2 className="w-3.5 h-3.5" />
                  <span>Struktur Kode</span>
                </div>
                <div className="text-slate-400 text-[11px]">Maven / NetBeans / CMake</div>
              </div>

              <div className="p-3 rounded-xl bg-black/40 border border-white/5 text-slate-300">
                <div className="text-emerald-400 font-semibold mb-1 flex items-center gap-1.5">
                  <BookOpenCheck className="w-3.5 h-3.5" />
                  <span>Format Standar</span>
                </div>
                <div className="text-slate-400 text-[11px]">Margin 4-4-3-3 &amp; .docx / .pdf</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
