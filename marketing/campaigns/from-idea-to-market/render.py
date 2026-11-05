#!/usr/bin/env python3
# ============================================================================
#  Code & Canvas — «من فكرة لمنتج» campaign renderer
#  ---------------------------------------------------------------------------
#  Brand-locked feed (1080×1350) + story (1080×1920) artwork for the 5-post
#  campaign, built on the studio's real identity:
#
#    canvas ....... #00001E navy · violet/teal/pink brand gradient · hairline
#                   frame · 90px grid · chromatic glow · film grain
#    Arabic ....... Alexandria (display) · IBM Plex Sans Arabic (text)
#    Latin ........ Signate Grotesk · Poppins · Raleway
#    lockup ....... the site's licensed wordmark (rasterised from brand SVG)
#    shaping ...... HarfBuzz + FreeType via typeset.py — real GSUB, correct
#                   joining and correct bidi for mixed Arabic/Latin lines
#
#  Requires: pillow numpy fonttools uharfbuzz freetype-py
#  Usage:    python3 render.py [feed|story] [1..5]
# ============================================================================
import os
import sys
import numpy as np
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from PIL import Image, ImageDraw, ImageFilter

from typeset import Typesetter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
OUT = os.path.join(HERE, "assets")
BRAND = os.path.join(OUT, "brand")
CACHE = os.path.join(HERE, ".fontcache")
S = 2  # supersampling factor

# ---------------------------------------------------------------- brand tokens
NAVY = (0, 0, 30)
INK = (245, 244, 255)
VIOLET = (139, 108, 255)
TEAL = (63, 214, 196)
PINK = (238, 91, 163)
GOLD = (243, 199, 122)
INDIGO = (79, 63, 216)
BRAND_GRAD = [TEAL, VIOLET, PINK]
W_ = (255, 255, 255)


def a(alpha):
    """White at a given opacity — how the brand tints secondary type."""
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
    "latin-display": (os.path.join(LAT_DIR, "signategrotesk-black.ttf"), None),
    "latin-label": (os.path.join(LAT_DIR, "Poppins-SemiBold.ttf"), None),
    "latin-mid": (os.path.join(LAT_DIR, "Poppins-Medium.ttf"), None),
    "latin-num": (os.path.join(LAT_DIR, "Raleway-ExtraBold.ttf"), None),
}


