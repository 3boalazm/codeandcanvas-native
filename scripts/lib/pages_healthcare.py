# -*- coding: utf-8 -*-
"""/healthcare/ — Healthcare track.

v3 architecture: a decision path for a clinic or hospital owner, the five
services as decision rows, the regulatory context with its verification status,
and a clinic-vs-hospital fit split. No unverified compliance claims.
"""
from catalog import SERVICES
from h import (esc, t, th, icon, crumbs, closing, btn, page, service_ld, PERSON_LD,
               sec_head, svc_rows, steps3, facts)

HC = [c for c in SERVICES if c.startswith('HC-')]

PATH = [
    ('01', 'Diagnose the gap', 'تشخيص الفجوة',
     'Where the clinic or hospital stands today: systems in place, data actually used, and the compliance items that are already late.',
     'أين تقف العيادة أو المستشفى اليوم: الأنظمة القائمة، والبيانات المستخدمة فعلًا، وبنود الامتثال المتأخرة بالفعل.',
     'Gap and risk list', 'قائمة الفجوات والمخاطر'),
    ('02', 'Choose with evidence', 'الاختيار بالدليل',
     'If a system purchase is coming, run a scored vendor selection before the demos begin — so the decision is defensible to the board.',
     'إذا كان شراء نظام قادمًا، نُجري اختيارًا موزونًا للمورّدين قبل بدء العروض — ليكون القرار قابلًا للدفاع أمام الإدارة.',
     'Scored criteria + RFP', 'معايير موزونة + طلب عروض'),
    ('03', 'Launch and train', 'الإطلاق والتدريب',
     'Identity, digital presence and clinical workflows shipped together, with the front desk and clinical staff trained on what changed.',
     'الهوية والحضور الرقمي ومسارات العمل السريرية تُسلَّم معًا، مع تدريب الاستقبال والفريق السريري على ما تغيّر.',
     'Launch + training', 'إطلاق + تدريب'),
    ('04', 'Measure and decide next', 'القياس والقرار التالي',
     'Dashboards tied to CBAHI-relevant KPIs, so the next investment is decided on numbers rather than on a vendor’s promise.',
     'لوحات مؤشرات مرتبطة بمؤشرات CBAHI، ليُبنى القرار الاستثماري التالي على أرقام لا على وعود مورّد.',
     'KPI dashboards', 'لوحات المؤشرات'),
]

CONTEXT = [
    ('CBAHI', 'Saudi central board for accreditation of healthcare institutions — the accreditation body clinic and hospital work is measured against in KSA.',
     'المركز السعودي لاعتماد المنشآت الصحية — الجهة التي يُقاس عليها عمل العيادات والمستشفيات في السعودية.'),
    ('NORA', 'The national health information exchange architecture — the interoperability frame KSA healthcare integrations are expected to follow.',
     'عمارة التبادل الوطني للمعلومات الصحية — الإطار الذي يُتوقع أن تتبعه التكاملات الصحية في السعودية.'),
    ('HL7 · FHIR · DICOM', 'The standards used to move clinical data between HIS, LIS, RIS/PACS and portals without rebuilding them every time.',
     'المعايير المستخدمة لنقل البيانات السريرية بين أنظمة HIS و LIS و RIS/PACS والبوابات دون إعادة بنائها كل مرة.'),
    ('ETA e-invoice (EG)', 'Egyptian tax authority e-invoicing requirements, relevant to clinic billing and pharmacy workflows in Egypt.',
     'متطلبات الفاتورة الإلكترونية لهيئة الضرائب المصرية، وترتبط بفوترة العيادات ومسارات الصيدليات في مصر.'),
]

FIT = [
    ('A clinic or a small group', 'عيادة أو مجموعة صغيرة', True,
     ['Clinic Digital Launch (HC-01) — identity, site, booking and Google presence in one engagement',
      'Clinic Brand Identity Kit (HC-04) if the digital presence already exists',
      'Healthcare BI (HC-02) once there are two or more branches to compare'],
     ['الإطلاق الرقمي للعيادات (HC-01) — هوية وموقع وحجوزات وحضور Google في مشروع واحد',
      'حزمة هوية العيادة (HC-04) إن كان الحضور الرقمي موجودًا بالفعل',
      'ذكاء الأعمال الصحي (HC-02) عند وجود فرعين أو أكثر للمقارنة']),
    ('A hospital or an investor', 'مستشفى أو مستثمر', False,
     ['HIS Selection Advisory (HC-03) before any system commitment',
      'Healthcare EA Assessment (HC-05) for EMRAM scoring and a 90-day roadmap',
      'Healthcare BI (HC-02) as the measurement layer under both'],
     ['استشارات اختيار نظام HIS (HC-03) قبل أي التزام بنظام',
      'تقييم العمارة المؤسسية الصحية (HC-05) لتحديد مرحلة EMRAM وخارطة 90 يومًا',
      'ذكاء الأعمال الصحي (HC-02) كطبقة قياس تحت كل ما سبق']),
]


