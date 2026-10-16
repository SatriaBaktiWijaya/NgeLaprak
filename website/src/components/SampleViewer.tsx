import React, { useState } from 'react'
import { Download, ExternalLink, BookOpen, FileDown, Code } from 'lucide-react'

export const SampleViewer: React.FC = () => {
  const [activeCourse, setActiveCourse] = useState<'strukdat' | 'adpl'>('strukdat')
  const [activePage, setActivePage] = useState<number>(0)

  const courses = {
    strukdat: {
      name: 'Struktur Data (C++)',
      sub: 'Modul 3 — Stack & Linked List',
      codeUrl: '/samples/strukdat/main.cpp',
      codeName: 'main.cpp',
      pdfUrl: '/samples/strukdat/LAPRAK_SAMPLE_STRUKDAT_MODUL3.pdf',
      docxUrl: '/samples/strukdat/LAPRAK_SAMPLE_STRUKDAT_MODUL3.docx',
      previewImg: '/samples/strukdat/preview_sample.png',
      pages: ['Halaman Cover', 'Landasan Teori', 'Kode & Screenshot IDE', 'Analisis & Kesimpulan']
    },
    adpl: {
      name: 'ADPL / PBO (Java)',
      sub: 'Modul 4 — Swing GUI & MySQL',
      codeUrl: '/samples/adpl/KoneksiDB.java',
      codeName: 'KoneksiDB.java',
      pdfUrl: '/samples/adpl/LAPRAK_SAMPLE_ADPL_MODUL4.pdf',
      docxUrl: '/samples/adpl/LAPRAK_SAMPLE_ADPL_MODUL4.docx',
      previewImg: '/samples/adpl/preview_sample.png',
      pages: ['Cover Laporan', 'Teori MVC & JDBC', 'Kode & Tangkapan Layar GUI', 'Evaluasi & Kesimpulan']
    }
  }

  const current = courses[activeCourse]

  return (
    <section id="samples" className="py-20 md:py-28 relative overflow-hidden bg-[#090A0F]">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 relative z-10">
        {/* Header */}
        <div className="text-center max-w-2xl mx-auto mb-12">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-mono uppercase tracking-wider mb-3">
            <BookOpen className="w-3.5 h-3.5" />
            <span>Dokumen Nyata</span>
          </div>
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-white tracking-[-0.035em] mb-3 font-sans [text-wrap:balance]">
            Inspeksi Dokumen Hasil <span className="text-indigo-400">Word, PDF &amp; Kode</span>
          </h2>
          <p className="text-slate-400 text-sm sm:text-base leading-relaxed [text-wrap:pretty]">
            Lihat langsung berkas laporan yang dihasilkan skill ini pada praktikum mahasiswa sesungguhnya.
          </p>
        </div>

        {/* Course Switcher */}
        <div className="flex justify-center mb-8">
          <div className="inline-flex p-1 rounded-xl bg-[#0D0F18] border border-white/10 shadow-inner">
            <button
              onClick={() => {
                setActiveCourse('strukdat')
                setActivePage(0)
              }}
              className={`px-4 sm:px-6 py-2 rounded-lg text-xs sm:text-sm font-semibold transition-all active:scale-[0.98] cursor-pointer ${
                activeCourse === 'strukdat'
                  ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              C++ Struktur Data
            </button>
            <button
              onClick={() => {
                setActiveCourse('adpl')
                setActivePage(0)
              }}
              className={`px-4 sm:px-6 py-2 rounded-lg text-xs sm:text-sm font-semibold transition-all active:scale-[0.98] cursor-pointer ${
                activeCourse === 'adpl'
                  ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Java PBO / ADPL
            </button>
          </div>
        </div>

        {/* Preview Container */}
        <div className="rounded-3xl bg-[#0D0F18] border border-white/10 p-6 sm:p-8 shadow-2xl">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
            {/* Left Column: Minimal Page Selector & Download */}
            <div className="lg:col-span-5 flex flex-col justify-between h-full">
              <div>
                <h3 className="text-xl sm:text-2xl font-bold text-white mb-1 tracking-tight">{current.name}</h3>
                <p className="text-xs sm:text-sm text-slate-400 mb-6">{current.sub}</p>

                {/* Minimalist page pills */}
                <div className="space-y-2 mb-6">
                  {current.pages.map((title, idx) => (
                    <button
                      key={idx}
                      onClick={() => setActivePage(idx)}
                      className={`w-full p-3 rounded-xl border text-left cursor-pointer transition-all active:scale-[0.98] flex items-center justify-between text-xs ${
                        activePage === idx
                          ? 'bg-indigo-600/20 border-indigo-500/50 text-white font-semibold'
                          : 'bg-black/30 border-white/5 text-slate-400 hover:text-white'
                      }`}
                    >
                      <span>{title}</span>
                      <span className="text-[10px] font-mono text-indigo-400">0{idx + 1}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Action buttons */}
              <div className="grid grid-cols-3 gap-1.5 sm:gap-2 pt-4 border-t border-white/10 text-[10.5px] sm:text-xs">
                <a
                  href={current.codeUrl}
                  download
                  className="flex items-center justify-center gap-1 sm:gap-1.5 px-2 sm:px-3 py-2 sm:py-2.5 rounded-xl bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-300 font-semibold border border-emerald-500/25 transition-all text-center truncate"
                  title={`Unduh ${current.codeName}`}
                >
                  <Code className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                  <span className="truncate">{current.codeName}</span>
                </a>
                <a
                  href={current.pdfUrl}
                  download
                  className="flex items-center justify-center gap-1 sm:gap-1.5 px-2 sm:px-3 py-2 sm:py-2.5 rounded-xl bg-white/5 hover:bg-white/10 text-white font-semibold border border-white/10 transition-all text-center truncate"
                >
                  <FileDown className="w-3.5 h-3.5 text-rose-400 shrink-0" />
                  <span>.PDF</span>
                </a>
                <a
                  href={current.docxUrl}
                  download
                  className="flex items-center justify-center gap-1 sm:gap-1.5 px-2 sm:px-3 py-2 sm:py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold shadow-md shadow-indigo-600/30 transition-all text-center truncate"
                >
                  <Download className="w-3.5 h-3.5 text-white shrink-0" />
                  <span>.DOCX</span>
                </a>
              </div>
            </div>

            {/* Right Column: Clean Document Preview Frame */}
            <div className="lg:col-span-7 flex flex-col items-center">
              <div className="w-full rounded-2xl bg-black/60 border border-white/10 p-3 sm:p-4 shadow-2xl relative group">
                <div className="rounded-xl overflow-hidden bg-[#141724] relative flex items-center justify-center min-h-[360px]">
                  <img
                    src={current.previewImg}
                    alt="Document Sample Preview"
                    className="w-full max-h-[460px] object-contain rounded-lg transition-transform duration-300 group-hover:scale-[1.005]"
                    loading="lazy"
                  />
                  <div className="absolute bottom-3 right-3">
                    <a
                      href={current.pdfUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-xs text-white px-3 py-1.5 rounded-lg bg-black/80 backdrop-blur-md border border-white/15 hover:bg-black flex items-center gap-1.5 font-sans"
                    >
                      <span>Buka PDF Penuh</span>
                      <ExternalLink className="w-3 h-3 text-indigo-400" />
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
