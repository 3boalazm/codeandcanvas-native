# -*- coding: utf-8 -*-
"""/our-story/ — the five practices the studio grew out of, told as chapters.
v3 layout: numbered heads, mono chapter plates, dense index of the chapters."""
from h import esc, icon, crumbs, closing, btn, page, sec_head, facts

CHAPTERS = [
    dict(id='architecture', num='01', accent='tech', kicker='Technology & Architecture', kicker_ar='التقنية والعمارة',
         title='Where a technology decision starts from a business goal.', title_ar='حيث يبدأ القرار التقني من هدف عمل.',
         lead='Architecture work traced back to commercial intent — <strong>not to a specification document.</strong> TOGAF-anchored. NORA-aligned. Vision 2030-aware.',
         lead_ar='عمل معماري يُتتبّع فيه كل قرار إلى النية التجارية — <strong>لا إلى وثيقة مواصفات.</strong> مرتكز على TOGAF. متوائم مع NORA. واعٍ برؤية 2030.',
         body='Ahmed builds enterprise architectures in KSA grounded in <strong>TOGAF, ArchiMate and NORA</strong> — translating a CIO\'s problem into a traceable decision tree a board can approve and a developer can implement. Every engagement produces a <em>Business-to-Technology Alignment Matrix.</em>',
         body_ar='يبني أحمد عمارات مؤسسية في السعودية مرتكزة على <strong>TOGAF و ArchiMate و NORA</strong> — محوّلًا مشكلة مدير تقنية المعلومات إلى شجرة قرارات قابلة للتتبع يعتمدها مجلس الإدارة وينفذها المطوّر. كل مشروع ينتج <em>مصفوفة مواءمة الأعمال مع التقنية.</em>',
         pills=['TOGAF', 'NORA', 'ArchiMate 3.1', 'Vision 2030'], href='/technology-services/',
         cap='AB · Enterprise Architecture', cap2='Enterprise Architecture Practice', cap2_ar='ممارسة العمارة المؤسسية', flip=False),
    dict(id='identity', num='02', accent='brand', kicker='Brand Identity & Creative', kicker_ar='هوية العلامة والإبداع',
         title='Where a logo becomes a system a team can run.', title_ar='حيث يصبح الشعار نظامًا يستطيع الفريق تشغيله.',
         lead='Where a logo becomes a system, a system becomes a language, and a language <strong>becomes the thing clients recognise before they read a word.</strong>',
         lead_ar='حيث يصبح الشعار نظامًا، والنظام لغة، واللغة <strong>هي ما يتعرّف عليه العملاء قبل أن يقرأوا كلمة واحدة.</strong>',
         body='Mustafa treats brand work as <strong>commercial work</strong> — every design decision either supports a revenue outcome or gets cut. The four-act methodology (Discovery, Strategy, Concept, Refine) exists because <em>skipping strategy gives you a logo, not a brand.</em>',
         body_ar='يتعامل مصطفى مع عمل العلامة بوصفه <strong>عملًا تجاريًا</strong> — كل قرار تصميمي إما يدعم نتيجة إيرادية أو يُستبعد. منهجية الفصول الأربعة (الاستكشاف، الاستراتيجية، المفهوم، الصقل) موجودة لأن <em>تخطّي الاستراتيجية يعطيك شعارًا لا علامة.</em>',
         pills=['Brand Strategy', 'Bilingual AR/EN', 'Design Systems', 'Figma'], href='/creative-services/',
         cap='MA · Brand Systems', cap2='Brand systems built across sectors', cap2_ar='أنظمة علامة عبر قطاعات مختلفة', flip=True),
    dict(id='healthcare', num='03', accent='health', kicker='Healthcare Vertical', kicker_ar='قطاع الرعاية الصحية',
         title='Where clinical context is built in from day one.', title_ar='حيث يُبنى السياق السريري من اليوم الأول.',
         lead='Clinical context from the first call — not briefed in on the first call. <strong>CPHIMS. EMRAM. CBAHI. NORA.</strong> Not listed frameworks. Worked credentials.',
         lead_ar='سياق سريري من أول مكالمة — لا شرح يُقدَّم في أول مكالمة. <strong>CPHIMS. EMRAM. CBAHI. NORA.</strong> ليست أطرًا مُدرجة بل اعتمادات يمارسها الفريق.',
         body='Healthcare IT is where a wrong decision costs most — a misaligned HIS is not a licence you cancel, it is years of workarounds and manual reporting. We operate <em>inside</em> the ecosystem: clinical workflow context in every technology recommendation, CBAHI-aware design in every visual decision.',
         body_ar='تقنية الرعاية الصحية هي حيث يكلّف القرار الخاطئ أكثر — النظام غير المتوائم ليس ترخيصًا يُلغى، بل سنوات من الحلول المؤقتة والتقارير اليدوية. نعمل <em>داخل</em> المنظومة: سياق مسارات العمل السريرية في كل توصية تقنية، وتصميم واعٍ بـ CBAHI في كل قرار بصري.',
         pills=['CPHIMS', 'HIMSS EMRAM', 'CBAHI', 'NORA'], href='/healthcare/',
         cap='HC · Clinical Architecture', cap2='CBAHI · NORA · HIMSS', cap2_ar='CBAHI · NORA · HIMSS', flip=False),
    dict(id='data', num='04', accent='data', kicker='Data & Analytics', kicker_ar='البيانات والتحليلات',
         title='Where data stops being a reporting burden.', title_ar='حيث تتوقف البيانات عن كونها عبء تقارير.',
         lead='Where operational data starts being <strong>the thing that tells leadership what to do next.</strong>',
         lead_ar='حيث تبدأ البيانات التشغيلية في أن تكون <strong>ما يخبر القيادة بالخطوة التالية.</strong>',
         body='The problem is rarely the data — <em>it is the distance between the data and the decision.</em> We close it by building <strong>the right KPI framework first</strong>, then connecting the data, then making it visible in a format leadership can act on without a data team in the room.',
         body_ar='نادرًا ما تكون المشكلة في البيانات — <em>بل في المسافة بين البيانات والقرار.</em> نغلقها ببناء <strong>إطار المؤشرات الصحيح أولًا</strong>، ثم ربط البيانات، ثم إظهارها بصيغة تستطيع القيادة التصرف بناءً عليها دون فريق بيانات في الغرفة.',
         pills=['Power BI', 'Tableau', 'Python', 'CBAHI KPIs'], href='/technology-services/#ab-03',
         cap='AB · Data & Analytics', cap2='Power BI · Tableau · Python · EDW', cap2_ar='Power BI · Tableau · Python · EDW', flip=True),
    dict(id='media', num='05', accent='media', kicker='Media & Content Production', kicker_ar='الإعلام وإنتاج المحتوى',
         title='Where every frame has a strategic reason to exist.', title_ar='حيث لكل لقطة سبب استراتيجي لوجودها.',
         lead='Where the brand system meets the camera. <strong>Directed. Scripted. Bilingual. Brand-aligned.</strong>',
         lead_ar='حيث يلتقي نظام العلامة بالكاميرا. <strong>مُخرَجة. مكتوبة. ثنائية اللغة. متوائمة مع العلامة.</strong>',
         body='Media without direction is expensive content nobody remembers. Every production starts with a creative brief and a <strong>bilingual script</strong> — <em>the message is designed before the camera turns on.</em> Brand systems need to live in motion, not only in guidelines PDFs.',
         body_ar='الإعلام بلا إخراج محتوى مكلف لا يتذكره أحد. كل إنتاج يبدأ بموجز إبداعي و<strong>نص ثنائي اللغة</strong> — <em>الرسالة تُصمَّم قبل أن تدور الكاميرا.</em> أنظمة العلامة يجب أن تعيش في الحركة، لا في ملفات الأدلة فقط.',
         pills=['Art Direction', 'Video', 'Photography', 'Voice-over'], href='/creative-services/#ma-08',
         cap='MA · Production', cap2='Photography · Video · Voice-over', cap2_ar='تصوير · فيديو · تعليق صوتي', flip=False),
]


