# -*- coding: utf-8 -*-
"""/case-studies/ — Work: a method-first reading of the three shipped systems.

v3 architecture: each project is told as brief → constraints → our role →
approach → artifacts → status/evidence → next step, and each one states exactly
what can be published. No "proven results" claim without a measured source.
"""
from h import esc, icon, crumbs, closing, btn, page, sec_head, facts

PROJECTS = [
    dict(
        n='01', anchor='pharmacy-os',
        meta='Healthcare · Multi-tenant SaaS · 2024–2026', meta_ar='رعاية صحية · SaaS متعدد المستأجرين · 2024–2026',
        name_ar='صيدليتي', name='Pharmacy OS', client='Doctor Pharmacy', client_ar='صيدلية دكتور',
        brief='A pharmacy chain running point of sale, stock, prescriptions and finance in separate tools, with no single view of a shift or a branch.',
        brief_ar='سلسلة صيدليات تدير نقطة البيع والمخزون والروشتات والمالية في أدوات منفصلة، بلا صورة واحدة للوردية أو الفرع.',
        constraints=[
            'Arabic RTL as the primary interface, not a translated skin',
            'Multi-tenant from day one — branches must not see each other’s data',
            'Must work on the counter hardware already in the branches',
            'Pharmacy workflows: batch numbers, expiry and prescription linking',
        ],
        constraints_ar=[
            'العربية RTL كواجهة أساسية، لا طبقة مترجمة',
            'متعدد المستأجرين من اليوم الأول — لا يرى فرع بيانات فرع آخر',
            'يعمل على أجهزة الكاشير الموجودة بالفعل في الفروع',
            'مسارات صيدلية حقيقية: أرقام التشغيلات والصلاحية وربط الروشتات',
        ],
        role='Architecture and full-stack delivery by the studio — data model, multi-tenant boundaries, RTL interface system and the module rollout order.',
        role_ar='العمارة والتنفيذ الكامل من الاستوديو — نموذج البيانات وحدود تعدد المستأجرين ونظام الواجهة العربية وترتيب إطلاق الوحدات.',
        approach=[
            'Modelled the pharmacy day first: counter, shift, stock receipt, prescription, month-end',
            'One tenant-isolation rule enforced at the data layer, not in each screen',
            'Shipped in modules, each one usable the week it was delivered',
        ],
        approach_ar=[
            'نمذجة يوم الصيدلية أولًا: الكاشير، الوردية، استلام المخزون، الروشتة، إقفال الشهر',
            'قاعدة واحدة لعزل المستأجرين مُنفَّذة في طبقة البيانات لا في كل شاشة',
            'التسليم بوحدات، كل وحدة قابلة للاستخدام في الأسبوع الذي تُسلَّم فيه',
        ],
        artifacts=[
            ('14 modules shipped', 'Point of sale, invoicing, inventory and goods receipt, prescriptions, customer records, shifts, reports'),
            ('Multi-tenant data model', 'Tenant isolation, branch roll-ups and per-branch permissions'),
            ('Bilingual interface system', 'RTL-first components reused across every module'),
        ],
        artifacts_ar=[
            ('14 وحدة مُسلَّمة', 'نقطة البيع والفوترة والمخزون واستلام البضاعة والروشتات وسجلات العملاء والورديات والتقارير'),
            ('نموذج بيانات متعدد المستأجرين', 'عزل المستأجرين وتجميع الفروع والصلاحيات لكل فرع'),
            ('نظام واجهة ثنائي اللغة', 'مكوّنات RTL-first مُعاد استخدامها في كل الوحدات'),
        ],
        stack=['Next.js', 'NestJS', 'TypeScript', 'Prisma', 'Postgres', 'PWA'],
        status='Live product, private deployment', status_ar='منتج حي، نشر خاص',
        evidence='No public screenshots. Screens contain branch data, so any published view would need written client approval first.',
        evidence_ar='لا لقطات عامة. الشاشات تحتوي بيانات فروع، وأي عرض منشور يحتاج موافقة كتابية من العميل أولًا.',
        next='Discuss a similar build', next_ar='ناقش بناءً مشابهًا',
        art='pharmacy-os', alt_ar='رسم توضيحي لنطاق نظام الصيدليات — ليس لقطة شاشة',
    ),
    dict(
        n='02', anchor='zad',
        meta='PWA · Offline-first · Public project · 2026', meta_ar='تطبيق ويب · يعمل دون اتصال · مشروع عام · 2026',
        name_ar='زاد', name='Zad', client='Worship Companion', client_ar='رفيق العبادات',
        brief='A daily-use worship companion for the first ten days of Dhul-Hijjah — used in places with weak or no connectivity.',
        brief_ar='رفيق عبادة للاستخدام اليومي في عشر ذي الحجة — يُستخدم في أماكن ضعيفة الاتصال أو بلا اتصال.',
        constraints=[
            'Fully usable offline — the offline state is the normal state',
            'Bilingual Arabic/English with correct RTL presentation',
            'Readable type for Quranic text at phone sizes',
            'No account, no tracking, nothing to sign up for',
        ],
        constraints_ar=[
            'قابل للاستخدام دون اتصال بالكامل — حالة عدم الاتصال هي الحالة الطبيعية',
            'ثنائي اللغة عربي/إنجليزي مع عرض RTL صحيح',
            'خطوط مقروءة للنص القرآني على مقاسات الهاتف',
            'بلا حساب ولا تتبّع ولا تسجيل',
        ],
        role='Concept, interface design and front-end implementation, including the offline data strategy and type system.',
        role_ar='الفكرة وتصميم الواجهة وتنفيذ الواجهة الأمامية، بما في ذلك استراتيجية البيانات دون اتصال ونظام الخطوط.',
        approach=[
            'Data cached on first load; every core feature works with the radio off',
            'Arabic typography tested on a small screen before the language switch was built',
            'Gesture and thumb reach drove the layout more than the desktop comp',
        ],
        approach_ar=[
            'تخزين البيانات عند أول تحميل؛ كل الميزات الأساسية تعمل مع إيقاف الشبكة',
            'اختبار الخطوط العربية على شاشة صغيرة قبل بناء مبدّل اللغة',
            'حركة الإصبع ومدى الوصول بالإبهام حكما التخطيط أكثر من تصميم الشاشة الكبيرة',
        ],
        artifacts=[
            ('12 worship modules', 'Prayer times, Qibla, Quran, adhkar, tasbih, Ruqyah, Asmaa Allah, Ramadan, Hajj, kids section'),
            ('Offline-first data layer', 'Service worker and local storage — no network calls required for core reading'),
            ('Public release', 'Deployed publicly, open for anyone to use without an account'),
        ],
        artifacts_ar=[
            ('12 وحدة عبادات', 'مواقيت الصلاة والقبلة والمصحف والأذكار والتسبيح والرقية وأسماء الله ورمضان والحج وقسم الأطفال'),
            ('طبقة بيانات تعمل دون اتصال', 'Service worker وتخزين محلي — بلا طلبات شبكة للقراءة الأساسية'),
            ('إصدار عام', 'منشور للعامة، متاح للاستخدام دون حساب'),
        ],
        stack=['PWA', 'Service Worker', 'Vanilla JS', 'localStorage', 'Vercel'],
        status='Live and public', status_ar='حي ومتاح للعامة',
        evidence='The live app is the evidence — anyone can open it and use the offline state.',
        evidence_ar='التطبيق الحي هو الإثبات — يمكن لأي شخص فتحه واستخدام وضع عدم الاتصال.',
        link='https://zadullashr.vercel.app/', link_label='Open the live app ↗', link_label_ar='افتح التطبيق الحي ↗',
        next='Discuss a similar build', next_ar='ناقش بناءً مشابهًا',
        art='zad', alt_ar='رسم توضيحي لنطاق تطبيق زاد — ليس لقطة شاشة',
    ),
    dict(
        n='03', anchor='nile-pharma',
        meta='Pharma ERP · Internal system · 2026', meta_ar='ERP أدوية · نظام داخلي · 2026',
        name_ar='نايل فارما', name='Nile Pharma ERP', client='Nile Pharma, Food & Supplements', client_ar='النيل للأدوية والأغذية والمكملات',
        brief='A pharmaceutical distributor running the full sales cycle on paper and spreadsheets — including expiry-sensitive stock and rep incentives.',
        brief_ar='موزّع أدوية يدير دورة البيع الكاملة على الورق وجداول البيانات — بما يشمل المخزون الحساس للصلاحية وحوافز المناديب.',
        constraints=[
            'FEFO allocation is compulsory, not a best effort',
            'Consignment (amanah) stock must be tracked separately from owned stock',
            'Rep incentives calculated from actual collections, not invoices issued',
            'The team had to keep working during rollout — no downtime window',
        ],
        constraints_ar=[
            'تخصيص FEFO إلزامي وليس تفضيلًا',
            'مخزون الأمانة يُتتبع منفصلًا عن المخزون المملوك',
            'حوافز المناديب تُحسب من التحصيل الفعلي لا من الفواتير الصادرة',
            'الفريق يجب أن يواصل العمل أثناء الانتقال — لا نافذة توقف',
        ],
        role='Business analysis, system design and delivery of the ERP modules with the client’s operations team.',
        role_ar='تحليل الأعمال وتصميم النظام وتسليم وحدات ERP مع فريق العمليات لدى العميل.',
        approach=[
            'Mapped the sales cycle end to end with the reps before designing any screen',
            'FEFO enforced in the allocation engine so no screen can bypass it',
            'Incentive rules written down as formulas and reviewed with finance',
        ],
        approach_ar=[
            'رسم دورة البيع من البداية للنهاية مع المناديب قبل تصميم أي شاشة',
            'تطبيق FEFO في محرّك التخصيص حتى لا تتجاوزه أي شاشة',
            'قواعد الحوافز مكتوبة كمعادلات ومراجعة مع الإدارة المالية',
        ],
        artifacts=[
            ('10 ERP modules', 'Catalogue, inventory, consignment, FEFO sales orders, invoicing, collections, incentives'),
            ('Allocation engine', 'FEFO rules applied to every order, with an audit trail'),
            ('Incentive calculation', 'Rep ranking and payouts derived from collected amounts'),
        ],
        artifacts_ar=[
            ('10 وحدات ERP', 'الكتالوج والمخزون والأمانة وأوامر البيع FEFO والفوترة والتحصيل والحوافز'),
            ('محرّك التخصيص', 'قواعد FEFO مُطبَّقة على كل أمر مع مسار تدقيق'),
            ('حساب الحوافز', 'ترتيب المناديب والمستحقات مشتق من المبالغ المحصّلة'),
        ],
        stack=['React 18', 'RTL', 'IBM Plex Sans Arabic', 'FEFO logic'],
        status='Internal system — NDA', status_ar='نظام داخلي — اتفاقية سرية',
        evidence='Nothing can be published: commercial volumes, margins and rep data are all under NDA. What can be discussed on a call is the design approach, not the numbers.',
        evidence_ar='لا يمكن نشر أي شيء: الأحجام التجارية والهوامش وبيانات المناديب كلها تحت اتفاقية سرية. ما يمكن مناقشته في مكالمة هو منهج التصميم لا الأرقام.',
        next='Discuss a similar challenge', next_ar='ناقش تحديًا مشابهًا',
        art='nile-pharma-erp', alt_ar='رسم توضيحي لنطاق منصة ERP — ليس لقطة شاشة',
    ),
]


