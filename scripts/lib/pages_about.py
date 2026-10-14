# -*- coding: utf-8 -*-
"""/about/ — live copy of codeandcanvas.net/about/."""
from h import esc, icon, crumbs, closing, btn, page

WHY = [
    ('Productized, not open-ended', 'مُنتجة، لا مفتوحة النهاية',
     'Every engagement has <strong>defined scope, fixed milestones, and a traceable business outcome</strong>. No retainers. No surprise scope creep. You know exactly what you\'re buying before signing.',
     'كل مشروع له &lt;strong&gt;نطاق محدد ومعالم ثابتة ونتيجة أعمال قابلة للتتبع&lt;/strong&gt;. لا عقود مستمرة. لا توسّع مفاجئ في النطاق. تعرف تمامًا ما تشتريه قبل التوقيع.', 'package'),
    ('BD logic in every track', 'منطق تطوير الأعمال في كل مسار',
     'Whether we\'re building a brand or an architecture, the starting point is always the same: <strong>your business goals</strong>. We use the Business Motivation Model before any design or tech decision is made.',
     'سواء كنا نبني علامة أو عمارة، نقطة البداية واحدة دائمًا: &lt;strong&gt;أهداف عملك&lt;/strong&gt;. نستخدم نموذج دوافع الأعمال (BMM) قبل أي قرار تصميمي أو تقني.', 'target'),
    ('Dual expertise — one studio', 'خبرة مزدوجة — استوديو واحد',
     'An Enterprise Architect and a Brand Identity Designer as co-founders means <strong>technology and brand decisions happen in the same room</strong>, aligned from day one.',
     'مهندس معماري مؤسسي ومصمم هوية بصرية كشريكين مؤسسين يعني أن &lt;strong&gt;قرارات التقنية والعلامة تُتخذ في الغرفة نفسها&lt;/strong&gt;، متوائمة من اليوم الأول.', 'users'),
    ('Deep healthcare domain knowledge', 'معرفة عميقة بقطاع الرعاية الصحية',
     'CPHIMS, HIMSS EMRAM, CBAHI, NORA — <strong>active credentials, not listed frameworks</strong>. Every HC engagement is delivered with clinical workflow context built in from the first call.',
     'CPHIMS و HIMSS EMRAM و CBAHI و NORA — &lt;strong&gt;اعتمادات فعّالة لا أطر مُدرجة&lt;/strong&gt;. كل مشروع صحي يُنفَّذ بسياق مسارات العمل السريرية من المكالمة الأولى.', 'stethoscope'),
    ('MENA-native delivery', 'تنفيذ بروح المنطقة',
     'Bilingual AR/EN as standard. Vision 2030 and NORA alignment built into architecture. <strong>Saudi-specific regulatory context</strong> embedded in every technology recommendation.',
     'ثنائية اللغة عربي/إنجليزي كمعيار. مواءمة رؤية 2030 و NORA مدمجة في العمارة. &lt;strong&gt;السياق التنظيمي السعودي&lt;/strong&gt; متضمَّن في كل توصية تقنية.', 'globe'),
    ('Milestone-based payment', 'دفعات حسب المعالم',
     'Payment is tied to deliverables, not time. <strong>Files release only on full settlement.</strong> This structure protects both sides and keeps every milestone meaningful.',
     'الدفع مرتبط بالمخرجات لا بالوقت. &lt;strong&gt;الملفات تُسلَّم فقط عند السداد الكامل.&lt;/strong&gt; هذا الهيكل يحمي الطرفين ويجعل كل معلم ذا معنى.', 'wallet'),
]

