#!/usr/bin/env python3
# ============================================================================
#  build_board.py — generates index.html (the campaign board) from captions.md
#  ---------------------------------------------------------------------------
#  Single source of truth for the copy: captions.md. This script parses it and
#  renders the presentation board, so the page can never disagree with the deck
#  that goes to the client / to Drive.
#
#  Usage: python3 build_board.py
# ============================================================================
import html
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "/marketing/campaigns/second-invoice"
SRC = os.path.join(HERE, "captions.md")
OUT = os.path.join(HERE, "index.html")

META = {
    1: dict(tag="THE HOOK", label="الادعاء", accent="gold"),
    2: dict(tag="THE INVOICES", label="التفصيل", accent="gold"),
    3: dict(tag="THE PATCH", label="السبب", accent="violet"),
    4: dict(tag="THE COMPARISON", label="المقارنة", accent="teal"),
    5: dict(tag="THE ASK", label="الخطوة", accent="pink"),
}

BEATS = [
    ("01 الادعاء", "«رخيص» = أول قسط. إعادة تعريف كلمة مطمّنة."),
    ("02 التفصيل", "3 فواتير بتوصل بعدين: إعادة بناء، ترحيل، فريق."),
    ("03 السبب", "كل ترقيع بيغلي اللي بعده. ليه التكلفة بتزيد."),
    ("04 المقارنة", "الأغلى إنك تعمله مرتين: مرة ومرة صح."),
    ("05 الخطوة", "30 دقيقة على اللي بنيته — توصية واحدة مكتوبة."),
]

SCHEDULE = [
    ("01", "الرخيص مش رخيص", "22 نوفمبر 2026", "الأحد", "8:00–9:30 م", "افتتاحية"),
    ("02", "3 فواتير", "24 نوفمبر 2026", "الثلاثاء", "8:00–9:30 م", "حفظ ومشاركة"),
    ("03", "كل ترقيع بيغلي اللي بعده", "26 نوفمبر 2026", "الخميس", "8:00–9:30 م", "Boost"),
    ("04", "الأغلى إنك تعمله مرتين", "29 نوفمبر 2026", "الأحد", "8:00–9:30 م", "حسم المقارنة"),
    ("05", "قبل ما تدفع المرة التانية", "1 ديسمبر 2026", "الثلاثاء", "8:00–9:30 م", "CTA"),
]


def parse():
    raw = open(SRC, encoding="utf-8").read()
    chunks = re.split(r"^## البوست (\d) — «(.+?)»\s*$", raw, flags=re.M)
    posts = []
    # chunks[0] = header, then (num, title, body) triples
    for i in range(1, len(chunks), 3):
        num, title, body = int(chunks[i]), chunks[i + 1], chunks[i + 2]

        def field(name):
            m = re.search(rf"\*\*{name}:\*\*\s*(.+)", body)
            return m.group(1).strip() if m else ""

        def block(after):
            m = re.search(rf"### {re.escape(after)}\s*\n+```\n(.*?)```", body, re.S)
            return m.group(1).strip() if m else ""

        hashtags = re.search(r"### هاشتاجات\s*\n+\s*`(.+?)`", body, re.S)
        comment_h = re.search(r"### كومنت أول[^\n]*\n+```\n(.*?)```", body, re.S)
        alt = re.search(r"\*\*Alt text:\*\*\s*(.+)", body)
        posts.append(dict(
            n=num, title=title,
            goal=field("الهدف"), audience=field("الجمهور"), design=field("التصميم"),
            ar=block("كابشن (مصري)"), en=block("Caption (EN)"),
            tags=hashtags.group(1).strip() if hashtags else "",
            comment=comment_h.group(1).strip() if comment_h else "",
            alt=alt.group(1).strip() if alt else "",
            **META[num],
        ))
    return posts


def esc(t):
    return html.escape(t)


