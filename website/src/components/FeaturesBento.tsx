import React, { useState } from 'react'
import {
  FolderGit2,
  ShieldCheck,
  Camera,
  FileCheck2,
  Cpu,
  Sparkles,
  Check,
  Layers,
  GraduationCap,
  Image as ImageIcon,
  TerminalSquare,
  BookOpenCheck
} from 'lucide-react'

export const FeaturesBento: React.FC = () => {
  const [activeCampus, setActiveCampus] = useState(0)

  const campusList = [
    { name: 'Universitas Indonesia', faculty: 'Fakultas Ilmu Komputer', city: 'Depok', badge: 'Cover Standar UI' },
    { name: 'Institut Teknologi Bandung', faculty: 'Sekolah Teknik Elektro dan Informatika', city: 'Bandung', badge: 'Format STEI' },
    { name: 'Universitas Gadjah Mada', faculty: 'Fakultas MIPA / Ilmu Komputer', city: 'Yogyakarta', badge: 'Standar Lab UGM' },
    { name: 'Telkom University', faculty: 'Fakultas Informatika', city: 'Purwokerto & Bandung', badge: 'Format Resmi Tel-U' }
  ]

  return (
    <section id="features" className="py-24 relative overflow-hidden bg-[#090A0F]">
      {/* Subtle backdrop glow */}
      <div className="absolute top-1/3 left-1/2 -translate-x-1/2 w-[700px] h-[350px] bg-indigo-600/[0.04] blur-[140px] rounded-full pointer-events-none" />

      <div className="max-w-6xl mx-auto px-4 sm:px-6 relative z-10">
        {/* Section Header */}
        <div className="text-center max-w-2xl mx-auto mb-16">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-mono uppercase tracking-wider mb-3">
            <Layers className="w-3.5 h-3.5" />
            <span>Kapabilitas Inti Agent</span>
          </div>
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-white tracking-[-0.035em] mb-4 font-sans [text-wrap:balance]">
            Dirancang Khusus Mahasiswa{' '}
            <span className="text-indigo-400 underline decoration-indigo-500/40 decoration-wavy underline-offset-4">
              Ilmu Komputer & Teknik
            </span>
          </h2>
          <p className="text-slate-400 text-sm sm:text-base leading-relaxed [text-wrap:pretty]">
            Bukan sekadar chatbot teks umum. NgeLaprak adalah autonomous compiler yang memahami struktur proyek IDE, standar laboratorium kampus, dan etika penulisan laporan ilmiah.
          </p>
        </div>

        {/* Bento Grid */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-5">
          {/* Card 1: Multi-Campus Adaptive Cover Engine (Col 7) */}
          <div className="md:col-span-7 rounded-3xl bg-[#0D0F18] border border-white/8 hover:border-indigo-500/30 p-6 sm:p-8 relative overflow-hidden transition-all duration-300 group shadow-xl shadow-black/40 shadow-[inset_0_1px_0_rgba(255,255,255,0.06)] flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-6">
                <div className="w-11 h-11 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 group-hover:scale-105 transition-transform">
                  <GraduationCap className="w-5 h-5" />
                </div>
                <span className="text-[11px] font-mono text-indigo-300/80 bg-indigo-950/40 px-2.5 py-1 rounded-full border border-indigo-800/40 tabular-nums">
                  Multi-Campus Adaptive
                </span>
              </div>

              <div className="mb-2">
                <span className="text-[11px] font-mono uppercase tracking-wider text-indigo-400 font-semibold">
                  Universal Institution Detection
                </span>
              </div>
              <h3 className="text-xl sm:text-2xl font-bold text-white mb-3 tracking-[-0.025em]">
                Adaptasi Format Cover Semua Kampus
              </h3>
              <p className="text-slate-400 text-sm leading-relaxed mb-6 [text-wrap:pretty]">
                Agent secara cerdas mendeteksi identitas universitas, fakultas, dan program studi dari modul praktikum atau template PDF/Word apapun (UI, ITB, UGM, ITS, Telkom University, UNDIP, UNAIR), lalu menyesuaikan tata letak halaman sampul secara presisi.
              </p>
            </div>

            {/* Interactive Campus Selector Pills */}
            <div className="rounded-2xl bg-[#08090F] border border-white/5 p-4 shadow-inner">
              <div className="text-[11px] font-mono text-slate-400 mb-2 flex items-center justify-between">
                <span>Contoh Deteksi Universitas:</span>
                <span className="text-emerald-400 font-medium">● Pattern Matcher Active</span>
              </div>
              <div className="grid grid-cols-2 gap-2 mb-3">
                {campusList.map((campus, idx) => (
                  <button
                    key={idx}
                    onClick={() => setActiveCampus(idx)}
                    className={`text-left p-2.5 rounded-xl border transition-all text-xs active:scale-[0.98] ${
                      activeCampus === idx
                        ? 'bg-indigo-950/50 border-indigo-500/50 text-white font-semibold'
                        : 'bg-white/[0.02] border-white/5 text-slate-400 hover:text-white hover:bg-white/[0.04]'
                    }`}
                  >
                    <div className="truncate text-white">{campus.name}</div>
                    <div className="text-[10px] text-slate-400 truncate">{campus.city}</div>
                  </button>
                ))}
              </div>
              <div className="p-2.5 rounded-lg bg-black/40 border border-white/5 text-[11px] font-mono text-slate-300 flex items-center justify-between">
                <span className="text-slate-400">Layout Terpilih:</span>
                <span className="text-indigo-300 font-medium">{campusList[activeCampus].badge} — {campusList[activeCampus].faculty}</span>
              </div>
            </div>
          </div>

          {/* Card 2: Auto PDF Logo Extraction (Col 5) */}
          <div className="md:col-span-5 rounded-3xl bg-[#0D0F18] border border-white/8 hover:border-indigo-500/30 p-6 sm:p-8 relative overflow-hidden transition-all duration-300 group shadow-xl shadow-black/40 shadow-[inset_0_1px_0_rgba(255,255,255,0.06)] flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-6">
                <div className="w-11 h-11 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 group-hover:scale-105 transition-transform">
                  <ImageIcon className="w-5 h-5" />
                </div>
                <span className="text-[11px] font-mono text-slate-400 bg-white/5 px-2.5 py-1 rounded-full border border-white/10">
                  extract_cover_logo_from_pdf
                </span>
              </div>

              <span className="text-[11px] font-mono uppercase tracking-wider text-indigo-400 font-semibold mb-2 block">
                Automatic Logo Harvester
              </span>
              <h3 className="text-xl sm:text-2xl font-bold text-white mb-3 tracking-[-0.025em]">
                Ekstraksi Logo Kampus dari PDF Asli
              </h3>
              <p className="text-slate-400 text-sm leading-relaxed mb-6 [text-wrap:pretty]">
                Punya contoh laprak PDF dari aslab? Skill akan otomatis mengekstrak logo instansi langsung dari berkas referensi tanpa perlu mencari file PNG logo di internet.
              </p>
            </div>

            <div className="p-4 rounded-2xl bg-[#08090F] border border-white/5 font-mono text-xs text-slate-300 space-y-2.5">
              <div className="flex items-center gap-2 text-indigo-300">
                <Check className="w-4 h-4 text-emerald-400 shrink-0" />
                <span>Ekstrak gambar vektor & bitmap resolusi tinggi</span>
              </div>
              <div className="flex items-center gap-2 text-slate-400">
                <Check className="w-4 h-4 text-emerald-400 shrink-0" />
                <span>Auto-crop rasio aspek 1:1 tanpa distorsi gepeng</span>
              </div>
              <div className="flex items-center gap-2 text-slate-400">
                <Check className="w-4 h-4 text-emerald-400 shrink-0" />
                <span>Otomatis di-embed ke halaman cover Word & PDF</span>
              </div>
            </div>
          </div>

          {/* Card 3: Interactive CLI Runner Simulator (Col 5) */}
          <div className="md:col-span-5 rounded-3xl bg-[#0D0F18] border border-white/8 hover:border-indigo-500/30 p-6 sm:p-8 relative overflow-hidden transition-all duration-300 group shadow-xl shadow-black/40 shadow-[inset_0_1px_0_rgba(255,255,255,0.06)] flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-6">
                <div className="w-11 h-11 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 group-hover:scale-105 transition-transform">
                  <TerminalSquare className="w-5 h-5" />
                </div>
                <span className="text-[11px] font-mono text-slate-400 bg-white/5 px-2.5 py-1 rounded-full border border-white/10">
                  cli_simulator.py
                </span>
              </div>

              <span className="text-[11px] font-mono uppercase tracking-wider text-indigo-400 font-semibold mb-2 block">
                Interactive Program Runner
              </span>
              <h3 className="text-xl sm:text-2xl font-bold text-white mb-3 tracking-[-0.025em]">
                Simulasi Input Interaktif Console
              </h3>
              <p className="text-slate-400 text-sm leading-relaxed mb-6 [text-wrap:pretty]">
                Program praktikum punya menu pilihan berulang? Agent mengeksekusi skenario input bertahap sehingga screenshot terminal tampak seperti dijalankan langsung oleh mahasiswa.
              </p>
            </div>

            <div className="rounded-xl bg-[#08090F] border border-white/5 p-3.5 font-mono text-[11px] text-slate-300 space-y-1 shadow-inner">
              <div className="text-slate-500">// Simulasi Menu Bertahap</div>
              <div className="text-slate-300">Pilih menu [1-4]: <span className="text-amber-400 font-bold">1</span></div>
              <div className="text-slate-300">Masukkan nilai node: <span className="text-amber-400 font-bold">42</span></div>
              <div className="text-emerald-400">[OK] Node 42 berhasil ditambahkan!</div>
              <div className="text-slate-300">Pilih menu [1-4]: <span className="text-amber-400 font-bold">3</span></div>
              <div className="text-indigo-300">Display: [Root: 42] -&gt; Left: NULL, Right: NULL</div>
            </div>
          </div>

          {/* Card 4: Authentic IDE Renderers & Anti-Plagiat (Col 7) */}
          <div className="md:col-span-7 rounded-3xl bg-[#0D0F18] border border-white/8 hover:border-indigo-500/30 p-6 sm:p-8 relative overflow-hidden transition-all duration-300 group shadow-xl shadow-black/40 shadow-[inset_0_1px_0_rgba(255,255,255,0.06)] flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-6">
                <div className="w-11 h-11 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 group-hover:scale-105 transition-transform">
                  <Camera className="w-5 h-5" />
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-[11px] font-mono text-emerald-400 bg-emerald-950/40 px-2 py-0.5 rounded-full border border-emerald-800/40">
                    NetBeans • Code::Blocks • VS Code • DBeaver
                  </span>
                </div>
              </div>

              <div className="flex items-center gap-2 mb-2">
                <span className="text-[11px] font-mono uppercase tracking-wider text-indigo-400 font-semibold">
                  Dual Output & Industrial Standards
                </span>
              </div>
              <h3 className="text-xl sm:text-2xl font-bold text-white mb-3 tracking-[-0.025em]">
                Struktur Proyek Resmi + Dual Output .docx & .pdf
              </h3>
              <p className="text-slate-400 text-sm leading-relaxed mb-6 [text-wrap:pretty]">
                Menghasilkan struktur repositori standar (NetBeans Maven, C++ include/src) dan dua dokumen sekaligus: Word (.docx) untuk suntingan bebas, dan PDF (.pdf) siap kumpul dengan margin standar 4-4-3-3 dan penomoran Romawi/Arab otomatis.
              </p>
            </div>

            {/* Micro visual: Directory Tree & Output Checks */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs text-slate-300 font-mono">
              <div className="p-3 rounded-xl bg-[#08090F] border border-white/5 space-y-1">
                <div className="text-indigo-400 font-semibold flex items-center gap-1.5">
                  <FolderGit2 className="w-3.5 h-3.5" />
                  <span>Project Scaffold</span>
                </div>
                <div className="text-slate-400 text-[11px]">📁 src/main/java/</div>
                <div className="text-slate-400 text-[11px]">📁 screenshots/ (auto-capture)</div>
                <div className="text-slate-400 text-[11px]">📄 pom.xml / CMakeLists.txt</div>
              </div>

              <div className="p-3 rounded-xl bg-[#08090F] border border-white/5 space-y-1">
                <div className="text-emerald-400 font-semibold flex items-center gap-1.5">
                  <BookOpenCheck className="w-3.5 h-3.5" />
                  <span>Standard Lab Layout</span>
                </div>
                <div className="text-slate-400 text-[11px]">✓ Margin 4-4-3-3 Presisi</div>
                <div className="text-slate-400 text-[11px]">✓ Romawi (i, ii) & Arab (1, 2)</div>
                <div className="text-slate-400 text-[11px]">✓ Pembahasan gaya mahasiswa</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
