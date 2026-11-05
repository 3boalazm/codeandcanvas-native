#!/usr/bin/env python3
# ============================================================================
#  Code & Canvas — «من فكرة لمنتج» campaign renderer · v2 (light)
#  ---------------------------------------------------------------------------
#  Design notes for v2 — the point of this pass is AIR:
#    · no grid, no corner ticks, no footer rules, no series dots: one logo,
#      one index, one 3px brand line — nothing else competes with the type
#    · three posts carry photography (duotoned into the brand palette),
#      two stay purely typographic so the set still feels designed, not stock
#    · two type sizes, one accent per post, one idea per frame
#
#  Brand: #00001E navy · violet/teal/pink gradient · Alexandria (display)
#         IBM Plex Sans Arabic (text) · Signate Grotesk / Poppins / Raleway
#  Shaping: HarfBuzz + FreeType (typeset.py). Requires pillow numpy fonttools
#           uharfbuzz freetype-py.
#  Usage:  python3 render.py [feed|story] [1..5]
# ============================================================================
import os
import sys
import numpy as np
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from PIL import Image, ImageDraw, ImageOps, ImageFilter, ImageEnhance

from typeset import Typesetter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
OUT = os.path.join(HERE, "assets")
BRAND = os.path.join(OUT, "brand")
PHOTOS = os.path.join(OUT, "photos")
CACHE = os.path.join(HERE, ".fontcache")
S = 2

# ---------------------------------------------------------------- tokens
NAVY = (0, 0, 30)
DEEP = (5, 6, 26)
INK = (245, 244, 255)
VIOLET = (139, 108, 255)
TEAL = (63, 214, 196)
PINK = (238, 91, 163)
GOLD = (243, 199, 122)
BRAND_GRAD = [TEAL, VIOLET, PINK]
W_ = (255, 255, 255)


def a(alpha):
    return (255, 255, 255, int(round(alpha * 255)))


# ---------------------------------------------------------------- fonts
AR_DIR = os.path.join(BRAND, "fonts")
LAT_DIR = os.path.join(ROOT, "assets", "fonts")

PATHS = {
    "display": ("vf", 800),
    "title": ("vf", 700),
    "lead": ("vf", 600),
    "body": (os.path.join(AR_DIR, "IBMPlexSansArabic-Regular.ttf"), None),
    "body-mid": (os.path.join(AR_DIR, "IBMPlexSansArabic-Medium.ttf"), None),
    "body-bold": (os.path.join(AR_DIR, "IBMPlexSansArabic-SemiBold.ttf"), None),
    "latin-label": (os.path.join(LAT_DIR, "Poppins-SemiBold.ttf"), None),
    "latin-mid": (os.path.join(LAT_DIR, "Poppins-Medium.ttf"), None),
    "latin-num": (os.path.join(LAT_DIR, "Raleway-ExtraBold.ttf"), None),
}


def prepare_fonts():
    os.makedirs(CACHE, exist_ok=True)
    vf = os.path.join(AR_DIR, "Alexandria-VF.ttf")
    for w in sorted({w for _, w in PATHS.values() if w}):
        dst = os.path.join(CACHE, f"Alexandria-{w}.ttf")
        if not os.path.exists(dst):
            instancer.instantiateVariableFont(TTFont(vf), {"wght": w}).save(dst)


def font_path(key):
    src, wght = PATHS[key]
    return os.path.join(CACHE, f"Alexandria-{wght}.ttf") if wght else src


