# -*- coding: utf-8 -*-
"""/creative-services/ — Creative track.

v3 architecture: the ten services as decision rows, the four-act method (owned
here rather than duplicated from /methodology/), an explicit statement of what
creative proof exists today and what does not, retainers, and who delivers.
"""
from catalog import SERVICES
from h import (esc, t, th, icon, crumbs, closing, btn, page, service_ld, PERSON_LD,
               sec_head, svc_rows, steps3, facts)

MA = [c for c in SERVICES if c.startswith('MA-')]
SPRINTS = ['MA-01', 'MA-02', 'MA-03', 'MA-04']
PRODUCTION = ['MA-05', 'MA-06', 'MA-07', 'MA-08']
RETAINERS = ['MA-09', 'MA-10']

PROOF = [
    ('Concept directions', 'اتجاهات مفاهيمية',
     'Three strategic directions per identity project, each justified against the positioning rather than presented as taste.',
     'ثلاثة اتجاهات استراتيجية لكل مشروع هوية، كلٌّ منها مبرَّر مقابل التموضع لا معروضًا كذوق شخصي.'),
    ('Bilingual craft', 'صناعة ثنائية اللغة',
     'Arabic lockups and RTL layouts are designed as the primary case, not adapted from an English master at the end.',
     'التركيبات العربية وتخطيطات RTL تُصمَّم كالحالة الأساسية، لا تُكيَّف من نسخة إنجليزية في النهاية.'),
    ('System handover', 'تسليم كنظام',
     'Guidelines, tokens and source files your team can run without us — with the naming and structure documented.',
     'أدلة معايير ورموز وملفات مصدرية يستطيع فريقك إدارتها دوننا — مع توثيق التسمية والبنية.'),
]

METHOD = [
    ('01', 'Diagnose', 'التشخيص',
     'Brand audit, competitor teardown and the business outcome the identity has to support. Nothing visual happens before this is written down.',
     'تدقيق العلامة وتحليل المنافسين ونتيجة العمل التي يجب أن تدعمها الهوية. لا شيء بصري يحدث قبل أن يُكتب هذا.',
     'Positioning one-pager', 'صفحة تموضع واحدة'),
    ('02', 'Direct', 'التوجيه',
     'Two or three strategic directions with the trade-offs named. You choose a direction — not a colour you happened to like in a mockup.',
     'اتجاهان أو ثلاثة اتجاهات استراتيجية مع تسمية المفاضلات. تختار اتجاهًا — لا لونًا أعجبك في نموذج.',
     'Direction rationale', 'مبررات الاتجاه'),
    ('03', 'Design', 'التصميم',
     'The chosen direction is built into a full system: mark, type, colour, layout, applications and the Arabic case alongside the English.',
     'الاتجاه المختار يُبنى إلى منظومة كاملة: الشعار والخط والألوان والتخطيط والتطبيقات، والحالة العربية بجانب الإنجليزية.',
     'Full identity system', 'منظومة هوية كاملة'),
    ('04', 'Deploy', 'الإطلاق',
     'Guidelines, templates and files organised so the brand survives the first hundred assets your team produces without us.',
     'أدلة وقوالب وملفات منظمة لتصمد العلامة أمام أول مئة مادة ينتجها فريقك بدوننا.',
     'Guidelines + source files', 'دليل + ملفات مصدرية'),
]