def prepare_fonts():
    """Instance Alexandria's variable axis into the weights the artwork uses."""
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

    # ---------- background ----------
    def background(self, seed=7):
        w, h = self.W, self.H
        y = np.linspace(0, 1, h)[:, None, None]
        x = np.linspace(0, 1, w)[None, :, None]
        base = np.array([10, 10, 40], float) * (1 - y) + np.array([2, 2, 12], float) * y
        for cx, cy, r, col, s in [
            (0.92, 0.04, 0.60, np.array(VIOLET), 0.44),
            (0.06, 0.92, 0.70, np.array(TEAL), 0.20),
            (0.78, 0.70, 0.50, np.array(self.accent), 0.12),
            (0.12, 0.16, 0.44, np.array(INDIGO), 0.30),
        ]:
            d = np.sqrt(((x - cx) * 0.86) ** 2 + (y - cy) ** 2) / r
            base = base + col[None, None, :] * (np.clip(1 - d, 0, 1) ** 2.1 * s)
        dx, dy = (x - 0.5) * 0.9, y - 0.46
        base = base * (1 - 0.42 * np.clip(np.sqrt(dx ** 2 + dy ** 2) / 0.80, 0, 1) ** 2)
        base = base + np.random.default_rng(seed).normal(0, 2.3, (h, w, 1))
        self.img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB")
        ov = Image.new("RGBA", (self.W, self.H), (0, 0, 0, 0))
        g = ImageDraw.Draw(ov)
        step = 90 * S
        for gx in range(0, self.W + step, step):
            g.line([(gx, 0), (gx, self.H)], fill=(255, 255, 255, 7), width=S)
        for gy in range(0, self.H + step, step):
            g.line([(0, gy), (self.W, gy)], fill=(255, 255, 255, 7), width=S)
        self.img = Image.alpha_composite(self.img.convert("RGBA"), ov).convert("RGB")
        self._d = ImageDraw.Draw(self.img, "RGBA")

    @property
    def d(self):
        return self._d

    def gradient(self, span=None):
        """Brand gradient across the canvas — or across one line's own box."""
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

    def fit(self, lines, key, base_size, max_w, floor=44):
        widest = max(self.tw(l, key, base_size) for l in lines)
        return max(floor, min(base_size, base_size * max_w / widest)) if widest else base_size

    # ---------- primitives ----------
    def rrect(self, box, radius, fill=None, outline=None, width=1):
        x0, y0, x1, y1 = [v * S for v in box]
        self.d.rounded_rectangle([x0, y0, x1, y1], radius=radius * S, fill=fill,
                                 outline=outline, width=max(1, int(width * S)))

    def hline(self, x0, x1, y, color=None, width=1.2):
        self.d.line([(x0 * S, y * S), (x1 * S, y * S)], fill=color or a(.10),
                    width=max(1, int(width * S)))

    def dashed(self, x0, x1, y, color=None, dash=6, gap=11, width=1.6):
        x = x0
        while x < x1:
            self.d.line([(x * S, y * S), (min(x + dash, x1) * S, y * S)],
                        fill=color or a(.24), width=max(1, int(width * S)))
            x += dash + gap

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
                       fill=color + (int(26 * strength * (1 - f) ** 1.7),))
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

    def rrect_grad(self, box, radius):
        x0, y0, x1, y1 = [int(round(v * S)) for v in box]
        bw, bh = max(1, x1 - x0), max(1, y1 - y0)
        mask = Image.new("L", (bw, bh), 0)
        r = max(0, min(int(radius * S), min(bw, bh) // 2))
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, bw - 1, bh - 1], radius=r, fill=255)
        self.img.paste(self.gradient().crop((x0, y0, x0 + bw, y0 + bh)), (x0, y0), mask)
        self._d = ImageDraw.Draw(self.img, "RGBA")

    # ---------- brand chrome ----------
    def chrome(self, post, story=False):
        w, h, PAD = self.w, self.h, 76
        accent = post["accent"]
        logo = Image.open(os.path.join(BRAND, "logo-white-h.png")).convert("RGBA")
        lh = 33
        lay = logo.resize((int(logo.width * (lh / logo.height) * S), lh * S), Image.LANCZOS)
        self.img.paste(lay, (int((w - PAD) * S - lay.width), int(84 * S)), lay)

        # index block (left)
        self.latin(PAD, 132, f"{post['n']:02d}", "latin-num", 30, a(.92), anchor="ls")
        self.latin(PAD + 46, 131, "/ 05", "latin-mid", 14, a(.42), anchor="ls", tracking=1.4)
        self.d.rectangle([PAD * S, 146 * S, (PAD + 72) * S, 147 * S], fill=accent + (120,))
        self.latin(PAD, 158, "FROM IDEA TO MARKET", "latin-mid", 11, a(.40), anchor="la", tracking=2.4)

        # kicker pill (RTL start)
        pad_x, gap = 17, 13
        ar_w = self.tw(post["kicker_ar"], "body-bold", 21)
        en_w = self.tw(post["kicker_en"], "latin-label", 12.5, 2.2, "ltr")
        box_w = pad_x * 2 + 9 + gap + ar_w + gap + en_w
        x1, top = w - PAD, 208
        self.rrect((x1 - box_w, top, x1, top + 44), 22, fill=(255, 255, 255, 14),
                   outline=(255, 255, 255, 34), width=1)
        self.dot(x1 - pad_x - 3, top + 22, 4, accent + (255,))
        self.ar(x1 - pad_x - 14, top + 22, post["kicker_ar"], "body-bold", 21, INK, anchor="rm")
        self.latin(x1 - box_w + pad_x, top + 22, post["kicker_en"], "latin-label", 12.5,
                   a(.48), anchor="lm", tracking=2.2)

        # footer
        fy = h - (214 if story else 96)
        self.hline(PAD, w - PAD, fy - 30, a(.08), 1)
        self.latin(PAD, fy, "codeandcanvas.net", "latin-mid", 15.5, a(.58), anchor="la", tracking=0.4)
        self.ar(w - PAD, fy, "من فكرة لمنتج", "body-bold", 17.5, a(.62), anchor="ra")
        cx = w / 2 - 44
        for i in range(5):
            x = cx + (4 - i) * 22
            if i + 1 == post["n"]:
                self.grad_bar((x - 5, fy - 8, x + 5, fy + 2), radius=5)
            else:
                self.dot(x, fy - 3, 3.1, a(.22))

        # bottom edge accent + hairline frame with corner ticks
        self.img.paste(self.gradient().resize((self.W, 5 * S), Image.BILINEAR),
                       (0, self.H - 5 * S))
        self._d = ImageDraw.Draw(self.img, "RGBA")
        IN = 30
        self.d.rounded_rectangle([IN * S, IN * S, self.W - IN * S, self.H - IN * S],
                                 radius=26 * S, outline=a(.09), width=S)
        for cx_, cy_, sx, sy in [(IN, IN, 1, 1), (w - IN, IN, -1, 1),
                                 (IN, h - IN, 1, -1), (w - IN, h - IN, -1, -1)]:
            self.d.line([(cx_ * S, cy_ * S), ((cx_ + 24 * sx) * S, cy_ * S)],
                        fill=accent + (170,), width=2 * S)
            self.d.line([(cx_ * S, cy_ * S), (cx_ * S, (cy_ + 24 * sy) * S)],
                        fill=accent + (170,), width=2 * S)