CSS = """
  @font-face { font-family:'Alexandria'; src:url('/assets/fonts/alexandria-arabic-wght-normal.woff2') format('woff2'); font-weight:100 900; font-display:swap; }
  @font-face { font-family:'PlexArabic'; src:url('/assets/fonts/ibm-plex-sans-arabic-arabic-400-normal.woff2') format('woff2'); font-weight:400; font-display:swap; }
  @font-face { font-family:'PlexArabic'; src:url('/assets/fonts/ibm-plex-sans-arabic-arabic-500-normal.woff2') format('woff2'); font-weight:500; font-display:swap; }
  @font-face { font-family:'PlexArabic'; src:url('/assets/fonts/ibm-plex-sans-arabic-arabic-600-normal.woff2') format('woff2'); font-weight:600; font-display:swap; }
  @font-face { font-family:'Poppins'; src:url('/assets/fonts/Poppins-SemiBold.woff2') format('woff2'); font-weight:600; font-display:swap; }
  @font-face { font-family:'Poppins'; src:url('/assets/fonts/Poppins-Medium.woff2') format('woff2'); font-weight:500; font-display:swap; }
  @font-face { font-family:'Raleway'; src:url('/assets/fonts/Raleway-ExtraBold.woff2') format('woff2'); font-weight:800; font-display:swap; }
  :root{
    --bg:#04040c; --ink:#f7f5ff; --ink-2:rgba(231,229,250,.74); --ink-3:#948fae;
    --violet:#8b6cff; --teal:#3fd6c4; --pink:#ee5ba3; --gold:#f3c77a;
    --line:rgba(255,255,255,.09); --panel:rgba(255,255,255,.035);
    --grad:linear-gradient(100deg,#3fd6c4 0%,#8b6cff 50%,#ee5ba3 100%);
    --f-head:'Alexandria',system-ui,sans-serif; --f-body:'PlexArabic','Alexandria',sans-serif;
    --lat:'Poppins',system-ui,sans-serif; --num:'Raleway',system-ui,sans-serif;
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--f-body);font-size:17px;line-height:1.85;-webkit-font-smoothing:antialiased}
  body::before{content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;
    background:radial-gradient(52vw 44vh at 90% 0%,rgba(243,199,122,.16),transparent 70%),
               radial-gradient(50vw 40vh at 6% 22%,rgba(139,108,255,.16),transparent 72%),
               radial-gradient(46vw 40vh at 78% 96%,rgba(238,91,163,.10),transparent 72%),
               linear-gradient(180deg,#0a0a20,#030309 70%)}
  a{color:inherit}
  .wrap{width:min(1180px,92vw);margin-inline:auto}
  .lat{font-family:var(--lat);letter-spacing:.18em;text-transform:uppercase;font-size:11px;font-weight:600}
  .num{font-family:var(--num);font-weight:800}
  header.top{position:sticky;top:0;z-index:40;backdrop-filter:blur(16px);background:rgba(4,4,12,.76);border-bottom:1px solid var(--line)}
  .top__in{display:flex;align-items:center;gap:20px;padding:13px 0}
  .top img{height:32px;width:auto;display:block}
  .top .badge{margin-inline-start:auto;font-size:12.5px;padding:6px 14px;border-radius:999px;border:1px solid rgba(255,255,255,.15);color:var(--ink-2);white-space:nowrap}
  .hero{padding:clamp(52px,8vw,110px) 0 48px}
  .kicker{display:inline-flex;align-items:center;gap:10px;color:var(--gold)}
  .kicker i{width:7px;height:7px;border-radius:50%;background:var(--gold);box-shadow:0 0 18px 3px rgba(243,199,122,.55)}
  h1{font-family:var(--f-head);font-weight:800;line-height:1.1;margin:20px 0 0;font-size:clamp(42px,7.4vw,96px);letter-spacing:-.015em}
  h1 em{font-style:normal;background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
  .lede{font-size:clamp(17px,2vw,21px);color:var(--ink-2);max-width:62ch;margin:24px 0 0}
  .chips{display:flex;flex-wrap:wrap;gap:10px;margin-top:30px}
  .chip{border:1px solid var(--line);background:rgba(255,255,255,.03);border-radius:999px;padding:8px 16px;font-size:13.5px;color:var(--ink-2)}
  .chip b{color:#fff}
  section{padding:clamp(44px,5vw,76px) 0;border-top:1px solid var(--line)}
  .sec-head{display:flex;align-items:baseline;gap:16px;flex-wrap:wrap;margin-bottom:28px}
  .sec-head h2{font-family:var(--f-head);font-weight:700;font-size:clamp(24px,3vw,34px);margin:0}
  .sec-head span{color:var(--ink-3);font-size:14px}
  .grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
  @media(max-width:900px){.grid3{grid-template-columns:1fr}}
  .card{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:24px 22px}
  .card h3{margin:0 0 10px;font-family:var(--f-head);font-size:17px;font-weight:700}
  .card p{margin:0;color:var(--ink-2);font-size:15.5px}
  .card .lat{color:var(--gold);display:block;margin-bottom:12px}
  .arc{display:grid;grid-template-columns:repeat(5,1fr);gap:12px}
  @media(max-width:900px){.arc{grid-template-columns:1fr 1fr}}
  .beat{border-top:2px solid rgba(255,255,255,.12);padding-top:14px}
  .beat:nth-child(1){border-top-color:var(--gold)}.beat:nth-child(2){border-top-color:var(--gold)}
  .beat:nth-child(3){border-top-color:var(--violet)}.beat:nth-child(4){border-top-color:var(--teal)}
  .beat:nth-child(5){border-top-color:var(--pink)}
  .beat b{display:block;font-family:var(--f-head);font-size:15.5px;margin-bottom:4px}
  .beat small{color:var(--ink-3);font-size:13.5px;line-height:1.7;display:block}
  .post{display:grid;grid-template-columns:.62fr 1fr;gap:clamp(18px,3vw,42px);padding:clamp(26px,3vw,40px) 0;border-top:1px solid var(--line)}
  .post:first-of-type{border-top:0}
  @media(max-width:880px){.post{grid-template-columns:1fr}}
  .shot{display:grid;grid-template-columns:1fr .62fr;gap:10px;align-items:start}
  .shot img{width:100%;height:auto;display:block;border-radius:12px;border:1px solid var(--line);background:#08080f}
  .post__head{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:6px}
  .post__head .idx{font-family:var(--num);font-size:26px;font-weight:800;color:var(--gold);line-height:1}
  .post__head h3{font-family:var(--f-head);font-size:clamp(20px,2.4vw,27px);margin:0;font-weight:700}
  .tag{font-family:var(--lat);font-size:10px;letter-spacing:.18em;text-transform:uppercase;padding:4px 10px;border-radius:999px;border:1px solid rgba(255,255,255,.16);color:var(--ink-2)}
  .meta{display:grid;gap:8px;margin:14px 0 18px;font-size:14.5px;color:var(--ink-2)}
  .meta b{color:#fff;font-weight:600}
  details{border:1px solid var(--line);border-radius:12px;padding:0 16px;background:rgba(255,255,255,.02);margin-top:10px}
  details+details{margin-top:8px}
  summary{cursor:pointer;padding:12px 0;font-size:14px;font-weight:600;color:var(--ink-2);list-style:none}
  summary::-webkit-details-marker{display:none}
  summary::before{content:"+";font-family:var(--num);color:var(--gold);margin-inline-end:10px}
  details[open] summary::before{content:"–"}
  pre{margin:0 0 16px;white-space:pre-wrap;word-break:break-word;font-family:var(--f-body);font-size:15px;line-height:1.95;color:var(--ink)}
  .tags{font-family:var(--lat);font-size:12.5px;color:var(--teal);word-break:break-word}
  .spec{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
  @media(max-width:900px){.spec{grid-template-columns:1fr 1fr}}
  table{width:100%;border-collapse:collapse;font-size:15px}
  th,td{text-align:right;padding:13px 10px;border-bottom:1px solid var(--line);vertical-align:top}
  th{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3);font-family:var(--lat);font-weight:600}
  td b{color:#fff}
  .swatch{display:flex;gap:10px;flex-wrap:wrap;margin-top:14px}
  .sw{display:flex;align-items:center;gap:8px;font-size:12.5px;color:var(--ink-3);font-family:var(--lat)}
  .sw i{width:16px;height:16px;border-radius:4px;display:block}
  footer{padding:44px 0 70px;border-top:1px solid var(--line);color:var(--ink-3);font-size:14px}
  footer a{color:var(--ink-2)}
"""


