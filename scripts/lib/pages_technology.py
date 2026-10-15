# -*- coding: utf-8 -*-
"""/technology-services/ — Technology track.

v3 architecture: every service is a decision row (who it is for, what you keep,
duration, price), followed by how the engagement runs, the credentials behind it,
attributed numbers with their limits, and who delivers.
"""
from catalog import SERVICES
from h import (esc, t, th, icon, crumbs, closing, btn, page, service_ld, PERSON_LD,
               sec_head, svc_rows, steps3, facts)

AB = [c for c in SERVICES if c.startswith('AB-')]

CAPS = [
    ('EA', 'Enterprise Architecture', 'العمارة المؤسسية',
     'Capability models, operating models and IT governance that translate strategy into BDAT layers.',
     'نمذجة القدرات ونماذج التشغيل وحوكمة تقنية المعلومات التي تترجم الاستراتيجية إلى طبقات BDAT.', ['TOGAF', 'ArchiMate', 'Sparx EA']),
    ('HC', 'Healthcare Informatics', 'المعلوماتية الصحية',
     'HIS, EHR/EMR, LIS, RIS/PACS and patient portals, with clinical workflow design and HIMSS Stage 6 readiness.',
     'أنظمة HIS و EHR/EMR و LIS و RIS/PACS وبوابات المرضى، مع تصميم المسارات السريرية وجاهزية HIMSS المرحلة 6.', ['CPHIMS', 'HIMSS', 'HL7 · FHIR']),
    ('INT', 'Integration & Interoperability', 'التكامل والتشغيل البيني',
     'Integration engines, FHIR APIs, HL7 v2.x and DICOM, with terminology mapping against LOINC and SNOMED CT.',
     'محرّكات التكامل وواجهات FHIR و HL7 v2.x و DICOM، مع ربط المصطلحات وفق LOINC و SNOMED CT.', ['FHIR', 'HL7 v2.x', 'DICOM']),
    ('DATA', 'Data & Analytics', 'البيانات والتحليلات',
     'ODS → EDW pipelines, ETL orchestration, BI dashboards and predictive analytics with a data-governance model.',
     'خطوط ODS ← EDW وتنسيق ETL ولوحات ذكاء الأعمال والتحليلات التنبؤية مع نموذج لحوكمة البيانات.', ['Power BI', 'Python · SQL', 'EDW']),
    ('CLOUD', 'Cloud & Infrastructure', 'السحابة والبنية التحتية',
     'Workload assessment, migration sequencing, HA/DR posture and a 3-year TCO model — not a lift-and-shift.',
     'تقييم الأحمال وتسلسل الهجرة ووضعية التوافر العالي/التعافي ونموذج تكلفة لثلاث سنوات — لا نقلًا أعمى.', ['Docker · K8s', 'HA · DR', 'TCO']),
    ('PMO', 'Programme Delivery', 'تسليم البرامج',
     'PMO collaboration, vendor and SOW review, technical documentation and SME advisory across the programme.',
     'التعاون مع مكاتب إدارة المشاريع ومراجعة المورّدين ونطاقات العمل والتوثيق التقني واستشارات الخبراء.', ['Agile', 'SOW Review', 'Governance']),
]

CREDS = [
    ('CPHIMS', 'Certified Professional in Health Informatics', 'محترف معتمد في المعلوماتية الصحية', 'HIMSS · health informatics and information management', 'HIMSS · المعلوماتية الصحية وإدارة المعلومات', 'award'),
    ('EMRAM', 'EMR Adoption Model assessor', 'مقيّم نموذج تبنّي السجلات الطبية الإلكترونية', 'HIMSS · certified stage assessment', 'HIMSS · تقييم معتمد للمراحل', 'shield'),
    ('TOGAF', 'Enterprise architecture framework', 'إطار العمارة المؤسسية', 'The Open Group · ADM-anchored delivery', 'The Open Group · تسليم مرتكز على ADM', 'layers'),
    ('NORA', 'National health exchange architecture · KSA', 'عمارة التبادل الصحي الوطني · السعودية', 'Saudi MOH · active integration architecture', 'وزارة الصحة السعودية · عمارة تكامل فعّالة', 'plug'),
]

