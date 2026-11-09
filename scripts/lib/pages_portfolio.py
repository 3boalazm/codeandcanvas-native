# -*- coding: utf-8 -*-
"""/work/ — the visual portfolio hub, four *labelled* concept case studies, and
the founder work archive (25 re-indexed projects, see data_founder_work.py).

Honesty contract: generated imagery is illustrative studio artwork. It is never
captioned as a client deliverable, never presented as a product screenshot and
never paired with a fabricated result. The archive documents the co-founder's
own published projects with links back to their sources; it does not promote
them to verified studio client engagements. Real client cases stay in
/case-studies/ with their published evidence limits, and new ones enter through
the permission / evidence / attribution gate described on this page and in
docs/ASSET-AND-CLAIM-REGISTER.md.
"""
from h import esc, icon, crumbs, closing, btn, page, sec_head, facts, media_img
from data_growth import PORTFOLIO, CONCEPT_LABEL, CONCEPT_LABEL_AR, EVIDENCE, EVIDENCE_AR
from data_founder_work import FOUNDER_WORK, IDENTITY, PRODUCT
from data_case_studies import archive_case_slug
from pages_case_studies import case_studies_section, CSS

MEDIA = '/assets/media/'
CAT_KEY = {'Brand Identity': 'brand', 'Packaging & Print': 'packaging', 'Digital Products': 'product', 'Web Experiences': 'web'}


def tile(p, i=0):
    return f'''
      <article class="work-tile" data-category="{CAT_KEY[p['cat']]}" data-reveal style="--d:{(i % 2) * .06:.2f}s">
        <div class="work-tile__media">
          {media_img(p['media'], CONCEPT_LABEL + ' — ' + p['title'], CONCEPT_LABEL_AR + ' — ' + p['title_ar'], sizes='(max-width: 720px) 92vw, (max-width: 1024px) 46vw, 520px')}
          <span class="work-tile__badge" data-ar="دراسة مفاهيمية · ليست عمل عميل">CONCEPT STUDY · NOT CLIENT WORK</span>
          <span class="work-tile__cat" data-ar="{esc(p['cat_ar'])}">{esc(p['cat'])}</span>
        </div>
        <div class="work-tile__body">
          <h3 data-ar="{esc(p['title_ar'])}">{esc(p['title'])}</h3>
          <p data-ar="{esc(p['lede_ar'])}">{esc(p['lede'])}</p>
          <div class="work-tile__foot">
            <span data-ar="المشكلة · الاستراتيجية · الدور · التنفيذ · النتيجة">Problem · Strategy · Role · Execution · Outcome</span>
            <a href="/work/{esc(p['slug'])}/" data-track="case_study_view" data-track-id="{esc(p['slug'])}"><span data-ar="افتح دراسة الحالة">Open the case study</span> ↗</a>
          </div>
        </div>
      </article>'''


def archive_card(w):
    """One compact, bilingual archive row. No imagery is republished here: the
    founder's visuals stay on his own case-study pages, which every card links
    to. External links are explicitly external; internal ones are rewritten by
    the AR generator like every other first-party route."""
    tags = ''.join(
        f'<li data-ar="{esc(ar)}">{esc(en)}</li>'
        for en, ar in zip(w['tags'], w['tags_ar'])
    )
    links = []
    if w['case']:
        links.append(('Case study ↗', 'دراسة الحالة ↗', w['case']))
    if w['live']:
        links.append(('Live ↗', 'الموقع المباشر ↗', w['live']))
    if w['repo']:
        links.append(('Code ↗', 'الكود ↗', w['repo']))
    if w['own']:
        links.append(('Our notes →', 'ملاحظاتنا →', w['own']))
    slug = archive_case_slug(w)
    if slug:
        links.insert(0, ('Detailed case study →', 'دراسة الحالة المفصلة →', f'/work/{slug}/'))
    link_html = ''.join(
        f'<a href="{esc(url)}"'
        + (' target="_blank" rel="noopener noreferrer"' if url.startswith('http') else '')
        + f'><span data-ar="{esc(ar)}">{esc(en)}</span></a>'
        for en, ar, url in links
    )
    status = (f'<span class="wa-card__status" data-ar="{esc(w["status_ar"])}">{esc(w["status"])}</span>'
              if w['status'] else '')
    return f'''
      <article class="wa-card" data-category="{w['track']}">
        <div class="wa-card__top"><span class="wa-card__no">{w['no']}</span><span class="wa-card__year">{esc(w['year'])}</span>{status}</div>
        <h3 data-ar="{esc(w['title_ar'])}">{esc(w['title'])}</h3>
        <p data-ar="{esc(w['desc_ar'])}">{esc(w['desc'])}</p>
        <ul class="wa-card__tags">{tags}</ul>
        <div class="wa-card__links">{link_html}</div>
      </article>'''


