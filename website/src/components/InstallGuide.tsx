import React, { useState } from 'react'
import { Terminal, Copy, Check, MessageSquareCode, FolderCheck, Sparkles, ArrowRight } from 'lucide-react'

export const InstallGuide: React.FC = () => {
  const [copied, setCopied] = useState(false)
  const cmd = 'npx skills add ngelaprak'

  const handleCopy = () => {
    navigator.clipboard.writeText(cmd)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const steps = [
    {
      num: '01',
      title: 'Tambahkan Skill ke AI Agent',
      icon: Terminal,
      desc: 'Jalankan perintah instalasi satu baris di terminal AI IDE favorit kamu (Cursor, Claude Code, Gemini CLI, Antigravity, VS Code).'
    },
    {
      num: '02',
      title: 'Taruh Berkas Praktikum',
      icon: FolderCheck,
      desc: 'Letakkan source code tugas (.java/.cpp), file modul/soal (.pdf), serta template lab kampus (.docx/.pdf jika ada).'
    },
    {
      num: '03',
      title: 'Ketik Prompt Praktikum Singkat',
      icon: MessageSquareCode,
      desc: 'Cukup ketik: "Buatkan laprak modul 3 dari file ini", dan AI agent akan merakit seluruh dokumen secara mandiri.'
    }
  ]

  return (
    <section id="install" className="py-24 relative overflow-hidden bg-[#090A0F]">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 relative z-10">
        {/* Header */}
        <div className="text-center max-w-2xl mx-auto mb-16">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-mono uppercase tracking-wider mb-3">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Cara Penggunaan</span>
          </div>
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-white tracking-[-0.035em] mb-4 font-sans [text-wrap:balance]">
            Mulai Dalam <span className="text-indigo-400">3 Langkah Mudah</span>
          </h2>
          <p className="text-slate-400 text-sm sm:text-base leading-relaxed [text-wrap:pretty]">
            Tanpa perlu instalasi software desktop berat terpisah. Cukup pasang skill NgeLaprak di dalam terminal agen coding kamu.
          </p>
        </div>

        {/* 3 Step Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          {steps.map((s, idx) => {
            const Icon = s.icon
            return (
              <div
                key={idx}
                className="rounded-3xl bg-[#0D0F18] border border-white/8 hover:border-indigo-500/30 p-6 sm:p-7 relative group transition-all duration-300 shadow-xl shadow-black/40 shadow-[inset_0_1px_0_rgba(255,255,255,0.06)] flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between mb-6">
                    <div className="w-11 h-11 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 group-hover:scale-105 transition-transform">
                      <Icon className="w-5 h-5" />
                    </div>
                    <span className="text-2xl font-black font-mono text-slate-700 group-hover:text-indigo-400 transition-colors tabular-nums">
                      {s.num}
                    </span>
                  </div>

                  <h3 className="font-bold text-white text-base sm:text-lg mb-2 tracking-tight">{s.title}</h3>
                  <p className="text-xs sm:text-sm text-slate-400 leading-relaxed mb-6 [text-wrap:pretty]">{s.desc}</p>
                </div>

                {/* Bottom slot aligned via mt-auto */}
                <div className="mt-auto pt-2">
                  {idx === 0 && (
                    <div className="p-2.5 rounded-xl bg-black/40 border border-white/10 flex items-center justify-between gap-2 font-mono text-xs text-slate-200">
                      <span className="truncate">{cmd}</span>
                      <button
                        onClick={handleCopy}
                        className="p-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white shrink-0 active:scale-[0.98] transition-all"
                        title="Salin"
                      >
                        {copied ? <Check className="w-3.5 h-3.5 text-emerald-300" /> : <Copy className="w-3.5 h-3.5" />}
                      </button>
                    </div>
                  )}

                  {idx === 1 && (
                    <div className="p-2.5 rounded-xl bg-white/[0.02] border border-white/5 text-[11px] text-slate-400 font-mono flex items-center justify-between">
                      <span>📁 3 File Praktikum</span>
                      <span className="text-emerald-400 font-semibold">Siap di workspace</span>
                    </div>
                  )}

                  {idx === 2 && (
                    <div className="p-2.5 rounded-xl bg-indigo-950/30 border border-indigo-500/20 text-xs text-indigo-200 font-mono">
                      💬 "Buatkan laprak modul 3..."
                    </div>
                  )}
                </div>
              </div>
            )
          })}
        </div>

        {/* Refined Banner CTA */}
        <div className="rounded-3xl bg-[#0D0F18] border border-indigo-500/30 p-8 sm:p-10 text-center relative overflow-hidden shadow-2xl shadow-indigo-950/20 shadow-[inset_0_1px_0_rgba(255,255,255,0.08)]">
          <div className="absolute top-0 right-1/4 w-96 h-96 bg-indigo-600/[0.06] blur-[120px] rounded-full pointer-events-none" />

          <div className="max-w-xl mx-auto relative z-10">
            <h3 className="text-2xl sm:text-3xl font-extrabold text-white mb-2.5 font-sans tracking-[-0.03em] [text-wrap:balance]">
              Siap Menghemat Jam Begadang Praktikum?
            </h3>
            <p className="text-slate-400 text-xs sm:text-sm mb-7 [text-wrap:pretty]">
              Pasang skill NgeLaprak sekarang juga dan rasakan pengalaman menyusun laporan tanpa stres revisi margin atau screenshot pecah.
            </p>
            <div className="inline-flex items-center gap-2 p-1.5 rounded-2xl bg-[#08090F] border border-white/10 max-w-md w-full justify-between shadow-2xl">
              <span className="font-mono text-xs sm:text-sm text-slate-300 px-3 truncate">$ {cmd}</span>
              <button
                onClick={handleCopy}
                className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold shrink-0 transition-all shadow-md shadow-indigo-600/30 active:scale-[0.98] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-300" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copied ? 'Tersalin!' : 'Salin Perintah'}</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