RESULTS = [
    ('12%', 'ICU length-of-stay reduction', 'خفض مدة الإقامة في العناية المركزة',
     'Predictive analytics and care-gap alerting integrated into the EDW supported proactive clinical outreach.',
     'التحليلات التنبؤية وتنبيهات فجوات الرعاية المدمجة في مستودع البيانات دعمت التواصل السريري الاستباقي.'),
    ('25%', 'Faster month-end close', 'إقفال شهري أسرع',
     'UML-modelled revenue-cycle workflows streamlined the order lifecycle and charge capture.',
     'مسارات دورة الإيرادات المنمذجة بـ UML بسّطت دورة الطلبات وتسجيل الرسوم.'),
    ('40%', 'Less administrative overhead', 'أعباء إدارية أقل',
     'A patient-centric Java/Spring Boot application automated appointment and insurance workflows end to end.',
     'تطبيق متمحور حول المريض بـ Java/Spring Boot أتمّ مسارات المواعيد والتأمين من البداية للنهاية.'),
    ('$500K+', 'Cost savings identified', 'وفورات تكلفة مرصودة',
     'An automated market-analysis dashboard delivered insights that drove measurable stakeholder decisions.',
     'لوحة تحليل سوق مؤتمتة قدّمت رؤى قادت قرارات قابلة للقياس لأصحاب المصلحة.'),
]


