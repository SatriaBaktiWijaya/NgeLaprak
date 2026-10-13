import React, { useState } from 'react'
import { FileText, Download, Eye, ExternalLink, Sparkles, BookOpen, Check, Layers, FileDown } from 'lucide-react'

export const SampleViewer: React.FC = () => {
  const [activeCourse, setActiveCourse] = useState<'strukdat' | 'adpl'>('strukdat')
  const [activePage, setActivePage] = useState<number>(0)

  const courses = {
    strukdat: {
      name: 'Struktur Data — Modul 3',
      sub: 'Implementasi Stack & Linked List (C++ / Code::Blocks)',
      pagesCount: '12 Halaman',
      pdfUrl: '/samples/strukdat/LAPRAK_SAMPLE_STRUKDAT_MODUL3.pdf',
      docxUrl: '/samples/strukdat/LAPRAK_SAMPLE_STRUKDAT_MODUL3.docx',
      previewImg: '/samples/strukdat/preview_sample.png',
      badge: 'C++ / Algorithm',
      pages: [
        {
          title: 'Halaman Judul & Cover',
          desc: 'Logo universitas berpusat, identitas mahasiswa (Nama & NIM), judul praktikum standar lab.',
          tag: 'Standard Cover'
        },
        {
          title: 'Bab I & II: Teori & Algoritma',
          desc: 'Konsep LIFO Stack, struktur memory heap vs stack, dan kompleksitas waktu O(1) Push/Pop.',
          tag: 'Kajian Pustaka'
        },
        {
          title: 'Bab III: Source Code & IDE Capture',
          desc: 'Header Stack.h, main.cpp, serta screenshot Code::Blocks lengkap console output running.',
          tag: 'Screenshot & Code'
        },
        {
          title: 'Bab IV: Analisis & Kesimpulan',
          desc: 'Evaluasi overflow, edge case handling, dan rangkuman hasil eksekusi program.',
          tag: 'Refleksi Praktikan'
        }
      ]
    },
    adpl: {
      name: 'ADPL — Modul 4',
      sub: 'Aplikasi Kasir Swing GUI & MySQL (Java / Apache NetBeans)',
      pagesCount: '15 Halaman',
      pdfUrl: '/samples/adpl/LAPRAK_SAMPLE_ADPL_MODUL4.pdf',
      docxUrl: '/samples/adpl/LAPRAK_SAMPLE_ADPL_MODUL4.docx',
      previewImg: '/samples/adpl/preview_sample.png',
      badge: 'Java / GUI Database',
      pages: [
        {
          title: 'Cover Resmi Laporan',
          desc: 'Format cover fakultas teknik dengan margin 4-4-3-3 dan tahun akademik berjalan.',
          tag: 'Standard Cover'
        },
        {
          title: 'Bab I & II: Arsitektur MVC & JDBC',
          desc: 'Prinsip koneksi database MySQL, penanganan SQLException, dan alur data Swing form.',
          tag: 'Kajian Pustaka'
        },
        {
          title: 'Bab III: Kode Program & GUI Render',
          desc: 'Form kasir NetBeans, diagram relasi database, dan tangkapan layar antarmuka form kasir.',
          tag: 'Screenshot & Code'
        },
        {
          title: 'Bab IV: Kesimpulan & Evaluasi',
          desc: 'Analisis transaksi database, validasi input harga & stok, dan penutup praktikum.',
          tag: 'Refleksi Praktikan'
        }
      ]
    }
  }

  const current = courses[activeCourse]

  return (
    <section id="samples" className="py-24 relative overflow-hidden bg-[#090A0F]">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 relative z-10">
        {/* Header */}
        <div className="text-center max-w-2xl mx-auto mb-16">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-mono uppercase tracking-wider mb-3">
            <BookOpen className="w-3.5 h-3.5" />
            <span>Bukti Fisik Laporan</span>
          </div>
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-white tracking-[-0.035em] mb-4 font-sans [text-wrap:balance]">
            Inspeksi Dokumen Hasil{' '}
            <span className="text-indigo-400">Secara Nyata</span>
          </h2>
          <p className="text-slate-400 text-sm sm:text-base leading-relaxed [text-wrap:pretty]">
            Unduh atau intip langsung berkas Word dan PDF yang dihasilkan skill ini pada modul praktikum mahasiswa sesungguhnya.
          </p>
        </div>

        {/* Course Switcher */}
        <div className="flex justify-center mb-8">
          <div className="inline-flex p-1.5 rounded-2xl bg-[#0D0F18] border border-white/10 shadow-inner">
            <button
              onClick={() => {
                setActiveCourse('strukdat')
                setActivePage(0)
              }}
              className={`px-4 sm:px-6 py-2.5 rounded-xl text-xs sm:text-sm font-semibold transition-all active:scale-[0.98] ${
                activeCourse === 'strukdat'
                  ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/30'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              C++ Struktur Data (Modul 3)
            </button>
            <button
              onClick={() => {
                setActiveCourse('adpl')
                setActivePage(0)
              }}
              className={`px-4 sm:px-6 py-2.5 rounded-xl text-xs sm:text-sm font-semibold transition-all active:scale-[0.98] ${
                activeCourse === 'adpl'
                  ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/30'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Java PBO / ADPL (Modul 4)
            </button>
          </div>
        </div>

        {/* Preview Container */}
        <div className="rounded-3xl bg-[#0D0F18] border border-white/10 p-6 sm:p-8 shadow-2xl shadow-[inset_0_1px_0_rgba(255,255,255,0.06)]">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
            {/* Left: Document Info & Page Navigator (Col 5) */}
            <div className="lg:col-span-5 flex flex-col justify-between h-full">
              <div>
                <div className="flex items-center gap-2 mb-3">
                  <span className="text-xs font-mono font-bold px-2.5 py-0.5 rounded-full bg-indigo-500/10 text-indigo-300 border border-indigo-500/25">
                    {current.badge}
                  </span>
                  <span className="text-xs text-slate-400 font-mono tabular-nums">{current.pagesCount}</span>
                </div>

                <h3 className="text-2xl font-bold text-white mb-2 tracking-tight">{current.name}</h3>
                <p className="text-xs sm:text-sm text-slate-400 mb-6 [text-wrap:pretty]">{current.sub}</p>

                {/* Page breakdown tabs */}
                <div className="space-y-2 mb-8">
                  {current.pages.map((p, idx) => (
                    <div
                      key={idx}
                      onClick={() => setActivePage(idx)}
                      className={`p-3 rounded-xl border text-left cursor-pointer transition-all active:scale-[0.98] ${
                        activePage === idx
                          ? 'bg-indigo-950/40 border-indigo-500/50 shadow-sm'
                          : 'bg-black/20 border-white/5 hover:border-white/15'
                      }`}
                    >
                      <div className="flex items-center justify-between mb-1">
                        <h4 className="text-xs font-bold text-white">{p.title}</h4>
                        <span className="text-[10px] font-mono text-indigo-300">{p.tag}</span>
                      </div>
                      <p className="text-[11px] text-slate-400 line-clamp-1">{p.desc}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Action buttons: aligned at baseline */}
              <div className="mt-auto flex flex-wrap items-center gap-3 pt-4 border-t border-white/10">
                <a
                  href={current.pdfUrl}
                  download
                  className="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-white/10 hover:bg-white/15 text-white text-xs font-semibold border border-white/10 shadow-md active:scale-[0.98] transition-all text-center focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500"
                >
                  <FileDown className="w-3.5 h-3.5 text-rose-400" />
                  <span>Download .PDF</span>
                </a>
                <a
                  href={current.docxUrl}
                  download
                  className="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-md shadow-indigo-600/30 active:scale-[0.98] transition-all text-center focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500"
                >
                  <Download className="w-3.5 h-3.5 text-white" />
                  <span>Download .DOCX</span>
                </a>
              </div>
            </div>

            {/* Right: Realistic Document Preview Frame (Col 7) */}
            <div className="lg:col-span-7 flex flex-col items-center">
              <div className="w-full rounded-2xl bg-black/60 border border-white/10 p-3 sm:p-4 shadow-2xl relative group shadow-[inset_0_1px_0_rgba(255,255,255,0.06)]">
                <div className="rounded-xl overflow-hidden bg-[#141724] relative flex items-center justify-center min-h-[380px]">
                  <img
                    src={current.previewImg}
                    alt="Document Sample Preview"
                    className="w-full max-h-[460px] object-contain rounded-lg transition-transform duration-300 group-hover:scale-[1.01]"
                    loading="lazy"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent pointer-events-none" />
                  <div className="absolute bottom-3 left-3 right-3 flex items-center justify-between text-xs text-slate-300 px-3 py-2 rounded-lg bg-black/80 backdrop-blur-md border border-white/10 font-mono">
                    <span className="flex items-center gap-1.5">
                      <Check className="w-3.5 h-3.5 text-emerald-400" />
                      {current.pages[activePage].title}
                    </span>
                    <a
                      href={current.pdfUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-indigo-300 hover:text-white flex items-center gap-1 font-sans"
                    >
                      Buka PDF <ExternalLink className="w-3 h-3" />
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
