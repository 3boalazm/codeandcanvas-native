# -*- coding: utf-8 -*-
"""/methodology/ — live copy of codeandcanvas.net/methodology/."""
from h import esc, icon, crumbs, closing, btn, page, sec_head, steps3, facts

PHASES = [
    ('01', 'Foundation', 'الأساس', 'Discovery & Business Goals', 'الاستكشاف وأهداف الأعمال',
     'We start with the Business Motivation Model — mapping your vision, goals, strategies, and tactics before a single design decision is made. This produces a traceable chain from commercial intent to deliverable scope. Nothing is assumed; everything is confirmed in writing.',
     'نبدأ بنموذج دوافع الأعمال — نرسم رؤيتك وأهدافك واستراتيجياتك وتكتيكاتك قبل أي قرار تصميمي. ينتج عن ذلك سلسلة قابلة للتتبع من النية التجارية إلى نطاق التسليم. لا شيء يُفترض؛ كل شيء يُؤكَّد كتابةً.',
     ['BMM', 'Stakeholder Workshop', 'Goals Map']),
    ('02', 'Alignment', 'المواءمة', 'Kickoff + Engagement Brief', 'الانطلاق + موجز المشروع',
     'Formal scope confirmation, stakeholder alignment, and engagement brief sign-off. The brief defines what success looks like, what is out of scope, and how decisions will be made. First milestone payment is triggered here.',
     'تأكيد رسمي للنطاق ومواءمة أصحاب المصلحة واعتماد موجز المشروع. يحدد الموجز شكل النجاح وما هو خارج النطاق وكيف تُتخذ القرارات. هنا تُستحق دفعة المعلم الأول.',
     ['Engagement Brief', 'Scope Matrix', 'RACI']),
    ('03', 'Diagnosis', 'التشخيص', 'Capability Research', 'بحث القدرات',
     'Value stream mapping and capability heatmap — identifying what\'s broken, missing, or misaligned with your commercial objectives. This is the diagnostic layer that makes every downstream decision defensible, not intuitive.',
     'رسم تدفق القيمة وخريطة حرارية للقدرات — لتحديد ما هو معطّل أو مفقود أو غير متوائم مع أهدافك التجارية. هذه هي طبقة التشخيص التي تجعل كل قرار لاحق قابلًا للدفاع عنه لا حدسيًا.',
     ['Capability Map', 'Value Stream Analysis', 'Heatmap']),
    ('04', 'Architecture', 'العمارة', 'Strategy & Target State Design', 'الاستراتيجية وتصميم الوضع المستهدف',
     'TOGAF ADM-grounded target state design. Business-to-Technology Alignment Matrix produced — linking every strategic objective to a capability, technology asset, or data initiative. For brand engagements: strategic platform, positioning, and brand architecture.',
     'تصميم الوضع المستهدف المرتكز على TOGAF ADM. إنتاج مصفوفة مواءمة الأعمال مع التقنية — تربط كل هدف استراتيجي بقدرة أو أصل تقني أو مبادرة بيانات. ولمشاريع العلامة: المنصة الاستراتيجية والتموضع وعمارة العلامة.',
     ['TOGAF ADM', 'ArchiMate', 'Alignment Matrix', 'Brand Platform']),
    ('05', 'Creation', 'الابتكار', 'Concept Development', 'تطوير المفهوم',
     'Concepts aligned to strategy — not to aesthetics or personal preference. Brand concepts are evaluated against the strategic platform. Architecture options are evaluated against the capability model. Analytics models are evaluated against business decisions they must enable.',
     'مفاهيم متوائمة مع الاستراتيجية — لا مع الجماليات أو التفضيل الشخصي. تُقيَّم مفاهيم العلامة مقابل المنصة الاستراتيجية، وخيارات العمارة مقابل نموذج القدرات، ونماذج التحليلات مقابل قرارات الأعمال التي يجب أن تمكّنها.',
     ['Brand Concepts', 'Architecture Options', 'Analytics Models']),
    ('06', 'Production', 'الإنتاج', 'Design & Build', 'التصميم والبناء',
     'Full production — visual identity systems, architecture documentation, dashboard builds, or digital product development. Every output is traceable to a business requirement established in phases 1–5. No scope creep; no undocumented additions.',
     'إنتاج كامل — منظومات هوية بصرية أو وثائق معمارية أو بناء لوحات مؤشرات أو تطوير منتجات رقمية. كل مخرج قابل للتتبع إلى متطلب عمل حُدد في المراحل 1–5. لا توسّع في النطاق ولا إضافات غير موثقة.',
     ['Figma', 'Adobe Suite', 'Sparx EA', 'Power BI']),
    ('07', 'Validation', 'التحقق', 'Validation & Refinement', 'التحقق والصقل',
     'Structured review cycle with defined revision scope. Client sign-off gate before final delivery. Revisions are tracked against the original brief — changes to scope are documented and, if significant, trigger a scope amendment. Second milestone payment is triggered at sign-off.',
     'دورة مراجعة منظمة بنطاق تعديل محدد. بوابة اعتماد العميل قبل التسليم النهائي. تُتتبّع التعديلات مقابل الموجز الأصلي — تُوثَّق تغييرات النطاق، وإن كانت جوهرية تستدعي تعديلًا في النطاق. تُستحق دفعة المعلم الثاني عند الاعتماد.',
     ['Revision Rounds', 'Sign-off Gate', 'Scope Amendment']),
    ('08', 'Handover', 'التسليم', 'Launch & Embed', 'الإطلاق والترسيخ',
     'Deployment, handover documentation, and post-launch support where applicable. File release is conditional on full settlement. For EA and advisory engagements: implementation oversight is available as a separate retainer.',
     'النشر ووثائق التسليم ودعم ما بعد الإطلاق حيثما ينطبق. تسليم الملفات مشروط بالسداد الكامل. ولمشاريع العمارة المؤسسية والاستشارات: الإشراف على التنفيذ متاح كاتفاق منفصل.',
     ['Handover Pack', 'Post-Launch Support', 'Implementation Oversight']),
]