def project(p, i):
    flip = i % 2 == 1
    facts_list = [(f'0{j + 1}', f'0{j + 1}', '', False) for j in range(0)]
    constraints = ''.join(f'<li data-ar="{esc(a)}">{esc(e)}</li>' for e, a in zip(p['constraints'], p['constraints_ar']))
    approach = ''.join(f'<li data-ar="{esc(a)}">{esc(e)}</li>' for e, a in zip(p['approach'], p['approach_ar']))
    artifacts = ''.join(
        f'<div><b data-ar="{esc(a_ar)}">{a_en}</b><span data-ar="{esc(d_ar)}">{d_en}</span></div>'
        for (a_en, d_en), (a_ar, d_ar) in zip(p['artifacts'], p['artifacts_ar']))
    stack = ''.join(f'<span class="pill">{esc(s)}</span>' for s in p['stack'])
    if p.get('link'):
        action = f'<a class="btn btn--glass" href="{p["link"]}" target="_blank" rel="noopener"><span data-ar="{esc(p["link_label_ar"])}">{esc(p["link_label"])}</span>{icon("arrowUpRight", "flip")}</a>'
    else:
        action = f'<span class="tag-soft tag-soft--warn" data-ar="{esc(p["status_ar"])}">{esc(p["status"])}</span>'
    visual = f'''
          <figure class="case-visual">
            <img src="/assets/brand/work/{p['art']}.svg" width="960" height="600" loading="lazy" alt="{esc(p['name'])} — conceptual scope diagram, not a screenshot" data-ar-alt="{esc(p['alt_ar'])}" />
            <figcaption data-ar="رسم توضيحي مبني على النطاق الموثق للمشروع، وليس لقطة من واجهة المنتج ولا إثباتًا لنتيجة تجارية.">Conceptual illustration of the project’s documented scope — not a product screenshot and not evidence of a commercial outcome.</figcaption>
          </figure>'''
    text = f'''
          <div class="cs__text">
            <p class="sec-head__no"><b>{p['n']}</b><span data-ar="{esc(p['meta_ar'])}">{esc(p['meta'])}</span></p>
            <h2 class="cs__title" id="cs-{p['n']}-title"><span lang="ar" dir="rtl" data-ar="{esc(p['name_ar'])}">{esc(p['name_ar'])}</span> <span class="grad-text">{esc(p['name'])}</span></h2>
            <p class="person__tag" data-ar="{esc(p['client_ar'])}">{esc(p['client'])}</p>
            <p class="cs__brief" data-ar="{esc(p['brief_ar'])}">{esc(p['brief'])}</p>
            <div class="cs__block"><b data-ar="القيود">Constraints</b><ul class="svc-row__list">{constraints}</ul></div>
            <div class="cs__block"><b data-ar="دورنا">Our role</b><p data-ar="{esc(p['role_ar'])}">{esc(p['role'])}</p></div>
            <div class="cs__block"><b data-ar="المنهج">Approach</b><ul class="svc-row__list">{approach}</ul></div>
            <div class="cs__block"><b data-ar="المخرجات">Artifacts</b><div class="cs__artifacts">{artifacts}</div></div>
            <div class="pill-list" style="margin-top:16px">{stack}</div>
            <div class="cs__evidence">
              <b data-ar="حالة النشر والدليل">Publication status &amp; evidence</b>
              <p data-ar="{esc(p['evidence_ar'])}">{esc(p['evidence'])}</p>
              <div class="hero__ctas" style="margin-top:14px">{action}<a class="btn btn--primary" href="/contact/?inquiry=custom#message" data-track="service-inquiry" data-track-service="custom"><span data-ar="{esc(p['next_ar'])}">{esc(p['next'])}</span>{icon("arrowUpRight", "flip")}</a></div>
            </div>
          </div>'''
    return f'''
      <section class="section container work-case" id="{p['anchor']}" aria-labelledby="cs-{p['n']}-title">
        <span class="anchor-alias" id="project-{p['n']}" aria-hidden="true"></span>
        <div class="cs__grid" data-reveal>{(visual + text) if flip else (text + visual)}
        </div>
      </section>'''