def build():
    context = ''.join(f'''
          <article class="panel mini" data-reveal style="--d:{i * .05:.2f}s">
            <span class="mini__code">{esc(name)}</span>
            <p data-ar="{esc(ar)}">{esc(en)}</p>
          </article>''' for i, (name, en, ar) in enumerate(CONTEXT))

    fit = ''.join(f'''
          <article class="panel mini{' mini--warn' if not primary else ''}" data-reveal style="--d:{i * .05:.2f}s">
            <h3 data-ar="{esc(title_ar)}">{title_en}</h3>
            <ul class="svc-row__list">{''.join(f'<li data-ar="{esc(a)}">{esc(e)}</li>' for e, a in zip(items_en, items_ar))}</ul>
          </article>''' for i, (title_en, title_ar, primary, items_en, items_ar) in enumerate([(a, b, c, d, e) for a, b, c, d, e in FIT]))

    body = f'''
      <!-- ░░ Hero ░░ -->
      <section class="phero container phero--left" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('Solutions', 'الحلول', '/services/'), ('Healthcare', 'الرعاية الصحية', None)])}
        <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="عيادات ومستشفيات · السعودية ومصر · ثنائي اللغة">Clinics &amp; hospitals · KSA + Egypt · bilingual</span></span>
        <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s"><span data-ar="قرارات الرعاية الصحية">Healthcare decisions</span><br /><span class="grad-text" data-ar="تُبنى على بيانات وأدلة.">built on data and evidence.</span></h1>
        <p class="hero__lead" data-reveal style="--d:.16s" data-ar-html="خمس خدمات للعيادات والمستشفيات: الإطلاق الرقمي وذكاء الأعمال الصحي واستشارات اختيار HIS وهوية العيادة وتقييم العمارة المؤسسية. &lt;strong&gt;يُسلّمها فريق يحمل CPHIMS و EMRAM ويعمل بسياق سريري حقيقي.&lt;/strong&gt;">Five services for clinics and hospitals: digital launch, healthcare BI, HIS selection advisory, clinic identity and enterprise-architecture assessment. <strong>Delivered by a team holding CPHIMS and EMRAM, working with real clinical context.</strong></p>
        <div class="hero__ctas" data-reveal style="--d:.24s">
          {btn('Book a 30-min call', 'احجز مكالمة 30 دقيقة', '/contact/#book')}
          {btn('Healthcare pricing', 'أسعار الرعاية الصحية', '/pricing-faq/', 'glass')}
        </div>
        {facts([('Services', 'خدمات', '5', True), ('Engagements from', 'تبدأ المشاريع من', '$1,500', True),
                ('Built for', 'مبنية لـ', 'KSA + Egypt', True), ('Delivery', 'التسليم', '2–7 weeks', True)])}
      </section>

      <!-- ░░ 01 · The decision path ░░ -->
      <section class="section container" id="path" aria-labelledby="path-title">
        {sec_head('01', 'THE DECISION PATH', 'مسار القرار',
                  '<span id="path-title" data-ar="أربع خطوات">Four steps</span> <span class="grad-text" data-ar="من الفجوة إلى المقارنة.">from the gap to the comparison.</span>',
                  'This is the sequence a clinic owner or investor usually faces. You can enter it at any step — most enter at the second one, when a system purchase is already on the table.',
                  'هذا هو التسلسل الذي يواجهه صاحب العيادة أو المستثمر عادةً. يمكنك الدخول من أي خطوة — ومعظم العملاء يدخلون من الثانية حين يكون شراء النظام مطروحًا بالفعل.')}
        {steps3(PATH)}
      </section>

      <!-- ░░ 02 · Services ░░ -->
      <section class="section container" id="services" aria-labelledby="svc-title">
        {sec_head('02', 'THE SERVICES', 'الخدمات', '<span id="svc-title" data-ar="خمس خدمات.">Five services.</span> <span class="grad-text" data-ar="قرار واحد لكل صف.">One decision per row.</span>',
                  'Background on the founder’s healthcare work: <a href="/technology-services/#results">numbers with their limits</a>. Scope and price per service are below.',
                  'خلفية عمل المؤسس في الرعاية الصحية: <a href="/technology-services/#results">أرقام بحدودها</a>. النطاق والسعر لكل خدمة أدناه.',
                  aside=f'<a class="text-link" href="/pricing-faq/" data-track="navigation" data-track-to="pricing"><span data-ar="الأسعار وشروط الدفع">Prices &amp; payment terms</span>{icon("arrowUpRight", "flip")}</a>')}
        {svc_rows(HC)}
        <p class="note-quiet" style="margin-top:16px" data-ar-html="الأسعار استرشادية وتُثبَّت في العرض المكتوب. المشاريع الصحية تبدأ عادةً بمكالمة نطاق نحدد فيها ما هو &lt;em&gt;خارج&lt;/em&gt; النطاق بوضوح — من تشغيل النظام إلى مسؤوليات المورّد. &lt;a href=&quot;/contact/?inquiry=HC-03#message&quot;&gt;لست متأكدًا من أين تبدأ؟&lt;/a&gt;">Prices are indicative and fixed in the written proposal. Healthcare engagements start with a scoping call where we state plainly what is <em>out</em> of scope — from system operation to vendor responsibilities. <a href="/contact/?inquiry=HC-03#message">Not sure where to start?</a></p>
      </section>

      <!-- ░░ 03 · Regulatory context ░░ -->
      <section class="section section--band" id="context" aria-labelledby="ctx-title">
        <div class="container">
          {sec_head('03', 'REGULATORY CONTEXT', 'السياق التنظيمي',
                    '<span id="ctx-title" data-ar="المفردات التي">The vocabulary</span> <span class="grad-text" data-ar="تُناقش بها القرارات.">the decisions are made in.</span>',
                    'These are the frameworks and standards the work is delivered against. Anything project-specific — including which requirements apply to your facility — is confirmed with your quality and compliance leads before scope is fixed.',
                    'هذه هي الأطر والمعايير التي يُسلَّم العمل وفقها. أي تفصيل خاص بالمشروع — بما فيه المتطلبات التي تنطبق على منشأتك — يُؤكَّد مع مسؤولي الجودة والامتثال قبل تثبيت النطاق.')}
          <div class="grid-4">{context}
          </div>
          <p class="note-quiet" style="margin-top:16px" data-ar-html="لا ندّعي اعتمادًا تنظيميًا أو شهادة لمنشأتك. الاستشارة تُنتج تقييمًا ووثائق وخارطة طريق، والقرار النهائي والمسؤولية التنظيمية يبقيان لك وللمعنيين بالامتثال. &lt;a href=&quot;/contact/?inquiry=HC-03#message&quot;&gt;ناقش التفاصيل&lt;/a&gt;.">We do not claim regulatory accreditation or certification for your facility. The engagement produces an assessment, documents and a roadmap; the decision and regulatory responsibility stay with you and your compliance owners. <a href="/contact/?inquiry=HC-03#message">Discuss the detail</a>.</p>
        </div>
      </section>

      <!-- ░░ 04 · Which one are you ░░ -->
      <section class="section container" id="fit" aria-labelledby="fit-title">
        {sec_head('04', 'WHICH ONE ARE YOU?', 'أيّهما أنت؟', '<span id="fit-title" data-ar="عيادة صغيرة">A small clinic</span> <span class="grad-text" data-ar="أم مستشفى أو مستثمر؟">or a hospital / investor?</span>',
                  'The two paths need different first steps — pick the row that describes you and start there.',
                  'المساران يحتاجان أول خطوة مختلفة — اختر الصف الذي يصفك وابدأ منه.')}
        <div class="grid-2">{fit}
        </div>
      </section>

      {closing('START A HEALTHCARE ENGAGEMENT', 'ابدأ مشروعًا صحيًا',
               '<span data-ar="قرار صحي">A healthcare decision</span> <span class="grad-text" data-ar="تريد أن تدافع عنه؟">you need to defend?</span>',
               'Bring the situation — a system purchase, an accreditation deadline, a branch launch — and we will propose the smallest engagement that makes the next decision defensible.',
               'أحضر الحالة — شراء نظام أو موعد اعتماد أو إطلاق فرع — وسنقترح أصغر مشروع يجعل القرار التالي قابلًا للدفاع.',
               [btn('Book a 30-min call', 'احجز مكالمة 30 دقيقة', '/contact/#book'), btn('All 23 services', 'كل الخدمات الـ23', '/services/', 'glass')])}
'''
    return [page('/healthcare/', title='Healthcare Solutions — Clinics and hospitals in KSA and Egypt · Code & Canvas',
                 title_ar='حلول الرعاية الصحية — العيادات والمستشفيات في السعودية ومصر · Code & Canvas',
                 desc='Five healthcare services for clinics and hospitals: clinic digital launch, healthcare BI, HIS selection advisory, clinic brand identity and enterprise-architecture assessment — delivered with CPHIMS and EMRAM experience.',
                 desc_ar='خمس خدمات صحية للعيادات والمستشفيات: الإطلاق الرقمي للعيادات وذكاء الأعمال الصحي واستشارات اختيار نظام HIS وهوية العيادة وتقييم العمارة المؤسسية — بما يحمله الفريق من CPHIMS و EMRAM.',
                 nav='healthcare', body=body,
                 ld=[service_ld(HC, 'https://codeandcanvas.net/healthcare/'), PERSON_LD['ahmed'], PERSON_LD['mustafa']])]
