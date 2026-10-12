import React, { useState } from 'react'
import { FileText, Download, Eye, ExternalLink, Sparkles, BookOpen, Check, Layers } from 'lucide-react'

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
    <section id="samples" className="py-24 relative overflow-hidden bg-[#0A0C14]">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 relative z-10">
        {/* Header */}
        <div className="text-center max-w-2xl mx-auto mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-semibold mb-3">
            <BookOpen className="w-3.5 h-3.5" />
            <span>Bukti Fisik Laporan</span>
          </div>
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-white tracking-tight mb-4 font-sans">
            Inspeksi Dokumen Hasil{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">
              Secara Nyata
            </span>
          </h2>
          <p className="text-slate-400 text-sm sm:text-base leading-relaxed">
            Unduh atau intip langsung dokumen Word dan PDF yang dihasilkan skill ini pada modul praktikum sesungguhnya.
          </p>
        </div>

        {/* Course Switcher */}
        <div className="flex justify-center mb-8">
          <div className="inline-flex p-1.5 rounded-2xl bg-[#121524] border border-white/10">
            <button
              onClick={() => {
                setActiveCourse('strukdat')
                setActivePage(0)
              }}
              className={`px-4 sm:px-6 py-2.5 rounded-xl text-xs sm:text-sm font-semibold transition-all ${
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
              className={`px-4 sm:px-6 py-2.5 rounded-xl text-xs sm:text-sm font-semibold transition-all ${
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
        <div className="rounded-3xl bg-[#0F1221] border border-white/10 p-6 sm:p-8 shadow-2xl">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
            {/* Left: Document Info & Page Navigator (Col 5) */}
            <div className="lg:col-span-5 flex flex-col justify-between">
              <div>
                <div className="flex items-center gap-2 mb-3">
                  <span className="text-xs font-mono font-bold px-2.5 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                    {current.badge}
                  </span>
                  <span className="text-xs text-slate-400 font-mono">{current.pagesCount}</span>
                </div>

                <h3 className="text-2xl font-bold text-white mb-2">{current.name}</h3>
                <p className="text-xs sm:text-sm text-slate-400 mb-6">{current.sub}</p>

                {/* Page breakdown tabs */}
                <div className="space-y-2 mb-8">
                  {current.pages.map((p, idx) => (
                    <div
                      key={idx}
                      onClick={() => setActivePage(idx)}
                      className={`p-3 rounded-xl border text-left cursor-pointer transition-all ${
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

              {/* Action buttons */}
              <div className="flex flex-wrap items-center gap-3 pt-4 border-t border-white/10">
                <a
                  href={current.pdfUrl}
                  download
                  className="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-red-600/90 hover:bg-red-500 text-white text-xs font-bold shadow-lg shadow-red-600/25 transition-all text-center"
                >
                  <Download className="w-3.5 h-3.5" />
                  <span>Download .PDF</span>
                </a>
                <a
                  href={current.docxUrl}
                  download
                  className="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-blue-600/90 hover:bg-blue-500 text-white text-xs font-bold shadow-lg shadow-blue-600/25 transition-all text-center"
                >
                  <Download className="w-3.5 h-3.5" />
                  <span>Download .DOCX</span>
                </a>
              </div>
            </div>

            {/* Right: Realistic Document Preview Frame (Col 7) */}
            <div className="lg:col-span-7 flex flex-col items-center">
              <div className="w-full rounded-2xl bg-black/60 border border-white/10 p-3 sm:p-4 shadow-2xl relative group">
                <div className="rounded-xl overflow-hidden bg-[#1A1D2B] relative flex items-center justify-center min-h-[380px]">
                  <img
                    src={current.previewImg}
                    alt="Document Sample Preview"
                    className="w-full max-h-[460px] object-contain rounded-lg transition-transform duration-300 group-hover:scale-[1.02]"
                    loading="lazy"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent pointer-events-none" />
                  <div className="absolute bottom-3 left-3 right-3 flex items-center justify-between text-xs text-slate-300 px-3 py-2 rounded-lg bg-black/70 backdrop-blur-md border border-white/10 font-mono">
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