def build():
    body = f'''
      <!-- ░░ Hero ░░ -->
      <section class="phero container phero--left" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('Work', 'أعمالنا', None)])}
        <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="ثلاثة أنظمة · 2024–2026 · عربية أولًا">Three systems · 2024–2026 · Arabic-first</span></span>
        <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s"><span data-ar="مشاريع حقيقية">Real projects,</span><br /><span class="grad-text" data-ar="وثائق نطاق لا شعارات.">documented scope — not badges.</span></h1>
        <p class="hero__lead" data-reveal style="--d:.16s" data-ar="كل مشروع أدناه مكتوب بالترتيب نفسه: الموجز، القيود، دورنا، المنهج، المخرجات، ثم ما يمكن نشره فعلًا وما لا يمكن. لن تجد هنا «نتائج مضمونة» أو لقطات شاشة لعميل لم يوافق على نشرها.">Every project below is written in the same order: brief, constraints, our role, approach, artifacts — then exactly what can be published and what cannot. You will not find “proven results” or screenshots from a client who has not approved publication.</p>
        <nav class="subnav container" aria-label="Projects" data-ar-label="المشاريع" data-reveal style="--d:.22s">{''.join(f'<a href="#{p["anchor"]}">{p["n"]} · <span data-ar="{esc(p["name_ar"])}">{esc(p["name"])}</span></a>' for p in PROJECTS)}</nav>
        {facts([('Projects on this page', 'مشاريع هذه الصفحة', '3', True), ('Publicly usable', 'متاح للاستخدام العام', '1', True),
                ('Under NDA', 'تحت اتفاقية سرية', '1', True), ('Concept diagrams', 'رسوم توضيحية', '3', True)])}
      </section>

      {''.join(project(p, i) for i, p in enumerate(PROJECTS))}

      <!-- ░░ What these cases do not claim ░░ -->
      <section class="section container section--tight" id="limits" aria-labelledby="lim-title">
        {sec_head('LIMITS', 'WHAT THIS SECTION DOES NOT CLAIM', 'ما لا تدّعيه هذه الصفحة',
                  '<span id="lim-title" data-ar="لا أرقام امتثال">No audited numbers,</span> <span class="grad-text" data-ar="ولا صور عميل.">no borrowed client imagery.</span>',
                  'Three honest limits, stated up front — so nobody has to discover them later.',
                  'ثلاثة حدود نقولها مسبقًا — حتى لا يكتشفها أحد لاحقًا.', center=False)}
        <div class="grid-3">
          <article class="panel mini" data-reveal><h3 data-ar="لا نتائج مُدقّقة">No audited outcomes</h3><p data-ar="لم تُقس نتائج تجارية لهذه المشاريع بأداة مستقلة، ولا ننشر نسبًا مستنتجة. أي رقم في الموقع يظهر مع أصله وحدوده.">No commercial outcome for these projects has been measured by an independent tool, and we do not publish inferred percentages. Where a number appears on this site it comes with its source and limits.</p></article>
          <article class="panel mini" data-reveal style="--d:.05s"><h3 data-ar="لا مواد عميل محمية">No protected client material</h3><p data-ar="الرسوم الثلاثة رسوم توضيحية للنطاق، لا لقطات منتج. مواد العميل المحمية باتفاقية سرية لا تُنشر — يمكن مناقشته شفهيًا في مكالمة.">The three visuals are scope diagrams, not product screenshots. Client material under NDA is not published — it can be discussed on a call.</p></article>
          <article class="panel mini" data-reveal style="--d:.1s"><h3 data-ar="لا شهادات">No testimonials</h3><p data-ar="لم نطلب ولن نخترع شهادات عملاء. من يريد مرجعًا تجاريًا يطلبه في المكالمة، ويُتعامل معه وفق ما يسمح به العقد.">We have not solicited and will not invent client testimonials. Anyone who wants a reference asks on the call, and it is handled within what each contract allows.</p></article>
        </div>
        <div class="callout panel" data-reveal style="margin-top:22px">
          <div>
            <h3 data-ar="تريد أن ترى نظامًا أكمل؟">Want to see a working system?</h3>
            <p data-ar="تطبيق زاد منشور للعامة ويمكن فتحه الآن — الوحدات الإحدى عشرة الأخرى تعمل دون اتصال، وهذا أسرع دليل يمكننا تقديمه.">The Zad app is public and you can open it right now — eleven of its modules work offline, and that is the fastest proof we can offer.</p>
          </div>
          <div class="callout__actions">
            {btn('Open Zad ↗', 'افتح زاد ↗', 'https://zadullashr.vercel.app/', 'glass')}
            {btn('Book a 30-min call', 'احجز مكالمة 30 دقيقة', '/contact/#book')}
          </div>
        </div>
      </section>

      {closing('NEXT STEP', 'الخطوة التالية',
               '<span data-ar="لديك نظام">Have a system</span> <span class="grad-text" data-ar="يستحق التوثيق؟">worth documenting?</span>',
               'Bring the situation and we will tell you which of the three shapes — product, platform or brand — it actually needs.',
               'أحضر الحالة وسنقول لك أي شكل من الثلاثة تحتاج فعلًا — منتج أو منصة أو علامة.',
               [btn('Book a 30-min call', 'احجز مكالمة 30 دقيقة', '/contact/#book'), btn('Services', 'الخدمات', '/services/', 'glass')])}
'''
    return [page('/case-studies/', title='Work — Three shipped systems, documented scope · Code & Canvas',
                 title_ar='أعمالنا — ثلاثة أنظمة مُسلَّمة بنطاق موثق · Code & Canvas',
                 desc='Pharmacy OS (multi-tenant pharmacy platform), Zad (offline-first worship PWA) and the Nile Pharma ERP — each written as brief, constraints, role, approach, artifacts, and exactly what can be published.',
                 desc_ar='نظام تشغيل الصيدليات (منصة متعددة المستأجرين)، وزاد (تطبيق عبادات يعمل دون اتصال)، ومنصة نايل فارما ERP — كل واحد مكتوب كموجز وقيود ودور ومنهج ومخرجات وما يمكن نشره فعلًا.',
                 nav='work', body=body)]
