# -*- coding: utf-8 -*-
"""/our-story/ — live copy of codeandcanvas.net/our-story/ (chapter layout).
Image placeholders on the live page ("Replace src=YOUR_IMAGE_URL_HERE") become
CSS art tiles with a `data-slot` so real photos can be dropped in later."""
from h import esc, icon, crumbs, closing, btn, page

CHAPTERS = [
    dict(id='architecture', num='01', kicker='Technology & Architecture', kicker_ar='التقنية والعمارة',
         title='The Home of Architecture.', title_ar='موطن العمارة.',
         lead='Where every technology decision is traced back to a business goal — <strong>not a specification document.</strong> TOGAF-anchored. NORA-aligned. Vision 2030-aware.',
         lead_ar='حيث يُتتبّع كل قرار تقني إلى هدف عمل — <strong>لا إلى وثيقة مواصفات.</strong> مرتكز على TOGAF. متوائم مع NORA. واعٍ برؤية 2030.',
         body='Ahmed builds enterprise architectures in KSA grounded in <strong>TOGAF, ArchiMate, and NORA</strong> — translating a CIO\'s problem into a traceable decision tree a board can approve and a developer can implement. Every engagement produces a <em>Business-to-Technology Alignment Matrix.</em>',
         body_ar='يبني أحمد عمارات مؤسسية في السعودية مرتكزة على <strong>TOGAF و ArchiMate و NORA</strong> — محوّلًا مشكلة مدير تقنية المعلومات إلى شجرة قرارات قابلة للتتبع يعتمدها مجلس الإدارة وينفذها المطوّر. كل مشروع ينتج <em>مصفوفة مواءمة الأعمال مع التقنية.</em>',
         pills=['TOGAF', 'NORA', 'ArchiMate 3.1', 'Vision 2030'], href='/technology-services/',
         art='art--violet', mark='🏗', cap='TOGAF · NORA', cap2='Enterprise Architecture Practice', cap2_ar='ممارسة العمارة المؤسسية', slot='story/01-architecture', flip=False),
    dict(id='identity', num='02', kicker='Brand Identity & Creative', kicker_ar='هوية العلامة والإبداع',
         title='The Home of Identity.', title_ar='موطن الهوية.',
         lead='Where a logo becomes a system, a system becomes a language, and a language <strong>becomes the thing clients recognize before they read a word.</strong>',
         lead_ar='حيث يصبح الشعار نظامًا، والنظام لغة، واللغة <strong>هي ما يتعرّف عليه العملاء قبل أن يقرأوا كلمة واحدة.</strong>',
         body='Mustafa treats brand work as <strong>commercial work</strong> — every design decision either supports a revenue outcome or gets cut. The 4-act methodology (Discovery, Strategy, Concept, Refine) exists because <em>skipping strategy gives you a logo, not a brand.</em>',
         body_ar='يتعامل مصطفى مع عمل العلامة بوصفه <strong>عملًا تجاريًا</strong> — كل قرار تصميمي إما يدعم نتيجة إيرادية أو يُستبعد. منهجية الفصول الأربعة (الاستكشاف، الاستراتيجية، المفهوم، الصقل) موجودة لأن <em>تخطّي الاستراتيجية يعطيك شعارًا لا علامة.</em>',
         pills=['Brand Strategy', 'Bilingual AR/EN', 'Design Systems', 'Figma'], href='/creative-services/',
         art='art--pink', mark='🎨', cap='20+ Brands', cap2='Shaped across 6 sectors', cap2_ar='صُغناها عبر 6 قطاعات', slot='story/02-identity', flip=True),
    dict(id='healthcare', num='03', kicker='Healthcare Vertical', kicker_ar='قطاع الرعاية الصحية',
         title='The Home of Healthcare.', title_ar='موطن الرعاية الصحية.',
         lead='Where clinical context is built in from day one — not briefed in on day one. <strong>CPHIMS. EMRAM. CBAHI. NORA.</strong> Not listed frameworks. Active credentials.',
         lead_ar='حيث يُبنى السياق السريري من اليوم الأول — لا يُشرح في اليوم الأول. <strong>CPHIMS. EMRAM. CBAHI. NORA.</strong> ليست أطرًا مُدرجة بل اعتمادات فعّالة.',
         body='Healthcare IT is where a wrong decision costs most — a misaligned HIS costs $50K–$200K to exit. We operate <em>inside</em> the ecosystem: clinical workflow context in every technology recommendation, CBAHI-aware design in every visual decision.',
         body_ar='تقنية الرعاية الصحية هي حيث يكلّف القرار الخاطئ أكثر — نظام HIS غير متوائم يكلّف ⁦$50K–$200K⁩ للخروج منه. نعمل <em>داخل</em> المنظومة: سياق مسارات العمل السريرية في كل توصية تقنية، وتصميم واعٍ بـ CBAHI في كل قرار بصري.',
         pills=['CPHIMS', 'HIMSS EMRAM', 'CBAHI', 'NORA'], href='/healthcare/',
         art='art--mint', mark='⚕', cap='CPHIMS · EMRAM', cap2='CBAHI · NORA · HIMSS', cap2_ar='CBAHI · NORA · HIMSS', slot='story/03-healthcare', flip=False),
    dict(id='data', num='04', kicker='Data & Analytics', kicker_ar='البيانات والتحليلات',
         title='The Home of Data.', title_ar='موطن البيانات.',
         lead='Where operational data stops being a reporting burden and starts being <strong>the thing that tells leadership what to do next.</strong>',
         lead_ar='حيث تتوقف البيانات التشغيلية عن كونها عبء تقارير وتصبح <strong>ما يخبر القيادة بالخطوة التالية.</strong>',
         body='The problem is rarely the data — <em>it\'s the distance between the data and the decision.</em> We close it by building <strong>the right KPI framework first</strong>, then connecting the data, then making it visible in a format leadership can act on without a data team in the room.',
         body_ar='نادرًا ما تكون المشكلة في البيانات — <em>بل في المسافة بين البيانات والقرار.</em> نغلقها ببناء <strong>إطار المؤشرات الصحيح أولًا</strong>، ثم ربط البيانات، ثم إظهارها بصيغة تستطيع القيادة التصرف بناءً عليها دون فريق بيانات في الغرفة.',
         pills=['Power BI', 'Tableau', 'Python', 'CBAHI KPIs'], href='/technology-services/#ab-03',
         art='art--violet', mark='Σ', cap='Power BI · Tableau', cap2='Python · SQL · EDW', cap2_ar='Python · SQL · EDW', slot='story/04-data', flip=True),
    dict(id='media', num='05', kicker='Media & Content Production', kicker_ar='الإعلام وإنتاج المحتوى',
         title='The Home of Media.', title_ar='موطن الإعلام.',
         lead='Where the brand system meets the camera — and every frame has <strong>a strategic reason to exist.</strong> Directed. Scripted. Bilingual. Brand-aligned.',
         lead_ar='حيث يلتقي نظام العلامة بالكاميرا — ولكل لقطة <strong>سبب استراتيجي لوجودها.</strong> مُخرَجة. مكتوبة. ثنائية اللغة. متوائمة مع العلامة.',
         body='Media without direction is expensive content nobody remembers. Every production starts with a creative brief and a <strong>bilingual script</strong> — <em>the message is designed before the camera turns on.</em> Brand systems need to live in motion, not just in guidelines PDFs.',
         body_ar='الإعلام بلا إخراج محتوى مكلف لا يتذكره أحد. كل إنتاج يبدأ بموجز إبداعي و<strong>نص ثنائي اللغة</strong> — <em>الرسالة تُصمَّم قبل أن تدور الكاميرا.</em> أنظمة العلامة يجب أن تعيش في الحركة، لا في ملفات الأدلة فقط.',
         pills=['Art Direction', 'Video', 'Photography', 'Voice-over'], href='/creative-services/#ma-08',
         art='art--pink', mark='🎬', cap='5+ Years Direction', cap2='Photography · Video · Voice-over', cap2_ar='تصوير · فيديو · تعليق صوتي', slot='story/05-media', flip=False),
]


