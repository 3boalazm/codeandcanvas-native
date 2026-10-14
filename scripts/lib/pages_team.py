# -*- coding: utf-8 -*-
"""/team/ — live copy of codeandcanvas.net/team/."""
from h import esc, icon, crumbs, closing, btn, page

FLAGSHIPS = [
    (['Canvas', 'Code'], 'Venture Launch 0 → 1', 'إطلاق مشروع من 0 إلى 1',
     'Brand + positioning + bilingual website + product architecture + analytics — from the first strategy session to a market-ready launch in one governed pipeline.',
     'هوية + تموضع + موقع ثنائي اللغة + عمارة منتج + تحليلات — من أول جلسة استراتيجية إلى إطلاق جاهز للسوق في مسار واحد محكوم.',
     '/services/#cc-01', 'Learn more →', 'اعرف المزيد ←', None),
    (['EMRAM · CBAHI', 'Brand'], 'Healthcare Digital Identity', 'الهوية الرقمية للرعاية الصحية',
     'Clinic or hospital brand + patient experience + EMRAM/NORA architecture + HIS advisory. The only studio in MENA that combines branding with CPHIMS-level clinical architecture.',
     'هوية عيادة أو مستشفى + تجربة مريض + عمارة EMRAM/NORA + استشارات HIS. الاستوديو الوحيد في المنطقة الذي يجمع بين بناء العلامة والعمارة السريرية بمستوى CPHIMS.',
     '/healthcare/', 'Learn more →', 'اعرف المزيد ←', None),
    (['Rebrand', 'Re-platform'], 'Rebrand + Re-platform', 'إعادة بناء الهوية + إعادة بناء المنصة',
     'For established companies whose brand AND tech have both aged without a plan. We modernize the whole organization — inside and out — in one milestone-based engagement.',
     'للشركات القائمة التي شاخت هويتها وتقنيتها معًا دون خطة. نحدّث المؤسسة كاملة — من الداخل والخارج — في مشروع واحد قائم على المعالم.',
     '/services/', 'Most requested →', 'الأكثر طلبًا ←',
     [('Brand audit + refresh', 'تدقيق وتجديد العلامة'), ('Visual identity system', 'منظومة هوية بصرية'), ('EA assessment (TOGAF)', 'تقييم العمارة المؤسسية (TOGAF)'), ('Legacy modernization', 'تحديث الأنظمة القديمة'), ('Cloud migration plan', 'خطة الهجرة السحابية')]),
    (['Canvas', 'Code'], 'Brand-to-Code Design System', 'نظام تصميم من العلامة إلى الكود',
     'A design system that is simultaneously a brand system AND an engineering component library — from Figma tokens to coded components your dev team actually uses.',
     'نظام تصميم هو في الوقت نفسه نظام علامة ومكتبة مكوّنات هندسية — من رموز Figma إلى مكوّنات مبرمجة يستخدمها فريق التطوير فعلًا.',
     '/creative-services/#ma-04', 'Learn more →', 'اعرف المزيد ←', None),
    (['BI · Analytics', 'Visual'], 'Executive Data Intelligence', 'ذكاء البيانات التنفيذي',
     'Ahmed builds the EDW + dashboards + predictive models. Mustafa designs the data language and executive-facing reports. Decision intelligence that performs AND communicates.',
     'يبني أحمد مستودع البيانات ولوحات المؤشرات والنماذج التنبؤية. ويصمم مصطفى لغة البيانات والتقارير الموجّهة للإدارة التنفيذية. ذكاء قرارات يعمل ويتواصل معًا.',
     '/technology-services/#ab-03', 'Learn more →', 'اعرف المزيد ←', None),
]