def post_html(p):
    img_f = f"{BASE}/assets/feed/{p['n']:02d}.png"
    img_s = f"{BASE}/assets/story/{p['n']:02d}.png"
    return f"""
      <article class="post" id="post-{p['n']:02d}">
        <div class="shot">
          <a href="{img_f}" target="_blank" rel="noopener"><img src="{img_f}" alt="{esc(p['alt'])}" loading="lazy"></a>
          <a href="{img_s}" target="_blank" rel="noopener"><img src="{img_s}" alt="نسخة الستوري — {esc(p['title'])}" loading="lazy"></a>
        </div>
        <div>
          <div class="post__head">
            <span class="idx">{p['n']:02d}</span>
            <h3>{esc(p['title'])}</h3>
            <span class="tag">{p['tag']}</span>
          </div>
          <div class="meta">
            <div><b>الهدف:</b> {esc(p['goal'])}</div>
            <div><b>الجمهور:</b> {esc(p['audience'])}</div>
            <div><b>التصميم:</b> {esc(p['design'])}</div>
          </div>
          <details>
            <summary>الكابشن — مصري</summary>
            <pre>{esc(p['ar'])}</pre>
          </details>
          <details>
            <summary>Caption — English</summary>
            <pre dir="ltr" style="text-align:left">{esc(p['en'])}</pre>
          </details>
          <details>
            <summary>كومنت أول + هاشتاجات</summary>
            <pre>{esc(p['comment'])}</pre>
            <p class="tags">{esc(p['tags'])}</p>
          </details>
        </div>
      </article>"""