# ---------------------------------------------------------------- board
class Board:
    def __init__(self, w, h, accent=TEAL):
        self.w, self.h = w, h
        self.W, self.H = w * S, h * S
        self.accent = accent
        self.img = Image.new("RGB", (self.W, self.H), NAVY)
        self.ts = Typesetter(S)
        self._grad = None
        self._d = ImageDraw.Draw(self.img, "RGBA")

    # ---------- background: two soft glows, nothing else ----------
    def background(self, seed=7):
        w, h = self.W, self.H
        y = np.linspace(0, 1, h)[:, None, None]
        x = np.linspace(0, 1, w)[None, :, None]
        base = np.array([11, 11, 42], float) * (1 - y) + np.array([2, 2, 11], float) * y
        for cx, cy, r, col, s in [
            (0.94, 0.02, 0.66, np.array(VIOLET), 0.40),
            (0.06, 0.96, 0.70, np.array(self.accent), 0.16),
            (0.30, 0.10, 0.50, np.array((79, 63, 216)), 0.20),
        ]:
            d = np.sqrt(((x - cx) * 0.88) ** 2 + (y - cy) ** 2) / r
            base = base + col[None, None, :] * (np.clip(1 - d, 0, 1) ** 2.2 * s)
        base = base + np.random.default_rng(seed).normal(0, 1.6, (h, w, 1))
        self.img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB")
        self._d = ImageDraw.Draw(self.img, "RGBA")

    # ---------- background: brand-duotoned photograph ----------
    def photo(self, path, scrim_from=0.34, scrim_to=0.98, exposure=0.86):
        im = Image.open(path).convert("RGB")
        scale = max(self.W / im.width, self.H / im.height)
        im = im.resize((int(im.width * scale) + 1, int(im.height * scale) + 1), Image.LANCZOS)
        im = ImageOps.fit(im, (self.W, self.H), Image.LANCZOS, centering=(0.5, 0.45))

        # duotone into the brand night palette, keeping a little of the original
        lum = im.convert("L")
        duo = ImageOps.colorize(lum, black=(7, 8, 28), white=(206, 198, 245))
        duo = ImageEnhance.Contrast(duo).enhance(1.06)
        im = Image.blend(duo, im, 0.18)
        im = ImageEnhance.Brightness(im).enhance(exposure)

        # a whisper of accent light in the shadows
        tint = Image.new("RGB", (self.W, self.H), self.accent)
        im = Image.blend(im, Image.blend(im, tint, 0.25), 0.16)

        # scrim: readable type at the bottom, readable logo at the top
        scrim = Image.new("L", (self.W, self.H), 0)
        sd = ImageDraw.Draw(scrim)
        top = int(self.H * scrim_from)
        for i in range(self.H - top):
            f = i / max(1, self.H - top)
            sd.line([(0, top + i), (self.W, top + i)],
                    fill=int(255 * (f ** 1.55) * scrim_to))
        topp = int(self.H * 0.16)
        for i in range(topp):
            sd.line([(0, i), (self.W, i)], fill=int(90 * (1 - i / topp)))
        dark = Image.new("RGB", (self.W, self.H), DEEP)
        im = Image.composite(dark, im, scrim)

        grain = np.random.default_rng(23).normal(0, 2.0, (self.H, self.W, 1))
        arr = np.clip(np.array(im, float) + grain, 0, 255).astype(np.uint8)
        self.img = Image.fromarray(arr, "RGB")
        self._d = ImageDraw.Draw(self.img, "RGBA")

    @property
    def d(self):
        return self._d

    # ---------- gradient ----------
    def gradient(self, span=None):
        if span is None and self._grad is not None:
            return self._grad
        cols = np.array(BRAND_GRAD, float)
        n = len(cols) - 1
        if span:
            t = np.clip((np.arange(self.W, dtype=float) - span[0]) /
                        max(1.0, span[1] - span[0]), 0, 1) * n
        else:
            t = np.linspace(0, n, self.W)
        i = np.clip(np.floor(t).astype(int), 0, n - 1)
        f = (t - i)[:, None]
        strip = cols[i] * (1 - f) + cols[i + 1] * f
        img = Image.fromarray(np.clip(np.tile(strip[None, :, :], (self.H, 1, 1)),
                                      0, 255).astype(np.uint8), "RGB")
        if span is None:
            self._grad = img
        return img

    # ---------- type ----------
    def _paint(self, mask, fill):
        if fill == "grad":
            box = mask.getbbox()
            self.img.paste(self.gradient((box[0], box[2]) if box else None), (0, 0), mask)
        else:
            alpha = (fill[3] / 255.0) if len(fill) == 4 else 1.0
            if alpha < 1:
                mask = mask.point(lambda v: int(v * alpha))
            self.img.paste(tuple(fill[:3]), (0, 0, self.W, self.H), mask)
        self._d = ImageDraw.Draw(self.img, "RGBA")

    def text(self, x, y, txt, key, size, fill, anchor="ra", tracking=0.0, base="rtl"):
        mask = self.ts.mask((self.W, self.H), x, y, txt, font_path(key), size,
                            anchor=anchor, tracking=tracking, base=base)
        self._paint(mask, fill)

    def ar(self, x, y, txt, key, size, fill, anchor="ra"):
        self.text(x, y, txt, key, size, fill, anchor=anchor, base="rtl")

    def latin(self, x, y, txt, key, size, fill, anchor="la", tracking=0.0):
        self.text(x, y, txt, key, size, fill, anchor=anchor, tracking=tracking, base="ltr")

    def grad_text(self, x, y, txt, key, size, anchor="ra", base="rtl", tracking=0.0):
        self.text(x, y, txt, key, size, "grad", anchor=anchor, tracking=tracking, base=base)

    def tw(self, txt, key, size, tracking=0.0, base="rtl"):
        return self.ts.width(txt, font_path(key), size, tracking, base)

    def fit(self, lines, key, base_size, max_w, floor=40):
        widest = max(self.tw(l, key, base_size) for l in lines)
        return max(floor, min(base_size, base_size * max_w / widest)) if widest else base_size

    # ---------- primitives ----------
    def rrect(self, box, radius, fill=None, outline=None, width=1):
        x0, y0, x1, y1 = [v * S for v in box]
        self.d.rounded_rectangle([x0, y0, x1, y1], radius=radius * S, fill=fill,
                                 outline=outline, width=max(1, int(width * S)))

    def rrect_grad(self, box, radius):
        x0, y0, x1, y1 = [int(round(v * S)) for v in box]
        bw, bh = max(1, x1 - x0), max(1, y1 - y0)
        mask = Image.new("L", (bw, bh), 0)
        r = max(0, min(int(radius * S), min(bw, bh) // 2))
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, bw - 1, bh - 1], radius=r, fill=255)
        self.img.paste(self.gradient().crop((x0, y0, x0 + bw, y0 + bh)), (x0, y0), mask)
        self._d = ImageDraw.Draw(self.img, "RGBA")

    def hline(self, x0, x1, y, color=None, width=1.2):
        self.d.line([(x0 * S, y * S), (x1 * S, y * S)], fill=color or a(.10),
                    width=max(1, int(width * S)))

    def dot(self, cx, cy, r, fill):
        self.d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=fill)

    def glow(self, cx, cy, r, color, strength=1.0):
        size = int(r * 9 * S)
        layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        for i in range(16, 0, -1):
            f = i / 16
            rr = r * S * (0.5 + 3.0 * f)
            ld.ellipse([size / 2 - rr, size / 2 - rr, size / 2 + rr, size / 2 + rr],
                       fill=color + (int(24 * strength * (1 - f) ** 1.7),))
        layer = layer.filter(ImageFilter.GaussianBlur(r * S * 0.45))
        self.img.paste(layer, (int(cx * S - size / 2), int(cy * S - size / 2)), layer)
        self._d = ImageDraw.Draw(self.img, "RGBA")

    def grad_bar(self, box, radius=2):
        x0, y0, x1, y1 = [int(round(v * S)) for v in box]
        bw, bh = max(1, x1 - x0), max(1, y1 - y0)
        mask = Image.new("L", (bw, bh), 0)
        r = max(0, min(int(radius * S), min(bw, bh) // 2))
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, bw - 1, bh - 1], radius=r, fill=255)
        self.img.paste(self.gradient().crop((x0, y0, x0 + bw, y0 + bh)), (x0, y0), mask)
        self._d = ImageDraw.Draw(self.img, "RGBA")

    # ---------- minimal brand chrome: logo, index, 3px line ----------
    def chrome(self, post):
        w, h, PAD = self.w, self.h, 84
        logo = Image.open(os.path.join(BRAND, "logo-white-h.png")).convert("RGBA")
        lh = 28
        lay = logo.resize((int(logo.width * (lh / logo.height) * S), lh * S), Image.LANCZOS)
        alpha = lay.getchannel("A").point(lambda v: int(v * 0.92))
        lay.putalpha(alpha)
        self.img.paste(lay, (int((w - PAD) * S - lay.width), int(64 * S)), lay)

        self.latin(PAD, 78, f"{post['n']:02d}", "latin-num", 22, a(.72), anchor="la")
        self.latin(PAD + 34, 77, "/05", "latin-mid", 11, a(.34), anchor="la", tracking=1.2)

        self.img.paste(self.gradient().resize((self.W, 3 * S), Image.BILINEAR),
                       (0, self.H - 3 * S))
        self._d = ImageDraw.Draw(self.img, "RGBA")