def chapter(c):
    pills = ''.join(f'<span class="pill">{esc(p)}</span>' for p in c['pills'])
    art = f'''
          <div class="art art--wide {c['art']}" data-slot="{c['slot']}" aria-hidden="true">
            <span class="art__mark">{c['mark']}</span>
            <span class="art__cap">{esc(c['cap'])}</span>
            <span class="art__cap2" data-ar="{esc(c['cap2_ar'])}">{esc(c['cap2'])}</span>
          </div>'''
    text = f'''
          <div>
            <p class="kicker"><span class="kicker__num">{c['num']}</span><span data-ar="{esc('الفصل ' + c['num'] + ' · ' + c['kicker_ar'])}">Chapter {c['num']} · {esc(c['kicker'])}</span></p>
            <h2 class="section__title" id="ch-{c['id']}-title" data-ar="{esc(c['title_ar'])}">{esc(c['title'])}</h2>
            <p class="section__lead" data-ar-html="{esc(c['lead_ar'])}">{c['lead']}</p>
            <p data-ar-html="{esc(c['body_ar'])}">{c['body']}</p>
            <div class="pill-list" style="margin-top:16px">{pills}</div>
            <p style="margin-top:18px"><a class="text-link" href="{c['href']}"><span data-ar="اقرأ الفصل كاملًا ←">Read the full chapter →</span>{icon('arrow')}</a></p>
          </div>'''
    cols = (art + text) if c['flip'] else (text + art)
    return f'''
      <section class="section container section--flush-top chapter" id="{c['id']}" aria-labelledby="ch-{c['id']}-title">
        <div class="grid grid--2 grid--center" data-reveal>{cols}
        </div>
      </section>'''


