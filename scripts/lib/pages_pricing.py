# -*- coding: utf-8 -*-
"""/pricing-faq/ — live copy of codeandcanvas.net/pricing-faq/ with the legacy
S-codes mapped to the unified catalogue (AB / MA / HC / CC)."""
from catalog import SERVICES, TRACKS, href
from h import esc, icon, crumbs, closing, btn, page, svc_grid

# (code, note_en, note_ar, star, bullets_en, bullets_ar, [price_override, dur_override])
PKG = {
    'tech': [
        ('AB-01', 'Two tiers · ex-S03 / S04', 'مستويان · S03 / S04 سابقًا', False,
         ['EA Quick-Start ($1,000 – $2,500 · 2 weeks): current state across BDAT layers · capability gap analysis · Business-to-Technology Alignment Matrix · 90-day action plan · ArchiMate / Sparx EA documentation',
          'Transformation Advisory ($3,000 – $8,000 · 4–8 weeks): governance model design · phased roadmap · NORA & Vision 2030 alignment · KPI framework · stakeholder presentation'],
         ['البداية السريعة للعمارة المؤسسية (⁦$1,000 – $2,500⁩ · أسبوعان): الوضع الحالي عبر طبقات BDAT · تحليل فجوات القدرات · مصفوفة مواءمة الأعمال مع التقنية · خطة عمل لـ 90 يومًا · توثيق ArchiMate / Sparx EA',
          'استشارات التحول (⁦$3,000 – $8,000⁩ · ⁦4–8⁩ أسابيع): تصميم نموذج الحوكمة · خارطة طريق مرحلية · مواءمة NORA ورؤية 2030 · إطار مؤشرات الأداء · عرض لأصحاب المصلحة']),
        ('AB-05', '3–6 weeks · Architecture-first', '⁦3–6⁩ أسابيع · العمارة أولًا', False,
         ['Workload assessment', 'Provider evaluation matrix', 'Migration sequencing plan', 'Risk register', 'Cloud governance framework'],
         ['تقييم أحمال العمل', 'مصفوفة تقييم مزوّدي الخدمة', 'خطة تسلسل الهجرة', 'سجل المخاطر', 'إطار حوكمة السحابة']),
        ('AB-04', '3–5 days · .NET', '⁦3–5⁩ أيام · .NET', False,
         ['Automated .NET source analysis', 'Application landscape map', 'Service dependency map', 'Technical documentation', 'Replaces weeks of manual discovery'],
         ['تحليل آلي لمصدر .NET', 'خريطة مشهد التطبيقات', 'خريطة اعتماديات الخدمات', 'توثيق تقني', 'يحل محل أسابيع من الاستكشاف اليدوي']),
    ],
    'brand': [
        ('MA-03', 'Flagship · 8-stage V2', 'الباقة الرئيسية · منهجية V2 من 8 مراحل', True,
         ['Logo system (5+ variants)', 'Brand strategy document', 'Color + typography system', 'Brand guidelines (AR + EN)', 'Full stationery kit', 'Social media template pack'],
         ['منظومة شعار (+5 نسخ)', 'وثيقة استراتيجية العلامة', 'نظام ألوان وخطوط', 'دليل العلامة (عربي + إنجليزي)', 'حزمة قرطاسية كاملة', 'حزمة قوالب سوشيال ميديا']),
        ('MA-02', 'Includes Brand Audit + Refresh tier ($500 – $1,500 · 1–2 weeks)', 'يتضمن مستوى تدقيق وتجديد العلامة (⁦$500 – $1,500⁩ · ⁦1–2⁩ أسبوع)', False,
         ['Brand health diagnosis', 'Stay / update / rebrand decision', 'Targeted refresh delivery', 'Updated guidelines'],
         ['تشخيص صحة العلامة', 'قرار الإبقاء / التحديث / إعادة البناء', 'تسليم تجديد موجّه', 'دليل محدَّث']),
        ('CC-01', '6–8 weeks · Flagship', '⁦6–8⁩ أسابيع · الباقة الرئيسية', True,
         ['Brand identity system', 'Bilingual website (AR + EN)', 'Digital architecture', 'Booking system + GA4 + SEO', 'Social media kit', '30-day post-launch support'],
         ['منظومة هوية العلامة', 'موقع ثنائي اللغة (عربي + إنجليزي)', 'عمارة رقمية', 'نظام حجوزات + GA4 + SEO', 'حزمة سوشيال ميديا', 'دعم 30 يومًا بعد الإطلاق']),
    ],
    'data': [
        ('AB-03', 'Power BI · Python', 'Power BI · Python', False,
         ['Operational data → executive dashboards', 'Power BI or Tableau delivery', 'Python data pipeline (if needed)', 'Decision intelligence framing', 'Entry point to AB-01'],
         ['بيانات تشغيلية ← لوحات تنفيذية', 'تسليم عبر Power BI أو Tableau', 'خط بيانات Python (عند الحاجة)', 'تأطير ذكاء القرارات', 'نقطة دخول إلى AB-01']),
        ('CC-02', '2–4 weeks · Framework + execution', '⁦2–4⁩ أسابيع · إطار + تنفيذ', False,
         ['Market entry strategy', 'Commercial positioning (framework)', 'BD framework / BD pipeline design', 'Go-to-market (execution) plan'],
         ['استراتيجية دخول السوق', 'التموضع التجاري (إطار)', 'إطار تطوير الأعمال / تصميم خط التطوير', 'خطة الوصول إلى السوق (تنفيذ)']),
    ],
    'health': [
        ('HC-01', '5–7 weeks · Brand + Tech', '⁦5–7⁩ أسابيع · هوية + تقنية', True,
         ['Brand identity + bilingual digital presence', 'Booking system + Google presence', 'CBAHI-aware design', 'NORA-compliant patient comms', 'AR + EN as standard'],
         ['هوية العلامة + حضور رقمي ثنائي اللغة', 'نظام حجوزات + حضور على Google', 'تصميم واعٍ بمتطلبات CBAHI', 'تواصل مع المرضى متوافق مع NORA', 'عربي + إنجليزي كمعيار']),
        ('HC-03', '3–5 weeks · CBAHI + NORA', '⁦3–5⁩ أسابيع · CBAHI + NORA', False,
         ['Clinical workflow mapping', 'Vendor scoring matrix (10+ vendors)', 'RFP template', 'Contract review checklist', '⚠ Wrong HIS: $50K–$200K exposure'],
         ['رسم مسارات العمل السريرية', 'مصفوفة تقييم المورّدين (+10 مورّدين)', 'قالب طلب العروض (RFP)', 'قائمة مراجعة العقد', '⚠ نظام HIS خاطئ: تعرّض بقيمة ⁦$50K–$200K⁩']),
        ('HC-02', '2–3 weeks · CBAHI KPIs', '⁦2–3⁩ أسابيع · مؤشرات CBAHI', False,
         ['Clinical operational data → dashboards', 'CBAHI KPI library included', 'BD insight layer', 'Executive reporting format'],
         ['بيانات تشغيلية سريرية ← لوحات مؤشرات', 'مكتبة مؤشرات CBAHI مضمّنة', 'طبقة رؤى تطوير الأعمال', 'صيغة تقارير تنفيذية']),
        ('HC-05', '2–3 weeks · CPHIMS-delivered', '⁦2–3⁩ أسابيع · بتنفيذ CPHIMS', False,
         ['EMRAM stage scoring', 'CBAHI readiness gap report', 'NORA alignment review', '90-day technology roadmap'],
         ['تحديد مرحلة EMRAM', 'تقرير فجوات الجاهزية لـ CBAHI', 'مراجعة المواءمة مع NORA', 'خارطة طريق تقنية لمدة 90 يومًا']),
    ],
}
ALSO = {'tech': ['AB-02', 'AB-06'], 'brand': ['MA-01', 'MA-04', 'MA-05', 'MA-06', 'MA-07', 'MA-08', 'MA-09', 'MA-10'], 'data': [], 'health': ['HC-04']}
TABS = [('tech', 'Technology & EA', 'التقنية والعمارة المؤسسية', 'layers'), ('brand', 'Brand & Creative', 'الهوية والإبداع', 'pen'), ('data', 'Data & BD', 'البيانات وتطوير الأعمال', 'chart'), ('health', 'Healthcare', 'الرعاية الصحية', 'stethoscope')]

