"""
NgeLaprak Anti-Trap Full Defense-in-Depth Module.

Protects AI agents from prompt-injection traps, hidden instructions, and canary
watermarks embedded across academic documents, images, slides, spreadsheets,
markup files, notebooks, and starter source code.

Layers:
  1. PDF Dual-Engine (`pymupdf` primary with pixel-contrast/occlusion sampling,
     `pdfplumber` fallback, `pypdf` fallback)
  2. Images & Photos (`PNG`, `JPG`, `JPEG`, `WEBP`, `BMP`, `GIF` via Pillow
     metadata stripping + alpha-channel flattening + alpha-stego detection;
     `SVG` XML/CSS/off-canvas stripping)
  3. Academic Formats (`DOCX`, `PPTX`, `XLSX`, `HTML`, `Markdown`, `.ipynb`,
     starter source code)
  4. Unicode & Text Steganography (zero-width, Tag Block, Variation Selectors,
     Bidi Override / Trojan Source, cross-script homoglyph normalization)
  5. Semantic Trap / Honeypot Detection & Forbidden Identifier Extraction
  6. Final Codebase Audit (`audit_code_for_traps`)
"""

from __future__ import annotations

import io
import json
import math
import os
import re
import tempfile
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass, field
from html.parser import HTMLParser
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple, Union


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

class TrapRecord(dict):
    """Dictionary with attribute access for ergonomic usage & native JSON export."""

    def __getattr__(self, name: str) -> Any:
        try:
            return self[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def __setattr__(self, name: str, value: Any) -> None:
        self[name] = value


@dataclass
class SanitizationReport:
    clean_text: str = ""
    stripped_traps: List[TrapRecord] = field(default_factory=list)
    semantic_warnings: List[TrapRecord] = field(default_factory=list)
    forbidden_identifiers: List[str] = field(default_factory=list)
    sanitized_image_path: Optional[str] = None
    engine_used: str = "none"
    risk_level: str = "none"
    file_type: str = "unknown"
    stats: Dict[str, Any] = field(default_factory=dict)
    source_path: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_path": self.source_path,
            "file_type": self.file_type,
            "engine_used": self.engine_used,
            "risk_level": self.risk_level,
            "clean_text": self.clean_text,
            "stripped_traps": [dict(t) for t in self.stripped_traps],
            "semantic_warnings": [dict(w) for w in self.semantic_warnings],
            "forbidden_identifiers": list(self.forbidden_identifiers),
            "sanitized_image_path": self.sanitized_image_path,
            "stats": dict(self.stats),
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

    def save_json(self, out_path: str) -> str:
        os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(self.to_json())
        return os.path.abspath(out_path)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SanitizationReport":
        return cls(
            clean_text=data.get("clean_text", ""),
            stripped_traps=[TrapRecord(t) for t in data.get("stripped_traps", [])],
            semantic_warnings=[TrapRecord(w) for w in data.get("semantic_warnings", [])],
            forbidden_identifiers=list(data.get("forbidden_identifiers", [])),
            sanitized_image_path=data.get("sanitized_image_path"),
            engine_used=data.get("engine_used", "none"),
            risk_level=data.get("risk_level", "none"),
            file_type=data.get("file_type", "unknown"),
            stats=dict(data.get("stats", {})),
            source_path=data.get("source_path"),
        )


def _make_trap(
    reason: str,
    text: str,
    location: str = "",
    severity: str = "high",
    details: Optional[Dict[str, Any]] = None,
) -> TrapRecord:
    return TrapRecord(
        reason=reason,
        text=(text or "").strip(),
        location=location,
        severity=severity,
        details=details or {},
    )


def _make_warning(
    category: str,
    text: str,
    location: str = "",
    pattern: str = "",
    needs_user_confirmation: bool = True,
    severity: str = "high",
    candidates: Optional[List[str]] = None,
) -> TrapRecord:
    return TrapRecord(
        category=category,
        text=(text or "").strip(),
        location=location,
        pattern=pattern,
        needs_user_confirmation=needs_user_confirmation,
        severity=severity,
        candidates=list(candidates or []),
    )


# ---------------------------------------------------------------------------
# Color & WCAG Contrast Utilities
# ---------------------------------------------------------------------------

_NAMED_COLORS: Dict[str, Tuple[int, int, int]] = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 128, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "gray": (128, 128, 128),
    "grey": (128, 128, 128),
    "lightgray": (211, 211, 211),
    "lightgrey": (211, 211, 211),
    "silver": (192, 192, 192),
    "whitesmoke": (245, 245, 245),
    "snow": (255, 250, 250),
    "ivory": (255, 255, 240),
    "ghostwhite": (248, 248, 255),
    "aliceblue": (240, 248, 255),
    "beige": (245, 245, 220),
    "floralwhite": (255, 250, 240),
    "seashell": (255, 245, 238),
    "linen": (250, 240, 230),
    "offwhite": (250, 250, 250),
}


def _srgb_to_linear(channel_01: float) -> float:
    return channel_01 / 12.92 if channel_01 <= 0.03928 else ((channel_01 + 0.055) / 1.055) ** 2.4


def relative_luminance(rgb: Tuple[int, int, int]) -> float:
    r = _srgb_to_linear(max(0, min(255, int(rgb[0]))) / 255.0)
    g = _srgb_to_linear(max(0, min(255, int(rgb[1]))) / 255.0)
    b = _srgb_to_linear(max(0, min(255, int(rgb[2]))) / 255.0)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(rgb1: Tuple[int, int, int], rgb2: Tuple[int, int, int]) -> float:
    l1 = relative_luminance(rgb1)
    l2 = relative_luminance(rgb2)
    lighter, darker = (l1, l2) if l1 >= l2 else (l2, l1)
    return (lighter + 0.05) / (darker + 0.05)


def _int_color_to_rgb(color_int: int) -> Tuple[int, int, int]:
    return ((color_int >> 16) & 0xFF, (color_int >> 8) & 0xFF, color_int & 0xFF)


def _pdf_color_to_rgb(color: Any) -> Optional[Tuple[int, int, int]]:
    """Converts PyMuPDF / pdfplumber / PDF color tuple or int to (R, G, B) 0..255."""
    if color is None:
        return None
    if isinstance(color, int):
        return _int_color_to_rgb(color)
    if isinstance(color, (float,)):
        v = int(round(max(0.0, min(1.0, color)) * 255))
        return (v, v, v)
    if isinstance(color, (list, tuple)):
        if len(color) == 0:
            return None
        if len(color) == 1:
            g = float(color[0])
            v = int(round(max(0.0, min(1.0, g)) * 255)) if g <= 1.0 else int(max(0, min(255, g)))
            return (v, v, v)
        if len(color) == 3:
            if all(isinstance(c, (int, float)) and 0.0 <= float(c) <= 1.0 for c in color):
                return tuple(int(round(float(c) * 255)) for c in color)  # type: ignore[return-value]
            return tuple(int(max(0, min(255, float(c)))) for c in color)  # type: ignore[return-value]
        if len(color) == 4:
            # CMYK in 0..1
            c, m, y, k = (max(0.0, min(1.0, float(v))) for v in color)
            r = int(round(255 * (1.0 - c) * (1.0 - k)))
            g = int(round(255 * (1.0 - m) * (1.0 - k)))
            b = int(round(255 * (1.0 - y) * (1.0 - k)))
            return (r, g, b)
    return None


def parse_css_color(value: Optional[str]) -> Tuple[Optional[Tuple[int, int, int]], Optional[float]]:
    """
    Parses CSS/SVG/OOXML color strings.
    Returns (rgb_tuple_or_None, alpha_0_to_1_or_None).
    """
    if not value:
        return None, None
    s = value.strip().lower()
    if s in ("none", "auto", "inherit", "initial", "unset", "currentcolor"):
        return None, None
    if s == "transparent":
        return (255, 255, 255), 0.0
    if s in _NAMED_COLORS:
        return _NAMED_COLORS[s], 1.0

    # Hex: #RGB, #RGBA, #RRGGBB, #RRGGBBAA, or bare 6/8-digit OOXML hex (AARRGGBB / RRGGBB)
    raw_hex = s[1:] if s.startswith("#") else s
    if re.fullmatch(r"[0-9a-f]{3}", raw_hex):
        r = int(raw_hex[0] * 2, 16)
        g = int(raw_hex[1] * 2, 16)
        b = int(raw_hex[2] * 2, 16)
        return (r, g, b), 1.0
    if re.fullmatch(r"[0-9a-f]{4}", raw_hex):
        r = int(raw_hex[0] * 2, 16)
        g = int(raw_hex[1] * 2, 16)
        b = int(raw_hex[2] * 2, 16)
        a = int(raw_hex[3] * 2, 16) / 255.0
        return (r, g, b), a
    if re.fullmatch(r"[0-9a-f]{6}", raw_hex):
        return (int(raw_hex[0:2], 16), int(raw_hex[2:4], 16), int(raw_hex[4:6], 16)), 1.0
    if re.fullmatch(r"[0-9a-f]{8}", raw_hex):
        if s.startswith("#"):
            # CSS #RRGGBBAA
            return (
                int(raw_hex[0:2], 16),
                int(raw_hex[2:4], 16),
                int(raw_hex[4:6], 16),
            ), int(raw_hex[6:8], 16) / 255.0
        else:
            # OOXML AARRGGBB (e.g. FFFFFFFF)
            return (
                int(raw_hex[2:4], 16),
                int(raw_hex[4:6], 16),
                int(raw_hex[6:8], 16),
            ), int(raw_hex[0:2], 16) / 255.0

    m_rgb = re.match(r"rgba?\(\s*([^\)]+)\)", s)
    if m_rgb:
        parts = [p.strip() for p in re.split(r"[,\s/]+", m_rgb.group(1).strip()) if p.strip()]
        if len(parts) >= 3:
            def _chan(tok: str) -> int:
                if tok.endswith("%"):
                    return int(round(max(0.0, min(100.0, float(tok[:-1]))) * 2.55))
                return int(round(max(0.0, min(255.0, float(tok)))))

            try:
                rgb = (_chan(parts[0]), _chan(parts[1]), _chan(parts[2]))
                alpha = 1.0
                if len(parts) >= 4:
                    a_tok = parts[3]
                    alpha = float(a_tok[:-1]) / 100.0 if a_tok.endswith("%") else float(a_tok)
                return rgb, max(0.0, min(1.0, alpha))
            except ValueError:
                return None, None
    return None, None


def _is_near_white(rgb: Tuple[int, int, int], threshold: int = 238) -> bool:
    return rgb[0] >= threshold and rgb[1] >= threshold and rgb[2] >= threshold


# ---------------------------------------------------------------------------
# Layer 4: Unicode & Text Steganography Sanitization
# ---------------------------------------------------------------------------

_ZERO_WIDTH_CHARS = {
    "\u200B",  # ZERO WIDTH SPACE
    "\u200C",  # ZERO WIDTH NON-JOINER
    "\u200D",  # ZERO WIDTH JOINER
    "\u2060",  # WORD JOINER
    "\uFEFF",  # ZERO WIDTH NO-BREAK SPACE / BOM
    "\u00AD",  # SOFT HYPHEN
    "\u180E",  # MONGOLIAN VOWEL SEPARATOR
    "\u034F",  # COMBINING GRAPHEME JOINER
    "\u061C",  # ARABIC LETTER MARK
    "\u200E",  # LEFT-TO-RIGHT MARK
    "\u200F",  # RIGHT-TO-LEFT MARK
    "\u2061",  # FUNCTION APPLICATION
    "\u2062",  # INVISIBLE TIMES
    "\u2063",  # INVISIBLE SEPARATOR
    "\u2064",  # INVISIBLE PLUS
    "\u180B",  # MONGOLIAN FREE VARIATION SELECTOR ONE
    "\u180C",  # MONGOLIAN FREE VARIATION SELECTOR TWO
    "\u180D",  # MONGOLIAN FREE VARIATION SELECTOR THREE
    "\u180F",  # MONGOLIAN FREE VARIATION SELECTOR FOUR
    "\u115F",  # HANGUL CHOSEONG FILLER
    "\u1160",  # HANGUL JUNGSEONG FILLER
    "\u3164",  # HANGUL FILLER
    "\uFFA0",  # HALFWIDTH HANGUL FILLER
    "\u2800",  # BRAILLE PATTERN BLANK
    "\uFFF9",  # INTERLINEAR ANNOTATION ANCHOR
    "\uFFFA",  # INTERLINEAR ANNOTATION SEPARATOR
    "\uFFFB",  # INTERLINEAR ANNOTATION TERMINATOR
}

_BIDI_OVERRIDE_CHARS = {
    "\u202A",  # LRE
    "\u202B",  # RLE
    "\u202C",  # PDF
    "\u202D",  # LRO
    "\u202E",  # RLO
    "\u2066",  # LRI
    "\u2067",  # RLI
    "\u2068",  # FSI
    "\u2069",  # PDI
}

# Cyrillic & Greek visual confusables mapped to ASCII Latin equivalents
_HOMOGLYPH_MAP: Dict[str, str] = {
    # Cyrillic lowercase
    "\u0430": "a",  # а
    "\u0435": "e",  # е
    "\u043E": "o",  # о
    "\u0440": "p",  # р
    "\u0441": "c",  # с
    "\u0443": "y",  # у
    "\u0445": "x",  # х
    "\u0456": "i",  # і
    "\u0458": "j",  # ј
    "\u0455": "s",  # ѕ
    "\u04BB": "h",  # һ
    "\u04CF": "l",  # ӏ
    "\u0501": "d",  # ԁ
    "\u051B": "q",  # ԛ
    "\u051D": "w",  # ԝ
    # Cyrillic uppercase
    "\u0410": "A",  # А
    "\u0412": "B",  # В
    "\u0415": "E",  # Е
    "\u041A": "K",  # К
    "\u041C": "M",  # М
    "\u041D": "H",  # Н
    "\u041E": "O",  # О
    "\u0420": "P",  # Р
    "\u0421": "C",  # С
    "\u0422": "T",  # Т
    "\u0425": "X",  # Х
    "\u0406": "I",  # І
    "\u0405": "S",  # Ѕ
    "\u0408": "J",  # Ј
    # Greek confusables
    "\u03BF": "o",  # ο
    "\u03B1": "a",  # α (only normalized inside mixed-script Latin tokens)
    "\u03C1": "p",  # ρ (only normalized inside mixed-script Latin tokens)
    "\u03BD": "v",  # ν (only normalized inside mixed-script Latin tokens)
    "\u0391": "A",  # Α
    "\u0392": "B",  # Β
    "\u0395": "E",  # Ε
    "\u0396": "Z",  # Ζ
    "\u0397": "H",  # Η
    "\u0399": "I",  # Ι
    "\u039A": "K",  # Κ
    "\u039C": "M",  # Μ
    "\u039D": "N",  # Ν
    "\u039F": "O",  # Ο
    "\u03A1": "P",  # Ρ
    "\u03A4": "T",  # Τ
    "\u03A5": "Y",  # Υ
    "\u03A7": "X",  # Χ
    # Armenian / IPA / Latin-extended confusables
    "\u0570": "h",  # հ
    "\u0578": "n",  # ո
    "\u0585": "o",  # օ
    "\u0261": "g",  # ɡ
    "\u026A": "I",  # ɪ
    "\u029F": "L",  # ʟ
    "\u0131": "i",  # ı
    "\u017F": "s",  # ſ
}

_GREEK_MATH_STANDALONE = {"\u03B1", "\u03C1", "\u03BD"}


def _is_math_or_fullwidth_latin(ch: str) -> bool:
    cp = ord(ch)
    return (0x1D400 <= cp <= 0x1D7FF) or (0xFF21 <= cp <= 0xFF5A)


def _is_variation_selector(cp: int) -> bool:
    return (0xFE00 <= cp <= 0xFE0F) or (0xE0100 <= cp <= 0xE01EF)


def _is_tag_char(cp: int) -> bool:
    return 0xE0000 <= cp <= 0xE007F


def sanitize_text(
    text: str,
    location: str = "text",
) -> Tuple[str, List[TrapRecord], Dict[str, int]]:
    """
    Layer 4: Strips invisible Unicode steganography & normalizes cross-script homoglyphs.
    Returns (cleaned_text, findings, unicode_stats).
    """
    if not text:
        return "", [], {
            "zero_width_removed": 0,
            "tag_block_removed": 0,
            "variation_selector_removed": 0,
            "bidi_override_removed": 0,
            "homoglyph_normalized": 0,
        }

    findings: List[TrapRecord] = []
    zw_chars: List[str] = []
    bidi_chars: List[str] = []
    vs_chars: List[str] = []
    tag_chunks: List[str] = []
    current_tag_buf: List[str] = []

    out_chars: List[str] = []
    prev_cp: Optional[int] = None

    for ch in text:
        cp = ord(ch)
        if _is_tag_char(cp):
            # Decode ASCII tag payload (U+E0020..U+E007E -> chr(cp - 0xE0000))
            if 0xE0020 <= cp <= 0xE007E:
                current_tag_buf.append(chr(cp - 0xE0000))
            else:
                current_tag_buf.append("")
            continue
        else:
            if current_tag_buf:
                decoded = "".join(current_tag_buf)
                tag_chunks.append(decoded)
                current_tag_buf = []

        if ch in _BIDI_OVERRIDE_CHARS:
            bidi_chars.append(f"U+{cp:04X}")
            continue

        if ch in _ZERO_WIDTH_CHARS:
            zw_chars.append(f"U+{cp:04X}")
            continue

        if _is_variation_selector(cp):
            # Allow a single standard emoji variation selector (FE0E/FE0F) directly after an emoji (>= 0x2600)
            is_legit_emoji_vs = (
                cp in (0xFE0E, 0xFE0F)
                and prev_cp is not None
                and prev_cp >= 0x2600
                and not _is_variation_selector(prev_cp)
            )
            if not is_legit_emoji_vs:
                vs_chars.append(f"U+{cp:04X}")
                prev_cp = cp
                continue

        out_chars.append(ch)
        prev_cp = cp

    if current_tag_buf:
        tag_chunks.append("".join(current_tag_buf))

    cleaned = "".join(out_chars)

    if zw_chars:
        findings.append(
            _make_trap(
                reason="unicode_zero_width",
                text=f"Removed {len(zw_chars)} invisible/zero-width character(s)",
                location=location,
                severity="medium" if len(zw_chars) >= 2 else "low",
                details={"count": len(zw_chars), "codepoints": sorted(set(zw_chars))},
            )
        )

    if tag_chunks:
        decoded_payload = " ".join(c for c in tag_chunks if c).strip()
        findings.append(
            _make_trap(
                reason="unicode_tag_block",
                text=decoded_payload or f"Removed {len(tag_chunks)} Unicode Tag Block sequence(s)",
                location=location,
                severity="high",
                details={"sequences": len(tag_chunks), "decoded_payload": decoded_payload},
            )
        )

    if vs_chars:
        findings.append(
            _make_trap(
                reason="unicode_variation_selector",
                text=f"Removed {len(vs_chars)} suspicious Variation Selector character(s)",
                location=location,
                severity="high" if len(vs_chars) >= 3 else "medium",
                details={"count": len(vs_chars), "codepoints": sorted(set(vs_chars))},
            )
        )

    if bidi_chars:
        findings.append(
            _make_trap(
                reason="unicode_bidi_override",
                text=f"Removed {len(bidi_chars)} Bidi Override / Trojan Source character(s)",
                location=location,
                severity="high",
                details={"count": len(bidi_chars), "codepoints": sorted(set(bidi_chars))},
            )
        )

    # Cross-script homoglyph detection & normalization
    homoglyph_replacements: List[Dict[str, str]] = []
    latin_count = sum(1 for c in cleaned if ("a" <= c <= "z") or ("A" <= c <= "Z"))
    mostly_latin_doc = latin_count >= 10

    def _replace_token(match: re.Match[str]) -> str:
        tok = match.group(0)
        has_latin = any(("a" <= c <= "z") or ("A" <= c <= "Z") for c in tok)
        has_confusable = any(c in _HOMOGLYPH_MAP for c in tok)
        if not has_confusable:
            return tok

        # Case 1: Mixed Latin + Cyrillic/Greek inside same identifier/word -> ALWAYS normalize
        # Case 2: All-confusable token (>= 2 chars, not standalone Greek math) inside a Latin doc -> normalize
        all_confusable_or_ascii = all(
            (c in _HOMOGLYPH_MAP) or c.isascii() for c in tok
        )
        only_greek_math = all(c in _GREEK_MATH_STANDALONE for c in tok)

        should_normalize = has_latin or (
            mostly_latin_doc and all_confusable_or_ascii and len(tok) >= 2 and not only_greek_math
        )
        if not should_normalize:
            return tok

        normalized = "".join(_HOMOGLYPH_MAP.get(c, c) for c in tok)
        if normalized != tok:
            homoglyph_replacements.append({"original": tok, "normalized": normalized})
        return normalized

    cleaned = re.sub(r"[^\s\.,;:!\?\(\)\[\]\{\}\"'`<>/\\|=+\-*&^%$#@~]+", _replace_token, cleaned)

    if homoglyph_replacements:
        preview = ", ".join(
            f"{h['original']} -> {h['normalized']}" for h in homoglyph_replacements[:8]
        )
        findings.append(
            _make_trap(
                reason="unicode_homoglyph",
                text=f"Normalized cross-script homoglyph(s): {preview}",
                location=location,
                severity="high",
                details={"count": len(homoglyph_replacements), "replacements": homoglyph_replacements},
            )
        )

    # Detect & normalize Mathematical Alphanumeric / Fullwidth Latin NFKC obfuscation when suspicious
    obf_tokens = [
        tok
        for tok in re.findall(r"\S+", cleaned)
        if any(_is_math_or_fullwidth_latin(c) for c in tok)
    ]
    obfuscated_count = 0
    if obf_tokens:
        nfkc_shadow = unicodedata.normalize("NFKC", cleaned)
        if nfkc_shadow != cleaned and _is_suspicious_channel_text(nfkc_shadow):
            obfuscated_count = len(obf_tokens)
            findings.append(
                _make_trap(
                    reason="unicode_obfuscated_script",
                    text=f"Normalized NFKC obfuscated Latin sequence(s): {' '.join(obf_tokens[:6])}",
                    location=location,
                    severity="high",
                    details={"count": obfuscated_count},
                )
            )
            cleaned = "".join(
                unicodedata.normalize("NFKC", c) if _is_math_or_fullwidth_latin(c) else c
                for c in cleaned
            )

    stats = {
        "zero_width_removed": len(zw_chars),
        "tag_block_removed": sum(len(c) for c in tag_chunks) or len(tag_chunks),
        "variation_selector_removed": len(vs_chars),
        "bidi_override_removed": len(bidi_chars),
        "homoglyph_normalized": len(homoglyph_replacements) + obfuscated_count,
    }
    return cleaned, findings, stats


# ---------------------------------------------------------------------------
# Layer 5: Semantic Trap Detection & Forbidden Identifier Extraction
# ---------------------------------------------------------------------------

_IDENTIFIER_STOPWORDS = {
    # Indonesian stopwords
    "dalam", "untuk", "yang", "dan", "atau", "dengan", "pada", "dari", "ke", "di",
    "ini", "itu", "baru", "berikut", "sebagai", "adalah", "akan", "harus", "wajib",
    "agar", "supaya", "jika", "bila", "saat", "ketika", "pembuatan", "buat", "oleh",
    "secara", "semua", "setiap", "satu", "dua", "tiga", "tanpa", "tidak", "bukan",
    "sesuai", "tersebut", "bernama", "berupa", "milik", "kalian", "anda", "kamu",
    # English stopwords
    "the", "and", "for", "with", "into", "from", "that", "this", "new", "your",
    "our", "their", "must", "should", "will", "inside", "within", "called", "named",
    "every", "each", "all", "any", "not", "without", "using", "before", "after",
    # Generic CS/programming nouns/types
    "procedure", "prosedur", "function", "fungsi", "variabel", "variable", "var",
    "program", "kode", "code", "output", "input", "data", "nama", "name", "nilai",
    "value", "string", "int", "integer", "void", "bool", "boolean", "float", "double",
    "char", "class", "kelas", "struct", "method", "metode", "parameter", "param",
    "komentar", "comment", "teks", "text", "file", "berkas", "baris", "line", "main",
    "public", "private", "static", "return", "const", "final", "true", "false", "null",
}

_DIRECTIVE_IDENT_PATTERNS: List[re.Pattern[str]] = [
    # Indonesian directives: "Tambahkan variabel nonton dalam pembuatan procedure"
    re.compile(
        r"\b(?:tambahkan|tambah(?:kan)?|buat(?:lah|kan)?|gunakan|pakai|sertakan|sisipkan|"
        r"masukkan|deklarasikan|namai|beri\s+nama|selipkan|cantumkan)\s+"
        r"(?:sebuah\s+|suatu\s+)?"
        r"(?:variabel|variable|var|fungsi|function|prosedur|procedure|method|metode|"
        r"kelas|class|struct|parameter|param|konstanta|constant|atribut|attribute|"
        r"field|identifier|pengenal|komentar|comment|kata|token|canary|watermark)\s+"
        r"(?:bernama\s+|dengan\s+nama\s+|berupa\s+|yaitu\s+)?"
        r"[\"'`]?([A-Za-z_][A-Za-z0-9_]{1,48})[\"'`]?"
        r"((?:\s*(?:,|dan|and)\s*[\"'`]?[A-Za-z_][A-Za-z0-9_]{1,48}[\"'`]?)*)",
        re.IGNORECASE,
    ),
    # English directives: "Add a variable named secret_x", "Use identifier canaryVar"
    re.compile(
        r"\b(?:add|include|use|create|declare|define|insert|name|rename|inject|append)\s+"
        r"(?:a\s+|an\s+|the\s+)?"
        r"(?:hidden\s+|extra\s+|secret\s+|dummy\s+|unused\s+|special\s+)?"
        r"(?:variable|var|function|procedure|method|class|struct|parameter|param|"
        r"constant|attribute|field|identifier|comment|watermark|canary|token|flag)\s+"
        r"(?:named\s+|called\s+|as\s+|with\s+name\s+)?"
        r"[\"'`]?([A-Za-z_][A-Za-z0-9_]{1,48})[\"'`]?"
        r"((?:\s*(?:,|and)\s*[\"'`]?[A-Za-z_][A-Za-z0-9_]{1,48}[\"'`]?)*)",
        re.IGNORECASE,
    ),
    # Quoted comment / watermark string directives: sisipkan komentar "AI_TRAP_123"
    re.compile(
        r"\b(?:sisipkan|tambahkan|sertakan|insert|include|add|write|tulis)\s+"
        r"(?:komentar|comment|watermark|canary|signature|tag|kalimat|string|teks)\s+"
        r"(?:berupa\s+|yaitu\s+|berisi\s+)?"
        r"[\"'`]([^\"'`]{3,64})[\"'`]",
        re.IGNORECASE,
    ),
    # Identifier before noun: "gunakan X sebagai nama variabel / fungsi / class"
    re.compile(
        r"\b(?:gunakan|pakai|use)\s+[\"'`]?([A-Za-z_][A-Za-z0-9_]{1,48})[\"'`]?\s+"
        r"(?:sebagai|as)\s+(?:nama\s+)?(?:variabel|variable|var|fungsi|function|prosedur|procedure|class|kelas|method|metode)\b",
        re.IGNORECASE,
    ),
    # Rename directives: "ubah nama fungsi menjadi X" / "rename variable to X"
    re.compile(
        r"\b(?:ubah|ganti|rename)\s+(?:nama\s+)?(?:variabel|variable|var|fungsi|function|prosedur|procedure|class|kelas|method|metode)\b"
        r"[^.!?\n]{0,40}?\b(?:menjadi|ke|to|as)\s+[\"'`]?([A-Za-z_][A-Za-z0-9_]{1,48})[\"'`]?",
        re.IGNORECASE,
    ),
    # Output / print canary directives: cetak kata 'kucing' di akhir
    re.compile(
        r"\b(?:cetak|tampilkan|print|output|keluarkan)\s+(?:kata|teks|kalimat|string|pesan)\s+"
        r"[\"'`]([^\"'`]{2,64})[\"'`]",
        re.IGNORECASE,
    ),
    # Explicit naming phrase: "variabel bernama X" / "variable named X"
    re.compile(
        r"\b(?:variabel|variable)\s+(?:bernama|named|called)\s+[\"'`]?([A-Za-z_][A-Za-z0-9_]{1,48})[\"'`]?",
        re.IGNORECASE,
    ),
]