def build():
    flags = ''
    for i, (tags, en, ar, den, dar, href, cta, cta_ar, extra) in enumerate(FLAGSHIPS):
        tg = ''.join(f'<span class="pill">{esc(x)}</span>' for x in tags)
        ex = ''
        if extra:
            ex = '<ul class="ticks ticks--dense" style="margin-top:12px">' + ''.join(f'<li data-ar="{esc(a)}">↳ {esc(e)}</li>' for e, a in extra) + '</ul>'
        flags += f'''
          <article class="card glass tile{' tile--accent' if extra else ''}" data-tilt data-reveal style="--d:{(i % 3) * .07:.2f}s">
            <div class="pill-list">{tg}</div>
            <h3 style="margin-top:14px" data-ar="{esc(ar)}">{esc(en)}</h3>
            <p data-ar="{esc(dar)}">{esc(den)}</p>{ex}
            <a class="text-link" href="{href}" style="margin-top:14px"><span data-ar="{esc(cta_ar)}">{esc(cta)}</span></a>
          </article>'''

    body = f'''
      <!-- ░░ Hero ░░ -->
      <section class="phero container phero--center" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('About', 'من نحن', '/about/'), ('Team', 'الفريق', None)])}
        <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="Code &amp; Canvas · الاستوديو">Code &amp; Canvas · The Studio</span></span>
        <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s"><span data-ar="عقلان.">Two Minds.</span> <span class="grad-text" data-ar="منظومة واحدة.">One Ecosystem.</span></h1>
        <p class="hero__lead" data-reveal style="--d:.16s" data-ar-html="لسنا وكالة من 100 شخص. بل استوديو رشيق بشريكين حيث تعمل &lt;strong&gt;عمارة العلامة&lt;/strong&gt; و&lt;strong&gt;الهندسة الرقمية&lt;/strong&gt; كنظام واحد متكامل — من أول جلسة استراتيجية إلى يوم الإطلاق.">Not a 100-person agency. A lean, two-partner studio where <strong>brand architecture</strong> and <strong>digital engineering</strong> operate as one integrated system — from the first strategy session to launch day.</p>
        <nav class="subnav" aria-label="Founders" data-ar-label="المؤسسان" data-reveal style="--d:.22s"><a href="#ahmed" data-ar="الكود">The Code</a><a href="#mustafa" data-ar="الكانفاس">The Canvas</a><a href="#together" data-ar="لماذا معًا">Why Together</a></nav>
      </section>

      <!-- ░░ Founders ░░ -->
      <section class="section container section--tight" aria-label="Founders" data-ar-label="المؤسسان">
        <div class="grid grid--2">
          <article class="card glass person person--stack" id="ahmed" data-reveal>
            <div class="art art--portrait" data-slot="team/ahmed-bedeer"><span class="art__mark">{{ }}</span><span class="art__cap" data-ar="{{ }} الكود">{{ }} The Code</span></div>
            <div>
              <p class="person__role" data-ar="{{ }} الكود">{{ }} The Code</p>
              <h2>Ahmed M. Bedeer</h2>
              <p class="person__tag" data-ar="مهندس معماري مؤسسي · مهندس حلول">Enterprise Architect · Solution Architect</p>
              <blockquote class="quote" data-ar="«يحوّل التعقيد إلى بنية تحتية مرنة وقابلة للتوسع.»">"Turns complexity into flexible, scalable infrastructure."</blockquote>
              <p class="person__hint">// <span data-ar="المنظومة التقنية">the stack</span></p>
              <div class="creds"><span>TOGAF · NORA</span><span>ArchiMate</span><span>Java · Spring Boot</span><span data-ar="إدارة البيانات">Data Management</span><span data-ar="تقنية الرعاية الصحية">Healthcare IT</span><span>FHIR · HL7</span><span data-ar="السحابة والعمارة المؤسسية">Cloud &amp; EA</span></div>
              <div class="person__links">
                <a href="https://linkedin.com/in/ahmed-bedeer" target="_blank" rel="noopener" title="LinkedIn">{icon('linkedin')}<span>LinkedIn</span></a>
                <a href="https://ahmed-bedeer.vercel.app/" target="_blank" rel="noopener" title="Portfolio">{icon('link')}<span data-ar="الأعمال">Portfolio</span></a>
                <a href="https://github.com/ahmedbdeer" target="_blank" rel="noopener" title="GitHub">{icon('github')}<span>GitHub</span></a>
              </div>
            </div>
          </article>
          <article class="card glass person person--stack" id="mustafa" data-reveal style="--d:.08s">
            <div class="art art--portrait art--pink" data-slot="team/mustafa-aboalazm"><span class="art__mark">✦</span><span class="art__cap" data-ar="✦ الكانفاس">✦ The Canvas</span></div>
            <div>
              <p class="person__role" data-ar="✦ الكانفاس">✦ The Canvas</p>
              <h2>Mustafa Aboalazm</h2>
              <p class="person__tag" data-ar="مدير إبداعي · مهندس هوية بصرية">Creative Director · Visual Brand Architect</p>
              <blockquote class="quote" data-ar="«يحوّل الأفكار إلى تجارب بصرية تترك أثرًا دائمًا.»">"Turns ideas into visual experiences that leave a lasting impression."</blockquote>
              <p class="person__hint">// <span data-ar="الأدوات">the toolkit</span></p>
              <div class="creds"><span data-ar="هوية العلامة">Brand Identity</span><span data-ar="الأنظمة البصرية">Visual Systems</span><span>Figma · Webflow</span><span data-ar="الإخراج الفني">Art Direction</span><span data-ar="المطبوعات والتغليف">Print &amp; Packaging</span><span data-ar="التصوير">Photography</span><span data-ar="إنتاج الفيديو">Video Production</span></div>
              <div class="person__links">
                <a href="https://behance.net/aboalazm" target="_blank" rel="noopener" title="Behance">{icon('pen')}<span>Behance</span></a>
                <a href="https://aboalazm-os.vercel.app/" target="_blank" rel="noopener" title="Portfolio">{icon('link')}<span data-ar="الأعمال">Portfolio</span></a>
                <a href="https://wa.me/201092500454" target="_blank" rel="noopener" title="WhatsApp">{icon('chat')}<span>WhatsApp</span></a>
              </div>
            </div>
          </article>
        </div>
      </section>

      <!-- ░░ Why together ░░ -->
      <section class="section container section--flush-top" id="together" aria-labelledby="tog-title">
        <header class="section__head" data-reveal>
          <p class="kicker"><span class="kicker__num">01</span><span data-ar="لماذا معًا">Why Together</span></p>
          <h2 class="section__title" id="tog-title"><span data-ar="حيث يلتقي">Where the</span> <span class="grad-text" data-ar="الكانفاس بالكود.">Canvas meets the Code.</span></h2>
          <p class="section__lead" data-ar="خمسة مشاريع رئيسية لا يستطيع أيٌّ منا تقديمها وحده — كل منها اندماج يعزّز فيه تفكير العلامة وانضباط العمارة بعضهما بعضًا.">Five flagship engagements that neither of us could deliver alone — each one a fusion where brand thinking and architecture discipline reinforce each other.</p>
        </header>
        <div class="grid grid--3">{flags}
        </div>
      </section>

      <!-- ░░ CTA ░░ -->
      <section class="section container section--tight" aria-labelledby="cta-title">
        <div class="callout glass glass--deep" data-reveal>
          <div>
            <h3 id="cta-title"><span data-ar="موجز واحد. تخصصان.">One brief. Two disciplines.</span> <em class="grad-text" data-ar="صفر فجوات تسليم.">Zero handoff gaps.</em></h3>
            <p data-ar="كل مشروع في Code &amp; Canvas يعمل على موجز واحد مشترك — لا سياق ضائع بين مكتب العلامة ولوحة العمارة. هذه هي ميزة الكفاءة التي تحصل عليها من استوديو بشريكين.">Every engagement at Code &amp; Canvas runs on a single shared brief — no lost context between the brand desk and the architecture board. That's the efficiency premium you get from a two-partner studio.</p>
          </div>
          <div class="callout__actions">{btn('Book a Free Discovery Call', 'احجز مكالمة استكشافية مجانية', '/contact/#book')}</div>
        </div>
      </section>

      {closing('HOPE YOU HAVE ENJOYED OUR JOURNEY', 'نأمل أن تكون قد استمتعت برحلتنا',
               '<span data-ar="ما الخدمة التي لفتت انتباهك">What service appealed to you</span><br /><span class="grad-text" data-ar="أو التي يمكننا تقديمها لك؟">or that we could provide for you?</span>',
               'Tell us where your problem sits and we’ll point you to the right engagement — and the right founder to lead it.',
               'أخبرنا أين تقع مشكلتك وسنوجّهك إلى المشروع المناسب — والمؤسس المناسب لقيادته.',
               [btn('Contacts', 'تواصل معنا', '/contact/'), btn('Services', 'الخدمات', '/services/', 'glass', 'arrow')])}
'''
    return [page('/team/', title='Team — Code & Canvas', title_ar='الفريق — Code & Canvas',
                 desc='Two minds, one ecosystem. Ahmed M. Bedeer (Enterprise Architect) and Mustafa Aboalazm (Creative Director) — a lean two-partner studio where brand architecture and digital engineering operate as one system.',
                 desc_ar='عقلان ومنظومة واحدة. أحمد بدير (مهندس معماري مؤسسي) ومصطفى أبو العزم (مدير إبداعي) — استوديو رشيق بشريكين تعمل فيه عمارة العلامة والهندسة الرقمية كنظام واحد.',
                 nav='about', body=body)]
