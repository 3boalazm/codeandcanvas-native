#!/usr/bin/env python3
# ============================================================================
#  Code & Canvas — «الفاتورة التانية» campaign renderer
#  ---------------------------------------------------------------------------
#  A different idea AND a different visual system from «من فكرة لمنتج»:
#    · split composition — type lives on a quiet near-black panel on top,
#      photography owns the bottom band, and a 3px brand gradient is the
#      only thing sitting on the seam
#    · type is bigger and tighter than the first campaign (display ~116/130px
#      at 1.12 leading) — the words are the artwork, not the layout
#    · warm duotone (bone + accent) instead of the cool violet/teal duotone,
#      so the two campaigns read as siblings, not repeats
#    · one device only (the invoice ledger) on the single typographic post
#
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
INK = (247, 245, 255)
VIOLET = (139, 108, 255)
TEAL = (63, 214, 196)
PINK = (238, 91, 163)
GOLD = (243, 199, 122)
BRAND_GRAD = [TEAL, VIOLET, PINK]
PANEL_TOP = (10, 10, 30)
PANEL_BOT = (3, 3, 10)
PHOTO_BLACK = (9, 7, 12)
PHOTO_WHITE = (236, 224, 198)
PAD = 76


def a(alpha):
    return (255, 255, 255, int(round(alpha * 255)))


# ---------------------------------------------------------------- fonts
AR_DIR = os.path.join(BRAND, "fonts")
LAT_DIR = os.path.join(ROOT, "assets", "fonts")

