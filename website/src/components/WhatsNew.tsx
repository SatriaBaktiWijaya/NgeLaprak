import React, { useState } from 'react'
import {
  Sparkles,
  Cpu,
  Terminal,
  Layers,
  Zap,
  CheckCircle2,
  Maximize2,
  X,
  Code2,
  Monitor,
  Copy,
  Check
} from 'lucide-react'

interface IdeShowcaseItem {
  id: 'netbeans' | 'codeblocks'
  name: string
  language: string
  engine: string
  fontRendering: string
  views: {
    editor: {
      image: string
      width: number
      height: number
      size: string
      command: string
      description: string
    }
    full: {
      image: string
      width: number
      height: number
      size: string
      command: string
      description: string
    }
  }
}

const SHOWCASE_DATA: Record<'netbeans' | 'codeblocks', IdeShowcaseItem> = {
  netbeans: {
    id: 'netbeans',
    name: 'Apache NetBeans',
    language: 'Java (Swing & JDBC)',
    engine: 'Java2D Graphics2D + FlatLaf Light + javac AST Tree API',
    fontRendering: 'Subpixel LCD_HRGB Antialiasing',
    views: {
      editor: {
        image: '/images/renderers/after_netbeans_editor.png',
        width: 1010,
        height: 707,
        size: '98 KB',
        command: 'python -m ngelaprak render --ide netbeans --view editor --file KoneksiDB.java --out 1_KoneksiDB_NetBeans.png',
        description: 'Fokus area kodingan dengan tab editor NetBeans, line numbers presisi, dan syntax highlighting semantik javac AST.'
      },
      full: {
        image: '/images/renderers/after_netbeans_full.png',
        width: 1275,
        height: 859,
        size: '133 KB',
        command: 'python -m ngelaprak render --ide netbeans --view full --file KoneksiDB.java --project KasirApp --out 1_KoneksiDB_NetBeans_full.png',
        description: 'Tampilan utuh jendela Apache NetBeans mencakup Menu Bar resmi, Toolbar action icons, Projects Tree Navigator, dan Status Bar.'
      }
    }
  },
  codeblocks: {
    id: 'codeblocks',
    name: 'Code::Blocks',
    language: 'C++ (Header & Implementation)',
    engine: 'wxWidgets wxScintilla StyledTextCtrl + lexer_cpp.xml',
    fontRendering: 'Win32 GDI Subpixel ClearType',
    views: {
      editor: {
        image: '/images/renderers/after_codeblocks_editor.png',
        width: 701,
        height: 688,
        size: '72 KB',
        command: 'python -m ngelaprak render --ide codeblocks --view editor --file main.cpp --out 2_main_cpp_CodeBlocks.png',
        description: 'Fokus potongan source code C++ dengan Scintilla folding margin, tab khas Code::Blocks, dan keyword highlighting lexer_cpp.'
      },
      full: {
        image: '/images/renderers/after_codeblocks_full.png',
        width: 974,
        height: 884,
        size: '115 KB',
        command: 'python -m ngelaprak render --ide codeblocks --view full --file main.cpp --project StrukdatModul3 --out 2_main_cpp_CodeBlocks_full.png',
        description: 'Workspace lengkap Code::Blocks dengan menu bar klasik Win32, Management tree (Projects & Files), dan editor Scintilla.'
      }
    }
  }
}

