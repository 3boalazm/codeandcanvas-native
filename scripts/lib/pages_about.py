# -*- coding: utf-8 -*-
"""/about/ — the studio page: position, six structural differences, the two tracks,
and the engagement process. v3 editorial layout (numbered heads, dense rows)."""
from h import esc, icon, crumbs, closing, btn, page, sec_head, steps3, facts, PERSON_LD

WHY = [
    ('Productized, not open-ended', 'مُنتجة، لا مفتوحة النهاية',
     'Every engagement has <strong>defined scope, fixed milestones, and a traceable business outcome</strong>. Retainers are available only for specified services. No surprise scope creep. You know exactly what you\'re buying before signing.',
     'كل مشروع له <strong>نطاق محدد ومعالم ثابتة ونتيجة أعمال قابلة للتتبع</strong>. تتاح الاشتراكات للخدمات المحددة فقط. لا توسّع مفاجئ في النطاق. تعرف تمامًا ما تشتريه قبل التوقيع.'),
    ('BD logic in every track', 'منطق تطوير الأعمال في كل مسار',
     'Whether we\'re building a brand or an architecture, the starting point is always the same: <strong>your business goals</strong>. We use the Business Motivation Model before any design or tech decision is made.',
     'سواء كنا نبني علامة أو عمارة، نقطة البداية واحدة دائمًا: <strong>أهداف عملك</strong>. نستخدم نموذج دوافع الأعمال (BMM) قبل أي قرار تصميمي أو تقني.'),
    ('Dual expertise — one studio', 'خبرة مزدوجة — استوديو واحد',
     'An Enterprise Architect and a Brand Identity Designer as co-founders means <strong>technology and brand decisions happen in the same room</strong>, aligned from day one.',
     'مهندس معماري مؤسسي ومصمم هوية بصرية كشريكين مؤسسين يعني أن <strong>قرارات التقنية والعلامة تُتخذ في الغرفة نفسها</strong>، متوائمة من اليوم الأول.'),
    ('Deep healthcare domain knowledge', 'معرفة عميقة بقطاع الرعاية الصحية',
     'CPHIMS, HIMSS EMRAM, CBAHI, NORA — <strong>active credentials, not listed frameworks</strong>. Every HC engagement is delivered with clinical workflow context built in from the first call.',
     'CPHIMS و HIMSS EMRAM و CBAHI و NORA — <strong>اعتمادات فعّالة لا أطر مُدرجة</strong>. كل مشروع صحي يُنفَّذ بسياق مسارات العمل السريرية من المكالمة الأولى.'),
    ('MENA-native delivery', 'تنفيذ بروح المنطقة',
     'Bilingual AR/EN as standard. Vision 2030 and NORA alignment built into architecture. <strong>Saudi-specific regulatory context</strong> embedded in every technology recommendation.',
     'ثنائية اللغة عربي/إنجليزي كمعيار. مواءمة رؤية 2030 و NORA مدمجة في العمارة. <strong>السياق التنظيمي السعودي</strong> متضمَّن في كل توصية تقنية.'),
    ('Milestone-based payment', 'دفعات حسب المعالم',
     'Payment is tied to deliverables, not time. <strong>Files release only on full settlement.</strong> This structure protects both sides and keeps every milestone meaningful.',
     'الدفع مرتبط بالمخرجات لا بالوقت. <strong>الملفات تُسلَّم فقط عند السداد الكامل.</strong> هذا الهيكل يحمي الطرفين ويجعل كل معلم ذا معنى.'),
]