_SEMANTIC_TRAP_RULES: List[Tuple[str, str, re.Pattern[str], str]] = [
    (
        "prompt_injection",
        "ignore_previous_instructions",
        re.compile(
            r"\b(?:ignore|disregard|forget|override|bypass)\s+(?:all\s+)?"
            r"(?:previous|prior|above|earlier|your)\s+(?:instructions?|rules?|prompts?|directions?)\b",
            re.IGNORECASE,
        ),
        "high",
    ),
    (
        "prompt_injection",
        "abaikan_instruksi_sebelumnya",
        re.compile(
            r"\b(?:abaikan|lupakan|hiraukan|kesampingkan)\s+(?:semua\s+|seluruh\s+)?"
            r"(?:instruksi|perintah|aturan|prompt)\s+(?:sebelumnya|di\s+atas|awal)\b",
            re.IGNORECASE,
        ),
        "high",
    ),
    (
        "prompt_injection",
        "system_prompt_injection",
        re.compile(
            r"(?:\bsystem\s+prompt\b|<\s*system\s*>|\[/?SYSTEM\]|\bnew\s+system\s+instruction\b|"
            r"\bact\s+as\s+(?:a\s+)?(?:system|developer)\b)",
            re.IGNORECASE,
        ),
        "high",
    ),
    (
        "ai_meta_instruction",
        "if_you_are_an_ai_en",
        re.compile(
            r"\b(?:if|when|whenever)\s+you\s+(?:are|'re)\s+(?:an?\s+)?"
            r"(?:ai|llm|large\s+language\s+model|language\s+model|chatgpt|gpt(?:-?\d)?|"
            r"claude|gemini|copilot|assistant|bot)\b",
            re.IGNORECASE,
        ),
        "high",
    ),
    (
        "ai_meta_instruction",
        "jika_kamu_ai_id",
        re.compile(
            r"\b(?:jika|apabila|kalau|bila)\s+(?:kamu|anda|kau|kalian)\s+(?:adalah\s+|merupakan\s+)?"
            r"(?:sebuah\s+)?(?:ai|llm|chatgpt|gpt(?:-?\d)?|claude|gemini|copilot|"
            r"asisten\s+ai|kecerdasan\s+buatan|model\s+bahasa|bot)\b",
            re.IGNORECASE,
        ),
        "high",
    ),
    (
        "ai_meta_instruction",
        "note_for_ai",
        re.compile(
            r"\b(?:note|instruction|instructions|message|directive|command|prompt|important|"
            r"catatan|instruksi|pesan|perintah|khusus)\s+(?:for|to|untuk|buat)\s+"
            r"(?:the\s+|an?\s+|all\s+)?(?:ai|llm|chatgpt|gpt(?:-?\d)?|claude|gemini|copilot|assistant|bot)\b",
            re.IGNORECASE,
        ),
        "high",
    ),
    (
        "stealth_instruction",
        "do_not_tell_user_en",
        re.compile(
            r"\b(?:do\s+not|don't|never)\s+(?:tell|inform|mention|reveal|show|notify|alert)\s+"
            r"(?:the\s+)?(?:user|student|human|developer|programmer|person)\b",
            re.IGNORECASE,
        ),
        "high",
    ),
    (
        "stealth_instruction",
        "jangan_beritahu_user_id",
        re.compile(
            r"\b(?:jangan|tidak\s+boleh|dilarang)\s+"
            r"(?:beritahu|memberitahu|kasih\s+tahu|sebutkan|menyebutkan|tunjukkan|ungkapkan|laporkan)\s+"
            r"(?:ke\s+|kepada\s+)?(?:pengguna|user|mahasiswa|manusia|pemakai)\b",
            re.IGNORECASE,
        ),
        "high",
    ),
    (
        "stealth_instruction",
        "silent_insertion",
        re.compile(
            r"\b(?:silently|secretly|covertly|diam-diam|secara\s+tersembunyi|tanpa\s+sepengetahuan\s+(?:user|pengguna))\s+"
            r"(?:add|insert|include|inject|rename|tambahkan|sisipkan|masukkan|ubah)\b",
            re.IGNORECASE,
        ),
        "high",
    ),
    (
        "canary_watermark",
        "canary_or_watermark_directive",
        re.compile(
            r"\b(?:ai\s+watermark|canary\s+(?:variable|token|string|word|identifier)|"
            r"honeypot\s+(?:variable|token)|variabel\s+jebakan|penanda\s+ai|bukti\s+pakai\s+ai|"
            r"(?:always|wajib)\s+(?:include|insert|tambahkan|sisipkan)\s+(?:the\s+)?"
            r"(?:secret|hidden|magic|rahasia|tersembunyi)\s+(?:variable|word|comment|token|variabel|kata|komentar))\b",
            re.IGNORECASE,
        ),
        "high",
    ),
    (
        "prompt_injection",
        "chat_template_spoofing",
        re.compile(
            r"(?:<\|im_start\|>|<\|im_end\|>|<\|eot_id\|>|\[/?INST\]|"
            r"^\s*###\s*(?:System|Instruction)\s*:|</(?:document|context|user)>\s*<(?:system|instructions?)>)",
            re.IGNORECASE,
        ),
        "high",
    ),
    (
        "prompt_injection",
        "encoded_payload_directive",
        re.compile(
            r"\b(?:decode|dekode|terjemahkan)\s+(?:this\s+|berikut\s+)?(?:base64|hex|rot13)\b",
            re.IGNORECASE,
        ),
        "high",
    ),
    (
        "ai_meta_instruction",
        "indonesian_ai_meta",
        re.compile(
            r"(?:\b(?:khusus|bagi|untuk)\s+(?:pengguna\s+|model\s+)?(?:ai|llm|chatgpt|claude|gemini)\b|"
            r"\b(?:hai|halo)\s+(?:chatgpt|claude|gemini)\b|"
            r"\btanpa\s+diketahui\s+(?:mahasiswa|user|pengguna)\b)",
            re.IGNORECASE,
        ),
        "high",
    ),
]


def extract_forbidden_identifiers(text: str) -> List[str]:
    """
    Extracts candidate forbidden identifiers / canary tokens from trap text
    (e.g., 'Tambahkan variabel nonton dalam pembuatan procedure' -> ['nonton']).
    """
    if not text:
        return []
    found: List[str] = []
    seen_lower: set[str] = set()

    def _add(candidate: str) -> None:
        cand = candidate.strip().strip("\"'`.,;:()[]{}")
        if not cand or len(cand) < 2:
            return
        if cand.lower() in _IDENTIFIER_STOPWORDS:
            return
        if cand.lower() not in seen_lower:
            seen_lower.add(cand.lower())
            found.append(cand)

    variants = [text]
    nfkc_text = unicodedata.normalize("NFKC", text)
    if nfkc_text != text:
        variants.append(nfkc_text)

    for variant in variants:
        for idx, pat in enumerate(_DIRECTIVE_IDENT_PATTERNS):
            for m in pat.finditer(variant):
                first = m.group(1)
                if idx in (2, 5):
                    # Quoted comment / watermark / output phrase
                    _add(first)
                    for sub_tok in re.findall(r"\b[A-Za-z_][A-Za-z0-9_]{2,40}\b", first):
                        if sub_tok.lower() not in _IDENTIFIER_STOPWORDS:
                            _add(sub_tok)
                else:
                    _add(first)
                    tail = m.group(2) if m.lastindex and m.lastindex >= 2 else ""
                    if tail:
                        for extra in re.findall(r"[\"'`]?([A-Za-z_][A-Za-z0-9_]{1,48})[\"'`]?", tail):
                            if extra.lower() not in ("dan", "and", "atau", "or"):
                                _add(extra)

    return found


def _is_suspicious_channel_text(text: str) -> bool:
    """Returns True if text from metadata/annotations/comments looks like a directive or trap."""
    if not text or not text.strip():
        return False
    nfkc = unicodedata.normalize("NFKC", text)
    if extract_forbidden_identifiers(nfkc):
        return True
    for _, _, pat, _ in _SEMANTIC_TRAP_RULES:
        if pat.search(nfkc) or pat.search(text):
            return True
    if re.search(
        r"\b(?:tambahkan|sisipkan|gunakan\s+variabel|add\s+variable|insert\s+comment|"
        r"ignore\s+previous|abaikan\s+instruksi|prompt|chatgpt|claude|gemini|llm)\b",
        nfkc,
        re.IGNORECASE,
    ):
        return True
    return False


def detect_semantic_traps(
    text: str,
    location: str = "visible_text",
) -> List[TrapRecord]:
    """
    Layer 5: Scans visible text for semantic prompt injections / AI honeypots.
    NEVER silently deletes text; marks every finding with needs_user_confirmation=True.
    """
    if not text:
        return []
    warnings: List[TrapRecord] = []
    seen_keys: set[Tuple[str, str]] = set()

    for line_idx, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        nfkc_line = unicodedata.normalize("NFKC", line)
        for category, rule_name, pat, severity in _SEMANTIC_TRAP_RULES:
            if pat.search(line) or pat.search(nfkc_line):
                key = (rule_name, nfkc_line.lower())
                if key in seen_keys:
                    continue
                seen_keys.add(key)
                candidates = extract_forbidden_identifiers(nfkc_line)
                warnings.append(
                    _make_warning(
                        category=category,
                        text=line[:400],
                        location=f"{location}:line {line_idx}",
                        pattern=rule_name,
                        needs_user_confirmation=True,
                        severity=severity,
                        candidates=candidates,
                    )
                )
    return warnings


_COALESCE_REASONS = {
    "white_text",
    "low_contrast",
    "occluded_text",
    "micro_font",
    "invisible_render_mode",
    "low_opacity",
    "off_page",
    "docx_vanish",
    "docx_web_hidden",
    "docx_low_contrast",
    "docx_micro_font",
    "pptx_hidden_text",
    "pptx_micro_font",
    "rtf_hidden_text",
    "odf_hidden_text",
}


def _coalesce_traps(traps: List[TrapRecord]) -> List[TrapRecord]:
    """
    Coalesces consecutive fragmented spans/runs on the SAME line or incomplete clause
    (e.g. 'Tambahkan ' + 'variabel split_id') while keeping separate multi-line traps distinct.
    """
    if not traps:
        return traps
    coalesced: List[TrapRecord] = []
    for t in traps:
        cur_copy = TrapRecord(t)
        if t.get("details"):
            cur_copy["details"] = dict(t["details"])
        if coalesced:
            prev = coalesced[-1]
            same_bucket = (
                t.get("reason") in _COALESCE_REASONS
                and prev.get("reason") == t.get("reason")
                and prev.get("location") == t.get("location")
                and len(prev.get("text", "")) < 800
            )
            if same_bucket:
                prev_txt = prev.get("text", "")
                cur_txt = t.get("text", "")
                prev_bbox = (prev.get("details") or {}).get("bbox")
                cur_bbox = (t.get("details") or {}).get("bbox")
                if prev_bbox and cur_bbox and len(prev_bbox) >= 4 and len(cur_bbox) >= 4:
                    same_fragment = abs(float(prev_bbox[1]) - float(cur_bbox[1])) <= 4.5
                else:
                    same_fragment = (
                        not prev_txt.rstrip().endswith((".", "!", "?"))
                        and not extract_forbidden_identifiers(prev_txt)
                    )
                if same_fragment:
                    sep = "" if (not prev_txt or not cur_txt or prev_txt.endswith((" ", "\n")) or cur_txt.startswith((" ", "\n", ".", ",", ";", ":"))) else " "
                    prev["text"] = f"{prev_txt}{sep}{cur_txt}".strip()
                    if prev_bbox and cur_bbox and len(prev_bbox) >= 4 and len(cur_bbox) >= 4:
                        prev["details"]["bbox"] = [
                            min(float(prev_bbox[0]), float(cur_bbox[0])),
                            min(float(prev_bbox[1]), float(cur_bbox[1])),
                            max(float(prev_bbox[2]), float(cur_bbox[2])),
                            max(float(prev_bbox[3]), float(cur_bbox[3])),
                        ]
                    continue
        coalesced.append(cur_copy)
    return coalesced


def _compute_risk_level(
    stripped_traps: Sequence[TrapRecord],
    semantic_warnings: Sequence[TrapRecord],
    forbidden_identifiers: Sequence[str],
) -> str:
    if not stripped_traps and not semantic_warnings:
        return "none"

    high_traps = [t for t in stripped_traps if t.get("severity") == "high"]
    med_traps = [t for t in stripped_traps if t.get("severity") == "medium"]
    high_warnings = [w for w in semantic_warnings if w.get("severity") == "high"]
    critical_reasons = {
        "alpha_channel_stego_suspected",
        "unicode_bidi_override",
        "unicode_tag_block",
        "unicode_obfuscated_script",
        "code_prompt_injection",
        "agent_rule_poisoning",
    }

    if (
        (high_traps and forbidden_identifiers)
        or any(t.get("reason") in critical_reasons for t in stripped_traps)
        or len(high_traps) >= 2
    ):
        return "critical"
    if high_traps or high_warnings:
        return "high"
    if med_traps or semantic_warnings:
        return "medium"
    return "low"


def _finalize_report(
    clean_text: str,
    stripped_traps: List[TrapRecord],
    file_type: str,
    engine_used: str,
    source_path: Optional[str] = None,
    sanitized_image_path: Optional[str] = None,
    extra_warnings: Optional[List[TrapRecord]] = None,
    extra_forbidden: Optional[Iterable[str]] = None,
    stats: Optional[Dict[str, Any]] = None,
    run_unicode_on_clean: bool = True,
) -> SanitizationReport:
    all_traps = _coalesce_traps(list(stripped_traps))
    all_warnings = list(extra_warnings or [])
    report_stats = dict(stats or {})

    if run_unicode_on_clean and clean_text:
        clean_text, uni_traps, uni_stats = sanitize_text(clean_text, location=file_type)
        all_traps.extend(uni_traps)
        report_stats.update(uni_stats)
    else:
        report_stats.setdefault("zero_width_removed", 0)
        report_stats.setdefault("tag_block_removed", 0)
        report_stats.setdefault("variation_selector_removed", 0)
        report_stats.setdefault("bidi_override_removed", 0)
        report_stats.setdefault("homoglyph_normalized", 0)

    # Run semantic detection on visible clean text (never deletes visible text)
    if clean_text:
        all_warnings.extend(detect_semantic_traps(clean_text, location=file_type))

    # Extract forbidden identifiers from ALL stripped hidden traps & explicit extras
    forbidden: List[str] = []
    seen_f: set[str] = set()

    def _add_forbidden(items: Iterable[str]) -> None:
        for item in items:
            low = item.lower()
            if low not in seen_f:
                seen_f.add(low)
                forbidden.append(item)

    if extra_forbidden:
        _add_forbidden(extra_forbidden)

    for trap in all_traps:
        trap_text = trap.get("text", "")
        if trap_text:
            _add_forbidden(extract_forbidden_identifiers(trap_text))
        decoded = (trap.get("details") or {}).get("decoded_payload", "")
        if decoded:
            _add_forbidden(extract_forbidden_identifiers(decoded))

    # Cross-line coalesced pass ONLY for forbidden-identifier extraction (preserves distinct TrapRecords)
    if all_traps:
        buf_key: Optional[Tuple[str, str]] = None
        buf_parts: List[str] = []
        for trap in all_traps:
            key = (trap.get("location", ""), trap.get("reason", ""))
            txt = (trap.get("text") or "").strip()
            if not txt:
                continue
            if buf_key == key and sum(len(p) for p in buf_parts) < 1200:
                buf_parts.append(txt)
            else:
                if len(buf_parts) > 1:
                    _add_forbidden(extract_forbidden_identifiers(" ".join(buf_parts)))
                buf_key = key
                buf_parts = [txt]
        if len(buf_parts) > 1:
            _add_forbidden(extract_forbidden_identifiers(" ".join(buf_parts)))

    report_stats["stripped_count"] = len(all_traps)
    report_stats["semantic_warning_count"] = len(all_warnings)
    report_stats["forbidden_identifier_count"] = len(forbidden)

    risk = _compute_risk_level(all_traps, all_warnings, forbidden)

    return SanitizationReport(
        clean_text=clean_text.strip(),
        stripped_traps=all_traps,
        semantic_warnings=all_warnings,
        forbidden_identifiers=forbidden,
        sanitized_image_path=sanitized_image_path,
        engine_used=engine_used,
        risk_level=risk,
        file_type=file_type,
        stats=report_stats,
        source_path=os.path.abspath(source_path) if source_path else None,
    )


# ---------------------------------------------------------------------------
# Layer 2 Helpers (shared with PDF embedded image auditing)
# ---------------------------------------------------------------------------

def _inspect_pil_metadata(
    pil_img: Any,
    raw_bytes: Optional[bytes],
    location_prefix: str,
) -> Tuple[List[TrapRecord], List[TrapRecord]]:
    """Audits EXIF, XMP, IPTC, JPEG COM, and PNG tEXt/iTXt/zTXt chunks."""
    traps: List[TrapRecord] = []
    warnings: List[TrapRecord] = []
    checked_pairs: set[Tuple[str, str]] = set()

    def _check_kv(channel: str, key: str, val: Any) -> None:
        if val is None:
            return
        if isinstance(val, bytes):
            try:
                text_val = val.decode("utf-8", errors="ignore").strip("\x00 \r\n\t")
            except Exception:
                return
        elif isinstance(val, str):
            text_val = val.strip("\x00 \r\n\t")
        else:
            return

        if not text_val or len(text_val) < 2:
            return
        pair = (channel, text_val[:200])
        if pair in checked_pairs:
            return
        checked_pairs.add(pair)

        # Check Unicode stego in metadata
        clean_val, uni_traps, _ = sanitize_text(text_val, location=f"{location_prefix}:{channel}:{key}")
        traps.extend(uni_traps)

        # Any meaningful textual chunk (PNG tEXt/iTXt/zTXt, JPEG COM, EXIF comment/description) or suspicious XMP
        is_text_comment_key = key.lower() in {
            "comment", "description", "title", "author", "subject", "keywords",
            "imagedescription", "usercomment", "xpcomment", "xptitle", "xpsubject",
            "instructions", "prompt", "note", "notes", "hidden", "secret", "warning",
            "software", "copyright", "artist", "disclaimer", "source",
        }
        is_suspicious = _is_suspicious_channel_text(clean_val)
        sem_hits = detect_semantic_traps(clean_val, location=f"{location_prefix}:{channel}:{key}")
        warnings.extend(sem_hits)

        if is_suspicious or sem_hits or (channel.startswith("PNG_") and len(clean_val) >= 4) or (
            is_text_comment_key and len(clean_val) >= 4 and not re.fullmatch(r"[\d\.\-\s/:]+", clean_val)
        ):
            traps.append(
                _make_trap(
                    reason="image_metadata",
                    text=clean_val[:500],
                    location=f"{location_prefix}:{channel}:{key}",
                    severity="high" if (is_suspicious or sem_hits) else "medium",
                    details={"channel": channel, "key": key},
                )
            )

    # 1. PNG text chunks (`img.text` preserves tEXt, iTXt, zTXt)
    png_text = getattr(pil_img, "text", None)
    if isinstance(png_text, dict):
        for k, v in png_text.items():
            _check_kv("PNG_text", str(k), v)

    # 2. General `img.info` entries (JPEG comment, XMP, ICC, etc.)
    info = getattr(pil_img, "info", {}) or {}
    skip_binary_keys = {"icc_profile", "dpi", "jfif", "jfif_version", "jfif_unit", "jfif_density",
                        "transparency", "gamma", "chromaticity", "srgb", "compression", "progressive",
                        "loop", "duration", "background", "version", "extension", "adobe", "adobe_transform"}
    for k, v in info.items():
        kl = str(k).lower()
        if kl in skip_binary_keys or kl == "exif":
            continue
        if kl in ("comment",):
            _check_kv("JPEG_COM", str(k), v)
        elif "xmp" in kl:
            _check_kv("XMP", str(k), v)
        elif "iptc" in kl or "photoshop" in kl:
            _check_kv("IPTC", str(k), v)
        elif isinstance(v, (str, bytes)):
            channel = "PNG_text" if (getattr(pil_img, "format", "") or "").upper() == "PNG" else "info"
            _check_kv(channel, str(k), v)

    # 3. EXIF tags
    try:
        from PIL import ExifTags
        exif = pil_img.getexif()
        if exif:
            for tag_id, val in exif.items():
                tag_name = ExifTags.TAGS.get(tag_id, str(tag_id))
                if isinstance(val, bytes) and tag_name.lower().startswith("xp"):
                    try:
                        val = val.decode("utf-16le", errors="ignore").rstrip("\x00")
                    except Exception:
                        pass
                _check_kv("EXIF", str(tag_name), val)
            # Also check Exif sub-IFD (e.g., UserComment 37510)
            try:
                sub_ifd = exif.get_ifd(0x8769)
                if sub_ifd:
                    for tag_id, val in sub_ifd.items():
                        tag_name = ExifTags.TAGS.get(tag_id, str(tag_id))
                        if isinstance(val, bytes) and val.startswith((b"ASCII\x00\x00\x00", b"UNICODE\x00")):
                            val = val[8:]
                        _check_kv("EXIF", str(tag_name), val)
            except Exception:
                pass
    except Exception:
        pass

    # 4. Raw XMP scan in file bytes (catches XMP packets Pillow doesn't populate into info)
    if raw_bytes:
        m_xmp = re.search(rb"<x:xmpmeta\b.*?</x:xmpmeta>", raw_bytes, re.DOTALL | re.IGNORECASE)
        if m_xmp:
            xmp_str = m_xmp.group(0).decode("utf-8", errors="ignore")
            # Strip XML tags to inspect textual values
            xmp_text = re.sub(r"<[^>]+>", " ", xmp_str)
            xmp_text = re.sub(r"\s+", " ", xmp_text).strip()
            if _is_suspicious_channel_text(xmp_text):
                _check_kv("XMP_raw", "xmpmeta", xmp_text)

    return traps, warnings


# ---------------------------------------------------------------------------
# Layer 1: PDF Dual-Engine (`pymupdf` primary, `pdfplumber` & `pypdf` fallback)
# ---------------------------------------------------------------------------

def _import_pymupdf():
    try:
        import pymupdf  # type: ignore
        return pymupdf
    except ImportError:
        try:
            import fitz as pymupdf  # type: ignore
            return pymupdf
        except ImportError:
            return None


def _bbox_overlap_ratio(inner: Tuple[float, float, float, float], outer: Tuple[float, float, float, float]) -> float:
    ix0, iy0, ix1, iy1 = inner
    ox0, oy0, ox1, oy1 = outer
    area_inner = max(0.0, ix1 - ix0) * max(0.0, iy1 - iy0)
    if area_inner <= 1e-6:
        return 0.0
    dx = max(0.0, min(ix1, ox1) - max(ix0, ox0))
    dy = max(0.0, min(iy1, oy1) - max(iy0, oy0))
    return (dx * dy) / area_inner