# ---------------------------------------------------------------- copy
SERIES = [
    dict(
        n=1, quote="الفجوة مش في الفكرة… الفجوة في إن حد يدفع فيها.", accent=TEAL, device="gap",
        kicker_ar="الحقيقة الأولى", kicker_en="THE GAP",
        head=[("فكرتك مش وحشة.", "ink"), ("هي بس مش منتج.", "grad")],
        head_size=100,
        body=["الفكرة تفضل فكرة لحد ما حد يدفع فيها.", "قبل كده هي مجرد تخمين حلو."],
        en="UNTIL SOMEONE PAYS FOR IT, AN IDEA IS ONLY A GOOD GUESS",
    ),
    dict(
        n=2, quote="كل ميزة زيادة قبل أول عميل = ميزانية بتتحول لتخمين.", accent=VIOLET, device="twenty",
        kicker_ar="أغلى غلطة", kicker_en="THE EXPENSIVE MISTAKE",
        head=[("تبني المنتج كله", "ink"), ("قبل ما تعرف", "ink"), ("مين هيدفع.", "grad")],
        head_size=84,
        body=["20% من المميزات بتاخد 80% من قرار الشراء.",
              "ابدأ بيها، والباقي يستنى السوق يقول كلمته."],
        en="SHIP THE 20% THAT CARRIES THE DECISION",
    ),
    dict(
        n=3, quote="السؤال مش «إيه اللي نبنيه»… السؤال «مين بيدفع، وليه».", accent=GOLD, device="five",
        kicker_ar="الطريقة", kicker_en="THE METHOD",
        head=[("5 أسئلة قبل", "ink"), ("أول سطر كود.", "grad")],
        head_size=96,
        body=["الإجابات دي بتحدد الشكل والنطاق والسعر.", "قبل أي التزام، وقبل أي فلوس."],
        en="FIVE QUESTIONS FIRST — EVERYTHING AFTER IS EXECUTION",
    ),
    dict(
        n=4, quote="14 موديول مش الرقم الكبير. الكبير إن كل واحد فيهم شغال.", accent=TEAL, device="modules",
        kicker_ar="البرهان", kicker_en="THE PROOF",
        head=[("14 موديول", "ink"), ("نزلوا كلهم شغالين.", "grad")],
        head_size=90,
        body=["نظام صيدليات متعدد الفروع، عربي RTL من الأول،",
              "وكل موديول كان شغال في نفس الأسبوع اللي نزل فيه."],
        en="PHARMACY OS · 2024–2026 · 14 MODULES, EACH USABLE THE WEEK IT LANDED",
    ),
    dict(
        n=5, quote="30 دقيقة. من غير عرض تقديمي (Pitch). وقرار واحد تخرج بيه.", accent=PINK, device="cta",
        kicker_ar="الخطوة الجاية", kicker_en="THE NEXT MOVE",
        head=[("30 دقيقة", "grad"), ("تكفي تعرف", "ink"), ("فكرتك تستاهل.", "ink")],
        head_size=86,
        body=["جلسة تشخيص مجانية، أونلاين، من غير عرض تقديمي.",
              "بتخرج منها بقرار، مش بمجاملات."],
        en="A FREE 30-MINUTE IDEA DIAGNOSTIC — YOU LEAVE WITH A DECISION",
    ),
]

MODULES = ["كاشير", "فواتير", "مخزون", "استلام", "روشتات", "عملاء", "ورديات",
           "تقارير", "مرتجعات", "أسعار", "فروع", "صلاحيات", "تنبيهات", "جرد"]