STAGES = [
    ('01', 'Discovery & Goals', 'الاستكشاف والأهداف',
     'BMM goals mapping — vision, strategies, tactics. Nothing built without a business reason.',
     'رسم أهداف BMM — الرؤية والاستراتيجيات والتكتيكات. لا يُبنى شيء بلا سبب عمل.',
     'BMM goal map', 'خريطة أهداف BMM'),
    ('02', 'Kickoff + Brief', 'الانطلاق + الموجز',
     'Formal scope confirmation, stakeholder alignment, and engagement brief sign-off.',
     'تأكيد رسمي للنطاق ومواءمة أصحاب المصلحة واعتماد موجز المشروع.',
     'Signed engagement brief', 'موجز مشروع معتمد'),
    ('03', 'Capability Research', 'بحث القدرات',
     'Value stream mapping and capability heatmap — what\'s broken, missing, or misaligned.',
     'رسم تدفق القيمة وخريطة حرارية للقدرات — ما هو معطّل أو مفقود أو غير متوائم.',
     'Capability heatmap', 'خريطة حرارية للقدرات'),
    ('04', 'Strategy & Architecture', 'الاستراتيجية والعمارة',
     'TOGAF ADM-grounded target state design. Business-to-Technology Alignment Matrix produced.',
     'تصميم الوضع المستهدف المرتكز على TOGAF ADM. إنتاج مصفوفة مواءمة الأعمال مع التقنية.',
     'Alignment matrix', 'مصفوفة المواءمة'),
    ('05–06', 'Concept → Design & Build', 'المفهوم ← التصميم والبناء',
     'Concepts aligned to strategy, then full production — identity systems, architecture docs, or dashboards.',
     'مفاهيم متوائمة مع الاستراتيجية ثم إنتاج كامل — منظومات هوية أو وثائق معمارية أو لوحات مؤشرات.',
     'Concept + production files', 'المفهوم + ملفات الإنتاج'),
    ('07–08', 'Validation → Launch & Embed', 'التحقق ← الإطلاق والترسيخ',
     'Structured review cycle, client sign-off gate, deployment, handover documentation, and post-launch support.',
     'دورة مراجعة منظمة وبوابة اعتماد العميل والنشر ووثائق التسليم ودعم ما بعد الإطلاق.',
     'Sign-off gate + handover pack', 'بوابة الاعتماد + حزمة التسليم'),
]


