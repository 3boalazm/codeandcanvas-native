# -*- coding: utf-8 -*-
"""/technology-services/ — live copy of codeandcanvas.net/technology-services/."""
from catalog import SERVICES
from h import esc, t, th, icon, crumbs, closing, btn, page


def tags(items):
    return '<div class="pill-list" style="margin-top:14px">' + ''.join(f'<span class="pill">{esc(i)}</span>' for i in items) + '</div>'


def ticks(items, ar_items, cls='ticks'):
    return f'<ul class="{cls}">' + ''.join(f'<li data-ar="{esc(a)}">{esc(e)}</li>' for e, a in zip(items, ar_items)) + '</ul>'


def detail(code, *, cls, tag_list, included=None, included_ar=None, tiers=None, price_note=None, price_note_ar=None, lead_by=('Ahmed Bedeer', 'أحمد بدير'), featured=False, badge=('Most Requested', 'الأكثر طلبًا'), cta=('Book a Discovery Call', 'احجز مكالمة استكشافية')):
    s = SERVICES[code]
    inc = ''
    if included:
        inc = f'<h4 data-ar="ما الذي تشمله">What\'s included</h4>{ticks(included, included_ar, "ticks ticks--dense")}'
    tier_html = ''
    if tiers:
        rows = ''.join(
            f'<div class="tier{" tier--star" if tr.get("star") else ""}"><b data-ar="{esc(tr["name_ar"])}">{esc(tr["name"])}</b><strong>{esc(tr["price"])}</strong><p data-ar="{esc(tr["desc_ar"])}">{esc(tr["desc"])}</p><small data-ar="{esc(tr["dur_ar"])}">{esc(tr["dur"])}</small></div>'
            for tr in tiers)
        tier_html = f'<h4 data-ar="صيغ المشروع">Engagement tiers</h4><div class="tiers">{rows}</div>'
    star = f'<span class="sdetail__star" aria-hidden="true">⭐</span><span class="sdetail__badge" data-ar="{esc(badge[1])}">{esc(badge[0])}</span>' if featured else ''
    note = f'<small data-ar="{esc(price_note_ar)}">{esc(price_note)}</small>' if price_note else ''
    price = (t(s['price'], s['price_ar'], tag='strong') if s.get('price_ar') else f'<strong>{esc(s["price"])}</strong>')
    dur = t(s['dur'], s['dur_ar']) if s.get('dur_ar') else f'<span>{esc(s["dur"])}</span>'
    return f'''
        <article class="sdetail glass {cls}" id="{code.lower()}" data-category="{code.lower()}" data-reveal>
          <div>
            <div class="sdetail__head"><span class="sdetail__code">{code}</span>{star}{t(s['tag'], s['tag_ar'], cls='sdetail__tag') if s.get('tag_ar') else f'<span class="sdetail__tag">{esc(s["tag"])}</span>'}</div>
            <h3 data-ar="{esc(s['title_ar'])}">{esc(s['title'])}</h3>
            <p class="sdetail__lead" data-ar="{esc(s['blurb_ar'])}">{esc(s['blurb'])}</p>
            {tags(tag_list)}
            {inc}
            {tier_html}
          </div>
          <aside class="sdetail__side">
            <div class="sdetail__price">{price}{dur}{note}</div>
            <a class="btn btn--primary magnetic" href="/contact/#book"><span data-ar="{esc(cta[1])}">{cta[0]}</span><i class="flip" data-icon="arrowUpRight"></i></a>
            <a class="btn btn--glass" href="/pricing-faq/"><span data-ar="شروط الدفع والأسئلة الشائعة">Payment terms &amp; FAQ</span></a>
            <span class="sdetail__lead-by">{icon('users')}<span data-ar="يقودها">Led by</span> <b data-ar="{esc(lead_by[1])}">{lead_by[0]}</b></span>
          </aside>
        </article>'''