QUESTIONS = [
    ("مين بيدفع فعلًا؟", "العميل اللي عنده ميزانية وقرار"),
    ("بيدفع في أنهي وجع؟", "الوجع الغالي، مش الوجع المزعج"),
    ("إيه أقل نسخة تحله؟", "أقل نطاق يوصل لقيمة حقيقية"),
    ("إزاي هنقيس نجاحها؟", "مؤشر واحد، رقم واحد، من الأول"),
    ("إيه اللي مش هنعمله؟", "الحدود هي اللي بتحمي الميزانية"),
]


# ---------------------------------------------------------------- devices
def dev_gap(b, cy, max_w):
    """فكرة ←→ سوق: the distance ideas die in (read right to left)."""
    accent, PAD = b.accent, 76
    xr, xl = PAD, b.w - PAD
    mid = (xr + xl) / 2
    gap = 250

    b.hline(xr + 74, mid - gap / 2, cy, a(.14), 1.6)
    b.hline(mid + gap / 2, xl - 70, cy, a(.14), 1.6)
    b.dashed(mid - gap / 2, mid + gap / 2, cy, a(.30), 6, 12, 1.6)

    # the idea, in your head (right node)
    b.glow(xl - 34, cy, 30, accent, 1.25)
    b.d.ellipse([(xl - 34 - 27) * S, (cy - 27) * S, (xl - 34 + 27) * S, (cy + 27) * S],
                outline=accent + (120,), width=1)
    b.dot(xl - 34, cy, 13, accent + (255,))
    b.dot(xl - 34, cy, 4, W_ + (255,))
    b.ar(xl, cy - 58, "فكرة", "display", 58, INK, anchor="rs")
    b.ar(xl, cy + 76, "في دماغك", "body-mid", 21, a(.40), anchor="ra")

    # the market, which decides (left node)
    b.glow(xr + 34, cy, 32, PINK, 1.0)
    b.d.ellipse([(xr + 34 - 30) * S, (cy - 30) * S, (xr + 34 + 30) * S, (cy + 30) * S],
                outline=PINK + (120,), width=1)
    b.dot(xr + 34, cy, 15, PINK + (255,))
    b.dot(xr + 34, cy, 4, W_ + (255,))
    b.ar(xr, cy - 58, "سوق", "display", 58, INK, anchor="ls")
    b.ar(xr, cy + 76, "بيدفع أو لأ", "body-mid", 21, a(.40), anchor="la")

    b.ar(mid, cy - 118, "المسافة اللي", "body-bold", 20, a(.52), anchor="ms")
    b.ar(mid, cy - 90, "بتموت فيها الأفكار", "body-bold", 20, a(.52), anchor="ms")
    b.latin(mid, cy - 44, "THE GAP", "latin-label", 12, accent + (215,), anchor="ms", tracking=4.2)
    b.ar(mid, cy + 124, "وهنا بتموت أغلب الأفكار", "body", 19, a(.30), anchor="ms")


def dev_twenty(b, cy, max_w):
    """A 20×5 build matrix: the decisive 20% is the lit row."""
    accent, PAD = b.accent, 76
    cell, gap, cols, rows = 32, 8, 20, 5
    gw = cols * cell + (cols - 1) * gap
    gh = rows * cell + (rows - 1) * gap
    x0 = b.w - PAD - gw
    y0 = cy - 150
    for r in range(rows):
        for c in range(cols):
            x, y = x0 + c * (cell + gap), y0 + r * (cell + gap)
            if r == 0:
                b.rrect_grad((x, y, x + cell, y + cell), 6)
            else:
                b.rrect((x, y, x + cell, y + cell), 6, fill=(255, 255, 255, 7),
                        outline=a(.09), width=1)

    base = y0 + gh + 46
    b.grad_text(PAD, base - 8, "20%", "latin-num", 76, anchor="ls", base="ltr")
    b.ar(b.w - PAD, base - 50, "صف واحد بس هو اللي", "body-bold", 21, INK, anchor="ra")
    b.ar(b.w - PAD, base - 18, "بيصنع قرار الشراء", "body-bold", 21, INK, anchor="ra")
    b.latin(b.w - PAD, base + 24, "START THERE · SHIP THE REST LATER", "latin-mid", 12,
            a(.32), anchor="ra", tracking=2.2)