def build():
    why = ''.join(f'''
          <article class="card tile" data-reveal style="--d:{(i % 3) * .07:.2f}s">
            <span class="tile__num">0{i + 1}</span>
            <h3 data-ar="{esc(ar)}">{esc(en)}</h3>
            <p data-ar-html="{esc(dar)}">{den}</p>
          </article>''' for i, (en, ar, den, dar) in enumerate(WHY))
    stages = steps3([(n, en, ar, den, dar, d_en, d_ar) for n, en, ar, den, dar, d_en, d_ar in STAGES])

    body = f'''
      <!-- ░░ Hero ░░ -->
      <section class="phero container phero--center" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('About', 'من نحن', None)])}
        <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="عن الاستوديو">About the Studio</span></span>
        <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s"><span data-ar="نبني ما تحتاجه الأعمال">We build what businesses need</span><br /><span class="grad-text" data-ar="لتنمو — بالتصميم.">to grow — by design.</span></h1>
        <p class="hero__lead" data-reveal style="--d:.16s" data-ar-html="Code &amp; Canvas استوديو بوتيكي لتطوير الأعمال أسّسه مهندس معماري مؤسسي ومصمم هوية بصرية — وكلاهما يمارس تطوير الأعمال فعليًا. نساعد المؤسسات في &lt;strong&gt;المنطقة&lt;/strong&gt; على النمو عبر مواءمة &lt;strong&gt;الهوية والتقنية والبيانات&lt;/strong&gt; مع الأهداف التجارية من خلال مشاريع ثابتة النطاق تُسلَّم على مراحل.">Code &amp; Canvas is a boutique business development studio co-founded by an Enterprise Architect and a Brand Identity Designer — both operating as active BD practitioners. We help organizations across <strong>MENA</strong> grow by aligning <strong>brand, technology, and data</strong> to commercial objectives through fixed-scope, milestone-delivered engagements.</p>
        <div class="hero__ctas hero__ctas--center" data-reveal style="--d:.24s">{btn('Book a 30-min call', 'احجز مكالمة 30 دقيقة', '/contact/#book')}{btn('Our story', 'قصتنا', '/our-story/', 'glass')}{btn('Meet the team', 'تعرّف على الفريق', '/team/', 'ghost', 'arrow')}</div>
      </section>

      <!-- ░░ Studio at a glance ░░ -->
      <section class="section container section--tight" aria-label="Studio at a glance" data-ar-label="الاستوديو في أرقام">
        {facts([('Years across both tracks', 'سنوات عبر كلا المسارين', '9+', True),
                ('Brands &amp; orgs delivered', 'علامة ومؤسسة سلّمناها', '40+', True),
                ('Sectors served', 'قطاعًا خدمناه', '12+', True),
                ('Productized services', 'خدمة مُنتجة', '23', True),
                ('Countries — KSA · Egypt', 'دولتان — السعودية · مصر', '2', True)])}
      </section>

      <!-- ░░ Position ░░ -->
      <section class="section container section--tight" id="position" aria-labelledby="pos-title">
        <div class="panel panel--deep" data-reveal>
          <p class="kicker"><span data-ar="موقفنا">Our position</span></p>
          <h2 class="statement__text" id="pos-title" style="font-size:clamp(26px,3.4vw,44px)"><span data-ar="تطوير الأعمال يُقدَّم عبر التقنية والتصميم —">Business development delivered through technology and design —</span> <span class="grad-text" data-ar="لا رغمًا عنهما.">not despite them.</span></h2>
          <p class="lead">Most studios separate brand from technology. Most consultancies separate strategy from delivery. We built Code &amp; Canvas to collapse those gaps — into a single studio, two specialist tracks, and a shared commercial discipline that makes both more effective.</p>
          <div class="pill-list" style="margin-top:22px"><span class="pill" data-ar="العمارة المؤسسية">Enterprise Architecture</span><span class="pill" data-ar="هوية العلامة">Brand Identity</span><span class="pill" data-ar="تقنية الرعاية الصحية">Healthcare IT</span><span class="pill" data-ar="التحول الرقمي">Digital Transformation</span><span class="pill" data-ar="البيانات والتحليلات">Data &amp; Analytics</span><span class="pill">TOGAF · CPHIMS · NORA</span></div>
        </div>
      </section>

      <!-- ░░ Why ░░ -->
      <section class="section container section--flush-top" id="why" aria-labelledby="why-title">
        {sec_head('01', 'WHY CODE & CANVAS', 'لماذا Code & Canvas',
                  '<span id="why-title" data-ar="لسنا استوديو عامًا.">Not a generic studio.</span> <span class="grad-text" data-ar="ولسنا شركة استشارات أيضًا.">Not a consultancy either.</span>',
                  'Six things that make our engagements structurally different — not just "we care more".',
                  'ستة أشياء تجعل مشاريعنا مختلفة بنيويًا — لا مجرد «نحن نهتم أكثر».')}
        <div class="grid grid--3">{why}
        </div>
      </section>

      <!-- ░░ Two tracks ░░ -->
      <section class="section container section--flush-top" id="tracks" aria-labelledby="tracks-title">
        {sec_head('02', 'THE TWO TRACKS', 'المساران',
                  '<span id="tracks-title" data-ar="شريك مؤسس لكل مسار.">One co-founder per track.</span> <span class="grad-text" data-ar="كلاهما موجَّه لتطوير الأعمال.">Both oriented to BD.</span>',
                  'Two specialists, not a generalist studio. Every engagement is led by the right person from day one.',
                  'متخصصان، لا استوديو عام. كل مشروع يقوده الشخص المناسب من اليوم الأول.',
                  aside=btn('Meet the team', 'تعرّف على الفريق', '/team/', 'glass'))}
        <div class="grid grid--2 grid--top">
          <article class="card tile" data-reveal><p class="kicker" data-ar="التقنية والرعاية الصحية">Technology &amp; healthcare</p><h3>Ahmed M. Bedeer</h3><p data-ar="العمارة المؤسسية والتحول والبيانات — بقيادة المؤسس التقني.">Enterprise architecture, transformation and data — led by the technical co-founder.</p>{btn('Meet Ahmed', 'تعرّف على أحمد', '/team/#ahmed', 'glass')}</article>
          <article class="card tile" data-reveal style="--d:.08s"><p class="kicker" data-ar="الهوية والتصميم">Brand &amp; design</p><h3>Mustafa Aboalazm</h3><p data-ar="استراتيجية العلامة والأنظمة البصرية — بقيادة المؤسس الإبداعي.">Brand strategy and visual systems — led by the creative co-founder.</p>{btn('Meet Mustafa', 'تعرّف على مصطفى', '/team/#mustafa', 'glass')}</article>
        </div>
      </section>

      <!-- ░░ Methodology ░░ -->
      <section class="section container section--flush-top" id="methodology" aria-labelledby="meth-title">
        {sec_head('03', 'OUR METHODOLOGY', 'منهجيتنا',
                  '<span id="meth-title" data-ar="ثماني مراحل.">Eight stages.</span> <span class="grad-text" data-ar="في كل مشروع.">Every engagement.</span>',
                  'From discovery to launch, every Code & Canvas engagement follows the same structured process — anchored in the Business Motivation Model and TOGAF ADM. Nothing is built without a business reason.',
                  'من الاستكشاف إلى الإطلاق، يتبع كل مشروع في Code & Canvas العملية المنظمة نفسها — المرتكزة على نموذج دوافع الأعمال و TOGAF ADM. لا يُبنى شيء بلا سبب عمل.',
                  aside=f'<a class="text-link" href="/methodology/"><span data-ar="المنهجية كاملة ←">Full methodology →</span>{icon("arrow")}</a>')}
        {stages}
        <div class="notice notice--violet" data-reveal style="margin-top:26px">{icon('wallet')}<p data-ar-html="&lt;strong&gt;الدفع حسب المعالم — لا حسب الوقت.&lt;/strong&gt; مشاريع الهوية: 50% عند الانطلاق · 25% عند اعتماد الاستراتيجية · 25% عند التسليم النهائي. الاستشارات: 50% عند الانطلاق · 50% عند التسليم. الملفات تُسلَّم عند السداد الكامل."><strong>Payment is milestone-based — not time-based.</strong> Brand engagements: 50% Kickoff · 25% Strategy Sign-off · 25% Final. Advisory: 50% Kickoff · 50% Final. Files release on full settlement.</p></div>
      </section>

      <!-- ░░ CTA ░░ -->
      <section class="section container section--tight" id="book" aria-labelledby="cta-title">
        <div class="callout panel" data-reveal>
          <div>
            <p class="kicker"><span data-ar="مستعد؟">READY?</span></p>
            <h3 id="cta-title" data-ar="مستعد لبناء شيء يحرّك المؤشر فعلًا؟">Ready to build something that actually moves the needle?</h3>
            <p data-ar="احجز مكالمة استكشافية مدتها 30 دقيقة. نحدد النطاق ونؤكد الملاءمة ونعطيك صورة واضحة عمّا يبدو عليه المشروع — أو نخبرك بصراحة إن لم نكن الخيار المناسب.">Book a 30-minute discovery call. We define the scope, confirm the fit, and give you a clear picture of what an engagement looks like — or tell you directly if we're not the right match.</p>
          </div>
          <div class="callout__actions">
            {btn('Book a free call', 'احجز مكالمة مجانية', '/contact/#book')}
            <a class="text-link" href="/our-story/"><span data-ar="اقرأ قصتنا ←">Read our story →</span></a>
            <a class="text-link" href="/team/"><span data-ar="تعرّف على الفريق ←">Meet the team →</span></a>
          </div>
        </div>
      </section>

'''
    return [page('/about/', title='About — Code & Canvas', title_ar='من نحن — Code & Canvas',
                 desc='Code & Canvas is a boutique business development studio co-founded by an Enterprise Architect and a Brand Identity Designer. We help organizations across MENA grow by aligning brand, technology, and data to commercial objectives.',
                 desc_ar='Code & Canvas استوديو بوتيكي لتطوير الأعمال أسّسه مهندس معماري مؤسسي ومصمم هوية بصرية. نساعد المؤسسات في المنطقة على النمو عبر مواءمة الهوية والتقنية والبيانات مع الأهداف التجارية.',
                 nav='about', body=body, ld=[PERSON_LD['ahmed'], PERSON_LD['mustafa']])]
