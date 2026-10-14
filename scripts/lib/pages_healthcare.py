# -*- coding: utf-8 -*-
"""/healthcare/ — the healthcare track as a real page (the live site only had a
`/services/#healthcare` anchor that pointed nowhere and a `/healthcare-hub/`
duplicate of the creative page). Copy is assembled from the live HC cards,
the pricing page bullets, and Ahmed's credentials/outcomes."""
from h import esc, icon, crumbs, closing, btn, page
from pages_technology import detail


def build():
    both = ('Ahmed Bedeer + Mustafa Aboalazm', 'أحمد بدير + مصطفى أبو العزم')
    ahmed = ('Ahmed Bedeer', 'أحمد بدير')
    mustafa = ('Mustafa Aboalazm', 'مصطفى أبو العزم')
    body = f'''
      <!-- ░░ Hero ░░ -->
      <section class="phero container" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('Solutions', 'الحلول', '/services/'), ('Healthcare', 'الرعاية الصحية', None)])}
        <div class="phero__split">
          <div>
            <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="الرعاية الصحية · CPHIMS · EMRAM · CBAHI · NORA">Healthcare · CPHIMS · EMRAM · CBAHI · NORA</span></span>
            <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s"><span data-ar="تعمل في الرعاية الصحية؟">Working in healthcare?</span><br /><span class="grad-text" data-ar="لنتحدث بالتفاصيل.">Let’s talk specifics.</span></h1>
            <p class="hero__lead" data-reveal style="--d:.16s" data-ar-html="&lt;strong&gt;خمس خدمات صحية مُنتجة&lt;/strong&gt; للعيادات والمراكز الطبية والمستشفيات في السعودية ومصر — من هوية تبني ثقة المرضى إلى اختيار نظام HIS وجاهزية EMRAM. المكالمات الاستكشافية متخصصة بالقطاع — نأتي مستعدين بسياق CBAHI و HIMSS EMRAM و NORA ومسارات العمل السريرية."><strong>Five productized healthcare services</strong> for clinics, medical centres, and hospitals in KSA and Egypt — from patient-trust identity to HIS selection and EMRAM readiness. Discovery calls are sector-specific — we come prepared with CBAHI, HIMSS EMRAM, NORA, and clinical workflow context already built in.</p>
            <div class="hero__ctas" data-reveal style="--d:.24s">{btn('Book a Healthcare Discovery Call', 'احجز مكالمة استكشافية للرعاية الصحية', '/contact/#book')}{btn('See the 5 services', 'استعرض الخدمات الخمس', '#services', 'glass', 'arrowDown')}</div>
          </div>
          <div class="phero__aside" data-reveal style="--d:.2s">
            <div class="stats__inner glass" style="grid-template-columns:repeat(2,1fr)">
              <div class="stat"><span class="stat__num stat__num--ltr"><span data-count="85" data-latin="1">85</span>%</span><p class="stat__label" data-ar-html="جاهزية HIMSS&lt;br /&gt;المرحلة 6 المحققة">HIMSS Stage 6<br />readiness achieved</p></div>
              <div class="stat"><span class="stat__num stat__num--ltr"><span data-count="12" data-latin="1">12</span>%</span><p class="stat__label" data-ar-html="خفض مدة الإقامة&lt;br /&gt;في العناية المركزة">ICU length-of-stay<br />reduction</p></div>
              <div class="stat"><span class="stat__num stat__num--ltr"><span data-count="5" data-latin="1">5</span></span><p class="stat__label" data-ar-html="خدمات صحية&lt;br /&gt;مُنتجة">Productized<br />healthcare services</p></div>
              <div class="stat"><span class="stat__num stat__num--ltr">$50–200K</span><p class="stat__label" data-ar-html="كلفة الخروج من&lt;br /&gt;نظام HIS خاطئ">Cost to exit<br />a wrong HIS</p></div>
            </div>
          </div>
        </div>
      </section>

      <!-- ░░ Who leads what ░░ -->
      <section class="section container section--tight" aria-labelledby="lead-title">
        <div class="grid grid--3">
          <article class="card glass tile" data-tilt data-reveal><span class="card__icon">{icon('stethoscope')}</span><h3 id="lead-title" data-ar="يقودها أحمد بدير">Led by Ahmed Bedeer</h3><p data-ar="الخدمات الصحية المتخصصة (HC-03، HC-05) يقودها أحمد بدير — CPHIMS، مقيّم HIMSS EMRAM، NORA — بخبرة أكثر من 7 سنوات في السعودية عبر الرعاية الصحية والحكومة والقطاع الخاص.">Healthcare-specific services (HC-03, HC-05) are led by Ahmed Bedeer — CPHIMS, HIMSS EMRAM assessor, NORA — with 7+ years in KSA across healthcare, government, and the private sector.</p></article>
          <article class="card glass tile" data-tilt data-reveal style="--d:.07s"><span class="card__icon">{icon('pen')}</span><h3 data-ar="يقودها مصطفى أبو العزم">Led by Mustafa Aboalazm</h3><p data-ar="مشاريع الهوية الصحية فقط (HC-04) يقودها مصطفى — إشارات ثقة للمرضى وتصميم واعٍ بالمتطلبات التنظيمية وتسليم ثنائي اللغة.">Brand-only healthcare engagements (HC-04) are led by Mustafa — patient trust signals, regulatory-aware design, bilingual delivery.</p></article>
          <article class="card glass tile tile--accent" data-tilt data-reveal style="--d:.14s"><span class="card__icon">{icon('sparkles')}</span><h3 data-ar="مشاريع متكاملة">Combined engagements</h3><p data-ar="المشاريع المتكاملة (HC-01، HC-02) يشارك فيها المؤسسان معًا — وتُسعَّر كباقة واحدة، دون فوترة مزدوجة أبدًا.">Combined engagements (HC-01, HC-02) involve both founders — quoted as a single package, never double-billed.</p></article>
        </div>
      </section>

      <!-- ░░ Services ░░ -->
      <section class="section container section--flush-top" id="services" aria-labelledby="svc-title">
        <header class="section__head" data-reveal>
          <p class="kicker"><span class="kicker__num">01</span><span data-ar="5 خدمات صحية · HC-01 → HC-05">5 Healthcare Services · HC-01 → HC-05</span></p>
          <h2 class="section__title" id="svc-title"><span data-ar="مبنية للعيادات والمستشفيات">Built for clinics and hospitals</span><br /><span class="grad-text" data-ar="في السعودية ومصر.">in KSA and Egypt.</span></h2>
          <p class="section__lead" data-ar="واعية بمتطلبات CBAHI · متوافقة مع NORA · عربي + إنجليزي كمعيار. كل خدمة بنطاق ثابت ودفعات حسب المعالم.">CBAHI-aware · NORA-compliant · AR + EN as standard. Every service has a fixed scope and milestone-based payment.</p>
        </header>
        <div id="svc-list">
        {detail('HC-01', cls='sdetail--health', featured=True, lead_by=both,
                tag_list=['Brand identity', 'Bilingual digital presence', 'Booking system', 'Google presence', 'Social kit', 'CBAHI-aware', 'NORA-compliant'],
                included=['Brand identity + bilingual digital presence', 'Booking system + Google presence', 'CBAHI-aware design', 'NORA-compliant patient comms', 'AR + EN as standard', '30-day post-launch support'],
                included_ar=['هوية العلامة + حضور رقمي ثنائي اللغة', 'نظام حجوزات + حضور على Google', 'تصميم واعٍ بمتطلبات CBAHI', 'تواصل مع المرضى متوافق مع NORA', 'عربي + إنجليزي كمعيار', 'دعم 30 يومًا بعد الإطلاق'],
                price_note='Brand + Tech · 50 / 25 / 25', price_note_ar='هوية + تقنية · 50 / 25 / 25', cta=('Start Clinic Launch', 'ابدأ إطلاق العيادة'))}
        {detail('HC-02', cls='sdetail--health', lead_by=both, tag_list=['Power BI', 'CBAHI KPI library', 'Patient flow', 'Revenue cycle', 'Executive reporting'],
                included=['Clinical operational data → dashboards', 'CBAHI KPI library included', 'BD insight layer', 'Executive reporting format'],
                included_ar=['بيانات تشغيلية سريرية ← لوحات مؤشرات', 'مكتبة مؤشرات CBAHI مضمّنة', 'طبقة رؤى تطوير الأعمال', 'صيغة تقارير تنفيذية'],
                price_note='Combined · 50 / 50', price_note_ar='متكاملة · 50 / 50', cta=('Start HC-BI', 'ابدأ ذكاء الأعمال الصحي'))}
        {detail('HC-03', cls='sdetail--health', lead_by=ahmed, tag_list=['CPHIMS-delivered', 'CBAHI + NORA', 'Vendor scoring (10+ vendors)', 'RFP template', 'Contract review'],
                included=['Clinical workflow mapping', 'Vendor scoring matrix (10+ vendors)', 'RFP template', 'Contract review checklist', '⚠ Wrong HIS: $50K–$200K exposure'],
                included_ar=['رسم مسارات العمل السريرية', 'مصفوفة تقييم المورّدين (+10 مورّدين)', 'قالب طلب العروض (RFP)', 'قائمة مراجعة العقد', '⚠ نظام HIS خاطئ: تعرّض بقيمة ⁦$50K–$200K⁩'],
                price_note='EA + CPHIMS · 50 / 50', price_note_ar='عمارة مؤسسية + CPHIMS · 50 / 50', cta=('Start HIS Advisory', 'ابدأ استشارات HIS'))}
        {detail('HC-04', cls='sdetail--health', lead_by=mustafa, tag_list=['Patient trust signals', 'Regulatory-aware design', 'Bilingual AR/EN', 'Signage · stationery', 'Patient-facing templates'],
                included=['Logo system + bilingual AR/EN lockup', 'Patient trust signals built into the identity', 'Regulatory-aware design (CBAHI context)', 'Signage, stationery, and patient-facing templates', 'Brand guidelines (AR + EN)'],
                included_ar=['منظومة شعار + تركيب ثنائي اللغة عربي/إنجليزي', 'إشارات ثقة للمرضى مدمجة في الهوية', 'تصميم واعٍ بالمتطلبات التنظيمية (سياق CBAHI)', 'لوحات وقرطاسية وقوالب موجّهة للمرضى', 'دليل العلامة (عربي + إنجليزي)'],
                price_note='Brand · 50 / 25 / 25', price_note_ar='هوية · 50 / 25 / 25', cta=('Start Clinic Identity', 'ابدأ هوية العيادة'))}
        {detail('HC-05', cls='sdetail--health', lead_by=ahmed, tag_list=['TOGAF-anchored', 'EMRAM stage scoring', 'CBAHI readiness', 'NORA alignment', '90-day roadmap'],
                included=['EMRAM stage scoring', 'CBAHI readiness gap report', 'NORA alignment review', '90-day technology roadmap'],
                included_ar=['تحديد مرحلة EMRAM', 'تقرير فجوات الجاهزية لـ CBAHI', 'مراجعة المواءمة مع NORA', 'خارطة طريق تقنية لمدة 90 يومًا'],
                price_note='EA + EMRAM · 50 / 50', price_note_ar='عمارة مؤسسية + EMRAM · 50 / 50', cta=('Start EA Assessment', 'ابدأ تقييم العمارة'))}
        </div>
      </section>

      <!-- ░░ Credentials + outcomes ░░ -->
      <section class="section container section--flush-top" aria-labelledby="cred-title">
        <header class="section__head" data-reveal>
          <p class="kicker"><span class="kicker__num">02</span><span data-ar="اعتمادات فعّالة · نتائج لا مجرد مخططات">ACTIVE CREDENTIALS · OUTCOMES, NOT JUST DIAGRAMS</span></p>
          <h2 class="section__title" id="cred-title"><span data-ar="سياق سريري">Clinical context</span> <span class="grad-text" data-ar="من المكالمة الأولى.">from the first call.</span></h2>
        </header>
        <div class="grid grid--4">
          <article class="card glass tile" data-tilt data-reveal><span class="card__icon">{icon('award')}</span><h3>CPHIMS</h3><p data-ar="محترف معتمد في المعلوماتية الصحية — HIMSS">Certified Professional in Health Informatics — HIMSS</p></article>
          <article class="card glass tile" data-tilt data-reveal style="--d:.07s"><span class="card__icon">{icon('shield')}</span><h3>HIMSS EMRAM</h3><p data-ar="مقيّم مراحل معتمد لنموذج تبنّي السجلات الطبية الإلكترونية">Certified stage assessor — EMR Adoption Model</p></article>
          <article class="card glass tile" data-tilt data-reveal style="--d:.14s"><span class="card__icon">{icon('check')}</span><h3>CBAHI</h3><p data-ar="جاهزية اعتماد المركز السعودي لاعتماد المنشآت الصحية مدمجة في كل مشروع صحي">Saudi accreditation readiness built into every HC engagement</p></article>
          <article class="card glass tile" data-tilt data-reveal style="--d:.21s"><span class="card__icon">{icon('plug')}</span><h3>NORA</h3><p data-ar="منصة التبادل الصحي الوطنية · وزارة الصحة السعودية · عمارة تكامل فعّالة">National Health Exchange · Saudi MOH · active integration architecture</p></article>
        </div>
        <div class="grid grid--3" style="margin-top:18px">
          <article class="card glass tile" data-tilt data-reveal><strong class="art__mark" style="font-size:44px">12%</strong><h3 style="margin-top:12px" data-ar="خفض مدة الإقامة في العناية المركزة">ICU LOS Reduction</h3><p data-ar="التحليلات التنبؤية وتنبيهات فجوات الرعاية المدمجة في مستودع البيانات دعمت التواصل السريري الاستباقي">Predictive analytics &amp; care-gap alerting integrated into the EDW supported proactive clinical outreach</p></article>
          <article class="card glass tile" data-tilt data-reveal style="--d:.07s"><strong class="art__mark" style="font-size:44px">25%</strong><h3 style="margin-top:12px" data-ar="إقفال شهري أسرع">Faster Month-End Close</h3><p data-ar="مسارات دورة الإيرادات المنمذجة بـ UML بسّطت دورة الطلبات وعمليات تسجيل الرسوم">UML-modeled revenue-cycle workflows streamlined order lifecycle and charge capture processes</p></article>
          <article class="card glass tile" data-tilt data-reveal style="--d:.14s"><strong class="art__mark" style="font-size:44px">40%</strong><h3 style="margin-top:12px" data-ar="أعباء إدارية أقل">Less Admin Overhead</h3><p data-ar="تطبيق Java/Spring Boot متمحور حول المريض أتمت مسارات المواعيد والتأمين من البداية للنهاية">Patient-centric Java/Spring Boot application automated appointment and insurance workflows end-to-end</p></article>
        </div>
      </section>

      <!-- ░░ CTA ░░ -->
      <section class="section container section--tight" aria-labelledby="cta-title">
        <div class="callout glass glass--deep" data-reveal>
          <div>
            <p class="kicker"><span data-ar="المؤسسات الصحية">HEALTHCARE ORGANIZATIONS</span></p>
            <h3 id="cta-title"><span data-ar="أحضر تحدّيك.">Bring your challenge.</span> <span class="grad-text" data-ar="سنأتي بالسياق.">We’ll bring the context.</span></h3>
            <p data-ar="سواء كانت عيادة جديدة تحتاج هوية وحضورًا رقميًا، أو مستشفى يختار نظام HIS، أو مجلس إدارة يريد لوحات CBAHI — أخبرنا بمشكلة العمل وسنقترح أخف مشروع يوصلك إلى قرار واثق.">Whether it's a new clinic that needs an identity and digital presence, a hospital choosing an HIS, or a board that wants CBAHI dashboards — tell us the business problem and we'll propose the lightest engagement that gets you a confident decision.</p>
          </div>
          <div class="callout__actions">
            {btn('Book a Healthcare Discovery Call', 'احجز مكالمة استكشافية للرعاية الصحية', '/contact/#book')}
            <a class="text-link" href="https://wa.me/966545520750" target="_blank" rel="noopener">{icon('chat')}<span data-ar="واتساب · السعودية">WhatsApp · KSA</span></a>
          </div>
        </div>
        <ul class="promises glass" data-reveal aria-label="Engagement principles" data-ar-label="مبادئ التعاون">
          <li>{icon('check')}<span data-ar="نطاق واضح من المكالمة الأولى">Clear scope from the first call</span></li>
          <li>{icon('check')}<span data-ar="دفعات حسب المعالم — دون عقود مستمرة">Milestone-based payment — no retainers</span></li>
          <li>{icon('check')}<span data-ar="سنخبرك إن لم نكن الخيار المناسب">We’ll tell you if we’re not the right match</span></li>
          <li>{icon('check')}<span data-ar="السعودية + مصر · تغطية MENA">KSA + Egypt · MENA coverage</span></li>
        </ul>
      </section>

      {closing("CAN'T WAIT TO HEAR FROM YOU", 'نتطلع لسماعك',
               '<span data-ar="لا نطيق الانتظار">Can’t Wait To</span><br /><span class="grad-text" data-ar="لنسمع منك.">Hear From You.</span>',
               'Book an appointment, get started with a brief, or browse the full catalogue of services.',
               'احجز موعدًا، أو ابدأ بموجز مختصر، أو تصفّح كتالوج الخدمات الكامل.',
               [btn('Book an Appointment', 'احجز موعدًا', '/contact/#book'), btn('Get Started', 'ابدأ الآن', '/contact/', 'glass'), btn('Full Services', 'كل الخدمات', '/services/', 'ghost', 'arrow')])}
'''
    return [page('/healthcare/', title='Healthcare Solutions — Code & Canvas', title_ar='حلول الرعاية الصحية — Code & Canvas',
                 desc='Five productized healthcare services for clinics and hospitals in KSA and Egypt — Clinic Digital Launch, Healthcare BI, HIS Selection Advisory, Clinic Brand Identity, Healthcare EA + EMRAM. CPHIMS · EMRAM · CBAHI · NORA.',
                 desc_ar='خمس خدمات صحية مُنتجة للعيادات والمستشفيات في السعودية ومصر — الإطلاق الرقمي للعيادات وذكاء الأعمال الصحي واستشارات اختيار HIS وهوية العيادة وتقييم العمارة الصحية + EMRAM. CPHIMS · EMRAM · CBAHI · NORA.',
                 nav='healthcare', body=body)]
