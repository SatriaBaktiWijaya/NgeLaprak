import React, { useState } from 'react'
import { XCircle, CheckCircle2, Clock, Sparkles, AlertTriangle, ArrowRight } from 'lucide-react'

export const BeforeAfter: React.FC = () => {
  const comparisons = [
    {
      feature: 'Struktur Project Kode',
      before: '1 file kode tergeletak di Desktop tanpa package/header',
      after: 'Struktur folder resmi Maven / NetBeans / CMake siap di-build',
      beforeStatus: 'Berantakan',
      afterStatus: 'Standar Industri'
    },
    {
      feature: 'Tangkapan Layar (Screenshot)',
      before: 'Foto HP layar monitor atau snipping tool terpotong buram',
      after: 'Frame IDE autentik dengan traffic lights & font anti-aliased',
      beforeStatus: 'Buram & Miring',
      afterStatus: 'Pixel-Perfect'
    },
    {
      feature: 'Format Margin & Spasi',
      before: 'Margin acak-acakan, spasi tidak rata, heading bergeser',
      after: 'Margin standar 4-4-3-3, font 12pt Times/Calibri, spasi 1.5 rapi',
      beforeStatus: 'Revisi Aslab',
      afterStatus: 'Langsung ACC'
    },
    {
      feature: 'Pembahasan & Teori',
      before: 'Copas Wikipedia / dokumen teman berisiko kena plagiarisme',
      after: 'Penjelasan baris-per-baris dengan student voice yang unik',
      beforeStatus: 'Indikasi Plagiat',
      afterStatus: 'Orisinal & Alami'
    },
    {
      feature: 'Waktu Pengerjaan',
      before: '3 – 5 Jam begadang format dokumen manual semalaman',
      after: 'Cukup 30 Detik — 3 file otomatis dirakit oleh AI agent',
      beforeStatus: 'Melelahkan',
      afterStatus: 'Instan & Santai'
    }
  ]

  return (
    <section id="compare" className="py-24 relative overflow-hidden bg-[#0A0C14]">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 relative z-10">
        {/* Section Header */}
        <div className="text-center max-w-2xl mx-auto mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-semibold mb-3">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Realita Praktikan</span>
          </div>
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-white tracking-tight mb-4 font-sans">
            Sebelum vs Sesudah{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">
              NgeLaprak
            </span>
          </h2>
          <p className="text-slate-400 text-sm sm:text-base leading-relaxed">
            Bandingkan repotnya membuat laporan secara konvensional dengan kepraktisan ekosistem NgeLaprak.
          </p>
        </div>

        {/* 2 Big Side-by-side Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
          {/* BEFORE CARD */}
          <div className="rounded-2xl bg-[#120F15] border border-red-500/20 p-6 sm:p-8 relative overflow-hidden shadow-xl">
            <div className="absolute top-0 right-0 w-32 h-32 bg-red-500/10 rounded-full blur-3xl pointer-events-none" />

            <div className="flex items-center justify-between mb-6 pb-4 border-b border-white/5">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-red-500/15 border border-red-500/30 flex items-center justify-center text-red-400">
                  <XCircle className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-bold text-white text-lg">Format Manual</h3>
                  <span className="text-xs text-red-400 font-mono">Cara Konvensional</span>
                </div>
              </div>
              <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-red-500/10 text-red-400 border border-red-500/20">
                Pusing & Lama
              </span>
            </div>

            {/* Badges/preview mock */}
            <div className="space-y-4">
              <div className="p-3.5 rounded-xl bg-black/40 border border-red-500/20 text-xs text-slate-300 flex items-start gap-3">
                <span className="text-red-400 font-bold shrink-0">❌ 01</span>
                <span>Screenshots cropping manual berantakan, resolusi pecah, dan sering kena komplain asisten lab.</span>
              </div>
              <div className="p-3.5 rounded-xl bg-black/40 border border-red-500/20 text-xs text-slate-300 flex items-start gap-3">
                <span className="text-red-400 font-bold shrink-0">❌ 02</span>
                <span>Margin Word bergeser saat di-convert ke PDF, nomor romawi halaman sampul rusak.</span>
              </div>
              <div className="p-3.5 rounded-xl bg-black/40 border border-red-500/20 text-xs text-slate-300 flex items-start gap-3">
                <span className="text-red-400 font-bold shrink-0">❌ 03</span>
                <span>Struktur kode acak-acakan tidak bisa di-run langsung di Apache NetBeans atau Code::Blocks.</span>
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-white/5 flex items-center justify-between text-xs text-slate-500 font-mono">
              <span className="flex items-center gap-1.5 text-red-400/90">
                <Clock className="w-3.5 h-3.5" /> Rata-rata 4 jam / minggu
              </span>
              <span>Tingkat Revisi: Tinggi</span>
            </div>
          </div>

          {/* AFTER CARD */}
          <div className="rounded-2xl bg-[#0F1424] border border-indigo-500/40 p-6 sm:p-8 relative overflow-hidden shadow-2xl ring-1 ring-indigo-500/20">
            <div className="absolute top-0 right-0 w-40 h-40 bg-indigo-500/15 rounded-full blur-3xl pointer-events-none" />

            <div className="flex items-center justify-between mb-6 pb-4 border-b border-white/5">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-indigo-500/20 border border-indigo-500/40 flex items-center justify-center text-indigo-400 shadow-md">
                  <CheckCircle2 className="w-5 h-5 text-indigo-400" />
                </div>
                <div>
                  <h3 className="font-bold text-white text-lg">Dengan NgeLaprak</h3>
                  <span className="text-xs text-indigo-300 font-mono">AI Agent Automated</span>
                </div>
              </div>
              <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                Otomatis & Sempurna
              </span>
            </div>

            {/* Badges/preview mock */}
            <div className="space-y-4">
              <div className="p-3.5 rounded-xl bg-black/40 border border-indigo-500/30 text-xs text-slate-200 flex items-start gap-3">
                <span className="text-emerald-400 font-bold shrink-0">✓ 01</span>
                <span>Screenshot IDE asli beresolusi tinggi otomatis di-render dan disisipkan per bab kode.</span>
              </div>
              <div className="p-3.5 rounded-xl bg-black/40 border border-indigo-500/30 text-xs text-slate-200 flex items-start gap-3">
                <span className="text-emerald-400 font-bold shrink-0">✓ 02</span>
                <span>Margin 4-4-3-3 baku, penomoran Romawi & Arab otomatis, cover lengkap logo universitas.</span>
              </div>
              <div className="p-3.5 rounded-xl bg-black/40 border border-indigo-500/30 text-xs text-slate-200 flex items-start gap-3">
                <span className="text-emerald-400 font-bold shrink-0">✓ 03</span>
                <span>Struktur folder modular NetBeans Maven / C++ yang langsung bisa dibuka dan dijalankan.</span>
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-white/5 flex items-center justify-between text-xs text-slate-400 font-mono">
              <span className="flex items-center gap-1.5 text-emerald-400">
                <Sparkles className="w-3.5 h-3.5" /> Selesai dalam ~30 detik
              </span>
              <span className="text-indigo-300">Siap Kumpul Langsung ACC</span>
            </div>
          </div>
        </div>

        {/* Detailed Comparison Table */}
        <div className="rounded-2xl bg-[#0E111E]/80 border border-white/5 overflow-hidden">
          <div className="p-4 bg-[#141829] border-b border-white/5 flex items-center justify-between">
            <span className="text-xs font-mono font-bold text-slate-300 uppercase tracking-wider">
              Tabel Komparasi Fitur
            </span>
            <span className="text-xs text-indigo-400 font-mono">5 Parameter Kritis</span>
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
                  <span className="w-2 h-2 rounded-full bg-red-500 shrink-0" />
                  <span className="truncate">{item.before}</span>
                </div>
                <div className="md:col-span-4 text-slate-200 flex items-center gap-2 font-medium">
                  <span className="w-2 h-2 rounded-full bg-emerald-400 shrink-0" />
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