STAGES = [
    ('01', 'Discovery & Goals', 'الاستكشاف والأهداف', 'BMM goals mapping — vision, strategies, tactics. Nothing built without a business reason.', 'رسم أهداف BMM — الرؤية والاستراتيجيات والتكتيكات. لا يُبنى شيء بلا سبب عمل.'),
    ('02', 'Kickoff + Brief', 'الانطلاق + الموجز', 'Formal scope confirmation, stakeholder alignment, and engagement brief sign-off.', 'تأكيد رسمي للنطاق ومواءمة أصحاب المصلحة واعتماد موجز المشروع.'),
    ('03', 'Capability Research', 'بحث القدرات', 'Value stream mapping and capability heatmap — what\'s broken, missing, or misaligned.', 'رسم تدفق القيمة وخريطة حرارية للقدرات — ما هو معطّل أو مفقود أو غير متوائم.'),
    ('04', 'Strategy & Architecture', 'الاستراتيجية والعمارة', 'TOGAF ADM-grounded target state design. Business-to-Technology Alignment Matrix produced.', 'تصميم الوضع المستهدف المرتكز على TOGAF ADM. إنتاج مصفوفة مواءمة الأعمال مع التقنية.'),
    ('05–06', 'Concept → Design & Build', 'المفهوم ← التصميم والبناء', 'Concepts aligned to strategy, then full production — identity systems, architecture docs, or dashboards.', 'مفاهيم متوائمة مع الاستراتيجية ثم إنتاج كامل — منظومات هوية أو وثائق معمارية أو لوحات مؤشرات.'),
    ('07–08', 'Validation → Launch & Embed', 'التحقق ← الإطلاق والترسيخ', 'Structured review cycle, client sign-off gate, deployment, handover documentation, and post-launch support.', 'دورة مراجعة منظمة وبوابة اعتماد العميل والنشر ووثائق التسليم ودعم ما بعد الإطلاق.'),
]