# ---------------------------------------------------------------- copy
#  head: [(line, style)] · support: one line · kind: photo | type
SERIES = [
    dict(n=1, accent=TEAL, kind="photo", photo="idea.jpg", device=None,
         kicker="الحقيقة الأولى",
         head=[("فكرتك مش وحشة.", "ink"), ("هي بس مش منتج.", "grad")],
         support="الفكرة تفضل فكرة لحد ما حد يدفع فيها.",
         cta=None),
    dict(n=2, accent=VIOLET, kind="type", photo=None, device="matrix",
         kicker="أغلى غلطة",
         head=[("تبني كل حاجة", "ink"), ("قبل ما تعرف مين هيدفع.", "grad")],
         support="20% من المميزات بتاخد 80% من قرار الشراء.",
         cta=None),
    dict(n=3, accent=GOLD, kind="type", photo=None, device="five",
         kicker="الطريقة",
         head=[("5 أسئلة قبل", "ink"), ("أول سطر كود.", "grad")],
         support="الإجابات دي بتحدد الشكل والنطاق والسعر.",
         cta=None),
    dict(n=4, accent=TEAL, kind="photo", photo="pharmacy.jpg", device=None,
         kicker="البرهان",
         head=[("14 موديول", "ink"), ("نزلوا كلهم شغالين.", "grad")],
         support="Pharmacy OS — نظام صيدليات متعدد الفروع، عربي RTL من الأول.",
         cta=None),
    dict(n=5, accent=PINK, kind="photo", photo="call.jpg", device=None,
         kicker="الخطوة الجاية",
         head=[("30 دقيقة", "grad"), ("تكفي تعرف", "ink"), ("فكرتك تستاهل.", "ink")],
         support="جلسة تشخيص مجانية، أونلاين، من غير عرض تقديمي.",
         cta="codeandcanvas.net/contact   ·   +20 109 250 0454"),
]

