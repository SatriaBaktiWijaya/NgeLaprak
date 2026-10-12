---
name: NgeLaprak Showcase Website
colors:
  background-deep: "#08090E"
  background-canvas: "#0D0F18"
  surface-card: "#131625"
  surface-card-hover: "#1A1E33"
  surface-border: "#20263D"
  surface-border-glow: "#6366F1"
  primary-indigo: "#6366F1"
  primary-purple: "#8B5CF6"
  primary-violet: "#A855F7"
  accent-cyan: "#06B6D4"
  accent-glow: "#4F46E5"
  text-primary: "#F8FAFC"
  text-secondary: "#94A3B8"
  text-muted: "#64748B"
  state-success: "#10B981"
  state-warning: "#F59E0B"
  state-error: "#EF4444"
---

# Design System: NgeLaprak Showcase Website

## 1. Visual Theme & Atmosphere

Website showcase NgeLaprak mengusung konsep visual **"Luminous Dark Modern Developer Precision"** yang terinspirasi dari estetika modern alat pengembang papan atas seperti Supaste, Linear, dan Raycast. Berlandaskan kanvas hitam pekat bergradasi kosmik (`#08090E` hingga `#0D0F18`), antarmuka memancarkan aura futuristik yang tenang namun memikat. Aksen pendaran cahaya (glowing aura) dalam spektrum biru-ungu elektrik (`#6366F1` ke `#8B5CF6`) membingkai elemen-elemen penting, memandu mata pengunjung secara natural ke setiap titik fokus tanpa terasa silau atau berlebihan. Efek tekstur shader dithering dari `@paper-design/shaders-react` menghadirkan sentuhan retro-analog computing yang elegan di latar belakang hero section, merepresentasikan perpaduan presisi kode klasik dengan kecerdasan generasi AI mutakhir.

Filosofi inti dari pengalaman pengguna adalah **"Show, Don't Tell"** (Visual-First, Minimum Text). Sebagai sarana showcase bagi mahasiswa teknik dan pengembang, halaman meminimalkan paragraf teks naratif dan menggantinya dengan mockup interaktif beresolusi tinggi: frame jendela IDE asli dengan traffic light buttons, simulasi visual aliran 3 berkas menjadi dokumen PDF/Word resmi, dan animasi kinetik bertenaga GSAP yang merespons setiap putaran scroll secara mulus dan responsif. Pengunjung langsung merasakan bahwa NgeLaprak adalah produk yang solid, teruji, dan siap menuntaskan tugas kuliah mereka dengan standar profesional.

---

## 2. Color Palette & Roles

### Primary Foundation
- **"Deep Cosmic Void" (`#08090E`)**: Warna dasar halaman web terluar, memberikan kedalaman ruang tanpa batas dan kontras maksimal untuk teks terang.
- **"Obsidian Surface" (`#0D0F18`)**: Warna latar belakang canvas section dan container utama.
- **"Midnight Glass Card" (`#131625` / RGBA `rgba(19, 22, 37, 0.75)`)**: Warna permukaan kartu (bento cards) dengan efek backdrop-blur 16px untuk glassmorphism modern.
- **"Hover Elevation" (`#1A1E33`)**: State hover kartu untuk memberi respons interaktif saat kursor menyentuh elemen.
- **"Subtle Hairline Border" (`#20263D`)**: Garis tepi 1px presisi pada kartu dan container, menjaga struktur layout tetap rapi tanpa terasa kasar.

### Accent & Interactive
- **"Electric Indigo" (`#6366F1`)**: Warna brand primer dan tombol CTA utama. Digunakan untuk ikon aktif, status sukses download, dan gradient awal.
- **"Cyber Violet" (`#8B5CF6`)**: Gradien pendamping indigo, menghasilkan transisi spektrum cahaya techy premium pada teks judul dan tombol.
- **"Neon Cyan Accent" (`#06B6D4`)**: Aksen kontras mikro untuk menyorot kata kunci penting, badge "v1.2 Released", dan efek partikel data.
- **"Indigo Ambient Glow" (`rgba(99, 102, 241, 0.25)`)**: Radial glow di belakang terminal hero dan judul untuk menciptakan ilusi pencahayaan ruangan gelap.

### Typography & Text Hierarchy
- **"Pure White Glow" (`#F8FAFC`)**: Digunakan untuk judul utama (Display Heading), angka statistik, dan teks tombol primer.
- **"Cool Slate Secondary" (`#94A3B8`)**: Digunakan untuk sub-judul, deskripsi singkat fitur, dan label navigasi.
- **"Muted Steel" (`#64748B`)**: Digunakan untuk teks bantuan mikro, footer copyright, dan teks placeholder yang tidak boleh mencuri perhatian.