def build():
    posts = parse()
    rows = "\n".join(
        f"      <tr><td><b>{n}</b></td><td>{esc(t)}</td><td>{d}</td><td>{w}</td><td>{h}</td><td>{note}</td></tr>"
        for n, t, d, w, h, note in SCHEDULE)
    beats = "\n".join(f'        <div class="beat"><b>{esc(b)}</b><small>{esc(s)}</small></div>'
                      for b, s in BEATS)
    body = "\n".join(post_html(p) for p in posts)

    page = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>«الفاتورة التانية» — لوحة كامبين Code &amp; Canvas</title>
<meta name="description" content="لوحة كامبين Code & Canvas: 5 بوستات عن التكلفة المخفية للتطوير الرخيص — كوبي مصري وإنجليزي وتصميمات 1080×1350 و1080×1920." />
<meta name="robots" content="noindex" />
<link rel="icon" href="/favicon.svg" type="image/svg+xml" />
<style>{CSS}</style>
</head>
<body>

<header class="top">
  <div class="wrap top__in">
    <img src="/assets/brand/logo-white-horizontal.svg" alt="Code &amp; Canvas" />
    <span class="badge">حملة 05 بوستات · فيسبوك + إنستجرام</span>
  </div>
</header>

<div class="wrap hero">
  <div class="kicker lat"><i></i> Campaign board · The second invoice</div>
  <h1>الفاتورة <em>التانية</em></h1>
  <p class="lede">حملة تانية لنفس البراند بفكرة مختلفة: مش «إزاي تدخل السوق»، لكن «تمن إنك تدخله بسرعة». خمس بوستات بتفكّ التكلفة المخفية للتطوير الرخيص — بلوك بصري جديد: بانل هادي فوق، صورة دافئة تحت، وشريط التدرّج هو الخط الوحيد اللي بينهم.</p>
  <div class="chips">
    <span class="chip"><b>5</b> بوستات · فكرة واحدة</span>
    <span class="chip"><b>4</b> بوستات بصور · <b>1</b> تايبوجرافي</span>
    <span class="chip"><b>10</b> تصميمات: 1080×1350 + 1080×1920</span>
    <span class="chip"><b>2</b> لغات: مصري + إنجليزي</span>
    <span class="chip"><b>10</b> أيام نشر · 22 نوفمبر – 1 ديسمبر 2026</span>
    <span class="chip">هوية <b>Code &amp; Canvas</b> كاملة</span>
  </div>
</div>

<section id="idea">
  <div class="wrap">
    <div class="sec-head">
      <span class="lat" style="color:var(--teal)">01 — The big idea</span>
      <h2>التوفير بيرجع فاتورة</h2>
    </div>
    <div class="grid3">
      <div class="card">
        <span class="lat">Audience</span>
        <h3>اللي بيدور على أرخص عرض</h3>
        <p>صاحب بيزنس عنده فكرة أو نظام شغال بالفعل، بيوازن بين عروض أسعار، ولسه مش شايف إن القرار ده مش سعري — ده قرار تكلفة مؤجّلة.</p>
      </div>
      <div class="card">
        <span class="lat">Message</span>
        <h3>«رخيص» = أول قسط</h3>
        <p>الرسالة واحدة في الخمس بوستات: السعر اللي بتشوفه مش السعر اللي هتدفعه. الباقي بيوصل بعدين، في صورة إعادة بناء، وترحيل بيانات، وفريق بيدفع تمن الفهم من الأول.</p>
      </div>
      <div class="card">
        <span class="lat">Difference</span>
        <h3>بلوك بصري منفصل</h3>
        <p>مش تكرار لكامبين «من فكرة لمنتج»: تقسيم أفقي صارم (بانل/صورة)، تايبوجرافي أكبر، دوتون دافئ ذهبي بدل البنفسجي البارد، وشريط تدرّج واحد بدل الجلوات.</p>
      </div>
    </div>
  </div>
