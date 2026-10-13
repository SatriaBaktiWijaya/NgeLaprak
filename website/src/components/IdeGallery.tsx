import React, { useState } from 'react'
import { Monitor, Code, Maximize2, Sparkles, FolderTree, Check, Terminal, Copy } from 'lucide-react'

interface IdeProfile {
  id: string
  name: string
  course: string
  lang: string
  filename: string
  badge: string
  screenshotPath: string
  codeSnippet: string
  outputSample: string
  structurePath: string
  runtimeMetric: string
}

export const IdeGallery: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('netbeans')
  const [viewMode, setViewMode] = useState<'screenshot' | 'code'>('screenshot')
  const [zoomModal, setZoomModal] = useState<string | null>(null)
  const [copied, setCopied] = useState(false)

  const ideList: IdeProfile[] = [
    {
      id: 'netbeans',
      name: 'Apache NetBeans',
      course: 'PBO & Rekayasa Perangkat Lunak',
      lang: 'Java / Swing',
      filename: 'KoneksiDB.java',
      badge: 'Maven Architecture',
      screenshotPath: '/samples/adpl/screenshots/1_KoneksiDB_NetBeans.png',
      structurePath: 'src/main/java/com/praktikum/adpl/',
      outputSample: 'BUILD SUCCESS',
      runtimeMetric: '1.284s',
      codeSnippet: `package com.praktikum.adpl;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class KoneksiDB {
    private static Connection koneksi;
    
    public static Connection getKoneksi() {
        if (koneksi == null) {
            try {
                String url = "jdbc:mysql://localhost:3306/db_kasir";
                String user = "root";
                String pass = "";
                DriverManager.registerDriver(new com.mysql.cj.jdbc.Driver());
                koneksi = DriverManager.getConnection(url, user, pass);
                System.out.println("Koneksi Database Berhasil!");
            } catch (SQLException e) {
                System.err.println("Koneksi Gagal: " + e.getMessage());
            }
        }
        return koneksi;
    }
}`
    },
    {
      id: 'codeblocks',
      name: 'Code::Blocks',
      course: 'Struktur Data & Algoritma',
      lang: 'C / C++',
      filename: 'Stack.h',
      badge: 'Modular Header & Source',
      screenshotPath: '/samples/strukdat/screenshots/1_Stack_h_CodeBlocks.png',
      structurePath: 'include/Stack.h & src/main.cpp',
      outputSample: 'Process returned 0 (0x0)',
      runtimeMetric: '0.012s',
      codeSnippet: `#ifndef STACK_H
#define STACK_H

#define MAX_STACK 100

typedef struct {
    int top;
    int data[MAX_STACK];
} Stack;

void initStack(Stack *s);
int isFull(Stack *s);
int isEmpty(Stack *s);
void push(Stack *s, int val);
int pop(Stack *s);
void displayStack(Stack *s);

#endif // STACK_H`
    },
    {
      id: 'vscode',
      name: 'Visual Studio Code',
      course: 'Kecerdasan Buatan & Web',
      lang: 'Python / JS',
      filename: 'dijkstra_graph.py',
      badge: 'Modern Dark One',
      screenshotPath: '/samples/strukdat/screenshots/2_main_cpp_CodeBlocks.png',
      structurePath: 'scripts/graph_analysis.py',
      outputSample: 'Shortest path found: [A -> B -> D -> E]',
      runtimeMetric: '0.045s',
      codeSnippet: `import heapq

class Graph:
    def __init__(self):
        self.adj = {}
        
    def add_edge(self, u, v, weight):
        self.adj.setdefault(u, []).append((v, weight))
        self.adj.setdefault(v, []).append((u, weight))
        
    def dijkstra(self, start):
        dist = {node: float('inf') for node in self.adj}
        dist[start] = 0
        pq = [(0, start)]
        
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for v, w in self.adj[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    heapq.heappush(pq, (dist[v], v))
        return dist`
    },
    {
      id: 'dbeaver',
      name: 'DBeaver / Terminal',
      course: 'Sistem Basis Data',
      lang: 'SQL / Shell',
      filename: 'query_analisis.sql',
      badge: 'Console Execution Frame',
      screenshotPath: '/samples/adpl/screenshots/4_MySQL_Terminal.png',
      structurePath: 'database/schema_and_queries.sql',
      outputSample: 'Query OK, 5 rows affected',
      runtimeMetric: '0.003s',
      codeSnippet: `-- Laporan Modul Basis Data: Relasi & Indexing
SELECT 
    p.kode_produk,
    p.nama_produk,
    k.nama_kategori,
    SUM(d.qty) AS total_terjual,
    SUM(d.qty * p.harga) AS subtotal
FROM produk p
JOIN kategori k ON p.id_kategori = k.id_kategori
JOIN transaksi_detail d ON p.id_produk = d.id_produk
GROUP BY p.id_produk
ORDER BY total_terjual DESC
LIMIT 5;`
    }
  ]

  const current = ideList.find((i) => i.id === activeTab) || ideList[0]

  const handleCopyCode = () => {
    navigator.clipboard.writeText(current.codeSnippet)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <section id="gallery" className="py-24 relative overflow-hidden bg-[#090A0F]">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 relative z-10">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-12">
          <div>
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-mono uppercase tracking-wider mb-3">
              <Monitor className="w-3.5 h-3.5" />
              <span>Authentic IDE Rendering Engine</span>
            </div>
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-white tracking-[-0.035em] font-sans [text-wrap:balance]">
              Screenshot IDE Asli,{' '}
              <span className="text-indigo-400">Bukan Teks Mentah</span>
            </h2>
            <p className="text-slate-400 text-sm sm:text-base mt-2 max-w-xl [text-wrap:pretty]">
              NgeLaprak menghasilkan visual IDE nyata berstandar sistem operasi tanpa watermark, langsung disematkan rapi ke bab pembahasan laporan.
            </p>
          </div>

          {/* Screenshot / Code View Mode Toggle */}
          <div className="flex items-center bg-[#0D0F18] p-1 rounded-xl border border-white/10 self-start md:self-auto shadow-inner">
            <button
              onClick={() => setViewMode('screenshot')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all active:scale-[0.98] ${
                viewMode === 'screenshot'
                  ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <Monitor className="w-3.5 h-3.5" />
              <span>Screenshot IDE</span>
            </button>
            <button
              onClick={() => setViewMode('code')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all active:scale-[0.98] ${
                viewMode === 'code'
                  ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <Code className="w-3.5 h-3.5" />
              <span>Source Code</span>
            </button>
          </div>
        </div>

        {/* IDE Selector Tabs */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-8">
          {ideList.map((ide) => {
            const isActive = activeTab === ide.id
            return (
              <button
                key={ide.id}
                onClick={() => setActiveTab(ide.id)}
                className={`p-3.5 sm:p-4 rounded-2xl border text-left transition-all duration-200 relative overflow-hidden active:scale-[0.98] shadow-[inset_0_1px_0_rgba(255,255,255,0.06)] ${
                  isActive
                    ? 'bg-[#121522] border-indigo-500/60 shadow-lg shadow-indigo-950/40 ring-1 ring-indigo-500/20'
                    : 'bg-[#0D0F18] border-white/8 hover:border-white/15 hover:bg-[#101320]'
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="font-bold text-white text-xs sm:text-sm">{ide.name}</span>
                  {isActive && <div className="w-1.5 h-1.5 rounded-full bg-indigo-400" />}
                </div>
                <div className="text-[11px] text-slate-400 truncate">{ide.lang}</div>
                <div className="mt-2 text-[10px] font-mono text-indigo-300/80 truncate">
                  {ide.filename}
                </div>
              </button>
            )
          })}
        </div>

        {/* Active IDE Frame Showcase */}
        <div className="rounded-2xl bg-[#0D0F18] border border-white/10 overflow-hidden shadow-2xl relative shadow-[inset_0_1px_0_rgba(255,255,255,0.08)]">
          {/* OS Titlebar */}
          <div className="flex items-center justify-between px-4 py-3 bg-[#111422] border-b border-white/10">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-[#FF5F56] border border-[#E0443E]" />
              <div className="w-3 h-3 rounded-full bg-[#FFBD2E] border border-[#DEA123]" />
              <div className="w-3 h-3 rounded-full bg-[#27C93F] border border-[#1AAB29]" />
              <div className="ml-3 flex items-center gap-2">
                <span className="text-xs font-mono font-medium text-slate-200">{current.filename}</span>
                <span className="text-[10px] font-mono text-slate-500 hidden sm:inline">— {current.name}</span>
              </div>
            </div>

            <div className="flex items-center gap-2.5">
              <span className="text-[10px] font-mono text-indigo-300 hidden sm:inline-block bg-indigo-950/50 px-2 py-0.5 rounded border border-indigo-800/40">
                {current.badge}
              </span>
              {viewMode === 'code' ? (
                <button
                  onClick={handleCopyCode}
                  className="flex items-center gap-1 px-2 py-1 rounded text-[11px] font-mono text-slate-300 hover:text-white bg-white/5 hover:bg-white/10 border border-white/10 transition-colors"
                >
                  {copied ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                  <span>{copied ? 'Copied' : 'Copy'}</span>
                </button>
              ) : (
                <button
                  onClick={() => setZoomModal(current.screenshotPath)}
                  className="p-1 rounded-md text-slate-400 hover:text-white hover:bg-white/10 transition-colors"
                  title="Perbesar Screenshot"
                >
                  <Maximize2 className="w-3.5 h-3.5" />
                </button>
              )}
            </div>
          </div>

          {/* IDE Content Area */}
          <div className="p-4 sm:p-6 bg-[#07080E]">
            {viewMode === 'screenshot' ? (
              <div className="relative group rounded-xl overflow-hidden border border-white/10 bg-black/40">
                <img
                  src={current.screenshotPath}
                  alt={`${current.name} Screenshot`}
                  className="w-full max-h-[500px] object-contain mx-auto rounded-lg transition-transform duration-300 group-hover:scale-[1.008]"
                  loading="lazy"
                  onError={(e) => {
                    const target = e.target as HTMLImageElement
                    target.style.display = 'none'
                  }}
                />
                <div className="absolute bottom-3 right-3 bg-black/85 backdrop-blur-md px-3 py-1.5 rounded-lg border border-white/10 text-[11px] font-mono text-slate-300 flex items-center gap-1.5">
                  <Check className="w-3 h-3 text-emerald-400" />
                  <span>Pixel-Perfect Rendered Capture</span>
                </div>
              </div>
            ) : (
              <div className="rounded-xl bg-[#0A0C14] border border-white/5 p-4 sm:p-5 overflow-x-auto font-mono text-xs sm:text-sm text-slate-300 leading-relaxed max-h-[500px]">
                <pre>{current.codeSnippet}</pre>
              </div>
            )}

            {/* Folder structure & Runtime metrics */}
            <div className="mt-4 flex flex-wrap items-center justify-between gap-3 text-xs text-slate-400 pt-3 border-t border-white/5 font-mono">
              <div className="flex items-center gap-2">
                <FolderTree className="w-4 h-4 text-indigo-400" />
                <span className="truncate">Struktur: {current.structurePath}</span>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-slate-400">Runtime: <strong className="text-white font-mono tabular-nums">{current.runtimeMetric}</strong></span>
                <span className="text-emerald-400 font-medium">● {current.outputSample}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* High-res Zoom Modal */}
      {zoomModal && (
        <div
          onClick={() => setZoomModal(null)}
          className="fixed inset-0 z-50 bg-black/90 backdrop-blur-md flex items-center justify-center p-4 sm:p-8 cursor-pointer animate-in fade-in duration-200"
        >
          <div className="relative max-w-5xl w-full max-h-[90vh] bg-[#0E101A] rounded-2xl border border-white/15 overflow-hidden p-2 shadow-2xl">
            <img
              src={zoomModal}
              alt="Zoomed Screenshot"
              className="w-full h-auto max-h-[85vh] object-contain rounded-xl"
            />
            <div className="absolute top-4 right-4 bg-black/80 px-3 py-1 rounded-full text-xs text-white border border-white/20">
              Klik di mana saja untuk menutup
            </div>
          </div>
        </div>
      )}
    </section>
  )
}
