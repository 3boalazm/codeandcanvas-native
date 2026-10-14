# -*- coding: utf-8 -*-
"""/blog/ hub + /blog/<slug>/ articles — literal copy of the live Insights Hub.

Live facts (WP REST, 2026-06-18): 8 published posts. Two hub cards ("From Brand
Identity to Brand Systems", "Creative Strategy in the Age of Generative AI") never
had an article (404) → shown as "coming soon", not linked. Two posts were published
under wrong slugs with a "– Copy" title → re-slugged (see POST['aliases'] + _redirects).
Articles are English-only on the live site; chrome/meta are bilingual."""
import re
from h import esc, icon, crumbs, closing, btn, page, sec_head, facts, PERSON_LD
from posts import all_posts

AUTHORS = {
    'cc': dict(ini='CC', name='Code & Canvas Editorial', name_ar='تحرير Code & Canvas',
               line='Product Strategy · Enterprise Architecture · Brand Identity · MENA',
               bio='Code & Canvas is a digital product studio and advisory firm operating across KSA and Egypt. We specialize in enterprise architecture, healthcare informatics, brand identity, and product strategy — helping organizations bridge the gap between innovation and measurable impact.',
               links=[('Our Services →', 'خدماتنا ←', '/services/'), ('Work With Us →', 'اعمل معنا ←', '/contact/'), ('Our Story →', 'قصتنا ←', '/our-story/')]),
    'ma': dict(ini='MA', name='Mustafa Aboalazm', name_ar='مصطفى أبو العزم',
               line='Head of Brand Strategy · Co-Founder · Code & Canvas · Al Obour, Egypt',
               bio='Systemic Identity Architect and Senior Brand Designer with 9+ years building brand systems across MENA. Former Media Director at Nile Pharma Food. Co-Founder of Code & Canvas — where enterprise architecture meets strategic creative practice.',
               links=[('Our Services →', 'خدماتنا ←', '/services/'), ('Work With Us →', 'اعمل معنا ←', '/contact/'), ('Portfolio ↗', 'الأعمال ↗', 'https://aboalazm-os.vercel.app/work')]),
}

COMING_SOON = [
    dict(title='From Brand Identity to Brand Systems', title_ar='من هوية العلامة إلى أنظمة العلامة', cat='Brand Identity', cat_ar='هوية العلامة', minutes=4, emoji='🏛️', author='ma',
         excerpt='Static manuals are obsolete. The evolution from logo to living system — and why it determines whether your brand scales or fractures.',
         excerpt_ar='الأدلة الثابتة عفا عليها الزمن. التطور من الشعار إلى نظام حي — ولماذا يحدد ما إذا كانت علامتك ستتوسع أم تتصدع.'),
    dict(title='Creative Strategy in the Age of Generative AI', title_ar='الاستراتيجية الإبداعية في عصر الذكاء الاصطناعي التوليدي', cat='Creative Strategy', cat_ar='الاستراتيجية الإبداعية', minutes=4, emoji='🤖', author='ma',
         excerpt='GenAI can generate 1,500 names in hours. It has simultaneously made human judgment more valuable than ever.',
         excerpt_ar='يستطيع الذكاء الاصطناعي التوليدي إنتاج 1,500 اسم في ساعات. وفي الوقت نفسه جعل الحكم البشري أثمن من أي وقت مضى.'),
]

CAT_KEY = {'Product Strategy': 'product', 'Digital Transformation': 'transformation', 'Product Thinking': 'thinking',
           'Brand Strategy': 'brand', 'Brand Identity': 'brand', 'Design Systems': 'brand', 'Creative Strategy': 'brand', 'Experience Design': 'brand'}


def _author_chip(key):
    a = AUTHORS[key]
    return f'<span class="author"><span class="avatar">{a["ini"]}</span><span data-ar="{esc(a["name_ar"])}">{esc(a["name"])}</span></span>'