def build():
    nav = ''.join(f'<a href="#{c["id"]}" data-ar="{esc(c["kicker_ar"].split(" و")[0] if False else c["kicker_ar"])}">{esc(c["kicker"])}</a>' for c in CHAPTERS)
    cards = ''.join(f'''
          <a class="card glass tile tile--mini" href="#{c['id']}" data-reveal style="--d:{i * .06:.2f}s"><span class="art__mark" style="font-size:28px">{c['mark']}</span><h3 data-ar="{esc(c['kicker_ar'])}">{esc(c['kicker'])}</h3></a>''' for i, c in enumerate(CHAPTERS))
    body = f'''
      <!-- ░░ Hero ░░ -->
      <section class="phero container phero--center" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('About', 'من نحن', '/about/'), ('Our Story', 'قصتنا', None)])}
        <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="Code &amp; Canvas · تأسس 2024 · السعودية + مصر">Code &amp; Canvas · Est. 2024 · KSA + Egypt</span></span>
        <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s"><span data-ar="قصتنا">Our Story</span><span class="grad-text">+</span></h1>
        <p class="hero__lead" data-reveal style="--d:.16s" data-ar-html="كل مشروع سلّمناه، وكل نظام صممناه، وكل علامة صغناها — &lt;strong&gt;يروي قصة واحدة متصلة.&lt;/strong&gt; هكذا وصلنا إلى هنا، ولهذا بنيناها بهذه الطريقة.">Every engagement we've delivered, every system we've architected, every brand we've shaped — <strong>tells one continuous story.</strong> This is how we got here, and why we built it this way.</p>
        <p class="phero__hint" data-reveal style="--d:.22s">{icon('arrowDown')}<span data-ar="مرّر لاستكشاف الفصول">Scroll to explore the chapters</span></p>
        <nav class="subnav" aria-label="Chapters" data-ar-label="الفصول" data-reveal style="--d:.26s">{nav}</nav>
      </section>

      <!-- ░░ Intro ░░ -->
      <section class="section container section--tight" aria-labelledby="intro-title">
        <div class="head-split">
          <header class="section__head" data-reveal>
            <h2 class="section__title" id="intro-title"><span data-ar="لنبدأ">Let's Begin</span><br /><span class="grad-text" data-ar="في صياغة قصتنا.">Crafting Our Story.</span></h2>
          </header>
          <div class="head-aside" data-reveal style="--d:.12s">
            <p data-ar-html="لم نبدأ بقائمة خدمات. بدأنا بقناعة — أن &lt;strong&gt;تطوير الأعمال، حين يُمارَس كما ينبغي، يحتاج مهندسًا وفنانًا معًا.&lt;/strong&gt; واحد يرسم النظام، وآخر يشكّل كيف يراه العالم.">We didn't start with a service menu. We started with a conviction — that <strong>business development, done properly, requires both an architect and an artist.</strong> One to map the system. One to shape how the world sees it.</p>
            <p data-ar="الفصول أدناه تتتبّع كل مسار بنيناه. ليست محفظة مخرجات — بل سجل لكيف نفكر وما نهتم به والمعيار الذي نلتزم به.">The chapters below trace each track we've built. Not a portfolio of deliverables — a record of how we think, what we care about, and the standard we hold ourselves to.</p>
          </div>
        </div>
        <div class="grid grid--5">{cards}
        </div>
      </section>

      {''.join(chapter(c) for c in CHAPTERS)}

      <!-- ░░ Outro ░░ -->
      <section class="section container section--tight" aria-labelledby="outro-title">
        <div class="callout glass glass--deep" data-reveal>
          <div>
            <p class="kicker"><span data-ar="هذه هي القصة — حتى الآن.">That's the story — for now.</span></p>
            <h3 id="outro-title"><span data-ar="نأمل أن تكون قد استمتعت">Hope you enjoyed</span> <span class="grad-text" data-ar="بالرحلة.">the journey.</span></h3>
            <p data-ar="خمسة مسارات. مؤسسان. انضباط واحد مشترك — أن كل مشروع، أيًّا كانت فئته، يجب أن يحقق نتيجة أعمال قابلة للتتبع. إن رأيت مشكلتك في مكان ما من هذه الصفحات، فلنتحدث.">Five tracks. Two founders. One shared discipline — that every engagement, regardless of category, must deliver a traceable business outcome. If you see your problem somewhere in these pages, let's talk.</p>
          </div>
          <div class="callout__actions">
            {btn('Start a Conversation', 'ابدأ محادثة', '/contact/')}
            <a class="text-link" href="/services/"><span data-ar="استكشف كل الخدمات ←">Explore All Services →</span></a>
            <a class="text-link" href="https://wa.me/966545520750" target="_blank" rel="noopener">{icon('chat')}<span>💬 WhatsApp</span></a>
          </div>
        </div>
      </section>

      {closing('HOPE YOU HAVE ENJOYED OUR JOURNEY', 'نأمل أن تكون قد استمتعت برحلتنا',
               '<span data-ar="ما الخدمة التي لفتت انتباهك">What service appealed to you</span><br /><span class="grad-text" data-ar="أو التي يمكننا تقديمها لك؟">or that we could provide for you?</span>',
               'Tell us where your problem sits — brand, technology, healthcare, data, or media — and we’ll point you to the right engagement.',
               'أخبرنا أين تقع مشكلتك — هوية أو تقنية أو رعاية صحية أو بيانات أو إعلام — وسنوجّهك إلى المشروع المناسب.',
               [btn('Contact', 'تواصل معنا', '/contact/'), btn('Services', 'الخدمات', '/services/', 'glass', 'arrow')])}
'''
    return [page('/our-story/', title='Our Story — Code & Canvas', title_ar='قصتنا — Code & Canvas',
                 desc='Five tracks, two founders, one shared discipline. The story of Code & Canvas across architecture, brand identity, healthcare, data, and media — and why we built it this way.',
                 desc_ar='خمسة مسارات ومؤسسان وانضباط واحد مشترك. قصة Code & Canvas عبر العمارة وهوية العلامة والرعاية الصحية والبيانات والإعلام — ولماذا بنيناها بهذه الطريقة.',
                 nav='about', body=body)]