QUESTIONS = ["مين بيدفع فعلًا؟", "بيدفع في أنهي وجع؟", "إيه أقل نسخة تحله؟",
             "إزاي هنقيس نجاحها؟", "إيه اللي مش هنعمله؟"]


# ---------------------------------------------------------------- devices
def dev_matrix(b, cy, max_w):
    """20×5 build matrix — one row lit. Nothing else needs saying."""
    cell, gap, cols, rows = 34, 9, 20, 5
    gw = cols * cell + (cols - 1) * gap
    gh = rows * cell + (rows - 1) * gap
    x0 = b.w - 84 - gw
    y0 = cy - gh / 2
    for r in range(rows):
        for c in range(cols):
            x, y = x0 + c * (cell + gap), y0 + r * (cell + gap)
            if r == 0:
                b.rrect_grad((x, y, x + cell, y + cell), 7)
            else:
                b.rrect((x, y, x + cell, y + cell), 7, fill=(255, 255, 255, 6),
                        outline=a(.085), width=1)


def dev_five(b, cy, max_w):
    """The five questions: number + question. No sub-copy, no rules."""
    xr = b.w - 84
    row_h = 82
    y0 = cy - (row_h * len(QUESTIONS)) / 2 + 10
    for i, q in enumerate(QUESTIONS):
        y = y0 + i * row_h
        if i in (2, 4):
            b.grad_text(xr, y + 4, f"0{i+1}", "latin-num", 26, anchor="rs", base="ltr")
        else:
            b.latin(xr, y + 4, f"0{i+1}", "latin-num", 26, a(.26), anchor="rs")
        b.ar(xr - 58, y, q, "title", 36, INK, anchor="rs")


