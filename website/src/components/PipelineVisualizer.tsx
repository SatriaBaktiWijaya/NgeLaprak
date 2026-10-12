import React, { useState } from 'react'
import { FileCode, FileText, LayoutTemplate, Sparkles, CheckCircle2, FileType, Check, Eye } from 'lucide-react'

export const PipelineVisualizer: React.FC = () => {
  const [selectedInput, setSelectedInput] = useState<number>(0)

  const inputs = [
    {
      id: 0,
      title: '1. Source Code',
      badge: 'Wajib',
      badgeColor: 'text-indigo-400 bg-indigo-500/10 border-indigo-500/20',
      ext: '.java / .cpp / .py / .sql',
      desc: 'Kode tugas praktikum yang sudah dibuat.',
      sampleName: 'GraphTraversal.java / Stack.cpp',
      icon: FileCode,
      color: 'from-blue-500 to-indigo-600'
    },
    {
      id: 1,
      title: '2. Modul / Soal',
      badge: 'Wajib',
      badgeColor: 'text-purple-400 bg-purple-500/10 border-purple-500/20',
      ext: '.pdf / .txt / .docx',
      desc: 'Petunjuk praktikum dan soal evaluasi dosen.',
      sampleName: 'Modul_03_Struktur_Data.pdf',
      icon: FileText,
      color: 'from-purple-500 to-pink-600'
    },
    {
      id: 2,
      title: '3. Template Word',
      badge: 'Opsional',
      badgeColor: 'text-amber-400 bg-amber-500/10 border-amber-500/20',
      ext: '.docx / Standar Otomatis',
      desc: 'Template format laporan kampus/lab kamu.',
      sampleName: 'Template_Laprak_LabSI.docx',
      icon: LayoutTemplate,
      color: 'from-amber-500 to-orange-600'
    }
  ]

  const engineSteps = [
    'Deteksi otomatis mata kuliah & struktur modul',
    'Restrukturisasi folder standar (NetBeans / C++)',
    'Render screenshot IDE autentik tanpa watermark',
    'Penulisan pembahasan baris-per-baris gaya mahasiswa',
    'Kompilasi layout standar 4-4-3-3 ke Word & PDF'
  ]

  return (
    <section id="pipeline" className="py-16 md:py-24 relative overflow-hidden bg-[#090C16]">
      {/* Background ambient lighting */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[300px] bg-indigo-600/10 blur-[120px] rounded-full pointer-events-none" />

      <div className="max-w-6xl mx-auto px-4 sm:px-6 relative z-10">
        {/* Section Header */}
        <div className="text-center max-w-2xl mx-auto mb-12 md:mb-16">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-semibold mb-3">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Alur Otomatisasi</span>
          </div>
          <h2 className="text-2xl sm:text-3xl md:text-4xl font-extrabold text-white tracking-tight mb-3 font-sans">
            Cukup <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">3 File</span>, Sisanya Otomatis
          </h2>
          <p className="text-slate-400 text-xs sm:text-sm md:text-base leading-relaxed">
            Tidak perlu copy-paste teks atau potong screenshot satu per satu. NgeLaprak merakit seluruh laporan secara mandiri.
          </p>
        </div>

        {/* 3-Step Interactive Pipeline Canvas */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 items-stretch">
          {/* STEP 1: Inputs (Col 4) */}
          <div className="lg:col-span-4 flex flex-col gap-3">
            <div className="flex items-center justify-between px-1">
              <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider font-mono">
                [INPUT] TIGA BERKAS
              </span>
              <span className="text-[11px] text-indigo-400">Pilih berkas</span>
            </div>

            {inputs.map((inp) => {
              const Icon = inp.icon
              const isSelected = selectedInput === inp.id
              return (
                <div
                  key={inp.id}
                  onClick={() => setSelectedInput(inp.id)}
                  className={`cursor-pointer p-3.5 rounded-2xl border transition-all duration-200 text-left ${
                    isSelected
                      ? 'bg-[#15192C] border-indigo-500/70 shadow-lg shadow-indigo-500/15 ring-1 ring-indigo-500/30'
                      : 'bg-[#0E111E]/80 border-white/5 hover:border-white/15 hover:bg-[#121626]'
                  }`}
                >
                  <div className="flex items-start gap-3">
                    <div
                      className={`w-9 h-9 rounded-xl bg-gradient-to-br ${inp.color} flex items-center justify-center shrink-0 shadow-md`}
                    >
                      <Icon className="w-4 h-4 text-white" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between gap-1 mb-0.5">
                        <h4 className="font-bold text-white text-xs sm:text-sm tracking-tight truncate">{inp.title}</h4>
                        <span
                          className={`text-[9px] font-mono px-1.5 py-0.2 rounded-full border ${inp.badgeColor}`}
                        >
                          {inp.badge}
                        </span>
                      </div>
                      <p className="text-[11px] text-slate-400 line-clamp-1 mb-1">{inp.desc}</p>
                      <div className="font-mono text-[10px] text-indigo-300/80 bg-black/40 px-2 py-0.5 rounded border border-white/5 truncate">
                        {inp.sampleName}
                      </div>
                    </div>
                  </div>
                </div>
              )
            })}
          </div>

          {/* STEP 2: The Core Engine (Col 4) */}
          <div className="lg:col-span-4 flex flex-col">
            <div className="h-full bg-[#121526] border border-indigo-500/30 rounded-2xl p-5 shadow-2xl relative overflow-hidden backdrop-blur-xl flex flex-col justify-between">
              <div>
                <div className="flex flex-col items-center text-center mb-4">
                  <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-indigo-500 via-purple-600 to-pink-500 flex items-center justify-center mb-2.5 shadow-lg shadow-indigo-500/30">
                    <Sparkles className="w-6 h-6 text-white" />
                  </div>
                  <h3 className="font-bold text-white text-sm sm:text-base font-sans">NgeLaprak Agent Core</h3>
                  <span className="text-[10px] font-mono text-indigo-300">Autonomous Processing Pipeline</span>
                </div>

                {/* Engine Steps Checklist */}
                <div className="space-y-2 text-left">
                  {engineSteps.map((step, idx) => (
                    <div
                      key={idx}
                      className="flex items-start gap-2 text-[11px] text-slate-300 bg-black/30 p-2 rounded-lg border border-white/5"
                    >
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0 mt-0.5" />
                      <span className="leading-tight">{step}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="mt-4 pt-3 border-t border-white/10 flex items-center justify-between text-[11px] text-slate-400 font-mono">
                <span>Waktu Proses: ~15-30 dtk</span>
                <span className="text-emerald-400">● Status: Standby</span>
              </div>
            </div>
          </div>

          {/* STEP 3: The Outputs (Col 4) */}
          <div className="lg:col-span-4 flex flex-col gap-3">
            <div className="flex items-center justify-between px-1">
              <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider font-mono">
                [OUTPUT] SIAP KUMPUL
              </span>
              <span className="text-[11px] text-emerald-400">100% Terformat</span>
            </div>

            {/* Word Card */}
            <div className="p-3.5 rounded-2xl bg-[#0E111E]/80 border border-blue-500/30 hover:border-blue-500/60 transition-all shadow-lg text-left">
              <div className="flex items-start gap-3">
                <div className="w-9 h-9 rounded-xl bg-blue-600/20 border border-blue-500/30 flex items-center justify-center shrink-0 text-blue-400">
                  <FileType className="w-4 h-4 text-blue-400" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between gap-1 mb-0.5">
                    <h4 className="font-bold text-white text-xs sm:text-sm">Dokumen Word (.docx)</h4>
                    <span className="text-[9px] font-mono px-1.5 py-0.2 rounded-full bg-blue-500/10 text-blue-300 border border-blue-500/20">
                      Editable
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-400 mb-1.5">
                    Margin 4-4-3-3, font Times New Roman/Calibri 12pt, spasi 1.5, dan cover otomatis.
                  </p>
                  <div className="flex items-center gap-1.5 text-[10px] font-mono text-slate-400">
                    <Check className="w-3 h-3 text-emerald-400" /> Heading 1, 2, 3 Terstandar
                  </div>
                </div>
              </div>
            </div>

            {/* PDF Card */}
            <div className="p-3.5 rounded-2xl bg-[#0E111E]/80 border border-red-500/30 hover:border-red-500/60 transition-all shadow-lg text-left">
              <div className="flex items-start gap-3">
                <div className="w-9 h-9 rounded-xl bg-red-600/20 border border-red-500/30 flex items-center justify-center shrink-0 text-red-400">
                  <FileText className="w-4 h-4 text-red-400" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between gap-1 mb-0.5">
                    <h4 className="font-bold text-white text-xs sm:text-sm">Dokumen PDF (.pdf)</h4>
                    <span className="text-[9px] font-mono px-1.5 py-0.2 rounded-full bg-red-500/10 text-red-300 border border-red-500/20">
                      Print-Ready
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-400 mb-1.5">
                    Siap upload ke portal e-learning kampus tanpa pergeseran layout atau font missing.
                  </p>
                  <div className="flex items-center gap-1.5 text-[10px] font-mono text-slate-400">
                    <Check className="w-3 h-3 text-emerald-400" /> Vector Sharpness & Standar Lab
                  </div>
                </div>
              </div>
            </div>

            {/* Direct button */}
            <a
              href="#samples"
              className="flex items-center justify-center gap-1.5 py-2.5 px-3 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 text-xs font-semibold text-slate-300 hover:text-white transition-all text-center"
            >
              <Eye className="w-3.5 h-3.5 text-indigo-400" />
              <span>Lihat Contoh Dokumen Hasil</span>
            </a>
          </div>
        </div>
      </div>
    </section>
  )
}