def archive_section():
    """Section 02: the founder's 25 published projects, re-indexed in our
    two-track order (identity first, then digital products) with a local filter."""
    cats = [('all', 'All · 25', 'الكل · 25'), ('identity', 'Identity · 8', 'الهوية · 8'), ('product', 'Digital products · 17', 'المنتجات الرقمية · 17')]
    filters = ''.join(
        f'<button type="button" class="filter{" is-active" if k == "all" else ""}" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}"><span data-ar="{esc(ar)}">{esc(en)}</span></button>'
        for k, en, ar in cats
    )
    identity = ''.join(archive_card(w) for w in IDENTITY)
    product = ''.join(archive_card(w) for w in PRODUCT)
    return f'''
      <section class="section container section--flush-top" id="archive" aria-labelledby="archive-title">
        {sec_head('02', 'FOUNDER WORK ARCHIVE', 'أرشيف أعمال المؤسس',
                  '<span id="archive-title" data-ar="خمسة وعشرون مشروعًا.">Twenty-five projects.</span> <span class="grad-text" data-ar="مصدر واحد للتحقق.">One place to check them.</span>',
                  'Selected work by co-founder Mustafa Aboalazm, re-indexed in our two-track order. Every entry links back to its source; overlapping projects also open a detailed bilingual case study.',
                  'أعمال مختارة للمؤسس الشريك مصطفى أبو العزم، مُرتبة من جديد وفق مسارينا. كل مدخل يعود إلى مصدره؛ والمشروعات المشتركة تفتح أيضًا دراسة حالة ثنائية اللغة مفصلة.')}
        <div class="work-disclaimer work-disclaimer--archive">
          {icon('alert')}
          <div>
            <strong data-ar="توثيق أعمال المؤسس، وليس ادعاءات عملاء مُثبتة.">Founder work, documented — not verified studio client claims.</strong>
            <p data-ar="هذه مشاريع نشرها مصطفى في بورتفوليوه الخاص وريبوGitHub العام. نُدرجها هنا كفهرس موثّق يبدأ بالهوية ثم المنتجات الرقمية، مع روابط للتحقق. لا نقدّمها كتعاقدات عملاء مُثبتة للاستوديو، ولا ندّعي نتائج مُقاسة، ولا نعيد نشر صوره دون إذن. الحالات التي لها حدود إثبات منشورة عندنا تظهر في صفحة دراسات الحالة.">These projects were published by Mustafa on his own portfolio and public GitHub repositories. We index them here — identity first, then digital products — with links back to the source. We do not present them as verified studio client engagements, claim measured outcomes, or republish his imagery without permission. Cases with published evidence limits live on our case-studies page.</p>
          </div>
        </div>
        <div class="work-filters" role="group" aria-label="Filter founder work" data-ar-label="تصفية أعمال المؤسس" data-filter-group="#archive">{filters}</div>
        <h3 class="wa-track" data-category="identity"><span data-ar="المسار ٠١ · أنظمة الهوية">TRACK 01 · IDENTITY SYSTEMS</span><b>8</b></h3>
        <div class="wa-grid">{identity}
        </div>
        <h3 class="wa-track" data-category="product"><span data-ar="المسار ٠٢ · المنتجات الرقمية والهندسة">TRACK 02 · DIGITAL PRODUCTS &amp; ENGINEERING</span><b>17</b></h3>
        <div class="wa-grid">{product}
        </div>
        <p class="live-media-note" data-ar="التصفية تعمل محليًا دون إرسال أي بيانات. الروابط الخارجية تفتح في تبويب جديد.">Filtering runs locally; nothing is sent. External links open in a new tab.</p>
        <p class="live-media-note"><a href="https://github.com/3boalazm?tab=repositories" target="_blank" rel="noopener noreferrer"><span data-ar="كل المستودعات العامة على GitHub ↗">All public repositories on GitHub ↗</span></a> · <span data-ar="سجل المصادر وحدود الإثبات: docs/FOUNDER-WORK-ARCHIVE.md">Sources and evidence limits: <code>docs/FOUNDER-WORK-ARCHIVE.md</code></span></p>
      </section>'''