### Functional States
- **"Emerald Active" (`#10B981`)**: State sukses (indikator "Tersalin ke Clipboard", status "Build Passing", checklist validasi laprak).
- **"Amber Warning" (`#F59E0B`)**: Indikator file input yang membutuhkan perhatian (e.g. template kustom terdeteksi).
- **"Crimson Alert" (`#EF4444`)**: Menandai kegagalan format atau perbandingan kondisi "Before" (laprak tidak terstruktur).

---

## 3. Typography Rules

### Hierarchy & Weights
Typography dibangun menggunakan jenis huruf **Satoshi** (modern geometric grotesque sans-serif) yang dipadukan dengan **JetBrains Mono** untuk representasi baris kode dan CLI:

| Level | Font Family | Size | Weight | Line Height | Letter Spacing | Penggunaan |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Hero Display** | Satoshi | `3.5rem` – `4.5rem` (56px–72px) | 800 (Bold / Extrabold) | 1.05 | `-0.03em` | Tagline utama di Hero Section |
| **Section Title** | Satoshi | `2.25rem` – `2.75rem` (36px–44px) | 700 (Bold) | 1.15 | `-0.02em` | Judul setiap bab showcase |
| **Card Heading** | Satoshi | `1.25rem` – `1.5rem` (20px–24px) | 600 (Semibold) | 1.25 | `-0.01em` | Judul fitur pada kartu bento |
| **Body Large** | Satoshi | `1.125rem` (18px) | 400 (Regular) | 1.6 | `normal` | Sub-tagline di bawah hero |
| **Body Standard**| Satoshi | `0.9375rem` (15px) | 400 (Regular) | 1.5 | `normal` | Keterangan ringkas fitur kartu |
| **Code / CLI** | JetBrains Mono| `0.875rem` (14px) | 500 (Medium) | 1.4 | `-0.01em` | Baris perintah `npx skills add` & cuplikan kode |
| **Badge / Meta** | Satoshi | `0.75rem` (12px) | 600 (Semibold) | 1.0 | `0.05em` (Caps) | Tag kategori, versi, status "Auto-Generated" |

### Spacing Principles
- Heading menggunakan letter-spacing negatif (`-0.02em` hingga `-0.03em`) untuk menghasilkan impresi kokoh, presisi, dan padat khas desain Silicon Valley.
- Body text dibatasi maksimal 2–3 kalimat per blok dengan line-height rileks (1.5–1.6) untuk mematuhi prinsip *minimalist reading cognitive load*.

---

## 4. Component Stylings

### Buttons
1. **Primary Glowing CTA (`.btn-primary`)**:
   - Background: Gradien linier 135deg dari `#6366F1` ke `#8B5CF6`.
   - Corner Radius: `9999px` (Full Pill) atau `12px` (Modern Rounded).
   - Shadow: `0 0 20px rgba(99, 102, 241, 0.45)`, bertambah intens saat hover (`0 0 32px rgba(99, 102, 241, 0.7)`).
   - Hover Transition: `all 0.25s cubic-bezier(0.16, 1, 0.3, 1)`, scale `1.03`.

2. **Terminal Copy Button (`.btn-terminal`)**:
   - Background: `#0E111D` dengan border hairline `#252B44`.
   - Monospace text dengan ikon copy interaktif di sisi kanan.
   - Click Feedback: Micro-animation dengan ikon ceklis hijau dan teks berubah menjadi "Copied to clipboard!".

3. **Ghost Secondary Button (`.btn-ghost`)**:
   - Background: `transparent`, border: `1px solid rgba(255, 255, 255, 0.1)`.
   - Hover State: Background `rgba(255, 255, 255, 0.05)`, border `rgba(255, 255, 255, 0.2)`.

### Cards & Containers
- **Bento Grid Cards**:
  - Background: Glassmorphic dark card (`rgba(19, 22, 37, 0.65)` dengan `backdrop-filter: blur(16px)`).
  - Border: 1px `rgba(255, 255, 255, 0.08)`.
  - Corner Radius: `20px`.
  - Hover Effect: Subtle 3D tilt gesture dengan GSAP/CSS transform dan glowing highlight mengikuti pergerakan kursor (radial gradient mask).

### Navigation
- **Floating Blur Pill Bar**:
  - Posisi: `fixed top-6 left-1/2 -translate-x-1/2 z-50`.
  - Padding: `8px 24px`.
  - Corner Radius: `9999px` (Pill shape).
  - Background: `rgba(13, 15, 24, 0.8)` didukung `backdrop-filter: blur(20px)` dan border halus.
  - Elemen: Logo NgeLaprak (ikon buku + kilat AI), tautan jangkar (Alur, Fitur, Galeri, Panduan), serta tombol GitHub Star.