export const WhatsNew: React.FC = () => {
  const [selectedIde, setSelectedIde] = useState<'netbeans' | 'codeblocks'>('netbeans')
  const [selectedView, setSelectedView] = useState<'editor' | 'full'>('editor')
  const [copied, setCopied] = useState(false)
  const [zoomModalOpen, setZoomModalOpen] = useState(false)

  const currentIde = SHOWCASE_DATA[selectedIde]
  const currentView = currentIde.views[selectedView]

  const handleCopyCommand = () => {
    navigator.clipboard.writeText(currentView.command)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <section id="whats-new" className="py-20 md:py-28 relative overflow-hidden bg-[#090A0F] border-t border-white/5">
      {/* Background radial glow */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] bg-emerald-500/10 blur-[130px] rounded-full pointer-events-none" />
      <div className="absolute bottom-10 right-10 w-[400px] h-[300px] bg-indigo-500/10 blur-[120px] rounded-full pointer-events-none" />

      <div className="max-w-6xl mx-auto px-4 sm:px-6 relative z-10">
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-16">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/25 text-emerald-400 text-xs font-mono uppercase tracking-wider mb-4 shadow-sm shadow-emerald-950/40">
            <Sparkles className="w-3.5 h-3.5 animate-pulse" />
            <span>What's New in v1.3 • Merged PR #6</span>
          </div>

          <h2 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-white tracking-[-0.035em] mb-4 font-sans [text-wrap:balance]">
            Rilis v1.3:{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 via-teal-300 to-indigo-400">
              Pixel-Perfect Native Engines
            </span>
          </h2>

          <p className="text-slate-400 text-sm sm:text-base leading-relaxed [text-wrap:pretty]">
            Pembaruan arsitektur besar dari PR #6 oleh kontributor{' '}
            <a
              href="https://github.com/alexanderfrit"
              target="_blank"
              rel="noopener noreferrer"
              className="text-emerald-400 hover:text-emerald-300 font-semibold underline underline-offset-2 decoration-emerald-500/40 transition-colors"
            >
              Alexander Frit (@alexanderfrit)
            </a>
            : Menghilangkan mockup browser headless dengan renderer native Java2D dan wxScintilla, dukungan dual viewport, serta eksekusi lokal 0-token.
          </p>
        </div>

        {/* 4 Feature Highlights Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5 mb-14">
          {/* Highlight 1: NetBeans Java2D */}
          <div className="rounded-2xl bg-[#0D0F18]/90 border border-white/8 hover:border-emerald-500/30 p-5 sm:p-6 transition-all duration-300 group shadow-lg shadow-black/40 flex flex-col justify-between">
            <div>
              <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 mb-4 group-hover:scale-105 transition-transform">
                <Cpu className="w-5 h-5" />
              </div>
              <h3 className="text-base sm:text-lg font-bold text-white mb-2 tracking-tight group-hover:text-emerald-300 transition-colors">
                Apache NetBeans Native
              </h3>
              <p className="text-slate-400 text-xs sm:text-sm leading-relaxed mb-4">
                Compiler AST dari <code className="text-slate-200 font-mono">javac</code> membaca struktur Java murni. FlatLaf Light Theme dan subpixel antialiasing <code className="text-emerald-400 font-mono">LCD_HRGB</code> menghasilkan screenshot identik 100% dengan NetBeans asli.
              </p>
            </div>
            <div className="flex flex-wrap gap-1.5 pt-3 border-t border-white/5">
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-white/5 text-slate-300 border border-white/5">Java2D</span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/20">javac AST</span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-white/5 text-slate-300 border border-white/5">FlatLaf Light</span>
            </div>
          </div>

          {/* Highlight 2: Code::Blocks wxScintilla */}
          <div className="rounded-2xl bg-[#0D0F18]/90 border border-white/8 hover:border-indigo-500/30 p-5 sm:p-6 transition-all duration-300 group shadow-lg shadow-black/40 flex flex-col justify-between">
            <div>
              <div className="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 mb-4 group-hover:scale-105 transition-transform">
                <Code2 className="w-5 h-5" />
              </div>
              <h3 className="text-base sm:text-lg font-bold text-white mb-2 tracking-tight group-hover:text-indigo-300 transition-colors">
                Code::Blocks wxScintilla
              </h3>
              <p className="text-slate-400 text-xs sm:text-sm leading-relaxed mb-4">
                Engine berbasis <code className="text-slate-200 font-mono">wxScintilla StyledTextCtrl</code> resmi dengan parser <code className="text-indigo-400 font-mono">lexer_cpp.xml</code> dan Win32 GDI antialiasing. Menghapus artifak mock browser secara total.
              </p>
            </div>
            <div className="flex flex-wrap gap-1.5 pt-3 border-t border-white/5">
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-white/5 text-slate-300 border border-white/5">wxScintilla</span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-300 border border-indigo-500/20">lexer_cpp.xml</span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-white/5 text-slate-300 border border-white/5">Win32 GDI</span>
            </div>
          </div>

          {/* Highlight 3: Dual Viewport Modes */}
          <div className="rounded-2xl bg-[#0D0F18]/90 border border-white/8 hover:border-teal-500/30 p-5 sm:p-6 transition-all duration-300 group shadow-lg shadow-black/40 flex flex-col justify-between">
            <div>
              <div className="w-10 h-10 rounded-xl bg-teal-500/10 border border-teal-500/20 flex items-center justify-center text-teal-400 mb-4 group-hover:scale-105 transition-transform">
                <Layers className="w-5 h-5" />
              </div>
              <h3 className="text-base sm:text-lg font-bold text-white mb-2 tracking-tight group-hover:text-teal-300 transition-colors">
                Dual Viewport Modes
              </h3>
              <p className="text-slate-400 text-xs sm:text-sm leading-relaxed mb-4">
                Pilih antara <code className="text-teal-400 font-mono">--view editor</code> (slice kode terfokus untuk walkthrough modul) atau <code className="text-teal-400 font-mono">--view full</code> (jendela utuh dengan menu bar, toolbar, dan tree explorer).
              </p>
            </div>
            <div className="flex flex-wrap gap-1.5 pt-3 border-t border-white/5">
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-teal-500/10 text-teal-300 border border-teal-500/20">--view editor</span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-teal-500/10 text-teal-300 border border-teal-500/20">--view full</span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-white/5 text-slate-300 border border-white/5">--project</span>
            </div>
          </div>

          {/* Highlight 4: 0-Token Offline Engine */}
          <div className="rounded-2xl bg-[#0D0F18]/90 border border-white/8 hover:border-amber-500/30 p-5 sm:p-6 transition-all duration-300 group shadow-lg shadow-black/40 flex flex-col justify-between">
            <div>
              <div className="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-400 mb-4 group-hover:scale-105 transition-transform">
                <Zap className="w-5 h-5" />
              </div>
              <h3 className="text-base sm:text-lg font-bold text-white mb-2 tracking-tight group-hover:text-amber-300 transition-colors">
                0-Token Local CLI
              </h3>
              <p className="text-slate-400 text-xs sm:text-sm leading-relaxed mb-4">
                Proses rastering screenshot berjalan 100% secara offline dan deterministik via CLI lokal. Tidak menghabiskan kuota token context window LLM dan tanpa dependensi browser berat.
              </p>
            </div>
            <div className="flex flex-wrap gap-1.5 pt-3 border-t border-white/5">
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-500/10 text-amber-300 border border-amber-500/20">0 Token Spent</span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-white/5 text-slate-300 border border-white/5">No Puppeteer</span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-white/5 text-slate-300 border border-white/5">Deterministic</span>
            </div>
          </div>
        </div>

        {/* Interactive Dual-Viewport Showcase Console */}
        <div className="rounded-3xl bg-[#0D0F18]/95 border border-white/10 shadow-2xl shadow-black/80 overflow-hidden">
          {/* Console Header Bar */}
          <div className="px-5 sm:px-7 py-4 border-b border-white/10 bg-[#121524]/60 flex flex-col md:flex-row md:items-center justify-between gap-4">
            {/* Left: IDE Selector Tabs */}
            <div className="flex items-center gap-2">
              <span className="text-xs font-mono text-slate-400 uppercase tracking-wider mr-1 hidden sm:inline">Pilih IDE:</span>
              <button
                onClick={() => setSelectedIde('netbeans')}
                className={`flex items-center gap-2 px-3.5 py-1.5 rounded-xl font-medium text-xs sm:text-sm transition-all cursor-pointer ${
                  selectedIde === 'netbeans'
                    ? 'bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 shadow-md shadow-emerald-950/40 font-semibold'
                    : 'bg-white/5 border border-transparent text-slate-400 hover:text-white hover:bg-white/10'
                }`}
              >
                <span className="w-2 h-2 rounded-full bg-emerald-400" />
                <span>Apache NetBeans</span>
              </button>
              <button
                onClick={() => setSelectedIde('codeblocks')}
                className={`flex items-center gap-2 px-3.5 py-1.5 rounded-xl font-medium text-xs sm:text-sm transition-all cursor-pointer ${
                  selectedIde === 'codeblocks'
                    ? 'bg-indigo-500/20 border border-indigo-500/40 text-indigo-300 shadow-md shadow-indigo-950/40 font-semibold'
                    : 'bg-white/5 border border-transparent text-slate-400 hover:text-white hover:bg-white/10'
                }`}
              >
                <span className="w-2 h-2 rounded-full bg-indigo-400" />
                <span>Code::Blocks</span>
              </button>
            </div>

            {/* Right: Viewport Mode Switcher */}
            <div className="flex items-center gap-2 self-start md:self-auto">
              <span className="text-xs font-mono text-slate-400 uppercase tracking-wider mr-1">Viewport Mode:</span>
              <div className="p-1 rounded-xl bg-black/40 border border-white/10 flex items-center gap-1">
                <button
                  onClick={() => setSelectedView('editor')}
                  className={`flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-medium font-mono transition-all cursor-pointer ${
                    selectedView === 'editor'
                      ? 'bg-white/15 text-white shadow-sm font-semibold'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  <Code2 className="w-3.5 h-3.5" />
                  <span>--view editor</span>
                </button>
                <button
                  onClick={() => setSelectedView('full')}
                  className={`flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-medium font-mono transition-all cursor-pointer ${
                    selectedView === 'full'
                      ? 'bg-white/15 text-white shadow-sm font-semibold'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  <Monitor className="w-3.5 h-3.5" />
                  <span>--view full</span>
                </button>
              </div>
            </div>
          </div>

          {/* Interactive Preview Canvas */}
          <div className="p-6 sm:p-8">
            {/* Metadata Callout */}
            <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4 mb-6 pb-6 border-b border-white/5">
              <div>
                <div className="flex items-center gap-2 mb-1.5">
                  <h4 className="text-lg font-bold text-white tracking-tight">
                    {currentIde.name} — Mode{' '}
                    <span className="text-emerald-400 font-mono text-base">
                      {selectedView === 'editor' ? '--view editor' : '--view full'}
                    </span>
                  </h4>
                  <span className="text-[11px] font-mono px-2 py-0.5 rounded-full bg-white/10 text-slate-300 border border-white/10">
                    {currentView.size} • {currentView.width}×{currentView.height} px
                  </span>
                </div>
                <p className="text-slate-400 text-xs sm:text-sm max-w-2xl leading-relaxed">
                  {currentView.description}
                </p>
              </div>

              {/* Technical badges */}
              <div className="flex flex-wrap items-center gap-2 shrink-0">
                <div className="text-right">
                  <div className="text-[10px] font-mono text-slate-400 uppercase tracking-wider">Engine:</div>
                  <div className="text-xs font-mono text-slate-200">{currentIde.engine.split('+')[0].trim()}</div>
                </div>
                <div className="h-8 w-px bg-white/10 mx-2 hidden sm:block" />
                <div className="text-right">
                  <div className="text-[10px] font-mono text-slate-400 uppercase tracking-wider">Antialiasing:</div>
                  <div className="text-xs font-mono text-emerald-400">{currentIde.fontRendering}</div>
                </div>
              </div>
            </div>

            {/* CLI Command Line */}
            <div className="mb-6 rounded-xl bg-black/60 border border-white/10 p-3 sm:p-3.5 flex items-center justify-between gap-3 font-mono text-xs text-slate-300 overflow-hidden">
              <div className="flex items-center gap-2 overflow-x-auto scrollbar-none py-0.5">
                <span className="text-emerald-400 font-bold select-none">$</span>
                <span className="whitespace-nowrap">{currentView.command}</span>
              </div>
              <button
                onClick={handleCopyCommand}
                className="shrink-0 flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-white/5 hover:bg-white/10 text-slate-300 hover:text-white transition-all cursor-pointer text-[11px]"
                title="Salin Perintah CLI"
              >
                {copied ? (
                  <>
                    <Check className="w-3.5 h-3.5 text-emerald-400" />
                    <span className="text-emerald-400 font-sans">Tersalin!</span>
                  </>
                ) : (
                  <>
                    <Copy className="w-3.5 h-3.5 text-slate-400" />
                    <span className="font-sans">Salin</span>
                  </>
                )}
              </button>
            </div>

            {/* Image Frame with Glass Styling */}
            <div className="relative rounded-2xl bg-black/40 border border-white/10 overflow-hidden shadow-2xl group">
              <div className="relative overflow-hidden flex items-center justify-center p-2 sm:p-4 bg-[radial-gradient(#ffffff08_1px,transparent_1px)] [background-size:16px_16px]">
                <img
                  src={currentView.image}
                  alt={`${currentIde.name} ${selectedView} Screenshot`}
                  className="rounded-xl max-h-[580px] w-auto object-contain shadow-2xl border border-white/5 transition-transform duration-500 group-hover:scale-[1.01]"
                />
              </div>

              {/* Hover Zoom Button */}
              <button
                onClick={() => setZoomModalOpen(true)}
                className="absolute bottom-4 right-4 flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-[#0D0F18]/90 hover:bg-[#0D0F18] border border-white/20 text-slate-200 text-xs font-medium shadow-xl backdrop-blur-md transition-all active:scale-95 cursor-pointer"
              >
                <Maximize2 className="w-3.5 h-3.5 text-emerald-400" />
                <span>Perbesar Resolusi Asli</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Lightbox Zoom Modal */}
      {zoomModalOpen && (
        <div
          className="fixed inset-0 z-50 bg-black/90 backdrop-blur-md flex items-center justify-center p-4 sm:p-8"
          onClick={() => setZoomModalOpen(false)}
        >
          <div
            className="relative max-w-6xl max-h-[90vh] w-full flex flex-col items-center"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="w-full flex items-center justify-between pb-3 text-slate-300">
              <div className="flex items-center gap-2">
                <span className="font-semibold text-white">{currentIde.name}</span>
                <span className="font-mono text-xs text-emerald-400">({selectedView === 'editor' ? '--view editor' : '--view full'})</span>
                <span className="text-xs text-slate-400">• {currentView.width}×{currentView.height} px ({currentView.size})</span>
              </div>
              <button
                onClick={() => setZoomModalOpen(false)}
                className="p-1.5 rounded-xl bg-white/10 hover:bg-white/20 text-white cursor-pointer transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            <div className="overflow-auto max-h-[82vh] w-full rounded-xl border border-white/15 bg-black/60 p-2 flex items-center justify-center">
              <img
                src={currentView.image}
                alt="Full resolution preview"
                className="max-w-none max-h-none object-contain rounded-lg shadow-2xl"
              />
            </div>
          </div>
        </div>
      )}
    </section>
  )
}