def plate(c):
    """Mono chapter plate: solid panel, big number, no illustration pretence."""
    return f'''
          <div class="story-plate story-plate--{c['accent']}" aria-hidden="true">
            <span class="story-plate__no">{c['num']}</span>
            <span class="story-plate__cap">{esc(c['cap'])}</span>
            <span class="story-plate__cap2" data-ar="{esc(c['cap2_ar'])}">{esc(c['cap2'])}</span>
          </div>'''


def chapter(c):
    pills = ''.join(f'<span class="tag-soft">{esc(p)}</span>' for p in c['pills'])
    text = f'''
          <div class="story-body">
            <h2 id="ch-{c['id']}-title" data-ar="{esc(c['title_ar'])}">{esc(c['title'])}</h2>
            <p class="lead" data-ar-html="{esc(c['lead_ar'])}">{c['lead']}</p>
            <p data-ar-html="{esc(c['body_ar'])}">{c['body']}</p>
            <div class="who__creds" style="margin-top:4px">{pills}</div>
            <p style="margin-top:6px"><a class="text-link" href="{c['href']}"><span data-ar="اقرأ المسار كاملًا ←">Read the full track →</span>{icon('arrow')}</a></p>
          </div>'''
    cols = (text + plate(c)) if c['flip'] else (plate(c) + text)
    return f'''
      <section class="section container section--flush-top story-chapter" id="{c['id']}" aria-labelledby="ch-{c['id']}-title">
        <p class="kicker" data-reveal><span class="kicker__num">{c['num']}</span><span data-ar="{esc(c['kicker_ar'])}">{esc(c['kicker'])}</span></p>
        <div class="story-grid"{' data-reveal' if not c['flip'] else ''}>{cols}
        </div>
      </section>'''