# Business-to-Technology Alignment Matrix (● primary · ◐ supporting · ○ indirect)
MATRIX = [
    ('Growth & Market Entry', 'النمو ودخول السوق', '●', '◐', '◐', '●'),
    ('Operational Efficiency', 'الكفاءة التشغيلية', '○', '●', '●', '●'),
    ('Digital Credibility', 'المصداقية الرقمية', '●', '●', '○', '◐'),
    ('Regulatory Compliance', 'الامتثال التنظيمي', '◐', '●', '◐', '●'),
    ('Strategic Insight', 'الرؤية الاستراتيجية', '○', '◐', '●', '◐'),
]


def build():
    phases = steps3([
        (n, f'{ten} — {pen}', f'{tar} — {par}', den, dar, ' · '.join(tags), ' · '.join(tags))
        for n, pen, par, ten, tar, den, dar, tags in PHASES])
    rows = ''.join(f'''
              <tr><th scope="row" data-ar="{esc(ar)}">{esc(en)}</th><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>''' for en, ar, a, b, c, d in MATRIX)

    body = f'''
      <!-- ░░ Hero ░░ -->
      <section class="phero container phero--left" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('About', 'من نحن', '/about/'), ('Methodology', 'المنهجية', None)])}
        <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="منهجيتنا">Our Methodology</span></span>
        <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s"><span data-ar="مواءمة الأعمال مع الأصول.">Business-Asset Alignment.</span><br /><span class="grad-text" data-ar="لا مجرد تسليم.">Not just delivery.</span></h1>
        <p class="hero__lead" data-reveal style="--d:.16s" data-ar="معظم المشاريع تسلّم مخرجات. مشاريعنا تسلّم مواءمة — رابطًا قابلًا للتتبع بين أهدافك وقدراتك وتقنيتك وبياناتك. كل مرحلة مقصودة. لا يُبنى شيء بلا سبب عمل.">Most engagements deliver outputs. Ours deliver alignment — a traceable connection between your goals, capabilities, technology, and data. Every phase is intentional. Nothing is built without a business reason.</p>
        <div class="hero__ctas" data-reveal style="--d:.24s">{btn('Book a 30-min call', 'احجز مكالمة 30 دقيقة', '/contact/#book')}{btn('See the 8 stages', 'استعرض المراحل الثماني', '#stages', 'glass', 'arrowDown')}</div>
      </section>

      <!-- ░░ At a glance ░░ -->
      <section class="section container section--tight" aria-label="The methodology at a glance" data-ar-label="المنهجية في أرقام">
        {facts([('Stages in every engagement', 'مرحلة في كل مشروع', '8', True),
                ('Diagnostic layers before any build', 'طبقتا تشخيص قبل أي بناء', '2', True),
                ('Stages with a named deliverable', 'مرحلة لها مخرج مسمّى', '8', True),
                ('Productized services on this process', 'خدمة مُنتجة تعمل بهذه العملية', '23', True)])}
      </section>

      <!-- ░░ 8 stages ░░ -->
      <section class="section container section--tight" id="stages" aria-labelledby="stages-title">
        {sec_head('01', 'THE PROCESS', 'العملية',
                  '<span id="stages-title" data-ar="ثماني مراحل.">Eight stages.</span> <span class="grad-text" data-ar="في كل مشروع.">Every engagement.</span>',
                  'One process runs every engagement, whichever track owns it. Each stage ends with a named deliverable you keep — no stage is «internal work» you never see.',
                  'عملية واحدة تدير كل مشروع أيًّا كان مساره. كل مرحلة تنتهي بمخرج مسمّى تحتفظ به — لا مرحلة «عمل داخلي» لا تراها.')}
        {phases}
      </section>

      <!-- ░░ Diagnostic layers ░░ -->
      <section class="section container section--flush-top" id="layers" aria-labelledby="layers-title">
        {sec_head('02', 'DIAGNOSIS', 'التشخيص',
                  '<span id="layers-title" data-ar="الغايات أولًا.">Ends first.</span> <span class="grad-text" data-ar="ثم الأصول.">Then assets.</span>',
                  'Two diagnostic layers decide everything that follows: what you are trying to achieve, and which assets can actually achieve it.',
                  'طبقتان تشخيصيتان تحدّدان كل ما يلي: ما تسعى إلى تحقيقه، وأي الأصول قادرة على تحقيقه فعلًا.')}
        <div class="grid grid--2">
          <article class="panel tier" data-reveal>
            <p class="tier__code" data-ar="نموذج دوافع الأعمال (BMM)">Business Motivation Model (BMM)</p>
            <h3 data-ar="نبدأ بالغايات لا بالوسائل.">We start with ends, not means.</h3>
            <p data-ar-html="قبل أي عمل تصميمي أو معماري، نرسم &lt;strong&gt;أهداف عملك ← استراتيجياتك ← تكتيكاتك ← قدراتك&lt;/strong&gt; باستخدام نموذج دوافع الأعمال. ينتج عن ذلك سلسلة قابلة للتتبع — من الرؤية وصولًا إلى القدرة أو عنصر العلامة المحدد الذي يحققها. لا يُبنى شيء بلا سبب عمل.">Before any design or architecture work begins, we map your <strong>business goals → strategies → tactics → capabilities</strong> using the Business Motivation Model. This produces a traceable chain — from vision down to the specific capability or brand element that delivers it. Nothing is built without a business reason.</p>
          </article>
          <article class="panel tier" data-reveal style="--d:.08s">
            <p class="tier__code" data-ar="تدفق القيمة + رسم القدرات">Value Stream + Capability Mapping</p>
            <h3 data-ar="ثم نربط تلك الغايات بأصولك.">Then we connect those ends to your assets.</h3>
            <p data-ar-html="نبني &lt;strong&gt;خرائط قدرات الأعمال&lt;/strong&gt; ونوائمها مع تدفقات القيمة — لتحديد أي القدرات معطّلة أو مفقودة أو غير متوائمة مع أهدافك التجارية. هذه هي طبقة التشخيص التي تجعل كل قرار لاحق قابلًا للدفاع عنه لا حدسيًا.">We construct <strong>business capability maps</strong> and align them to value streams — identifying which capabilities are broken, missing, or misaligned with your commercial objectives. This is the diagnostic layer that makes every downstream decision defensible, not intuitive.</p>
          </article>
        </div>
      </section>

      <!-- ░░ Matrix ░░ -->
      <section class="section container section--flush-top" id="matrix" aria-labelledby="matrix-title">
        {sec_head('03', 'TRACEABILITY', 'التتبع',
                  '<span id="matrix-title" data-ar="لتعرف دائمًا">So you always know</span> <span class="grad-text" data-ar="لماذا اتُّخذ القرار.">why a decision was made.</span>',
                  'A traceability matrix linking business goals to capabilities, technology assets, and transformation initiatives. Every engagement produces a version of this — so you always know why a decision was made.',
                  'مصفوفة تتبّع تربط أهداف الأعمال بالقدرات والأصول التقنية ومبادرات التحول. كل مشروع ينتج نسخة منها — لتعرف دائمًا سبب كل قرار.')}
        <div class="tbl-wrap panel" data-reveal>
          <table class="matrix">
            <thead><tr><th scope="col" data-ar="هدف العمل">Business Goal</th><th scope="col" data-ar="قدرة العلامة">Brand Capability</th><th scope="col" data-ar="الأصل التقني">Technology Asset</th><th scope="col" data-ar="البيانات / التحليلات">Data / Analytics</th><th scope="col" data-ar="التحول">Transformation</th></tr></thead>
            <tbody>{rows}
            </tbody>
          </table>
          <p class="matrix__legend"><span>● <span data-ar="محرك أساسي">Primary driver</span></span><span>◐ <span data-ar="داعم">Supporting</span></span><span>○ <span data-ar="غير مباشر">Indirect</span></span></p>
        </div>
      </section>

      <!-- ░░ Payment + CTA ░░ -->
      <section class="section container section--tight" aria-labelledby="cta-title">
        <div class="notice notice--violet" data-reveal>{icon('wallet')}<p data-ar-html="&lt;strong&gt;الدفع مرتبط بالمعالم لا بالساعات.&lt;/strong&gt; تُطلق المرحلة التالية بعد اعتماد مخرج المرحلة السابقة، وتسليم الملفات مشروط بالسداد الكامل. جدول المعالم الكامل ونسبه منشور في &lt;a href=&quot;/pricing-faq/#how-we-charge&quot;&gt;الأسعار وشروط الدفع&lt;/a&gt;."><strong>Payment follows milestones, not hours.</strong> The next stage starts when the previous stage's deliverable is signed off, and file release is conditional on full settlement. The full schedule and percentages are published in <a href="/pricing-faq/#how-we-charge">pricing &amp; payment terms</a>.</p></div>
        <div class="callout panel" data-reveal style="margin-top:18px">
          <div>
            <h3 id="cta-title" data-ar="تريد رؤية المنهجية مطبّقة؟">Want to see the methodology applied?</h3>
            <p data-ar="احجز مكالمة استكشافية مدتها 30 دقيقة. سنشرح لك كيف تنطبق العملية ذات المراحل الثماني على مشروعك تحديدًا — ونعطيك صورة واضحة عن شكل المخرجات.">Book a 30-minute discovery call. We'll walk you through how the 8-stage process applies to your specific engagement — and give you a clear picture of what the output looks like.</p>
          </div>
          <div class="callout__actions">{btn('Book a Discovery Call', 'احجز مكالمة استكشافية', '/contact/#book')}<a class="text-link" href="/pricing-faq/"><span data-ar="الأسعار والأسئلة الشائعة ←">Pricing &amp; FAQ →</span></a></div>
        </div>
      </section>

      {closing('THE HOME OF INNOVATION', 'موطن الابتكار',
               '<span data-ar="لنحدد خطوتك التالية.">Let’s scope your next step.</span>',
               'Start with our story, or book an appointment and bring the business problem — we’ll bring the structure.',
               'ابدأ بقصتنا، أو احجز موعدًا وأحضر مشكلة العمل — ونحن نُحضر الهيكل.',
               [btn('Get Started', 'ابدأ الآن', '/our-story/'), btn('Book an Appointment', 'احجز موعدًا', '/contact/#book', 'glass')])}
'''
    return [page('/methodology/', title='Methodology — Code & Canvas', title_ar='المنهجية — Code & Canvas',
                 desc='Business-Asset Alignment, not just delivery. The 8-stage Code & Canvas methodology — BMM discovery, engagement brief, capability research, TOGAF ADM target state, concept, build, validation, and launch — plus the Business-to-Technology Alignment Matrix.',
                 desc_ar='مواءمة الأعمال مع الأصول لا مجرد تسليم. منهجية Code & Canvas ذات المراحل الثماني — استكشاف BMM وموجز المشروع وبحث القدرات والوضع المستهدف وفق TOGAF ADM والمفهوم والبناء والتحقق والإطلاق — إضافة إلى مصفوفة مواءمة الأعمال مع التقنية.',
                 nav='about', body=body)]
