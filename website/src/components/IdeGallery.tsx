import React, { useState } from 'react'
import { Monitor, Code, Maximize2, Check, Copy } from 'lucide-react'
import { ImageDithering } from '@paper-design/shaders-react'

interface IdeProfile {
  id: string
  name: string
  lang: string
  filename: string
  screenshotPath: string
  colorFront: string
  colorHighlight: string
  codeSnippet: string
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
      lang: 'Java / Swing',
      filename: 'KoneksiDB.java',
      screenshotPath: '/samples/adpl/screenshots/1_KoneksiDB_NetBeans.png',
      colorFront: '#4f46e5',
      colorHighlight: '#818cf8',
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
      lang: 'C / C++',
      filename: 'Stack.h',
      screenshotPath: '/samples/strukdat/screenshots/1_Stack_h_CodeBlocks.png',
      colorFront: '#3b82f6',
      colorHighlight: '#93c5fd',
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
      name: 'VS Code',
      lang: 'Python / JS',
      filename: 'dijkstra.py',
      screenshotPath: '/samples/strukdat/screenshots/2_main_cpp_CodeBlocks.png',
      colorFront: '#6366f1',
      colorHighlight: '#c7d2fe',
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
      name: 'Terminal / SQL',
      lang: 'SQL / Shell',
      filename: 'query.sql',
      screenshotPath: '/samples/adpl/screenshots/4_MySQL_Terminal.png',
      colorFront: '#059669',
      colorHighlight: '#34d399',
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
    <section id="gallery" className="py-20 md:py-28 relative overflow-hidden bg-[#090A0F]">
      {/* Dynamic Image Dithering Background linked to the active IDE screenshot */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none select-none z-0">
        <ImageDithering
          key={current.id}
          width="100%"
          height="100%"
          image={current.screenshotPath}
          colorBack="#090a0f"
          colorFront={current.colorFront}
          colorHighlight={current.colorHighlight}
          originalColors={false}
          inverted={false}
          type="8x8"
          size={3}
          colorSteps={2}
          fit="cover"
          className="w-full h-full opacity-25 md:opacity-35 transition-opacity duration-700"
        />
        {/* Soft radial vignette & vertical gradient overlay to guarantee text legibility & smooth section blending */}
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(9,10,15,0.4)_0%,transparent_55%,#090A0F_88%)]" />
        <div className="absolute inset-0 bg-gradient-to-b from-[#090A0F] via-transparent to-[#090A0F]" />
      </div>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 relative z-10">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-10">
          <div>
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-mono uppercase tracking-wider mb-3">
              <Monitor className="w-3.5 h-3.5" />
              <span>Galeri IDE</span>
            </div>
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-white tracking-[-0.035em] font-sans [text-wrap:balance]">
              Screenshot IDE Asli,{' '}
              <span className="text-indigo-400">Tanpa Watermark</span>
            </h2>
            <p className="text-slate-400 text-sm sm:text-base mt-2 max-w-xl [text-wrap:pretty]">
              Visual tangkapan layar IDE berstandar sistem operasi yang otomatis disematkan rapi ke bab pembahasan.
            </p>
          </div>

          {/* Screenshot / Code View Mode Toggle */}
          <div className="flex items-center bg-[#0D0F18]/90 backdrop-blur-md p-1 rounded-xl border border-white/10 self-start md:self-auto shadow-inner">
            <button
              onClick={() => setViewMode('screenshot')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all active:scale-[0.98] cursor-pointer ${
                viewMode === 'screenshot'
                  ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <Monitor className="w-3.5 h-3.5" />
              <span>Screenshot</span>
            </button>
            <button
              onClick={() => setViewMode('code')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all active:scale-[0.98] cursor-pointer ${
                viewMode === 'code'
                  ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <Code className="w-3.5 h-3.5" />
              <span>Kode</span>
            </button>
          </div>
        </div>

        {/* Minimalist IDE Selector Tabs */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 mb-6">
          {ideList.map((ide) => {
            const isActive = activeTab === ide.id
            return (
              <button
                key={ide.id}
                onClick={() => setActiveTab(ide.id)}
                className={`py-3 px-4 rounded-xl border text-center transition-all duration-200 active:scale-[0.98] cursor-pointer backdrop-blur-sm ${
                  isActive
                    ? 'bg-indigo-600/25 border-indigo-500/60 text-white shadow-lg shadow-indigo-950/40 ring-1 ring-indigo-500/30'
                    : 'bg-[#0D0F18]/80 border-white/8 text-slate-400 hover:text-white hover:border-white/15 hover:bg-[#101320]'
                }`}
              >
                <div className="font-bold text-xs sm:text-sm">{ide.name}</div>
              </button>
            )
          })}
        </div>

        {/* Active IDE Frame Showcase */}
        <div className="rounded-2xl bg-[#0D0F18]/90 backdrop-blur-md border border-white/10 overflow-hidden shadow-2xl relative">
          {/* OS Titlebar */}
          <div className="flex items-center justify-between px-4 py-3 bg-[#111422]/95 border-b border-white/10">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-[#FF5F56] opacity-80" />
              <div className="w-3 h-3 rounded-full bg-[#FFBD2E] opacity-80" />
              <div className="w-3 h-3 rounded-full bg-[#27C93F] opacity-80" />
              <span className="ml-3 text-xs font-mono font-medium text-slate-300">{current.filename}</span>
            </div>

            <div className="flex items-center gap-2">
              {viewMode === 'code' ? (
                <button
                  onClick={handleCopyCode}
                  className="flex items-center gap-1.5 px-2.5 py-1 rounded text-xs font-mono text-slate-300 hover:text-white bg-white/5 hover:bg-white/10 border border-white/10 transition-colors cursor-pointer"
                >
                  {copied ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                  <span>{copied ? 'Tersalin' : 'Salin'}</span>
                </button>
              ) : (
                <button
                  onClick={() => setZoomModal(current.screenshotPath)}
                  className="p-1 rounded-md text-slate-400 hover:text-white hover:bg-white/10 transition-colors cursor-pointer"
                  title="Perbesar"
                >
                  <Maximize2 className="w-3.5 h-3.5" />
                </button>
              )}
            </div>
          </div>

          {/* IDE Content Area */}
          <div className="p-3 sm:p-5 bg-[#07080E]/95">
            {viewMode === 'screenshot' ? (
              <div className="relative group rounded-xl overflow-hidden border border-white/10 bg-black/40">
                <img
                  src={current.screenshotPath}
                  alt={`${current.name} Screenshot`}
                  className="w-full max-h-[520px] object-contain mx-auto rounded-lg transition-transform duration-300 group-hover:scale-[1.005]"
                  loading="lazy"
                  onError={(e) => {
                    const target = e.target as HTMLImageElement
                    target.style.display = 'none'
                  }}
                />
              </div>
            ) : (
              <div className="rounded-xl bg-[#0A0C14] border border-white/5 p-4 sm:p-5 overflow-x-auto font-mono text-xs sm:text-sm text-slate-300 leading-relaxed max-h-[500px]">
                <pre>{current.codeSnippet}</pre>
              </div>
            )}
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
          </div>
        </div>
      )}
    </section>
  )
}
