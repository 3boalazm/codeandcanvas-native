# -*- coding: utf-8 -*-
"""Tiny HTML helpers used by scripts/gen-pages.py (scaffolding only — the
committed HTML under each route folder is the source of truth)."""
import html as _html
import json as _json
import os
import re
from catalog import SERVICES, TRACKS, href

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SITE = 'https://codeandcanvas.net'


def esc(s):
    return _html.escape(s, quote=True)


def t(en, ar, tag='span', cls='', attrs=''):
    """Bilingual inline: English text with the Arabic twin in data-ar."""
    c = f' class="{cls}"' if cls else ''
    a = f' {attrs}' if attrs else ''
    return f'<{tag}{c}{a} data-ar="{esc(ar)}">{en}</{tag}>'


def th(en, ar, tag='span', cls='', attrs=''):
    """Bilingual inline where both sides contain markup (data-ar-html)."""
    c = f' class="{cls}"' if cls else ''
    a = f' {attrs}' if attrs else ''
    return f'<{tag}{c}{a} data-ar-html="{esc(ar)}">{en}</{tag}>'


def icon(name, cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<i{c} data-icon="{name}" aria-hidden="true"></i>'


def arrow():
    return '<span class="round-arrow" aria-hidden="true"><i class="flip" data-icon="arrowUpRight"></i></span>'


def svc_card(code, delay=0, link=None):
    s = SERVICES[code]
    tr = TRACKS[s['track']]
    tag = t(s['tag'], s['tag_ar'], cls='svc__tag') if s.get('tag_ar') else f'<span class="svc__tag">{esc(s["tag"])}</span>'
    price = (t(s['price'], s['price_ar'], tag='strong', cls='ltr') if s.get('price_ar')
             else f'<strong class="ltr">{esc(s["price"])}</strong>')
    dur = t(s['dur'], s['dur_ar']) if s.get('dur_ar') else f'<span>{esc(s["dur"])}</span>'
    return (
        f'<a class="card glass svc {tr["cls"]}" id="{code.lower()}-card" data-category="{s["track"]}" href="{link or href(code)}" data-tilt data-reveal style="--d:{delay:.2f}s">\n'
        f'  <span class="svc__top"><span class="svc__no">{code}</span>{tag}</span>\n'
        f'  <h3 data-ar="{esc(s["title_ar"])}">{esc(s["title"])}</h3>\n'
        f'  <p data-ar="{esc(s["blurb_ar"])}">{esc(s["blurb"])}</p>\n'
        f'  <span class="svc__foot"><span class="svc__price">{price}{dur}</span>{arrow()}</span>\n'
        f'</a>'
    )


def svc_grid(codes, link_self=False):
    out = ['<div class="svc-grid">']
    for i, c in enumerate(codes):
        out.append(svc_card(c, (i % 3) * 0.07, link=f'#{c.lower()}' if link_self else None))
    out.append('</div>')
    return '\n'.join(out)


_LAST_CRUMBS = []  # set by crumbs(); consumed by page() for the BreadcrumbList JSON-LD


def crumbs(items):
    """items = [(label_en, label_ar, href|None)] — last item is current."""
    _LAST_CRUMBS[:] = list(items)
    parts = []
    for i, (en, ar, h) in enumerate(items):
        if h:
            parts.append(f'<a href="{h}" data-ar="{esc(ar)}">{en}</a>')
        else:
            parts.append(f'<span aria-current="page" data-ar="{esc(ar)}">{en}</span>')
        if i < len(items) - 1:
            parts.append('<i>›</i>')
    return '<nav class="crumbs" aria-label="Breadcrumb" data-ar-label="مسار التنقل">' + ''.join(parts) + '</nav>'


def closing(kicker, kicker_ar, title_html, text, text_ar, buttons, contact=True):
    btns = ''.join(buttons[:2])
    contact_html = ('<p class="closing__contact"><a href="mailto:info@codeandcanvas.net">info@codeandcanvas.net</a> · '
                    '<a class="ltr" href="tel:+966545520750">+966 54 552 0750</a> · <a class="ltr" href="tel:+201092500454">+20 109 250 0454</a></p>') if contact else ''
    return f'''
      <section class="section container section--tight" aria-label="Next step" data-ar-label="الخطوة التالية">
        <div class="closing" data-reveal>
          <span class="closing__border" aria-hidden="true"></span>
          <div class="closing__inner glass glass--deep">
            <p class="kicker kicker--center"><span data-ar="{esc(kicker_ar)}">{kicker}</span></p>
            <h2 class="closing__title">{title_html}</h2>
            <p class="closing__text" data-ar="{esc(text_ar)}">{text}</p>
            <div class="hero__ctas hero__ctas--center">{btns}</div>
            {contact_html}
          </div>
        </div>
      </section>'''


def btn(label, label_ar, h, kind='primary', icon_name='arrowUpRight', extra=''):
    cls = {'primary': 'btn btn--primary magnetic', 'glass': 'btn btn--glass', 'ghost': 'btn btn--ghost'}[kind]
    ic = f'<i class="flip" data-icon="{icon_name}"></i>' if icon_name else ''
    ext = ' target="_blank" rel="noopener"' if h.startswith('http') else ''
    return f'<a class="{cls}{(" " + extra) if extra else ""}" href="{h}"{ext}><span data-ar="{esc(label_ar)}">{label}</span>{ic}</a>'


REGISTRY = []  # (path, title, title_ar) of every page written this run


ORG_ID = SITE + '/#org'
SITE_ID = SITE + '/#website'


def jsonld(*objects):
    """Serialise schema.org objects into one <script type="application/ld+json"> block."""
    objs = [o for o in objects if o]
    if not objs:
        return ''
    data = {'@context': 'https://schema.org', '@graph': objs} if len(objs) > 1 else {'@context': 'https://schema.org', **objs[0]}
    return '    <script type="application/ld+json">' + _json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + '</script>\n'


PERSON_LD = {
    'ahmed': {'@type': 'Person', '@id': SITE + '/team/#ahmed', 'name': 'Ahmed M. Bedeer', 'url': SITE + '/team/#ahmed',
              'jobTitle': 'Co-Founder · Enterprise Architect · Solution Architect', 'worksFor': {'@id': ORG_ID},
              'knowsAbout': ['Enterprise Architecture', 'TOGAF', 'NORA', 'ArchiMate', 'Healthcare IT', 'HL7 FHIR', 'Java · Spring Boot', 'Cloud'],
              'sameAs': ['https://linkedin.com/in/ahmed-bedeer', 'https://ahmed-bedeer.vercel.app/', 'https://github.com/ahmedbdeer']},
    'mustafa': {'@type': 'Person', '@id': SITE + '/team/#mustafa', 'name': 'Mustafa Aboalazm', 'url': SITE + '/team/#mustafa',
                'jobTitle': 'Co-Founder · Creative Director · Visual Brand Architect', 'worksFor': {'@id': ORG_ID},
                'knowsAbout': ['Brand Identity', 'Visual Systems', 'Design Systems', 'Art Direction', 'Print & Packaging', 'Web Design'],
                'sameAs': ['https://behance.net/aboalazm', 'https://aboalazm-os.vercel.app/']},
}


def service_ld(codes, page_url):
    """OfferCatalog-style ItemList of Service nodes for a track/hub page."""
    items = []
    for i, code in enumerate(codes):
        sv = SERVICES[code]
        node = {'@type': 'Service', '@id': page_url + '#' + code.lower(), 'name': sv['title'], 'serviceType': sv.get('tag') or sv['title'],
                'description': re.sub(r'<[^>]+>', '', sv.get('blurb') or sv['title']), 'provider': {'@id': ORG_ID},
                'areaServed': ['Saudi Arabia', 'Egypt', 'MENA'], 'url': SITE + href(code)}
        items.append({'@type': 'ListItem', 'position': i + 1, 'item': node})
    return {'@type': 'ItemList', 'itemListElement': items}


def sec_head(no, kicker, kicker_ar, title_html, lead, lead_ar, aside=None, center=False):
    """Numbered editorial section head: rule, kicker, title, lead and an optional aside."""
    cls = 'sec-head sec-head--center' if center else 'sec-head'
    aside_html = f'<div class="sec-head__aside">{aside}</div>' if aside else ''
    lead_html = f'<p class="lead" data-ar="{esc(lead_ar)}">{lead}</p>' if lead else ''
    return f'''
        <header class="{cls}" data-reveal>
          <div>
            <p class="sec-head__no"><b>{no}</b><span data-ar="{esc(kicker_ar)}">{kicker}</span></p>
            <h2>{title_html}</h2>
            {lead_html}
          </div>
          {aside_html}
        </header>'''


def svc_row(code, delay=0, alt=False, cta=('Start a scoped inquiry', 'ابدأ استفسارًا بنطاق واضح')):
    """One decision row per service: who it is for, what the client keeps, price and CTA."""
    s = SERVICES[code]
    out = ''.join(f'<li data-ar="{esc(a)}">{esc(e)}</li>' for e, a in zip(s['out'], s['out_ar']))
    dur = t(s['dur'], s['dur_ar']) if s.get('dur_ar') else f'<span>{esc(s["dur"])}</span>'
    price = t(s['price'], s['price_ar'], tag='strong') if s.get('price_ar') else f'<strong class="ltr">{esc(s["price"])}</strong>'
    star = ' ✦' if s.get('star') else ''
    tag = t(s['tag'], s['tag_ar'], cls='tag-soft') if s.get('tag_ar') else f'<span class="tag-soft">{esc(s["tag"])}</span>'
    cls = 'svc-row svc-row--alt' if alt else 'svc-row'
    return f'''
        <article class="{cls}" id="{code.lower()}" data-category="{s['track']}" data-reveal{f' style="--d:{delay:.2f}s"' if delay else ''}>
          <div class="svc-row__code">{code}{star}</div>
          <div class="svc-row__body">
            <h3 data-ar="{esc(s['title_ar'])}">{esc(s['title'])}</h3>
            <p data-ar="{esc(s['blurb_ar'])}">{esc(s['blurb'])}</p>
            <div class="svc-row__out"><b data-ar="ما تحصل عليه">{'What you keep'}</b><ul class="svc-row__list">{out}</ul></div>
          </div>
          <div class="svc-row__fit">
            <div><b data-ar="لمن؟">Who it is for</b><span data-ar="{esc(s['for_ar'])}">{esc(s['for_'])}</span></div>
            <div>{tag}</div>
          </div>
          <div class="svc-row__act">
            <span class="svc-row__price">{price}{dur}</span>
            <a class="btn btn--glass btn--sm" href="/contact/?inquiry={code}#message" data-track="service-inquiry" data-track-service="{code}"><span data-ar="{esc(cta[1])}">{cta[0]}</span><i class="flip" data-icon="arrowUpRight"></i></a>
          </div>
        </article>'''


def svc_rows(codes, alt_ids=False, alt_every=None):
    rows = []
    for i, c in enumerate(codes):
        alt = (i % alt_every == 1) if alt_every else False
        rows.append(svc_row(c, (i % 3) * 0.05, alt=alt))
    return '<div class="svc-rows">' + ''.join(rows) + '</div>'


def svc_index_row(code):
    """Compact index row used by the /services/ hub: code, title, who, duration, price."""
    s = SERVICES[code]
    return (f'<li><a href="{href(code)}" data-track="service-detail" data-track-id="{code}">'
            f'<span class="idx__code">{code}</span>'
            f'<span class="idx__title" data-ar="{esc(s["title_ar"])}">{esc(s["title"])}</span>'
            f'<span class="idx__who" data-ar="{esc(s["for_ar"])}">{esc(s["for_"])}</span>'
            f'<span class="idx__price ltr">{esc(s["price"])}</span>'
            f'<span class="idx__dur" data-ar="{esc(s.get("dur_ar") or s["dur"])}">{esc(s["dur"])}</span>'
            f'<i class="flip" data-icon="arrowUpRight" aria-hidden="true"></i></a></li>')


def steps3(items):
    """items = [(no, title_en, title_ar, body_en, body_ar, deliverable_en, deliverable_ar)]"""
    blocks = ''.join(f'''
            <div>
              <span class="stepno">{no}</span>
              <h3 data-ar="{esc(t_ar)}">{esc(t_en)}</h3>
              <p data-ar="{esc(b_ar)}">{esc(b_en)}</p>
              <span class="step__deliv"><i data-icon="check" aria-hidden="true"></i><span data-ar="{esc(d_ar)}">{esc(d_en)}</span></span>
            </div>''' for no, t_en, t_ar, b_en, b_ar, d_en, d_ar in items)
    return f'<div class="steps3" data-reveal>{blocks}</div>'


def chal(code, kicker, kicker_ar, title, title_ar, symptoms, symptoms_ar, price_en, price_ar, delay=0, link=None):
    """Problem-first entry card: opens the service page, with a scoped inquiry link."""
    sym = ''.join(f'<li data-ar="{esc(a)}">{esc(e)}</li>' for e, a in zip(symptoms, symptoms_ar))
    return f'''
          <article class="chal" data-reveal{f' style="--d:{delay:.2f}s"' if delay else ''}>
            <span class="chal__k" data-ar="{esc(kicker_ar)}">{kicker}</span>
            <h3><a class="chal__link" href="{link or href(code)}" data-track="service-finder" data-track-id="{code}" data-ar="{esc(title_ar)}">{title}</a></h3>
            <ul class="chal__sym">{sym}</ul>
            <span class="chal__fix">
              <span class="chal__code">{code} · <b data-ar="{esc(SERVICES[code]['title_ar'])}">{esc(SERVICES[code]['title'])}</b></span>
              <span class="chal__price" data-ar="{esc(price_ar)}">{price_en}</span>
              <a class="chal__cta" href="/contact/?inquiry={code}#message" data-track="service-inquiry" data-track-service="{code}"><span data-ar="ابدأ استفسارًا بنطاق">Start a scoped inquiry</span>{icon('arrowUpRight', 'flip')}</a>
            </span>
          </article>'''


def facts(items):
    """items = [(label_en, label_ar, value, value_is_ltr, value_ar or None)]"""
    cells = []
    for item in items:
        e, a, v, ltr = item[0], item[1], item[2], item[3]
        va = item[4] if len(item) > 4 else None
        b = f'<b class="ltr">{v}</b>' if ltr else (f'<b data-ar="{esc(va)}">{v}</b>' if va else f'<b>{v}</b>')
        cells.append(f'<div><span data-ar="{esc(a)}">{esc(e)}</span>{b}</div>')
    return '<div class="facts" data-reveal>' + ''.join(cells) + '</div>'


def page(path, *, title, title_ar, desc, desc_ar, nav, body, body_class='', extra_head='', scripts=('/assets/js/pages.js',), og_type='website', canonical=None, ld=None):
    """Write <ROOT>/<path>/index.html (or ROOT/<path> when path ends with .html).

    ld — optional list of extra schema.org objects (Article, Product, Service…);
    a WebPage node and a BreadcrumbList (from the last crumbs() call) are always emitted.
    """
    url = canonical or (SITE + (path if path.endswith('.html') else path))
    ar_url = SITE + '/ar/' if path == '/' else SITE + '/ar' + path
    ar_path = '/ar/' if path == '/' else '/ar' + path
    if path.startswith('/books/') and not path.endswith('/read/'):
        body = body.replace('</h1>', '</h1><p class="notice" data-ar="معاينات عامة فقط. الشراء الإلكتروني غير متاح حاليًا؛ الأسعار استرشادية. احفظ قائمة أو استفسر عن التوفر.">Public previews only. Online purchasing is not available yet; prices are indicative. Save a shortlist or ask about availability.</p><p><a class="text-link" href="/cart/" data-ar="قائمة الكتب المحفوظة ←">Your saved shortlist →</a></p>', 1)
    body = body.replace('<form ', '<form method="post" ')  # JS intercepts; never leak form values via GET if scripts fail.
    script_tags = '\n'.join(f'    <script src="{s}"></script>' for s in scripts)
    graph = [{
        '@type': 'WebPage', '@id': url + '#webpage', 'url': url, 'name': title, 'description': desc,
        'inLanguage': ['en', 'ar'], 'isPartOf': {'@id': SITE_ID}, 'publisher': {'@id': ORG_ID},
        'primaryImageOfPage': {'@type': 'ImageObject', 'url': SITE + '/assets/brand/og-default.png', 'width': 1200, 'height': 630},
    }]
    if _LAST_CRUMBS:
        graph.append({'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'name': en, **({'item': SITE + h} if h else {})}
            for i, (en, ar, h) in enumerate(_LAST_CRUMBS)]})
        _LAST_CRUMBS.clear()
    graph.extend(ld or [])
    if path in ('/account/', '/cart/', '/checkout/', '/thank-you/', '/login/', '/register/', '/forgot-password/', '/reset-password/', '/404.html') or path.endswith('/read/'):
        extra_head += '    <meta name="robots" content="noindex, follow" />\n'
    extra_head = jsonld(*graph) + extra_head
    doc = f'''<!doctype html>
<html lang="en" dir="ltr" data-title-ar="{esc(title_ar)}" data-desc-ar="{esc(desc_ar)}" data-lang-mirror="{ar_path}">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
    <title>{esc(title)}</title>
    <meta name="description" content="{esc(desc)}" />
    <meta property="og:type" content="{og_type}" />
    <meta property="og:title" content="{esc(title)}" />
    <meta property="og:description" content="{esc(desc)}" />
    <meta property="og:url" content="{url}" />
    <meta property="og:locale" content="en_US" />
    <link rel="canonical" href="{url}" />
    <link rel="alternate" hreflang="en" href="{url}" />
    <link rel="alternate" hreflang="ar" href="{ar_url}" />
    <link rel="alternate" hreflang="x-default" href="{url}" />
    <!-- cc:head -->
    <!-- /cc:head -->
{extra_head}  </head>
  <body class="is-loading{(' ' + body_class) if body_class else ''}"{f' data-nav="{nav}"' if nav else ''}>
    <!-- cc:top -->
    <!-- /cc:top -->

    <main id="main">
{body}
    </main>

    <!-- cc:bottom -->
    <!-- /cc:bottom -->
{script_tags}
  </body>
</html>
'''
    out = os.path.join(ROOT, path.lstrip('/')) if path.endswith('.html') else os.path.join(ROOT, path.strip('/'), 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    REGISTRY.append((path, title, title_ar))
    with open(out, 'w', encoding='utf-8') as f:
        f.write(doc)
    return out
