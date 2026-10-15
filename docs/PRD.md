# Product Requirements Document (PRD)
## NgeLaprak — Official Showcase Website

---

### 1. Executive Summary

- **Problem Statement**:
  Mahasiswa teknik informatika dan sains komputer seringkali menghabiskan waktu berjam-jam untuk memformat laporan praktikum (laprak) secara manual, menyusun screenshot IDE yang berantakan, serta menghadapi risiko plagiarisme template. Meskipun skill AI `NgeLaprak` hadir sebagai solusi terautomasi via Agentic AI & CLI, banyak calon pengguna belum memahami kapabilitasnya secara visual dan kesulitan menemukan cara instalasi yang instan.

- **Proposed Solution**:
  Membangun website *showcase landing page* satu halaman (single-page) bertema dark modern ala Supaste yang memvisualisasikan keunggulan skill `NgeLaprak` secara padat, minim teks, dan kaya animasi interaktif: mengubah 3 berkas praktikum (kode sumber, petunjuk/modul, dan template) langsung menjadi dokumen Word (.docx) & PDF (.pdf) siap kumpul lengkap dengan screenshot IDE autentik.

- **Success Criteria**:
  1. **Speed & Performance**: Website memuat halaman pertama (First Contentful Paint) dalam waktu < 0.8 detik dan mencapai skor Google Lighthouse Performance >= 95.
  2. **Copy Conversion Rate**: Tingkat klik tombol "Copy Command" (`npx skills add SatriaBaktiWijaya/NgeLaprak`) mencapai >= 25% dari total kunjungan unik.
  3. **Visual Engagement**: Rata-rata durasi sesi pengunjung (Average Session Duration) >= 60 detik berkat interaksi scroll motion GSAP dan visual shader dithering.
  4. **Zero Layout Shifts**: Cumulative Layout Shift (CLS) = 0 pada perangkat desktop maupun mobile.

---

### 2. User Experience & Functionality

#### User Personas

1. **Mahasiswa Praktikan (Primary Persona - "Rian, Mahasiswa Semester 3")**:
   - *Karakteristik*: Sering dikejar deadline mingguan praktikum Struktur Data / Pemrograman Berorientasi Objek. Butuh tool yang cepat, tidak ribet, dan menghasilkan laporan dengan struktur folder rapi standar industri (NetBeans/VS Code).
   - *Kebutuhan*: Ingin melihat bukti visual hasil laprak (.pdf/.docx), format screenshot kode, dan perintah satu baris untuk memasang tool di AI IDE mereka (Cursor, Gemini CLI, Claude Code).

2. **Asisten Laboratorium / Dosen (Secondary Persona - "Kak Dian, Asisten Lab")**:
   - *Karakteristik*: Menilai ratusan laporan per minggu dan membenci laporan hasil plagiarisme/copas seragam.
   - *Kebutuhan*: Memastikan bahwa laporan yang digenerate oleh mahasiswa memiliki orisinalitas tinggi, penjelasan alami (natural student voice), dan screenshot kode yang benar-benar bisa dijalankan.

3. **AI Engineer / Agentic Developer (Tertiary Persona - "Budi, Open Source Contributor")**:
   - *Karakteristik*: Ingin mengeksplorasi ekosistem AI skills standar open-source.
   - *Kebutuhan*: Memeriksa dokumentasi instalasi repo, arsitektur skill, dan kompatibilitas format.

---

#### User Stories & Acceptance Criteria

- **Story 1 (Instalasi 1-Klik)**:
  *Sebagai mahasiswa praktikan, saya ingin menyalin perintah instalasi satu baris langsung dari halaman utama agar saya bisa segera menggunakannya di AI agent saya tanpa membaca dokumentasi panjang.*
  - **Acceptance Criteria**:
    - [x] Tombol CTA terminal di Hero section menampilkan teks `npx skills add SatriaBaktiWijaya/NgeLaprak`.
    - [x] Sekali klik tombol copy, perintah tersalin ke clipboard sistem.
    - [x] Muncul feedback visual micro-animation (ikon berubah menjadi centang hijau dan teks "Tersalin!" selama 2 detik).
    - [x] Disediakan toggle tab alternatif: `npx`, `powershell (install.ps1)`, dan `bash (install.sh)`.

