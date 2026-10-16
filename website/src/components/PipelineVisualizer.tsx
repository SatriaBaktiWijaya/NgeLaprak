import React, { useState } from 'react'
import { FileCode, FileText, LayoutTemplate, Sparkles, CheckCircle2, FileType, Check, Eye, ArrowRight } from 'lucide-react'
import { NgeLaprakLogo } from './NgeLaprakLogo'

export const PipelineVisualizer: React.FC = () => {
  const [selectedInput, setSelectedInput] = useState<number>(0)

  const inputs = [
    {
      id: 0,
      title: '1. Source Code',
      badge: 'Wajib',
      ext: '.java / .cpp / .py / .sql',
      desc: 'Kode program tugas atau latihan praktikum yang sudah dibuat.',
      sampleName: 'GraphTraversal.java / Stack.cpp',
      icon: FileCode,
      details: 'Dianalisis AST untuk mendeteksi class, method, kompleksitas algoritma, dan alur eksekusi.',
      exampleSnippet: 'void insertNode(int val) { ... }'
    },
    {
      id: 1,
      title: '2. Modul / Soal',
      badge: 'Wajib',
      ext: '.pdf / .txt / .docx',
      desc: 'Petunjuk praktikum, teori dasar, dan soal evaluasi dosen.',
      sampleName: 'Modul_03_Struktur_Data.pdf',
      icon: FileText,
      details: 'Diekstrak tujuan praktikum, dasar teori, rumusan tugas, dan logo universitas aslinya.',
      exampleSnippet: 'Tujuan: Mahasiswa memahami konsep operasi push & pop pada LIFO Stack...'
    },
    {
      id: 2,
      title: '3. Template Word',
      badge: 'Opsional',
      ext: '.docx / Default Otomatis',
      desc: 'Template format laporan laboratorium kampus kamu.',
      sampleName: 'Template_Laprak_LabSI.docx',
      icon: LayoutTemplate,
      details: 'Jika ada, gaya heading, margin, dan cover disalin persis. Jika nihil, format standar 4-4-3-3 otomatis diterapkan.',
      exampleSnippet: 'Format: Font Times New Roman 12pt, Spasi 1.5, Margin 4-4-3-3 cm'
    }
  ]

  const engineSteps = [
    'Ekstraksi AST kode & deteksi bahasa pemrograman',
    'Deteksi identitas kampus, logo instansi & modul evaluasi',
    'Scaffold struktur folder resmi (NetBeans Maven / C++ modular)',
    'Simulasi CLI & render screenshot IDE resolusi tinggi',
    'Penyusunan bab pembahasan bergaya mahasiswa kritis',
    'Kompilasi dwiformat Word (.docx) & PDF (.pdf)'
  ]

  return (
    <section id="pipeline" className="py-20 md:py-28 relative overflow-hidden bg-[#090A0F]">
      {/* Background ambient lighting */}
      <div
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[350px] rounded-full pointer-events-none"
        style={{
          background: 'radial-gradient(ellipse at center, rgba(99, 102, 241, 0.08) 0%, transparent 70%)'
        }}
      />

      <div className="max-w-6xl mx-auto px-4 sm:px-6 relative z-10">
        {/* Section Header */}
        <div className="text-center max-w-2xl mx-auto mb-14 md:mb-18">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-mono uppercase tracking-wider mb-3">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Alur Otomatisasi</span>
          </div>
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-white tracking-[-0.035em] mb-3 font-sans [text-wrap:balance]">
            Cukup <span className="text-indigo-400">3 Berkas</span>, Sisanya Otomatis
          </h2>
          <p className="text-slate-400 text-xs sm:text-sm md:text-base leading-relaxed [text-wrap:pretty]">
            Tanpa copy-paste manual, tanpa crop screenshot manual satu per satu. Biarkan agent merakit laporan lengkap dari nol.
          </p>
        </div>

        {/* 3-Step Pipeline Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 items-stretch">
          {/* STEP 1: Inputs (Col 4) */}
          <div className="lg:col-span-4 flex flex-col gap-3">
            <div className="flex items-center justify-between px-1">
              <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider font-mono">
                [INPUT] 3 Berkas Praktikum
              </span>
              <span className="text-[11px] text-indigo-400 font-mono">Klik berkas</span>
            </div>

            {inputs.map((inp) => {
              const Icon = inp.icon
              const isSelected = selectedInput === inp.id
              return (
                <button
                  key={inp.id}
                  onClick={() => setSelectedInput(inp.id)}
                  className={`w-full p-4 rounded-2xl border transition-all text-left active:scale-[0.98] shadow-[inset_0_1px_0_rgba(255,255,255,0.06)] ${
                    isSelected
                      ? 'bg-[#121522] border-indigo-500/50 shadow-lg shadow-indigo-950/40'
                      : 'bg-[#0D0F18] border-white/8 hover:border-white/15 hover:bg-[#101320]'
                  }`}
                >
                  <div className="flex items-start gap-3.5">
                    <div
                      className={`w-9 h-9 rounded-xl border flex items-center justify-center shrink-0 transition-colors ${
                        isSelected
                          ? 'bg-indigo-600/20 border-indigo-500/40 text-indigo-400'
                          : 'bg-white/5 border-white/10 text-slate-400'
                      }`}
                    >
                      <Icon className="w-4 h-4" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between gap-1 mb-1">
                        <h4 className="font-bold text-white text-xs sm:text-sm tracking-tight truncate">{inp.title}</h4>
                        <span
                          className={`text-[9px] font-mono px-1.5 py-0.5 rounded-full border ${
                            inp.badge === 'Wajib'
                              ? 'bg-indigo-500/10 text-indigo-300 border-indigo-500/25'
                              : 'bg-white/5 text-slate-400 border-white/10'
                          }`}
                        >
                          {inp.badge}
                        </span>
                      </div>
                      <p className="text-[11px] text-slate-400 line-clamp-1 mb-2">{inp.desc}</p>
                      <div className="font-mono text-[10px] text-indigo-300/80 bg-black/40 px-2 py-1 rounded-lg border border-white/5 truncate">
                        {inp.sampleName}
                      </div>
                    </div>
                  </div>
                </button>
              )
            })}
          </div>

          {/* STEP 2: The Core Engine (Col 4) */}
          <div className="lg:col-span-4 flex flex-col">
            <div className="h-full bg-[#0D0F18] border border-indigo-500/30 rounded-2xl p-5 sm:p-6 shadow-2xl relative overflow-hidden backdrop-blur-xl flex flex-col justify-between shadow-[inset_0_1px_0_rgba(255,255,255,0.06)]">
              <div>
                <div className="flex flex-col items-center text-center mb-5">
                  <NgeLaprakLogo size={46} className="rounded-xl shadow-xl shadow-indigo-600/30 mb-2.5" />
                  <h3 className="font-bold text-white text-sm sm:text-base font-sans tracking-[-0.02em]">
                    NgeLaprak Autonomous Engine
                  </h3>
                  <span className="text-[10px] font-mono text-indigo-300">
                    Inspeksi: {inputs[selectedInput].title}
                  </span>
                </div>

                {/* Selected File Deep-Dive Box */}
                <div className="p-3.5 rounded-xl bg-[#08090F] border border-white/5 mb-4 text-xs font-mono text-slate-300">
                  <div className="text-[10px] uppercase text-indigo-400 font-semibold mb-1">
                    Fungsi Analisis Berkas:
                  </div>
                  <p className="text-slate-300 text-[11px] leading-relaxed mb-2 font-sans">
                    {inputs[selectedInput].details}
                  </p>
                  <div className="text-[10px] text-slate-500 truncate bg-black/40 p-1.5 rounded border border-white/5">
                    {inputs[selectedInput].exampleSnippet}
                  </div>
                </div>

                {/* Engine Steps Checklist */}
                <div className="space-y-1.5 text-left">
                  {engineSteps.map((step, idx) => (
                    <div
                      key={idx}
                      className="flex items-start gap-2 text-[11px] text-slate-300 bg-white/[0.02] p-2 rounded-lg border border-white/5"
                    >
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0 mt-0.5" />
                      <span className="leading-tight">{step}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="mt-5 pt-3 border-t border-white/10 flex items-center justify-between text-[11px] text-slate-400 font-mono">
                <span className="tabular-nums">Durasi: ~15 - 30 dtk</span>
                <span className="text-emerald-400 font-medium">● Status: Standby</span>
              </div>
            </div>
          </div>

          {/* STEP 3: The Outputs (Col 4) */}
          <div className="lg:col-span-4 flex flex-col gap-2.5">
            <div className="flex items-center justify-between px-1">
              <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider font-mono">
                [OUTPUT] 3 Berkas Matang
              </span>
              <span className="text-[11px] text-emerald-400 font-mono">100% Siap Kumpul</span>
            </div>

            {/* Code Output Card */}
            <div className="p-3.5 rounded-2xl bg-[#0D0F18] border border-white/8 hover:border-emerald-500/30 transition-all text-left shadow-[inset_0_1px_0_rgba(255,255,255,0.06)]">
              <div className="flex items-start gap-3.5">
                <div className="w-8 h-8 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center shrink-0 text-emerald-400">
                  <FileCode className="w-4 h-4" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between gap-1 mb-1">
                    <h4 className="font-bold text-white text-xs sm:text-sm">Kode Sumber Program</h4>
                    <span className="text-[9px] font-mono px-1.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-300 border border-emerald-500/20">
                      Siap Run
                    </span>
                  </div>
                  <p className="text-[10.5px] text-slate-400 mb-1.5 leading-relaxed">
                    Struktur folder resmi (Maven / modular C++), sintaks rapi dan tervalidasi AST.
                  </p>
                  <div className="flex items-center gap-1.5 text-[9.5px] font-mono text-slate-400">
                    <Check className="w-3 h-3 text-emerald-400" /> Bebas Error Kompilasi &amp; Lolos Run
                  </div>
                </div>
              </div>
            </div>

            {/* Word Card */}
            <div className="p-3.5 rounded-2xl bg-[#0D0F18] border border-white/8 hover:border-indigo-500/30 transition-all text-left shadow-[inset_0_1px_0_rgba(255,255,255,0.06)]">
              <div className="flex items-start gap-3.5">
                <div className="w-8 h-8 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center shrink-0 text-indigo-400">
                  <FileType className="w-4 h-4" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between gap-1 mb-1">
                    <h4 className="font-bold text-white text-xs sm:text-sm">Dokumen Word (.docx)</h4>
                    <span className="text-[9px] font-mono px-1.5 py-0.5 rounded-full bg-blue-500/10 text-blue-300 border border-blue-500/20">
                      Editable
                    </span>
                  </div>
                  <p className="text-[10.5px] text-slate-400 mb-1.5 leading-relaxed">
                    Margin 4-4-3-3, font 12pt Times New Roman, spasi 1.5, dan cover logo resmi.
                  </p>
                  <div className="flex items-center gap-1.5 text-[9.5px] font-mono text-slate-400">
                    <Check className="w-3 h-3 text-emerald-400" /> Heading 1, 2, 3 Terstandarisasi
                  </div>
                </div>
              </div>
            </div>

            {/* PDF Card */}
            <div className="p-3.5 rounded-2xl bg-[#0D0F18] border border-white/8 hover:border-indigo-500/30 transition-all text-left shadow-[inset_0_1px_0_rgba(255,255,255,0.06)]">
              <div className="flex items-start gap-3.5">
                <div className="w-8 h-8 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center shrink-0 text-indigo-400">
                  <FileText className="w-4 h-4" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between gap-1 mb-1">
                    <h4 className="font-bold text-white text-xs sm:text-sm">Dokumen PDF (.pdf)</h4>
                    <span className="text-[9px] font-mono px-1.5 py-0.5 rounded-full bg-rose-500/10 text-rose-300 border border-rose-500/20">
                      Print-Ready
                    </span>
                  </div>
                  <p className="text-[10.5px] text-slate-400 mb-1.5 leading-relaxed">
                    Siap upload langsung ke portal kampus tanpa layout geser atau font missing.
                  </p>
                  <div className="flex items-center gap-1.5 text-[9.5px] font-mono text-slate-400">
                    <Check className="w-3 h-3 text-emerald-400" /> Vector Sharpness &amp; Standar Lab
                  </div>
                </div>
              </div>
            </div>

            {/* Direct button */}
            <a
              href="#samples"
              className="mt-auto flex items-center justify-center gap-2 py-3 px-4 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 text-xs font-semibold text-slate-300 hover:text-white transition-all text-center active:scale-[0.98] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500"
            >
              <Eye className="w-3.5 h-3.5 text-indigo-400" />
              <span>Lihat Contoh Dokumen Fisik</span>
              <ArrowRight className="w-3 h-3 text-slate-500" />
            </a>
          </div>
        </div>
      </div>
    </section>
  )
}