def dev_five(b, cy, max_w):
    """The five questions — the saveable post."""
    accent, PAD = b.accent, 76
    xr = b.w - PAD
    row_h = 84
    y0 = cy - (row_h * len(QUESTIONS)) / 2 + 10
    for i, (q, note) in enumerate(QUESTIONS):
        y = y0 + i * row_h
        if i:
            b.hline(PAD, xr, y - 26, a(.07), 1)
        if i in (2, 4):
            b.grad_text(xr, y + 4, f"0{i+1}", "latin-num", 29, anchor="rs", base="ltr")
        else:
            b.latin(xr, y + 4, f"0{i+1}", "latin-num", 29, a(.32), anchor="rs")
        b.ar(xr - 54, y - 2, q, "title", 32, INK, anchor="rs")
        b.ar(xr - 54, y + 32, note, "body", 18.5, a(.38), anchor="rs")


def dev_modules(b, cy, max_w):
    """Proof card: the 14 modules Pharmacy OS shipped."""
    accent, PAD = b.accent, 76
    x0, x1 = PAD, b.w - PAD
    top, bot = cy - 172, cy + 172
    b.rrect((x0, top, x1, bot), 20, fill=(255, 255, 255, 9), outline=a(.13), width=1.2)

    b.latin(x1 - 30, top + 30, "PHARMACY OS", "latin-label", 15, INK, anchor="rm", tracking=2.8)
    b.latin(x1 - 30, top + 54, "MULTI-BRANCH PHARMACY SYSTEM · 2024–2026", "latin-mid", 11,
            a(.38), anchor="rm", tracking=1.8)
    pill = "14 MODULES"
    pw = b.tw(pill, "latin-label", 11.5, 2.4, "ltr") + 28
    b.rrect((x0 + 30, top + 30, x0 + 30 + pw, top + 60), 15, fill=accent + (26,),
            outline=accent + (110,), width=1)
    b.latin(x0 + 30 + pw / 2, top + 45, pill, "latin-label", 11.5, accent + (255,),
            anchor="mm", tracking=2.4)
    b.hline(x0 + 30, x1 - 30, top + 84, a(.08), 1)

    cols, rows, gap = 7, 2, 10
    cw = (x1 - x0 - 60 - (cols - 1) * gap) / cols
    ch = 64
    y0 = top + 96
    hl = {0, 4, 7, 11}
    for i, label in enumerate(MODULES):
        r, c = divmod(i, cols)
        cx1 = x1 - 30 - c * (cw + gap)
        cx0 = cx1 - cw
        y = y0 + r * (ch + gap)
        if i in hl:
            b.rrect((cx0, y, cx1, y + ch), 12, fill=accent + (30,), outline=accent + (115,), width=1.1)
            b.ar(cx1 - cw / 2, y + ch / 2 - 1, label, "body-bold", 17, INK, anchor="mm")
        else:
            b.rrect((cx0, y, cx1, y + ch), 12, fill=(255, 255, 255, 7), outline=a(.09), width=1)
            b.ar(cx1 - cw / 2, y + ch / 2 - 1, label, "body-mid", 17, a(.55), anchor="mm")

    fy = bot - 34
    b.hline(x0 + 30, x1 - 30, fy - 22, a(.07), 1)
    b.ar(x1 - 30, fy, "اتسلّم على مراحل، وكل مرحلة كانت شغالة", "body-mid", 18, a(.55), anchor="ra")
    x = x0 + 30
    for t in ["RTL-FIRST", "MULTI-TENANT", "NEXTJS"]:
        tw = b.tw(t, "latin-label", 10.5, 2.0, "ltr") + 24
        b.rrect((x, fy - 12, x + tw, fy + 12), 12, fill=(255, 255, 255, 8), outline=a(.10), width=1)
        b.latin(x + tw / 2, fy, t, "latin-label", 10.5, a(.48), anchor="mm", tracking=2.0)
        x += tw + 6


