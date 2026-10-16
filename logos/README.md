# NgeLaprak Brand Identity & Logo Suite

Official vector logo design specifications and guidelines for **NgeLaprak** — The Universal Autonomous Laboratory Report Generator.

---

## 🎨 Design Concepts Overview

### Concept 1: The "Code Document N" (Primary Direction — Recommended)
- **Visual Metaphors**:
  - **The Letter 'N'**: Distinct, memorable brand mark.
  - **Academic Document Sheet**: Left spine/margins with standard academic 4-4-3-3 corner indicators.
  - **Compiler Acceleration Beam**: Dynamic geometric diagonal slash connecting code directly into academic reporting.
  - **AI Quantum Spark**: 4-point star in the top-right corner representing intelligent agent compilation.
- **Palette**:
  - Primary Indigo: `#4F46E5` (Brand anchor)
  - Deep Indigo: `#1E1B4B` (Background base)
  - Electric Cyan: `#38BDF8` (Terminal beam & AI spark)
  - Crisp White: `#FFFFFF` (Document readability)
- **Files**:
  - `logos/concept-1-code-document-n/logo-icon.svg`
  - `logos/concept-1-code-document-n/logo-horizontal.svg`
  - `logos/concept-1-code-document-n/logo-monochrome-dark.svg`
  - `logos/concept-1-code-document-n/logo-monochrome-light.svg`

---

### Concept 2: The "Hex Compiler Emblem"
- **Visual Metaphors**:
  - Modern isometric developer tool emblem (Docker / Rust / Node style).
  - 3D cube where the top face is a document sheet, left face is a terminal console (`> _`), and right face is structured academic margins.
- **Files**:
  - `logos/concept-2-hex-compiler/logo-icon.svg`
  - `logos/concept-2-hex-compiler/logo-horizontal.svg`

---

### Concept 3: The "Lab Flask & Code Solution"
- **Visual Metaphors**:
  - Chemistry / informatics laboratory Erlenmeyer flask.
  - The liquid solution is composed of nested code syntax brackets `{ }` and floating compilation bubbles.
- **Files**:
  - `logos/concept-3-lab-flask-code/logo-icon.svg`
  - `logos/concept-3-lab-flask-code/logo-horizontal.svg`

---

## 📐 Usage Guidelines

### Clear Space
Maintain clear space equal to at least 25% of the logo's width around all sides.

### Minimum Sizes
- **Digital Icon Only**: 16×16px (Favicon), 24×24px (Navbar badge), 64×64px (App icon)
- **Horizontal Lockup**: Minimum width 140px

### Exporting to PNG (High Resolution)
```bash
# Inkscape
inkscape logos/concept-1-code-document-n/logo-icon.svg --export-filename=logo-icon.png --export-width=512

# ImageMagick
magick -background none logos/concept-1-code-document-n/logo-icon.svg -resize 512x512 logo-icon.png
```
