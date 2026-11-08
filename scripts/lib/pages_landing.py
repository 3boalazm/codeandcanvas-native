# -*- coding: utf-8 -*-
"""Seven standalone, original service landing pages.

Each page: a value-led hero, the problem it solves, scope/deliverables, a
three-step process, real internal links (concept study → published case →
article), a scoped inquiry CTA, a booking CTA and an FAQ. Prices are the
indicative catalogue ranges and are always described as such.
"""
from h import esc, icon, crumbs, closing, btn, page, sec_head, ORG_ID, SITE, media_img
from data_growth import SERVICE_LANDINGS

MEDIA = '/assets/media/'


def landing(x):
    scope = ''.join(f'<div class="sls-deliverable">{icon("check")}<div><b data-ar="{esc(a)}">{esc(e)}</b></div></div>' for e, a in zip(x['scope'], x['scope_ar']))
    steps = ''.join(f'''<article class="case-step" data-reveal style="--d:{i * .06:.2f}s"><span>0{i + 1} · STEP</span><h3 data-ar="{esc(s[1])}">{esc(s[0])}</h3><p data-ar="{esc(x['steps_ar'][i])}">{esc(s[2])}</p></article>''' for i, s in enumerate(x['steps']))
    faq = ''.join(f'''<div class="faq__item"><button class="faq__q" type="button" aria-expanded="false"><span data-ar="{esc(x['faq_ar'][i][0])}">{esc(q)}</span><span class="pm" aria-hidden="true"></span></button><div class="faq__a"><div><p data-ar="{esc(x['faq_ar'][i][1])}">{esc(a)}</p></div></div></div>''' for i, (q, a) in enumerate(x['faq']))
    ld_service = {'@type': 'Service', '@id': f'{SITE}/services/{x["slug"]}/#service', 'name': x['title'],
                  'description': x['lead'], 'provider': {'@id': ORG_ID}, 'serviceType': x['kicker'],
                  'areaServed': ['Saudi Arabia', 'Egypt', 'MENA'], 'url': f'{SITE}/services/{x["slug"]}/'}
    ld_faq = {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in x['faq']]}

    body = f'''
      <section class="phero container phero--left" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('Services', 'الخدمات', '/services/'), (x['title'], x['title_ar'], None)])}
        <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="{esc(x['kicker_ar'])}">{esc(x['kicker'])}</span></span>
        <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s" data-ar="{esc(x['title_ar'])}">{esc(x['title'])}</h1>
        <p class="hero__lead" data-reveal style="--d:.16s" data-ar="{esc(x['lead_ar'])}">{esc(x['lead'])}</p>
        <div class="sls-hero__badges" data-reveal style="--d:.2s"><span data-ar="نطاق مكتوب">Written scope</span><span data-ar="{esc(x['duration_ar'])}">{esc(x['duration'])}</span><span data-ar="عربي / إنجليزي">Arabic / English</span><span data-ar="السعودية + مصر">KSA + Egypt</span></div>
        <div class="hero__ctas" data-reveal style="--d:.24s"><a class="btn btn--primary magnetic" href="/contact/?inquiry={x["code"]}#message" data-track="cta_click" data-track-service="{x["code"]}"><span data-ar="ابدأ استفسارًا بنطاق">Start a scoped inquiry</span><i class="flip" data-icon="mail"></i></a>{btn('Book a 30-min call', 'احجز مكالمة 30 دقيقة', '/book/?specialty=' + ('brand' if x['code'].startswith('MA') and x['code'] in ('MA-01','MA-02','MA-03','MA-04','MA-07') else 'product' if x['code'] in ('MA-05','MA-06') else 'healthcare' if x['code'].startswith('HC') else 'technology'), 'glass', 'calendar')}</div>
      </section>

      <section class="section container section--tight" aria-label="Service visual" data-ar-label="صورة الخدمة">
        <figure class="live-figure live-figure--wide">
          {media_img(x['media'], 'Illustrative studio artwork for ' + x['title'], 'عمل فني توضيحي للاستوديو — ' + x['title_ar'], sizes='(max-width: 720px) 92vw, 1200px', eager=True, fetchpriority='high')}
          <figcaption><span data-ar="عمل توضيحي • ليس لقطة منتج">ILLUSTRATIVE · NOT A PRODUCT SHOT</span><span class="live-figure__disclaimer" data-ar="تصميم توضيحي للسيكشن">SECTION ARTWORK</span></figcaption>
        </figure>
        <p class="live-media-note" data-ar="عمل فني توضيحي أُنشئ للموقع؛ لا يمثّل لقطة شاشة لمنتج عميل ولا إثبات نتيجة.">Illustrative artwork created for this site; it is not a client product screenshot or evidence of a result.</p>
      </section>

      <section class="section container section--flush-top" id="problem" aria-labelledby="problem-title">
        {sec_head('01', 'THE PROBLEM', 'المشكلة',
                  '<span id="problem-title" data-ar="لماذا يُطلب هذا العمل أصلًا.">Why this work gets commissioned.</span>',
                  'We start from the failure pattern, not from a feature list.', 'نبدأ من نمط الفشل لا من قائمة مزايا.')}
        <div class="panel panel--deep" data-reveal><p class="lead" style="margin:0" data-ar="{esc(x['problem_ar'])}">{esc(x['problem'])}</p></div>
      </section>

      <section class="section container section--flush-top" id="scope" aria-labelledby="scope-title">
        {sec_head('02', 'SCOPE & DELIVERABLES', 'النطاق والمخرجات',
                  '<span id="scope-title" data-ar="بالضبط ما تحصل عليه.">Exactly what you keep.</span>',
                  'Every line is an artefact you can open, review and own.', 'كل سطر هو ملف تستطيع فتحه ومراجعته وامتلاكه.')}
        <div class="sls-deliverables">{scope}
        </div>
      </section>

      <section class="section container section--flush-top" id="process" aria-labelledby="process-title">
        {sec_head('03', 'HOW IT RUNS', 'كيف يسير العمل',
                  '<span id="process-title" data-ar="ثلاث خطوات بمعالم واضحة.">Three steps, clear milestones.</span>',
                  'A written scope, staged delivery and a named hand-over.', 'نطاق مكتوب، وتسليم على مراحل، وتسليم مسمّى.')}
        <div class="case-steps">{steps}
        </div>
      </section>

      <section class="section container section--flush-top" id="proof" aria-labelledby="proof-title">
        {sec_head('04', 'SEE THE WORK', 'اطّلع على الأعمال',
                  '<span id="proof-title" data-ar="المنهج قبل الوعود.">The method before the promises.</span>',
                  'A labelled study, published client work and a related article — the full path from reading to deciding.',
                  'دراسة مُعلَّنة، وأعمال عملاء منشورة، ومقال مرتبط — المسار كاملًا من القراءة إلى القرار.')}
        <div class="live-crosslinks" data-reveal>
          <div class="live-crosslink"><b data-ar="دراسة حالة">Case study</b><span data-ar="{esc(x['work_label_ar'])}">{esc(x['work_label'])}</span><a href="{esc(x['work'])}" data-track="case_study_view"><span data-ar="افتح الدراسة →">Open the study →</span></a></div>
          <div class="live-crosslink"><b data-ar="مقال مرتبط">Related reading</b><span data-ar="{esc(x['post_label_ar'])}">{esc(x['post_label'])}</span><a href="{esc(x['post'])}"><span data-ar="اقرأ المقال →">Read the article →</span></a></div>
          <div class="live-crosslink"><b data-ar="كل الأعمال">All work</b><span data-ar="البورتفوليو الإبداعي ودراسات الحالة المنشورة.">The creative portfolio and published case studies.</span><a href="/work/"><span data-ar="الأعمال →">Work →</span></a></div>
        </div>
      </section>

      <section class="section container section--flush-top" id="start" aria-labelledby="start-title">
        <div class="book-shell">
          <div class="book-panel" data-reveal>
            <p class="kicker"><span data-ar="الخطوة التالية">NEXT STEP</span></p>
            <h2 id="start-title" style="font-size:clamp(24px,2.6vw,34px);margin:10px 0" data-ar="ابدأ بموجز، لا بعرض تقديمي.">Start with a brief, not a deck.</h2>
            <p class="lead" data-ar="أرسل المشكلة في رسالة قصيرة، أو احجز مكالمة 30 دقيقة. نرد بنطاق مكتوب وسعر استرشادي أو نخبرك بصراحة إن لم نكن مناسبين.">Send the problem in a short message, or book a 30-minute call. We reply with a written scope and an indicative price — or tell you honestly if we are not the right fit.</p>
            <div class="hero__ctas" style="margin-top:20px">{btn('Send a scoped inquiry', 'أرسل استفسارًا بنطاق', f'/contact/?inquiry={x["code"]}#message', 'primary', 'mail')}{btn('Book a 30-min call', 'احجز مكالمة 30 دقيقة', '/book/', 'glass', 'calendar')}</div>
          </div>
          <aside class="sls-side">
            <div class="sls-price" data-reveal><b class="ltr" data-ar="{esc(x['price_ar'])}">{esc(x['price'])}</b><span data-ar="نطاق استرشادي — يُثبَّت السعر النهائي في عرض مكتوب.">Indicative range — the final price is fixed in a written proposal.</span></div>
            <div class="panel tier" data-reveal style="--d:.06s"><h3 data-ar="المدة">Typical duration</h3><p style="margin:8px 0 0" data-ar="{esc(x['duration_ar'])}">{esc(x['duration'])}</p></div>
            <div class="panel tier" data-reveal style="--d:.12s"><h3 data-ar="رمز الخدمة">Service code</h3><p style="margin:8px 0 0"><b class="ltr">{esc(x['code'])}</b> · <a href="/services/" data-ar="العودة للكتالوج">Back to catalogue</a></p></div>
          </aside>
        </div>
      </section>

      <section class="section container section--flush-top" id="faq" aria-labelledby="faq-title">
        {sec_head('05', 'FAQ', 'الأسئلة الشائعة', '<span id="faq-title" data-ar="أسئلة قبل أن تسألها.">The questions before you ask them.</span>',
                  'Straight answers on scope, timing and what happens next.', 'إجابات مباشرة عن النطاق والتوقيت والخطوة التالية.')}
        <div class="faq faq--prose" data-reveal>{faq}
        </div>
      </section>

      {closing('ONE CLEAR FIRST STEP', 'خطوة أولى واحدة واضحة',
              '<span data-ar="أخبرنا بالمشكلة.">Tell us the problem.</span> <span class="grad-text" data-ar="سنحدّد أول خطوة.">We’ll name the first step.</span>',
              'A message, a call, or an honest “not the right fit”. No sales sequence.',
              'رسالة، أو مكالمة، أو «لسنا الخيار المناسب» بصراحة. بلا سلسلة مبيعات.',
              [btn('Contact the studio', 'تواصل مع الاستوديو', '/contact/', 'primary', 'mail'), btn('Book a call', 'احجز مكالمة', '/book/', 'glass', 'calendar')])}
'''
    return page(f'/services/{x["slug"]}/', title=f'{x["title"]} — Code & Canvas',
                title_ar=f'{x["title_ar"]} — Code & Canvas',
                desc=x['lead'], desc_ar=x['lead_ar'], nav='services', body=body,
                og_image=f'/assets/brand/og/{x["og"]}.png', view_track='service_view', ld=[ld_service, ld_faq])


def build():
    return [landing(x) for x in SERVICE_LANDINGS]
