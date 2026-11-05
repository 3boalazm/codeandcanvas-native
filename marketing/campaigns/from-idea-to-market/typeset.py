#!/usr/bin/env python3
# ============================================================================
#  typeset.py — real text shaping + rasterising for the campaign renderer
#  ---------------------------------------------------------------------------
#  Pillow's own text engine has no OpenType support: Arabic falls back to
#  Unicode presentation forms and breaks (final waw / qaf / jeem come out as
#  tofu). This module shapes text with HarfBuzz (real GSUB/GPOS, lam-alef
#  ligatures, correct joining) and rasterises the glyphs with FreeType,
#  returning an 8-bit mask the renderer fills with a colour or the brand
#  gradient.
#
#  A light bidi pass splits a paragraph into Arabic (RTL) and Latin/digit (LTR)
#  runs and composes them in the paragraph's base direction, so
#  "Pharmacy OS: نظام صيدليات" and "نسخة MVP" both read correctly.
# ============================================================================
import re
import freetype
import uharfbuzz as hb
from PIL import Image

ARABIC = re.compile(r"[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]")
LATIN = re.compile(r"[A-Za-z0-9@#&%+\-\u2013\u00b7.,:;/()\[\]'\"]")
NEUTRAL = " \u00a0\u200f\u200e"
AR_PUNCT = "\u060c\u061b\u061f"


def tokenize(text):
    """Split into [('sp', ' ') | ('ar'|'lat', phrase)] tokens.

    Adjacent words of the same script are merged into one run (with their
    spaces) so a Latin phrase inside an Arabic sentence — "Pharmacy OS" —
    keeps its own left-to-right order instead of being flipped word by word.
    Whitespace between two different scripts stays a plain advance, which
    keeps mixed lines correctly spaced.
    """
    tokens = []
    for chunk in re.split(r"(\s+)", text):
        if not chunk:
            continue
        if chunk.isspace():
            tokens.append(("sp", " "))
            continue
        kind = "ar" if ARABIC.search(chunk) else "lat"
        if (len(tokens) >= 2 and tokens[-1][0] == "sp"
                and tokens[-2][0] == kind):
            tokens[-1] = (kind, " ")
            tokens.pop()
            tokens.append((kind, tokens.pop()[1] + " " + chunk))
        else:
            tokens.append((kind, chunk))
    return tokens


class Typesetter:
    """Shapes + rasterises text with the exact fonts the artwork needs."""

    def __init__(self, scale=2):
        self.scale = scale
        self._hb = {}
        self._ft = {}

    # ---------- resources ----------
    def _resources(self, path, dpx):
        dpx = max(4, int(round(dpx)))
        key = (path, dpx)
        if key not in self._hb:
            with open(path, "rb") as fh:
                data = fh.read()
            face = hb.Face(data)
            font = hb.Font(face)
            ftf = freetype.Face(path)
            ftf.set_char_size(dpx * 64)
            self._hb[key] = font
            self._ft[key] = ftf
        return self._hb[key], self._ft[key]

    def metrics(self, path, dpx):
        _, ftf = self._resources(path, dpx)
        return ftf.size.ascender / 64.0, ftf.size.descender / 64.0

    # ---------- shaping ----------
    def shape_run(self, text, path, dpx, tracking=0.0):
        """Return ([(gid, dx, dy)], width) — all values in device px."""
        font, _ = self._resources(path, dpx)
        k = dpx / font.face.upem
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(font, buf, {"kern": True, "liga": True})
        glyphs, x = [], 0.0
        for i, (info, pos) in enumerate(zip(buf.glyph_infos, buf.glyph_positions)):
            glyphs.append((info.codepoint, x + pos.x_offset * k, pos.y_offset * k))
            x += pos.x_advance * k + (tracking if i < len(buf.glyph_infos) - 1 else 0)
        return glyphs, x

    def layout(self, text, path, dpx, tracking=0.0, base="rtl"):
        """Compose tokens in the paragraph base direction. Returns glyphs + width."""
        tokens = tokenize(text)
        if not tokens:
            return [], 0.0
        space_w = self.shape_run(" ", path, dpx)[1] + tracking * 1.7
        glyphs = []
        total = 0.0
        placed = []
        for kind, chunk in tokens:
            if kind == "sp":
                placed.append(("sp", None, space_w))
                total += space_w
            else:
                gl, w = self.shape_run(chunk, path, dpx, tracking if kind == "lat" else 0.0)
                placed.append((kind, gl, w))
                total += w
        if base == "rtl":
            x = total
            for kind, gl, w in placed:
                if kind == "sp":
                    x -= w
                    continue
                x -= w
                for gid, dx, dy in gl:
                    glyphs.append((gid, x + dx, dy))
        else:
            x = 0.0
            for kind, gl, w in placed:
                if kind != "sp":
                    for gid, dx, dy in gl:
                        glyphs.append((gid, x + dx, dy))
                x += w
        return glyphs, total

    # ---------- rasterising ----------
    def mask(self, canvas, x, y, text, path, px, anchor="ra", tracking=0.0, base="rtl"):
        """Draw text into a full-canvas 8-bit mask.

        x, y, px and tracking are in design units; the mask is in device px.
        anchor = [l|m|r] + [a (ascender top) | s (baseline) | m (cap middle)].
        """
        W, H = canvas
        img = Image.new("L", (W, H), 0)
        dpx = px * self.scale
        glyphs, width = self.layout(text, path, dpx, tracking * self.scale, base)
        if not glyphs:
            return img
        ascent, descent = self.metrics(path, dpx)
        ox = x * self.scale
        if anchor[0] == "r":
            ox -= width
        elif anchor[0] == "m":
            ox -= width / 2
        oy = y * self.scale
        if anchor[1] == "a":
            oy += ascent
        elif anchor[1] == "m":
            oy += (ascent + descent) / 2
        _, ftf = self._resources(path, dpx)
        flags = freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_NORMAL | freetype.FT_LOAD_NO_HINTING
        for gid, gx, gy in glyphs:
            try:
                ftf.load_glyph(gid, flags)
            except Exception:
                continue
            bm = ftf.glyph.bitmap
            if bm.width == 0 or bm.rows == 0:
                continue
            buf = bytes(bytearray(bm.buffer))
            pitch = abs(bm.pitch)
            if pitch != bm.width:
                buf = b"".join(buf[r * pitch: r * pitch + bm.width] for r in range(bm.rows))
            g = Image.frombytes("L", (bm.width, bm.rows), buf)
            gx_ = int(round(ox + gx + ftf.glyph.bitmap_left))
            gy_ = int(round(oy - gy - ftf.glyph.bitmap_top))
            if gx_ + g.width < 0 or gy_ + g.height < 0 or gx_ > W or gy_ > H:
                continue
            img.paste(g, (gx_, gy_), g)
        return img

    def width(self, text, path, px, tracking=0.0, base="rtl"):
        _, w = self.layout(text, path, px * self.scale, tracking * self.scale, base)
        return w / self.scale