def card(p, i=0, featured=False, soon=False):
    """One article row: category, title, excerpt, reading meta — no invented artwork."""
    tag = 'a' if not soon else 'div'
    hr = f' href="/blog/{p["slug"]}/"' if not soon else ''
    body_txt = p.get('card') or p['excerpt']
    foot = ('<span class="post-row__go"><span data-ar="اقرأ المقال">Read the article</span>' + icon('arrowUpRight', 'flip') + '</span>') if not soon else f'<span class="tag-soft tag-soft--soon" data-ar="قريبًا">Coming soon</span><span>~{p["minutes"]} <span data-ar="دقائق">min</span></span>'
    return f'''
          <{tag} class="post-row{' is-soon' if soon else ''}"{hr} data-category="{CAT_KEY.get(p['cat'], 'brand')}" data-reveal style="--d:{(i % 3) * .05:.2f}s">
            <span class="post-row__no">{i + 1:02d}</span>
            <div class="post-row__body">
              <div class="post-row__meta"><span class="tag-soft" data-ar="{esc(p['cat_ar'])}">{esc(p['cat'])}</span><span>{p['minutes']} <span data-ar="دقائق قراءة">min read</span></span><span>{_author_chip(p['author'])}</span></div>
              <h3 data-ar="{esc(p['title_ar'])}">{esc(p['title'])}</h3>
              <p data-ar="{esc(p['excerpt_ar'])}">{esc(body_txt)}</p>
            </div>
            <span class="post-row__foot">{foot}</span>
          </{tag}>'''