def case_page(p):
    steps = ''.join(f'<li data-ar="{esc(a)}">{esc(e)}</li>' for e, a in zip(p['execution'], p['execution_ar']))
    deliverables = ''.join(f'<li data-ar="{esc(a)}">{esc(e)}</li>' for e, a in zip(p['deliverables'], p['deliverables_ar']))
    body = f'''
      <section class="phero container phero--left" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('Work', 'أعمالنا', '/work/'), (p['cat'], p['cat_ar'], None)])}
        <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="دراسة حالة · مفاهيمية">CASE STUDY · CONCEPT</span></span>
        <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s" data-ar="{esc(p['title_ar'])}">{esc(p['title'])}</h1>
        <p class="hero__lead" data-reveal style="--d:.16s" data-ar="{esc(p['lede_ar'])}">{esc(p['lede'])}</p>
        <div class="hero__ctas" data-reveal style="--d:.24s">{btn('Discuss a similar brief', 'ناقش موجزًا مشابهًا', '/contact/?inquiry=custom#message', 'primary', 'chat')}{btn('Book a 30-min call', 'احجز مكالمة 30 دقيقة', '/book/', 'glass', 'calendar')}</div>
      </section>

      <section class="section container section--tight" aria-label="Case study visual" data-ar-label="العمل الفني لدراسة الحالة">
        <figure class="live-figure live-figure--wide">
          {media_img(p['media'], CONCEPT_LABEL + ' — ' + p['title'], CONCEPT_LABEL_AR + ' — ' + p['title_ar'], sizes='(max-width: 720px) 92vw, 1200px')}
          <figcaption><span data-ar="{esc(p['cat_ar'])}">{esc(p['cat'])}</span><span class="live-figure__disclaimer" data-ar="{esc(CONCEPT_LABEL_AR)}">{esc(CONCEPT_LABEL)}</span></figcaption>
        </figure>
        <p class="live-media-note" data-ar="عمل فني توضيحي أُنشئ لهذا الموقع. ليس لقطة شاشة لمنتج، ولا صورة لتغليف عميل، ولا إثباتًا على نتيجة عمل.">Illustrative artwork created for this site. It is not a product screenshot, a photograph of a client pack, or evidence of a business result.</p>
      </section>

      <section class="section container section--flush-top" id="case" aria-labelledby="case-title">
        {sec_head('01', 'THE CASE STRUCTURE', 'بنية دراسة الحالة', '<span id="case-title" data-ar="كل مشروع يُروى بنفس الصراحة.">Every project is told with the same honesty.</span>',
                  'Problem, strategy, our role, execution and an outcome that states exactly what is — and is not — proven.',
                  'المشكلة، والاستراتيجية، ودورنا، والتنفيذ، ونتيجة توضّح بالضبط ما هو مُثبَت وما ليس كذلك.')}
        <div class="case-steps">
          <article class="case-step" data-reveal><span>01 · PROBLEM</span><h3 data-ar="المشكلة">The problem</h3><p data-ar="{esc(p['problem_ar'])}">{esc(p['problem'])}</p></article>
          <article class="case-step" data-reveal style="--d:.06s"><span>02 · STRATEGY</span><h3 data-ar="الاستراتيجية">The strategy</h3><p data-ar="{esc(p['strategy_ar'])}">{esc(p['strategy'])}</p></article>
          <article class="case-step" data-reveal style="--d:.12s"><span>03 · OUR ROLE</span><h3 data-ar="دور الاستوديو">Our role</h3><p data-ar="{esc(p['role_ar'])}">{esc(p['role'])}</p></article>
        </div>
      </section>

      <section class="section container section--flush-top" id="execution" aria-labelledby="exec-title">
        {sec_head('02', 'EXECUTION', 'التنفيذ', '<span id="exec-title" data-ar="الخطوات التي تُسلَّم فعلًا.">The steps that actually ship.</span>',
                  'Concrete deliverables, not adjectives. Each line is something a client can open, review and keep.',
                  'مخرجات ملموسة لا صفات. كل سطر شيء يستطيع العميل فتحه ومراجعته والاحتفاظ به.')}
        <div class="grid grid--2 grid--top">
          <div class="panel tier" data-reveal><h3 data-ar="خطوات التنفيذ">Execution steps</h3><ul class="ticks" style="margin-top:14px">{steps}</ul></div>
          <div class="panel tier" data-reveal style="--d:.08s"><h3 data-ar="ما تحصل عليه">What you keep</h3><ul class="ticks" style="margin-top:14px">{deliverables}</ul></div>
        </div>
      </section>

      <section class="section container section--flush-top" id="outcome" aria-labelledby="outcome-title">
        {sec_head('03', 'OUTCOME & EVIDENCE', 'النتيجة والإثبات', '<span id="outcome-title" data-ar="لا نخترع أرقامًا.">We do not invent numbers.</span>',
                  'A named status for every claim is part of the deliverable — because an attractive image is not evidence.',
                  'تسمية حالة كل ادعاء جزء من المخرج — لأن الصورة الجميلة ليست إثباتًا.')}
        <div class="case-gate" data-reveal><p data-ar="{esc(p['outcome_ar'])}">{esc(p['outcome'])}</p></div>
        <div class="grid grid--2" style="margin-top:18px">
          <article class="panel tier" data-reveal><h3 data-ar="الخدمة المرتبطة">Related service</h3><p style="margin:10px 0" data-ar="{esc(p['service_label_ar'])}">{esc(p['service_label'])}</p><a class="text-link" href="{esc(p['service'])}"><span data-ar="صفحة الخدمة ←">Service page →</span></a></article>
          <article class="panel tier" data-reveal style="--d:.08s"><h3 data-ar="الأعمال المنشورة بالفعل">Published client work</h3><p style="margin:10px 0" data-ar="دراسات الحالة الثلاث للمنتجات والأنظمة، مع حدود إثبات معلنة لكل مشروع.">Three product and systems case studies, each with a published evidence limit.</p><a class="text-link" href="/case-studies/"><span data-ar="دراسات الحالة →">Case studies →</span></a></article>
        </div>
      </section>

      {closing('NEXT STEP', 'الخطوة التالية',
              '<span data-ar="عندك موجز شبيه؟">Have a brief like this?</span> <span class="grad-text" data-ar="لنحدّد أول خطوة.">Let’s name the first step.</span>',
              'Send the problem in one message, or book a 30-minute call. You get a clear next step — a scope, a price, or an honest “not the right fit”.',
              'أرسل المشكلة في رسالة واحدة، أو احجز مكالمة 30 دقيقة. تحصل على خطوة واضحة: نطاق، أو سعر، أو «لسنا الخيار المناسب» بصراحة.',
              [btn('Start a scoped inquiry', 'ابدأ استفسارًا بنطاق', '/contact/?inquiry=custom#message', 'primary', 'mail'), btn('Book a 30-min call', 'احجز مكالمة 30 دقيقة', '/book/', 'glass', 'calendar')])}
'''
    return page(f'/work/{p["slug"]}/', title=f'{p["title"]} — Concept Study · Code & Canvas',
                title_ar=f'{p["title_ar"]} — دراسة مفاهيمية · Code & Canvas',
                desc=p['lede'], desc_ar=p['lede_ar'], nav='work', body=body,
                og_image=f'/assets/brand/og/{p["slug"]}.png', view_track='case_study_view')