def dev_cta(b, cy, max_w):
    """The offer card."""
    accent, PAD = b.accent, 76
    x0, x1 = PAD, b.w - PAD
    top, bot = cy - 158, cy + 158
    b.rrect((x0, top, x1, bot), 22, fill=(255, 255, 255, 11), outline=a(.14), width=1.2)

    b.latin(x0 + 30, top + 32, "FREE · 30 MIN · ONLINE · AR / EN", "latin-label", 12,
            a(.50), anchor="lm", tracking=2.4)
    b.dot(x1 - 30, top + 32, 4.4, accent + (255,))
    b.hline(x0 + 30, x1 - 30, top + 54, a(.09), 1)

    b.ar(x1 - 30, top + 66, "جلسة تشخيص الفكرة", "display", 32, INK, anchor="ra")
    b.ar(x1 - 30, top + 104, "تقييم صريح، نطاق أول نسخة، وتقدير وقت وتكلفة.",
         "body", 18, a(.42), anchor="ra")
    for i, item in enumerate(["تقييم الفكرة: تستاهل تكمّل ولا لأ",
                              "نطاق أول نسخة MVP وخطة الإطلاق",
                              "تقدير الوقت والتكلفة بأرقام"]):
        y = top + 148 + i * 29
        b.dot(x1 - 36, y - 6, 2.8, accent + (255,))
        b.ar(x1 - 50, y, item, "body-mid", 17.5, a(.70), anchor="ra")

    by = bot - 46
    btn_w = 250
    b.rrect((x0 + 30, by, x0 + 30 + btn_w, by + 38), 19, fill=None, outline=a(.22), width=1.2)
    b.latin(x0 + 30 + btn_w / 2, by + 19, "+20 109 250 0454", "latin-label", 15, INK,
            anchor="mm", tracking=0.8)
    b.latin(x0 + 30 + btn_w + 14, by + 19, "codeandcanvas.net/contact", "latin-mid", 12.5, a(.52), anchor="lm")


DEVICES = dict(gap=dev_gap, twenty=dev_twenty, five=dev_five,
               modules=dev_modules, cta=dev_cta)
DEVICE_H = dict(gap=340, twenty=320, five=440, modules=346, cta=316)


# ---------------------------------------------------------------- render
def render(post, fmt="feed"):
    w = 1080
    story = fmt == "story"
    h = 1920 if story else 1350
    b = Board(w, h, accent=post["accent"])
    b.background(seed=311 + post["n"] * 7)
    b.chrome(post)

    PAD = 76
    max_w = w - 2 * PAD
    head_top = 432 if story else 306
    wanted = post["head_size"] * (1.22 if story else 1.0)
    size = b.fit([l for l, _ in post["head"]], "display", wanted, max_w)
    lh = size * 1.34

    y = head_top
    for line, style in post["head"]:
        if style == "grad":
            b.grad_text(w - PAD, y, line, "display", size)
        else:
            b.ar(w - PAD, y, line, "display", size, INK)
        y += lh

    by = y + (44 if story else 36)
    bsize = 26 if story else 23.5
    for ln in post["body"]:
        b.ar(w - PAD, by, ln, "body", bsize, a(.72))
        by += bsize * 1.65
    b.grad_bar((w - PAD - 44, by + 8, w - PAD, by + 10))
    b.latin(w - PAD, by + 24, post["en"], "latin-mid", 13, a(.42), anchor="ra", tracking=1.6)

    field_top = by + (104 if story else 92)
    field_bottom = h - (246 if story else 158)
    dh = DEVICE_H[post["device"]]

    if story:
        # a pull-quote fills the tall field and gives the story its own voice
        dev_cy = field_bottom - dh / 2
        lines = [l for l in [post["quote"][:post["quote"].find("…") + 1].strip(),
                             post["quote"][post["quote"].find("…") + 1:].strip()] if l]
        block = 44 * len(lines)
        top_gap = by + 88
        ask = len(lines) * 22
        room = (dev_cy - dh / 2) - top_gap
        qy = top_gap + (room - block) / 2 if room > block + 60 else top_gap
        b.grad_bar((w - PAD - 3, qy - 6, w - PAD, qy + block - 6), radius=1.6)
        for l in lines:
            b.ar(w - PAD - 26, qy, l, "lead", 27, a(.80), anchor="ra")
            qy += 44
    else:
        centre = (field_top + field_bottom) / 2
        dev_cy = min(max(centre, field_top + dh / 2), field_bottom - dh / 2)
    DEVICES[post["device"]](b, dev_cy, max_w)

    os.makedirs(os.path.join(OUT, fmt), exist_ok=True)
    path = os.path.join(OUT, fmt, f"{post['n']:02d}.png")
    b.img.resize((w, h), Image.LANCZOS).save(path, optimize=True)
    print(f"→ {os.path.relpath(path, ROOT)}  {os.path.getsize(path)//1024} KB  "
          f"(head {size:.0f}px · field {field_top:.0f}-{field_bottom:.0f} · dev@{dev_cy:.0f})")


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