FAQ = [
    ('Do you work with clients outside KSA and Egypt?', 'هل تعملون مع عملاء خارج السعودية ومصر؟',
     'Yes. We serve organizations across MENA. All engagements are delivered fully remotely, with communication in Arabic and English.',
     'نعم. نخدم مؤسسات في أنحاء المنطقة. تُنفَّذ كل المشاريع عن بُعد بالكامل، مع التواصل بالعربية والإنجليزية.'),
    ('Can I get a custom quote for a larger engagement?', 'هل يمكنني الحصول على عرض سعر مخصص لمشروع أكبر؟',
     'Yes. Larger or multi-phase engagements are quoted individually. Book a discovery call and we\'ll scope it with you.',
     'نعم. المشاريع الأكبر أو متعددة المراحل تُسعَّر بشكل فردي. احجز مكالمة استكشافية وسنحدد نطاقها معك.'),
    ('Do you offer retainers?', 'هل تقدمون عقودًا مستمرة (ريتينر)؟',
     'No open-ended retainers. Every engagement has a productized scope. Repeat engagements are welcome, and 30-day post-launch support is included in CC-01 Digital Launch Package and HC-01 Clinic Digital Launch.',
     'لا عقود مفتوحة النهاية. كل مشروع له نطاق مُنتج. المشاريع المتكررة مرحَّب بها، ويشمل كلٌّ من باقة الإطلاق الرقمي CC-01 والإطلاق الرقمي للعيادات HC-01 دعمًا لمدة 30 يومًا بعد الإطلاق.'),
    ('What if I need changes after delivery?', 'ماذا لو احتجت تعديلات بعد التسليم؟',
     'Every engagement includes a structured revision cycle before final sign-off. Changes outside the agreed scope are quoted as a new mini-engagement — never silently absorbed.',
     'كل مشروع يتضمن دورة تعديلات منظمة قبل الاعتماد النهائي. التغييرات خارج النطاق المتفق عليه تُسعَّر كمشروع مصغّر جديد — ولا تُستوعب بصمت أبدًا.'),
    ('What happens on a discovery call?', 'ماذا يحدث في المكالمة الاستكشافية؟',
     'A 30-minute structured session. We come prepared, ask about your business problem, and leave you with a clear scope, timeline, and fit assessment — or tell you directly if we\'re not the right match.',
     'جلسة منظمة مدتها 30 دقيقة. نأتي مستعدين ونسأل عن مشكلة عملك ونترك لك نطاقًا واضحًا وجدولًا زمنيًا وتقييمًا للملاءمة — أو نخبرك بصراحة إن لم نكن الخيار المناسب.'),
    ('Do you work on healthcare projects only as a unit?', 'هل تعملون على المشاريع الصحية كوحدة واحدة فقط؟',
     'No. Healthcare-specific services (HC-01 to HC-05) are led by Ahmed Bedeer (CPHIMS, HIMSS EMRAM, NORA). HC-04 Clinic Brand Identity is brand-only and led by Mustafa. Combined engagements (HC-01, HC-02) involve both founders.',
     'لا. الخدمات الصحية المتخصصة (HC-01 إلى HC-05) يقودها أحمد بدير (CPHIMS، HIMSS EMRAM، NORA). هوية العيادة HC-04 مشروع هوية فقط ويقوده مصطفى. المشاريع المتكاملة (HC-01، HC-02) يشارك فيها المؤسسان.'),
    ('Can I combine services across categories?', 'هل يمكنني الجمع بين خدمات من فئات مختلفة؟',
     'Yes. CC-01 Digital Launch Package and HC-01 / HC-02 already combine brand and technology. Any cross-track engagement is quoted as a single package — never double-billed.',
     'نعم. باقة الإطلاق الرقمي CC-01 و HC-01 / HC-02 تجمع بالفعل بين الهوية والتقنية. أي مشروع عابر للمسارات يُسعَّر كباقة واحدة — دون فوترة مزدوجة أبدًا.'),
    ('What currency do you invoice in?', 'بأي عملة تصدرون الفواتير؟',
     'Pricing is shown in USD. Equivalent SAR or EGP rates are confirmed at contract. Bank transfer or digital payment accepted. One invoice per milestone.',
     'الأسعار معروضة بالدولار الأمريكي. تُؤكَّد المعادلات بالريال السعودي أو الجنيه المصري عند التعاقد. يُقبل التحويل البنكي أو الدفع الرقمي. فاتورة واحدة لكل معلم.'),
    ('Are your credentials active?', 'هل اعتماداتكم سارية؟',
     'Active. TOGAF, CPHIMS, HIMSS EMRAM Assessor, NORA, and CBAHI are used in every relevant engagement — not listed for decoration.',
     'سارية. TOGAF و CPHIMS ومقيّم HIMSS EMRAM و NORA و CBAHI تُستخدم في كل مشروع ذي صلة — وليست مُدرجة للزينة.'),
    ('I\'m not sure which service I need.', 'لست متأكدًا أي خدمة أحتاج.',
     'That\'s what the discovery call is for. Tell us the business problem and we\'ll point you to the right engagement. If we\'re not the right match, we\'ll say so directly.',
     'لهذا وُجدت المكالمة الاستكشافية. أخبرنا بمشكلة العمل وسنوجّهك إلى المشروع المناسب. وإن لم نكن الخيار المناسب، فسنقولها بصراحة.'),
]