def hub():
    cats = [('all', 'All', 'الكل'), ('brand', 'Brand Identity', 'هوية العلامة'), ('packaging', 'Packaging & Print', 'التغليف والمطبوعات'), ('product', 'Digital Products', 'المنتجات الرقمية'), ('web', 'Web Experiences', 'تجارب الويب')]
    filters = ''.join(f'<button type="button" class="filter{" is-active" if k == "all" else ""}" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}"><span data-ar="{esc(ar)}">{esc(en)}</span></button>' for k, en, ar in cats)
    tiles = ''.join(tile(p, i) for i, p in enumerate(PORTFOLIO))
    ev_rows = ''.join(f'<tr><td data-ar="{esc(EVIDENCE_AR[i][0])}">{esc(e[0])}</td><td><span class="st {"st--ok" if e[1] == "Published" or e[1] == "Resolved" else "st--pending" if e[1] in ("Qualified", "Editorial") else "st--removed"}">{esc(e[1])}</span></td><td data-ar="{esc(EVIDENCE_AR[i][3])}">{esc(e[3])}</td><td data-ar="{esc(EVIDENCE_AR[i][4])}">{esc(e[4])}</td></tr>' for i, e in enumerate(EVIDENCE))
    body = f'''
      <section class="phero container phero--left" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('Work', 'أعمالنا', None)])}
        <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="بورتفوليو إبداعي · دراسات مُعلَّنة">CREATIVE PORTFOLIO · LABELLED STUDIES</span></span>
        <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s"><span data-ar="اعرض الحرفة،">Show the craft,</span><br /><span class="grad-text" data-ar="لا قائمة الخدمات.">not the service list.</span></h1>
        <p class="hero__lead" data-reveal style="--d:.16s" data-ar="أربع دراسات مفاهيمية تُظهر طريقة تفكير الاستوديو، يليها أرشيف موثّق بخمسة وعشرين مشروعًا من أعمال المؤسس الشريك — هوية أولًا، ثم منتجات رقمية. كل مدخل بمصدره وحدود إثباته.">Four concept studies show how the studio thinks, followed by a documented archive of 25 projects by our co-founder — identity first, then digital products. Every entry carries its source and its evidence limit.</p>
        <div class="hero__ctas" data-reveal style="--d:.24s">{btn('See the concept studies', 'اطّلع على الدراسات', '#studies', 'primary', 'arrowDown')}{btn('Founder work · 25', 'أعمال المؤسس · 25', '#archive', 'glass', 'grid')}{btn('Project cases · 15', 'دراسات المشاريع · 15', '#project-cases', 'glass', 'layers')}{btn('Published client cases', 'دراسات عملاء منشورة', '/case-studies/', 'ghost', 'layers')}{btn('Book a 30-min call', 'احجز مكالمة 30 دقيقة', '/book/', 'ghost', 'calendar')}</div>
      </section>

      <section class="section container section--tight" aria-label="Portfolio visual" data-ar-label="صورة البورتفوليو">
        <figure class="live-figure live-figure--wide">
          {media_img('brand-system', CONCEPT_LABEL, CONCEPT_LABEL_AR, sizes='(max-width: 720px) 92vw, 1200px', eager=True)}
          <figcaption><span data-ar="أنظمة العلامة · Code &amp; Canvas">BRAND SYSTEMS · CODE &amp; CANVAS</span><span class="live-figure__disclaimer" data-ar="{esc(CONCEPT_LABEL_AR)}">{esc(CONCEPT_LABEL)}</span></figcaption>
        </figure>
      </section>

      <section class="section container section--flush-top" id="labels" aria-labelledby="labels-title">
        <div class="work-disclaimer" data-reveal>
          {icon('alert')}
          <div>
            <strong data-ar="قاعدة واضحة: الصورة الجميلة ليست إثباتًا.">A clear rule: an attractive image is not evidence.</strong>
            <p data-ar="كل عمل فني في هذه الصفحة توضيحي أُنشئ للموقع ومُعلَّن كدراسة مفاهيمية. ليس عمل عميل، ولا لقطة شاشة لمنتج، ولا يدّعي نتيجة مُقاسة. أعمال العملاء الحقيقية في صفحة دراسات الحالة مع حدود الإثبات المنشورة، وأي حالة جديدة تدخل عبر بوابة اعتماد موثّقة.">Every artwork here is illustrative, created for this site and labelled a concept study. It is not client work, not a product screenshot and claims no measured result. Real client work lives on the case-studies page with published evidence limits, and any new case enters through a documented approval gate.</p>
          </div>
        </div>
      </section>

      <section class="section container section--flush-top" id="studies" aria-labelledby="studies-title">
        {sec_head('01', 'SELECTED STUDIES', 'دراسات مختارة',
                  '<span id="studies-title" data-ar="أربعة مسارات بصرية.">Four visual disciplines.</span> <span class="grad-text" data-ar="بنية واحدة للعرض.">One honest structure.</span>',
                  'Filter by discipline. Every tile opens a full case-study page — no pretty mockup without the reasoning behind it.',
                  'رشّح حسب التخصص. كل بطاقة تفتح صفحة دراسة كاملة — بلا ماكيت جميل بلا المنطق الذي يقف خلفه.')}
        <div class="work-filters" role="group" aria-label="Filter portfolio" data-ar-label="تصفية الأعمال" data-filter-group="#work-grid">{filters}</div>
        <div class="work-grid" id="work-grid">{tiles}
        </div>
        <p class="live-media-note" data-ar="التصفية تعمل محليًا دون إرسال أي بيانات.">Filtering runs locally; nothing is sent.</p>
      </section>

      {archive_section()}

      {case_studies_section()}

      <section class="section container section--flush-top" id="intake" aria-labelledby="intake-title">
        {sec_head('04', 'HOW REAL WORK GETS PUBLISHED', 'كيف تُنشر الأعمال الحقيقية',
                  '<span id="intake-title" data-ar="من الموجز إلى الإثبات.">From the brief to the evidence.</span>',
                  'The gate a real client case must pass before it replaces — or sits beside — a concept study.',
                  'البوابة التي يجب أن تمر بها أي حالة عميل حقيقية قبل أن تحلّ محل دراسة مفاهيمية أو تجاورها.')}
        <div class="case-steps">
          <article class="case-step" data-reveal><span>01 · PERMISSION</span><h3 data-ar="إذن">Permission</h3><p data-ar="إذن كتابي يحدّد ما يُعرض وفي أي أسواق ولأي مدة.">Written client permission naming what may be shown, in which markets and for how long.</p></article>
          <article class="case-step" data-reveal style="--d:.06s"><span>02 · EVIDENCE</span><h3 data-ar="إثبات">Evidence</h3><p data-ar="لقطات أو صور معتمدة مع حجب بيانات الأشخاص والصحة والمالية.">Approved screenshots or photography, with people, health and financial data redacted.</p></article>
          <article class="case-step" data-reveal style="--d:.12s"><span>03 · ATTRIBUTION</span><h3 data-ar="نسبة العمل">Attribution</h3><p data-ar="الدور الدقيق للاستوديو والفريق والتاريخ والقيود — بلا نسبة عمل الغير.">The studio’s exact role, the team, the date and the constraints — no borrowed credit.</p></article>
        </div>
      </section>

      <section class="section container section--flush-top" id="evidence" aria-labelledby="ev-title">
        {sec_head('05', 'CLAIMS & EVIDENCE REGISTER', 'سجل الادعاءات والأدلة',
                  '<span id="ev-title" data-ar="ما ننشره، ولماذا.">What we publish, and why.</span>',
                  'A live register of numbers and claims: published, qualified, removed or resolved. Anything without evidence is rewritten or taken down.',
                  'سجل حيّ للأرقام والادعاءات: منشور، أو مقيَّد، أو محذوف، أو محسوم. أي شيء بلا إثبات يُعاد صياغته أو يُشال.')}
        <div class="evidence-scroll" data-reveal tabindex="0" role="region" aria-label="Claims and evidence table" data-ar-label="جدول الادعاءات والأدلة"><table class="evidence-table">
          <thead><tr><th data-ar="الادعاء">Claim</th><th data-ar="الحالة">Status</th><th data-ar="المطلوب قبل النشر الأقوى">Required before a stronger claim</th><th data-ar="المالك">Owner</th></tr></thead>
          <tbody>{ev_rows}</tbody>
        </table></div>
        <p class="live-media-note" data-ar="النسخة الكاملة مع الأدلة والمصادر: docs/CLAIMS-REGISTER.md">Full version with sources and evidence: <code>docs/CLAIMS-REGISTER.md</code>.</p>
      </section>

      <section class="section container section--flush-top" aria-label="Continue" data-ar-label="تابع">
        <div class="live-crosslinks">
          <div class="live-crosslink"><b data-ar="دراسات حالة منشورة">Published case studies</b><span data-ar="صيدليتي، زاد، ونايل فارما ERP — الدور والمنهج وحدود الإثبات.">Pharmacy OS, Zad and Nile Pharma ERP — role, approach and evidence limits.</span><a href="/case-studies/" data-track="case_study_view" data-track-id="index"><span data-ar="افتح الصفحة →">Open the page →</span></a></div>
          <div class="live-crosslink"><b data-ar="الخدمات السبع الرئيسية">Seven flagship services</b><span data-ar="صفحات مستقلة بالنطاق والمخرجات والخطوات والأسئلة الشائعة.">Standalone pages with scope, deliverables, steps and FAQ.</span><a href="/services/"><span data-ar="كتالوج الخدمات →">Service catalogue →</span></a></div>
          <div class="live-crosslink"><b data-ar="احجز مكالمة">Book a call</b><span data-ar="30 دقيقة، اختيار التخصص والموعد، تأكيد ودعوة تقويم.">30 minutes: choose a specialty, pick a slot, get a confirmation and a calendar invite.</span><a href="/book/" data-track="cta_click" data-track-id="work-book"><span data-ar="احجز الآن →">Book now →</span></a></div>
        </div>
      </section>

      {closing('READY WHEN YOU ARE', 'جاهزون عندما تكون جاهزًا',
              '<span data-ar="أرِنا المشكلة.">Show us the problem.</span> <span class="grad-text" data-ar="سنقول لك أول خطوة.">We’ll name the first step.</span>',
              'One message is enough. We reply with a scope, a price, or an honest “we are not the right fit”.',
              'رسالة واحدة تكفي. نرد بنطاق أو سعر أو «لسنا الخيار المناسب» بصراحة.',
              [btn('Send a message', 'أرسل رسالة', '/contact/', 'primary', 'mail'), btn('Book a call', 'احجز مكالمة', '/book/', 'glass', 'calendar')])}
'''
    return page('/work/', title='Creative Work — Brand, Packaging, Product & Web · Code & Canvas',
                title_ar='الأعمال الإبداعية — العلامة والتغليف والمنتج والويب · Code & Canvas',
                desc='A labelled visual portfolio: four concept studies, a 25-project founder work archive and 15 detailed live-project case studies spanning brand identity and digital products. Every entry states its source, role and evidence limit.',
                desc_ar='بورتفوليو بصري مُعلَّن: أربع دراسات مفاهيمية، يليها أرشيف بخمسة وعشرين مشروعًا من أعمال المؤسس، ثم خمس عشرة دراسة حالة تفصيلية لمشروعات مباشرة بين أنظمة الهوية والمنتجات الرقمية. كل مدخل يوضّح مصدره ودوره وحدود إثباته.',
                nav='work', body=body, extra_head=CSS, og_image='/assets/brand/og/work.png', view_track='case_study_view')


def build():
    return [hub()] + [case_page(p) for p in PORTFOLIO]
