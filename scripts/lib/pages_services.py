# -*- coding: utf-8 -*-
"""/services/ — Solutions hub (live copy of codeandcanvas.net/services/ + the
healthcare and combined tracks that the home/footer already link to)."""
from catalog import SERVICES, href
from h import esc, t, th, icon, svc_grid, crumbs, closing, btn, page


def person_card(kind):
    if kind == 'ahmed':
        return f'''
        <article class="card glass person" data-reveal>
          <div class="art art--square" data-slot="team/ahmed-bedeer"><span class="art__mark">AB</span><span class="art__cap" data-ar="{{ }} الكود">{{ }} THE CODE</span></div>
          <div>
            <p class="person__role" data-ar="المسار التقني · الخبر، السعودية">TECHNOLOGY TRACK · AL KHOBAR, KSA</p>
            <h3>Ahmed Bedeer</h3>
            <p class="person__tag" data-ar="مهندس معماري مؤسسي ومتخصص في التحول الرقمي · الخبر، السعودية">Enterprise Architect &amp; Digital Transformation Specialist · Al Khobar, KSA</p>
            <div class="creds" aria-label="Credentials" data-ar-label="الاعتمادات"><span>CPHIMS</span><span>TOGAF</span><span>EMRAM</span><span>NORA</span></div>
            <div class="person__links">
              <a href="https://ahmed-bedeer.vercel.app/" target="_blank" rel="noopener" title="Ahmed's Portfolio">{icon('link')}<span data-ar="الأعمال">Portfolio</span></a>
              <a href="/technology-services/">{icon('layers')}<span data-ar="خدمات التقنية">Technology Services</span></a>
              <a href="https://wa.me/966545520750" target="_blank" rel="noopener">{icon('chat')}<span data-ar="واتساب · السعودية">WhatsApp · KSA</span></a>
            </div>
          </div>
        </article>'''
    return f'''
        <article class="card glass person" data-reveal>
          <div class="art art--square art--pink" data-slot="team/mustafa-aboalazm"><span class="art__mark">MA</span><span class="art__cap" data-ar="✦ الكانفاس">✦ THE CANVAS</span></div>
          <div>
            <p class="person__role" data-ar="المسار الإبداعي · العبور، مصر">CREATIVE TRACK · AL OBOUR, EGYPT</p>
            <h3>Mustafa Aboalazm</h3>
            <p class="person__tag" data-ar="مصمم هوية بصرية أول ومهندس هويات منهجية · العبور، مصر">Senior Brand Identity Designer &amp; Systemic Identity Architect · Al Obour, Egypt</p>
            <div class="creds" aria-label="Highlights" data-ar-label="أبرز النقاط"><span data-ar="استراتيجية العلامة">Brand Strategy</span><span data-ar="+9 سنوات">9+ Years</span><span data-ar="+20 علامة">20+ Brands</span><span data-ar="عربي + إنجليزي">AR + EN</span></div>
            <div class="person__links">
              <a href="https://aboalazm-os.vercel.app/" target="_blank" rel="noopener" title="Mustafa's Portfolio">{icon('link')}<span data-ar="الأعمال">Portfolio</span></a>
              <a href="/creative-services/">{icon('pen')}<span data-ar="الخدمات الإبداعية">Creative Services</span></a>
              <a href="https://wa.me/201092500454" target="_blank" rel="noopener">{icon('chat')}<span data-ar="واتساب · مصر">WhatsApp · EG</span></a>
            </div>
          </div>
        </article>'''