- **Story 2 (Visualisasi Pipeline 3 File)**:
  *Sebagai pengunjung, saya ingin memahami cara kerja NgeLaprak melalui ilustrasi visual 3 langkah agar saya langsung mengerti tanpa harus membaca paragraf instruksi yang panjang.*
  - **Acceptance Criteria**:
    - [x] Visual interaktif menampilkan 3 ikon berkas input: `1. Source Code`, `2. Modul/Soal Praktikum`, `3. Template Word / Format Bebas`.
    - [x] Efek partikel/aliran garis neon menghubungkan ketiga berkas menuju AI Core NgeLaprak.
    - [x] Output bercabang menjadi 2 berkas berkelas: `Laporan_Praktikum.docx` dan `Laporan_Praktikum.pdf`.
    - [x] Scroll-triggered reveal menggunakan GSAP memunculkan langkah secara bertahap saat pengguna scroll ke bawah.

- **Story 3 (Galeri Screenshot IDE Autentik)**:
  *Sebagai pengguna potensial, saya ingin melihat contoh screenshot kode yang di-generate agar saya yakin hasilnya bukan sekadar teks mentah melainkan tampilan IDE nyata.*
  - **Acceptance Criteria**:
    - [x] Bento grid / carousel interaktif menampilkan 4 profil IDE: **Apache NetBeans (Java)**, **Code::Blocks (C/C++)**, **VS Code (Python/Web)**, dan **DBeaver (Basis Data/SQL)**.
    - [x] Setiap frame jendela menampilkan window header bergaya OS asli (traffic light buttons, titlebar) dengan syntax highlighting elegan.
    - [x] Interaksi zoom / preview modal resolusi tinggi saat kartu diklik atau di-hover.

- **Story 4 (Perbandingan Before / After)**:
  *Sebagai mahasiswa yang sering pusing dengan folder berantakan, saya ingin melihat perbandingan visual sebelum dan sesudah menggunakan NgeLaprak.*
  - **Acceptance Criteria**:
    - [x] Slider perbandingan atau side-by-side card:
      - **Before**: 1 file main.java acak-acakan di desktop, gambar screenshot buram terpotong, format Word berantakan.
      - **After**: Struktur Maven/NetBeans rapi (`src/main/java`), folder `screenshots/` otomatis, Word rapi 2 spasi & heading terstandarisasi.
    - [x] Indikator visual hijau/merah yang kontras dan informatif.

- **Story 5 (Fitur Unggulan Minimalis)**:
  *Sebagai pengunjung, saya ingin mengetahui 4 pilar utama NgeLaprak dalam kartu visual yang padat dan menarik.*
  - **Acceptance Criteria**:
    - [x] 4 Kartu Bento Fitur:
      1. **Autonomous Scaffold**: Struktur folder NetBeans & C++ standar otomatis.
      2. **Anti-Plagiat Engine**: Frasa dan penjelasan unik per mahasiswa.
      3. **Real IDE Renderer**: Sintaks berwarna tajam tanpa watermark aneh.
      4. **Bilingual & Multi-Format**: Output ganda .docx & .pdf seketika.
    - [x] Efek hover kartu dengan glowing gradient border dan pergeseran depth (tilt).

---

#### Non-Goals

1. **Bukan Web Generator / Web-based Laprak Editor**: Website ini murni bersifat *product showcase & landing page*. Proses pembuatan laprak tetap dijalankan di lingkungan lokal/CLI mahasiswa bersama AI agent.
2. **Tidak Menggunakan Sistem Autentikasi / Akun**: Tidak ada login Google/GitHub, penyimpanan database pengguna, atau profil berbayar.
3. **Bukan Dokumentasi Multi-Halaman Kompleks**: Menghindari dokumentasi teks tebal seperti Docusaurus; informasi disajikan seringkas dan sevisual mungkin.