def _sample_pixmap_contrast(
    samples: bytes,
    width: int,
    height: int,
    crop_x0: float,
    crop_y0: float,
    scale_x: float,
    scale_y: float,
    bbox: Tuple[float, float, float, float],
    span_rgb: Tuple[int, int, int],
) -> Dict[str, Any]:
    """
    Samples rendered RGB pixmap around and inside a text span's bounding box.
    Returns background RGB, fg-vs-bg WCAG contrast, internal luminance contrast,
    and whether any rendered pixel inside bbox matches the span ink color.
    """
    x0, y0, x1, y1 = bbox
    px0 = max(0, min(width - 1, int(math.floor((x0 - crop_x0) * scale_x))))
    py0 = max(0, min(height - 1, int(math.floor((y0 - crop_y0) * scale_y))))
    px1 = max(px0 + 1, min(width, int(math.ceil((x1 - crop_x0) * scale_x))))
    py1 = max(py0 + 1, min(height, int(math.ceil((y1 - crop_y0) * scale_y))))

    stride = width * 3

    def _get_rgb(px: int, py: int) -> Tuple[int, int, int]:
        idx = py * stride + px * 3
        return (samples[idx], samples[idx + 1], samples[idx + 2])

    # 1. Sample background ring (2..4 px outside bbox)
    ring_r: List[int] = []
    ring_g: List[int] = []
    ring_b: List[int] = []
    pad_outer = 4
    pad_inner = 1
    rx0 = max(0, px0 - pad_outer)
    ry0 = max(0, py0 - pad_outer)
    rx1 = min(width, px1 + pad_outer)
    ry1 = min(height, py1 + pad_outer)

    step_x = max(1, (rx1 - rx0) // 24)
    step_y = max(1, (ry1 - ry0) // 12)

    for py in range(ry0, ry1, step_y):
        for px in range(rx0, rx1, step_x):
            if (px0 - pad_inner) <= px < (px1 + pad_inner) and (py0 - pad_inner) <= py < (py1 + pad_inner):
                continue
            r, g, b = _get_rgb(px, py)
            ring_r.append(r)
            ring_g.append(g)
            ring_b.append(b)

    if ring_r:
        ring_r.sort()
        ring_g.sort()
        ring_b.sort()
        mid = len(ring_r) // 2
        bg_rgb = (ring_r[mid], ring_g[mid], ring_b[mid])
    else:
        bg_rgb = (255, 255, 255)

    # 2. Sample interior pixels of bbox (dense enough to hit thin glyph strokes)
    in_step_x = max(1, (px1 - px0) // 60)
    in_step_y = max(1, (py1 - py0) // 24)
    min_lum = 1.0
    max_lum = 0.0
    min_dist_to_fg = 999
    max_contrast_to_bg = 1.0
    sr, sg, sb = span_rgb

    for py in range(py0, py1, in_step_y):
        row_base = py * stride
        for px in range(px0, px1, in_step_x):
            idx = row_base + px * 3
            r, g, b = samples[idx], samples[idx + 1], samples[idx + 2]
            lum = relative_luminance((r, g, b))
            if lum < min_lum:
                min_lum = lum
            if lum > max_lum:
                max_lum = lum
            dist = abs(r - sr) + abs(g - sg) + abs(b - sb)
            if dist < min_dist_to_fg:
                min_dist_to_fg = dist
            c_bg = contrast_ratio((r, g, b), bg_rgb)
            if c_bg > max_contrast_to_bg:
                max_contrast_to_bg = c_bg

    internal_contrast = (max_lum + 0.05) / (min_lum + 0.05) if max_lum >= min_lum else 1.0
    fg_bg_contrast = contrast_ratio(span_rgb, bg_rgb)

    return {
        "bg_rgb": bg_rgb,
        "fg_bg_contrast": fg_bg_contrast,
        "internal_contrast": internal_contrast,
        "max_contrast_to_bg": max_contrast_to_bg,
        "min_dist_to_fg": min_dist_to_fg,
    }


def _sanitize_pdf_pymupdf(
    pdf_path: str,
    max_pages: Optional[int],
    contrast_threshold: float,
    min_font_size: float,
    min_opacity: float,
) -> SanitizationReport:
    pymupdf = _import_pymupdf()
    assert pymupdf is not None

    stripped_traps: List[TrapRecord] = []
    extra_warnings: List[TrapRecord] = []
    clean_pages: List[str] = []
    image_heavy_pages: List[int] = []
    audited_img_xrefs: set[int] = set()

    doc = pymupdf.open(pdf_path)
    try:
        total_pages = len(doc)
        page_limit = total_pages if max_pages is None else min(total_pages, max_pages)

        # 1. Audit document metadata & XMP (never merged into clean_text)
        meta = doc.metadata or {}
        for k, v in meta.items():
            if not v or not isinstance(v, str):
                continue
            v_clean, uni_traps, _ = sanitize_text(v, location=f"pdf_metadata:{k}")
            stripped_traps.extend(uni_traps)
            if _is_suspicious_channel_text(v_clean):
                stripped_traps.append(
                    _make_trap(
                        reason="pdf_metadata",
                        text=v_clean[:500],
                        location=f"pdf_metadata:{k}",
                        severity="high",
                        details={"field": k},
                    )
                )
        try:
            xmp = doc.get_xml_metadata()
            if xmp:
                xmp_plain = re.sub(r"<[^>]+>", " ", xmp)
                xmp_plain = re.sub(r"\s+", " ", xmp_plain).strip()
                if _is_suspicious_channel_text(xmp_plain):
                    stripped_traps.append(
                        _make_trap(
                            reason="pdf_metadata",
                            text=xmp_plain[:500],
                            location="pdf_metadata:xmp",
                            severity="high",
                            details={"field": "xmp"},
                        )
                    )
        except Exception:
            pass

        # Detect disabled OCG layers
        ocg_map = doc.get_ocgs() or {}
        off_ocg_names = {
            info.get("name", "") for info in ocg_map.values() if not info.get("on", True)
        }

        dpi = 144
        scale = dpi / 72.0

        for page_idx in range(page_limit):
            page = doc[page_idx]
            page_num = page_idx + 1
            loc = f"page {page_num}"
            crop = page.cropbox

            # Render page to pixmap for real visual contrast & occlusion sampling
            pix = page.get_pixmap(dpi=dpi, alpha=False)
            samples = pix.samples
            pix_w, pix_h = pix.width, pix.height
            scale_x = pix_w / max(1.0, crop.width)
            scale_y = pix_h / max(1.0, crop.height)

            # Texttrace gives render_mode (`type == 3`), exact `opacity`, `seqno`, and off-page traces
            traces = page.get_texttrace() or []
            drawings = page.get_drawings() or []
            img_infos = page.get_image_info(xrefs=True) or []
            bboxlog = page.get_bboxlog() or []

            # Map `fill-image` seqno indices from bboxlog to opaque image rects (for z-order occlusion)
            fill_img_logs = [(idx, bb) for idx, (kind, bb) in enumerate(bboxlog) if kind == "fill-image"]
            opaque_images: List[Tuple[int, Tuple[float, float, float, float]]] = []
            for img_i, info in enumerate(img_infos):
                if info.get("has-mask", False):
                    continue
                ib = info.get("bbox")
                if not ib:
                    continue
                img_seq = int(info.get("number", -1))
                # Match bboxlog index if available for exact z-order against texttrace seqno
                if img_i < len(fill_img_logs):
                    img_seq = max(img_seq, fill_img_logs[img_i][0])
                opaque_images.append((img_seq, tuple(float(v) for v in ib)))

            # Build opaque drawings list with seqno for z-order occlusion check
            opaque_drawings: List[Tuple[int, Tuple[float, float, float, float], Optional[Tuple[int, int, int]]]] = []
            for dr in drawings:
                fill = dr.get("fill")
                fill_op = dr.get("fill_opacity")
                if fill is not None and (fill_op is None or float(fill_op) >= 0.85):
                    r = dr.get("rect")
                    if r is not None:
                        opaque_drawings.append(
                            (int(dr.get("seqno", -1)), (r.x0, r.y0, r.x1, r.y1), _pdf_color_to_rgb(fill))
                        )

            # Audit off-page text from texttrace (since get_text('dict') clips to page rect)
            for tr in traces:
                tr_text = "".join(chr(c[0]) for c in tr.get("chars", [])).strip()
                if not tr_text:
                    continue
                tb = tr.get("bbox", (0, 0, 0, 0))
                if (
                    tb[2] <= crop.x0 + 0.5
                    or tb[0] >= crop.x1 - 0.5
                    or tb[3] <= crop.y0 + 0.5
                    or tb[1] >= crop.y1 - 0.5
                ):
                    stripped_traps.append(
                        _make_trap(
                            reason="off_page",
                            text=tr_text,
                            location=loc,
                            severity="high",
                            details={"bbox": [round(float(v), 2) for v in tb]},
                        )
                    )

            # Extract structured spans (visible OCGs only by default in PyMuPDF)
            page_dict = page.get_text("dict")
            page_lines: List[str] = []
            visible_char_count = 0
            dict_span_bboxes: List[Tuple[float, float, float, float]] = []

            for block in page_dict.get("blocks", []):
                if block.get("type", 0) != 0:
                    continue
                for line in block.get("lines", []):
                    line_parts: List[str] = []
                    for span in line.get("spans", []):
                        raw_span_text = span.get("text", "")
                        if not raw_span_text:
                            continue
                        if not raw_span_text.strip():
                            line_parts.append(raw_span_text)
                            continue

                        sb = tuple(float(v) for v in span.get("bbox", (0, 0, 0, 0)))
                        dict_span_bboxes.append(sb)
                        size = float(span.get("size", 0.0))
                        color_int = int(span.get("color", 0))
                        span_rgb = _int_color_to_rgb(color_int)
                        alpha_255 = span.get("alpha", 255)
                        opacity = (float(alpha_255) / 255.0) if alpha_255 is not None else 1.0

                        # Match corresponding texttrace entry (if any) for render_mode & seqno
                        matched_tr = None
                        best_ov = 0.0
                        for tr in traces:
                            ov = _bbox_overlap_ratio(sb, tr.get("bbox", (0, 0, 0, 0)))
                            if ov > best_ov:
                                best_ov = ov
                                matched_tr = tr

                        render_mode = matched_tr.get("type", 0) if (matched_tr and best_ov > 0.3) else 0
                        tr_opacity = (
                            float(matched_tr.get("opacity", 1.0))
                            if (matched_tr and best_ov > 0.3 and matched_tr.get("opacity") is not None)
                            else opacity
                        )
                        span_seqno = int(matched_tr.get("seqno", -1)) if (matched_tr and best_ov > 0.3) else -1

                        strip_reason: Optional[str] = None
                        strip_details: Dict[str, Any] = {
                            "color": f"#{color_int:06x}",
                            "font": span.get("font", ""),
                            "size": round(size, 2),
                            "bbox": [round(v, 2) for v in sb],
                        }

                        span_w = max(0.0, sb[2] - sb[0])
                        span_h = max(0.0, sb[3] - sb[1])
                        stripped_len = len(raw_span_text.strip())

                        # Check 1: Off-page / clipped
                        if (
                            sb[2] <= crop.x0 + 0.5
                            or sb[0] >= crop.x1 - 0.5
                            or sb[3] <= crop.y0 + 0.5
                            or sb[1] >= crop.y1 - 0.5
                        ):
                            strip_reason = "off_page"

                        # Check 2: Invisible rendering mode (Tr == 3)
                        elif render_mode == 3:
                            strip_reason = "invisible_render_mode"
                            strip_details["render_mode"] = 3

                        # Check 3: Low opacity / transparent
                        elif min(opacity, tr_opacity) < min_opacity:
                            strip_reason = "low_opacity"
                            strip_details["opacity"] = round(min(opacity, tr_opacity), 3)

                        # Check 4: Micro-font, rotated micro-text, collapsed bbox, or 1 Tz horizontal scaling collapse
                        elif (
                            size < min_font_size
                            or min(span_w, span_h) < min_font_size
                            or (span_w * span_h) < 1.0
                            or (stripped_len >= 5 and (max(span_w, span_h) / stripped_len) < 0.8)
                        ):
                            strip_reason = "micro_font"

                        # Check 4b: Z-order occlusion by opaque raster image drawn AFTER text
                        elif span_seqno >= 0 and any(
                            img_seq > span_seqno and _bbox_overlap_ratio(sb, img_bb) >= 0.75
                            for img_seq, img_bb in opaque_images
                        ):
                            strip_reason = "occluded_text"

                        else:
                            # Check 5: Pixel-sampled WCAG contrast & occlusion detection
                            px_info = _sample_pixmap_contrast(
                                samples, pix_w, pix_h, crop.x0, crop.y0, scale_x, scale_y, sb, span_rgb
                            )
                            bg_rgb = px_info["bg_rgb"]
                            fg_bg_c = px_info["fg_bg_contrast"]
                            int_c = px_info["internal_contrast"]
                            max_bg_c = px_info["max_contrast_to_bg"]
                            min_fg_dist = px_info["min_dist_to_fg"]

                            strip_details["bg_color"] = "#{:02x}{:02x}{:02x}".format(*bg_rgb)
                            strip_details["contrast_ratio"] = round(fg_bg_c, 2)
                            strip_details["internal_contrast"] = round(int_c, 2)

                            # Check z-order occlusion by later opaque drawing
                            covered_by_later_rect = False
                            if span_seqno >= 0:
                                for dr_seq, dr_rect, _ in opaque_drawings:
                                    if dr_seq > span_seqno and _bbox_overlap_ratio(sb, dr_rect) >= 0.80:
                                        covered_by_later_rect = True
                                        break

                            if fg_bg_c < contrast_threshold:
                                if _is_near_white(span_rgb) and _is_near_white(bg_rgb):
                                    strip_reason = "white_text"
                                else:
                                    strip_reason = "low_contrast"
                            elif (int_c < contrast_threshold and max_bg_c < contrast_threshold) or (
                                covered_by_later_rect and min_fg_dist > 90
                            ):
                                strip_reason = "occluded_text"

                        if strip_reason is not None:
                            stripped_traps.append(
                                _make_trap(
                                    reason=strip_reason,
                                    text=raw_span_text,
                                    location=loc,
                                    severity="high",
                                    details=strip_details,
                                )
                            )
                        else:
                            line_parts.append(raw_span_text)
                            visible_char_count += len(raw_span_text.strip())

                    joined_line = "".join(line_parts).rstrip()
                    if joined_line.strip():
                        page_lines.append(joined_line)

            # Audit clipping-path hidden text (present in texttrace inside cropbox, omitted from get_text("dict"))
            for tr in traces:
                tr_text = "".join(chr(c[0]) for c in tr.get("chars", [])).strip()
                if not tr_text:
                    continue
                tb = tuple(float(v) for v in tr.get("bbox", (0, 0, 0, 0)))
                inside_crop = (
                    tb[2] > crop.x0 + 0.5
                    and tb[0] < crop.x1 - 0.5
                    and tb[3] > crop.y0 + 0.5
                    and tb[1] < crop.y1 - 0.5
                )
                if not inside_crop:
                    continue
                if tr.get("type", 0) == 3 or (tr.get("opacity") is not None and float(tr.get("opacity", 1.0)) < min_opacity):
                    continue
                if not any(_bbox_overlap_ratio(tb, db) >= 0.1 for db in dict_span_bboxes):
                    stripped_traps.append(
                        _make_trap(
                            reason="pdf_clipped_text",
                            text=tr_text,
                            location=loc,
                            severity="high",
                            details={"bbox": [round(v, 2) for v in tb]},
                        )
                    )

            clean_pages.append("\n".join(page_lines))

            # Audit Hyperlink URIs
            try:
                for lnk in page.get_links() or []:
                    uri = str(lnk.get("uri", "") or "").strip()
                    if uri and _is_suspicious_channel_text(uri):
                        stripped_traps.append(
                            _make_trap(
                                reason="pdf_hyperlink",
                                text=uri[:500],
                                location=f"{loc} (link)",
                                severity="high",
                            )
                        )
            except Exception:
                pass

            # 2. Audit Annotations (never merged into clean_text)
            try:
                for annot in page.annots() or []:
                    atype = annot.type[1] if annot.type else "Annot"
                    ainfo = annot.info or {}
                    content_parts = [
                        str(ainfo.get(k, "")).strip()
                        for k in ("content", "subject", "title")
                        if ainfo.get(k)
                    ]
                    annot_text = " | ".join(p for p in content_parts if p)
                    if annot_text:
                        stripped_traps.append(
                            _make_trap(
                                reason="pdf_annotation",
                                text=annot_text[:500],
                                location=f"{loc} (annot:{atype})",
                                severity="high" if _is_suspicious_channel_text(annot_text) else "medium",
                                details={"annot_type": atype},
                            )
                        )
            except Exception:
                pass

            # 3. Audit Form Fields / Widgets (never merged into clean_text)
            try:
                for widget in page.widgets() or []:
                    w_parts = [
                        str(getattr(widget, attr, "") or "").strip()
                        for attr in ("field_value", "field_label")
                    ]
                    w_text = " | ".join(p for p in w_parts if p)
                    if w_text:
                        stripped_traps.append(
                            _make_trap(
                                reason="pdf_form_field",
                                text=w_text[:500],
                                location=f"{loc} (field:{getattr(widget, 'field_name', '')})",
                                severity="high" if _is_suspicious_channel_text(w_text) else "medium",
                                details={"field_name": getattr(widget, "field_name", "")},
                            )
                        )
            except Exception:
                pass

            # 4. Embedded Images check + image-heavy page detection
            page_area = max(1.0, crop.width * crop.height)
            img_area_sum = 0.0
            for info in img_infos:
                ib = info.get("bbox")
                if ib:
                    ix0 = max(crop.x0, ib[0])
                    iy0 = max(crop.y0, ib[1])
                    ix1 = min(crop.x1, ib[2])
                    iy1 = min(crop.y1, ib[3])
                    img_area_sum += max(0.0, ix1 - ix0) * max(0.0, iy1 - iy0)
                xref = info.get("xref")
                if xref and xref not in audited_img_xrefs:
                    audited_img_xrefs.add(xref)
                    try:
                        img_dict = doc.extract_image(xref)
                        raw_img = img_dict.get("image") if img_dict else None
                        if raw_img:
                            from PIL import Image
                            with Image.open(io.BytesIO(raw_img)) as pil_im:
                                im_traps, im_warns = _inspect_pil_metadata(
                                    pil_im, raw_img, location_prefix=f"{loc}:img_xref_{xref}"
                                )
                                for t in im_traps:
                                    t["reason"] = "pdf_embedded_image_metadata"
                                stripped_traps.extend(im_traps)
                                extra_warnings.extend(im_warns)
                    except Exception:
                        pass

            coverage = min(1.0, img_area_sum / page_area)
            if coverage >= 0.55 or (len(img_infos) > 0 and visible_char_count < 40):
                image_heavy_pages.append(page_num)

        # 5. Audit hidden (OFF) OCG layers without adding them to clean_text
        if off_ocg_names:
            try:
                ui_cfgs = doc.layer_ui_configs() or []
                off_numbers = [cfg["number"] for cfg in ui_cfgs if not cfg.get("on", True)]
                if off_numbers:
                    for num in off_numbers:
                        doc.set_layer_ui_config(num, 0)  # temporarily turn ON to inspect
                    for page_idx in range(page_limit):
                        page = doc[page_idx]
                        for tr in page.get_texttrace() or []:
                            layer_name = tr.get("layer", "")
                            if layer_name in off_ocg_names:
                                h_text = "".join(chr(c[0]) for c in tr.get("chars", [])).strip()
                                if h_text:
                                    stripped_traps.append(
                                        _make_trap(
                                            reason="hidden_ocg_layer",
                                            text=h_text,
                                            location=f"page {page_idx + 1} (layer:{layer_name})",
                                            severity="high",
                                            details={"layer": layer_name},
                                        )
                                    )
                    for num in off_numbers:
                        doc.set_layer_ui_config(num, 2)  # restore OFF
            except Exception:
                # Even if layer_ui_configs isn't populated, report presence of OFF OCGs
                stripped_traps.append(
                    _make_trap(
                        reason="hidden_ocg_layer",
                        text=f"Hidden PDF OCG layer(s) detected: {', '.join(sorted(off_ocg_names))}",
                        location="pdf_ocg",
                        severity="medium",
                        details={"layers": sorted(off_ocg_names)},
                    )
                )

        # 6. Audit Bookmarks / TOC
        try:
            for lvl, title, _pno in doc.get_toc() or []:
                if title and _is_suspicious_channel_text(str(title)):
                    stripped_traps.append(
                        _make_trap(
                            reason="pdf_bookmark",
                            text=str(title)[:500],
                            location=f"pdf_toc:level_{lvl}",
                            severity="high",
                        )
                    )
        except Exception:
            pass

        # 7. Audit Embedded File Attachments
        try:
            for emb_name in doc.embfile_names() or []:
                emb_txt = ""
                try:
                    raw_emb = doc.embfile_get(emb_name)
                    if isinstance(raw_emb, bytes) and len(raw_emb) <= 262144:
                        emb_txt = raw_emb.decode("utf-8", errors="ignore")[:800]
                except Exception:
                    pass
                combined = f"{emb_name}: {emb_txt}".strip(": ")
                is_susp = _is_suspicious_channel_text(combined)
                stripped_traps.append(
                    _make_trap(
                        reason="pdf_attachment",
                        text=combined[:500],
                        location=f"pdf_attachment:{emb_name}",
                        severity="high" if is_susp else "medium",
                    )
                )
        except Exception:
            pass

        # 8. Audit Tagged PDF /Alt & /ActualText attributes (capped to avoid large-doc slowdown)
        try:
            xref_cap = min(doc.xref_length(), 2000)
            for xref in range(1, xref_cap):
                obj_str = doc.xref_object(xref, compressed=False)
                if not obj_str or ("/Alt" not in obj_str and "/ActualText" not in obj_str):
                    continue
                for key_m in re.finditer(r"/(Alt|ActualText)\s*(?:\(([^()]*)\)|<([0-9A-Fa-f]+)>)", obj_str):
                    val = key_m.group(2)
                    if val is None and key_m.group(3):
                        try:
                            raw_b = bytes.fromhex(key_m.group(3))
                            val = raw_b.decode("utf-16-be" if raw_b.startswith(b"\xfe\xff") else "latin-1", errors="ignore")
                        except Exception:
                            val = ""
                    if val and _is_suspicious_channel_text(val):
                        stripped_traps.append(
                            _make_trap(
                                reason="pdf_tagged_alt_text",
                                text=val.strip()[:500],
                                location=f"pdf_xref:{xref}/{key_m.group(1)}",
                                severity="high",
                            )
                        )
        except Exception:
            pass

    finally:
        doc.close()

    clean_text = "\n\n".join(p for p in clean_pages if p.strip())
    return _finalize_report(
        clean_text=clean_text,
        stripped_traps=stripped_traps,
        file_type="pdf",
        engine_used="pymupdf",
        source_path=pdf_path,
        extra_warnings=extra_warnings,
        stats={
            "total_pages": total_pages,
            "pages_scanned": page_limit,
            "image_heavy_pages": image_heavy_pages,
            "is_image_heavy_page": len(image_heavy_pages) > 0,
            "is_image_heavy_document": len(image_heavy_pages) > 0,
        },
    )


def _extract_pypdf_aux_channels(pdf_path: str, max_pages: Optional[int] = None) -> Tuple[List[TrapRecord], Dict[int, set[str]]]:
    """
    Helper using pypdf to audit PDF metadata, annotations, and detect `3 Tr`
    (invisible rendering mode) text strings in raw content streams for pdfplumber/pypdf fallback.
    """
    traps: List[TrapRecord] = []
    tr3_strings_by_page: Dict[int, set[str]] = {}
    try:
        import pypdf
        reader = pypdf.PdfReader(pdf_path)
        meta = reader.metadata or {}
        for k, v in meta.items():
            if isinstance(v, str) and v.strip():
                key_name = str(k).lstrip("/")
                if _is_suspicious_channel_text(v):
                    traps.append(
                        _make_trap(
                            reason="pdf_metadata",
                            text=v.strip()[:500],
                            location=f"pdf_metadata:{key_name}",
                            severity="high",
                            details={"field": key_name},
                        )
                    )
        pages = reader.pages if max_pages is None else reader.pages[:max_pages]
        for idx, pg in enumerate(pages, start=1):
            # Annotations
            annots = pg.get("/Annots") or []
            if hasattr(annots, "get_object"):
                annots = annots.get_object()
            for a_ref in annots or []:
                try:
                    a_obj = a_ref.get_object()
                    contents = str(a_obj.get("/Contents", "") or "").strip()
                    subtype = str(a_obj.get("/Subtype", "Annot")).lstrip("/")
                    if contents:
                        traps.append(
                            _make_trap(
                                reason="pdf_annotation",
                                text=contents[:500],
                                location=f"page {idx} (annot:{subtype})",
                                severity="high" if _is_suspicious_channel_text(contents) else "medium",
                                details={"annot_type": subtype},
                            )
                        )
                except Exception:
                    pass

            # Detect `3 Tr` text operations in raw content stream (both literal (...) and hex <...> strings)
            try:
                contents_obj = pg.get_contents()
                if contents_obj is not None:
                    raw = contents_obj.get_data()
                    if isinstance(raw, bytes) and b"Tr" in raw:
                        stream_txt = raw.decode("latin-1", errors="ignore")
                        cur_tr = 0
                        in_tr3_tokens: set[str] = set()

                        def _decode_pdf_hex(h: str) -> str:
                            h_clean = re.sub(r"\s+", "", h)
                            if len(h_clean) % 2 == 1:
                                h_clean += "0"
                            try:
                                raw_b = bytes.fromhex(h_clean)
                                if len(raw_b) >= 2 and raw_b[0] == 0:
                                    return raw_b.decode("utf-16-be", errors="ignore")
                                return raw_b.decode("latin-1", errors="ignore")
                            except Exception:
                                return ""

                        for m in re.finditer(
                            r"\b(ET|Q)\b|(\d+)\s+Tr\b|\(([^()]*)\)\s*Tj|<([0-9A-Fa-f\s]+)>\s*Tj|\[(.*?)\]\s*TJ",
                            stream_txt,
                            re.DOTALL,
                        ):
                            if m.group(1) is not None:
                                cur_tr = 0
                            elif m.group(2) is not None:
                                cur_tr = int(m.group(2))
                            elif cur_tr == 3:
                                if m.group(3) is not None:
                                    s = m.group(3).strip()
                                    if s:
                                        in_tr3_tokens.add(s)
                                elif m.group(4) is not None:
                                    s = _decode_pdf_hex(m.group(4)).strip()
                                    if s:
                                        in_tr3_tokens.add(s)
                                elif m.group(5) is not None:
                                    parts = []
                                    for item_m in re.finditer(r"\(([^()]*)\)|<([0-9A-Fa-f\s]+)>", m.group(5)):
                                        if item_m.group(1) is not None:
                                            parts.append(item_m.group(1))
                                        elif item_m.group(2) is not None:
                                            parts.append(_decode_pdf_hex(item_m.group(2)))
                                    joined = "".join(parts).strip()
                                    if joined:
                                        in_tr3_tokens.add(joined)
                        if in_tr3_tokens:
                            tr3_strings_by_page[idx] = in_tr3_tokens
            except Exception:
                pass
    except Exception:
        pass
    return traps, tr3_strings_by_page


def _sanitize_pdf_pdfplumber(
    pdf_path: str,
    max_pages: Optional[int],
    contrast_threshold: float,
    min_font_size: float,
) -> SanitizationReport:
    import pdfplumber  # type: ignore

    stripped_traps, tr3_by_page = _extract_pypdf_aux_channels(pdf_path, max_pages=max_pages)
    clean_pages: List[str] = []
    image_heavy_pages: List[int] = []
    total_pages = 0

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        pages = pdf.pages if max_pages is None else pdf.pages[:max_pages]

        for page_idx, page in enumerate(pages):
            page_num = page_idx + 1
            loc = f"page {page_num}"
            pw, ph = float(page.width), float(page.height)
            tr3_texts = tr3_by_page.get(page_num, set())

            filled_rects: List[Tuple[Tuple[float, float, float, float], Tuple[int, int, int]]] = []
            for r in list(page.rects or []) + list(page.curves or []):
                if r.get("fill") and r.get("non_stroking_color") is not None:
                    rgb = _pdf_color_to_rgb(r.get("non_stroking_color"))
                    if rgb is not None:
                        filled_rects.append(
                            ((float(r["x0"]), float(r["top"]), float(r["x1"]), float(r["bottom"])), rgb)
                        )

            img_bboxes: List[Tuple[float, float, float, float]] = []
            img_area = 0.0
            for im in page.images or []:
                ib = (float(im["x0"]), float(im["top"]), float(im["x1"]), float(im["bottom"]))
                img_bboxes.append(ib)
                img_area += max(0.0, ib[2] - ib[0]) * max(0.0, ib[3] - ib[1])

            # Group characters by approximate line (top rounded to 2pt)
            kept_chars: List[Dict[str, Any]] = []
            stripped_buckets: Dict[Tuple[str, int], List[str]] = {}

            for ch in page.chars or []:
                c_txt = ch.get("text", "")
                if not c_txt:
                    continue
                x0 = float(ch.get("x0", 0.0))
                x1 = float(ch.get("x1", 0.0))
                top = float(ch.get("top", 0.0))
                bottom = float(ch.get("bottom", 0.0))
                size = float(ch.get("size", 0.0))
                cb = (x0, top, x1, bottom)
                line_bucket = int(round(top / 4.0))

                nsc = ch.get("non_stroking_color")
                sc = ch.get("stroking_color")
                fg_rgb = _pdf_color_to_rgb(nsc) or _pdf_color_to_rgb(sc)
                render_mode = ch.get("rendering_mode", 0)

                reason: Optional[str] = None
                if x1 <= 0.5 or x0 >= pw - 0.5 or bottom <= 0.5 or top >= ph - 0.5:
                    reason = "off_page"
                elif render_mode == 3:
                    reason = "invisible_render_mode"
                elif size < min_font_size or (bottom - top) < min_font_size:
                    reason = "micro_font"
                elif fg_rgb is None:
                    reason = "invisible_render_mode"
                else:
                    # Determine local background from covering filled rects (prefer smallest/most-local rect)
                    bg_rgb = (255, 255, 255)
                    covering = [
                        ((rb[2] - rb[0]) * (rb[3] - rb[1]), r_rgb)
                        for rb, r_rgb in filled_rects
                        if _bbox_overlap_ratio(cb, rb) >= 0.70
                    ]
                    if covering:
                        covering.sort(key=lambda item: item[0])
                        bg_rgb = covering[0][1]

                    if contrast_ratio(fg_rgb, bg_rgb) < contrast_threshold:
                        reason = "white_text" if (_is_near_white(fg_rgb) and _is_near_white(bg_rgb)) else "low_contrast"
                    elif any(_bbox_overlap_ratio(cb, ib) >= 0.85 for ib in img_bboxes):
                        reason = "occluded_text"

                if reason is not None:
                    stripped_buckets.setdefault((reason, line_bucket), []).append(c_txt)
                else:
                    kept_chars.append(ch)

            # Reconstruct clean lines from kept_chars
            kept_chars.sort(key=lambda c: (round(float(c["top"]) / 4.0), float(c["x0"])))
            lines_out: List[str] = []
            cur_line_key: Optional[int] = None
            cur_line_chars: List[str] = []
            prev_x1: Optional[float] = None
            for ch in kept_chars:
                lk = int(round(float(ch["top"]) / 4.0))
                if cur_line_key is None or abs(lk - cur_line_key) > 1:
                    if cur_line_chars:
                        lines_out.append("".join(cur_line_chars).strip())
                    cur_line_key = lk
                    cur_line_chars = [ch["text"]]
                    prev_x1 = float(ch["x1"])
                else:
                    if prev_x1 is not None and float(ch["x0"]) - prev_x1 > max(1.5, float(ch.get("size", 10.0)) * 0.22):
                        cur_line_chars.append(" ")
                    cur_line_chars.append(ch["text"])
                    prev_x1 = float(ch["x1"])
            if cur_line_chars:
                lines_out.append("".join(cur_line_chars).strip())

            # Strip any `3 Tr` lines detected via pypdf content-stream scan
            filtered_lines: List[str] = []
            for ln in lines_out:
                if tr3_texts and any(t == ln or (len(t) >= 4 and t in ln) for t in tr3_texts):
                    stripped_traps.append(
                        _make_trap(
                            reason="invisible_render_mode",
                            text=ln,
                            location=loc,
                            severity="high",
                            details={"render_mode": 3},
                        )
                    )
                else:
                    filtered_lines.append(ln)

            for (reason, _), chars_list in stripped_buckets.items():
                txt = "".join(chars_list).strip()
                if txt:
                    stripped_traps.append(
                        _make_trap(
                            reason=reason,
                            text=txt,
                            location=loc,
                            severity="high",
                            details={},
                        )
                    )

            page_clean = "\n".join(l for l in filtered_lines if l)
            clean_pages.append(page_clean)

            page_area = max(1.0, pw * ph)
            if (img_area / page_area) >= 0.55 or (len(img_bboxes) > 0 and len(page_clean) < 40):
                image_heavy_pages.append(page_num)

    clean_text = "\n\n".join(p for p in clean_pages if p.strip())
    return _finalize_report(
        clean_text=clean_text,
        stripped_traps=stripped_traps,
        file_type="pdf",
        engine_used="pdfplumber",
        source_path=pdf_path,
        stats={
            "total_pages": total_pages,
            "pages_scanned": len(clean_pages),
            "image_heavy_pages": image_heavy_pages,
            "is_image_heavy_page": len(image_heavy_pages) > 0,
            "is_image_heavy_document": len(image_heavy_pages) > 0,
        },
    )


def _sanitize_pdf_pypdf(pdf_path: str, max_pages: Optional[int]) -> SanitizationReport:
    import pypdf

    stripped_traps, _ = _extract_pypdf_aux_channels(pdf_path, max_pages=max_pages)
    reader = pypdf.PdfReader(pdf_path)
    total_pages = len(reader.pages)
    pages = reader.pages if max_pages is None else reader.pages[:max_pages]
    text_pages = [(p.extract_text() or "") for p in pages]
    clean_text = "\n\n".join(t.strip() for t in text_pages if t.strip())
    return _finalize_report(
        clean_text=clean_text,
        stripped_traps=stripped_traps,
        file_type="pdf",
        engine_used="pypdf",
        source_path=pdf_path,
        stats={
            "total_pages": total_pages,
            "pages_scanned": len(pages),
            "image_heavy_pages": [],
            "is_image_heavy_page": False,
            "is_image_heavy_document": False,
        },
    )


def sanitize_pdf(
    pdf_path: str,
    engine: str = "auto",
    max_pages: Optional[int] = None,
    contrast_threshold: float = 1.8,
    min_font_size: float = 4.0,
    min_opacity: float = 0.15,
) -> SanitizationReport:
    """
    Layer 1: Dual-Engine PDF Sanitizer (`pymupdf` primary, `pdfplumber` fallback, `pypdf` fallback).
    """
    if not os.path.exists(pdf_path):
        return SanitizationReport(
            file_type="pdf", engine_used="none", risk_level="none", source_path=pdf_path
        )

    engine = (engine or "auto").lower()

    if engine in ("auto", "pymupdf", "fitz"):
        if _import_pymupdf() is not None:
            try:
                return _sanitize_pdf_pymupdf(
                    pdf_path, max_pages, contrast_threshold, min_font_size, min_opacity
                )
            except Exception:
                if engine in ("pymupdf", "fitz"):
                    raise

    if engine in ("auto", "pdfplumber"):
        try:
            import pdfplumber  # noqa: F401
            return _sanitize_pdf_pdfplumber(
                pdf_path, max_pages, contrast_threshold, min_font_size
            )
        except Exception:
            if engine == "pdfplumber":
                raise

    try:
        return _sanitize_pdf_pypdf(pdf_path, max_pages)
    except Exception:
        return SanitizationReport(
            file_type="pdf",
            engine_used="failed",
            risk_level="none",
            source_path=os.path.abspath(pdf_path),
            stats={"error": "Unable to parse PDF with any available engine"},
        )


# ---------------------------------------------------------------------------
# Layer 2: Images & Photos (`PNG`, `JPG`, `WEBP`, `BMP`, `GIF`, `SVG`)
# ---------------------------------------------------------------------------

def _parse_inline_style(style_str: str) -> Dict[str, str]:
    res: Dict[str, str] = {}
    if not style_str:
        return res
    for part in style_str.split(";"):
        if ":" in part:
            k, v = part.split(":", 1)
            res[k.strip().lower()] = v.strip()
    return res


def _parse_css_rules(css_text: str) -> Dict[str, Dict[str, str]]:
    """Parses simple CSS selector blocks (.class, #id, tag) from <style> blocks."""
    rules: Dict[str, Dict[str, str]] = {}
    if not css_text:
        return rules
    cleaned_css = re.sub(r"/\*.*?\*/", "", css_text, flags=re.DOTALL)
    for m in re.finditer(r"([^{}]+)\{([^{}]+)\}", cleaned_css):
        selectors = [s.strip().lower() for s in m.group(1).split(",") if s.strip()]
        decls = _parse_inline_style(m.group(2))
        if not decls:
            continue
        for sel in selectors:
            rules.setdefault(sel, {}).update(decls)
    return rules


def _resolve_css_for_element(
    tag: str,
    attr_dict: Dict[str, Optional[str]],
    css_rules: Optional[Dict[str, Dict[str, str]]],
) -> Dict[str, str]:
    """Merges tag, .class, #id CSS rules and inline style='' (inline wins)."""
    merged: Dict[str, str] = {}
    if css_rules:
        tl = tag.lower()
        if tl in css_rules:
            merged.update(css_rules[tl])
        for cls_tok in (attr_dict.get("class") or "").split():
            key = f".{cls_tok.strip().lower()}"
            if key in css_rules:
                merged.update(css_rules[key])
        el_id = (attr_dict.get("id") or "").strip().lower()
        if el_id:
            id_key = f"#{el_id}"
            if id_key in css_rules:
                merged.update(css_rules[id_key])
    merged.update(_parse_inline_style(attr_dict.get("style") or ""))
    return merged


def _parse_css_font_size_pt(val: Optional[str]) -> Optional[float]:
    if not val:
        return None
    m = re.match(r"^\s*([0-9]*\.?[0-9]+)\s*(px|pt|em|rem|%)?", val.strip().lower())
    if not m:
        return None
    num = float(m.group(1))
    unit = m.group(2) or "px"
    if unit == "pt":
        return num
    if unit == "px":
        return num * 0.75
    if unit in ("em", "rem"):
        return num * 12.0
    if unit == "%":
        return (num / 100.0) * 12.0
    return num


def sanitize_svg(
    svg_path: str,
    contrast_threshold: float = 1.8,
    min_font_size: float = 4.0,
    min_opacity: float = 0.15,
) -> SanitizationReport:
    """Sanitizes SVG vector files: strips XML comments, metadata, hidden/micro/low-contrast/off-canvas text."""
    with open(svg_path, "r", encoding="utf-8", errors="ignore") as f:
        raw_svg = f.read()

    stripped_traps: List[TrapRecord] = []

    # 1. Extract XML comments
    for idx, m in enumerate(re.finditer(r"<!--(.*?)-->", raw_svg, re.DOTALL), start=1):
        comment_txt = m.group(1).strip()
        if comment_txt:
            stripped_traps.append(
                _make_trap(
                    reason="svg_comment",
                    text=comment_txt[:500],
                    location=f"svg:comment#{idx}",
                    severity="high" if _is_suspicious_channel_text(comment_txt) else "medium",
                )
            )

    clean_lines: List[str] = []
    try:
        root = ET.fromstring(raw_svg)
    except ET.ParseError:
        return _finalize_report(
            clean_text="",
            stripped_traps=stripped_traps,
            file_type="svg",
            engine_used="svg-xml",
            source_path=svg_path,
            stats={"parse_error": True},
        )

    def _local(tag: str) -> str:
        return tag.split("}", 1)[-1].lower() if "}" in tag else tag.lower()

    # Determine viewBox bounds
    vb_bounds: Optional[Tuple[float, float, float, float]] = None
    vb_attr = root.attrib.get("viewBox") or root.attrib.get("viewbox")
    if vb_attr:
        nums = [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", vb_attr)]
        if len(nums) == 4:
            vb_bounds = (nums[0], nums[1], nums[0] + nums[2], nums[1] + nums[3])
    else:
        w_m = re.match(r"^\s*([0-9\.]+)", root.attrib.get("width", ""))
        h_m = re.match(r"^\s*([0-9\.]+)", root.attrib.get("height", ""))
        if w_m and h_m:
            vb_bounds = (0.0, 0.0, float(w_m.group(1)), float(h_m.group(1)))

    # Collect <style> rules inside SVG
    css_rules: Dict[str, Dict[str, str]] = {}
    for st_el in root.iter():
        if _local(st_el.tag) == "style" and st_el.text:
            css_rules.update(_parse_css_rules(st_el.text))

    # Detect background color from a full-size initial <rect> if present
    bg_rgb: Tuple[int, int, int] = (255, 255, 255)
    for child in list(root)[:4]:
        if _local(child.tag) == "rect":
            st = _resolve_css_for_element("rect", dict(child.attrib), css_rules)
            fill_val = st.get("fill") or child.attrib.get("fill")
            rgb, a = parse_css_color(fill_val)
            if rgb is not None and (a is None or a > 0.8):
                rw = child.attrib.get("width", "")
                rh = child.attrib.get("height", "")
                if rw == "100%" or rh == "100%" or (vb_bounds and rw and float(re.findall(r"[\d\.]+", rw)[0]) >= (vb_bounds[2] - vb_bounds[0]) * 0.8):
                    bg_rgb = rgb
                    break

    def _walk(
        elem: ET.Element,
        inherited_hidden: Optional[str],
        inherited_opacity: float,
        inherited_fill: Tuple[int, int, int],
        inherited_fsize: float,
    ) -> None:
        tag = _local(elem.tag)
        if tag in ("desc", "metadata", "title"):
            txt = "".join(elem.itertext()).strip()
            if txt and (_is_suspicious_channel_text(txt) or tag in ("desc", "metadata")):
                stripped_traps.append(
                    _make_trap(
                        reason="svg_metadata",
                        text=txt[:500],
                        location=f"svg:<{tag}>",
                        severity="high" if _is_suspicious_channel_text(txt) else "medium",
                        details={"tag": tag},
                    )
                )
            return
        if tag == "style":
            return
        if tag == "foreignobject":
            inner_html = "".join(ET.tostring(c, encoding="unicode") for c in elem)
            if inner_html.strip():
                fo_rep = sanitize_markup(inner_html, markup_type="html", is_text=True)
                stripped_traps.extend(fo_rep.stripped_traps)
                if fo_rep.clean_text:
                    clean_lines.append(fo_rep.clean_text)
            return

        elem_attrs = {k.lower(): v for k, v in elem.attrib.items()}
        st = _resolve_css_for_element(tag, elem_attrs, css_rules)
        display = (st.get("display") or elem_attrs.get("display") or "").strip().lower()
        visibility = (st.get("visibility") or elem_attrs.get("visibility") or "").strip().lower()
        transform = (st.get("transform") or elem_attrs.get("transform") or "").strip().lower()

        op_str = st.get("opacity") or elem_attrs.get("opacity")
        fill_op_str = st.get("fill-opacity") or elem_attrs.get("fill-opacity")
        cur_op = inherited_opacity
        for ostr in (op_str, fill_op_str):
            if ostr is not None:
                try:
                    cur_op = min(cur_op, float(ostr))
                except ValueError:
                    pass

        fill_str = st.get("fill") or elem_attrs.get("fill")
        cur_fill = inherited_fill
        if fill_str is not None:
            if fill_str.strip().lower() == "none":
                cur_op = 0.0
            else:
                rgb, ca = parse_css_color(fill_str)
                if rgb is not None:
                    cur_fill = rgb
                if ca is not None:
                    cur_op = min(cur_op, ca)

        fsize_str = st.get("font-size") or elem_attrs.get("font-size")
        parsed_fs = _parse_css_font_size_pt(fsize_str)
        cur_fs = parsed_fs if parsed_fs is not None else inherited_fsize

        cur_hidden = inherited_hidden
        if cur_hidden is None:
            if display == "none" or visibility == "hidden":
                cur_hidden = "svg_hidden_element"
            elif re.search(r"scale[xy]?\(\s*0(?:\.0+)?\s*(?:,|\))", transform):
                cur_hidden = "svg_hidden_element"
            elif cur_op < min_opacity:
                cur_hidden = "svg_low_opacity"
            elif cur_fs < min_font_size:
                cur_hidden = "svg_micro_font"

        if tag in ("text", "tspan"):
            # Check off-canvas coordinates
            local_hidden = cur_hidden
            if local_hidden is None and vb_bounds is not None:
                xs = re.findall(r"-?\d+(?:\.\d+)?", elem.attrib.get("x", ""))
                ys = re.findall(r"-?\d+(?:\.\d+)?", elem.attrib.get("y", ""))
                if xs:
                    xv = float(xs[0])
                    if xv < vb_bounds[0] - 5 or xv > vb_bounds[2] + 5:
                        local_hidden = "svg_off_canvas"
                if ys and local_hidden is None:
                    yv = float(ys[0])
                    if yv < vb_bounds[1] - 5 or yv > vb_bounds[3] + 5:
                        local_hidden = "svg_off_canvas"

            if local_hidden is None and contrast_ratio(cur_fill, bg_rgb) < contrast_threshold:
                local_hidden = "svg_low_contrast"

            own_text = (elem.text or "").strip()
            if own_text:
                if local_hidden:
                    stripped_traps.append(
                        _make_trap(
                            reason=local_hidden,
                            text=own_text,
                            location=f"svg:<{tag}>",
                            severity="high",
                            details={
                                "fill": "#{:02x}{:02x}{:02x}".format(*cur_fill),
                                "opacity": round(cur_op, 3),
                                "font_size": round(cur_fs, 2),
                            },
                        )
                    )
                else:
                    clean_lines.append(own_text)

            for child in elem:
                _walk(child, local_hidden, cur_op, cur_fill, cur_fs)
                tail_txt = (child.tail or "").strip()
                if tail_txt:
                    if local_hidden:
                        stripped_traps.append(
                            _make_trap(
                                reason=local_hidden,
                                text=tail_txt,
                                location=f"svg:<{tag}>",
                                severity="high",
                            )
                        )
                    else:
                        clean_lines.append(tail_txt)
            return

        for child in elem:
            _walk(child, cur_hidden, cur_op, cur_fill, cur_fs)

    _walk(root, None, 1.0, (0, 0, 0), 12.0)

    return _finalize_report(
        clean_text="\n".join(clean_lines),
        stripped_traps=stripped_traps,
        file_type="svg",
        engine_used="svg-xml",
        source_path=svg_path,
        stats={"bg_color": "#{:02x}{:02x}{:02x}".format(*bg_rgb)},
    )


def sanitize_image(
    image_path: str,
    out_image_path: Optional[str] = None,
    alpha_zero_threshold: int = 15,
    neutralize_low_contrast: bool = True,
) -> SanitizationReport:
    """
    Layer 2: Sanitizes raster images (PNG, JPG, JPEG, WEBP, BMP, GIF) and SVG vectors.
    - Audits & strips all metadata (EXIF, XMP, IPTC, JPEG COM, PNG tEXt/iTXt/zTXt).
    - Detects trailing polyglot bytes (post-IEND / post-FFD9) & multi-frame GIF/APNG.
    - Detects RGB steganography hidden behind alpha == 0 pixels.
    - Flattens alpha channel (alpha < 15 -> white) onto solid white RGB & optionally
      snaps invisible near-background low-contrast RGB pixels (#F6F6F6..#FEFEFE on white).
    """
    if not os.path.exists(image_path):
        return SanitizationReport(
            file_type="image", engine_used="none", risk_level="none", source_path=image_path
        )

    ext = os.path.splitext(image_path)[1].lower()
    if ext == ".svg":
        return sanitize_svg(image_path)

    from PIL import Image

    with open(image_path, "rb") as f:
        raw_bytes = f.read()

    stripped_traps: List[TrapRecord] = []
    extra_warnings: List[TrapRecord] = []
    alpha_stego_suspected = False
    had_alpha = False
    frames_stripped = 0
    low_contrast_neutralized = 0
    width = height = 0

    # Trailing polyglot inspection (post PNG IEND+CRC or JPEG EOI FF D9)
    trailing_bytes = b""
    if raw_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
        iend_idx = raw_bytes.find(b"IEND")
        if iend_idx != -1 and iend_idx + 8 < len(raw_bytes):
            trailing_bytes = raw_bytes[iend_idx + 8:]
    elif raw_bytes.startswith(b"\xff\xd8"):
        eoi_idx = raw_bytes.rfind(b"\xff\xd9")
        if eoi_idx != -1 and eoi_idx + 2 < len(raw_bytes):
            trailing_bytes = raw_bytes[eoi_idx + 2:]

    if len(trailing_bytes) >= 8:
        trailing_txt = re.sub(r"[^\x20-\x7e\r\n\t]+", " ", trailing_bytes.decode("utf-8", errors="ignore")).strip()
        if len(trailing_txt) >= 4:
            is_susp = _is_suspicious_channel_text(trailing_txt)
            stripped_traps.append(
                _make_trap(
                    reason="image_trailing_polyglot",
                    text=trailing_txt[:500],
                    location=f"{os.path.basename(image_path)}:trailing_bytes",
                    severity="high" if is_susp else "medium",
                    details={"trailing_len": len(trailing_bytes)},
                )
            )

    with Image.open(io.BytesIO(raw_bytes)) as img:
        width, height = img.size
        orig_mode = img.mode
        orig_format = img.format or ext.lstrip(".").upper()
        n_frames = int(getattr(img, "n_frames", 1) or 1)
        if n_frames > 1:
            frames_stripped = n_frames - 1
            stripped_traps.append(
                _make_trap(
                    reason="image_multiframe_stripped",
                    text=f"Animated image had {n_frames} frames; flattened frame 1 only (dropped {frames_stripped} hidden frame(s))",
                    location=f"{os.path.basename(image_path)}:frames",
                    severity="medium",
                    details={"n_frames": n_frames},
                )
            )

        # 1. Inspect metadata
        meta_traps, meta_warns = _inspect_pil_metadata(
            img, raw_bytes, location_prefix=os.path.basename(image_path)
        )
        stripped_traps.extend(meta_traps)
        extra_warnings.extend(meta_warns)

        # 2. Alpha-channel stego detection & flattening
        has_alpha = (
            orig_mode in ("RGBA", "LA", "PA", "RGBa", "La")
            or (orig_mode == "P" and "transparency" in img.info)
        )
        had_alpha = has_alpha

        if has_alpha:
            rgba = img.convert("RGBA")
            pixels = list(rgba.get_flattened_data()) if hasattr(rgba, "get_flattened_data") else list(rgba.getdata())

            # Detect structured RGB variation hidden behind alpha == 0
            zero_alpha_rgbs = [(r, g, b) for (r, g, b, a) in pixels if a == 0]
            if len(zero_alpha_rgbs) >= 16:
                counts: Dict[Tuple[int, int, int], int] = {}
                for rgb in zero_alpha_rgbs:
                    counts[rgb] = counts.get(rgb, 0) + 1
                if len(counts) >= 2:
                    mode_rgb = max(counts.items(), key=lambda kv: kv[1])[0]
                    mr, mg, mb = mode_rgb
                    divergent = sum(
                        cnt
                        for (r, g, b), cnt in counts.items()
                        if (abs(r - mr) + abs(g - mg) + abs(b - mb)) >= 15
                    )
                    if divergent >= 10:
                        alpha_stego_suspected = True
                        stripped_traps.append(
                            _make_trap(
                                reason="alpha_channel_stego_suspected",
                                text=(
                                    f"Structured RGB variation detected behind {len(zero_alpha_rgbs)} "
                                    f"fully transparent (alpha=0) pixels ({divergent} divergent pixels, "
                                    f"{len(counts)} unique RGB values)"
                                ),
                                location=f"{os.path.basename(image_path)}:alpha_channel",
                                severity="high",
                                details={
                                    "transparent_pixels": len(zero_alpha_rgbs),
                                    "divergent_pixels": divergent,
                                    "unique_rgb_behind_alpha0": len(counts),
                                },
                            )
                        )

            # Flatten: force pixels with alpha < threshold to white transparent, then composite on solid white
            cleaned_rgba_pixels = [
                (255, 255, 255, 0) if a < alpha_zero_threshold else (r, g, b, a)
                for (r, g, b, a) in pixels
            ]
            cleaned_rgba = Image.new("RGBA", rgba.size)
            cleaned_rgba.putdata(cleaned_rgba_pixels)
            white_bg = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
            composited = Image.alpha_composite(white_bg, cleaned_rgba).convert("RGB")
        else:
            # Strip metadata by copying raw pixel data into a brand-new Image
            rgb = img.convert("RGB")
            composited = Image.new("RGB", rgb.size)
            rgb_pixels = list(rgb.get_flattened_data()) if hasattr(rgb, "get_flattened_data") else list(rgb.getdata())
            composited.putdata(rgb_pixels)

        # Conservative near-background low-contrast snap (destroys #F8F8F8/#FAFAFA traps on #FFFFFF)
        if neutralize_low_contrast:
            final_px = list(composited.get_flattened_data()) if hasattr(composited, "get_flattened_data") else list(composited.getdata())
            total_px = max(1, len(final_px))
            pure_white_cnt = sum(1 for (r, g, b) in final_px if r == 255 and g == 255 and b == 255)
            pure_black_cnt = sum(1 for (r, g, b) in final_px if r == 0 and g == 0 and b == 0)

            snap_white = (pure_white_cnt / total_px) >= 0.25
            snap_black = (pure_black_cnt / total_px) >= 0.25
            if snap_white or snap_black:
                snapped_px: List[Tuple[int, int, int]] = []
                for (r, g, b) in final_px:
                    if snap_white and 246 <= r <= 254 and 246 <= g <= 254 and 246 <= b <= 254:
                        snapped_px.append((255, 255, 255))
                        low_contrast_neutralized += 1
                    elif snap_black and 1 <= r <= 10 and 1 <= g <= 10 and 1 <= b <= 10:
                        snapped_px.append((0, 0, 0))
                        low_contrast_neutralized += 1
                    else:
                        snapped_px.append((r, g, b))
                if low_contrast_neutralized > 0:
                    composited.putdata(snapped_px)
                    if low_contrast_neutralized >= 40:
                        stripped_traps.append(
                            _make_trap(
                                reason="image_low_contrast_neutralized",
                                text=f"Neutralized {low_contrast_neutralized} invisible near-background RGB pixel(s)",
                                location=f"{os.path.basename(image_path)}:rgb_contrast",
                                severity="low",
                                details={"pixels_neutralized": low_contrast_neutralized},
                            )
                        )

    # 3. Save clean metadata-free, alpha-flattened copy
    if out_image_path:
        target_out = os.path.abspath(out_image_path)
        os.makedirs(os.path.dirname(target_out), exist_ok=True)
    else:
        safe_dir = os.path.join(tempfile.gettempdir(), "ngelaprak_sanitized")
        os.makedirs(safe_dir, exist_ok=True)
        stem = os.path.splitext(os.path.basename(image_path))[0]
        target_out = os.path.join(safe_dir, f"{stem}_clean.png")

    out_ext = os.path.splitext(target_out)[1].lower()
    if out_ext in (".jpg", ".jpeg"):
        composited.save(target_out, format="JPEG", quality=95)
    elif out_ext == ".webp":
        composited.save(target_out, format="WEBP", quality=95)
    elif out_ext == ".bmp":
        composited.save(target_out, format="BMP")
    else:
        composited.save(target_out, format="PNG")

    return _finalize_report(
        clean_text="",
        stripped_traps=stripped_traps,
        file_type="image",
        engine_used="pillow",
        source_path=image_path,
        sanitized_image_path=target_out,
        extra_warnings=extra_warnings,
        stats={
            "width": width,
            "height": height,
            "original_mode": orig_mode,
            "original_format": orig_format,
            "had_alpha": had_alpha,
            "alpha_flattened": had_alpha,
            "alpha_channel_stego_suspected": alpha_stego_suspected,
            "frames_stripped": frames_stripped,
            "low_contrast_pixels_neutralized": low_contrast_neutralized,
            "metadata_stripped": True,
        },
        run_unicode_on_clean=False,
    )


# ---------------------------------------------------------------------------
# Layer 3: Academic Document Formats (DOCX, PPTX, XLSX, HTML, Markdown, ipynb, Code)
# ---------------------------------------------------------------------------

_VML_NS = "urn:schemas-microsoft-com:vml"
_W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
_WP_NS = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
_A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
_P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
_R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
_S_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"


def _w(tag: str) -> str:
    return f"{{{_W_NS}}}{tag}"


def _a(tag: str) -> str:
    return f"{{{_A_NS}}}{tag}"


def _p(tag: str) -> str:
    return f"{{{_P_NS}}}{tag}"


def _s(tag: str) -> str:
    return f"{{{_S_NS}}}{tag}"


def _audit_ooxml_core_props(zf: zipfile.ZipFile, reason: str) -> List[TrapRecord]:
    traps: List[TrapRecord] = []
    for prop_file in ("docProps/core.xml", "docProps/app.xml", "docProps/custom.xml"):
        if prop_file not in zf.namelist():
            continue
        try:
            root = ET.fromstring(zf.read(prop_file))
            for elem in root.iter():
                txt = (elem.text or "").strip()
                if not txt:
                    continue
                tag_name = elem.tag.split("}", 1)[-1]
                clean_v, uni_traps, _ = sanitize_text(txt, location=f"{prop_file}:{tag_name}")
                traps.extend(uni_traps)
                if _is_suspicious_channel_text(clean_v):
                    traps.append(
                        _make_trap(
                            reason=reason,
                            text=clean_v[:500],
                            location=f"{prop_file}:{tag_name}",
                            severity="high",
                            details={"field": tag_name},
                        )
                    )
        except Exception:
            pass
    return traps


def _ooxml_bool_prop(parent: Optional[ET.Element], tag: str) -> Optional[bool]:
    if parent is None:
        return None
    el = parent.find(tag)
    if el is None:
        return None
    val = el.attrib.get(_w("val"))
    if val is None:
        return True
    return val.lower() not in ("0", "false", "off", "none")


def _audit_ooxml_media(
    zf: zipfile.ZipFile,
    media_prefix: str,
    reason_prefix: str,
) -> Tuple[List[TrapRecord], List[TrapRecord]]:
    traps: List[TrapRecord] = []
    warnings: List[TrapRecord] = []
    for mpath in sorted(n for n in zf.namelist() if n.startswith(media_prefix)):
        ext = os.path.splitext(mpath)[1].lower()
        if ext not in (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"):
            continue
        try:
            raw = zf.read(mpath)
            from PIL import Image
            with Image.open(io.BytesIO(raw)) as pil_im:
                im_traps, im_warns = _inspect_pil_metadata(
                    pil_im, raw, location_prefix=mpath
                )
                for t in im_traps:
                    t["reason"] = f"{reason_prefix}_embedded_image_metadata"
                traps.extend(im_traps)
                warnings.extend(im_warns)
        except Exception:
            pass
    return traps, warnings


def sanitize_docx(
    docx_path: str,
    contrast_threshold: float = 1.8,
    min_font_size: float = 4.0,
) -> SanitizationReport:
    """
    Layer 3a: Sanitizes DOCX files via OOXML inspection.
    Strips <w:vanish/>, <w:webHidden/> (including via style inheritance), white/low-contrast
    runs vs <w:shd>, micro-font (< 4pt / w:sz < 8), <w:del>, comments.xml, off-canvas
    textboxes, VML hidden shapes, Word field codes (<w:instrText>), header/footer/footnote
    hidden traps, alt-text, embedded media metadata, and core metadata.
    """
    if not os.path.exists(docx_path):
        return SanitizationReport(
            file_type="docx", engine_used="none", risk_level="none", source_path=docx_path
        )

    stripped_traps: List[TrapRecord] = []
    extra_warnings: List[TrapRecord] = []
    clean_paragraphs: List[str] = []

    with zipfile.ZipFile(docx_path, "r") as zf:
        names = set(zf.namelist())

        # 1. Audit metadata & embedded media
        stripped_traps.extend(_audit_ooxml_core_props(zf, reason="docx_metadata"))
        m_traps, m_warns = _audit_ooxml_media(zf, "word/media/", "docx")
        stripped_traps.extend(m_traps)
        extra_warnings.extend(m_warns)

        # 2. Audit comments.xml (never included in clean_text)
        if "word/comments.xml" in names:
            try:
                c_root = ET.fromstring(zf.read("word/comments.xml"))
                for idx, c_el in enumerate(c_root.findall(_w("comment")), start=1):
                    c_txt = "".join(t.text or "" for t in c_el.iter(_w("t"))).strip()
                    if c_txt:
                        stripped_traps.append(
                            _make_trap(
                                reason="docx_comment",
                                text=c_txt[:500],
                                location=f"comment#{idx}",
                                severity="high" if _is_suspicious_channel_text(c_txt) else "medium",
                                details={"author": c_el.attrib.get(_w("author"), "")},
                            )
                        )
            except Exception:
                pass

        # 3. Parse styles.xml for inherited vanish / webHidden / color / sz
        styles_info: Dict[str, Dict[str, Any]] = {}
        if "word/styles.xml" in names:
            try:
                s_root = ET.fromstring(zf.read("word/styles.xml"))
                for st in s_root.findall(_w("style")):
                    sid = st.attrib.get(_w("styleId"), "")
                    based_on_el = st.find(_w("basedOn"))
                    based_on = based_on_el.attrib.get(_w("val")) if based_on_el is not None else None
                    rpr = st.find(_w("rPr"))
                    ppr = st.find(_w("pPr"))
                    st_dict: Dict[str, Any] = {"basedOn": based_on}
                    if rpr is not None:
                        v = _ooxml_bool_prop(rpr, _w("vanish"))
                        if v is not None:
                            st_dict["vanish"] = v
                        wh = _ooxml_bool_prop(rpr, _w("webHidden"))
                        if wh is not None:
                            st_dict["webHidden"] = wh
                        c_el = rpr.find(_w("color"))
                        if c_el is not None and c_el.attrib.get(_w("val")):
                            st_dict["color"] = c_el.attrib.get(_w("val"))
                        sz_el = rpr.find(_w("sz"))
                        if sz_el is not None and sz_el.attrib.get(_w("val")):
                            try:
                                st_dict["sz_pt"] = float(sz_el.attrib[_w("val")]) / 2.0
                            except ValueError:
                                pass
                        shd_el = rpr.find(_w("shd"))
                        if shd_el is not None and shd_el.attrib.get(_w("fill")):
                            st_dict["shd"] = shd_el.attrib.get(_w("fill"))
                    if ppr is not None:
                        shd_el = ppr.find(_w("shd"))
                        if shd_el is not None and shd_el.attrib.get(_w("fill")):
                            st_dict.setdefault("shd", shd_el.attrib.get(_w("fill")))
                    if sid:
                        styles_info[sid] = st_dict
            except Exception:
                pass

        def _resolve_style(sid: Optional[str]) -> Dict[str, Any]:
            merged: Dict[str, Any] = {}
            chain: List[str] = []
            cur = sid
            while cur and cur in styles_info and cur not in chain:
                chain.append(cur)
                cur = styles_info[cur].get("basedOn")
            for s in reversed(chain):
                merged.update({k: v for k, v in styles_info[s].items() if k != "basedOn"})
            return merged

        def _is_off_canvas_drawing(drawing_el: ET.Element) -> bool:
            for ext_el in drawing_el.iter(f"{{{_WP_NS}}}extent"):
                cx = int(ext_el.attrib.get("cx", "1") or "1")
                cy = int(ext_el.attrib.get("cy", "1") or "1")
                if cx <= 0 or cy <= 0:
                    return True
            for pos_el in drawing_el.iter(f"{{{_WP_NS}}}posOffset"):
                try:
                    val = int((pos_el.text or "0").strip())
                    if val < -914400 or val > 11887200:
                        return True
                except ValueError:
                    pass
            return False

        def _is_hidden_vml_shape(shape_el: ET.Element) -> bool:
            st = _parse_inline_style(shape_el.attrib.get("style", ""))
            if st.get("visibility", "").lower() == "hidden" or st.get("display", "").lower() == "none":
                return True
            for prop in ("left", "margin-left", "top", "margin-top"):
                m = re.match(r"^\s*-(\d+(?:\.\d+)?)", st.get(prop, ""))
                if m and float(m.group(1)) >= 400:
                    return True
            return False

        def _scan_xml_part(xml_path: str, loc_prefix: str, collect_clean: bool) -> None:
            root_el = ET.fromstring(zf.read(xml_path))

            # Audit image alt-text <wp:docPr descr/title> and hyperlink tooltips
            for docpr in root_el.iter(f"{{{_WP_NS}}}docPr"):
                for attr in ("descr", "title"):
                    aval = (docpr.attrib.get(attr) or "").strip()
                    if aval and _is_suspicious_channel_text(aval):
                        stripped_traps.append(
                            _make_trap(
                                reason="docx_alt_text",
                                text=aval[:500],
                                location=f"{loc_prefix}:docPr.{attr}",
                                severity="high",
                            )
                        )
            for hlink in root_el.iter(_w("hyperlink")):
                tval = (hlink.attrib.get(_w("tooltip")) or "").strip()
                if tval and _is_suspicious_channel_text(tval):
                    stripped_traps.append(
                        _make_trap(
                            reason="docx_alt_text",
                            text=tval[:500],
                            location=f"{loc_prefix}:hyperlink.tooltip",
                            severity="high",
                        )
                    )

            # Audit Word Field Codes <w:instrText>
            for instr in root_el.iter(_w("instrText")):
                itxt = (instr.text or "").strip()
                if itxt and _is_suspicious_channel_text(itxt):
                    stripped_traps.append(
                        _make_trap(
                            reason="docx_field_code",
                            text=itxt[:500],
                            location=f"{loc_prefix}:instrText",
                            severity="high",
                        )
                    )

            # Pre-identify paragraphs inside off-canvas drawings or hidden VML shapes
            off_canvas_ps: set[int] = set()
            for draw in root_el.iter(_w("drawing")):
                if _is_off_canvas_drawing(draw):
                    for inner_p in draw.iter(_w("p")):
                        off_canvas_ps.add(id(inner_p))
            for vshape in root_el.iter(f"{{{_VML_NS}}}shape"):
                if _is_hidden_vml_shape(vshape):
                    for inner_p in vshape.iter(_w("p")):
                        off_canvas_ps.add(id(inner_p))

            # Build cell shading map for table cells
            cell_shd_map: Dict[int, Tuple[int, int, int]] = {}
            for tc in root_el.iter(_w("tc")):
                tcpr = tc.find(_w("tcPr"))
                if tcpr is not None:
                    shd = tcpr.find(_w("shd"))
                    if shd is not None:
                        rgb, _ = parse_css_color(shd.attrib.get(_w("fill")))
                        if rgb is not None:
                            for inner_p in tc.iter(_w("p")):
                                cell_shd_map[id(inner_p)] = rgb

            for p_idx, p_el in enumerate(root_el.iter(_w("p")), start=1):
                loc = f"{loc_prefix}paragraph {p_idx}"

                if id(p_el) in off_canvas_ps:
                    txt = "".join(t.text or "" for t in p_el.iter(_w("t"))).strip()
                    if txt:
                        stripped_traps.append(
                            _make_trap(
                                reason="docx_off_canvas",
                                text=txt,
                                location=loc,
                                severity="high",
                            )
                        )
                    continue

                for del_el in p_el.findall(_w("del")):
                    del_txt = "".join(dt.text or "" for dt in del_el.iter(_w("delText"))).strip()
                    if del_txt:
                        stripped_traps.append(
                            _make_trap(
                                reason="docx_deleted_text",
                                text=del_txt,
                                location=loc,
                                severity="medium",
                            )
                        )

                ppr = p_el.find(_w("pPr"))
                p_style_id = None
                p_bg_rgb = cell_shd_map.get(id(p_el), (255, 255, 255))
                if ppr is not None:
                    ps_el = ppr.find(_w("pStyle"))
                    if ps_el is not None:
                        p_style_id = ps_el.attrib.get(_w("val"))
                    p_shd = ppr.find(_w("shd"))
                    if p_shd is not None:
                        rgb, _ = parse_css_color(p_shd.attrib.get(_w("fill")))
                        if rgb is not None:
                            p_bg_rgb = rgb

                p_style_props = _resolve_style(p_style_id)
                if p_style_props.get("shd"):
                    rgb, _ = parse_css_color(p_style_props["shd"])
                    if rgb is not None and p_bg_rgb == (255, 255, 255):
                        p_bg_rgb = rgb

                p_parts: List[str] = []

                def _iter_visible_runs(node: ET.Element) -> Iterable[ET.Element]:
                    for child in node:
                        if child.tag == _w("r"):
                            yield child
                        elif child.tag in (_w("hyperlink"), _w("ins"), _w("smartTag"), _w("sdt"), _w("sdtContent")):
                            yield from _iter_visible_runs(child)

                for r_el in _iter_visible_runs(p_el):
                    run_text = "".join(t.text or "" for t in r_el.findall(_w("t")))
                    if not run_text:
                        continue
                    if not run_text.strip():
                        p_parts.append(run_text)
                        continue

                    rpr = r_el.find(_w("rPr"))
                    r_style_id = None
                    if rpr is not None:
                        rs_el = rpr.find(_w("rStyle"))
                        if rs_el is not None:
                            r_style_id = rs_el.attrib.get(_w("val"))

                    eff = dict(p_style_props)
                    eff.update(_resolve_style(r_style_id))

                    vanish = eff.get("vanish", False)
                    web_hidden = eff.get("webHidden", False)
                    fg_color_str = eff.get("color")
                    sz_pt = eff.get("sz_pt", 11.0)
                    r_bg_rgb = p_bg_rgb

                    if rpr is not None:
                        v = _ooxml_bool_prop(rpr, _w("vanish"))
                        if v is not None:
                            vanish = v
                        wh = _ooxml_bool_prop(rpr, _w("webHidden"))
                        if wh is not None:
                            web_hidden = wh
                        c_el = rpr.find(_w("color"))
                        if c_el is not None and c_el.attrib.get(_w("val")):
                            fg_color_str = c_el.attrib.get(_w("val"))
                        sz_el = rpr.find(_w("sz"))
                        if sz_el is not None and sz_el.attrib.get(_w("val")):
                            try:
                                sz_pt = float(sz_el.attrib[_w("val")]) / 2.0
                            except ValueError:
                                pass
                        r_shd = rpr.find(_w("shd"))
                        if r_shd is not None:
                            rgb, _ = parse_css_color(r_shd.attrib.get(_w("fill")))
                            if rgb is not None:
                                r_bg_rgb = rgb

                    fg_rgb, _ = parse_css_color(fg_color_str)
                    if fg_rgb is None:
                        fg_rgb = (0, 0, 0)

                    reason: Optional[str] = None
                    details: Dict[str, Any] = {"size_pt": sz_pt}

                    if vanish:
                        reason = "docx_vanish"
                    elif web_hidden:
                        reason = "docx_web_hidden"
                    elif sz_pt < min_font_size:
                        reason = "docx_micro_font"
                    else:
                        cr = contrast_ratio(fg_rgb, r_bg_rgb)
                        if cr < contrast_threshold:
                            reason = "white_text" if (_is_near_white(fg_rgb) and _is_near_white(r_bg_rgb)) else "docx_low_contrast"
                            details["contrast_ratio"] = round(cr, 2)
                            details["color"] = "#{:02x}{:02x}{:02x}".format(*fg_rgb)
                            details["bg_color"] = "#{:02x}{:02x}{:02x}".format(*r_bg_rgb)

                    if reason:
                        stripped_traps.append(
                            _make_trap(
                                reason=reason,
                                text=run_text,
                                location=loc,
                                severity="high",
                                details=details,
                            )
                        )
                    else:
                        p_parts.append(run_text)

                p_joined = "".join(p_parts).strip()
                if p_joined:
                    if collect_clean:
                        clean_paragraphs.append(p_joined)
                    elif _is_suspicious_channel_text(p_joined):
                        stripped_traps.append(
                            _make_trap(
                                reason="docx_aux_channel",
                                text=p_joined[:500],
                                location=loc,
                                severity="high",
                            )
                        )

        # 4. Walk word/document.xml + auxiliary parts (headers, footers, footnotes, endnotes)
        if "word/document.xml" in names:
            _scan_xml_part("word/document.xml", loc_prefix="", collect_clean=True)

        aux_parts = sorted(
            n for n in names
            if re.fullmatch(r"word/(?:header\d+|footer\d+|footnotes|endnotes)\.xml", n)
        )
        for apart in aux_parts:
            try:
                _scan_xml_part(apart, loc_prefix=f"{os.path.basename(apart)}:", collect_clean=False)
            except Exception:
                pass

    return _finalize_report(
        clean_text="\n".join(clean_paragraphs),
        stripped_traps=stripped_traps,
        file_type="docx",
        engine_used="docx-xml",
        source_path=docx_path,
        extra_warnings=extra_warnings,
        stats={"paragraphs_kept": len(clean_paragraphs)},
    )


def sanitize_pptx(
    pptx_path: str,
    contrast_threshold: float = 1.8,
    min_font_size: float = 4.0,
    min_opacity: float = 0.15,
) -> SanitizationReport:
    """
    Layer 3b: Sanitizes PPTX presentations (stdlib zipfile + xml.etree).
    Extracts visible text from active slides only; audits & excludes Speaker Notes,
    Hidden Slides (show="0"), white/low-contrast/micro/off-slide text, comments, and metadata.
    """
    if not os.path.exists(pptx_path):
        return SanitizationReport(
            file_type="pptx", engine_used="none", risk_level="none", source_path=pptx_path
        )

    stripped_traps: List[TrapRecord] = []
    extra_warnings: List[TrapRecord] = []
    clean_slides: List[str] = []

    with zipfile.ZipFile(pptx_path, "r") as zf:
        names = set(zf.namelist())

        # 1. Metadata & embedded media
        stripped_traps.extend(_audit_ooxml_core_props(zf, reason="pptx_metadata"))
        m_traps, m_warns = _audit_ooxml_media(zf, "ppt/media/", "pptx")
        stripped_traps.extend(m_traps)
        extra_warnings.extend(m_warns)

        # 2. Determine slide size & slide order
        slide_cx, slide_cy = 9144000, 6858000
        slide_paths: List[str] = []
        if "ppt/presentation.xml" in names:
            try:
                pres = ET.fromstring(zf.read("ppt/presentation.xml"))
                sld_sz = pres.find(_p("sldSz"))
                if sld_sz is not None:
                    slide_cx = int(sld_sz.attrib.get("cx", slide_cx))
                    slide_cy = int(sld_sz.attrib.get("cy", slide_cy))
                rels_map: Dict[str, str] = {}
                if "ppt/_rels/presentation.xml.rels" in names:
                    rels_root = ET.fromstring(zf.read("ppt/_rels/presentation.xml.rels"))
                    for rel in rels_root:
                        rid = rel.attrib.get("Id")
                        target = rel.attrib.get("Target", "")
                        if rid and target:
                            norm = target.lstrip("/")
                            if not norm.startswith("ppt/"):
                                norm = "ppt/" + norm
                            rels_map[rid] = norm
                sld_id_lst = pres.find(_p("sldIdLst"))
                if sld_id_lst is not None:
                    for sld_id in sld_id_lst.findall(_p("sldId")):
                        rid = sld_id.attrib.get(f"{{{_R_NS}}}id")
                        if rid and rid in rels_map and rels_map[rid] in names:
                            slide_paths.append(rels_map[rid])
            except Exception:
                pass

        if not slide_paths:
            slide_paths = sorted(
                n for n in names if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)
            )

        def _extract_solid_fill(node: Optional[ET.Element]) -> Tuple[Optional[Tuple[int, int, int]], float]:
            if node is None:
                return None, 1.0
            sf = node.find(_a("solidFill"))
            if sf is None:
                return None, 1.0
            srgb = sf.find(_a("srgbClr"))
            if srgb is not None and srgb.attrib.get("val"):
                rgb, _ = parse_css_color(srgb.attrib["val"])
                alpha = 1.0
                a_el = srgb.find(_a("alpha"))
                if a_el is not None and a_el.attrib.get("val"):
                    try:
                        alpha = float(a_el.attrib["val"]) / 100000.0
                    except ValueError:
                        pass
                return rgb, alpha
            return None, 1.0

        # 3. Inspect slides
        for s_idx, spath in enumerate(slide_paths, start=1):
            loc = f"slide {s_idx}"
            root = ET.fromstring(zf.read(spath))
            show_attr = root.attrib.get("show", "1").lower()
            is_hidden_slide = show_attr in ("0", "false")

            if is_hidden_slide:
                all_txt = " ".join(t.text.strip() for t in root.iter(_a("t")) if t.text and t.text.strip())
                stripped_traps.append(
                    _make_trap(
                        reason="pptx_hidden_slide",
                        text=all_txt or f"Hidden slide {s_idx}",
                        location=loc,
                        severity="high",
                    )
                )
                continue

            # Slide background color
            slide_bg: Tuple[int, int, int] = (255, 255, 255)
            c_sld = root.find(_p("cSld"))
            if c_sld is not None:
                bg_el = c_sld.find(_p("bg"))
                if bg_el is not None:
                    bg_pr = bg_el.find(_p("bgPr"))
                    bg_rgb, _ = _extract_solid_fill(bg_pr)
                    if bg_rgb is not None:
                        slide_bg = bg_rgb

            slide_lines: List[str] = []
            # Audit alt-text <p:cNvPr descr/title> on shapes & pictures
            for cnv in root.iter(_p("cNvPr")):
                for attr in ("descr", "title"):
                    aval = (cnv.attrib.get(attr) or "").strip()
                    if aval and _is_suspicious_channel_text(aval):
                        stripped_traps.append(
                            _make_trap(
                                reason="pptx_alt_text",
                                text=aval[:500],
                                location=f"{loc}:cNvPr.{attr}",
                                severity="high",
                            )
                        )

            for sp in root.iter(_p("sp")):
                # Check off-slide coordinates
                sp_pr = sp.find(_p("spPr"))
                shape_bg = slide_bg
                off_slide = False
                if sp_pr is not None:
                    sh_rgb, _ = _extract_solid_fill(sp_pr)
                    if sh_rgb is not None:
                        shape_bg = sh_rgb
                    xfrm = sp_pr.find(_a("xfrm"))
                    if xfrm is not None:
                        off = xfrm.find(_a("off"))
                        ext = xfrm.find(_a("ext"))
                        if off is not None:
                            ox = int(off.attrib.get("x", "0"))
                            oy = int(off.attrib.get("y", "0"))
                            ex = int(ext.attrib.get("cx", "100000")) if ext is not None else 100000
                            ey = int(ext.attrib.get("cy", "100000")) if ext is not None else 100000
                            if (ox + ex) <= 0 or ox >= slide_cx or (oy + ey) <= 0 or oy >= slide_cy or ex <= 0 or ey <= 0:
                                off_slide = True

                tx_body = sp.find(_p("txBody"))
                if tx_body is None:
                    continue

                if off_slide:
                    off_txt = " ".join(t.text.strip() for t in tx_body.iter(_a("t")) if t.text and t.text.strip())
                    if off_txt:
                        stripped_traps.append(
                            _make_trap(
                                reason="pptx_off_slide",
                                text=off_txt,
                                location=loc,
                                severity="high",
                            )
                        )
                    continue

                for ap in tx_body.findall(_a("p")):
                    p_parts: List[str] = []
                    for ar in ap.findall(_a("r")):
                        t_el = ar.find(_a("t"))
                        r_txt = t_el.text if (t_el is not None and t_el.text) else ""
                        if not r_txt:
                            continue
                        if not r_txt.strip():
                            p_parts.append(r_txt)
                            continue
                        rpr = ar.find(_a("rPr"))
                        sz_pt = 18.0
                        fg_rgb = (0, 0, 0)
                        alpha = 1.0
                        if rpr is not None:
                            if rpr.attrib.get("sz"):
                                try:
                                    sz_pt = float(rpr.attrib["sz"]) / 100.0
                                except ValueError:
                                    pass
                            c_rgb, c_alpha = _extract_solid_fill(rpr)
                            if c_rgb is not None:
                                fg_rgb = c_rgb
                            alpha = c_alpha

                        reason: Optional[str] = None
                        if sz_pt < min_font_size:
                            reason = "pptx_micro_font"
                        elif alpha < min_opacity:
                            reason = "pptx_hidden_text"
                        elif contrast_ratio(fg_rgb, shape_bg) < contrast_threshold:
                            reason = "pptx_hidden_text"

                        if reason:
                            stripped_traps.append(
                                _make_trap(
                                    reason=reason,
                                    text=r_txt,
                                    location=loc,
                                    severity="high",
                                    details={"size_pt": sz_pt, "alpha": alpha},
                                )
                            )
                        else:
                            p_parts.append(r_txt)
                    joined = "".join(p_parts).strip()
                    if joined:
                        slide_lines.append(joined)

            if slide_lines:
                clean_slides.append("\n".join(slide_lines))

        # 4. Audit Speaker Notes (NEVER added to clean_text)
        for npath in sorted(n for n in names if re.fullmatch(r"ppt/notesSlides/notesSlide\d+\.xml", n)):
            try:
                n_root = ET.fromstring(zf.read(npath))
                n_texts = [t.text.strip() for t in n_root.iter(_a("t")) if t.text and t.text.strip()]
                # Filter out standalone slide number placeholder digits
                n_texts = [t for t in n_texts if not re.fullmatch(r"\d{1,3}", t)]
                notes_joined = " ".join(n_texts).strip()
                if notes_joined:
                    stripped_traps.append(
                        _make_trap(
                            reason="pptx_speaker_notes",
                            text=notes_joined[:600],
                            location=os.path.basename(npath),
                            severity="high" if _is_suspicious_channel_text(notes_joined) else "medium",
                        )
                    )
            except Exception:
                pass

        # 5. Audit Comments & SlideMasters / SlideLayouts
        for cpath in sorted(n for n in names if re.fullmatch(r"ppt/comments/comment\d+\.xml", n)):
            try:
                c_root = ET.fromstring(zf.read(cpath))
                for cm in c_root.iter(_p("text")):
                    ct = (cm.text or "").strip()
                    if ct:
                        stripped_traps.append(
                            _make_trap(
                                reason="pptx_comment",
                                text=ct[:500],
                                location=os.path.basename(cpath),
                                severity="high" if _is_suspicious_channel_text(ct) else "medium",
                            )
                        )
            except Exception:
                pass

        for ml_path in sorted(
            n for n in names
            if re.fullmatch(r"ppt/(?:slideMasters|slideLayouts)/[^/]+\.xml", n)
        ):
            try:
                ml_root = ET.fromstring(zf.read(ml_path))
                ml_txt = " ".join(t.text.strip() for t in ml_root.iter(_a("t")) if t.text and t.text.strip())
                if ml_txt and _is_suspicious_channel_text(ml_txt):
                    stripped_traps.append(
                        _make_trap(
                            reason="pptx_master_layout",
                            text=ml_txt[:500],
                            location=os.path.basename(ml_path),
                            severity="high",
                        )
                    )
            except Exception:
                pass

    return _finalize_report(
        clean_text="\n\n".join(clean_slides),
        stripped_traps=stripped_traps,
        file_type="pptx",
        engine_used="pptx-xml",
        source_path=pptx_path,
        extra_warnings=extra_warnings,
        stats={"slides_total": len(slide_paths), "slides_visible_with_text": len(clean_slides)},
    )


def _col_letters_to_index(col_ref: str) -> int:
    idx = 0
    for ch in col_ref.upper():
        if "A" <= ch <= "Z":
            idx = idx * 26 + (ord(ch) - ord("A") + 1)
    return idx


def sanitize_xlsx(
    xlsx_path: str,
    contrast_threshold: float = 1.8,
    min_font_size: float = 4.0,
) -> SanitizationReport:
    """
    Layer 3c: Sanitizes XLSX spreadsheets (stdlib zipfile + xml.etree).
    Extracts visible sheets only; audits & excludes hidden/veryHidden sheets,
    hidden rows/cols, white/low-contrast/micro text, cell comments/notes, and metadata.
    """
    if not os.path.exists(xlsx_path):
        return SanitizationReport(
            file_type="xlsx", engine_used="none", risk_level="none", source_path=xlsx_path
        )

    stripped_traps: List[TrapRecord] = []
    clean_sheets: List[str] = []

    with zipfile.ZipFile(xlsx_path, "r") as zf:
        names = set(zf.namelist())

        # 1. Metadata
        stripped_traps.extend(_audit_ooxml_core_props(zf, reason="xlsx_metadata"))

        # 2. Shared strings
        shared_strings: List[str] = []
        if "xl/sharedStrings.xml" in names:
            try:
                ss_root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
                for si in ss_root.findall(_s("si")):
                    shared_strings.append("".join(t.text or "" for t in si.iter(_s("t"))))
            except Exception:
                pass

        # 3. Theme colors (for <color theme="0"/>) & Styles (font, fill, numFmt `;;;`)
        theme_colors: List[Tuple[int, int, int]] = [
            (255, 255, 255),  # 0: lt1 (white)
            (0, 0, 0),        # 1: dk1 (black)
            (231, 230, 230),  # 2: lt2
            (68, 84, 106),    # 3: dk2
            (68, 114, 196),   # 4: accent1
            (237, 125, 49),   # 5: accent2
            (165, 165, 165),  # 6: accent3
            (255, 192, 0),    # 7: accent4
            (91, 155, 213),   # 8: accent5
            (112, 173, 71),   # 9: accent6
        ]
        if "xl/theme/theme1.xml" in names:
            try:
                th_root = ET.fromstring(zf.read("xl/theme/theme1.xml"))
                clr_scheme = th_root.find(f".//{{{_A_NS}}}clrScheme")
                if clr_scheme is not None:
                    slot_names = ["lt1", "dk1", "lt2", "dk2", "accent1", "accent2", "accent3", "accent4", "accent5", "accent6"]
                    for s_i, s_name in enumerate(slot_names):
                        slot = clr_scheme.find(f"{{{_A_NS}}}{s_name}")
                        if slot is not None:
                            srgb = slot.find(f"{{{_A_NS}}}srgbClr")
                            sysc = slot.find(f"{{{_A_NS}}}sysClr")
                            val = None
                            if srgb is not None:
                                val = srgb.attrib.get("val")
                            elif sysc is not None:
                                val = sysc.attrib.get("lastClr")
                            if val:
                                parsed, _ = parse_css_color(val)
                                if parsed is not None:
                                    theme_colors[s_i] = parsed
            except Exception:
                pass

        def _resolve_xlsx_color(col_el: Optional[ET.Element], default_rgb: Optional[Tuple[int, int, int]]) -> Optional[Tuple[int, int, int]]:
            if col_el is None:
                return default_rgb
            if col_el.attrib.get("rgb"):
                parsed, _ = parse_css_color(col_el.attrib["rgb"])
                if parsed is not None:
                    return parsed
            if col_el.attrib.get("theme") is not None:
                try:
                    t_idx = int(col_el.attrib["theme"])
                    if 0 <= t_idx < len(theme_colors):
                        base = theme_colors[t_idx]
                        tint_str = col_el.attrib.get("tint")
                        if tint_str is not None:
                            tint = float(tint_str)
                            if tint > 0:
                                return tuple(int(round(c + (255 - c) * tint)) for c in base)  # type: ignore[return-value]
                            elif tint < 0:
                                return tuple(int(round(c * (1.0 + tint))) for c in base)  # type: ignore[return-value]
                        return base
                except ValueError:
                    pass
            if col_el.attrib.get("indexed") is not None:
                try:
                    ix = int(col_el.attrib["indexed"])
                    if ix in (9, 1):
                        return (255, 255, 255)
                    if ix in (8, 0, 64):
                        return (0, 0, 0)
                except ValueError:
                    pass
            return default_rgb

        num_fmts: Dict[int, str] = {}
        fonts: List[Dict[str, Any]] = []
        fills: List[Optional[Tuple[int, int, int]]] = []
        cell_xfs: List[Tuple[int, int, int]] = []  # (fontId, fillId, numFmtId)
        if "xl/styles.xml" in names:
            try:
                st_root = ET.fromstring(zf.read("xl/styles.xml"))
                nfmts_el = st_root.find(_s("numFmts"))
                if nfmts_el is not None:
                    for nf in nfmts_el.findall(_s("numFmt")):
                        if nf.attrib.get("numFmtId", "").isdigit():
                            num_fmts[int(nf.attrib["numFmtId"])] = nf.attrib.get("formatCode", "")

                fonts_el = st_root.find(_s("fonts"))
                if fonts_el is not None:
                    for f_el in fonts_el.findall(_s("font")):
                        sz_el = f_el.find(_s("sz"))
                        sz = float(sz_el.attrib.get("val", "11")) if sz_el is not None else 11.0
                        col_el = f_el.find(_s("color"))
                        rgb = _resolve_xlsx_color(col_el, (0, 0, 0)) or (0, 0, 0)
                        fonts.append({"sz": sz, "rgb": rgb})

                fills_el = st_root.find(_s("fills"))
                if fills_el is not None:
                    for fl_el in fills_el.findall(_s("fill")):
                        pf = fl_el.find(_s("patternFill"))
                        fill_rgb = None
                        if pf is not None and pf.attrib.get("patternType", "none") != "none":
                            fg_c = pf.find(_s("fgColor"))
                            fill_rgb = _resolve_xlsx_color(fg_c, None)
                        fills.append(fill_rgb)

                xfs_el = st_root.find(_s("cellXfs"))
                if xfs_el is not None:
                    for xf in xfs_el.findall(_s("xf")):
                        cell_xfs.append(
                            (
                                int(xf.attrib.get("fontId", "0")),
                                int(xf.attrib.get("fillId", "0")),
                                int(xf.attrib.get("numFmtId", "0")),
                            )
                        )
            except Exception:
                pass

        # 4. Workbook sheets & relationships
        rels_map: Dict[str, str] = {}
        if "xl/_rels/workbook.xml.rels" in names:
            try:
                rels_root = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
                for rel in rels_root:
                    rid = rel.attrib.get("Id")
                    target = rel.attrib.get("Target", "").lstrip("/")
                    if rid and target:
                        if not target.startswith("xl/"):
                            target = "xl/" + target
                        rels_map[rid] = target
            except Exception:
                pass

        sheets_meta: List[Tuple[str, str, str]] = []  # (name, state, path)
        if "xl/workbook.xml" in names:
            try:
                wb_root = ET.fromstring(zf.read("xl/workbook.xml"))
                sheets_el = wb_root.find(_s("sheets"))
                if sheets_el is not None:
                    for sh in sheets_el.findall(_s("sheet")):
                        sh_name = sh.attrib.get("name", "Sheet")
                        sh_state = sh.attrib.get("state", "visible").lower()
                        rid = sh.attrib.get(f"{{{_R_NS}}}id", "")
                        sh_path = rels_map.get(rid, "")
                        if sh_path in names:
                            sheets_meta.append((sh_name, sh_state, sh_path))
                # Audit <definedNames>
                def_names = wb_root.find(_s("definedNames"))
                if def_names is not None:
                    for dn in def_names.findall(_s("definedName")):
                        dn_text = f"{dn.attrib.get('name', '')}: {dn.text or ''}".strip()
                        if dn_text and _is_suspicious_channel_text(dn_text):
                            stripped_traps.append(
                                _make_trap(
                                    reason="xlsx_formula_or_name",
                                    text=dn_text[:500],
                                    location="workbook.definedName",
                                    severity="high",
                                )
                            )
            except Exception:
                pass

        def _cell_value(c_el: ET.Element) -> str:
            ctype = c_el.attrib.get("t", "")
            if ctype == "s":
                v_el = c_el.find(_s("v"))
                if v_el is not None and v_el.text and v_el.text.isdigit():
                    idx = int(v_el.text)
                    if 0 <= idx < len(shared_strings):
                        return shared_strings[idx]
            elif ctype == "inlineStr":
                return "".join(t.text or "" for t in c_el.iter(_s("t")))
            else:
                v_el = c_el.find(_s("v"))
                if v_el is not None and v_el.text:
                    return v_el.text
            return ""

        for sh_name, sh_state, sh_path in sheets_meta:
            sh_root = ET.fromstring(zf.read(sh_path))
            is_hidden_sheet = sh_state in ("hidden", "veryhidden")

            if is_hidden_sheet:
                hidden_vals = []
                for c_el in sh_root.iter(_s("c")):
                    val = _cell_value(c_el).strip()
                    if val:
                        hidden_vals.append(val)
                stripped_traps.append(
                    _make_trap(
                        reason="xlsx_hidden_sheet",
                        text=" | ".join(hidden_vals)[:600] if hidden_vals else f"Hidden sheet '{sh_name}'",
                        location=f"sheet '{sh_name}' ({sh_state})",
                        severity="high",
                        details={"sheet": sh_name, "state": sh_state},
                    )
                )
                continue

            # Hidden columns
            hidden_cols: set[int] = set()
            cols_el = sh_root.find(_s("cols"))
            if cols_el is not None:
                for col in cols_el.findall(_s("col")):
                    is_h = col.attrib.get("hidden") in ("1", "true")
                    w_zero = col.attrib.get("width") in ("0", "0.0")
                    if is_h or w_zero:
                        cmin = int(col.attrib.get("min", "1"))
                        cmax = int(col.attrib.get("max", str(cmin)))
                        for ci in range(cmin, cmax + 1):
                            hidden_cols.add(ci)

            sheet_rows_out: List[str] = []
            sheet_data = sh_root.find(_s("sheetData"))
            if sheet_data is not None:
                for row_el in sheet_data.findall(_s("row")):
                    row_hidden = row_el.attrib.get("hidden") in ("1", "true") or row_el.attrib.get("ht") in ("0", "0.0")
                    row_vals: List[str] = []

                    for c_el in row_el.findall(_s("c")):
                        cell_ref = c_el.attrib.get("r", "")
                        f_el = c_el.find(_s("f"))
                        if f_el is not None and f_el.text and _is_suspicious_channel_text(f_el.text):
                            stripped_traps.append(
                                _make_trap(
                                    reason="xlsx_formula_or_name",
                                    text=f_el.text.strip()[:500],
                                    location=f"sheet '{sh_name}'!{cell_ref}:formula",
                                    severity="high",
                                )
                            )
                        val = _cell_value(c_el).strip()
                        if not val:
                            continue
                        col_letters = "".join(ch for ch in cell_ref if ch.isalpha())
                        col_idx = _col_letters_to_index(col_letters) if col_letters else -1
                        loc = f"sheet '{sh_name}'!{cell_ref}"

                        reason: Optional[str] = None
                        if row_hidden or (col_idx in hidden_cols):
                            reason = "xlsx_hidden_row_col"
                        else:
                            s_attr = c_el.attrib.get("s")
                            if s_attr and s_attr.isdigit():
                                xf_idx = int(s_attr)
                                if 0 <= xf_idx < len(cell_xfs):
                                    f_id, fl_id, nfmt_id = cell_xfs[xf_idx]
                                    fmt_code = num_fmts.get(nfmt_id, "")
                                    if fmt_code and re.fullmatch(r"\s*(?:;+\s*)+", fmt_code):
                                        reason = "xlsx_hidden_format"
                                    else:
                                        font = fonts[f_id] if 0 <= f_id < len(fonts) else {"sz": 11.0, "rgb": (0, 0, 0)}
                                        bg_rgb = fills[fl_id] if (0 <= fl_id < len(fills) and fills[fl_id] is not None) else (255, 255, 255)
                                        if font["sz"] < min_font_size:
                                            reason = "xlsx_micro_font"
                                        elif contrast_ratio(font["rgb"], bg_rgb) < contrast_threshold:
                                            reason = "xlsx_hidden_text"

                        if reason:
                            stripped_traps.append(
                                _make_trap(
                                    reason=reason,
                                    text=val[:500],
                                    location=loc,
                                    severity="high",
                                )
                            )
                        else:
                            row_vals.append(val)

                    if row_vals:
                        sheet_rows_out.append("\t".join(row_vals))

            if sheet_rows_out:
                clean_sheets.append(f"[Sheet: {sh_name}]\n" + "\n".join(sheet_rows_out))

        # 5. Audit Cell Comments & Threaded Comments (NEVER added to clean_text)
        for cpath in sorted(n for n in names if re.fullmatch(r"xl/comments\d*\.xml", n)):
            try:
                c_root = ET.fromstring(zf.read(cpath))
                for cm in c_root.iter(_s("comment")):
                    ref = cm.attrib.get("ref", "")
                    ct = "".join(t.text or "" for t in cm.iter(_s("t"))).strip()
                    if ct:
                        stripped_traps.append(
                            _make_trap(
                                reason="xlsx_comment",
                                text=ct[:500],
                                location=f"{os.path.basename(cpath)}:{ref}",
                                severity="high" if _is_suspicious_channel_text(ct) else "medium",
                            )
                        )
            except Exception:
                pass

        for tpath in sorted(n for n in names if n.startswith("xl/threadedComments/") and n.endswith(".xml")):
            try:
                t_root = ET.fromstring(zf.read(tpath))
                for el in t_root.iter():
                    if el.tag.endswith("}text") and el.text and el.text.strip():
                        ct = el.text.strip()
                        stripped_traps.append(
                            _make_trap(
                                reason="xlsx_comment",
                                text=ct[:500],
                                location=os.path.basename(tpath),
                                severity="high" if _is_suspicious_channel_text(ct) else "medium",
                            )
                        )
            except Exception:
                pass

    return _finalize_report(
        clean_text="\n\n".join(clean_sheets),
        stripped_traps=stripped_traps,
        file_type="xlsx",
        engine_used="xlsx-xml",
        source_path=xlsx_path,
        stats={"sheets_total": len(sheets_meta), "visible_sheets": len(clean_sheets)},
    )


class _SanitizingHTMLParser(HTMLParser):
    _SKIP_TAGS = {"style", "script", "template", "noscript"}
    _VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
    _BLOCK_TAGS = {"p", "div", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "br", "section", "article", "header", "footer"}

    def __init__(
        self,
        contrast_threshold: float = 1.8,
        min_font_size: float = 4.0,
        min_opacity: float = 0.15,
        css_rules: Optional[Dict[str, Dict[str, str]]] = None,
    ):
        super().__init__(convert_charrefs=True)
        self.contrast_threshold = contrast_threshold
        self.min_font_size = min_font_size
        self.min_opacity = min_opacity
        self.css_rules = css_rules or {}
        self.clean_chunks: List[str] = []
        self.traps: List[TrapRecord] = []
        # stack entries: (tag, hidden_reason_or_None, skip_tag_bool, bg_rgb)
        self._stack: List[Tuple[str, Optional[str], bool, Tuple[int, int, int]]] = []
        self._comment_idx = 0

    def _current_hidden(self) -> Optional[str]:
        for _, reason, _, _ in reversed(self._stack):
            if reason is not None:
                return reason
        return None

    def _current_skip(self) -> bool:
        return any(sk for _, _, sk, _ in self._stack)

    def _current_bg(self) -> Tuple[int, int, int]:
        return self._stack[-1][3] if self._stack else (255, 255, 255)

    def _check_hidden_attrs(
        self, tag: str, attr_dict: Dict[str, Optional[str]], parent_bg: Tuple[int, int, int]
    ) -> Tuple[Optional[str], Tuple[int, int, int]]:
        bg_rgb = parent_bg
        if "hidden" in attr_dict:
            return "html_hidden_element", bg_rgb

        style = _resolve_css_for_element(tag, attr_dict, self.css_rules)
        bg_str = style.get("background-color") or style.get("background")
        if bg_str:
            rgb, a = parse_css_color(bg_str.split()[0])
            if rgb is not None and (a is None or a > 0.5):
                bg_rgb = rgb

        if style.get("display", "").lower().startswith("none"):
            return "html_hidden_element", bg_rgb
        if style.get("visibility", "").lower().startswith("hidden"):
            return "html_hidden_element", bg_rgb

        transform = style.get("transform", "").lower()
        if re.search(r"scale[xy]?\(\s*0(?:\.0+)?\s*(?:,|\))", transform):
            return "html_hidden_element", bg_rgb

        clip_path = style.get("clip-path", "").lower().replace(" ", "")
        if "inset(100%" in clip_path or "circle(0" in clip_path or "polygon(0" in clip_path:
            return "html_hidden_element", bg_rgb

        flt = style.get("filter", "").lower().replace(" ", "")
        if "opacity(0)" in flt or "opacity(0%)" in flt:
            return "html_hidden_element", bg_rgb

        w_fill = style.get("-webkit-text-fill-color", "").lower().strip()
        if w_fill == "transparent":
            return "html_hidden_element", bg_rgb

        if style.get("overflow", "").lower().startswith("hidden"):
            for dim_k in ("height", "max-height", "width", "max-width"):
                dim_v = style.get(dim_k, "")
                if re.fullmatch(r"\s*0(?:px|pt|em|rem|%)?\s*", dim_v or ""):
                    return "html_hidden_element", bg_rgb

        op_str = style.get("opacity")
        if op_str is not None:
            try:
                if float(op_str) < self.min_opacity:
                    return "html_hidden_element", bg_rgb
            except ValueError:
                pass

        fsize = _parse_css_font_size_pt(style.get("font-size"))
        if fsize is not None and fsize < self.min_font_size:
            return "html_hidden_element", bg_rgb

        # Off-screen CSS tricks
        for prop in ("left", "top", "text-indent", "margin-left"):
            v = style.get(prop, "")
            m = re.match(r"^\s*-(\d+(?:\.\d+)?)", v)
            if m and float(m.group(1)) >= 500:
                return "html_hidden_element", bg_rgb
        if "rect(0" in style.get("clip", "").replace(" ", ""):
            return "html_hidden_element", bg_rgb

        color_str = style.get("color")
        if color_str:
            fg_rgb, fg_a = parse_css_color(color_str)
            if fg_a is not None and fg_a < self.min_opacity:
                return "html_hidden_element", bg_rgb
            if fg_rgb is not None and contrast_ratio(fg_rgb, bg_rgb) < self.contrast_threshold:
                return "html_hidden_element", bg_rgb

        return None, bg_rgb

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        tl = tag.lower()
        attr_dict = {k.lower(): v for k, v in attrs}

        # Audit suspicious aria-label / title / alt attributes
        for attr_name in ("aria-label", "title", "alt"):
            aval = (attr_dict.get(attr_name) or "").strip()
            if aval and _is_suspicious_channel_text(aval):
                self.traps.append(
                    _make_trap(
                        reason="html_suspicious_attr",
                        text=aval[:500],
                        location=f"<{tl} {attr_name}>",
                        severity="high",
                        details={"tag": tl, "attribute": attr_name},
                    )
                )

        if tl == "meta":
            mcontent = (attr_dict.get("content") or "").strip()
            if mcontent and _is_suspicious_channel_text(mcontent):
                self.traps.append(
                    _make_trap(
                        reason="html_suspicious_attr",
                        text=mcontent[:500],
                        location="<meta content>",
                        severity="high",
                    )
                )
        elif tl == "input" and (attr_dict.get("type") or "").lower() == "hidden":
            hval = (attr_dict.get("value") or "").strip()
            if hval and _is_suspicious_channel_text(hval):
                self.traps.append(
                    _make_trap(
                        reason="html_hidden_element",
                        text=hval[:500],
                        location="<input type='hidden'>",
                        severity="high",
                    )
                )

        if tl in self._BLOCK_TAGS:
            self.clean_chunks.append("\n")

        if tl in self._VOID_TAGS:
            return

        hidden_reason, bg_rgb = self._check_hidden_attrs(tl, attr_dict, self._current_bg())
        is_skip = tl in self._SKIP_TAGS
        self._stack.append((tl, hidden_reason, is_skip, bg_rgb))

    def handle_endtag(self, tag: str) -> None:
        tl = tag.lower()
        if tl in self._BLOCK_TAGS:
            self.clean_chunks.append("\n")
        for i in range(len(self._stack) - 1, -1, -1):
            if self._stack[i][0] == tl:
                del self._stack[i:]
                break

    def handle_data(self, data: str) -> None:
        if not data:
            return
        if self._current_skip():
            # Record suspicious directives in <template>/<noscript>
            top_tag = self._stack[-1][0] if self._stack else ""
            if top_tag in ("template", "noscript") and data.strip() and _is_suspicious_channel_text(data):
                self.traps.append(
                    _make_trap(
                        reason="html_hidden_element",
                        text=data.strip()[:500],
                        location=f"<{top_tag}>",
                        severity="high",
                    )
                )
            return

        hidden_reason = self._current_hidden()
        if hidden_reason is not None:
            if data.strip():
                top_tag = self._stack[-1][0] if self._stack else "html"
                self.traps.append(
                    _make_trap(
                        reason=hidden_reason,
                        text=data.strip()[:500],
                        location=f"<{top_tag}>",
                        severity="high",
                    )
                )
            return

        self.clean_chunks.append(data)

    def handle_comment(self, data: str) -> None:
        self._comment_idx += 1
        txt = (data or "").strip()
        if txt:
            self.traps.append(
                _make_trap(
                    reason="html_comment",
                    text=txt[:500],
                    location=f"html:comment#{self._comment_idx}",
                    severity="high" if _is_suspicious_channel_text(txt) else "medium",
                )
            )


def sanitize_markup(
    content_or_path: str,
    markup_type: str = "auto",
    is_text: bool = False,
) -> SanitizationReport:
    """
    Layer 3d: Sanitizes HTML or Markdown files (or inline strings when is_text=True).
    """
    source_path = None if is_text else content_or_path
    if is_text:
        raw = content_or_path
    else:
        with open(content_or_path, "r", encoding="utf-8", errors="ignore") as f:
            raw = f.read()

    if markup_type == "auto":
        ext = os.path.splitext(content_or_path)[1].lower() if not is_text else ""
        markup_type = "html" if ext in (".html", ".htm", ".xhtml") else "markdown"

    if markup_type == "html":
        css_rules: Dict[str, Dict[str, str]] = {}
        for st_m in re.finditer(r"<style\b[^>]*>(.*?)</style>", raw, re.IGNORECASE | re.DOTALL):
            css_rules.update(_parse_css_rules(st_m.group(1)))
        parser = _SanitizingHTMLParser(css_rules=css_rules)
        parser.feed(raw)
        parser.close()
        clean = re.sub(r"\n{3,}", "\n\n", "".join(parser.clean_chunks))
        clean = "\n".join(line.strip() for line in clean.splitlines())
        return _finalize_report(
            clean_text=clean,
            stripped_traps=parser.traps,
            file_type="html",
            engine_used="html-parser",
            source_path=source_path,
        )

    # Markdown sanitization
    stripped_traps: List[TrapRecord] = []
    text = raw

    # 1. Strip <!-- HTML comments -->
    def _strip_md_html_comment(m: re.Match[str]) -> str:
        txt = m.group(1).strip()
        if txt:
            stripped_traps.append(
                _make_trap(
                    reason="markdown_comment",
                    text=txt[:500],
                    location="markdown:html_comment",
                    severity="high" if _is_suspicious_channel_text(txt) else "medium",
                )
            )
        return ""

    text = re.sub(r"<!--(.*?)-->", _strip_md_html_comment, text, flags=re.DOTALL)

    # 2. Strip reference-style comments: [//]: # (hidden text) or [//]: # "hidden"
    def _strip_ref_comment(m: re.Match[str]) -> str:
        txt = (m.group(1) or "").strip()
        if txt:
            stripped_traps.append(
                _make_trap(
                    reason="markdown_comment",
                    text=txt[:500],
                    location="markdown:ref_comment",
                    severity="high" if _is_suspicious_channel_text(txt) else "medium",
                )
            )
        return ""

    text = re.sub(
        r"^[ \t]*\[//\]:[ \t]*#[ \t]*(?:\(([^)]*)\)|\"([^\"]*)\"|'([^']*)')[ \t]*$",
        lambda m: _strip_ref_comment(
            re.match(r"(.*)", m.group(1) or m.group(2) or m.group(3) or "", re.DOTALL)  # type: ignore[arg-type]
        ),
        text,
        flags=re.MULTILINE,
    )

    # 3. Strip inline hidden HTML elements embedded in Markdown (e.g. <span style="display:none">...</span>)
    hidden_html_pat = re.compile(
        r"<(span|div|p|font)\b([^>]*\b(?:hidden|style\s*=\s*[\"'][^\"']*(?:display\s*:\s*none|visibility\s*:\s*hidden|opacity\s*:\s*0(?:\.0+)?\b|font-size\s*:\s*0|color\s*:\s*(?:#fff(?:fff)?|white|transparent))[^\"']*[\"'])[^>]*)>(.*?)</\1>",
        re.IGNORECASE | re.DOTALL,
    )

    def _strip_inline_html(m: re.Match[str]) -> str:
        inner = re.sub(r"<[^>]+>", "", m.group(3)).strip()
        if inner:
            stripped_traps.append(
                _make_trap(
                    reason="html_hidden_element",
                    text=inner[:500],
                    location=f"markdown:<{m.group(1)}>",
                    severity="high",
                )
            )
        return ""

    text = hidden_html_pat.sub(_strip_inline_html, text)

    # 4. Strip unused or suspicious Markdown reference-link definitions: [id]: url "title"
    def _strip_ref_link(m: re.Match[str]) -> str:
        label = (m.group(1) or "").strip()
        target_and_title = (m.group(2) or "").strip()
        # Check if label is referenced anywhere else in document body
        is_referenced = bool(
            label
            and re.search(rf"\[[^\]]*\]\[{re.escape(label)}\]|\[{re.escape(label)}\]\[\]", text[:m.start()] + text[m.end():], re.IGNORECASE)
        )
        if not is_referenced or _is_suspicious_channel_text(target_and_title):
            stripped_traps.append(
                _make_trap(
                    reason="markdown_hidden_ref",
                    text=target_and_title[:500] or label,
                    location=f"markdown:ref[{label}]",
                    severity="high" if _is_suspicious_channel_text(target_and_title) else "medium",
                )
            )
            return ""
        return m.group(0)

    text = re.sub(
        r"^[ \t]*\[([^\]]+)\]:[ \t]+(.+?)[ \t]*$",
        _strip_ref_link,
        text,
        flags=re.MULTILINE,
    )

    # 5. Audit suspicious Markdown image alt / title texts ![alt](url "title")
    for img_m in re.finditer(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+[\"']([^\"']*)[\"'])?\)", text):
        alt_txt = (img_m.group(1) or "").strip()
        title_txt = (img_m.group(3) or "").strip()
        for kind, val in (("alt", alt_txt), ("title", title_txt)):
            if val and _is_suspicious_channel_text(val):
                stripped_traps.append(
                    _make_trap(
                        reason="markdown_suspicious_image_attr",
                        text=val[:500],
                        location=f"markdown:img.{kind}",
                        severity="high",
                    )
                )

    text = re.sub(r"\n{3,}", "\n\n", text)

    return _finalize_report(
        clean_text=text,
        stripped_traps=stripped_traps,
        file_type="markdown",
        engine_used="markdown",
        source_path=source_path,
    )


def sanitize_code(
    code_or_path: str,
    is_text: bool = False,
) -> SanitizationReport:
    """
    Layer 3e: Sanitizes starter source code (*.cpp, *.java, *.py, *.sql, *.js, etc.).
    Strips Trojan Source / invisible Unicode without corrupting valid code, and scans
    comments for AI prompt-injection traps.
    """
    source_path = None if is_text else code_or_path
    if is_text:
        raw = code_or_path
    else:
        with open(code_or_path, "r", encoding="utf-8", errors="ignore") as f:
            raw = f.read()

    # Step 1: Unicode stego & Trojan Source sanitization
    cleaned, uni_traps, uni_stats = sanitize_text(raw, location="source_code")
    stripped_traps: List[TrapRecord] = list(uni_traps)
    extra_warnings: List[TrapRecord] = []

    # Step 1.5: Strip malicious Python triple-quoted docstrings ("""...""" or '''...''')
    is_python_hint = (
        (source_path and source_path.lower().endswith(".py"))
        or bool(re.search(r"^\s*(?:def|class)\s+\w+", cleaned, re.MULTILINE))
    )

    def _is_malicious_code_comment(comment_body: str) -> bool:
        if not comment_body.strip():
            return False
        if detect_semantic_traps(comment_body, location="code_comment"):
            return True
        if _is_suspicious_channel_text(comment_body):
            return True
        if re.search(
            r"\b(?:note\s+for\s+ai|for\s+ai|untuk\s+ai|ignore\s+previous|abaikan\s+instruksi|"
            r"chatgpt|claude|gemini|llm|system\s+prompt|jangan\s+beritahu)\b",
            comment_body,
            re.IGNORECASE,
        ):
            return True
        return False

    if is_python_hint:
        def _strip_py_docstring(m: re.Match[str]) -> str:
            body = m.group(2)
            if _is_malicious_code_comment(body):
                line_no = cleaned[: m.start()].count("\n") + 1
                stripped_traps.append(
                    _make_trap(
                        reason="code_prompt_injection",
                        text=body.strip()[:500],
                        location=f"docstring:line {line_no}",
                        severity="high",
                    )
                )
                extra_warnings.extend(
                    detect_semantic_traps(body, location=f"code:line {line_no}")
                )
                return ""
            return m.group(0)

        cleaned = re.sub(
            r"(\"\"\"|''')(.*?)(\1)",
            _strip_py_docstring,
            cleaned,
            flags=re.DOTALL,
        )

    # Step 2: Inspect single-line & multi-line comments for AI prompt-injection traps
    lines = cleaned.splitlines()
    out_lines: List[str] = []
    in_block_comment = False

    block_buf: List[Tuple[int, str]] = []
    for lineno, line in enumerate(lines, start=1):
        stripped_l = line.strip()

        if in_block_comment:
            block_buf.append((lineno, line))
            if "*/" in line:
                in_block_comment = False
                full_block = "\n".join(l for _, l in block_buf)
                body = re.sub(r"/\*|\*/", "", full_block)
                if _is_malicious_code_comment(body):
                    stripped_traps.append(
                        _make_trap(
                            reason="code_prompt_injection",
                            text=body.strip()[:500],
                            location=f"line {block_buf[0][0]}-{lineno}",
                            severity="high",
                        )
                    )
                    extra_warnings.extend(
                        detect_semantic_traps(body, location=f"code:line {block_buf[0][0]}")
                    )
                else:
                    out_lines.extend(l for _, l in block_buf)
                block_buf = []
            continue

        # Start of /* ... */ block comment
        if "/*" in stripped_l:
            if "*/" in stripped_l[stripped_l.index("/*") + 2:]:
                m = re.search(r"/\*(.*?)\*/", line)
                if m and _is_malicious_code_comment(m.group(1)):
                    stripped_traps.append(
                        _make_trap(
                            reason="code_prompt_injection",
                            text=m.group(1).strip()[:500],
                            location=f"line {lineno}",
                            severity="high",
                        )
                    )
                    extra_warnings.extend(
                        detect_semantic_traps(m.group(1), location=f"code:line {lineno}")
                    )
                    cleaned_line = (line[:m.start()] + line[m.end():]).rstrip()
                    if cleaned_line.strip():
                        out_lines.append(cleaned_line)
                    continue
            else:
                in_block_comment = True
                block_buf = [(lineno, line)]
                continue

        # Single-line comments: //, #, --
        m_single = re.search(r"(//|#|--)(.*)$", line)
        if m_single:
            prefix = line[: m_single.start()]
            # Avoid matching inside string literals (rough quote parity check)
            if prefix.count('"') % 2 == 0 and prefix.count("'") % 2 == 0:
                # Don't treat C/C++ #include/#define as comments
                if m_single.group(1) == "#" and re.match(
                    r"^\s*#\s*(?:include|define|ifdef|ifndef|endif|pragma|if|else|elif|undef)\b",
                    line,
                ):
                    out_lines.append(line)
                    continue
                comment_body = m_single.group(2).strip()
                if _is_malicious_code_comment(comment_body):
                    stripped_traps.append(
                        _make_trap(
                            reason="code_prompt_injection",
                            text=comment_body[:500],
                            location=f"line {lineno}",
                            severity="high",
                        )
                    )
                    extra_warnings.extend(
                        detect_semantic_traps(comment_body, location=f"code:line {lineno}")
                    )
                    if prefix.strip():
                        out_lines.append(prefix.rstrip())
                    continue

        out_lines.append(line)

    if block_buf:
        out_lines.extend(l for _, l in block_buf)

    return _finalize_report(
        clean_text="\n".join(out_lines),
        stripped_traps=stripped_traps,
        file_type="code",
        engine_used="code-scanner",
        source_path=source_path,
        extra_warnings=extra_warnings,
        stats=uni_stats,
        run_unicode_on_clean=False,
    )


def sanitize_ipynb(ipynb_path: str) -> SanitizationReport:
    """
    Layer 3f: Sanitizes Jupyter Notebooks (.ipynb).
    Sanitizes Markdown and code cells, audits notebook/cell metadata and hidden raw cells.
    """
    with open(ipynb_path, "r", encoding="utf-8", errors="ignore") as f:
        nb = json.load(f)

    stripped_traps: List[TrapRecord] = []
    extra_warnings: List[TrapRecord] = []
    clean_cells: List[str] = []

    def _audit_meta_dict(meta: Any, loc: str) -> None:
        if not isinstance(meta, dict):
            return
        for k, v in meta.items():
            if isinstance(v, str) and v.strip():
                cv, ut, _ = sanitize_text(v, location=f"{loc}:{k}")
                stripped_traps.extend(ut)
                if _is_suspicious_channel_text(cv):
                    stripped_traps.append(
                        _make_trap(
                            reason="ipynb_hidden_metadata",
                            text=cv[:500],
                            location=f"{loc}:{k}",
                            severity="high",
                        )
                    )
            elif isinstance(v, dict):
                _audit_meta_dict(v, f"{loc}:{k}")

    _audit_meta_dict(nb.get("metadata"), "notebook.metadata")

    for idx, cell in enumerate(nb.get("cells", []), start=1):
        ctype = cell.get("cell_type", "")
        cmeta = cell.get("metadata") or {}
        _audit_meta_dict(cmeta, f"cell#{idx}.metadata")

        src = cell.get("source", "")
        if isinstance(src, list):
            src = "".join(src)

        if ctype == "raw":
            is_hidden = bool(cmeta.get("collapsed") or cmeta.get("hidden") or cmeta.get("jupyter", {}).get("source_hidden"))
            if is_hidden or _is_suspicious_channel_text(src):
                stripped_traps.append(
                    _make_trap(
                        reason="ipynb_raw_cell",
                        text=src.strip()[:500],
                        location=f"cell#{idx} (raw)",
                        severity="high" if _is_suspicious_channel_text(src) else "medium",
                    )
                )
            elif src.strip():
                clean_cells.append(src.strip())
        elif ctype == "markdown":
            rep = sanitize_markup(src, markup_type="markdown", is_text=True)
            for t in rep.stripped_traps:
                t["location"] = f"cell#{idx}:{t.get('location', '')}"
                stripped_traps.append(t)
            extra_warnings.extend(rep.semantic_warnings)
            if rep.clean_text:
                clean_cells.append(rep.clean_text)
        elif ctype == "code":
            rep = sanitize_code(src, is_text=True)
            for t in rep.stripped_traps:
                t["location"] = f"cell#{idx}:{t.get('location', '')}"
                stripped_traps.append(t)
            extra_warnings.extend(rep.semantic_warnings)
            if rep.clean_text:
                clean_cells.append(rep.clean_text)

    return _finalize_report(
        clean_text="\n\n".join(clean_cells),
        stripped_traps=stripped_traps,
        file_type="ipynb",
        engine_used="ipynb",
        source_path=ipynb_path,
        extra_warnings=extra_warnings,
        stats={"cells_total": len(nb.get("cells", []))},
    )


# ---------------------------------------------------------------------------
# Tier 2 Parsers: RTF, OpenDocument (ODT/ODP/ODS), ZIP & Agent-Rule Audit
# ---------------------------------------------------------------------------

def _is_suspicious_or_semantic(text: str) -> bool:
    """Return True if auxiliary channel text looks suspicious, semantic-trapped, or has directives."""
    if not text or not text.strip():
        return False
    if _is_suspicious_channel_text(text):
        return True
    if detect_semantic_traps(text):
        return True
    if extract_forbidden_identifiers(text):
        return True
    return False


def _audit_archive_images(
    zf: "zipfile.ZipFile",
    prefix: str,
    location_prefix: str,
    stripped_traps: List[TrapRecord],
) -> None:
    """Inspect image metadata chunks inside an office/ODF ZIP archive without disk writes."""
    img_exts = (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif", ".svg")
    for name in zf.namelist():
        low = name.lower()
        if prefix and not low.startswith(prefix.lower()):
            continue
        if not low.endswith(img_exts):
            continue
        try:
            raw_bytes = zf.read(name)
        except Exception:
            continue
        if len(raw_bytes) > 15_000_000:
            continue
        if low.endswith(".svg"):
            try:
                svg_txt = raw_bytes.decode("utf-8", errors="ignore")
                if _is_suspicious_or_semantic(svg_txt):
                    stripped_traps.append(
                        _make_trap(
                            f"{location_prefix}_media_metadata",
                            svg_txt.strip()[:200],
                            f"{location_prefix}:{name}",
                            "high",
                        )
                    )
            except Exception:
                pass
            continue
        # Inspect PNG text chunks & Pillow info/EXIF/COM
        if PILImage is not None:
            import io
            try:
                with PILImage.open(io.BytesIO(raw_bytes)) as im:
                    for k, v in (im.info or {}).items():
                        if isinstance(v, (str, bytes)):
                            val = v.decode("utf-8", errors="ignore") if isinstance(v, bytes) else v
                            if _is_suspicious_or_semantic(val):
                                stripped_traps.append(
                                    _make_trap(
                                        f"{location_prefix}_media_metadata",
                                        f"[{k}] {val.strip()[:200]}",
                                        f"{location_prefix}:{name}",
                                        "high",
                                    )
                                )
                    try:
                        exif = im.getexif()
                        for tag_id, val in (exif.items() if exif else ()):
                            sval = str(val)
                            if _is_suspicious_or_semantic(sval):
                                stripped_traps.append(
                                    _make_trap(
                                        f"{location_prefix}_media_metadata",
                                        f"[EXIF:{tag_id}] {sval[:200]}",
                                        f"{location_prefix}:{name}",
                                        "high",
                                    )
                                )
                    except Exception:
                        pass
            except Exception:
                pass


_RTF_SKIP_DESTS = {
    "fonttbl", "colortbl", "stylesheet", "pict", "object", "objdata",
    "blipuid", "listtable", "listoverridetable", "revtbl", "rsidtbl",
    "latentstyles", "datastore", "themedata", "colorschememapping",
    "pgdsctbl", "panose", "xmlnstbl", "mmathPr", "generator", "shppict",
    "nonshppict", "bkmkstart", "bkmkend", "xe", "tc",
}
_RTF_INFO_DESTS = {
    "info", "title", "subject", "author", "keywords", "doccomm",
    "company", "category", "comment", "operator", "manager",
}
_RTF_ANNOT_DESTS = {"annotation", "atnauthor", "atnid", "atnref", "atntime", "atnicn"}
_RTF_HEADER_DESTS = {"header", "headerl", "headerr", "headerf", "footer", "footerl", "footerr", "footerf"}


def _parse_rtf_colortbl(rtf_raw: str) -> List[Optional[Tuple[int, int, int]]]:
    """Extract RTF \\colortbl entries as RGB tuples (index 0 may be None/auto)."""
    m = re.search(r"\{\\colortbl\b", rtf_raw)
    if not m:
        return []
    start = m.start()
    depth = 0
    end = start
    n = len(rtf_raw)
    for idx in range(start, n):
        ch = rtf_raw[idx]
        if ch == "{" and (idx == 0 or rtf_raw[idx - 1] != "\\"):
            depth += 1
        elif ch == "}" and (idx == 0 or rtf_raw[idx - 1] != "\\"):
            depth -= 1
            if depth == 0:
                end = idx + 1
                break
    tbl = rtf_raw[start:end]
    # Remove outer '{\colortbl' and trailing '}'
    inner = re.sub(r"^\{\\colortbl\b\s*", "", tbl)
    if inner.endswith("}"):
        inner = inner[:-1]
    colors: List[Optional[Tuple[int, int, int]]] = []
    for entry in inner.split(";")[:-1]:
        r_m = re.search(r"\\red(\d+)", entry)
        g_m = re.search(r"\\green(\d+)", entry)
        b_m = re.search(r"\\blue(\d+)", entry)
        if r_m and g_m and b_m:
            colors.append((
                max(0, min(255, int(r_m.group(1)))),
                max(0, min(255, int(g_m.group(1)))),
                max(0, min(255, int(b_m.group(1)))),
            ))
        else:
            colors.append(None)
    return colors


def sanitize_rtf(rtf_path: str) -> SanitizationReport:
    """
    Layer 3 (Tier 2): Sanitize RTF files by parsing RTF groups/control words
    and stripping \\v hidden text, white/low-contrast colors, micro-font (<4pt),
    \\deleted revisions, and auditing \\info metadata, \\annotation, \\fldinst,
    headers/footers, and ignorable \\* destinations.
    """
    try:
        with open(rtf_path, "rb") as f:
            raw_bytes = f.read()
    except Exception as exc:
        return SanitizationReport(
            file_type="rtf",
            engine_used="rtf_stdlib",
            source_path=rtf_path,
            risk_level="none",
            stats={"error": str(exc)},
        )

    rtf_raw = raw_bytes.decode("latin-1", errors="ignore")
    cpg_m = re.search(r"\\ansicpg(\d+)", rtf_raw[:1024])
    codepage = f"cp{cpg_m.group(1)}" if cpg_m else "cp1252"
    try:
        b"a".decode(codepage)
    except Exception:
        codepage = "cp1252"

    colortbl = _parse_rtf_colortbl(rtf_raw)

    def _state_reason(st: Dict[str, Any]) -> Optional[str]:
        dest = st["dest"]
        if dest != "body":
            return f"aux:{dest}"
        if st["hidden"]:
            return "rtf_hidden_text"
        if st["deleted"]:
            return "rtf_tracked_deletion"
        if 0 < st["fs"] < 4.0:
            return "rtf_micro_font"
        cf_idx = st["cf"]
        cb_idx = st["cb"]
        fg = colortbl[cf_idx] if 0 <= cf_idx < len(colortbl) else None
        bg = colortbl[cb_idx] if 0 <= cb_idx < len(colortbl) else (255, 255, 255)
        if fg is not None and bg is not None and contrast_ratio(fg, bg) < 1.8:
            return "rtf_low_contrast"
        return None

    vis_parts: List[str] = []
    trap_buckets: Dict[str, List[str]] = {}
    aux_buckets: Dict[str, List[str]] = {}

    cur_buf: List[str] = []
    hex_buf = bytearray()
    skip_chars = 0
    ignorable_star = False

    stack: List[Dict[str, Any]] = [{
        "uc": 1,
        "hidden": False,
        "deleted": False,
        "fs": 12.0,
        "cf": -1,
        "cb": -1,
        "dest": "body",
        "skip_group": False,
    }]

    def _flush_hex() -> None:
        nonlocal hex_buf
        if hex_buf:
            cur_buf.append(bytes(hex_buf).decode(codepage, errors="replace"))
            hex_buf.clear()

    def _flush_run() -> None:
        _flush_hex()
        if not cur_buf:
            return
        text = "".join(cur_buf)
        cur_buf.clear()
        if not text:
            return
        top = stack[-1]
        if top["skip_group"]:
            return
        reason = _state_reason(top)
        if reason is None:
            vis_parts.append(text)
        elif reason.startswith("aux:"):
            dest = reason[4:]
            aux_buckets.setdefault(dest, []).append(text)
        else:
            trap_buckets.setdefault(reason, []).append(text)

    i = 0
    n = len(rtf_raw)
    while i < n:
        ch = rtf_raw[i]
        if ch == "{":
            _flush_run()
            stack.append(dict(stack[-1]))
            ignorable_star = False
            skip_chars = 0
            i += 1
        elif ch == "}":
            _flush_run()
            if len(stack) > 1:
                stack.pop()
            ignorable_star = False
            skip_chars = 0
            i += 1
        elif ch == "\\":
            if i + 1 >= n:
                break
            nxt = rtf_raw[i + 1]
            # Escaped literal chars
            if nxt in ("\\", "{", "}"):
                _flush_hex()
                if skip_chars > 0:
                    skip_chars -= 1
                elif not stack[-1]["skip_group"]:
                    cur_buf.append(nxt)
                i += 2
            elif nxt == "*":
                _flush_hex()
                ignorable_star = True
                i += 2
            elif nxt == "'":
                # Hex byte \'hh
                if i + 3 < n:
                    hx = rtf_raw[i + 2 : i + 4]
                    try:
                        bval = int(hx, 16)
                        if skip_chars > 0:
                            skip_chars -= 1
                        elif not stack[-1]["skip_group"]:
                            hex_buf.append(bval)
                        i += 4
                        continue
                    except ValueError:
                        pass
                i += 2
            elif nxt == "~":
                _flush_hex()
                if skip_chars > 0:
                    skip_chars -= 1
                elif not stack[-1]["skip_group"]:
                    cur_buf.append(" ")
                i += 2
            elif nxt == "_":
                _flush_hex()
                if skip_chars > 0:
                    skip_chars -= 1
                elif not stack[-1]["skip_group"]:
                    cur_buf.append("-")
                i += 2
            elif nxt in ("-", "\r", "\n"):
                _flush_hex()
                if nxt in ("\r", "\n") and not stack[-1]["skip_group"]:
                    cur_buf.append("\n")
                i += 2
            elif nxt.isalpha():
                _flush_hex()
                j = i + 1
                while j < n and rtf_raw[j].isalpha():
                    j += 1
                word = rtf_raw[i + 1 : j]
                # Optional numeric parameter
                k = j
                if k < n and (rtf_raw[k] == "-" or rtf_raw[k].isdigit()):
                    k += 1
                    while k < n and rtf_raw[k].isdigit():
                        k += 1
                    param_str = rtf_raw[j:k]
                    try:
                        param: Optional[int] = int(param_str)
                    except ValueError:
                        param = None
                else:
                    param = None
                # Single optional delimiter space is consumed by RTF spec
                if k < n and rtf_raw[k] == " ":
                    k += 1
                i = k

                top = stack[-1]
                # Destination words
                if word in _RTF_SKIP_DESTS:
                    _flush_run()
                    top["skip_group"] = True
                elif word in _RTF_INFO_DESTS:
                    _flush_run()
                    top["dest"] = "info"
                elif word in _RTF_ANNOT_DESTS:
                    _flush_run()
                    top["dest"] = "annotation"
                elif word == "fldinst":
                    _flush_run()
                    top["dest"] = "fldinst"
                elif word in _RTF_HEADER_DESTS:
                    _flush_run()
                    top["dest"] = "header_footer"
                elif ignorable_star and top["dest"] == "body" and word not in ("rtf",):
                    _flush_run()
                    top["dest"] = "ignorable"
                elif word == "v":
                    _flush_run()
                    top["hidden"] = False if param == 0 else True
                elif word == "deleted":
                    _flush_run()
                    top["deleted"] = False if param == 0 else True
                elif word == "plain":
                    _flush_run()
                    top["hidden"] = False
                    top["deleted"] = False
                    top["fs"] = 12.0
                    top["cf"] = -1
                    top["cb"] = -1
                elif word == "fs" and param is not None and param > 0:
                    _flush_run()
                    top["fs"] = param / 2.0
                elif word == "cf" and param is not None:
                    _flush_run()
                    top["cf"] = param
                elif word in ("cb", "highlight") and param is not None:
                    _flush_run()
                    top["cb"] = param
                elif word == "uc" and param is not None and param >= 0:
                    top["uc"] = param
                elif word == "u" and param is not None:
                    if not top["skip_group"]:
                        code = param if param >= 0 else param + 65536
                        if 0 <= code <= 0x10FFFF:
                            cur_buf.append(chr(code))
                    skip_chars = top["uc"]
                elif word in ("par", "line", "row"):
                    if not top["skip_group"]:
                        cur_buf.append("\n")
                elif word in ("tab", "cell"):
                    if not top["skip_group"]:
                        cur_buf.append("\t")
                ignorable_star = False
            else:
                i += 2
        elif ch in ("\r", "\n"):
            i += 1
        else:
            _flush_hex()
            if skip_chars > 0:
                skip_chars -= 1
            elif not stack[-1]["skip_group"]:
                cur_buf.append(ch)
            i += 1

    _flush_run()

    stripped_traps: List[TrapRecord] = []
    for reason, parts in trap_buckets.items():
        joined = "".join(parts).strip()
        if joined:
            stripped_traps.append(_make_trap(reason, joined, "rtf:body", "high"))

    dest_reason_map = {
        "info": "rtf_metadata",
        "annotation": "rtf_annotation",
        "fldinst": "rtf_field_code",
        "header_footer": "rtf_header_footer",
        "ignorable": "rtf_hidden_group",
    }
    for dest, parts in aux_buckets.items():
        joined = "".join(parts).strip()
        if not joined:
            continue
        if dest in ("annotation", "ignorable") or _is_suspicious_or_semantic(joined):
            stripped_traps.append(
                _make_trap(
                    dest_reason_map.get(dest, "rtf_hidden_group"),
                    joined[:300],
                    f"rtf:{dest}",
                    "high",
                )
            )

    clean_text = "\n".join(ln.rstrip() for ln in "".join(vis_parts).splitlines()).strip()
    return _finalize_report(
        clean_text=clean_text,
        stripped_traps=stripped_traps,
        file_type="rtf",
        engine_used="rtf_stdlib",
        source_path=rtf_path,
    )


def _odf_local(tag: str) -> str:
    return tag.split("}", 1)[-1] if "}" in tag else tag


def _odf_attr(elem: Any, names: Tuple[str, ...]) -> Optional[str]:
    """Lookup ODF attribute by exact local name(s) across namespaces."""
    for k, v in elem.attrib.items():
        loc = _odf_local(k)
        if loc in names:
            return v
    return None


def _parse_odf_coord_val(val: Optional[str]) -> Optional[float]:
    if not val:
        return None
    m = re.match(r"^\s*(-?\d+(?:\.\d+)?)\s*(cm|mm|in|pt|px)?\s*$", val, re.IGNORECASE)
    if not m:
        return None
    num = float(m.group(1))
    unit = (m.group(2) or "pt").lower()
    factor = {"pt": 1.0, "px": 0.75, "in": 72.0, "cm": 28.3465, "mm": 2.83465}.get(unit, 1.0)
    return num * factor


def _parse_odf_opacity(val: Optional[str]) -> Optional[float]:
    if not val:
        return None
    s = val.strip()
    if s.endswith("%"):
        try:
            return max(0.0, min(1.0, float(s[:-1]) / 100.0))
        except ValueError:
            return None
    try:
        v = float(s)
        return v / 100.0 if v > 1.0 else max(0.0, min(1.0, v))
    except ValueError:
        return None


def sanitize_odf(odf_path: str) -> SanitizationReport:
    """
    Layer 3 (Tier 2): Sanitize OpenDocument files (.odt, .odp, .ods) using stdlib
    zipfile + ElementTree. Strips text:display='none', white/low-contrast text,
    micro-font (<4pt), low opacity, hidden sections/slides/sheets/rows/columns,
    off-page frames, tracked deletions; audits annotations, presenter notes,
    meta.xml metadata, and Pictures/* image metadata.
    """
    import xml.etree.ElementTree as ET

    ext = os.path.splitext(odf_path)[1].lower().lstrip(".") or "odf"
    try:
        zf = zipfile.ZipFile(odf_path, "r")
    except Exception as exc:
        return SanitizationReport(
            file_type=ext,
            engine_used="odf_stdlib",
            source_path=odf_path,
            risk_level="none",
            stats={"error": str(exc)},
        )

    styles: Dict[str, Dict[str, Any]] = {}
    stripped_traps: List[TrapRecord] = []

    def _collect_styles(xml_bytes: bytes) -> None:
        try:
            root = ET.fromstring(xml_bytes)
        except Exception:
            return
        for st_el in root.iter():
            if _odf_local(st_el.tag) != "style":
                continue
            name = _odf_attr(st_el, ("name",))
            if not name:
                continue
            info: Dict[str, Any] = {
                "parent": _odf_attr(st_el, ("parent-style-name",)),
                "display": None,
                "color": None,
                "bg_color": None,
                "font_size_pt": None,
                "opacity": None,
                "table_display": None,
            }
            for child in st_el:
                loc = _odf_local(child.tag)
                if loc == "text-properties":
                    disp = _odf_attr(child, ("display",))
                    if disp is not None:
                        info["display"] = disp.strip().lower()
                    col = _odf_attr(child, ("color",))
                    if col:
                        rgb, _ = parse_css_color(col)
                        if rgb is not None:
                            info["color"] = rgb
                    bg = _odf_attr(child, ("background-color",))
                    if bg and bg.strip().lower() != "transparent":
                        rgb, _ = parse_css_color(bg)
                        if rgb is not None:
                            info["bg_color"] = rgb
                    fs = _odf_attr(child, ("font-size", "font-size-asian", "font-size-complex"))
                    if fs:
                        pt = _parse_css_font_size_pt(fs)
                        if pt is not None:
                            info["font_size_pt"] = pt
                elif loc == "paragraph-properties":
                    bg = _odf_attr(child, ("background-color",))
                    if bg and bg.strip().lower() != "transparent":
                        rgb, _ = parse_css_color(bg)
                        if rgb is not None:
                            info["bg_color"] = rgb
                elif loc == "graphic-properties":
                    op = _odf_attr(child, ("opacity",))
                    if op:
                        op_v = _parse_odf_opacity(op)
                        if op_v is not None:
                            info["opacity"] = op_v
                    fill_col = _odf_attr(child, ("fill-color",))
                    if fill_col and info["bg_color"] is None:
                        rgb, _ = parse_css_color(fill_col)
                        if rgb is not None:
                            info["bg_color"] = rgb
                elif loc == "table-properties":
                    td = _odf_attr(child, ("display",))
                    if td is not None:
                        info["table_display"] = td.strip().lower() != "false"
            styles[name] = info

    def _resolve_style(name: Optional[str]) -> Dict[str, Any]:
        resolved: Dict[str, Any] = {
            "display": None,
            "color": None,
            "bg_color": None,
            "font_size_pt": None,
            "opacity": None,
            "table_display": None,
        }
        if not name:
            return resolved
        chain: List[Dict[str, Any]] = []
        seen: set = set()
        cur: Optional[str] = name
        while cur and cur not in seen and cur in styles:
            seen.add(cur)
            chain.append(styles[cur])
            cur = styles[cur].get("parent")
        for item in reversed(chain):
            for k in resolved:
                if item.get(k) is not None:
                    resolved[k] = item[k]
        return resolved

    def _merge_style(base: Dict[str, Any], name: Optional[str]) -> Dict[str, Any]:
        out = dict(base)
        if name:
            st = _resolve_style(name)
            for k, v in st.items():
                if v is not None:
                    out[k] = v
        return out

    def _collect_plain_text(el: Any, exclude_annotations: bool = True) -> str:
        loc = _odf_local(el.tag)
        if exclude_annotations and loc in ("annotation", "tracked-changes", "deletion"):
            return ""
        parts: List[str] = []
        if el.text:
            parts.append(el.text)
        for ch in el:
            parts.append(_collect_plain_text(ch, exclude_annotations=exclude_annotations))
            if ch.tail:
                parts.append(ch.tail)
        return "".join(parts)

    with zf:
        for xml_name in ("styles.xml", "content.xml"):
            if xml_name in zf.namelist():
                try:
                    _collect_styles(zf.read(xml_name))
                except Exception:
                    pass

        visible_parts: List[str] = []
        slide_count = 0
        sheet_count = 0

        if "content.xml" in zf.namelist():
            try:
                content_root = ET.fromstring(zf.read("content.xml"))
            except Exception:
                content_root = None

            def _style_defect(eff: Dict[str, Any]) -> Optional[str]:
                if eff.get("display") == "none":
                    return "odf_hidden_text"
                if eff.get("opacity") is not None and eff["opacity"] < 0.15:
                    return "odf_transparent_text"
                fs_pt = eff.get("font_size_pt")
                if fs_pt is not None and 0 < fs_pt < 4.0:
                    return "odf_micro_font"
                fg = eff.get("color")
                if fg is not None:
                    bg = eff.get("bg_color") or (255, 255, 255)
                    if contrast_ratio(fg, bg) < 1.8:
                        return "odf_low_contrast"
                return None

            def _walk_table(tbl_el: Any, inherited: Dict[str, Any]) -> None:
                nonlocal sheet_count
                sheet_count += 1
                t_name = _odf_attr(tbl_el, ("name",)) or f"sheet_{sheet_count}"
                st_name = _odf_attr(tbl_el, ("style-name",))
                eff_tbl = _merge_style(inherited, st_name)
                if eff_tbl.get("table_display") is False:
                    hidden_txt = _collect_plain_text(tbl_el).strip()
                    if hidden_txt:
                        stripped_traps.append(
                            _make_trap("odf_hidden_sheet", hidden_txt[:300], f"{ext}:sheet:{t_name}", "high")
                        )
                    return

                hidden_cols: set = set()
                col_idx = 0
                for child in tbl_el:
                    cloc = _odf_local(child.tag)
                    if cloc == "table-column":
                        vis = (_odf_attr(child, ("visibility",)) or "").strip().lower()
                        rep_str = _odf_attr(child, ("number-columns-repeated",))
                        rep = int(rep_str) if rep_str and rep_str.isdigit() else 1
                        rep = min(rep, 1000)
                        if vis in ("collapse", "filter"):
                            for c_i in range(col_idx, col_idx + rep):
                                hidden_cols.add(c_i)
                        col_idx += rep
                    elif cloc in ("table-row", "table-header-rows", "table-rows"):
                        rows = [child] if cloc == "table-row" else list(child)
                        for row_el in rows:
                            if _odf_local(row_el.tag) != "table-row":
                                continue
                            rvis = (_odf_attr(row_el, ("visibility",)) or "").strip().lower()
                            if rvis in ("collapse", "filter"):
                                row_txt = _collect_plain_text(row_el).strip()
                                if row_txt:
                                    stripped_traps.append(
                                        _make_trap("odf_hidden_row_col", row_txt[:300], f"{ext}:sheet:{t_name}", "high")
                                    )
                                continue
                            c_idx = 0
                            row_cells: List[str] = []
                            for cell in row_el:
                                cell_loc = _odf_local(cell.tag)
                                if cell_loc not in ("table-cell", "covered-table-cell"):
                                    continue
                                rep_s = _odf_attr(cell, ("number-columns-repeated",))
                                rep = int(rep_s) if rep_s and rep_s.isdigit() else 1
                                rep = min(rep, 1000)
                                is_hidden_col = c_idx in hidden_cols
                                c_idx += rep
                                if is_hidden_col:
                                    ct = _collect_plain_text(cell).strip()
                                    if ct:
                                        stripped_traps.append(
                                            _make_trap("odf_hidden_row_col", ct[:300], f"{ext}:sheet:{t_name}", "high")
                                        )
                                    continue
                                cell_buf: List[str] = []
                                _walk_el(cell, eff_tbl, f"{ext}:sheet:{t_name}", cell_buf)
                                cell_txt = "".join(cell_buf).strip()
                                if cell_txt:
                                    row_cells.append(cell_txt)
                            if row_cells:
                                visible_parts.append("\t".join(row_cells) + "\n")

            def _walk_el(el: Any, inherited: Dict[str, Any], loc: str, out_buf: List[str]) -> None:
                nonlocal slide_count
                tag_loc = _odf_local(el.tag)

                if tag_loc in ("tracked-changes", "deletion"):
                    dt = _collect_plain_text(el, exclude_annotations=False).strip()
                    if dt:
                        stripped_traps.append(_make_trap("odf_tracked_deletion", dt[:300], loc, "high"))
                    return

                if tag_loc == "annotation":
                    at = _collect_plain_text(el, exclude_annotations=False).strip()
                    if at and _is_suspicious_or_semantic(at):
                        stripped_traps.append(_make_trap("odf_annotation", at[:300], loc, "high"))
                    return

                if tag_loc in ("hidden-text", "hidden-paragraph"):
                    ht = (_odf_attr(el, ("string-value",)) or _collect_plain_text(el)).strip()
                    if ht:
                        stripped_traps.append(_make_trap("odf_hidden_text", ht[:300], loc, "high"))
                    return

                if tag_loc == "section":
                    disp = (_odf_attr(el, ("display",)) or "").strip().lower()
                    cond = (_odf_attr(el, ("condition",)) or "").strip().lower()
                    if disp == "none" or (disp == "condition" and cond in ("0", "false", "false()", "off")):
                        st = _collect_plain_text(el).strip()
                        if st:
                            stripped_traps.append(_make_trap("odf_hidden_section", st[:300], loc, "high"))
                        return

                if tag_loc == "page":
                    slide_count += 1
                    p_loc = f"{ext}:slide:{slide_count}"
                    pvis = (_odf_attr(el, ("visibility",)) or "").strip().lower()
                    if pvis == "hidden":
                        st = _collect_plain_text(el).strip()
                        if st:
                            stripped_traps.append(_make_trap("odf_hidden_slide", st[:300], p_loc, "high"))
                        return
                    loc = p_loc

                if tag_loc == "notes":
                    nt = _collect_plain_text(el).strip()
                    if nt and _is_suspicious_or_semantic(nt):
                        stripped_traps.append(_make_trap("odf_speaker_notes", nt[:300], f"{loc}:notes", "high"))
                    return

                if tag_loc == "table":
                    _walk_table(el, inherited)
                    return

                # Inherit style + direct attribute overrides
                st_name = _odf_attr(el, ("style-name", "text-style-name"))
                eff = _merge_style(inherited, st_name)
                direct_disp = _odf_attr(el, ("display",))
                if direct_disp is not None and tag_loc != "section":
                    eff["display"] = direct_disp.strip().lower()
                direct_col = _odf_attr(el, ("color",))
                if direct_col:
                    rgb, _ = parse_css_color(direct_col)
                    if rgb is not None:
                        eff["color"] = rgb
                direct_fs = _odf_attr(el, ("font-size",))
                if direct_fs:
                    pt = _parse_css_font_size_pt(direct_fs)
                    if pt is not None:
                        eff["font_size_pt"] = pt

                if tag_loc == "frame":
                    x_pt = _parse_odf_coord_val(_odf_attr(el, ("x",)))
                    y_pt = _parse_odf_coord_val(_odf_attr(el, ("y",)))
                    if (x_pt is not None and (x_pt < -5.0 or x_pt > 2000.0)) or (
                        y_pt is not None and (y_pt < -5.0 or y_pt > 2000.0)
                    ):
                        ft = _collect_plain_text(el).strip()
                        if ft:
                            stripped_traps.append(_make_trap("odf_off_page", ft[:300], loc, "high"))
                        return

                defect = _style_defect(eff)
                if defect is not None:
                    dt_txt = _collect_plain_text(el).strip()
                    if dt_txt:
                        stripped_traps.append(_make_trap(defect, dt_txt[:300], loc, "high"))
                    return

                if tag_loc == "s":
                    cnt_s = _odf_attr(el, ("c",))
                    cnt = int(cnt_s) if cnt_s and cnt_s.isdigit() else 1
                    out_buf.append(" " * min(cnt, 50))
                elif tag_loc == "tab":
                    out_buf.append("\t")
                elif tag_loc == "line-break":
                    out_buf.append("\n")

                if el.text:
                    out_buf.append(el.text)
                for ch in el:
                    _walk_el(ch, eff, loc, out_buf)
                    if ch.tail:
                        out_buf.append(ch.tail)

                if tag_loc in ("p", "h", "list-item", "page"):
                    out_buf.append("\n")

            if content_root is not None:
                base_style = {
                    "display": None,
                    "color": None,
                    "bg_color": None,
                    "font_size_pt": None,
                    "opacity": None,
                    "table_display": None,
                }
                _walk_el(content_root, base_style, f"{ext}:body", visible_parts)

        # Audit meta.xml
        if "meta.xml" in zf.namelist():
            try:
                mroot = ET.fromstring(zf.read("meta.xml"))
                meta_tags = {"title", "description", "subject", "keyword", "user-defined", "creator", "initial-creator"}
                for mel in mroot.iter():
                    if _odf_local(mel.tag) in meta_tags:
                        mt = "".join(mel.itertext()).strip()
                        if mt and _is_suspicious_or_semantic(mt):
                            stripped_traps.append(
                                _make_trap(
                                    "odf_metadata",
                                    f"[{_odf_local(mel.tag)}] {mt[:250]}",
                                    f"{ext}:meta.xml",
                                    "high",
                                )
                            )
            except Exception:
                pass

        # Audit embedded images in Pictures/
        _audit_archive_images(zf, prefix="Pictures/", location_prefix=ext, stripped_traps=stripped_traps)

    clean_text = "\n".join(ln.rstrip() for ln in "".join(visible_parts).splitlines()).strip()
    return _finalize_report(
        clean_text=clean_text,
        stripped_traps=stripped_traps,
        file_type=ext,
        engine_used="odf_stdlib",
        source_path=odf_path,
    )


_AGENT_RULE_BASENAMES = {
    ".cursorrules",
    ".windsurfrules",
    ".clinerules",
    ".aider.conf.yml",
    "claude.md",
    "agents.md",
    "gemini.md",
    "copilot-instructions.md",
}
_AGENT_RULE_PATH_PREFIXES = (
    ".cursor/rules/",
    ".claude/rules/",
    ".claude/commands/",
    ".claude/agents/",
    ".agent/rules/",
    ".agent/workflows/",
    ".github/instructions/",
)
_AGENT_RULE_EXACT_PATHS = {
    ".github/copilot-instructions.md",
    ".mcp.json",
    ".cursor/mcp.json",
}
_RULE_WALK_SKIP_DIRS = {
    ".git",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "build",
    "dist",
    "target",
    "nbproject",
}


def _is_agent_rule_path(rel_path: str) -> bool:
    """Check if a relative path targets an AI IDE / coding-agent instruction or MCP config file."""
    norm = rel_path.replace("\\", "/").lower()
    while norm.startswith("./"):
        norm = norm[2:]
    norm = norm.lstrip("/")
    if not norm:
        return False
    base = os.path.basename(norm)
    if base in _AGENT_RULE_BASENAMES:
        return True
    if norm in _AGENT_RULE_EXACT_PATHS:
        return True
    for pref in _AGENT_RULE_PATH_PREFIXES:
        if norm.startswith(pref) or f"/{pref}" in norm:
            return True
    return False


def audit_workspace_agent_rules(workspace_dir: str, max_depth: int = 3) -> Dict[str, Any]:
    """
    Scan a workspace for poisoned AI IDE / CLI agent rule files (.cursorrules,
    CLAUDE.md, AGENTS.md, GEMINI.md, .windsurfrules, .clinerules, .cursor/rules/*,
    .github/copilot-instructions.md, .agent/rules/*, .mcp.json).
    Skips NgeLaprak's own repository directory cleanly.
    """
    root = os.path.abspath(workspace_dir)
    if not os.path.isdir(root):
        return {
            "workspace_dir": root,
            "skipped_self_repo": False,
            "rule_files_found": [],
            "findings": [],
            "forbidden_identifiers": [],
            "risk_level": "none",
            "has_poisoning": False,
        }

    # Skip NgeLaprak's own repo root / dual-copy package root
    if os.path.isfile(os.path.join(root, "ngelaprak", "core", "anti_trap.py")):
        return {
            "workspace_dir": root,
            "skipped_self_repo": True,
            "rule_files_found": [],
            "findings": [],
            "forbidden_identifiers": [],
            "risk_level": "none",
            "has_poisoning": False,
        }

    findings: List[Dict[str, Any]] = []
    all_forbidden: List[str] = []
    seen_ident: set = set()

    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root)
        depth = 0 if rel_dir == "." else len(rel_dir.replace("\\", "/").split("/"))
        dirnames[:] = [
            d for d in sorted(dirnames)
            if d not in _RULE_WALK_SKIP_DIRS and depth < max_depth
        ]
        for fname in sorted(filenames):
            rel = fname if rel_dir == "." else os.path.join(rel_dir, fname)
            rel_norm = rel.replace("\\", "/")
            if not _is_agent_rule_path(rel_norm):
                continue
            full_fp = os.path.join(dirpath, fname)
            try:
                with open(full_fp, "r", encoding="utf-8", errors="ignore") as f:
                    raw = f.read(100_000)
            except Exception:
                continue
            if not raw.strip():
                continue

            clean_u, u_traps, _ = sanitize_text(raw)
            sem_warns = detect_semantic_traps(clean_u)
            idents = extract_forbidden_identifiers(clean_u)
            for ident in idents:
                if ident.lower() not in seen_ident:
                    seen_ident.add(ident.lower())
                    all_forbidden.append(ident)

            findings.append(
                {
                    "file": rel_norm,
                    "reason": "agent_rule_poisoning",
                    "severity": "critical",
                    "snippet": clean_u.strip()[:250] or raw.strip()[:250],
                    "semantic_warnings": sem_warns,
                    "forbidden_identifiers": idents,
                    "unicode_traps": len(u_traps),
                }
            )

    return {
        "workspace_dir": root,
        "skipped_self_repo": False,
        "rule_files_found": [f["file"] for f in findings],
        "findings": findings,
        "forbidden_identifiers": all_forbidden,
        "risk_level": "critical" if findings else "none",
        "has_poisoning": len(findings) > 0,
    }


def sanitize_zip(zip_path: str, max_depth: int = 2) -> SanitizationReport:
    """
    Layer 3 (Tier 2): Safely inspect and sanitize .zip course/assignment archives.
    Guards against zip-slip and zip-bomb abuse, flags any bundled AI agent rule
    files (.cursorrules, CLAUDE.md, AGENTS.md, etc.) as agent_rule_poisoning,
    and recursively sanitizes supported document, image, and source files.
    """
    import tempfile

    if not os.path.exists(zip_path):
        return SanitizationReport(
            file_type="zip", engine_used="zip_stdlib", risk_level="none", source_path=zip_path
        )

    try:
        zf = zipfile.ZipFile(zip_path, "r")
    except Exception as exc:
        return SanitizationReport(
            file_type="zip",
            engine_used="zip_stdlib",
            risk_level="none",
            source_path=zip_path,
            stats={"error": str(exc)},
        )

    supported_doc_exts = {
        ".pdf", ".docx", ".pptx", ".xlsx", ".rtf", ".odt", ".odp", ".ods",
        ".html", ".htm", ".xhtml", ".md", ".markdown", ".ipynb", ".svg",
        ".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif", ".txt",
    } | _CODE_EXTS
    if max_depth > 0:
        supported_doc_exts.add(".zip")

    stripped_traps: List[TrapRecord] = []
    extra_warnings: List[Dict[str, Any]] = []
    extra_forbidden: List[str] = []
    clean_sections: List[str] = []
    audited_members: List[str] = []

    max_members = 60
    max_single_bytes = 20_000_000
    max_total_bytes = 50_000_000
    total_read = 0

    with zf, tempfile.TemporaryDirectory() as tmpdir:
        for info in zf.infolist():
            if info.is_dir():
                continue
            member = info.filename.replace("\\", "/")
            # Guard zip-slip & OS noise
            if member.startswith("/") or ".." in member.split("/") or re.match(r"^[A-Za-z]:", member):
                stripped_traps.append(
                    _make_trap("zip_unsafe_path", member[:200], f"zip:{member}", "critical")
                )
                continue
            low = member.lower()
            if low.startswith("__macosx/") or "/.git/" in f"/{low}" or "/node_modules/" in f"/{low}":
                continue
            if info.file_size > max_single_bytes or total_read + info.file_size > max_total_bytes:
                stripped_traps.append(
                    _make_trap("zip_size_limit", f"{member} ({info.file_size} bytes)", f"zip:{member}", "high")
                )
                continue

            is_rule = _is_agent_rule_path(member)
            ext = os.path.splitext(low)[1]
            if not is_rule and ext not in supported_doc_exts:
                continue
            if len(audited_members) >= max_members:
                break

            try:
                data = zf.read(info.filename)
            except Exception:
                continue
            if len(data) > max_single_bytes or total_read + len(data) > max_total_bytes:
                continue
            total_read += len(data)
            audited_members.append(member)

            if is_rule:
                raw_rule = data.decode("utf-8", errors="ignore")
                if raw_rule.strip():
                    clean_rule, _, _ = sanitize_text(raw_rule)
                    stripped_traps.append(
                        _make_trap(
                            "agent_rule_poisoning",
                            clean_rule.strip()[:300] or raw_rule.strip()[:300],
                            f"zip:{member}",
                            "critical",
                        )
                    )
                    extra_forbidden.extend(extract_forbidden_identifiers(clean_rule))
                    for w in detect_semantic_traps(clean_rule):
                        extra_warnings.append(w)
                continue

            # Safe flat-or-nested destination inside tmpdir
            safe_name = re.sub(r"[^A-Za-z0-9._-]", "_", os.path.basename(member)) or "item"
            out_fp = os.path.join(tmpdir, f"{len(audited_members)}_{safe_name}")
            with open(out_fp, "wb") as out_f:
                out_f.write(data)

            if ext == ".zip":
                rep = sanitize_zip(out_fp, max_depth=max_depth - 1)
            else:
                rep = sanitize_document(out_fp)

            for tr in rep.stripped_traps:
                stripped_traps.append(
                    _make_trap(
                        tr["reason"],
                        tr.get("text", ""),
                        f"zip:{member}:{tr.get('location', '')}",
                        tr.get("severity", "high"),
                        tr.get("details"),
                    )
                )
            extra_forbidden.extend(rep.forbidden_identifiers)
            for w in rep.semantic_warnings:
                extra_warnings.append(w)

            if rep.clean_text and rep.clean_text.strip() and ext not in (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"):
                clean_sections.append(f"[FILE: {member}]\n{rep.clean_text.strip()}")

    combined_clean = "\n\n".join(clean_sections)
    return _finalize_report(
        clean_text=combined_clean,
        stripped_traps=stripped_traps,
        file_type="zip",
        engine_used="zip_stdlib",
        source_path=zip_path,
        extra_warnings=extra_warnings,
        extra_forbidden=extra_forbidden,
        stats={"audited_members": len(audited_members), "total_bytes_read": total_read},
        run_unicode_on_clean=False,
    )


# ---------------------------------------------------------------------------
# Main Document Router
# ---------------------------------------------------------------------------

_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif", ".svg"}
_CODE_EXTS = {
    ".cpp", ".c", ".cc", ".cxx", ".h", ".hpp", ".java", ".py", ".sql",
    ".js", ".ts", ".jsx", ".tsx", ".php", ".cs", ".go", ".rs", ".kt",
    ".swift", ".rb", ".sh", ".ps1",
}


def sanitize_document(
    file_path: str,
    engine: str = "auto",
    max_pages: Optional[int] = None,
    out_image_path: Optional[str] = None,
) -> SanitizationReport:
    """
    Unified multi-format sanitization router. Dispatches based on file extension
    and applies all applicable defense-in-depth layers.
    """
    if not os.path.exists(file_path):
        return SanitizationReport(
            file_type="missing", engine_used="none", risk_level="none", source_path=file_path
        )

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return sanitize_pdf(file_path, engine=engine, max_pages=max_pages)
    if ext in _IMAGE_EXTS:
        return sanitize_image(file_path, out_image_path=out_image_path)
    if ext == ".docx":
        return sanitize_docx(file_path)
    if ext == ".pptx":
        return sanitize_pptx(file_path)
    if ext == ".xlsx":
        return sanitize_xlsx(file_path)
    if ext == ".rtf":
        return sanitize_rtf(file_path)
    if ext in (".odt", ".odp", ".ods"):
        return sanitize_odf(file_path)
    if ext == ".zip":
        return sanitize_zip(file_path)
    if ext in (".html", ".htm", ".xhtml"):
        return sanitize_markup(file_path, markup_type="html")
    if ext in (".md", ".markdown"):
        return sanitize_markup(file_path, markup_type="markdown")
    if ext == ".ipynb":
        return sanitize_ipynb(file_path)
    if ext in _CODE_EXTS:
        return sanitize_code(file_path)

    # Fallback: plain text file with Layer 4 (Unicode) + Layer 5 (Semantic)
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            raw = f.read()
    except Exception:
        raw = ""
    return _finalize_report(
        clean_text=raw,
        stripped_traps=[],
        file_type="text",
        engine_used="text",
        source_path=file_path,
    )


# ---------------------------------------------------------------------------
# Layer 6: Final Codebase Audit (`audit_code_for_traps`)
# ---------------------------------------------------------------------------

_AUDIT_SKIP_DIRS = {
    ".git", "node_modules", "venv", ".venv", "__pycache__", "target", "build",
    "dist", "bin", "obj", ".idea", ".vscode",
}

_AUDIT_CODE_EXTS = _CODE_EXTS | {".html", ".htm", ".css", ".xml", ".json", ".yaml", ".yml"}


def audit_code_for_traps(
    code_dir: str,
    forbidden_identifiers: Optional[Iterable[str]] = None,
    report: Optional[Union[SanitizationReport, Dict[str, Any], str]] = None,
    source_files: Optional[Iterable[str]] = None,
    extensions: Optional[Iterable[str]] = None,
) -> Dict[str, Any]:
    """
    Layer 6: Audits all source code files in `code_dir` (or a single file) for any
    leaked forbidden identifiers / canary watermarks extracted during document sanitization,
    as well as hidden Unicode / Trojan Source characters.
    """
    ids: List[str] = []
    seen_ids: set[str] = set()

    def _add_ids(items: Iterable[str]) -> None:
        for it in items:
            s = str(it).strip()
            if s and s.lower() not in seen_ids:
                seen_ids.add(s.lower())
                ids.append(s)

    if forbidden_identifiers:
        _add_ids(forbidden_identifiers)

    if report is not None:
        if isinstance(report, SanitizationReport):
            _add_ids(report.forbidden_identifiers)
        elif isinstance(report, dict):
            _add_ids(report.get("forbidden_identifiers", []))
        elif isinstance(report, str) and os.path.exists(report):
            with open(report, "r", encoding="utf-8") as f:
                data = json.load(f)
            _add_ids(data.get("forbidden_identifiers", []))

    if source_files:
        for sf in source_files:
            if sf and os.path.exists(sf):
                rep = sanitize_document(sf)
                _add_ids(rep.forbidden_identifiers)

    allowed_exts = {e.lower() for e in extensions} if extensions else _AUDIT_CODE_EXTS

    target = os.path.abspath(code_dir)
    files_to_scan: List[str] = []
    if os.path.isfile(target):
        files_to_scan.append(target)
    elif os.path.isdir(target):
        for root, dirs, files in os.walk(target):
            dirs[:] = [d for d in dirs if d not in _AUDIT_SKIP_DIRS and not d.startswith(".")]
            for fn in sorted(files):
                if os.path.splitext(fn)[1].lower() in allowed_exts:
                    files_to_scan.append(os.path.join(root, fn))

    # Compile word-boundary patterns for identifier tokens and substring patterns for multi-word phrases
    compiled_patterns: List[Tuple[str, re.Pattern[str]]] = []
    for ident in ids:
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", ident):
            pat = re.compile(rf"(?<![A-Za-z0-9_]){re.escape(ident)}(?![A-Za-z0-9_])", re.IGNORECASE)
        else:
            pat = re.compile(re.escape(ident), re.IGNORECASE)
        compiled_patterns.append((ident, pat))

    violations: List[Dict[str, Any]] = []
    for fp in files_to_scan:
        rel = os.path.relpath(fp, target) if os.path.isdir(target) else os.path.basename(fp)
        try:
            with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception:
            continue

        # Check Unicode stego / Trojan Source in generated code
        _, uni_traps, _ = sanitize_text(content, location=rel)
        for ut in uni_traps:
            if ut.get("reason") in ("unicode_bidi_override", "unicode_tag_block", "unicode_homoglyph"):
                violations.append(
                    {
                        "file": fp,
                        "rel_path": rel,
                        "line": 1,
                        "identifier": ut["reason"],
                        "snippet": ut.get("text", ""),
                        "reason": ut["reason"],
                    }
                )

        for lineno, line in enumerate(content.splitlines(), start=1):
            for ident, pat in compiled_patterns:
                if pat.search(line):
                    violations.append(
                        {
                            "file": fp,
                            "rel_path": rel,
                            "line": lineno,
                            "identifier": ident,
                            "snippet": line.strip()[:200],
                            "reason": "forbidden_identifier",
                        }
                    )

    return {
        "passed": len(violations) == 0,
        "code_dir": target,
        "scanned_files": files_to_scan,
        "checked_identifiers": ids,
        "violations": violations,
        "violation_count": len(violations),
    }


__all__ = [
    "TrapRecord",
    "SanitizationReport",
    "relative_luminance",
    "contrast_ratio",
    "parse_css_color",
    "sanitize_text",
    "extract_forbidden_identifiers",
    "detect_semantic_traps",
    "sanitize_pdf",
    "sanitize_image",
    "sanitize_svg",
    "sanitize_docx",
    "sanitize_pptx",
    "sanitize_xlsx",
    "sanitize_rtf",
    "sanitize_odf",
    "sanitize_zip",
    "audit_workspace_agent_rules",
    "sanitize_markup",
    "sanitize_ipynb",
    "sanitize_code",
    "sanitize_document",
    "audit_code_for_traps",
]
