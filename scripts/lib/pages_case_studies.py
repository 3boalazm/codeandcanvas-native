# -*- coding: utf-8 -*-
"""/work/<project>/ — 15 detailed, bilingual, evidence-led project case studies.

Each page documents one distinct project from the owner-supplied live URLs and
GitHub repositories. The structure is identical on purpose: problem, approach,
role, concrete build, verifiable checks, source links and explicit evidence
limits. Artwork is illustrative and labelled; no client screenshot or outcome
is implied. Source data lives in scripts/lib/data_case_studies.py.
"""
from h import esc, crumbs, btn, closing, page, media_img, sec_head, icon
from data_case_studies import CASE_STUDIES, LABELS

CSS = '    <link rel="stylesheet" href="/assets/css/case-study.css" />\n'
TRACKS = {
    'identity': ('IDENTITY SYSTEM', 'منظومة هوية'),
    'product': ('DIGITAL PRODUCT', 'منتج رقمي'),
}


def _b(en, ar, tag='span', cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<{tag}{c} data-ar="{esc(ar)}">{esc(en)}</{tag}>'


def _li(en, ar, cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<li{c} data-ar="{esc(ar)}">{esc(en)}</li>'


def _ext(url, en, ar):
    return (f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer">'
            f'<span data-ar="{esc(ar)}">{esc(en)}</span></a>')


def _case_page(c):
    L = LABELS
    slug = c['slug']
    path = f'/work/{slug}/'
    title = f"{c['title']} — Detailed Project Case Study · Code & Canvas"
    title_ar = f"{c['title_ar']} — دراسة حالة تفصيلية للمشروع · Code & Canvas"

    facts = ''.join([
        f'<li><b class="wa-card__year">{esc(c["year"])}</b><span data-ar="{esc(c["status_ar"])}">{esc(c["status"])}</span></li>',
        f'<li><b data-ar="{esc(TRACKS[c["track"]][1])}">{esc(TRACKS[c["track"]][0])}</b></li>',
        f'<li><b data-ar="{esc(c["kicker_ar"])}">{esc(c["kicker"])}</b></li>',
    ])

    hero = f'''
      <section class="phero container phero--left phero--tight cs-hero" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('Work', 'أعمالنا', '/work/'), (c['title'], c['title_ar'], None)])}
        <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span>{_b(*L['case_eyebrow'])}</span>
        <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s" data-ar="{esc(c['title_ar'])}">{esc(c['title'])}</h1>
        <p class="hero__lead" data-reveal style="--d:.16s" data-ar="{esc(c['lede_ar'])}">{esc(c['lede'])}</p>
        <ul class="cs-facts" data-reveal style="--d:.22s">{facts}</ul>
        <div class="hero__ctas" data-reveal style="--d:.28s">{btn('Back to the work index', 'العودة إلى فهرس الأعمال', '/work/', 'primary', 'grid')}{btn('Book a 30-min call', 'احجز مكالمة 30 دقيقة', '/book/', 'glass', 'calendar')}</div>
      </section>'''

    visual = f'''
      <section class="section container section--tight" aria-label="Illustrative case artwork" data-ar-label="عمل فني توضيحي لدراسة الحالة">
        <figure class="cs-figure" data-reveal>
          {media_img(c['media'], c['alt'], c['alt_ar'], eager=True, fetchpriority='high', sizes='(max-width: 720px) 92vw, 1400px')}
          <figcaption>{_b(c['title'], c['title_ar'])}<span class="cs-figure__disclaimer" data-ar="{esc(L['illustrative'][1])}">{esc(L['illustrative'][0])}</span></figcaption>
        </figure>
        <p class="live-media-note" data-ar="{esc(L['figure_note'][1])}">{esc(L['figure_note'][0])}</p>
      </section>'''

    problem = f'''
      <section class="section container section--flush-top" id="problem" aria-labelledby="problem-title">
        {sec_head(L['sec1'][0], L['sec1'][1], L['sec1'][2],
                  '<span id="problem-title" data-ar="المشكلة أولًا.">The problem, first.</span> <span class="grad-text" data-ar="ثم القرار.">Then the decision.</span>',
                  L['sec1_lead'][0], L['sec1_lead'][1])}
        <div class="cs-triad">
          <article class="cs-panel" data-reveal><span class="cs-panel__label" data-ar="{esc(L['p_problem'][1])}">{esc(L['p_problem'][0])}</span><p data-ar="{esc(c['problem_ar'])}">{esc(c['problem'])}</p></article>
          <article class="cs-panel" data-reveal style="--d:.06s"><span class="cs-panel__label" data-ar="{esc(L['p_approach'][1])}">{esc(L['p_approach'][0])}</span><p data-ar="{esc(c['approach_ar'])}">{esc(c['approach'])}</p></article>
          <article class="cs-panel" data-reveal style="--d:.12s"><span class="cs-panel__label" data-ar="{esc(L['p_role'][1])}">{esc(L['p_role'][0])}</span><p data-ar="{esc(c['role'][1])}">{esc(c['role'][0])}</p></article>
        </div>
      </section>'''

    build_items = ''.join(_li(e, a) for e, a in c['build'])
    stack_items = ''.join(_li(e, a) for e, a in c['stack'])
    build = f'''
      <section class="section container section--flush-top" id="build" aria-labelledby="build-title">
        {sec_head(L['sec2'][0], L['sec2'][1], L['sec2'][2],
                  f'<span id="build-title">{_b("Concrete deliverables.", "مخرجات ملموسة.")} <span class="grad-text" data-ar="لا صفات.">Not adjectives.</span></span>',
                  L['sec2_lead'][0], L['sec2_lead'][1])}
        <div class="cs-build-grid">
          <article class="cs-panel" data-reveal><span class="cs-panel__label" data-ar="{esc(L['p_build'][1])}">{esc(L['p_build'][0])}</span><ol class="cs-list">{build_items}</ol></article>
          <aside class="cs-panel" data-reveal style="--d:.08s"><span class="cs-panel__label" data-ar="{esc(L['p_stack'][1])}">{esc(L['p_stack'][0])}</span><ul class="cs-stack">{stack_items}</ul></aside>
        </div>
      </section>'''

    keeps = ''.join(_li(e, a) for e, a in c['keeps'])
    links = []
    if c['live']:
        links.append(f'<li>{_ext(c["live"], L["p_live"][0], L["p_live"][1])}</li>')
    else:
        links.append(f'<li class="cs-links__pending" data-ar="{esc(L["p_live_none"][1])}">{esc(L["p_live_none"][0])}</li>')
    if c['repo']:
        links.append(f'<li>{_ext(c["repo"], L["p_repo"][0], L["p_repo"][1])}</li>')
    else:
        links.append(f'<li class="cs-links__pending" data-ar="{esc(L["p_repo_none"][1])}">{esc(L["p_repo_none"][0])}</li>')
    links.append('<li><a href="/work/#project-cases"><span data-ar="كل دراسات المشاريع ←">All project case studies →</span></a></li>')

    source_note = ''
    if c.get('source_note'):
        source_note = (f'<p class="cs-source-note"><strong data-ar="{esc(L["p_source"][1])}">{esc(L["p_source"][0])}</strong> · '
                       f'<span data-ar="{esc(c["source_note"][1])}">{esc(c["source_note"][0])}</span></p>')

    verify = f'''
      <section class="section container section--flush-top" id="verify" aria-labelledby="verify-title">
        {sec_head(L['sec3'][0], L['sec3'][1], L['sec3'][2],
                  f'<span id="verify-title">{_b("The source is in front of you.", "المصدر قدّامك.")}</span>',
                  L['sec3_lead'][0], L['sec3_lead'][1])}
        <div class="cs-verify-grid">
          <article class="cs-panel" data-reveal><span class="cs-panel__label" data-ar="{esc(L['p_keeps'][1])}">{esc(L['p_keeps'][0])}</span><ul class="cs-list">{keeps}</ul></article>
          <article class="cs-panel" data-reveal style="--d:.08s"><span class="cs-panel__label" data-ar="روابط المصدر">SOURCE LINKS</span><ul class="cs-links">{''.join(links)}</ul></article>
        </div>
        {source_note}
      </section>'''

    evidence = f'''
      <section class="section container section--flush-top cs-evidence" id="evidence" aria-labelledby="evidence-title">
        {sec_head(L['sec4'][0], L['sec4'][1], L['sec4'][2],
                  f'<span id="evidence-title">{_b("What we say, and what we do not.", "ما نقوله، وما لا نقوله.")}</span>',
                  L['sec4_lead'][0], L['sec4_lead'][1])}
        <div class="work-disclaimer" data-reveal>
          {icon('alert')}
          <div>
            <strong data-ar="صورة جميلة ليست إثباتًا.">An attractive image is not evidence.</strong>
            <p data-ar="{esc(c['evidence'][1])}">{esc(c['evidence'][0])}</p>
          </div>
        </div>
        <div class="cs-evidence-grid" style="margin-top:16px">
          <article class="cs-panel" data-reveal><span class="cs-panel__label" data-ar="حدود الدور">ROLE BOUNDARY</span><p data-ar="{esc(c['role'][1])}">{esc(c['role'][0])}</p></article>
          <article class="cs-panel" data-reveal style="--d:.08s"><span class="cs-panel__label" data-ar="{esc(L['p_status'][1])}">{esc(L['p_status'][0])}</span><p data-ar="{esc(c['status_ar'])}">{esc(c['status'])}</p><p style="margin-top:10px" data-ar="لا ننشر شهادات عملاء ولا أرقام نتائج ولا لقطات شاشة غير معتمدة لهذا المشروع.">No client testimonial, measured result or unapproved screenshot is published for this project.</p></article>
        </div>
        <div class="cs-evidence-foot">
          <a href="/work/" data-track="case_study_view" data-track-id="{esc(slug)}"><span data-ar="{esc(L['p_index'][1])}">{esc(L['p_index'][0])}</span></a>
          <a href="/claims/"><span data-ar="{esc(L['p_claims'][1])}">{esc(L['p_claims'][0])}</span></a>
        </div>
      </section>'''

    close = closing(
        'NEXT STEP', 'الخطوة التالية',
        '<span data-ar="عندك موجز شبيه؟">Have a brief like this?</span> <span class="grad-text" data-ar="لنحدّد أول خطوة.">Let’s name the first step.</span>',
        'Send the problem in one message, or book a 30-minute call. We reply with a scope, a price, or an honest “not the right fit”.',
        'أرسل المشكلة في رسالة واحدة، أو احجز مكالمة 30 دقيقة. نرد بنطاق أو سعر أو «لسنا الخيار المناسب» بصراحة.',
        [btn('Start a scoped inquiry', 'ابدأ استفسارًا بنطاق', '/contact/?inquiry=custom#message', 'primary', 'mail'),
         btn('Book a 30-min call', 'احجز مكالمة 30 دقيقة', '/book/', 'glass', 'calendar')])

    body = hero + visual + problem + build + verify + evidence + close
    return page(path, title=title, title_ar=title_ar, desc=c['lede'], desc_ar=c['lede_ar'], nav='work',
                body=body, body_class='case-study-page', extra_head=CSS,
                og_image=f'/assets/brand/og/case-{slug}.png', view_track='case_study_view')


def case_studies_section():
    """The /work/ index section: 15 compact cards, each opening a full page."""
    cards = []
    for c in CASE_STUDIES:
        track_en, track_ar = TRACKS[c['track']]
        cards.append(f'''
          <a class="cs-index-card" href="/work/{esc(c['slug'])}/" data-track="case_study_view" data-track-id="{esc(c['slug'])}">
            <figure class="cs-index-card__art">
              {media_img(c['media'], c['alt'], c['alt_ar'], sizes='(max-width: 640px) 92vw, (max-width: 980px) 46vw, 400px')}
              <figcaption class="cs-index-card__badge" data-ar="توضيحي">ILLUSTRATIVE</figcaption>
            </figure>
            <div class="cs-index-card__body">
              <div class="cs-index-card__meta"><span class="wa-card__year">{esc(c['year'])}</span><span data-ar="{esc(track_ar)}">{esc(track_en)}</span></div>
              <h3 data-ar="{esc(c['title_ar'])}">{esc(c['title'])}</h3>
              <p data-ar="{esc(c['lede_ar'])}">{esc(c['lede'])}</p>
              <span class="cs-index-card__cta" data-ar="اقرأ دراسة الحالة ←">Read the case study →</span>
            </div>
          </a>''')
    return f'''
      <section class="section container section--flush-top" id="project-cases" aria-labelledby="project-cases-title">
        {sec_head('03', 'PROJECT CASE STUDIES', 'دراسات حالة المشاريع',
                  '<span id="project-cases-title" data-ar="خمسة عشر مشروعًا.">Fifteen projects.</span> <span class="grad-text" data-ar="صفحة موثّقة لكل واحد.">One documented page each.</span>',
                  'Detailed bilingual pages drawn from the supplied live deployments and repositories: problem, approach, founder role, concrete build, source links and evidence limits.',
                  'صفحات ثنائية اللغة تفصيلية من المواقع المباشرة والمستودعات المُقدَّمة: المشكلة، والمنهج، ودور المؤسس، وما بُني، وروابط المصدر، وحدود الإثبات.')}
        <div class="work-disclaimer work-disclaimer--archive" data-reveal>
          {icon('alert')}
          <div>
            <strong data-ar="توثيق مشاريع المؤسس، وليس ادعاءات عملاء مُثبتة.">Founder projects, documented — not verified studio client claims.</strong>
            <p data-ar="كل صورة هنا عمل توضيحي مولّد لهذا الموقع ومُعلَّن بوضوح. لا نعيد نشر صور المنتجات أو لقطات الشاشة من المواقع المباشرة، ولا ندّعي نتائج مُقاسة أو تعاقدات عملاء. ثلاث ريبهات من القائمة غير متاحة للعامة؛ حالتها موضحة داخل صفحتها.">Every image here is generated illustrative artwork, clearly labelled. We do not republish product photography or screenshots from the live sites, and we claim no measured outcomes or client engagements. Three supplied repositories are not publicly reachable; their status is stated on the relevant page.</p>
          </div>
        </div>
        <div class="cs-index-grid">{''.join(cards)}</div>
        <p class="live-media-note cs-index-note" data-ar="الصور أعمال توضيحية مولّدة، ليست لقطات شاشة للمنتجات ولا صور عملاء. الروابط الخارجية تفتح في تبويب جديد.">Artwork is generated and illustrative, not product screenshots or client photography. External links open in a new tab.</p>
      </section>'''


def build():
    return [_case_page(c) for c in CASE_STUDIES]
