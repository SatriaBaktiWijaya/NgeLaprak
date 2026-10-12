import React, { useState } from 'react'
import { Terminal, Copy, Check, MessageSquareCode, FolderCheck, Play, Sparkles } from 'lucide-react'

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
      desc: 'Jalankan perintah instalasi satu baris di terminal AI IDE favorit kamu (Cursor, Claude Code, Gemini CLI, VS Code).'
    },
    {
      num: '02',
      title: 'Taruh Berkas Praktikum',
      icon: FolderCheck,
      desc: 'Letakkan source code tugas (.java/.cpp), file modul/soal (.pdf), serta template lab (.docx jika ada).'
    },
    {
      num: '03',
      title: 'Beri Perintah Prompt Singkat',
      icon: MessageSquareCode,
      desc: 'Cukup ketik: "Buatkan laprak modul 3 dari file ini", dan AI agent akan merakit seluruh dokumen secara mandiri.'
    }
  ]

  return (
    <section id="install" className="py-24 relative overflow-hidden bg-[#08090E]">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 relative z-10">
        {/* Header */}
        <div className="text-center max-w-2xl mx-auto mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-semibold mb-3">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Cara Penggunaan</span>
          </div>
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-white tracking-tight mb-4 font-sans">
            Mulai Dalam{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">
              3 Langkah Mudah
            </span>
          </h2>
          <p className="text-slate-400 text-sm sm:text-base leading-relaxed">
            Tidak perlu install aplikasi berat terpisah. Cukup panggil skill NgeLaprak di dalam terminal agen coding kamu.
          </p>
        </div>

        {/* 3 Step Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          {steps.map((s, idx) => {
            const Icon = s.icon
            return (
              <div
                key={idx}
                className="rounded-3xl bg-[#0F1221] border border-white/8 hover:border-indigo-500/40 p-6 relative group transition-all duration-300 shadow-xl flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between mb-6">
                    <div className="w-12 h-12 rounded-2xl bg-indigo-500/15 border border-indigo-500/30 flex items-center justify-center text-indigo-400 group-hover:scale-105 transition-transform">
                      <Icon className="w-6 h-6" />
                    </div>
                    <span className="text-2xl font-black font-mono text-slate-700 group-hover:text-indigo-400 transition-colors">
                      {s.num}
                    </span>
                  </div>

                  <h3 className="font-bold text-white text-lg mb-2">{s.title}</h3>
                  <p className="text-xs sm:text-sm text-slate-400 leading-relaxed mb-6">{s.desc}</p>
                </div>

                {idx === 0 && (
                  <div className="p-3 rounded-xl bg-black/40 border border-white/5 flex items-center justify-between gap-2 font-mono text-xs text-slate-200">
                    <span className="truncate">{cmd}</span>
                    <button
                      onClick={handleCopy}
                      className="p-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white shrink-0 transition-colors"
                      title="Salin"
                    >
                      {copied ? <Check className="w-3.5 h-3.5 text-emerald-300" /> : <Copy className="w-3.5 h-3.5" />}
                    </button>
                  </div>
                )}

                {idx === 2 && (
                  <div className="p-3 rounded-xl bg-indigo-950/20 border border-indigo-500/20 text-xs text-indigo-200 font-mono">
                    💬 "Buatkan laprak modul 3..."
                  </div>
                )}
              </div>
            )
          })}
        </div>

        {/* Banner CTA */}
        <div className="rounded-3xl bg-gradient-to-r from-indigo-900/40 via-purple-900/30 to-pink-900/20 border border-indigo-500/30 p-8 text-center relative overflow-hidden backdrop-blur-xl">
          <div className="max-w-xl mx-auto">
            <h3 className="text-xl sm:text-2xl font-bold text-white mb-2 font-sans">
              Siap Menghemat Jam Begadang Praktikum?
            </h3>
            <p className="text-slate-400 text-xs sm:text-sm mb-6">
              Pasang skill NgeLaprak sekarang juga dan rasakan pengalaman menyusun laporan tanpa stres.
            </p>
            <div className="inline-flex items-center gap-2 p-1.5 rounded-2xl bg-[#090B14] border border-white/10 max-w-md w-full justify-between shadow-2xl">
              <span className="font-mono text-xs sm:text-sm text-slate-300 px-3 truncate">$ {cmd}</span>
              <button
                onClick={handleCopy}
                className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold shrink-0 transition-all shadow-md shadow-indigo-600/30"
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