### Domain-Specific Components

1. **3-File Drop Pipeline Visualizer**:
   - **Tampilan Kiri (Inputs)**: 3 kartu berkas melayang (1. Kode Sumber `.java/.cpp`, 2. Modul `.pdf`, 3. Template `.docx`).
   - **Tampilan Tengah (The Engine)**: Lingkaran reaktor "NgeLaprak Agent" berpendar dengan efek orbit partikel.
   - **Tampilan Kanan (Outputs)**: Dokumen ganda Word berhias ribbon biru dan PDF berhias ribbon merah dengan pratinjau halaman pertama.

2. **Authentic IDE Screenshot Frame**:
   - Frame jendela bernuansa macOS dark: 3 bulatan warna-warni (merah, kuning, hijau) di pojok kiri atas, nama file di tengah titlebar (`Main.java`, `Graph.cpp`).
   - Editor gutter dengan nomor baris halus.
   - Kode sumber berwarna dengan palet tema One Dark / Dracula yang tajam dan nyaman dibaca.

3. **Before / After Comparison Splitter**:
   - Sisi Kiri ("Before"): Dokumen kusut, screenshot buram, format spasi berantakan bertanda silang merah.
   - Sisi Kanan ("After"): Dokumen terstruktur, margin standar 4-4-3-3, diagram UML rapi, format cover otomatis bertanda centang emas.

---

## 5. Layout Principles

### Grid & Structure
- **Max Content Width**: `1200px` terpusat (`margin: 0 auto; padding: 0 24px;`).
- **Bento Layout**: Grid 12 kolom responsif:
  - Desktop (>1024px): 3–4 kolom bento cards bervariasi ukuran span (col-span-8 & col-span-4).
  - Tablet (768px–1023px): 2 kolom seimbang.
  - Mobile (<768px): 1 kolom vertikal rapi.

### Whitespace Strategy
- Jarak antar seksi besar: `100px` – `140px` untuk memberikan ruang nafas visual (breathable luxury).
- Gap antar kartu: `24px` konsisten.

### Alignment & Visual Balance
- Hero section terpusat secara optik (Centric Optical Alignment) dengan pendaran latar belakang simetris.
- Bagian alur dan fitur menggunakan variasi asimetris untuk menjaga mata tetap aktif menelusuri konten.

### Responsive Behavior & Touch
- Target sentuh tombol mobile minimal `48px x 48px` untuk aksesibilitas jempol optimal.
- Efek hover dinonaktifkan di layar sentuh, diganti dengan transisi sekali sentuh yang responsif.

---

## 6. Design System Notes for Stitch Generation

### Language to Use
- *"Dark futuristic developer tool with deep indigo glowing gradients"*
- *"Sleek minimalist interface with ultra-low text density and heavy visual impact"*
- *"Authentic IDE frames with crisp syntax highlighting and glassmorphic bento cards"*
- *"Smooth retro computing dithering shaders merged with high-end modern SaaS aesthetics"*

### Color References
- Primary Indigo: `#6366F1`
- Cyber Violet: `#8B5CF6`
- Cosmic Void: `#08090E`
- Obsidian Canvas: `#0D0F18`
- Text White: `#F8FAFC`
- Text Slate: `#94A3B8`

### Component Prompts
- **Hero Section**: *"A dark mode hero section for NgeLaprak developer tool, large Satoshi display headline 'Ubah 3 File Jadi Laporan Praktikum Sempurna', single-line glowing terminal with 'npx skills add ngelaprak' copy button, surrounded by deep purple ambient glow and subtle dithering mesh texture."*
- **Pipeline Section**: *"An interactive 3-step pipeline graphic showing three input files (code, module, template) converging into an illuminated AI engine core and splitting into two finished Word and PDF document mockups."*
- **IDE Showcase**: *"A bento grid of 4 IDE application frames showcasing Java in Apache NetBeans, C++ in Code::Blocks, Python in VS Code, and SQL in DBeaver with realistic title bars and syntax highlighted code."*

### Incremental Iteration
- Mulai dari struktur pondasi canvas dan floating navbar.
- Bangun Hero terminal dan shader dithering canvas.
- Lanjutkan dengan visualisasi pipeline 3 berkas dan galeri IDE bento grid.
- Akhiri dengan integrasi GSAP ScrollTrigger untuk animasi reveal yang mewah.