CAPS = [
    ('EA', 'Enterprise Architecture', 'العمارة المؤسسية', 'TOGAF-aligned roadmaps, capability modeling, operating models, and IT governance. Translates strategy into structured BDAT layers.', 'خرائط طريق متوافقة مع TOGAF ونمذجة القدرات ونماذج التشغيل وحوكمة تقنية المعلومات. تترجم الاستراتيجية إلى طبقات BDAT منظمة.', ['Sparx EA', 'Visual Paradigm', 'ArchiMate']),
    ('DX', 'Digital Transformation', 'التحول الرقمي', 'Business–IT alignment, process re-engineering, automation, and KPI-driven execution. From transformation roadmaps to value realization.', 'مواءمة الأعمال مع تقنية المعلومات وإعادة هندسة العمليات والأتمتة والتنفيذ المقاد بمؤشرات الأداء. من خرائط طريق التحول إلى تحقيق القيمة.', ['NORA', 'TOGAF', 'KPI Frameworks']),
    ('⚕ HC', 'Healthcare Informatics', 'المعلوماتية الصحية', 'HIS, EHR/EMR, LIS, RIS/PACS, ICU and patient portals. End-to-end clinical workflow design and HIMSS Stage 6 readiness.', 'أنظمة HIS و EHR/EMR و LIS و RIS/PACS والعناية المركزة وبوابات المرضى. تصميم مسارات العمل السريرية من البداية للنهاية وجاهزية HIMSS المرحلة 6.', ['HIMSS', 'CPHIMS', 'HL7 · FHIR']),
    ('⇄ INT', 'Integration & Interoperability', 'التكامل والتشغيل البيني', 'Mirth Connect integration bus, FHIR APIs, HL7 v2.x, and DICOM. Terminology mapping against LOINC and SNOMED CT.', 'ناقل تكامل Mirth Connect وواجهات FHIR و HL7 v2.x و DICOM. ربط المصطلحات وفق LOINC و SNOMED CT.', ['Mirth', 'API-First', 'REST · iPaaS']),
    ('Σ DATA', 'Data & Analytics', 'البيانات والتحليلات', 'ODS → EDW pipelines, ETL orchestration, BI dashboards, and predictive analytics. Data governance and population health registries.', 'خطوط ODS ← EDW وتنسيق ETL ولوحات ذكاء الأعمال والتحليلات التنبؤية. حوكمة البيانات وسجلات صحة السكان.', ['Power BI', 'Tableau', 'Python · SQL']),
    ('{} DEV', 'Software Engineering', 'هندسة البرمجيات', 'Java 17/Spring Boot microservices, Node.js services, OODA design, RESTful APIs, and PostgreSQL platforms — API-first.', 'خدمات مصغّرة بـ Java 17/Spring Boot وخدمات Node.js وتصميم OODA وواجهات RESTful ومنصات PostgreSQL — الواجهات أولًا.', ['Java · Spring', 'Node.js', 'PostgreSQL']),
    ('☁ CLOUD', 'Cloud & Infrastructure', 'السحابة والبنية التحتية', 'Docker, Kubernetes, VLAN-segmented networks, HA WAN links, active-passive clustering, and DR with sub-1% RTO failover.', 'Docker و Kubernetes وشبكات مقسّمة بـ VLAN ووصلات WAN عالية التوافر وتجميع نشط-خامل وتعافٍ من الكوارث بزمن تحويل أقل من 1%.', ['Docker', 'Kubernetes', 'Aruba · Palo Alto']),
    ('🛡 SEC', 'Security & Compliance', 'الأمن والامتثال', 'Privacy-by-design controls satisfying HIPAA & GDPR — AAA model, audit logging, encryption-at-rest, and healthcare regulation.', 'ضوابط الخصوصية بالتصميم المستوفية لـ HIPAA و GDPR — نموذج AAA وسجلات التدقيق والتشفير أثناء التخزين والتنظيمات الصحية.', ['HIPAA', 'GDPR', 'AAA · IAM']),
    ('⚙ PMO', 'Project & Program Delivery', 'تسليم المشاريع والبرامج', 'Active PMO collaboration, technical documentation, vendor & SOW review, and SME advisory. Lean Six Sigma and Agile.', 'تعاون فعّال مع مكاتب إدارة المشاريع وتوثيق تقني ومراجعة المورّدين ونطاقات العمل واستشارات الخبراء. Lean Six Sigma و Agile.', ['Agile', 'Lean Six Sigma', 'PMO']),
]