def hub(posts):
    feat = next(p for p in posts if p.get('featured'))
    total_min = sum(p['minutes'] for p in posts)
    cats = {}
    for p in posts:
        cats[p['cat']] = cats.get(p['cat'], 0) + 1
    topics = sorted(set(list(cats) + [c['cat'] for c in COMING_SOON]))
    counts = {'all': len(posts)}
    for p in posts:
        k = CAT_KEY[p['cat']]
        counts[k] = counts.get(k, 0) + 1
    filt = ''.join(f'<button class="filter{" is-active" if k == "all" else ""}" type="button" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}"><span data-ar="{esc(ar)}">{esc(en)}</span><b>{counts.get(k, 0)}</b></button>'
                   for k, en, ar in [('all', 'All', 'الكل'), ('product', 'Product Strategy', 'استراتيجية المنتج'), ('transformation', 'Digital Transformation', 'التحول الرقمي'), ('thinking', 'Product Thinking', 'التفكير المنتجي'), ('brand', 'Brand & Design', 'العلامة والتصميم')])
    cards = ''.join(card(p, i) for i, p in enumerate(posts))
    soon = ''.join(card(p, i, soon=True) for i, p in enumerate(COMING_SOON))
    topic_pills = ''.join(f'<span class="pill">{esc(t)}</span>' for t in topics)

    body = f'''
      <!-- ░░ Hero ░░ -->
      <section class="phero container phero--left" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('Insights', 'الرؤى', None)])}
        <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="قاعدة معرفة Code &amp; Canvas">Code &amp; Canvas · Knowledge Base</span></span>
        <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s"><span data-ar="أطر ومسائل">Frameworks and problems</span><br /><span class="grad-text" data-ar="من مشاريع فعلية.">from live engagements.</span></h1>
        <p class="hero__lead" data-reveal style="--d:.16s" data-ar-html="الاستراتيجية والعمارة وأنظمة العلامة والتفكير المنتجي والتحول الرقمي — &lt;strong&gt;مكتوبة لفريق يحتاج قرارًا، لا لفريق يبحث عن مصطلحات.&lt;/strong&gt; كل مقال منشور بالإنجليزية، والصفحات العربية متاحة للتنقّل.">Strategy, architecture, brand systems, product thinking and digital transformation — <strong>written for a team that has to decide something, not for one collecting buzzwords.</strong> Articles are published in English; the Arabic site carries the navigation and the summaries.</p>
        <div class="hero__ctas" data-reveal style="--d:.24s">{btn('Start with the most-read', 'ابدأ بالأكثر قراءة', f'#featured', 'primary', 'arrowDown')}{btn('Book a 30-min call', 'احجز مكالمة 30 دقيقة', '/contact/#book', 'glass')}</div>
      </section>

      <!-- ░░ At a glance ░░ -->
      <section class="section container section--tight" aria-label="The library at a glance" data-ar-label="المكتبة في أرقام">
        {facts([('Articles published', 'مقال منشور', str(len(posts)), True),
                ('Topics covered', 'موضوعًا مغطّى', str(len(topics)), True),
                ('Minutes of reading', 'دقيقة قراءة', f'~{total_min}', True),
                ('Founder perspectives', 'وجهتا نظر للمؤسسين', '2', True)])}
      </section>

      <!-- ░░ Featured ░░ -->
      <section class="section container section--flush-top" id="featured" aria-labelledby="feat-title">
        <p class="kicker" data-reveal><span data-ar="مقال مميز · الأكثر قراءة">Featured · Most read</span></p>
        <a class="feat-post panel" href="/blog/{feat['slug']}/" data-reveal>
          <div class="feat-post__body">
            <div class="post-row__meta"><span class="tag-soft" data-ar="{esc(feat['cat_ar'])}">{esc(feat['cat'])}</span><span>{feat['date']} · {feat['minutes']} <span data-ar="دقائق قراءة">min read</span></span>{_author_chip(feat['author'])}</div>
            <h2 id="feat-title" data-ar="{esc(feat['title_ar'])}">{esc(feat['title'])}</h2>
            <p data-ar="{esc(feat['excerpt_ar'])}">{esc(feat['excerpt'])}</p>
            <span class="post-row__go"><span data-ar="اقرأ المقال">Read the article</span>{icon('arrowUpRight', 'flip')}</span>
          </div>
          <div class="feat-post__plate" aria-hidden="true">
            <span class="feat-post__mark">{feat['emoji']}</span>
            <span class="story-plate__cap" data-ar="الأكثر قراءة">MOST READ</span>
            <span class="story-plate__cap2">{esc(feat['cat'])} · {feat['minutes']} <span data-ar="دقائق">min</span></span>
          </div>
        </a>
      </section>

      <!-- ░░ All articles ░░ -->
      <section class="section container section--flush-top" id="articles" aria-labelledby="all-title">
        {sec_head('01', 'THE LIBRARY', 'المكتبة',
                  '<span id="all-title" data-ar="كل المقالات.">Every article.</span>',
                  'Filter by topic, or read straight down — each row states its category, reading time and author before you commit to it.',
                  'رشّح حسب الموضوع أو اقرأ بالتتابع — كل صف يوضّح تصنيفه ووقت قراءته وكاتبه قبل أن تبدأ.')}
        <div class="toolbar" data-reveal>
          <div class="filters" role="group" aria-label="Browse by topic" data-ar-label="تصفّح حسب الموضوع" data-filter-group="#post-list">{filt}</div>
        </div>
        <div class="post-list" id="post-list">{cards}{soon}
        </div>
      </section>

      <!-- ░░ Subscribe ░░ -->
      <section class="section container section--flush-top" aria-labelledby="sub-title">
        <div class="callout panel" data-reveal>
          <div>
            <p class="kicker"><span data-ar="ابقَ على اطلاع · بلا رسائل مزعجة">Stay informed · No spam</span></p>
            <h3 id="sub-title"><span data-ar="احصل على الرؤى">Get insights</span> <span class="grad-text" data-ar="قبل الجميع.">before everyone else.</span></h3>
            <p data-ar="أطر جديدة ودراسات حالة وأدلة استراتيجية — تصلك عند نشرها. تركيز على الاستراتيجية. بلا حشو.">New frameworks, case studies, and strategic guides — delivered when they're published. Strategy-focused. No filler.</p>
          </div>
          <form class="form subscribe" data-form="contact" data-integration="newsletter" data-whatsapp="" data-mail="info@codeandcanvas.net" data-subject="Newsletter subscription — Code &amp; Canvas" data-endpoint="" novalidate>
            <input type="text" name="_hp" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px" />
            <div class="subscribe__row">
              <div class="field"><label class="sr-only" for="sub-email" data-ar="بريدك الإلكتروني">Your e-mail</label><input id="sub-email" name="email" type="email" required placeholder="you@company.com" autocomplete="email" /><span class="field__err" data-ar="أدخل بريدًا صحيحًا">Please enter a valid e-mail</span></div>
              <input type="hidden" name="inquiry" value="Newsletter subscription" />
              <button class="btn btn--primary" type="submit"><span data-ar="اشترك ←">Subscribe →</span></button>
            </div>
            <div class="form__status" role="status" aria-live="polite"></div>
            <ul class="promises promises--inline" aria-label="Promises" data-ar-label="وعود"><li>{icon('check')}<span data-ar="بلا رسائل مزعجة أبدًا">No spam, ever</span></li><li>{icon('check')}<span data-ar="إلغاء الاشتراك في أي وقت">Unsubscribe anytime</span></li><li>{icon('check')}<span data-ar="رؤى المنتج والعلامة فقط">Product &amp; Brand insights only</span></li><li>{icon('check')}<span data-ar="السعودية + مصر · MENA">KSA + Egypt · MENA</span></li></ul>
          </form>
        </div>
      </section>
'''
    return page('/blog/', title='Insights Hub — Code & Canvas', title_ar='مركز الرؤى — Code & Canvas',
                desc='Strategy, architecture, brand systems, product thinking, and digital transformation. Frameworks and insights for leaders building organizations across MENA — without the buzzwords.',
                desc_ar='الاستراتيجية والعمارة وأنظمة العلامة والتفكير المنتجي والتحول الرقمي. أطر ورؤى للقادة الذين يبنون مؤسسات في المنطقة — بلا مصطلحات رنانة.',
                nav='blog', body=body)