def pkg(code, note, note_ar, star, bul, bul_ar, delay=0.0):
    s = SERVICES[code]
    tr = TRACKS[s['track']]
    items = ''.join(f'<li data-ar="{esc(a)}">{esc(e)}</li>' for e, a in zip(bul, bul_ar))
    price_ar = s.get('price_ar') or s['price']
    return f'''
          <article class="card glass tier tier--pkg{' tier--star' if star else ''}" data-reveal style="--d:{delay:.2f}s">
            <div class="tier__head">
              <span class="svc__code">{code}{' ⭐' if star else ''}</span>
              <h3><a href="{href(code)}" data-ar="{esc(s['title_ar'])}">{esc(s['title'])}</a></h3>
              <p class="tier__note" data-ar="{esc(note_ar)}">{esc(note)}</p>
            </div>
            <p class="tier__price"><strong data-ar="{esc(price_ar)}">{esc(s['price'])}</strong><span data-ar="{esc(s.get('dur_ar') or s['dur'])}">{esc(s['dur'])}</span></p>
            <ul class="ticks ticks--dense">{items}</ul>
            <a class="text-link" href="{href(code)}"><span data-ar="تفاصيل الخدمة ←">Service details →</span></a>
          </article>'''


def build():
    tabs = ''.join(f'<button class="tab{" is-active" if i == 0 else ""}" type="button" role="tab" data-tab="{k}" aria-selected="{"true" if i == 0 else "false"}">{icon(ic)}<span data-ar="{esc(ar)}">{esc(en)}</span></button>' for i, (k, en, ar, ic) in enumerate(TABS))
    panels = ''
    for k, en, ar, ic in TABS:
        cards = ''.join(pkg(*p, delay=(i % 3) * .07) for i, p in enumerate(PKG[k]))
        also = ''
        if ALSO[k]:
            also = f'''
          <p class="kicker" style="margin-top:28px"><span data-ar="أيضًا في هذا المسار">Also in this track</span></p>
          {svc_grid(ALSO[k])}'''
        panels += f'''
        <div data-panel="{k}" data-scope="pricing" hidden>
          <div class="grid grid--3 grid--pkg">{cards}
          </div>{also}
        </div>'''
    faq = ''.join(f'''
          <div class="faq__item{' is-open' if i == 0 else ''}">
            <button class="faq__q" type="button" aria-expanded="{'true' if i == 0 else 'false'}"><span data-ar="{esc(qar)}">{esc(q)}</span><span class="pm" aria-hidden="true"></span></button>
            <div class="faq__a"><div><p data-ar="{esc(aar)}">{esc(a)}</p></div></div>
          </div>''' for i, (q, qar, a, aar) in enumerate(FAQ))

    body = f'''
      <!-- ░░ Hero ░░ -->
      <section class="phero container phero--center" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('Solutions', 'الحلول', '/services/'), ('Pricing & FAQ', 'الأسعار والأسئلة الشائعة', None)])}
        <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="الأسعار والأسئلة الشائعة">Pricing &amp; FAQ</span></span>
        <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s"><span data-ar="أسعار شفافة.">Transparent pricing.</span><br /><span class="grad-text" data-ar="بلا مفاجآت.">No surprises.</span></h1>
        <p class="hero__lead" data-reveal style="--d:.16s" data-ar="نطاق ثابت. دفعات حسب المعالم. لكل مشروع سعر واضح ومخرج محدد ونتيجة أعمال قابلة للتتبع — قبل أن توقّع أي شيء.">Fixed scope. Milestone-based payment. Every engagement has a clear price, a defined deliverable, and a traceable business outcome — before you sign anything.</p>
        <div class="hero__ctas hero__ctas--center" data-reveal style="--d:.24s">{btn('Book a Free Discovery Call', 'احجز مكالمة استكشافية مجانية', '/contact/#book')}{btn('Service pricing', 'أسعار الخدمات', '#pricing', 'glass', 'arrowDown')}</div>
      </section>

      <!-- ░░ How we charge ░░ -->
      <section class="section container section--tight" id="how-we-charge" aria-labelledby="charge-title">
        <header class="section__head" data-reveal>
          <p class="kicker"><span class="kicker__num">01</span><span data-ar="كيف نُسعّر">How We Charge</span></p>
          <h2 class="section__title" id="charge-title"><span data-ar="حسب المعالم.">Milestone-based.</span> <span class="grad-text" data-ar="لا حسب الوقت.">Not time-based.</span></h2>
          <p class="section__lead" data-ar="تُقسَّم الدفعات على معالم محددة — لا تُحتسب بالساعة أو بالشهر. تُسلَّم الملفات فقط عند السداد الكامل.">Payment is split across defined milestones — not billed by the hour or the month. Files are only released upon full settlement.</p>
        </header>
        <div class="grid grid--2">
          <article class="card glass tile" data-tilt data-reveal>
            <span class="card__icon">{icon('pen')}</span>
            <h3 data-ar="الهوية والإبداع">Brand &amp; Creative</h3>
            <p class="tile__sub" data-ar="MA-01 → MA-10 · CC-01 · HC-01 · HC-04">MA-01 → MA-10 · CC-01 · HC-01 · HC-04</p>
            <ol class="milestones">
              <li><b>50%</b><span data-ar="الانطلاق واعتماد الموجز">Kickoff &amp; Brief Sign-off</span></li>
              <li><b>25%</b><span data-ar="اعتماد الاستراتيجية">Strategy Sign-off</span></li>
              <li><b>25%</b><span data-ar="التسليم النهائي">Final Delivery</span></li>
            </ol>
          </article>
          <article class="card glass tile" data-tilt data-reveal style="--d:.08s">
            <span class="card__icon">{icon('layers')}</span>
            <h3 data-ar="التقنية والاستشارات">Technology &amp; Advisory</h3>
            <p class="tile__sub">AB-01 → AB-06 · CC-02 · HC-02 · HC-03 · HC-05</p>
            <ol class="milestones">
              <li><b>50%</b><span data-ar="الانطلاق وتثبيت النطاق">Kickoff &amp; Scope Lock</span></li>
              <li><b>50%</b><span data-ar="التسليم النهائي">Final Delivery</span></li>
            </ol>
          </article>
        </div>
        <div class="notice notice--violet" data-reveal style="margin-top:18px">{icon('alert')}<p data-ar-html="&lt;strong&gt;تسليم الملفات مشروط بالسداد الكامل.&lt;/strong&gt; تُحتسب على المدفوعات المتأخرة 2% شهريًا بعد 14 يومًا."><strong>File release is conditional on full payment.</strong> Late payments accrue at 2% per month after 14 days.</p></div>
        <div class="grid grid--3" style="margin-top:18px">
          <article class="card glass tile" data-tilt data-reveal><span class="card__icon">{icon('lock')}</span><h3 data-ar="الملفات عند السداد الكامل">Files on Full Settlement</h3><p data-ar="كل المخرجات — الملفات المصدرية والوثائق والأدلة — تُسلَّم فقط عند سداد 100%. بلا استثناءات.">All deliverables — source files, documentation, guidelines — are released only upon 100% payment. No exceptions.</p></article>
          <article class="card glass tile" data-tilt data-reveal style="--d:.07s"><span class="card__icon">{icon('receipt')}</span><h3 data-ar="النطاق يُثبَّت عند الانطلاق">Scope Locked at Kickoff</h3><p data-ar="يُحدَّد النطاق ويُعتمد قبل بدء العمل. الطلبات خارج النطاق تُسعَّر بشكل منفصل — ولا تُستوعب بصمت أبدًا.">Scope is defined and signed off before work begins. Out-of-scope requests are quoted separately — never silently absorbed.</p></article>
          <article class="card glass tile" data-tilt data-reveal style="--d:.14s"><span class="card__icon">{icon('wallet')}</span><h3>USD · SAR · EGP</h3><p data-ar="الأسعار معروضة بالدولار الأمريكي. تُؤكَّد المعادلات بالريال السعودي / الجنيه المصري عند التعاقد. يُقبل التحويل البنكي أو الدفع الرقمي.">Pricing shown in USD. Equivalent SAR/EGP rates confirmed at contract. Bank transfer or digital payment accepted.</p></article>
        </div>
      </section>

      <!-- ░░ Service pricing ░░ -->
      <section class="section container section--flush-top" id="pricing" aria-labelledby="pricing-title">
        <header class="section__head" data-reveal>
          <p class="kicker"><span class="kicker__num">02</span><span data-ar="أسعار الخدمات">Service Pricing</span></p>
          <h2 class="section__title" id="pricing-title"><span data-ar="23 خدمة مُنتجة.">23 productized services.</span> <span class="grad-text" data-ar="نطاق ثابت. تسليم واضح.">Fixed scope. Clear delivery.</span></h2>
          <p class="section__lead" data-ar="كل سعر يعكس مشروعًا محددًا — لا تقديرًا. اختر فئة لاستكشافها.">Every price reflects a defined engagement — not an estimate. Click a category to explore.</p>
        </header>
        <div class="tabs" role="tablist" data-tabs="pricing" data-reveal><span class="tabs__ind" aria-hidden="true"></span>{tabs}</div>{panels}
      </section>

      <!-- ░░ FAQ ░░ -->
      <section class="section container section--flush-top" id="faq" aria-labelledby="faq-title">
        <div class="grid grid--side-l">
          <header class="section__head" data-reveal>
            <p class="kicker"><span class="kicker__num">03</span><span data-ar="الأسئلة الشائعة">FAQ</span></p>
            <h2 class="section__title" id="faq-title"><span data-ar="أسئلة شائعة،">Common questions,</span><br /><span class="grad-text" data-ar="إجابات مباشرة.">direct answers.</span></h2>
            <p class="section__lead" data-ar="لم تجد سؤالك؟ راسلنا وسنجيب خلال يوم عمل واحد.">Didn't find your question? Write to us and we'll answer within one business day.</p>
            {btn('Ask us directly', 'اسألنا مباشرة', '/contact/', 'glass', 'mail')}
          </header>
          <div class="faq" data-reveal style="--d:.1s">{faq}
          </div>
        </div>
      </section>

      {closing('GET STARTED', 'ابدأ الآن',
               '<span data-ar="نطاق واضح">Clear scope</span><br /><span class="grad-text" data-ar="من المكالمة الأولى.">from the first call.</span>',
               'Book a 30-minute discovery call. We define the engagement, confirm the fit, and give you a price — or tell you directly if we’re not the right match.',
               'احجز مكالمة استكشافية مدتها 30 دقيقة. نحدد المشروع ونؤكد الملاءمة ونعطيك سعرًا — أو نخبرك بصراحة إن لم نكن الخيار المناسب.',
               [btn('Book a Free Discovery Call', 'احجز مكالمة استكشافية مجانية', '/contact/#book'), btn('View All Services', 'كل الخدمات', '/services/', 'glass', 'arrow')])}
'''
    return [page('/pricing-faq/', title='Pricing & FAQ — Code & Canvas', title_ar='الأسعار والأسئلة الشائعة — Code & Canvas',
                 desc='Transparent pricing, no surprises. Milestone-based payment, 23 productized services with fixed scope across technology, brand, data, and healthcare — plus answers to the questions we hear most.',
                 desc_ar='أسعار شفافة بلا مفاجآت. دفعات حسب المعالم و23 خدمة مُنتجة بنطاق ثابت عبر التقنية والهوية والبيانات والرعاية الصحية — مع إجابات عن أكثر الأسئلة شيوعًا.',
                 nav='services', body=body)]