def build():
    proof = ''.join(f'''
          <article class="panel mini" data-reveal style="--d:{i * .05:.2f}s">
            <h3 data-ar="{esc(h_ar)}">{h_en}</h3>
            <p data-ar="{esc(p_ar)}">{p_en}</p>
          </article>''' for i, (h_en, h_ar, p_en, p_ar) in enumerate(PROOF))

    body = f'''
      <!-- ░░ Hero ░░ -->
      <section class="phero container phero--left" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('Solutions', 'الحلول', '/services/'), ('Creative Services', 'الخدمات الإبداعية', None)])}
        <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="هوية · أنظمة تصميم · ويب · مطبوعات وإنتاج">Identity · Design systems · Web · Print &amp; production</span></span>
        <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s"><span data-ar="هوية تُدار">Identity you can run</span><br /><span class="grad-text" data-ar="كنظام، لا كملف شعار.">as a system, not a logo file.</span></h1>
        <p class="hero__lead" data-reveal style="--d:.16s" data-ar-html="عشر خدمات إبداعية — من سبرنت شعار بـ ⁦$170⁩ إلى منظومة علامة كاملة ومنصات مخصّصة واشتراكات شهرية. &lt;strong&gt;كلها ثنائية اللغة عربي/إنجليزي كأساس، لا كإضافة.&lt;/strong&gt;">Ten creative services — from a $170 logo sprint to a full brand system, custom platforms and monthly retainers. <strong>All of them bilingual Arabic/English as standard, not as an add-on.</strong></p>
        <div class="hero__ctas" data-reveal style="--d:.24s">
          {btn('Book a 30-min call', 'احجز مكالمة 30 دقيقة', '/contact/#book')}
          {btn('Founder portfolio', 'أعمال المؤسس', 'https://aboalazm-os.vercel.app/', 'glass')}
        </div>
        {facts([('Services', 'خدمات', '10', True), ('Years of practice', 'سنوات ممارسة', '9+ years', True),
                ('Languages', 'اللغات', 'AR + EN', True), ('Starting at', 'تبدأ من', '$170', True)])}
      </section>

      <!-- ░░ 01 · The method ░░ -->
      <section class="section container" id="method" aria-labelledby="method-title">
        {sec_head('01', 'THE METHOD', 'المنهجية', '<span id="method-title" data-ar="أربعة فصول.">Four acts.</span> <span class="grad-text" data-ar="التموضع أولًا.">Positioning first.</span>',
                  'The creative work runs on a stated method — the same four acts on a $170 sprint and a $2,975+ system. Scope changes, the method does not.',
                  'العمل الإبداعي يجري وفق منهجية معلنة — الفصول الأربعة نفسها في سبرنت ⁦$170⁩ ومنظومة ⁦$2,975+⁩. النطاق يتغير والمنهجية لا.')}
        {steps3(METHOD)}
      </section>

      <!-- ░░ 02 · Identity services ░░ -->
      <section class="section container" id="identity" aria-labelledby="id-title">
        {sec_head('02', 'IDENTITY', 'الهوية', '<span id="id-title" data-ar="من سبرنت إلى منظومة.">From a sprint to a full system.</span>',
                  'Start where the business needs to start. Most brands begin with Essentials (MA-02) and grow into the full system (MA-03) — we will say which one your situation needs.',
                  'ابدأ من حيث يحتاج العمل أن يبدأ. معظم العلامات تبدأ من الأساسيات (MA-02) وتنمو إلى المنظومة الكاملة (MA-03) — ونقول لك أيهما يناسب حالتك.', aside=f'<a class="text-link" href="/pricing-faq/" data-track="navigation" data-track-to="pricing"><span data-ar="الأسعار وشروط الدفع">Prices &amp; payment terms</span>{icon("arrowUpRight", "flip")}</a>')}
        {svc_rows(SPRINTS)}
      </section>

      <!-- ░░ 03 · Web and production ░░ -->
      <section class="section container section--flush-top" id="production" aria-labelledby="prod-title">
        {sec_head('03', 'WEB &amp; PRODUCTION', 'الويب والإنتاج', '<span id="prod-title" data-ar="حيث تظهر الهوية">Where the identity</span> <span class="grad-text" data-ar="على أرض الواقع.">meets the real world.</span>',
                  'Sites, print and production — the places where an identity either survives contact with reality or quietly falls apart.',
                  'المواقع والمطبوعات والإنتاج — حيث تنجو الهوية من الاحتكاك بالواقع أو تنهار بهدوء.')}
        {svc_rows(PRODUCTION, alt_every=2)}
      </section>

      <!-- ░░ 04 · Retainers ░░ -->
      <section class="section container section--flush-top" id="retainers" aria-labelledby="ret-title">
        {sec_head('04', 'RETAINERS', 'الاشتراكات', '<span id="ret-title" data-ar="للعلامات التي تنشر كل أسبوع.">For brands that publish every week.</span>',
                  'One designer inside your system, on a month-to-month queue with a minimum of three months. Predictable volume, no per-asset quoting.',
                  'مصمّم داخل نظامك، على قائمة شهرية متجددة مع حد أدنى ثلاثة أشهر. حجم متوقع وبلا تسعير لكل مادة.')}
        {svc_rows(RETAINERS)}
        <p class="note-quiet" style="margin-top:16px" data-ar="الاشتراكات شهرية بحد أدنى ثلاثة أشهر. الحجم المتفق عليه في العقد لا يُنقل بين الشهور، وأي عمل خارج النطاق يُسعَّر مسبقًا.">Retainers are monthly with a three-month minimum. Agreed volume does not roll over between months, and anything out of scope is quoted first.</p>
      </section>

      <!-- ░░ 05 · What proof looks like ░░ -->
      <section class="section section--band" id="proof" aria-labelledby="proof-title">
        <div class="container">
          {sec_head('05', 'PROOF — INCLUDING WHAT IS MISSING', 'الإثبات — وما ينقصه', '<span id="proof-title" data-ar="ما نستطيع إثباته">What we can show</span> <span class="grad-text" data-ar="وما لا نستطيع بعد.">and what we cannot show yet.</span>',
                    'Most creative suppliers show a logo wall. We would rather tell you exactly what is available today — and what is still waiting on client permissions.',
                    'معظم الموردين يعرضون جدارًا من الشعارات. نفضّل أن نقول لك بالضبط ما المتوفر اليوم — وما ينتظر موافقات العملاء.')}
          <div class="grid-3">{proof}
          </div>
          <div class="callout panel" data-reveal style="margin-top:22px">
            <div>
              <p class="sec-head__no" style="border:0;padding:0;margin:0 0 10px"><b>!</b><span data-ar="ما لا تجده هنا">WHAT YOU WON'T FIND HERE</span></p>
              <h3 data-ar="لا جدار شعارات، ولا أعمال عميل لم يُعتمد نشرها.">No logo wall, and no client work published without permission.</h3>
              <p data-ar-html="كثير من مشاريعنا تحت اتفاقيات سرية أو تنتظر موافقة كتابية على النشر. ما هو متاح بالفعل هو &lt;a href=&quot;https://aboalazm-os.vercel.app/&quot; target=&quot;_blank&quot; rel=&quot;noopener&quot;&gt;ملف أعمال المؤسس&lt;/a&gt; وحالات النظام في &lt;a href=&quot;/case-studies/&quot;&gt;دراسات الحالة&lt;/a&gt; — وكلها معلّمة بما هي عليه: نطاق ومنهج، لا ادعاء نتيجة.">Many of our projects are under NDA or await written permission to publish. What is genuinely available is the <a href="https://aboalazm-os.vercel.app/" target="_blank" rel="noopener">founder’s portfolio</a> and the product work in <a href="/case-studies/">case studies</a> — each labelled for exactly what it is: scope and method, not a claimed outcome.</p>
            </div>
            <div class="callout__actions">
              {btn('See the founder portfolio ↗', 'شاهد أعمال المؤسس ↗', 'https://aboalazm-os.vercel.app/', 'glass')}
              {btn('Discuss a similar brief', 'ناقش موجزًا مشابهًا', '/contact/?inquiry=MA-03#message')}
            </div>
          </div>
        </div>
      </section>

      <!-- ░░ 06 · Who delivers ░░ -->
      <section class="section container" id="who" aria-labelledby="bio-title">
        {sec_head('06', 'WHO DELIVERS', 'من ينفّذ', '<span id="bio-title" data-ar="المؤسس يصمّم —">The founder designs —</span> <span class="grad-text" data-ar="لا وكالة وسيطة.">not an agency middle layer.</span>', None, None)}
        <article class="panel person" data-reveal>
          <div class="art art--portrait" data-slot="team/mustafa-aboalazm"><span class="art__mark">MA</span><span class="art__cap" data-ar="✦ الكانفاس">✦ THE CANVAS</span></div>
          <div>
            <p class="person__role" data-ar="مدير إبداعي · مهندس هوية بصرية">Creative Director · Visual Brand Architect</p>
            <h3>Mustafa Aboalazm</h3>
            <p class="person__tag" data-ar="شريك مؤسس · Code &amp; Canvas · العبور، مصر">Co-Founder · Code &amp; Canvas · Al Obour, Egypt</p>
            <p data-ar="مدير إبداعي بخبرة تتجاوز 9 سنوات في أنظمة العلامة والهوية البصرية والمواد المطبوعة والرقمية — مع أكثر من 20 علامة صاغها. يقود التصميم بنفسه من الاستراتيجية إلى الملف النهائي، وبالعربية والإنجليزية كأساس.">Creative director with 9+ years across brand systems, visual identity and print/digital production — with 20+ brands shaped. He leads the design himself from strategy to final file, working in Arabic and English as standard.</p>
            <div class="creds" aria-label="Toolkit" data-ar-label="الأدوات"><span data-ar="استراتيجية العلامة">Brand strategy</span><span data-ar="أنظمة بصرية">Visual systems</span><span>Figma</span><span data-ar="الإخراج الفني">Art direction</span><span data-ar="طباعة وتغليف">Print &amp; packaging</span><span>AR + EN</span></div>
            <div class="person__links">
              <a href="https://aboalazm-os.vercel.app/" target="_blank" rel="noopener" title="Mustafa's portfolio">{icon('link')}<span data-ar="الأعمال ↗">Portfolio ↗</span></a>
              <a href="https://behance.net/aboalazm" target="_blank" rel="noopener">{icon('pen')}<span>Behance ↗</span></a>
              <a href="/team/#mustafa">{icon('users')}<span data-ar="ملفه في صفحة الفريق">Team profile</span></a>
            </div>
          </div>
        </article>
      </section>

      {closing('START A CREATIVE ENGAGEMENT', 'ابدأ مشروعًا إبداعيًا',
               '<span data-ar="علامة تصلح">A brand built to</span> <span class="grad-text" data-ar="للنمو، لا للعرض.">grow, not just to present.</span>',
               'Tell us what the business is trying to become — we will say whether that needs a sprint, a full system, or nothing visual at all yet.',
               'أخبرنا بما يريد العمل أن يصبح — وسنقول إن كان ذلك يحتاج سبرنت أو منظومة كاملة أو لا شيء بصريًا بعد.',
               [btn('Book a 30-min call', 'احجز مكالمة 30 دقيقة', '/contact/#book'), btn('All 23 services', 'كل الخدمات الـ23', '/services/', 'glass')])}
'''
    return [page('/creative-services/', title='Creative Services — Brand systems, web and production · Code & Canvas',
                 title_ar='الخدمات الإبداعية — أنظمة العلامة والويب والإنتاج · Code & Canvas',
                 desc='Ten creative services led by Mustafa Aboalazm: logo sprints, brand identity, full brand systems, design systems, web, print, production and monthly retainers — bilingual AR/EN with scope, deliverables and price ranges.',
                 desc_ar='عشر خدمات إبداعية بقيادة مصطفى أبو العزم: سبرنت الشعار وأساسيات الهوية ومنظومة العلامة الكاملة وأنظمة التصميم والمواقع والمطبوعات والإنتاج والاشتراكات الشهرية — ثنائية اللغة بالنطاق والمخرجات والنطاقات السعرية.',
                 nav='services', body=body,
                 ld=[service_ld(MA, 'https://codeandcanvas.net/creative-services/'), PERSON_LD['mustafa']])]