</section>

<section id="arc">
  <div class="wrap">
    <div class="sec-head">
      <span class="lat" style="color:var(--violet)">02 — The arc</span>
      <h2>قوس الحملة</h2>
    </div>
    <div class="arc">
{beats}
    </div>
  </div>
</section>

<section id="posts">
  <div class="wrap">
    <div class="sec-head">
      <span class="lat" style="color:var(--gold)">03 — The posts</span>
      <h2>خمس بوستات — الكوبي والتصميم</h2>
      <span>اضغط على أي قسم لفتح الكابشن</span>
    </div>
{body}
  </div>
</section>

<section id="design">
  <div class="wrap">
    <div class="sec-head">
      <span class="lat" style="color:var(--teal)">04 — Design system</span>
      <h2>نظام التصميم</h2>
    </div>
    <div class="spec">
      <div class="card"><span class="lat">Layout</span><h3>تقسيم أفقي</h3><p>بانل أسود علوي (600 / 880px) + باند صورة تحت + شريط تدرّج 3px على الخط الفاصل. النص دايمًا في البانل، الصورة عمرها ما بتاكل النص.</p></div>
      <div class="card"><span class="lat">Type</span><h3>أكبر وأضيق</h3><p>Alexandria 800 بحجم يوصل 116px (فيد) و130px (ستوري) على interlacing 1.12 — أضخم من الكامبين الأول بـ20% وأهدى.</p></div>
      <div class="card"><span class="lat">Photography</span><h3>دوتون دافئ</h3><p>عاجي/ذهبي بدل البنفسجي: تكحيل دافئ + 13% تينت من لون البوست + حبيبات 2. الصور مفهومية، مفيش أشخاص بيتكلموا باسم البراند.</p></div>
      <div class="card"><span class="lat">Chrome</span><h3>عنصرين بس</h3><p>اللوجو فوق يمين + فهرس 01/05 فوق شمال. مفيش شبكة، ولا زوايا، ولا خطوط تحت — كل حاجة تانية بتشيل عين القارئ من العنوان.</p></div>
    </div>
    <div class="swatch">
      <span class="sw"><i style="background:#04040c"></i>#04040C canvas</span>
      <span class="sw"><i style="background:#f3c77a"></i>#F3C77A gold</span>
      <span class="sw"><i style="background:#8b6cff"></i>#8B6CFF violet</span>
      <span class="sw"><i style="background:#3fd6c4"></i>#3FD6C4 teal</span>
      <span class="sw"><i style="background:#ee5ba3"></i>#EE5BA3 pink</span>
      <span class="sw"><i style="background:linear-gradient(100deg,#3fd6c4,#8b6cff,#ee5ba3)"></i>brand gradient</span>
    </div>
  </div>
</section>

<section id="schedule">
  <div class="wrap">
    <div class="sec-head">
      <span class="lat" style="color:var(--pink)">05 — Schedule</span>
      <h2>جدول النشر</h2>
      <span>القاهرة / الرياض · 8:00–9:30 م</span>
    </div>
    <table>
      <thead><tr><th>#</th><th>البوست</th><th>التاريخ</th><th>اليوم</th><th>الوقت</th><th>ملاحظة</th></tr></thead>
      <tbody>
{rows}
      </tbody>
    </table>
  </div>
</section>

<footer>
  <div class="wrap">
    <p style="margin:0 0 8px">Code &amp; Canvas — Business Development, By Design.</p>
    <p style="margin:0">الملفات: <code>assets/feed/01–05.png</code> · <code>assets/story/01–05.png</code> · <code>captions.md</code> · <code>campaign-kit.zip</code> — والتواصل: <a href="https://codeandcanvas.net/contact">codeandcanvas.net/contact</a></p>
  </div>
</footer>

</body>
</html>
"""
    open(OUT, "w", encoding="utf-8").write(page)
    print(f"→ {os.path.relpath(OUT, os.path.dirname(os.path.dirname(HERE)))}  "
          f"{len(posts)} posts · {len(page)//1024} KB")


if __name__ == "__main__":
    build()
