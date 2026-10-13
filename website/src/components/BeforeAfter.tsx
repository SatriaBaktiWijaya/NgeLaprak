import React from 'react'
import { XCircle, CheckCircle2, Clock, Sparkles, X, Check, ArrowRight } from 'lucide-react'

export const BeforeAfter: React.FC = () => {
  const comparisons = [
    {
      feature: 'Struktur Proyek Kode',
      before: '1 file source code tergeletak di Desktop tanpa package/header',
      after: 'Struktur resmi Maven / NetBeans / CMake siap di-build tanpa missing path',
      beforeStatus: 'Berantakan',
      afterStatus: 'Standar Industri'
    },
    {
      feature: 'Tangkapan Layar (Screenshot)',
      before: 'Foto kamera HP layar monitor atau snipping tool terpotong buram',
      after: 'Frame IDE autentik dengan traffic lights & font anti-aliased tajam',
      beforeStatus: 'Buram & Miring',
      afterStatus: 'Pixel-Perfect'
    },
    {
      feature: 'Format Margin & Spasi',
      before: 'Margin acak-acakan, spasi tidak rata, heading bergeser saat save',
      after: 'Margin standar 4-4-3-3, font 12pt Times New Roman, spasi 1.5 presisi',
      beforeStatus: 'Revisi Aslab',
      afterStatus: 'Langsung ACC'
    },
    {
      feature: 'Pembahasan & Teori',
      before: 'Copas Wikipedia / dokumen teman berisiko kena sanksi plagiarisme',
      after: 'Penjelasan baris-per-baris dengan student voice kritis yang orisinal',
      beforeStatus: 'Indikasi Plagiat',
      afterStatus: 'Orisinal & Alami'
    },
    {
      feature: 'Waktu Pengerjaan Laporan',
      before: '3 – 5 Jam begadang format dokumen manual semalaman',
      after: 'Cukup 30 Detik — 3 file otomatis dirakit oleh AI agent',
      beforeStatus: '3-5 Jam',
      afterStatus: '30 Detik'
    }
  ]

  return (
    <section id="compare" className="py-24 relative overflow-hidden bg-[#090A0F]">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 relative z-10">
        {/* Section Header */}
        <div className="text-center max-w-2xl mx-auto mb-16">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-mono uppercase tracking-wider mb-3">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Realita Praktikan</span>
          </div>
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-white tracking-[-0.035em] mb-4 font-sans [text-wrap:balance]">
            Sebelum vs Sesudah{' '}
            <span className="text-indigo-400">NgeLaprak</span>
          </h2>
          <p className="text-slate-400 text-sm sm:text-base leading-relaxed [text-wrap:pretty]">
            Bandingkan repotnya membuat laporan secara konvensional dengan kepraktisan ekosistem AI Agent.
          </p>
        </div>

        {/* 2 Big Side-by-side Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
          {/* BEFORE CARD */}
          <div className="rounded-3xl bg-[#0D0F18] border border-rose-500/20 p-6 sm:p-8 relative overflow-hidden shadow-xl shadow-black/40 shadow-[inset_0_1px_0_rgba(255,255,255,0.04)]">
            <div className="flex items-center justify-between mb-6 pb-4 border-b border-white/5">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-2xl bg-rose-500/10 border border-rose-500/20 flex items-center justify-center text-rose-400">
                  <XCircle className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-bold text-white text-lg tracking-tight">Format Manual Konvensional</h3>
                  <span className="text-xs text-rose-400/90 font-mono">Cara Tradisional Mahasiswa</span>
                </div>
              </div>
              <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-rose-500/10 text-rose-300 border border-rose-500/20 font-mono">
                Manual & Melelahkan
              </span>
            </div>

            {/* Pain points */}
            <div className="space-y-3.5">
              <div className="p-3.5 rounded-xl bg-black/30 border border-rose-500/15 text-xs text-slate-300 flex items-start gap-3">
                <span className="text-rose-400 font-bold shrink-0 font-mono">01</span>
                <span className="leading-relaxed">Screenshots cropping manual berantakan, resolusi pecah, dan sering kena komplain asisten lab karena tidak ada frame window.</span>
              </div>
              <div className="p-3.5 rounded-xl bg-black/30 border border-rose-500/15 text-xs text-slate-300 flex items-start gap-3">
                <span className="text-rose-400 font-bold shrink-0 font-mono">02</span>
                <span className="leading-relaxed">Margin Word bergeser saat di-convert ke PDF, nomor halaman romawi (i, ii) dan Arab (1, 2) saling bertabrakan.</span>
              </div>
              <div className="p-3.5 rounded-xl bg-black/30 border border-rose-500/15 text-xs text-slate-300 flex items-start gap-3">
                <span className="text-rose-400 font-bold shrink-0 font-mono">03</span>
                <span className="leading-relaxed">Struktur kode terpecah tanpa konfigurasi build sehingga aslab kesulitan mereview kode saat responsi praktikum.</span>
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-white/5 flex items-center justify-between text-xs text-slate-400 font-mono">
              <span className="flex items-center gap-1.5 text-rose-400">
                <Clock className="w-3.5 h-3.5" /> <strong className="tabular-nums">3 – 5 Jam</strong> / modul praktikum
              </span>
              <span>Tingkat Revisi: Tinggi</span>
            </div>
          </div>

          {/* AFTER CARD */}
          <div className="rounded-3xl bg-[#0D0F18] border border-indigo-500/40 p-6 sm:p-8 relative overflow-hidden shadow-2xl shadow-indigo-950/20 shadow-[inset_0_1px_0_rgba(255,255,255,0.08)]">
            <div className="flex items-center justify-between mb-6 pb-4 border-b border-white/5">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-2xl bg-indigo-500/15 border border-indigo-500/30 flex items-center justify-center text-indigo-400 shadow-md">
                  <CheckCircle2 className="w-5 h-5 text-indigo-400" />
                </div>
                <div>
                  <h3 className="font-bold text-white text-lg tracking-tight">Dengan NgeLaprak</h3>
                  <span className="text-xs text-indigo-300 font-mono">AI Agent Automated Pipeline</span>
                </div>
              </div>
              <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono">
                Otomatis & Presisi
              </span>
            </div>

            {/* Benefits */}
            <div className="space-y-3.5">
              <div className="p-3.5 rounded-xl bg-black/30 border border-indigo-500/30 text-xs text-slate-200 flex items-start gap-3">
                <span className="text-emerald-400 font-bold shrink-0 font-mono">01</span>
                <span className="leading-relaxed">Screenshot IDE asli beresolusi tinggi otomatis di-render dan disematkan per bab kode tanpa watermark.</span>
              </div>
              <div className="p-3.5 rounded-xl bg-black/30 border border-indigo-500/30 text-xs text-slate-200 flex items-start gap-3">
                <span className="text-emerald-400 font-bold shrink-0 font-mono">02</span>
                <span className="leading-relaxed">Margin 4-4-3-3 baku, penomoran Romawi & Arab otomatis, cover adaptif lengkap dengan logo universitas asli.</span>
              </div>
              <div className="p-3.5 rounded-xl bg-black/30 border border-indigo-500/30 text-xs text-slate-200 flex items-start gap-3">
                <span className="text-emerald-400 font-bold shrink-0 font-mono">03</span>
                <span className="leading-relaxed">Struktur folder modular NetBeans Maven / C++ yang langsung bisa dibuka dan dijalankan tanpa missing dependency.</span>
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-white/5 flex items-center justify-between text-xs text-slate-400 font-mono">
              <span className="flex items-center gap-1.5 text-emerald-400 font-medium">
                <Sparkles className="w-3.5 h-3.5" /> Selesai dalam <strong className="tabular-nums font-bold">~30 detik</strong>
              </span>
              <span className="text-indigo-300">Siap Kumpul Langsung ACC</span>
            </div>
          </div>
        </div>

        {/* Detailed Comparison Table */}
        <div className="rounded-2xl bg-[#0D0F18] border border-white/8 overflow-hidden shadow-xl shadow-[inset_0_1px_0_rgba(255,255,255,0.06)]">
          <div className="p-4 bg-[#111422] border-b border-white/8 flex items-center justify-between">
            <span className="text-xs font-mono font-bold text-slate-300 uppercase tracking-wider">
              Tabel Komparasi Fitur
            </span>
            <span className="text-xs text-indigo-400 font-mono">5 Parameter Kritis Laboratorium</span>
          </div>

          <div className="divide-y divide-white/5">
            {comparisons.map((item, idx) => (
              <div
                key={idx}
                className="grid grid-cols-1 md:grid-cols-12 p-4 text-xs sm:text-sm items-center hover:bg-white/[0.02] transition-colors gap-2 md:gap-4"
              >
                <div className="md:col-span-4 font-semibold text-white">
                  {item.feature}
                </div>
                <div className="md:col-span-4 text-slate-400 flex items-center gap-2">
                  <X className="w-3.5 h-3.5 text-rose-400 shrink-0" />
                  <span className="truncate">{item.before}</span>
                </div>
                <div className="md:col-span-4 text-slate-200 flex items-center gap-2 font-medium">
                  <Check className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                  <span className="truncate text-indigo-200">{item.after}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