---

### 3. AI System Requirements (Showcase Integration)

- **Showcase Tooling**:
  Website mengarahkan mahasiswa ke integrasi skill resmi:
  - Ekosistem Agent Skills: `npx skills add SatriaBaktiWijaya/NgeLaprak`
  - GitHub Repository Source: `https://github.com/SatriaBaktiWijaya/NgeLaprak`
  - Kompatibel dengan: Cursor, Google Antigravity, Claude Code, GitHub Copilot.

- **Simulasi Hasil AI (Interactive Preview)**:
  Halaman menyediakan komponen interaktif interaktif di mana pengunjung dapat membolak-balik lembar halaman laporan simulasi (Mockup PDF Viewer) untuk memeriksa konsistensi typography, penempatan screenshot gambar berseri, dan bab pembahasan.

---

### 4. Technical Specifications

#### Architecture Overview
- **Core Framework**: React 18+ dibangun di atas Vite (Fast HMR & Optimized Static Build).
- **Styling System**: Tailwind CSS dengan konfigurasi custom design tokens (Dark palette, glassmorphism, Satoshi typography).
- **Animation & Motion**:
  - `gsap` + `ScrollTrigger` untuk kinetic scroll reveals dan pinning animations.
- **Visual Shaders & Dithering**:
  - `@paper-design/shaders-react` untuk efek retro-modern computing dithering dan subtle organic canvas background.
- **Icons**:
  - `@heroicons-animated/bell-slash` dan Lucide React untuk ikon UI modern.
- **Typography**:
  - Font primer: **Satoshi** (Google Fonts / Fontshare CDN).
  - Font kode: **JetBrains Mono**.

#### Integration Points
- **Clipboard API**: `navigator.clipboard.writeText` dengan graceful fallback untuk eksekusi copy command instan.
- **Social & Community Links**: Tautan terverifikasi ke GitHub repository, rilis npm, dan profil developer.

#### Security & Privacy
- **Client-Side Only**: 100% static assets, tidak ada pengumpulan cookies, analitik invasif, atau pengiriman data pribadi pengguna.
- **Content Security Policy (CSP)**: Kompatibel dengan hosting statis modern tanpa script inline yang rentan.

---

### 5. Risks & Roadmap

#### Phased Rollout
- **Phase 1 (MVP)**:
  - Single-page showcase lengkap dengan 7 bagian (Hero, Pipeline, Features, Gallery, Before/After, Install, Footer).
  - Setup Shader Dithering & GSAP Smooth Transitions.
  - Deployment ke Vercel dengan custom domain / sub-domain.
- **Phase 2 (Interactive Playground)**:
  - Drag-and-drop file mock reader yang mendemonstrasikan visual preview instan bagaimana nama mahasiswa dan NIM diekstrak.
- **Phase 3 (Community Gallery)**:
  - Showcase karya laporan mahasiswa dari berbagai kampus di Indonesia.

#### Technical Risks & Mitigation
| Risiko | Dampak | Strategi Mitigasi |
| :--- | :--- | :--- |
| **GPU Load Shader Dithering** | HP spek rendah bisa lag atau panas | Shader hanya aktif pada viewport desktop atau dikonfigurasi dengan fps throttle / CSS fallback halus pada mobile |
| **GSAP Scroll Jank** | Scroll terasa tersendat di browser Safari/Mobile | Gunakan CSS `will-change` secara bijak dan matikan scroll trigger yang terlalu kompleks di layar sentuh kecil |
| **Font Loading Shift (FOUT)** | Perubahan layout saat font Satoshi dimuat | Gunakan `font-display: swap` dan preload link font di `<head>` |