PATHS = {
    "display": ("vf", 800),
    "title": ("vf", 700),
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
    def __init__(self, w, h, accent=GOLD):
        self.w, self.h = w, h
        self.W, self.H = w * S, h * S
        self.accent = accent
        self.img = Image.new("RGB", (self.W, self.H), PANEL_BOT)
        self.ts = Typesetter(S)
        self._grad = None
        self._d = ImageDraw.Draw(self.img, "RGBA")

    @property
    def d(self):
        return self._d

    # ---------- the quiet panel the type sits on ----------
    def panel(self, seed=11, glow=0.34):
        w, h = self.W, self.H
        y = np.linspace(0, 1, h)[:, None, None]
        x = np.linspace(0, 1, w)[None, :, None]
        base = np.array(PANEL_TOP, float) * (1 - y) + np.array(PANEL_BOT, float) * y
        d = np.sqrt(((x - 0.92) * 0.9) ** 2 + (y + 0.06) ** 2) / 0.62
        base = base + np.array(self.accent)[None, None, :] * (np.clip(1 - d, 0, 1) ** 2.4 * glow)
        base = base + np.random.default_rng(seed).normal(0, 1.4, (h, w, 1))
        self.img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB")
        self._d = ImageDraw.Draw(self.img, "RGBA")

    # ---------- photography: a band at the bottom, warm duotone ----------
    def photo_band(self, path, y0, y1, focus=0.5):
        bh = int((y1 - y0) * S)
        im = Image.open(path).convert("RGB")
        scale = max(self.W / im.width, bh / im.height)
        im = im.resize((int(im.width * scale) + 1, int(im.height * scale) + 1), Image.LANCZOS)
        im = ImageOps.fit(im, (self.W, bh), Image.LANCZOS, centering=(0.5, focus))

        lum = im.convert("L")
        duo = ImageOps.colorize(lum, black=PHOTO_BLACK, white=PHOTO_WHITE)
        duo = ImageEnhance.Contrast(duo).enhance(1.08)
        im = Image.blend(duo, im, 0.22)
        im = ImageEnhance.Brightness(im).enhance(0.94)
        tint = Image.new("RGB", im.size, self.accent)
        im = Image.blend(im, Image.blend(im, tint, 0.22), 0.13)

        # the band melts into the panel at the top, and into night at the base
        scrim = Image.new("L", (self.W, bh), 0)
        sd = ImageDraw.Draw(scrim)
        fh = int(bh * 0.40)
        for i in range(fh):
            sd.line([(0, i), (self.W, i)], fill=int(255 * (1 - i / fh) ** 1.7))
        tail = int(bh * 0.18)
        for i in range(tail):
            sd.line([(0, bh - 1 - i), (self.W, bh - 1 - i)],
                    fill=int(140 * (1 - i / tail) ** 1.5))
        im = Image.composite(Image.new("RGB", im.size, PANEL_BOT), im, scrim)

        grain = np.random.default_rng(31).normal(0, 2.0, (bh, self.W, 1))
        arr = np.clip(np.array(im, float) + grain, 0, 255).astype(np.uint8)
        self.img.paste(Image.fromarray(arr, "RGB"), (0, int(y0 * S)))
        self._d = ImageDraw.Draw(self.img, "RGBA")

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

    def hline(self, x0, x1, y, color=None, width=1.0):
        self.d.line([(x0 * S, y * S), (x1 * S, y * S)], fill=color or a(.10),
                    width=max(1, int(width * S)))

    def seam(self, y, thickness=3):
        self.img.paste(self.gradient().resize((self.W, thickness * S), Image.BILINEAR),
                       (0, int(y * S)))
        self._d = ImageDraw.Draw(self.img, "RGBA")

    # ---------- chrome: wordmark + index, nothing else ----------
    def chrome(self, post):
        logo = Image.open(os.path.join(BRAND, "logo-white-h.png")).convert("RGBA")
        lh = 26
        lay = logo.resize((int(logo.width * (lh / logo.height) * S), lh * S), Image.LANCZOS)
        lay.putalpha(lay.getchannel("A").point(lambda v: int(v * 0.90)))
        self.img.paste(lay, (int((self.w - PAD) * S - lay.width), int(58 * S)), lay)

        self.latin(PAD, 62, f"{post['n']:02d}", "latin-num", 21, a(.75), anchor="la")
        self.latin(PAD + 34, 61, "/05", "latin-mid", 10.5, a(.32), anchor="la", tracking=1.2)
        self._d = ImageDraw.Draw(self.img, "RGBA")


# ---------------------------------------------------------------- copy
#  head: [(line, style)] — style "grad" paints the brand gradient
LEDGER = [
    ("01", "إعادة بناء", "أول ما تكبر، هتبني تاني."),
    ("02", "نقل بيانات", "الترحيل بيوقف الشغل."),
    ("03", "فريق جديد", "كل حد يفهم من الأول."),
]

SERIES = [
    dict(n=1, accent=GOLD, kind="photo", photo="receipt.jpg", focus=0.55,
         kicker="الفاتورة الأولى",
         head=[("الرخيص", "ink"), ("مش رخيص.", "grad")],
         support="ده أول قسط. الباقي بيتدفع بعدين.", cta=None),
    dict(n=2, accent=GOLD, kind="type", device="ledger",
         kicker="التفصيل",
         head=[("3 فواتير", "ink"), ("بتوصل بعدين.", "grad")],
         support="التوفير بيتبدّل بتكلفة أكبر، متأخرة، ومفاجئة.", cta=None),
    dict(n=3, accent=VIOLET, kind="photo", photo="patch.jpg", focus=0.5,
         kicker="الترقيع",
         head=[("كل ترقيع", "ink"), ("بيغلي اللي بعده.", "grad")],
         support="الكود اللي مش متصمّم: كل إضافة فيه بتطلب وقت أكتر من اللي قبلها.",
         cta=None),
    dict(n=4, accent=TEAL, kind="photo", photo="rebuild.jpg", focus=0.5, seam_extra=62,
         kicker="المقارنة",
         head=[("الأغلى", "ink"), ("إنك تعمله", "ink"), ("مرتين.", "grad")],
         support="مرة رخيصة، ومرة صح. الاتنين بيتحاسبوا.", cta=None),
    dict(n=5, accent=PINK, kind="photo", photo="review.jpg", focus=0.45,
         kicker="الخطوة الجاية",
         head=[("قبل ما تدفع", "ink"), ("المرة التانية.", "grad")],
         support="ابعتلنا اللي بنيته. هنقولك إيه اللي هيغلي بعد كده.",
         cta="codeandcanvas.net/contact   ·   +20 109 250 0454"),
]


# ---------------------------------------------------------------- devices
def dev_ledger(b, top, bottom, max_w):
    """Three invoices: number as a left column, the line itself on the right."""
    story = b.h > 1500
    title_s, sub_s = (54, 24) if story else (46, 21)
    row_h = max(150, min(300 if story else 240, (bottom - top) / len(LEDGER)))
    y = top + max(0, (bottom - top - row_h * len(LEDGER)) / 2)
    for num, title, sub in LEDGER:
        b.hline(PAD, b.w - PAD, y, a(.10), 1)
        b.latin(PAD, y + row_h / 2 - 24, num, "latin-num", 40, a(.20), anchor="la")
        ty = y + max(18, (row_h - (title_s * 1.25 + sub_s * 1.6)) / 2)
        b.ar(b.w - PAD, ty, title, "title", title_s, INK, anchor="ra")
        b.ar(b.w - PAD, ty + title_s * 1.42, sub, "body", sub_s, a(.52), anchor="ra")
        y += row_h
    b.hline(PAD, b.w - PAD, y, a(.10), 1)


DEVICES = dict(ledger=dev_ledger)


# ---------------------------------------------------------------- render
def render(post, fmt="feed"):
    w = 1080
    story = fmt == "story"
    h = 1920 if story else 1350
    seam_y = (880 if story else 600) + post.get("seam_extra", 0)
    max_w = w - 2 * PAD
    b = Board(w, h, accent=post["accent"])
    b.panel(seed=901 + post["n"] * 7, glow=0.30)
    if post["kind"] == "photo":
        b.photo_band(os.path.join(PHOTOS, post["photo"]), seam_y, h,
                     focus=post.get("focus", 0.5))
    b.chrome(post)
    if post["kind"] == "photo":
        b.seam(seam_y, 3)

    # ---- type block, bottom-anchored to the seam (panel) or flowing (type post)
    head = [l for l, _ in post["head"]]
    cap = 130 if story else 116
    sup = 26 if story else 23
    kick = 40 if story else 34
    gap_sup = 52 if story else 44
    cta_gap = 62 if post["cta"] else 0

    size = b.fit(head, "display", cap, max_w)
    while True:
        lh = size * 1.12
        block = kick + lh * len(head) + gap_sup + sup * 1.45 + cta_gap
        if post["kind"] == "photo":
            floor_top = 176 if story else 136
            avail = (seam_y - 46) - floor_top
        else:
            avail = (h - 300) - (300 if story else 250)
        if block <= avail or size <= 54:
            break
        size -= 2
    lh = size * 1.12

    if post["kind"] == "photo":
        top = seam_y - 46 - block
    else:
        top = (300 if story else 250)

    y = top
    b.ar(w - PAD, y, post["kicker"], "body-bold", 18, a(.48), anchor="ra")
    y += kick

    for line, style in post["head"]:
        if style == "grad":
            b.grad_text(w - PAD, y, line, "display", size)
        else:
            b.ar(w - PAD, y, line, "display", size, INK)
        y += lh

    y += gap_sup
    b.ar(w - PAD, y, post["support"], "body", sup, a(.62), anchor="ra")
    y += sup * 1.45

    if post["cta"]:
        y += cta_gap - 10
        b.latin(w - PAD, y, post["cta"], "latin-mid", 13.5, a(.52),
                anchor="ra", tracking=0.8)
        y += 20

    if post.get("device"):
        DEVICES[post["device"]](b, y + 74, h - (210 if story else 130), max_w)

    os.makedirs(os.path.join(OUT, fmt), exist_ok=True)
    path = os.path.join(OUT, fmt, f"{post['n']:02d}.png")
    b.img.resize((w, h), Image.LANCZOS).save(path, optimize=True)
    print(f"→ {os.path.relpath(path, ROOT)}  {os.path.getsize(path)//1024} KB  "
          f"(head {size:.0f}px · block {top:.0f}-{y:.0f} · seam {seam_y})")


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