def build():
    why = ''.join(f'''
          <article class="card glass tile" data-tilt data-reveal style="--d:{(i % 3) * .07:.2f}s">
            <span class="tile__num">0{i + 1}</span>
            <h3 data-ar="{esc(ar)}">{esc(en)}</h3>
            <p data-ar-html="{esc(dar)}">{den}</p>
          </article>''' for i, (en, ar, den, dar, ic) in enumerate(WHY))
    stages = ''.join(f'''
          <article class="card glass tile" data-tilt data-reveal style="--d:{(i % 3) * .07:.2f}s">
            <span class="tile__num">{n}</span>
            <h3 data-ar="{esc(ar)}">{esc(en)}</h3>
            <p data-ar="{esc(dar)}">{esc(den)}</p>
          </article>''' for i, (n, en, ar, den, dar) in enumerate(STAGES))

    body = f'''
      <!-- ░░ Hero ░░ -->
      <section class="phero container phero--center" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('About', 'من نحن', None)])}
        <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="عن الاستوديو">About the Studio</span></span>
        <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s"><span data-ar="نبني ما تحتاجه الأعمال">We build what businesses need</span><br /><span class="grad-text" data-ar="لتنمو — بالتصميم.">to grow — by design.</span></h1>
        <p class="hero__lead" data-reveal style="--d:.16s" data-ar-html="Code &amp; Canvas استوديو بوتيكي لتطوير الأعمال أسّسه مهندس معماري مؤسسي ومصمم هوية بصرية — وكلاهما يمارس تطوير الأعمال فعليًا. نساعد المؤسسات في &lt;strong&gt;المنطقة&lt;/strong&gt; على النمو عبر مواءمة &lt;strong&gt;الهوية والتقنية والبيانات&lt;/strong&gt; مع الأهداف التجارية من خلال مشاريع ثابتة النطاق تُسلَّم على مراحل.">Code &amp; Canvas is a boutique business development studio co-founded by an Enterprise Architect and a Brand Identity Designer — both operating as active BD practitioners. We help organizations across <strong>MENA</strong> grow by aligning <strong>brand, technology, and data</strong> to commercial objectives through fixed-scope, milestone-delivered engagements.</p>
        <div class="hero__ctas hero__ctas--center" data-reveal style="--d:.24s">{btn('Book a Discovery Call', 'احجز مكالمة استكشافية', '/contact/#book')}{btn('Our Story', 'قصتنا', '/our-story/', 'glass')}{btn('Meet the Team', 'تعرّف على الفريق', '/team/', 'ghost', 'arrow')}</div>
      </section>

      <!-- ░░ Stats ░░ -->
      <section class="stats container" aria-label="Studio at a glance" data-ar-label="الاستوديو في أرقام">
        <div class="stats__inner glass" data-reveal style="grid-template-columns:repeat(5,1fr)">
          <div class="stat"><span class="stat__num stat__num--ltr"><span data-count="9" data-latin="1">9</span>+</span><p class="stat__label" data-ar-html="سنوات عبر&lt;br /&gt;كلا المسارين">Years across<br />both tracks</p></div>
          <div class="stat"><span class="stat__num stat__num--ltr"><span data-count="40" data-latin="1">40</span>+</span><p class="stat__label" data-ar-html="علامة ومؤسسة&lt;br /&gt;سلّمناها">Brands &amp; orgs<br />delivered</p></div>
          <div class="stat"><span class="stat__num stat__num--ltr"><span data-count="12" data-latin="1">12</span>+</span><p class="stat__label" data-ar-html="قطاعًا&lt;br /&gt;خدمناه">Sectors<br />served</p></div>
          <div class="stat"><span class="stat__num stat__num--ltr"><span data-count="23" data-latin="1">23</span></span><p class="stat__label" data-ar-html="خدمة&lt;br /&gt;مُنتجة">Productized<br />services</p></div>
          <div class="stat"><span class="stat__num stat__num--ltr"><span data-count="2" data-latin="1">2</span></span><p class="stat__label" data-ar-html="دولتان&lt;br /&gt;السعودية · مصر">Countries<br />KSA · Egypt</p></div>
        </div>
      </section>

      <!-- ░░ At a glance ░░ -->
      <section class="section container section--tight" aria-labelledby="glance-title">
        <div class="callout glass glass--deep" data-reveal>
          <div>
            <p class="kicker"><span data-ar="الاستوديو · لمحة سريعة">Studio · At a Glance</span></p>
            <h3 id="glance-title"><span data-ar="تخصص واحد. مساران.">One discipline. Two tracks.</span> <span class="grad-text" data-ar="صفر عقود مفتوحة.">Zero open-ended retainers.</span></h3>
            <p data-ar="كل مشروع — هوية أو تقنية أو متكامل — مرتكز على منطق تطوير الأعمال. نحن لا نسلّم مخرجات. نسلّم مواءمة بين أهدافك وقدراتك وأصولك.">Every engagement — brand, technology, or combined — is anchored in Business Development logic. We don't deliver outputs. We deliver alignment between your goals, capabilities, and assets.</p>
          </div>
          <ul class="ticks">
            <li data-ar-html="&lt;strong&gt;المسار التقني&lt;/strong&gt; — العمارة المؤسسية، تقنية الرعاية الصحية، السحابة، البيانات"><strong>Technology Track</strong> — EA, Healthcare IT, Cloud, Data</li>
            <li data-ar-html="&lt;strong&gt;المسار الإبداعي&lt;/strong&gt; — هوية العلامة، أنظمة التصميم، الإطلاق الرقمي"><strong>Creative Track</strong> — Brand Identity, Design Systems, Digital Launch</li>
            <li data-ar-html="&lt;strong&gt;مشاريع متكاملة&lt;/strong&gt; — الإطلاق الرقمي للعيادات، ذكاء الأعمال الصحي"><strong>Combined Engagements</strong> — Clinic Digital Launch, Healthcare BI</li>
            <li data-ar-html="&lt;strong&gt;نخدم&lt;/strong&gt; — السعودية · مصر · القطاعين الخاص والعام في المنطقة"><strong>Serving</strong> — KSA · Egypt · MENA private &amp; public sector</li>
          </ul>
        </div>
      </section>

      <!-- ░░ Why ░░ -->
      <section class="section container section--flush-top" id="why" aria-labelledby="why-title">
        <header class="section__head" data-reveal>
          <p class="kicker"><span class="kicker__num">01</span><span data-ar="لماذا Code &amp; Canvas">Why Code &amp; Canvas</span></p>
          <h2 class="section__title" id="why-title"><span data-ar="لسنا استوديو عامًا.">Not a generic studio.</span><br /><span class="grad-text" data-ar="ولسنا شركة استشارات أيضًا.">Not a consultancy either.</span></h2>
          <p class="section__lead" data-ar="ستة أشياء تجعل مشاريعنا مختلفة بنيويًا — لا مجرد «نحن نهتم أكثر».">Six things that make our engagements structurally different — not just "we care more."</p>
        </header>
        <div class="grid grid--3">{why}
        </div>
      </section>

      <!-- ░░ Two tracks ░░ -->
      <section class="section container section--flush-top" id="tracks" aria-labelledby="tracks-title">
        <header class="section__head" data-reveal>
          <p class="kicker"><span class="kicker__num">02</span><span data-ar="المساران">The Two Tracks</span></p>
          <h2 class="section__title" id="tracks-title"><span data-ar="شريك مؤسس لكل مسار.">One co-founder per track.</span><br /><span class="grad-text" data-ar="كلاهما موجَّه لتطوير الأعمال.">Both oriented to BD.</span></h2>
          <p class="section__lead" data-ar="متخصصان، لا استوديو عام. كل مشروع يقوده الشخص المناسب من اليوم الأول.">Two specialists, not a generalist studio. Every engagement is led by the right person from day one.</p>
        </header>
        <div class="grid grid--2">
          <article class="card glass person" data-reveal>
            <div class="art art--square" data-slot="team/ahmed-bedeer"><span class="art__mark">AB</span><span class="art__cap" data-ar="{{ }} الكود">{{ }} THE CODE</span></div>
            <div>
              <p class="person__role" data-ar="المسار التقني · شريك مؤسس">Technology Track · Co-Founder</p>
              <h3>Ahmed M. Bedeer</h3>
              <p class="person__tag" data-ar="مهندس معماري مؤسسي ومتخصص في التحول الرقمي · الخبر، السعودية">Enterprise Architect &amp; Digital Transformation Specialist · Al Khobar, KSA</p>
              <div class="creds"><span>TOGAF</span><span>CPHIMS</span><span>HIMSS EMRAM</span><span>NORA</span><span>CBAHI</span><span>ArchiMate 3.1</span></div>
              <p style="margin-top:14px" data-ar-html="أكثر من 7 سنوات عبر قطاعات الرعاية الصحية والحكومة والقطاع الخاص في السعودية. خبرة في &lt;strong&gt;عمارة TOGAF/NORA واختيار موردي أنظمة HIS والهجرة السحابية وتحليلات البيانات&lt;/strong&gt; بما يتماشى مع رؤية 2030. مقيّم HIMSS EMRAM نشط — سياق مسارات العمل السريرية متضمَّن في كل توصية تقنية.">7+ years across healthcare, government, and private sector in KSA. Expertise in <strong>TOGAF/NORA architecture, HIS vendor selection, cloud migration, and data analytics</strong> aligned to Vision 2030. Active HIMSS EMRAM assessor — clinical workflow context embedded in every technology recommendation.</p>
              <h4 class="person__role" style="margin-top:18px" data-ar="الخدمات التي يقودها">Services led</h4>
              <ul class="ticks ticks--dense">
                <li><a href="/technology-services/#ab-01">AB-01 · <span data-ar="تقييم البداية السريعة للعمارة المؤسسية">EA Quick-Start Assessment</span></a></li>
                <li><a href="/technology-services/#ab-02">AB-02 · <span data-ar="استشارات التحول الرقمي">Digital Transformation Advisory</span></a></li>
                <li><a href="/technology-services/#ab-05">AB-05 · <span data-ar="استراتيجية الهجرة السحابية">Cloud Migration Strategy</span></a></li>
                <li><a href="/technology-services/#ab-03">AB-03 · <span data-ar="لوحة التحليلات">Analytics Dashboard</span></a></li>
                <li><a href="/technology-services/#ab-04">AB-04 · <span data-ar="استكشاف محفظة التطبيقات">Application Portfolio Discovery</span></a></li>
                <li><a href="/healthcare/#hc-03">HC-03 · <span data-ar="استشارات اختيار HIS">HIS Selection Advisory</span></a> · <a href="/healthcare/#hc-05">HC-05 · <span data-ar="العمارة الصحية + EMRAM">Healthcare EA + EMRAM</span></a></li>
              </ul>
              <div class="person__links"><a href="https://ahmed-bedeer.vercel.app/" target="_blank" rel="noopener">{icon('link')}<span data-ar="عرض الأعمال ↗">View Portfolio ↗</span></a></div>
            </div>
          </article>
          <article class="card glass person" data-reveal style="--d:.08s">
            <div class="art art--square art--pink" data-slot="team/mustafa-aboalazm"><span class="art__mark">MA</span><span class="art__cap" data-ar="✦ الكانفاس">✦ THE CANVAS</span></div>
            <div>
              <p class="person__role" data-ar="المسار الإبداعي · شريك مؤسس">Creative Track · Co-Founder</p>
              <h3>Mustafa Aboalazm</h3>
              <p class="person__tag" data-ar="مصمم هوية بصرية أول ومستشار تطوير أعمال · العبور، مصر">Senior Brand Identity Designer &amp; Business Development Consultant · Al Obour, Egypt</p>
              <div class="creds"><span data-ar="استراتيجية العلامة">Brand Strategy</span><span data-ar="+9 سنوات">9+ Years</span><span data-ar="+20 علامة">20+ Brands</span><span>Adobe Suite</span><span>Figma</span></div>
              <p style="margin-top:14px" data-ar-html="أكثر من 9 سنوات، أكثر من 20 علامة، 6 قطاعات. مدير إعلام سابق في Nile Pharma Food (5 سنوات) — بنى هوية العلامة من الصفر وأطلق المنصة الرقمية وقاد إعادة بناء كاملة لهوية الشركة أسفرت عن &lt;strong&gt;+40% في الظهور الرقمي و+25% في التفاعل مع العلامة&lt;/strong&gt;. يمارس تطوير الأعمال فعليًا عبر القطاعات غير الربحية والحكومية والتعليمية والخاصة في مصر والسعودية.">9+ years, 20+ brands, 6 sectors. Former Media Director at Nile Pharma Food (5 years) — built brand identity from zero, launched the digital platform, and led a full corporate rebrand resulting in <strong>+40% online visibility and +25% brand engagement</strong>. Active BD practitioner across NGO, government, education, and private sector in Egypt and KSA.</p>
              <h4 class="person__role" style="margin-top:18px" data-ar="الخدمات التي يقودها">Services led</h4>
              <ul class="ticks ticks--dense">
                <li><a href="/creative-services/#ma-03">MA-03 · <span data-ar="منظومة هوية العلامة (منهجية V2 من 8 مراحل)">Brand Identity System (8-stage V2)</span></a></li>
                <li><a href="/creative-services/#ma-02">MA-02 · <span data-ar="تدقيق وتجديد العلامة">Brand Audit + Refresh</span></a></li>
                <li><a href="/services/#cc-01">CC-01 · <span data-ar="باقة الإطلاق الرقمي">Digital Launch Package</span></a></li>
                <li><a href="/services/#cc-02">CC-02 · <span data-ar="استشارات تطوير الأعمال">Business Development Advisory</span></a></li>
                <li><a href="/healthcare/#hc-01">HC-01 · <span data-ar="الإطلاق الرقمي للعيادات">Clinic Digital Launch</span></a> · <a href="/healthcare/#hc-04">HC-04 · <span data-ar="هوية العيادة">Clinic Brand Identity</span></a></li>
              </ul>
              <div class="person__links"><a href="https://aboalazm-os.vercel.app/" target="_blank" rel="noopener">{icon('link')}<span data-ar="عرض الأعمال ↗">View Portfolio ↗</span></a></div>
            </div>
          </article>
        </div>
      </section>

      <!-- ░░ Methodology ░░ -->
      <section class="section container section--flush-top" id="methodology" aria-labelledby="meth-title">
        <div class="head-split">
          <header class="section__head" data-reveal>
            <p class="kicker"><span class="kicker__num">03</span><span data-ar="منهجيتنا">Our Methodology</span></p>
            <h2 class="section__title" id="meth-title"><span data-ar="8 مراحل.">8 stages.</span> <span class="grad-text" data-ar="في كل مشروع.">Every engagement.</span></h2>
            <p class="section__lead" data-ar="من الاستكشاف إلى الإطلاق، يتبع كل مشروع في Code &amp; Canvas العملية المنظمة نفسها — المرتكزة على نموذج دوافع الأعمال و TOGAF ADM. لا يُبنى شيء بلا سبب عمل.">From discovery to launch, every Code &amp; Canvas engagement follows the same structured process — anchored in the Business Motivation Model and TOGAF ADM. Nothing is built without a business reason.</p>
          </header>
          <div class="head-aside" data-reveal style="--d:.15s">
            <div class="notice notice--violet">{icon('wallet')}<p data-ar-html="&lt;strong&gt;الدفع حسب المعالم — لا حسب الوقت.&lt;/strong&gt; مشاريع الهوية: 50% عند الانطلاق · 25% عند اعتماد الاستراتيجية · 25% عند التسليم النهائي. الاستشارات: 50% عند الانطلاق · 50% عند التسليم. الملفات تُسلَّم عند السداد الكامل."><strong>Payment is milestone-based — not time-based.</strong> Brand engagements: 50% Kickoff · 25% Strategy Sign-off · 25% Final. Advisory: 50% Kickoff · 50% Final. Files release on full settlement.</p></div>
            <p style="margin-top:14px"><a class="text-link" href="/methodology/"><span data-ar="المنهجية كاملة ←">Full methodology →</span></a> &nbsp; <a class="text-link" href="/services/"><span data-ar="كل الخدمات ←">View All Services →</span></a></p>
          </div>
        </div>
        <div class="grid grid--3">{stages}
        </div>
      </section>

      <!-- ░░ Position ░░ -->
      <section class="section container section--flush-top" aria-labelledby="pos-title">
        <div class="statement glass glass--deep" style="border-radius:var(--r-lg);padding-inline:clamp(20px,5vw,70px)" data-reveal>
          <p class="kicker kicker--center"><span data-ar="موقفنا">Our Position</span></p>
          <h2 class="statement__text" id="pos-title" style="font-size:clamp(28px,4.4vw,60px)"><span data-ar="تطوير الأعمال يُقدَّم عبر التقنية والتصميم —">Business development delivered through technology and design —</span> <span class="grad-text" data-ar="لا رغمًا عنهما.">not despite them.</span></h2>
          <p class="section__lead" style="margin-inline:auto;margin-top:22px" data-ar="معظم الاستوديوهات تفصل العلامة عن التقنية. ومعظم شركات الاستشارات تفصل الاستراتيجية عن التنفيذ. بنينا Code &amp; Canvas لنطوي هذه الفجوات — في استوديو واحد ومسارين متخصصين وانضباط تجاري مشترك يجعل كليهما أكثر فاعلية.">Most studios separate brand from technology. Most consultancies separate strategy from delivery. We built Code &amp; Canvas to collapse those gaps — into a single studio, two specialist tracks, and a shared commercial discipline that makes both more effective.</p>
          <div class="pill-list" style="justify-content:center;margin-top:26px"><span class="pill" data-ar="العمارة المؤسسية">Enterprise Architecture</span><span class="pill" data-ar="هوية العلامة">Brand Identity</span><span class="pill" data-ar="تقنية الرعاية الصحية">Healthcare IT</span><span class="pill" data-ar="التحول الرقمي">Digital Transformation</span><span class="pill" data-ar="البيانات والتحليلات">Data &amp; Analytics</span><span class="pill" data-ar="MENA · السعودية · مصر">MENA · KSA · Egypt</span><span class="pill" data-ar="متوافق مع رؤية 2030">Vision 2030 Aligned</span><span class="pill">TOGAF · CPHIMS · NORA</span></div>
        </div>
      </section>

      <!-- ░░ CTA ░░ -->
      <section class="section container section--tight" id="book" aria-labelledby="cta-title">
        <div class="callout glass glass--deep" data-reveal>
          <div>
            <p class="kicker"><span data-ar="مستعد؟">READY?</span></p>
            <h3 id="cta-title" data-ar="مستعد لبناء شيء يحرّك المؤشر فعلًا؟">Ready to build something that actually moves the needle?</h3>
            <p data-ar="احجز مكالمة استكشافية مدتها 30 دقيقة. نحدد النطاق ونؤكد الملاءمة ونعطيك صورة واضحة عمّا يبدو عليه المشروع — أو نخبرك بصراحة إن لم نكن الخيار المناسب.">Book a 30-minute discovery call. We define the scope, confirm the fit, and give you a clear picture of what an engagement looks like — or tell you directly if we're not the right match.</p>
          </div>
          <div class="callout__actions">
            {btn('Book a Free Call', 'احجز مكالمة مجانية', '/contact/#book')}
            <a class="text-link" href="/our-story/"><span data-ar="اقرأ قصتنا ←">Read Our Story →</span></a>
            <a class="text-link" href="/team/"><span data-ar="تعرّف على الفريق ←">Meet the Team →</span></a>
          </div>
        </div>
      </section>

      {closing('THE HOME OF INNOVATION', 'موطن الابتكار',
               '<span data-ar="أطلق إمكانات التقنية">Unlock the Potential of IT</span><br /><span class="grad-text" data-ar="لتبسيط العمليات وزيادة الإنتاجية.">to Streamline Operations and Boost Productivity.</span>',
               'Start with our story, or book an appointment and bring the business problem — we’ll bring the structure.',
               'ابدأ بقصتنا، أو احجز موعدًا وأحضر مشكلة العمل — ونحن نُحضر الهيكل.',
               [btn('Get Started', 'ابدأ الآن', '/our-story/'), btn('Book an Appointment', 'احجز موعدًا', '/contact/#book', 'glass')])}
'''
    return [page('/about/', title='About — Code & Canvas', title_ar='من نحن — Code & Canvas',
                 desc='Code & Canvas is a boutique business development studio co-founded by an Enterprise Architect and a Brand Identity Designer. We help organizations across MENA grow by aligning brand, technology, and data to commercial objectives.',
                 desc_ar='Code & Canvas استوديو بوتيكي لتطوير الأعمال أسّسه مهندس معماري مؤسسي ومصمم هوية بصرية. نساعد المؤسسات في المنطقة على النمو عبر مواءمة الهوية والتقنية والبيانات مع الأهداف التجارية.',
                 nav='about', body=body)]