def build():
    caps = ''.join(f'''
          <article class="card glass tile" data-tilt data-reveal style="--d:{(i % 3) * .07:.2f}s">
            <span class="tile__num">{esc(code)}</span>
            <h3 data-ar="{esc(ar)}">{esc(en)}</h3>
            <p data-ar="{esc(dar)}">{esc(den)}</p>
            <div class="tile__foot"><div class="pill-list">{''.join(f'<span class="pill">{esc(x)}</span>' for x in tl)}</div></div>
          </article>''' for i, (code, en, ar, den, dar, tl) in enumerate(CAPS))

    body = f'''
      <!-- ░░ Hero ░░ -->
      <section class="phero container" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('Solutions', 'الحلول', '/services/'), ('Technology Services', 'خدمات التقنية', None)])}
        <div class="phero__split">
          <div>
            <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="التقنية · العمارة · التحول · البيانات">Technology · Architecture · Transformation · Data</span></span>
            <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s"><span data-ar="نصمّم عمارة">Architecting</span><br /><span class="grad-text" data-ar="التحول الرقمي.">digital transformation.</span></h1>
            <p class="hero__lead" data-reveal style="--d:.16s" data-ar-html="العمارة المؤسسية · التحول الرقمي · المعلوماتية الصحية · عمارة الحلول · السحابة · الاستشارات التنفيذية. &lt;strong&gt;6 خدمات. ممارسة واحدة.&lt;/strong&gt; كل مشروع يُنتج مخرجات يستطيع التنفيذيون التصرف بناءً عليها — لا أوراقًا تُركن على الرف.">Enterprise Architecture · Digital Transformation · Healthcare Informatics · Solution Architecture · Cloud · Executive Advisory. <strong>6 services. One practice.</strong> Every engagement produces artifacts executives can act on — not shelfware.</p>
            <div class="hero__ctas" data-reveal style="--d:.24s">{btn('Book a Call', 'احجز مكالمة', '/contact/#book')}{btn('Portfolio', 'الأعمال', 'https://ahmed-bedeer.vercel.app/', 'glass')}</div>
          </div>
          <div class="phero__aside" data-reveal style="--d:.2s">
            <div class="stats__inner glass" style="grid-template-columns:repeat(2,1fr)">
              <div class="stat"><span class="stat__num stat__num--ltr"><span data-count="7" data-latin="1">7</span>+</span><p class="stat__label" data-ar-html="سنوات في&lt;br /&gt;السعودية والمنطقة">Years across<br />KSA &amp; MENA</p></div>
              <div class="stat"><span class="stat__num stat__num--ltr"><span data-count="3" data-latin="1">3</span></span><p class="stat__label" data-ar-html="أطر&lt;br /&gt;معمارية">Architecture<br />frameworks</p></div>
              <div class="stat"><span class="stat__num stat__num--ltr"><span data-count="85" data-latin="1">85</span>%</span><p class="stat__label" data-ar-html="جاهزية HIMSS&lt;br /&gt;المرحلة 6 المحققة">HIMSS Stage 6<br />readiness achieved</p></div>
              <div class="stat"><span class="stat__num stat__num--ltr"><span data-count="12" data-latin="1">12</span>+</span><p class="stat__label" data-ar-html="معيارًا تقنيًا&lt;br /&gt;ومعيار امتثال">Tech &amp;<br />compliance stds</p></div>
            </div>
          </div>
        </div>
      </section>

      <!-- ░░ Bio ░░ -->
      <section class="section container section--tight" aria-labelledby="bio-title">
        <article class="card glass person person--big" data-reveal>
          <div class="art art--portrait" data-slot="team/ahmed-bedeer"><span class="art__mark">AB</span><span class="art__cap" data-ar="{{ }} الكود">{{ }} THE CODE</span></div>
          <div>
            <p class="person__role" data-ar="مهندس معماري مؤسسي · متخصص في التحول الرقمي">Enterprise Architect · Digital Transformation Specialist</p>
            <h2 id="bio-title">Ahmed Bedeer</h2>
            <p class="person__tag" data-ar="شريك مؤسس · Code &amp; Canvas · الخبر، السعودية">Co-Founder · Code &amp; Canvas · Al Khobar, KSA</p>
            <p data-ar="مهندس معماري مؤسسي ومتخصص في التحول الرقمي بخبرة تتجاوز 7 سنوات في السعودية — عبر قطاعات الرعاية الصحية والحكومة والقطاع الخاص. حاصل على شهادة CPHIMS وبخبرة فعلية في تقييمات HIMSS EMRAM. خبرة في عمارة TOGAF/NORA واختيار موردي أنظمة HIS والهجرة السحابية وتحليلات البيانات وبناء قدرات العمارة المؤسسية بما يتماشى مع رؤية 2030.">Enterprise Architect and Digital Transformation Specialist with 7+ years in KSA — working across healthcare, government, and private sector. CPHIMS-certified with active HIMSS EMRAM assessment experience. Expertise in TOGAF/NORA architecture, HIS vendor selection, cloud migration, data analytics, and EA capability building aligned to Vision 2030.</p>
            <div class="creds" aria-label="Skills" data-ar-label="المهارات"><span>TOGAF</span><span>NORA</span><span>CPHIMS</span><span>EMRAM</span><span>ArchiMate</span><span>Sparx EA</span><span>Java · Spring</span><span>Power BI</span><span>FHIR · HL7</span><span>Vision 2030</span></div>
            <div class="person__links">
              <a href="https://ahmed-bedeer.vercel.app/" target="_blank" rel="noopener" title="Ahmed's Portfolio">{icon('link')}<span data-ar="الأعمال">Portfolio</span></a>
              <a href="/contact/#book">{icon('calendar')}<span data-ar="احجز مكالمة ←">Book a Call →</span></a>
              <a href="https://www.linkedin.com/in/ahmed-bedeer" target="_blank" rel="noopener">{icon('users')}<span>LinkedIn</span></a>
              <a href="https://github.com/ahmedbdeer" target="_blank" rel="noopener">{icon('kanban')}<span>GitHub</span></a>
            </div>
          </div>
        </article>
      </section>

      <!-- ░░ Credentials ░░ -->
      <section class="section container section--tight section--flush-top" aria-labelledby="cred-title">
        <header class="section__head" data-reveal>
          <p class="kicker"><span class="kicker__num">01</span><span data-ar="اعتمادات فعّالة · ليست أطرًا مُدرجة فحسب">ACTIVE CREDENTIALS · NOT LISTED FRAMEWORKS</span></p>
          <h2 class="section__title" id="cred-title"><span data-ar="اعتمادات تُستخدم">Credentials used</span> <span class="grad-text" data-ar="في كل مشروع ذي صلة.">in every relevant engagement.</span></h2>
        </header>
        <div class="grid grid--4">
          <article class="card glass tile" data-tilt data-reveal><span class="card__icon">{icon('award')}</span><h3>CPHIMS</h3><p data-ar="محترف معتمد في المعلوماتية الصحية">Certified Professional in Health Informatics</p><div class="tile__foot" data-ar="HIMSS · المعلوماتية الصحية وإدارة المعلومات">HIMSS · Health Informatics &amp; Info Mgmt</div></article>
          <article class="card glass tile" data-tilt data-reveal style="--d:.07s"><span class="card__icon">{icon('shield')}</span><h3>EMRAM</h3><p data-ar="مقيّم نموذج تبنّي السجلات الطبية الإلكترونية">EMR Adoption Model Assessor</p><div class="tile__foot" data-ar="HIMSS · مقيّم مراحل معتمد">HIMSS · Certified Stage Assessor</div></article>
          <article class="card glass tile" data-tilt data-reveal style="--d:.14s"><span class="card__icon">{icon('layers')}</span><h3>TOGAF</h3><p data-ar="إطار العمارة المؤسسية">Enterprise Architecture Framework</p><div class="tile__foot" data-ar="The Open Group · تسليم مرتكز على ADM">The Open Group · ADM-anchored delivery</div></article>
          <article class="card glass tile" data-tilt data-reveal style="--d:.21s"><span class="card__icon">{icon('plug')}</span><h3>NORA</h3><p data-ar="منصة التبادل الصحي الوطنية · السعودية">National Health Exchange · KSA</p><div class="tile__foot" data-ar="وزارة الصحة السعودية · عمارة تكامل فعّالة">Saudi MOH · Active integration architecture</div></article>
        </div>
      </section>

      <!-- ░░ Outcomes ░░ -->
      <section class="section container section--tight section--flush-top" aria-labelledby="out-title">
        <header class="section__head" data-reveal>
          <p class="kicker"><span class="kicker__num">02</span><span data-ar="نتائج · لا مجرد مخططات">OUTCOMES · NOT JUST DIAGRAMS</span></p>
          <h2 class="section__title" id="out-title"><span data-ar="أرقام من">Numbers from</span> <span class="grad-text" data-ar="مشاريع حقيقية.">real engagements.</span></h2>
        </header>
        <div class="grid grid--4">
          <article class="card glass tile" data-tilt data-reveal><strong class="art__mark" style="font-size:44px">12%</strong><h3 style="margin-top:12px" data-ar="خفض مدة الإقامة في العناية المركزة">ICU LOS Reduction</h3><p data-ar="التحليلات التنبؤية وتنبيهات فجوات الرعاية المدمجة في مستودع البيانات دعمت التواصل السريري الاستباقي">Predictive analytics &amp; care-gap alerting integrated into the EDW supported proactive clinical outreach</p></article>
          <article class="card glass tile" data-tilt data-reveal style="--d:.07s"><strong class="art__mark" style="font-size:44px">25%</strong><h3 style="margin-top:12px" data-ar="إقفال شهري أسرع">Faster Month-End Close</h3><p data-ar="مسارات دورة الإيرادات المنمذجة بـ UML بسّطت دورة الطلبات وعمليات تسجيل الرسوم">UML-modeled revenue-cycle workflows streamlined order lifecycle and charge capture processes</p></article>
          <article class="card glass tile" data-tilt data-reveal style="--d:.14s"><strong class="art__mark" style="font-size:44px">40%</strong><h3 style="margin-top:12px" data-ar="أعباء إدارية أقل">Less Admin Overhead</h3><p data-ar="تطبيق Java/Spring Boot متمحور حول المريض أتمت مسارات المواعيد والتأمين من البداية للنهاية">Patient-centric Java/Spring Boot application automated appointment and insurance workflows end-to-end</p></article>
          <article class="card glass tile" data-tilt data-reveal style="--d:.21s"><strong class="art__mark" style="font-size:44px">$500K+</strong><h3 style="margin-top:12px" data-ar="وفورات تكلفة مرصودة">Cost-Savings Identified</h3><p data-ar="لوحة تحليل سوق مؤتمتة قدّمت رؤى لحظية قادت قرارات قابلة للقياس لأصحاب المصلحة">Automated market analysis dashboard delivered real-time insights that drove measurable stakeholder decisions</p></article>
        </div>
      </section>

      <!-- ░░ Services ░░ -->
      <section class="section container" id="services" aria-labelledby="svc-title">
        <header class="section__head" data-reveal>
          <p class="kicker"><span class="kicker__num">03</span><span data-ar="6 خدمات تقنية">6 Technology Services</span></p>
          <h2 class="section__title" id="svc-title"><span data-ar="عمارة. تحوّل.">Architecture. Transformation.</span><br /><span class="grad-text" data-ar="بيانات. سحابة. استشارات.">Data. Cloud. Advisory.</span></h2>
        </header>
        <div class="toolbar" data-reveal>
          <p><span data-ar="تصفية حسب الممارسة">Filter by practice</span> <i data-icon="arrowDown" aria-hidden="true"></i></p>
          <div class="filters" role="group" aria-label="Filter services" data-ar-label="تصفية الخدمات" data-filter-group="#svc-list">
            <button class="filter is-active" type="button" data-filter="all" aria-pressed="true"><span data-ar="الكل">All</span><b>6</b></button>
            <button class="filter" type="button" data-filter="ab-01" aria-pressed="false"><span data-ar="العمارة والاستراتيجية">EA &amp; Strategy</span><b>1</b></button>
            <button class="filter" type="button" data-filter="ab-02" aria-pressed="false"><span data-ar="الرعاية الصحية">Healthcare</span><b>1</b></button>
            <button class="filter" type="button" data-filter="ab-03" aria-pressed="false"><span data-ar="البيانات">Data</span><b>1</b></button>
            <button class="filter" type="button" data-filter="ab-04" aria-pressed="false"><span data-ar="عمارة الحلول">Solution Arch</span><b>1</b></button>
            <button class="filter" type="button" data-filter="ab-05" aria-pressed="false"><span data-ar="السحابة">Cloud</span><b>1</b></button>
            <button class="filter" type="button" data-filter="ab-06" aria-pressed="false"><span data-ar="الاستشارات">Advisory</span><b>1</b></button>
          </div>
        </div>
        <div id="svc-list">
        {detail('AB-01', cls='', featured=True,
                tag_list=['TOGAF ADM', 'ArchiMate 3.1', 'NORA Alignment', 'Capability Mapping', 'Sparx EA', 'Architecture Governance', 'Vision 2030'],
                included=['Architecture Vision & Capability Mapping', 'Business · Data · Application · Tech layers (BDAT)', 'NORA alignment for KSA programs', 'ArchiMate modelling & documentation', 'Architecture Governance Board enablement', '90-day phased action plan', 'Business-to-Technology Alignment Matrix'],
                included_ar=['رؤية العمارة ورسم خرائط القدرات', 'طبقات الأعمال · البيانات · التطبيقات · التقنية (BDAT)', 'مواءمة NORA لبرامج السعودية', 'نمذجة وتوثيق ArchiMate', 'تمكين مجلس حوكمة العمارة', 'خطة عمل مرحلية لمدة 90 يومًا', 'مصفوفة مواءمة الأعمال مع التقنية'],
                tiers=[dict(name='EA Quick-Start Assessment', name_ar='تقييم البداية السريعة للعمارة المؤسسية', price='$1,000 – $2,500', dur='2 weeks · TOGAF-anchored', dur_ar='أسبوعان · مرتكز على TOGAF', desc='Current state across BDAT layers · capability gap analysis · Business-to-Technology Alignment Matrix · 90-day action plan · ArchiMate / Sparx EA documentation.', desc_ar='الوضع الحالي عبر طبقات BDAT · تحليل فجوات القدرات · مصفوفة مواءمة الأعمال مع التقنية · خطة عمل 90 يومًا · توثيق ArchiMate / Sparx EA.', star=True),
                       dict(name='Digital Transformation Advisory (extended)', name_ar='استشارات التحول الرقمي (موسّعة)', price='$3,000 – $8,000', dur='4–8 weeks · NORA / Vision 2030', dur_ar='⁦4–8⁩ أسابيع · NORA / رؤية 2030', desc='Governance model design · phased roadmap · NORA & Vision 2030 alignment · KPI framework · stakeholder presentation.', desc_ar='تصميم نموذج الحوكمة · خارطة طريق مرحلية · مواءمة NORA ورؤية 2030 · إطار مؤشرات الأداء · عرض لأصحاب المصلحة.')],
                price_note='Start an EA Engagement → from $1,000', price_note_ar='ابدأ مشروع عمارة مؤسسية ← ابتداءً من ⁦$1,000⁩', cta=('Start an EA Engagement', 'ابدأ مشروع عمارة مؤسسية'))}
        {detail('AB-02', cls='', tag_list=['HIS · EHR · EMR', 'HL7 · FHIR · DICOM', 'Mirth Connect', 'HIMSS EMRAM', 'CBAHI · NORA'], price_note='CPHIMS · EMRAM · NORA', price_note_ar='CPHIMS · EMRAM · NORA')}
        {detail('AB-03', cls='', tag_list=['Power BI · Tableau', 'Python · SQL', 'EDW · ETL', 'Master Data', 'KPI Frameworks'],
                tiers=[dict(name='Analytics Dashboard', name_ar='لوحة تحليلات', price='$800 – $2,000', dur='1–2 weeks · Power BI · Python', dur_ar='⁦1–2⁩ أسبوع · Power BI · Python', desc='Operational data → executive dashboards · Power BI or Tableau delivery · Python data pipeline (if needed) · decision intelligence framing · entry point to an EA engagement.', desc_ar='بيانات تشغيلية ← لوحات تنفيذية · تسليم عبر Power BI أو Tableau · خط بيانات Python (عند الحاجة) · تأطير ذكاء القرار · مدخل لمشروع عمارة مؤسسية.')])}
        {detail('AB-04', cls='', tag_list=['Java · Spring Boot', 'Node.js', 'PostgreSQL', 'Microservices', 'API Design'], price_note='Scoped per engagement', price_note_ar='يُحدَّد نطاقه لكل مشروع',
                tiers=[dict(name='Application Portfolio Discovery', name_ar='استكشاف محفظة التطبيقات', price='$800 – $2,000', dur='3–5 days · .NET stacks', dur_ar='⁦3–5⁩ أيام · أنظمة .NET', desc='Automated .NET source analysis · application landscape map · service dependency map · technical documentation · replaces weeks of manual discovery.', desc_ar='تحليل آلي لشفرة .NET · خريطة مشهد التطبيقات · خريطة اعتماديات الخدمات · توثيق تقني · يحل محل أسابيع من الاستكشاف اليدوي.')])}
        {detail('AB-05', cls='', tag_list=['Docker · Kubernetes', 'HA · DR Architecture', 'VLAN · Firewalls', 'Hybrid Cloud', 'Observability'],
                included=['Workload assessment', 'Provider evaluation matrix', 'Migration sequencing plan', 'Risk register', 'Cloud governance framework'],
                included_ar=['تقييم الأحمال', 'مصفوفة تقييم المزوّدين', 'خطة تسلسل الهجرة', 'سجل المخاطر', 'إطار حوكمة السحابة'])}
        {detail('AB-06', cls='', tag_list=['Vendor Review', 'PMO Governance', 'SOW Review', 'Lean Six Sigma', 'Agile Enablement'])}
        </div>
      </section>

      <!-- ░░ Capabilities ░░ -->
      <section class="section container section--flush-top" id="capabilities" aria-labelledby="cap-title">
        <header class="section__head" data-reveal>
          <p class="kicker"><span class="kicker__num">04</span><span data-ar="9 قدرات · ممارسة واحدة">9 Capabilities · One Practice</span></p>
          <h2 class="section__title" id="cap-title"><span data-ar="حيث يكمن">Where the</span> <span class="grad-text" data-ar="العمق.">depth lives.</span></h2>
          <p class="section__lead" data-ar="كل قدرة ترتبط بنتيجة أعمال قابلة للقياس — هذا هو الخط الفاصل بين مهندس الحلول والمهندس المعماري المؤسسي.">Each capability ties back to a measurable business outcome — that's the line between a solution architect and an enterprise architect.</p>
        </header>
        <div class="grid grid--3">{caps}
        </div>
      </section>

      <!-- ░░ Engagement model ░░ -->
      <section class="section container section--flush-top" aria-labelledby="model-title">
        <header class="section__head" data-reveal>
          <p class="kicker"><span class="kicker__num">05</span><span data-ar="نموذج التعاون">Engagement model</span></p>
          <h2 class="section__title" id="model-title"><span data-ar="نموذج تعاون">An engagement model</span> <span class="grad-text" data-ar="مبني لاتخاذ القرار.">built for decisions.</span></h2>
          <p class="section__lead" data-ar="كل مشروع يُنتج مخرجات يستطيع التنفيذيون التصرف بناءً عليها — لا أوراقًا تُركن على الرف.">Every engagement produces artifacts that executives can act on — not shelfware.</p>
        </header>
        <div class="grid grid--3">
          <article class="card glass tile" data-tilt data-reveal><span class="card__icon">{icon('layers')}</span><h3 data-ar="عروض معمارية">Architecture Views</h3><p data-ar="نماذج ArchiMate / UML ومخططات BDAT في Sparx EA أو Visual Paradigm — المصدر الحي القابل للمراجعة لكل قرار معماري يُتخذ أثناء المشروع.">ArchiMate / UML models and BDAT diagrams in Sparx EA or Visual Paradigm — the living, reviewable source of truth for every architecture decision made during the engagement.</p></article>
          <article class="card glass tile" data-tilt data-reveal style="--d:.07s"><span class="card__icon">{icon('chart')}</span><h3 data-ar="ملخصات تنفيذية من صفحة واحدة">Executive One-Pagers</h3><p data-ar="عروض وملخصات موجزة تترجم العمارة إلى لغة الاستثمار والمخاطر والنتائج لمجلس الإدارة — ليقرر صانعو القرار لا ليكتفوا بالمشاهدة.">Slide decks and concise summaries that translate architecture into investment, risk, and outcome language for the board — so the decision-makers can decide, not just observe.</p></article>
          <article class="card glass tile" data-tilt data-reveal style="--d:.14s"><span class="card__icon">{icon('sparkles')}</span><h3 data-ar="جولات شرح">Walkthroughs</h3><p data-ar="جولات قصيرة ومركّزة في فلسفة التصميم والمفاضلات — محتوى متعدد الوسائط ليفهمه كل صاحب مصلحة أيًا كان عمقه التقني.">Short, focused walkthroughs of design philosophy and trade-offs — multi-modal content so every stakeholder gets it, regardless of their technical depth.</p></article>
        </div>
      </section>

      <!-- ░░ CTA ░░ -->
      <section class="section container section--tight" aria-labelledby="cta-title">
        <div class="callout glass glass--deep" data-reveal>
          <div>
            <p class="kicker"><span data-ar="ابدأ مشروعًا">START AN ENGAGEMENT</span></p>
            <h3 id="cta-title"><span data-ar="لديك تحوّل">Have a transformation</span><br /><span class="grad-text" data-ar="يحتاج إلى عمارة؟">to architect?</span></h3>
            <p data-ar="سواء كان بناء مستشفى جديد أو برنامج حوكمة بيانات أو تحديثًا سحابيًا — أخبرني بمشكلة العمل وسأقترح أخف مشروع يوصلك إلى قرار واثق.">Whether it's a greenfield hospital build, a data-governance program, or a cloud modernization — tell me the business problem and I'll propose the lightest engagement that gets you a confident decision.</p>
          </div>
          <div class="callout__actions">
            {btn('Book a Discovery Call', 'احجز مكالمة استكشافية', '/contact/#book')}
            <a class="text-link" href="https://ahmed-bedeer.vercel.app/" target="_blank" rel="noopener"><span data-ar="عرض الأعمال ↗">View Portfolio ↗</span></a>
          </div>
        </div>
        <ul class="promises glass" data-reveal aria-label="Engagement principles" data-ar-label="مبادئ التعاون" style="grid-template-columns:repeat(5,1fr)">
          <li>{icon('check')}<span data-ar="TOGAF · NORA · CPHIMS فعّالة">TOGAF · NORA · CPHIMS active</span></li>
          <li>{icon('check')}<span data-ar="مخرجات يتصرف التنفيذيون بناءً عليها">Artifacts executives can act on</span></li>
          <li>{icon('check')}<span data-ar="دفعات حسب المعالم">Milestone-based payment</span></li>
          <li>{icon('check')}<span data-ar="السعودية + مصر · عن بُعد">KSA + Egypt · Remote</span></li>
          <li>{icon('check')}<span data-ar="العربية والإنجليزية">Arabic &amp; English</span></li>
        </ul>
      </section>

      {closing("CAN'T WAIT TO HEAR FROM YOU", 'نتطلع لسماعك',
               '<span data-ar="لا نطيق الانتظار">Can’t Wait To</span><br /><span class="grad-text" data-ar="لنسمع منك.">Hear From You.</span>',
               'Book an appointment, get started with a brief, or browse the full catalogue of services.',
               'احجز موعدًا، أو ابدأ بموجز مختصر، أو تصفّح كتالوج الخدمات الكامل.',
               [btn('Book an Appointment', 'احجز موعدًا', '/contact/#book'), btn('Get Started', 'ابدأ الآن', '/contact/', 'glass'), btn('Full Services', 'كل الخدمات', '/services/', 'ghost', 'arrow')])}
'''
    return [page('/technology-services/', title='Technology Services — Code & Canvas', title_ar='خدمات التقنية — Code & Canvas',
                 desc='Enterprise Architecture · Digital Transformation · Healthcare Informatics · Solution Architecture · Cloud · Executive Advisory. 6 services, one practice — led by Ahmed Bedeer (CPHIMS, TOGAF, EMRAM, NORA).',
                 desc_ar='العمارة المؤسسية · التحول الرقمي · المعلوماتية الصحية · عمارة الحلول · السحابة · الاستشارات التنفيذية. 6 خدمات وممارسة واحدة — بقيادة أحمد بدير (CPHIMS، TOGAF، EMRAM، NORA).',
                 nav='services', body=body)]