DEVICES = dict(matrix=dev_matrix, five=dev_five)
DEVICE_H = dict(matrix=252, five=424)


# ---------------------------------------------------------------- render
def render(post, fmt="feed"):
    w = 1080
    story = fmt == "story"
    h = 1920 if story else 1350
    PAD = 84
    max_w = w - 2 * PAD
    b = Board(w, h, accent=post["accent"])

    if post["kind"] == "photo":
        b.photo(os.path.join(PHOTOS, post["photo"]),
                scrim_from=0.30 if story else 0.33,
                scrim_to=0.99,
                exposure=0.90 if story else 0.88)
    else:
        b.background(seed=401 + post["n"] * 5)
        b.glow(w * 0.9, -60, 300, post["accent"], 1.0)

    b.chrome(post)

    hsize = b.fit([l for l, _ in post["head"]], "display",
                  106 if story else 94, max_w)
    lh = hsize * 1.34
    sup = 25 if story else 22
    cta_gap = 58 if post["cta"] else 0
    block = 46 + lh * len(post["head"]) + 30 + sup * 1.4 + cta_gap

    if post["kind"] == "photo":
        bottom = h - (246 if story else 112)
        top = bottom - block
    else:
        top = 470 if story else 356

    y = top
    b.ar(w - PAD, y, post["kicker"], "body-bold", 19, a(.55), anchor="ra")
    y += 46

    for line, style in post["head"]:
        if style == "grad":
            b.grad_text(w - PAD, y, line, "display", hsize)
        else:
            b.ar(w - PAD, y, line, "display", hsize, INK)
        y += lh

    y += 30
    b.ar(w - PAD, y, post["support"], "body", sup, a(.70), anchor="ra")

    if post["cta"]:
        y += cta_gap
        b.hline(w - PAD - 54, w - PAD, y - 16, a(.13), 1)
        b.latin(w - PAD, y + 12, post["cta"], "latin-mid", 13.5, a(.55),
                anchor="ra", tracking=0.8)
        y += 34

    if post["device"]:
        dh = DEVICE_H[post["device"]]
        field_top = y + (130 if story else 104)
        field_bottom = h - (230 if story else 150)
        cy = (field_top + field_bottom) / 2
        # keep the block inside the air it has, never on top of the type
        cy = max(cy, min(field_top + dh / 2 + 6, field_bottom - dh / 2))
        DEVICES[post["device"]](b, cy, max_w)

    os.makedirs(os.path.join(OUT, fmt), exist_ok=True)
    path = os.path.join(OUT, fmt, f"{post['n']:02d}.png")
    b.img.resize((w, h), Image.LANCZOS).save(path, optimize=True)
    print(f"→ {os.path.relpath(path, ROOT)}  {os.path.getsize(path)//1024} KB  "
          f"(head {hsize:.0f}px · block {top:.0f}-{y:.0f})")


def main():
    prepare_fonts()
    args = [x.lower() for x in sys.argv[1:]]
    fmts, only = ["feed", "story"], None
    for x in args:
        if x in ("feed", "story"):
            fmts = [x]
        elif x.isdigit():
            only = int(x)
    for fmt in fmts:
        for post in SERIES:
            if only and post["n"] != only:
                continue
            render(post, fmt)


if __name__ == "__main__":
    main()
