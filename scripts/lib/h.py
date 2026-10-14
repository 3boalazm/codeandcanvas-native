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
    btns = ''.join(buttons)
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


def page(path, *, title, title_ar, desc, desc_ar, nav, body, body_class='', extra_head='', scripts=('/assets/js/pages.js',), og_type='website', canonical=None, ld=None):
    """Write <ROOT>/<path>/index.html (or ROOT/<path> when path ends with .html).

    ld — optional list of extra schema.org objects (Article, Product, Service…);
    a WebPage node and a BreadcrumbList (from the last crumbs() call) are always emitted.
    """
    url = canonical or (SITE + (path if path.endswith('.html') else path))
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
    extra_head = jsonld(*graph) + extra_head
    doc = f'''<!doctype html>
<html lang="en" dir="ltr" data-title-ar="{esc(title_ar)}" data-desc-ar="{esc(desc_ar)}">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
    <title>{esc(title)}</title>
    <meta name="description" content="{esc(desc)}" />
    <meta property="og:type" content="{og_type}" />
    <meta property="og:title" content="{esc(title)}" />
    <meta property="og:description" content="{esc(desc)}" />
    <meta property="og:url" content="{url}" />
    <link rel="canonical" href="{url}" />
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