def build():
    creds = ''.join(f'''
          <article class="panel mini" data-reveal style="--d:{i * .05:.2f}s">
            <span class="card__icon">{icon(ic)}</span>
            <h3>{name}</h3>
            <p data-ar="{esc(p_ar)}">{p_en}</p>
            <span class="mini__foot" data-ar="{esc(f_ar)}">{f_en}</span>
          </article>''' for i, (name, p_en, p_ar, f_en, f_ar, ic) in enumerate(CREDS))

    caps = ''.join(f'''
          <article class="panel mini" data-reveal style="--d:{(i % 3) * .05:.2f}s">
            <span class="mini__code">{code}</span>
            <h3 data-ar="{esc(h_ar)}">{h_en}</h3>
            <p data-ar="{esc(p_ar)}">{p_en}</p>
            <div class="pill-list mini__tags">{''.join(f'<span class="pill">{esc(x)}</span>' for x in tags)}</div>
          </article>''' for i, (code, h_en, h_ar, p_en, p_ar, tags) in enumerate(CAPS))

    results = ''.join(f'''
          <article class="panel mini" data-reveal style="--d:{i * .05:.2f}s">
            <strong class="mini__num ltr">{n}</strong>
            <h3 data-ar="{esc(t_ar)}">{t_en}</h3>
            <p data-ar="{esc(d_ar)}">{d_en}</p>
          </article>''' for i, (n, t_en, t_ar, d_en, d_ar) in enumerate(RESULTS))

    body = f'''
      <!-- ░░ Hero ░░ -->
      <section class="phero container phero--left" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('Solutions', 'الحلول', '/services/'), ('Technology Services', 'خدمات التقنية', None)])}
        <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="العمارة · التحوّل · البيانات · السحابة">Architecture · Transformation · Data · Cloud</span></span>
        <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s"><span data-ar="عمارة تقنية">Technology architecture</span><br /><span class="grad-text" data-ar="تُقرَّر قبل أن يُنفَّق المال.">decided before the money moves.</span></h1>
        <p class="hero__lead" data-reveal style="--d:.16s" data-ar-html="ست خدمات يقودها مؤسس واحد بخبرة تتجاوز 7 سنوات في السعودية: العمارة المؤسسية والتحوّل الصحي وهندسة البيانات وعمارة الحلول والسحابة والاستشارات التنفيذية. &lt;strong&gt;كل مشروع ينتهي بمخرجات يستطيع التنفيذيون التصرف بناءً عليها.&lt;/strong&gt;">Six services led by one founder with 7+ years in KSA: enterprise architecture, healthcare transformation, data engineering, solution architecture, cloud and executive advisory. <strong>Every engagement ends with artifacts executives can act on.</strong></p>
        <div class="hero__ctas" data-reveal style="--d:.24s">
          {btn('Book a 30-min call', 'احجز مكالمة 30 دقيقة', '/contact/#book')}
          {btn('Founder portfolio', 'أعمال المؤسس', 'https://ahmed-bedeer.vercel.app/', 'glass')}
        </div>
        {facts([('Services', 'خدمات', '6', True), ('Experience in KSA', 'سنوات في السعودية', '7+ years', True),
                ('Frameworks', 'الأطر', 'TOGAF · NORA', True), ('Delivery', 'نموذج التسليم', 'Milestone-based', False, 'حسب المعالم')])}
      </section>

      <!-- ░░ 01 · Services ░░ -->
      <section class="section container" id="services" aria-labelledby="svc-title">
        {sec_head('01', 'THE SERVICES', 'الخدمات',
                  '<span id="svc-title" data-ar="ست خدمات.">Six services.</span> <span class="grad-text" data-ar="قرار واحد في كل صف.">One decision per row.</span>',
                  'Read who each service is for and what you keep before you see a price. Probe prices are published ranges, fixed in a written proposal after the scoping call.',
                  'اقرأ لمن الخدمة وما الذي تحصل عليه قبل أن ترى السعر. الأسعار نطاقات منشورة وتُثبَّت في عرض مكتوب بعد مكالمة النطاق.',
                  aside=f'<a class="text-link" href="#model" data-track="navigation" data-track-to="model"><span data-ar="كيف يدور المشروع">How an engagement runs</span>{icon("arrowDown", "flip")}</a>')}
        {svc_rows(AB)}
        <p class="note-quiet" style="margin-top:16px" data-ar-html="الأسعار استرشادية بالدولار وتُحدَّد نهائيًا في العرض المكتوب. وكل خدمة يمكن أن تكون مشروعًا مستقلًا أو مرحلة داخل برنامج أكبر — &lt;a href=&quot;/contact/?inquiry=custom#message&quot;&gt;أخبرنا بالسياق&lt;/a&gt;.">Prices are indicative USD ranges, finalised in the written proposal. Any service can stand alone or become a phase inside a larger programme — <a href="/contact/?inquiry=custom#message">tell us the context</a>.</p>
      </section>

      <!-- ░░ 02 · Engagement model ░░ -->
      <section class="section section--band" id="model" aria-labelledby="model-title">
        <div class="container">
          {sec_head('02', 'ENGAGEMENT MODEL', 'نموذج التعاون',
                    '<span id="model-title" data-ar="ثلاث خطوات.">Three steps.</span> <span class="grad-text" data-ar="لا ساعات مفتوحة.">No open-ended hours.</span>',
                    'The same three steps run on every technology engagement, from a two-week assessment to a multi-year programme.',
                    'الخطوات الثلاث نفسها في كل مشروع تقني — من تقييم أسبوعين إلى برنامج يمتد سنوات.')}
          {steps3([
              ('01', 'Assessment', 'التقييم', 'Current state across business, data, application and technology layers, with capability gaps and constraints named explicitly.', 'الوضع الحالي عبر طبقات الأعمال والبيانات والتطبيقات والتقنية، مع تسمية فجوات القدرات والقيود بوضوح.', 'Current-state findings', 'نتائج الوضع الحالي'),
              ('02', 'Architecture', 'العمارة', 'Target state, options and trade-offs, governance model and sequenced roadmap with the decisions that are genuinely yours to make.', 'الوضع المستهدف والخيارات والمفاضلات ونموذج الحوكمة وخارطة طريق متسلسلة بالقرارات التي تخصك فعلًا.', 'Target architecture + roadmap', 'العمارة المستهدفة وخارطة الطريق'),
              ('03', 'Enablement', 'التمكين', 'Executive one-pagers, walkthroughs with the delivery team, and documentation your own architects can extend after the engagement ends.', 'ملخصات تنفيذية وجولات مع فريق التنفيذ وتوثيق يستطيع معماريوك توسيعه بعد انتهاء المشروع.', 'Documented, extendable models', 'نماذج موثقة قابلة للتوسيع'),
          ])}
          <div class="grid-3" style="margin-top:22px">
            <article class="panel mini" data-reveal><h3 data-ar="عروض معمارية">Architecture views</h3><p data-ar="نماذج ArchiMate و UML ومخططات BDAT في Sparx EA أو Visual Paradigm — المصدر الحي القابل للمراجعة لكل قرار معماري.">ArchiMate / UML models and BDAT diagrams in Sparx EA or Visual Paradigm — the living, reviewable source of truth for each architecture decision.</p></article>
            <article class="panel mini" data-reveal style="--d:.05s"><h3 data-ar="ملخصات تنفيذية">Executive one-pagers</h3><p data-ar="صفحة واحدة تترجم العمارة إلى لغة الاستثمار والمخاطر والنتيجة لمجلس الإدارة — ليقرر صنّاع القرار لا يكتفوا بالمشاهدة.">One page per decision that translates architecture into investment, risk and outcome language for the board.</p></article>
            <article class="panel mini" data-reveal style="--d:.1s"><h3 data-ar="جولات شرح">Walkthroughs</h3><p data-ar="جولات قصيرة ومركّزة في فلسفة التصميم والمفاضلات — ليفهمها كل صاحب مصلحة أيًا كان عمقه التقني.">Short, focused walkthroughs of the design philosophy and trade-offs, so every stakeholder gets it regardless of technical depth.</p></article>
          </div>
        </div>
      </section>

      <!-- ░░ 03 · Credentials ░░ -->
      <section class="section container" id="credentials" aria-labelledby="cred-title">
        {sec_head('03', 'CREDENTIALS', 'الاعتمادات',
                  '<span id="cred-title" data-ar="أطر مستخدمة في العمل">Frameworks used in the work</span> <span class="grad-text" data-ar="لا مُدرجة على السيرة.">not listed on a CV.</span>',
                  'Each of these is part of how the work is actually delivered or assessed — not a badge added after the fact.',
                  'كل واحدة من هذه جزء من طريقة تنفيذ العمل أو تقييمه — لا شارة أُضيفت لاحقًا.')}
        <div class="grid-4">{creds}
        </div>
      </section>

      <!-- ░░ 04 · Depth ░░ -->
      <section class="section container" id="capabilities" aria-labelledby="cap-title">
        {sec_head('04', 'DEPTH', 'العمق', '<span id="cap-title" data-ar="أين يقع العمق.">Where the depth lives.</span>',
                  'Six capability areas. Each one ties back to a business decision rather than to a technology stack.',
                  'ست قدرات. كل واحدة ترتبط بقرار عمل لا بمجموعة تقنيات.', center=False)}
        <div class="grid-3">{caps}
        </div>
      </section>

      <!-- ░░ 05 · Evidence and limits ░░ -->
      <section class="section container" id="results" aria-labelledby="out-title">
        {sec_head('05', 'EVIDENCE &amp; LIMITS', 'الإثبات وحدوده',
                  '<span id="out-title" data-ar="أرقام بحدودها.">Numbers with their limits.</span>',
                  'These figures come from engagements led by the founder and are reported as such. They are not independently audited, and they are not a promise of the same result elsewhere.',
                  'هذه الأرقام من مشاريع قادها المؤسس وتُنشر بهذه الصفة. ليست مدققة بشكل مستقل، وليست وعدًا بالنتيجة نفسها في مكان آخر.')}
        <div class="grid-4">{results}
        </div>
        <p class="note-quiet" style="margin-top:16px" data-ar-html="لأي رقم هنا نُشر مقياسه وحدوده: النطاق، الفترة، ومن قاسه — عند مناقشة مشروع مشابه. الأمثلة التي ننشرها هي رسوم توضيحية للنطاق، &lt;a href=&quot;/case-studies/&quot;&gt;وليست لقطات منتج&lt;/a&gt;.">For any figure, the measurement basis and limits are published at kickoff: scope, period and who measured it. Published visuals are scope diagrams, <a href="/case-studies/">not product screenshots</a>.</p>
      </section>

      <!-- ░░ 06 · Who delivers ░░ -->
      <section class="section container" id="who" aria-labelledby="bio-title">
        {sec_head('06', 'WHO DELIVERS', 'من ينفّذ', '<span id="bio-title" data-ar="مؤسس واحد يقود كل مشروع —">One founder leads every engagement —</span> <span class="grad-text" data-ar="لا فريق مبيعات.">not a sales team.</span>', None, None)}
        <article class="panel person" data-reveal>
          <div class="art art--portrait" data-slot="team/ahmed-bedeer"><span class="art__mark">AB</span><span class="art__cap" data-ar="{{ }} الكود">{{ }} THE CODE</span></div>
          <div>
            <p class="person__role" data-ar="مهندس معماري مؤسسي · متخصص في التحول الرقمي">Enterprise Architect · Digital Transformation Specialist</p>
            <h3>Ahmed M. Bedeer</h3>
            <p class="person__tag" data-ar="شريك مؤسس · Code &amp; Canvas · الخبر، السعودية">Co-Founder · Code &amp; Canvas · Al Khobar, KSA</p>
            <p data-ar="مهندس معماري مؤسسي ومتخصص في التحول الرقمي بخبرة تتجاوز 7 سنوات في السعودية — عبر الرعاية الصحية والقطاع الحكومي والخاص. حاصل على CPHIMS وبخبرة فعلية في تقييمات HIMSS EMRAM، مع عمارة TOGAF/NORA واختيار موردي HIS والهجرة السحابية وتحليلات البيانات.">Enterprise architect and digital transformation specialist with 7+ years in KSA across healthcare, government and private sector. CPHIMS-certified with active HIMSS EMRAM assessment experience, working on TOGAF/NORA architecture, HIS vendor selection, cloud migration and data analytics.</p>
            <div class="creds" aria-label="Skills" data-ar-label="المهارات"><span>TOGAF</span><span>NORA</span><span>CPHIMS</span><span>EMRAM</span><span>ArchiMate</span><span>Sparx EA</span><span>Power BI</span><span>FHIR · HL7</span></div>
            <div class="person__links">
              <a href="https://ahmed-bedeer.vercel.app/" target="_blank" rel="noopener" title="Ahmed's portfolio">{icon('link')}<span data-ar="الأعمال ↗">Portfolio ↗</span></a>
              <a href="/team/#ahmed">{icon('users')}<span data-ar="ملفه في صفحة الفريق">Team profile</span></a>
              <a href="/contact/#book">{icon('calendar')}<span data-ar="احجز مكالمة">Book a call</span></a>
            </div>
          </div>
        </article>
      </section>

      {closing('START AN ENGAGEMENT', 'ابدأ مشروعًا',
               '<span data-ar="لديك قرار تقني">A technology decision</span> <span class="grad-text" data-ar="يستحق عمارة؟">worth architecting?</span>',
               'Tell us the business problem — greenfield hospital, data governance programme or cloud migration — and we will propose the lightest engagement that gets you a confident decision.',
               'أخبرنا بمشكلة العمل — مستشفى جديد أو برنامج حوكمة بيانات أو هجرة سحابية — وسنقترح أخف مشروع يوصلك إلى قرار واثق.',
               [btn('Book a 30-min call', 'احجز مكالمة 30 دقيقة', '/contact/#book'), btn('All 23 services', 'كل الخدمات الـ23', '/services/', 'glass')])}
'''
    return [page('/technology-services/', title='Technology Services — Enterprise architecture, data and cloud · Code & Canvas',
                 title_ar='خدمات التقنية — العمارة المؤسسية والبيانات والسحابة · Code & Canvas',
                 desc='Six technology services led by Ahmed Bedeer (CPHIMS, TOGAF, EMRAM, NORA): enterprise architecture, healthcare transformation, data architecture, solution architecture, cloud modernisation and executive advisory — with scope, deliverables and price ranges.',
                 desc_ar='ست خدمات تقنية بقيادة أحمد بدير (CPHIMS، TOGAF، EMRAM، NORA): العمارة المؤسسية والتحول الصحي وهندسة البيانات وعمارة الحلول والتحديث السحابي والاستشارات التنفيذية — بالنطاق والمخرجات والنطاقات السعرية.',
                 nav='services', body=body,
                 ld=[service_ld(AB, 'https://codeandcanvas.net/technology-services/'), PERSON_LD['ahmed']])]