def build():
    tech = [c for c in SERVICES if c.startswith('AB-')]
    creative = [c for c in SERVICES if c.startswith('MA-')]
    health = [c for c in SERVICES if c.startswith('HC-')]
    combined = [c for c in SERVICES if c.startswith('CC-')]

    body = f'''
      <!-- ░░ Hero ░░ -->
      <section class="phero container phero--center" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('Solutions', 'الحلول', None)])}
        <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="الهوية · التقنية · الرعاية الصحية · البيانات · الإعلام">Brand · Technology · Healthcare · Data · Media</span></span>
        <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s"><span data-ar="كل حلولنا.">All our solutions.</span><br /><span class="grad-text" data-ar="إبداعية. تقنية.">Creative. Technical.</span></h1>
        <p class="hero__lead" data-reveal style="--d:.16s" data-ar-html="مؤسِّسان. تخصصان. &lt;strong&gt;23 خدمة مُنتجة&lt;/strong&gt; عبر العمارة المؤسسية وتقنية الرعاية الصحية والتحول الرقمي والبيانات وهوية العلامة وأنظمة التصميم والويب والإعلام. اضغط أي خدمة لترى النطاق الكامل والمخرجات والتسعير.">Two co-founders. Two disciplines. <strong>23 productized services</strong> across enterprise architecture, healthcare IT, digital transformation, data, brand identity, design systems, web, and media. Tap any service for full scope, deliverables, and pricing.</p>
        <nav class="subnav" aria-label="Jump to a track" data-ar-label="انتقل إلى مسار" data-reveal style="--d:.24s">
          <a href="#technology">{icon('layers')}<span data-ar="التقنية">Technology</span><b>6</b></a>
          <a href="#creative">{icon('pen')}<span data-ar="الإبداع">Creative</span><b>10</b></a>
          <a href="#healthcare">{icon('stethoscope')}<span data-ar="الرعاية الصحية">Healthcare</span><b>5</b></a>
          <a href="#combined">{icon('sparkles')}<span data-ar="باقات متكاملة">Combined</span><b>2</b></a>
        </nav>
      </section>

      <!-- ░░ Stats ░░ -->
      <section class="stats container" aria-label="Solutions at a glance" data-ar-label="الحلول في أرقام">
        <div class="stats__inner glass" data-reveal>
          <div class="stat"><span class="stat__num stat__num--ltr"><span data-count="23" data-latin="1">23</span></span><p class="stat__label" data-ar-html="خدمة&lt;br /&gt;مُنتجة">Productized<br />services</p></div>
          <div class="stat"><span class="stat__num stat__num--ltr"><span data-count="9" data-latin="1">9</span>+</span><p class="stat__label" data-ar-html="سنوات عبر&lt;br /&gt;كلا التخصصين">Years across<br />both practices</p></div>
          <div class="stat"><span class="stat__num stat__num--ltr"><span data-count="40" data-latin="1">40</span>+</span><p class="stat__label" data-ar-html="علامة ومؤسسة&lt;br /&gt;خدمناها">Brands &amp;<br />orgs served</p></div>
          <div class="stat"><span class="stat__num stat__num--ltr">KSA+EG</span><p class="stat__label" data-ar-html="تغطية&lt;br /&gt;منطقة MENA">MENA<br />coverage</p></div>
        </div>
      </section>

      <!-- ░░ Technology ░░ -->
      <section class="section container" id="technology" aria-labelledby="tech-title">
        {person_card('ahmed')}
        <header class="section__head" style="margin-top:40px" data-reveal>
          <p class="kicker"><span class="kicker__num">01</span><span data-ar="خدمات التقنية · العمارة المؤسسية · تقنية الرعاية الصحية · السحابة · البيانات">Technology Services · EA · Healthcare IT · Cloud · Data</span></p>
          <h2 class="section__title" id="tech-title"><span data-ar="عمارة، تحوّل، بيانات.">Architecture, transformation, data.</span><br /><span class="grad-text" data-ar="مبنية لاتخاذ القرار.">Built for decisions.</span></h2>
          <p class="section__lead" data-ar="ستة مشاريع مُنتجة — كل مخرج يعود إلى مصفوفة مواءمة الأعمال مع التقنية. على مراحل بمعالم محددة، لا مفتوحة النهاية.">Six productized engagements — every artifact traces back to the Business-to-Technology Alignment Matrix. Milestone-based, not open-ended.</p>
        </header>
        {svc_grid(tech)}
        <p class="svc-note"><span data-ar="تريد النطاق الكامل والمخرجات والاعتمادات؟">Want full scope, deliverables, and credentials?</span> <a class="text-link" href="/technology-services/"><span data-ar="افتح صفحة خدمات التقنية">Open Technology Services</span>{icon('arrow', 'flip')}</a></p>
      </section>

      <!-- ░░ Creative ░░ -->
      <section class="section container section--flush-top" id="creative" aria-labelledby="creative-title">
        {person_card('mustafa')}
        <header class="section__head" style="margin-top:40px" data-reveal>
          <p class="kicker"><span class="kicker__num">02</span><span data-ar="الاستوديو الإبداعي · الهوية · التصميم · الويب · الإعلام">Creative Studio · Brand · Design · Web · Media</span></p>
          <h2 class="section__title" id="creative-title"><span data-ar="هوية مبنية">Identity built as</span><br /><span class="grad-text" data-ar="كنظام تشغيل.">an operating system.</span></h2>
          <p class="section__lead" data-ar="عشر خدمات — من سبرنت شعار بـ ⁦$170⁩ إلى منظومة علامة كاملة ومنصات مخصّصة واشتراكات شهرية. ثنائية اللغة عربي/إنجليزي كمعيار.">Ten services — from a $170 logo sprint to a full brand system, custom platforms, and monthly retainers. Bilingual AR/EN as standard.</p>
        </header>
        {svc_grid(creative)}
        <p class="svc-note"><span data-ar="تريد منهجية الأربعة فصول وقائمة الأسعار المفصّلة؟">Want the 4-act method and the à la carte price list?</span> <a class="text-link" href="/creative-services/"><span data-ar="افتح صفحة الخدمات الإبداعية">Open Creative Services</span>{icon('arrow', 'flip')}</a></p>
      </section>

      <!-- ░░ Healthcare ░░ -->
      <section class="section container section--flush-top" id="healthcare" aria-labelledby="hc-title">
        <header class="section__head" data-reveal>
          <p class="kicker"><span class="kicker__num">03</span><span data-ar="الرعاية الصحية · CPHIMS · EMRAM · CBAHI · NORA">Healthcare · CPHIMS · EMRAM · CBAHI · NORA</span></p>
          <h2 class="section__title" id="hc-title"><span data-ar="مبنية للعيادات والمستشفيات">Built for clinics and hospitals</span><br /><span class="grad-text" data-ar="في السعودية ومصر.">in KSA and Egypt.</span></h2>
          <p class="section__lead" data-ar="خمسة مشاريع تجمع التخصصين — هوية تبني الثقة، وتحوّل مُقاد بـ CPHIMS، وذكاء قرار متوافق مع CBAHI.">Five engagements that combine both disciplines — trust-building identity, CPHIMS-led transformation, and CBAHI-aligned decision intelligence.</p>
        </header>
        {svc_grid(health)}
        <p class="svc-note"><span data-ar="تعمل في الرعاية الصحية؟">Working in healthcare?</span> <a class="text-link" href="/healthcare/"><span data-ar="افتح صفحة حلول الرعاية الصحية">Open Healthcare Solutions</span>{icon('arrow', 'flip')}</a></p>
      </section>

      <!-- ░░ Combined ░░ -->
      <section class="section container section--flush-top" id="combined" aria-labelledby="cc-title">
        <header class="section__head" data-reveal>
          <p class="kicker"><span class="kicker__num">04</span><span data-ar="باقات متكاملة · موجز واحد · كلا المؤسسَين">Combined packages · One brief · Both founders</span></p>
          <h2 class="section__title" id="cc-title"><span data-ar="عندما تحتاج">When you need</span> <span class="grad-text" data-ar="الكود والكانفاس معًا.">the Code and the Canvas together.</span></h2>
          <p class="section__lead" data-ar="باقتان تُدار فيهما الهوية والتقنية وتطوير الأعمال كمشروع واحد — بدون فجوات تسليم بين مزوّدَين.">Two packages where brand, technology, and business development run as one engagement — no hand-off gaps between two vendors.</p>
        </header>
        <div class="svc-grid">
          {_combined_card('CC-01', 0)}
          {_combined_card('CC-02', 0.07)}
          <a class="card glass svc tile--accent" href="/pricing-faq/" data-tilt data-reveal style="--d:.14s">
            <span class="svc__top"><span class="svc__no">USD · SAR · EGP</span><span class="svc__tag" data-ar="الأسعار والأسئلة الشائعة">PRICING &amp; FAQ</span></span>
            <h3 data-ar="كيف نُحاسب — ولماذا لا توجد مفاجآت">How we charge — and why there are no surprises</h3>
            <p data-ar="المشاريع الإبداعية 50 / 25 / 25 · الاستشارات والعمارة المؤسسية 50 / 50 · النطاق يُثبَّت عند الانطلاق · الملفات تُسلَّم عند السداد الكامل.">Creative engagements 50 / 25 / 25 · Advisory &amp; EA 50 / 50 · Scope locked at kickoff · Files released on full settlement.</p>
            <span class="svc__foot"><span class="svc__price"><strong class="ltr" data-ar="10 أسئلة شائعة">10 FAQs</strong><span data-ar="شروط الدفع · السياسات · العملات">Payment terms · Policies · Currencies</span></span><span class="round-arrow" aria-hidden="true"><i class="flip" data-icon="arrowUpRight"></i></span></span>
          </a>
        </div>
      </section>

      <!-- ░░ Not sure ░░ -->
      <section class="section container section--tight" aria-labelledby="fit-title">
        <div class="callout glass glass--deep" data-reveal>
          <div>
            <p class="kicker"><span data-ar="لست متأكدًا؟">NOT SURE?</span></p>
            <h3 id="fit-title"><span data-ar="لست متأكدًا أي خدمة">Not sure which service</span><br /><span class="grad-text" data-ar="تناسب مشكلتك؟">fits your problem?</span></h3>
            <p data-ar="أخبرنا بمشكلة العمل — وسنقترح أخف مشروع يوصلك إلى قرار واثق. نطاق واضح من المكالمة الأولى، وإلا فلن نتابع.">Tell us the business problem — we'll propose the lightest engagement that gets you a confident decision. Clear scope from the first call, or we won't follow up.</p>
          </div>
          <div class="callout__actions">
            {btn('Book a Free 30-Min Call', 'احجز مكالمة مجانية · 30 دقيقة', '/contact/#book')}
            <a class="text-link" href="https://wa.me/966545520750" target="_blank" rel="noopener">{icon('chat')}<span data-ar="واتساب · السعودية (التقنية)">WhatsApp · KSA (Tech)</span></a>
            <a class="text-link" href="https://wa.me/201092500454" target="_blank" rel="noopener">{icon('chat')}<span data-ar="واتساب · مصر (الإبداع)">WhatsApp · EG (Creative)</span></a>
          </div>
        </div>
      </section>

      <!-- ░░ Freelancer / career form ░░ -->
      <section class="section container section--tight" id="career" aria-labelledby="career-title">
        <div class="grid grid--side-l">
          <header class="section__head sticky" data-reveal>
            <p class="kicker"><span class="kicker__num">05</span><span data-ar="مستقل؟ انضم إلى تطويرنا">Freelancer? Connect to our development</span></p>
            <h2 class="section__title" id="career-title"><span data-ar="مستقل؟">Freelancer?</span><br /><span class="grad-text" data-ar="انضم إلى فريق تطويرنا.">Connect to our development.</span></h2>
            <p class="section__lead" data-ar="نعمل مع مستقلين موهوبين في التصميم والهندسة والمحتوى من المنطقة. أخبرنا بقصتك — نردّ على كل طلب جادّ.">We work with talented freelancers in design, engineering, and content across the region. Tell us your story — every serious application gets a reply.</p>
            <ul class="hero__chips" aria-label="What we look for" data-ar-label="ما الذي نبحث عنه"><li>{icon('pen')}<span data-ar="التصميم">Design</span></li><li>{icon('layers')}<span data-ar="الهندسة">Engineering</span></li><li>{icon('sparkles')}<span data-ar="المحتوى والإنتاج">Content &amp; Production</span></li></ul>
          </header>
          <form class="form-card glass form" data-form="contact" data-whatsapp="201092500454" data-mail="info@codeandcanvas.net" data-subject="Freelancer application — Code &amp; Canvas" data-endpoint="" novalidate data-reveal>
            <h3 data-ar="الطلب">Career</h3>
            <p class="lead" data-ar="نموذج حواري — املأ ما يناسبك وأرسل.">Conversational form — fill what applies and send.</p>
            <input class="hp" type="text" name="_hp" tabindex="-1" autocomplete="off" aria-hidden="true" />
            <input type="hidden" name="inquiry" value="Freelancer / Career" />
            <div class="form__row">
              <div class="field"><label for="f-name" data-ar-html="اسمك &lt;i&gt;*&lt;/i&gt;">Your Name <i>*</i></label><input id="f-name" name="name" type="text" required autocomplete="name" /><span class="field__err" data-ar="أدخل اسمك">Please enter your name</span></div>
              <div class="field"><label for="f-city" data-ar="تعيش في؟">Live in?</label><input id="f-city" name="live_in" type="text" autocomplete="address-level2" /></div>
            </div>
            <div class="field"><label for="f-email" data-ar-html="البريد الإلكتروني &lt;i&gt;*&lt;/i&gt;">Email <i>*</i></label><input id="f-email" name="email" type="email" required autocomplete="email" /><span class="field__err" data-ar="أدخل بريدًا صحيحًا">Please enter a valid e-mail</span></div>
            <div class="field"><label for="f-spark" data-ar="شرارة مهارتك">Your Skill Spark</label><input id="f-spark" name="skill_spark" type="text" placeholder="Brand design · Next.js · Motion · Copywriting…" data-ar-placeholder="تصميم هوية · Next.js · موشن · كتابة محتوى…" /></div>
            <div class="field"><label for="f-growth" data-ar="فصول نموّك">Your Chapters of Growth</label><textarea id="f-growth" name="chapters_of_growth" rows="3" placeholder="Where you started, what you've shipped, what you're learning now." data-ar-placeholder="من أين بدأت، وماذا أنجزت، وماذا تتعلم الآن."></textarea></div>
            <div class="form__row">
              <div class="field"><label for="f-portfolio" data-ar="رابط الأعمال">Portfolio URL</label><input id="f-portfolio" name="portfolio_url" type="url" placeholder="https://" /></div>
              <div class="field"><label for="f-cv" data-ar="رابط السيرة الذاتية">CV URL</label><input id="f-cv" name="cv_url" type="url" placeholder="https://" /></div>
            </div>
            <div class="field"><label for="f-time" data-ar="وقت فراغك اليومي">Your Daily free time</label>
              <select id="f-time" name="daily_free_time"><option value="" data-ar="- اختر -">- Select -</option><option value="Daytime" data-ar="نهارًا">Daytime</option><option value="Nighttime" data-ar="ليلًا">Nighttime</option></select></div>
            <div class="field"><label for="f-ink" data-ar="حبرك المختلف">Your Different Ink</label><input id="f-ink" name="different_ink" type="text" placeholder="What makes your work unmistakably yours?" data-ar-placeholder="ما الذي يجعل عملك مميزًا بلا شك؟" /></div>
            <div class="field"><label for="f-note" data-ar="ملاحظتك">Your note</label><textarea id="f-note" name="message" rows="3"></textarea></div>
            <div class="form__actions">
              <button class="btn btn--primary magnetic" type="submit"><span data-ar="إرسال">Submit</span><i class="flip" data-icon="arrowUpRight"></i></button>
              <span class="field__hint" data-ar="يُفتح طلبك في واتساب أو البريد حتى يُربط النموذج بخدمة إرسال.">Opens in WhatsApp or e-mail until a form endpoint is connected.</span>
            </div>
            <div class="form__status" role="status" aria-live="polite"></div>
          </form>
        </div>
      </section>

      {closing('THE HOME OF BUSINESS DEVELOPMENT', 'موطن تطوير الأعمال',
               '<span data-ar="موطن">The Home of</span><br /><span class="grad-text" data-ar="تطوير الأعمال.">Business Development.</span>',
               'Read how two disciplines became one studio — and why every engagement starts with the business outcome, not the deliverable.',
               'اقرأ كيف أصبح تخصصان استوديو واحدًا — ولماذا يبدأ كل مشروع من نتيجة العمل لا من المخرج.',
               [btn('Our Story', 'قصتنا', '/our-story/'), btn('Book a Free Discovery Call', 'احجز مكالمة استكشافية مجانية', '/contact/#book', 'glass')])}
'''
    out = page('/services/', title='Solutions — Code & Canvas', title_ar='الحلول — Code & Canvas',
               desc='All Code & Canvas solutions: 23 productized services across enterprise architecture, healthcare IT, digital transformation, data, brand identity, design systems, web, and media — with scope, duration, and pricing.',
               desc_ar='كل حلول Code & Canvas: 23 خدمة مُنتجة عبر العمارة المؤسسية وتقنية الرعاية الصحية والتحول الرقمي والبيانات وهوية العلامة وأنظمة التصميم والويب والإعلام — بالنطاق والمدة والتسعير.',
               nav='services', body=body)
    return [out]


def _combined_card(code, delay):
    s = SERVICES[code]
    return f'''<a class="card glass svc svc--combined" id="{code.lower()}" data-category="combined" href="/contact/#book" data-tilt data-reveal style="--d:{delay}s">
            <span class="svc__top"><span class="svc__no">{code}</span>{t(s['tag'], s['tag_ar'], cls='svc__tag')}</span>
            <h3 data-ar="{esc(s['title_ar'])}">{esc(s['title'])}{' <i aria-hidden="true">✦</i>' if s.get('star') else ''}</h3>
            <p data-ar="{esc(s['blurb_ar'])}">{esc(s['blurb'])}</p>
            <span class="svc__foot"><span class="svc__price"><strong class="ltr">{esc(s['price'])}</strong>{t(s['dur'], s['dur_ar'])}</span><span class="round-arrow" aria-hidden="true"><i class="flip" data-icon="arrowUpRight"></i></span></span>
          </a>'''