def build():
    index = ''.join(f'''
          <a class="mini panel" href="#{c['id']}" data-reveal style="--d:{i * .05:.2f}s">
            <span class="mini__code">{c['num']}</span>
            <h3 data-ar="{esc(c['kicker_ar'])}">{esc(c['kicker'])}</h3>
            <p data-ar="{esc(c['cap2_ar'])}">{esc(c['cap2'])}</p>
          </a>''' for i, c in enumerate(CHAPTERS))

    body = f'''
      <!-- ░░ Hero ░░ -->
      <section class="phero container phero--left" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('About', 'من نحن', '/about/'), ('Our Story', 'قصتنا', None)])}
        <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="Code &amp; Canvas · تأسس 2024 · السعودية + مصر">Code &amp; Canvas · Est. 2024 · KSA + Egypt</span></span>
        <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s"><span data-ar="خمس ممارسات. مؤسسان.">Five practices. Two founders.</span><br /><span class="grad-text" data-ar="قصة واحدة متصلة.">One continuous story.</span></h1>
        <p class="hero__lead" data-reveal style="--d:.16s" data-ar-html="لم نبدأ بقائمة خدمات. بدأنا بقناعة — أن &lt;strong&gt;تطوير الأعمال، حين يُمارَس كما ينبغي، يحتاج مهندسًا وفنانًا معًا.&lt;/strong&gt; الفصول أدناه ليست محفظة مخرجات، بل سجل لكيف نفكر وما نلتزم به.">We did not start with a service menu. We started from one conviction — that <strong>business development, done properly, needs both an architect and an artist.</strong> The chapters below are not a portfolio; they are the record of how we think and what we hold ourselves to.</p>
        <div class="hero__ctas" data-reveal style="--d:.24s">{btn('Meet the founders', 'تعرّف على المؤسسين', '/team/', 'primary', 'arrow')}{btn('See the methodology', 'استعرض المنهجية', '/methodology/', 'glass')}</div>
      </section>

      <!-- ░░ At a glance ░░ -->
      <section class="section container section--tight" aria-label="The studio at a glance" data-ar-label="الاستوديو في أرقام">
        {facts([('Founded', 'التأسيس', '2024', True),
                ('Founders delivering the work', 'مؤسسان ينفّذان العمل', '2', True),
                ('Practices', 'ممارسات', '5', True),
                ('Productized services', 'خدمة مُنتجة', '23', True),
                ('Countries — KSA · Egypt', 'دولتان — السعودية · مصر', '2', True)])}
      </section>

      <!-- ░░ Chapters index ░░ -->
      <section class="section container section--flush-top" id="chapters" aria-labelledby="chapters-title">
        {sec_head('01', 'THE CHAPTERS', 'الفصول',
                  '<span id="chapters-title" data-ar="كل مسار بنيناه، ومن يقوده.">Every track we built, and who leads it.</span>',
                  'Each chapter below is a practice with a named owner, a published service list and a place to start. Nothing here is a service we would hand to a third party.',
                  'كل فصل أدناه ممارسة لها مالك مسمّى وقائمة خدمات منشورة ونقطة بداية. لا شيء هنا خدمة نمرّرها إلى طرف ثالث.',
                  aside=btn('Full service index', 'فهرس الخدمات الكامل', '/services/', 'glass'))}
        <div class="grid grid--3">{index}
        </div>
      </section>

      {''.join(chapter(c) for c in CHAPTERS)}

      <!-- ░░ Closing CTA ░░ -->
      {closing('ONE BRIEF, TWO DISCIPLINES', 'موجز واحد، تخصصان',
               '<span data-ar="إن رأيت مشكلتك في مكان ما من هذه الصفحات،">If you saw your problem somewhere in these chapters,</span> <span class="grad-text" data-ar="فلنتحدث.">let’s talk.</span>',
               'Twenty-three productized services across five practices, one published price list, and one shared brief. Start with the track that owns your decision.',
               'ثلاث وعشرون خدمة مُنتجة عبر خمس ممارسات، وقائمة أسعار منشورة، وموجز واحد مشترك. ابدأ بالمسار الذي يملك قرارك.',
               [btn('Contact', 'تواصل معنا', '/contact/'), btn('Pricing', 'الأسعار', '/pricing-faq/', 'glass', 'arrow')])}
'''
    return [page('/our-story/', title='Our Story — Code & Canvas', title_ar='قصتنا — Code & Canvas',
                 desc='Five practices, two founders, one shared discipline. How Code & Canvas grew across enterprise architecture, brand identity, healthcare, data and media — and who leads each track.',
                 desc_ar='خمس ممارسات ومؤسسان وانضباط واحد مشترك. كيف نمت Code & Canvas عبر العمارة المؤسسية وهوية العلامة والرعاية الصحية والبيانات والإعلام — ومن يقود كل مسار.',
                 nav='about', body=body)]