def article(p, by_slug):
    a = AUTHORS[p['author']]
    stats = ''.join(f'<div><strong>{esc(n)}</strong><span>{esc(l)}</span></div>' for n, l in p['stats'])
    cta = p.get('cta') or {}
    prim = cta.get('primary', ('Book a Free Discovery Call', '/contact/#book'))
    sec = cta.get('secondary', ('Explore Services', '/services/'))
    cta_html = f'''
<aside class="cta-box">
  <div><p class="meta">{esc(cta.get('k', 'Code & Canvas'))}</p><h3>{esc(cta.get('h', ''))}</h3><p>{esc(cta.get('p', ''))}</p></div>
  <div class="cta-box__actions"><a class="btn btn--primary" href="{prim[1]}"><span>{esc(prim[0])}</span><i class="flip" data-icon="arrowUpRight"></i></a><a class="btn btn--glass" href="{sec[1]}"><span>{esc(sec[0])}</span></a></div>
</aside>''' if cta else ''
    tk = p.get('takeaways')
    tk_html = ''
    if tk:
        title, sub, items = tk[0], tk[1], tk[2]
        numbered = len(tk) > 3 and tk[3]
        li = ''.join(f'<li>{x}</li>' for x in items)
        lst = f'<ol class="tk-list tk-list--num">{li}</ol>' if numbered else f'<ul class="tk-list">{li}</ul>'
        tk_html = f'<section class="takeaways" id="takeaways"><h2>{esc(title)}</h2><p class="meta">{esc(sub)}</p>{lst}</section>'
    concl = p.get('conclusion')
    concl_html = f'<h2 id="conclusion">{esc(concl[0])}</h2>{concl[1]}' if concl else ''
    main_tail = (concl_html + tk_html) if p.get('takeaways_after_conclusion') else (tk_html + concl_html)
    faq_html = ''
    if p.get('faq'):
        items = ''.join(f'''
      <div class="faq__item"><button class="faq__q" type="button" aria-expanded="false"><span>{esc(q)}</span><span class="pm" aria-hidden="true"></span></button><div class="faq__a"><div><p>{ans}</p></div></div></div>''' for q, ans in p['faq'][1])
        faq_html = f'<h2 id="faq">Frequently Asked Questions</h2><p class="meta">{esc(p["faq"][0])}</p><div class="faq faq--prose">{items}</div>'
    related = ''
    for s in p.get('related', []):
        r = by_slug.get(s)
        if r:
            related += card({'slug': r['slug'], 'cat': r['cat'], 'cat_ar': r['cat_ar'], 'title': r['title'], 'title_ar': r['title_ar'], 'excerpt': r['excerpt'], 'excerpt_ar': r['excerpt_ar'], 'minutes': r['minutes'], 'date': r['date'], 'author': r['author'], 'emoji': r['emoji']})
        else:
            cs = next((c for c in COMING_SOON if s in ('creative-strategy-generative-ai-age', 'brand-identity-to-brand-systems') and ((s.startswith('creative') and c['cat'] == 'Creative Strategy') or (s.startswith('brand') and c['cat'] == 'Brand Identity'))), None)
            if cs:
                related += card(cs, soon=True)
    toc_items = [(m.group(1), re.sub(r'<[^>]+>', '', m.group(2))) for m in re.finditer(r'<h2 id="([^"]+)">(.*?)</h2>', p['body'])]
    if tk: toc_items.append(('takeaways', tk[0]))
    if concl: toc_items.append(('conclusion', concl[0]))
    if p.get('faq'): toc_items.append(('faq', 'Frequently Asked Questions'))
    toc_html = ''.join(f'<a href="#{i}">{esc(t)}</a>' for i, t in toc_items)
    links = ''.join(f'<a class="text-link" href="{h}"{" target=_blank rel=noopener" if h.startswith("http") else ""}><span data-ar="{esc(ar)}">{esc(en)}</span></a>' for en, ar, h in a['links'])

    body = f'''
      <article class="post container" aria-labelledby="post-title">
        <header class="post__head">
          {crumbs([('Home', 'الرئيسية', '/'), ('Insights', 'الرؤى', '/blog/'), (p['cat'], p['cat_ar'], None)])}
          <div class="post__meta" data-reveal><span class="badge" data-ar="{esc(p['cat_ar'])}">{esc(p['cat'])}</span><span>{icon('clock')}{p['minutes']} <span data-ar="دقائق قراءة">min read</span></span><span>{icon('calendar')}{p['date']}</span><span>{_author_chip(p['author'])}</span></div>
          <h1 class="post__title" id="post-title" data-reveal style="--d:.06s" data-ar="{esc(p['title_ar'])}">{esc(p['title'])}</h1>
          <p class="post__excerpt" data-reveal style="--d:.12s" data-ar="{esc(p['excerpt_ar'])}">{esc(p['excerpt'])}</p>
          <p class="post__lang-note" data-ar="هذه المقالة منشورة بالإنجليزية كما كُتبت.">This article is published in English.</p>
        </header>
        <div class="post__cover" data-reveal>
          <div class="art art--wide {'art--pink' if p['author'] == 'ma' else 'art--violet'}" data-slot="blog/{p['slug']}/cover"><span class="art__mark" style="font-size:96px">{p['emoji']}</span><span class="art__cap">{esc(p['cat'])} · Code &amp; Canvas</span></div>
        </div>
        <div class="post__layout">
          <div class="post__body prose" dir="ltr" lang="en">
            <div class="post__stats">{stats}</div>
            {p['body']}
            {cta_html}
            {main_tail}
            {faq_html}
            <aside class="author-box">
              <span class="avatar avatar--lg">{a['ini']}</span>
              <div><strong>{esc(a['name'])}</strong><p class="meta">{esc(p.get('author_line') or a['line'])}</p><p>{esc(p.get('author_bio') or a['bio'])}</p><div class="author-box__links">{links}</div></div>
            </aside>
          </div>
          <aside class="post__side">
            <nav class="toc panel" aria-label="On this page" data-ar-label="في هذه الصفحة"><h4 data-ar="في هذه الصفحة">On this page</h4><div class="toc__list">{toc_html}</div></nav>
            <div class="panel tier" style="margin-top:14px">
              <p class="kicker"><span data-ar="ناقش هذا المقال">Discuss this article</span></p>
              <p data-ar="احجز مكالمة استكشافية مدتها 30 دقيقة — نأتي مستعدين، لا بعرض مبيعات.">Book a 30-minute discovery call — we come prepared, not with a pitch.</p>
              <div class="book-card__actions">{btn('Book a Free Call', 'احجز مكالمة مجانية', '/contact/#book')}</div>
            </div>
          </aside>
        </div>
        <section class="related">
          <div class="head-split"><h2 class="section__title" style="font-size:clamp(22px,2.4vw,30px)" data-ar="تابع القراءة">Continue reading</h2><a class="text-link" href="/blog/"><span data-ar="كل الرؤى ←">View all insights →</span></a></div>
          <div class="post-list">{related}
          </div>
        </section>
      </article>
'''
    url = f'https://codeandcanvas.net/blog/{p["slug"]}/'
    author_ld = PERSON_LD['mustafa'] if p['author'] == 'ma' else {'@type': 'Organization', '@id': 'https://codeandcanvas.net/#org'}
    article = {'@type': 'Article', 'headline': p['title'], 'description': p['excerpt'], 'url': url, 'mainEntityOfPage': url,
               'inLanguage': 'en', 'articleSection': p['cat'], 'timeRequired': f'PT{p["minutes"]}M', 'datePublished': '2026-06',
               'author': author_ld, 'publisher': {'@id': 'https://codeandcanvas.net/#org'},
               'image': 'https://codeandcanvas.net/assets/brand/og-default.png'}
    return page(f'/blog/{p["slug"]}/', title=f'{p.get("page_title") or p["title"]} — Code & Canvas', title_ar=f'{p["title_ar"]} — Code & Canvas',
                desc=p['excerpt'], desc_ar=p['excerpt_ar'], nav='blog', body=body, og_type='article', ld=[article])


def build():
    posts = all_posts()
    by_slug = {p['slug']: p for p in posts}
    out = [hub(posts)]
    for p in posts:
        out.append(article(p, by_slug))
    return out
