# -*- coding: utf-8 -*-
"""/services/ — Solutions hub.

v3 architecture: problem-first entry, a four-track comparison, then a compact
index of all 23 services. Full scope/deliverables for each service live on the
track pages; this hub stays short enough to decide on.
"""
from catalog import SERVICES, TRACKS
from h import esc, t, th, icon, crumbs, closing, btn, page, service_ld, sec_head, chal, facts, svc_index_row

TRACK_ORDER = ['technology', 'creative', 'healthcare', 'combined']

TRACK_META = {
    'technology': dict(
        id='technology', no='01',
        title='Technology &amp; Enterprise Architecture', title_ar='التقنية والعمارة المؤسسية',
        lead='Architecture decisions that survive audits, vendor changes and year three of the programme.',
        lead_ar='قرارات معمارية تصمد أمام التدقيق وتغيير المورّدين والسنة الثالثة من البرنامج.',
        who='CIOs, transformation leads, PMOs', who_ar='مديرو التقنية وقادة التحوّل ومكاتب المشاريع',
        starts='AB-01 Enterprise Architecture Quick-Start', starts_ar='AB-01 تقييم البداية السريعة للعمارة المؤسسية',
        owner='Ahmed Bedeer', owner_ar='أحمد بدير',
        anchor='AB-01'),
    'creative': dict(
        id='creative', no='02',
        title='Creative &amp; Brand Systems', title_ar='الإبداع وأنظمة العلامة',
        lead='Identity built as an operating system your team can run without calling a designer every week.',
        lead_ar='هوية مبنية كنظام تشغيل يستطيع فريقك إدارته دون الاتصال بمصمم كل أسبوع.',
        who='Founders, marketing leads, brand managers', who_ar='المؤسسون وقادة التسويق ومديرو العلامة',
        starts='MA-01 Logo Design Sprint', starts_ar='MA-01 سبرنت تصميم الشعار',
        owner='Mustafa Aboalazm', owner_ar='مصطفى أبو العزم',
        anchor='MA-01'),
    'healthcare': dict(
        id='healthcare', no='03',
        title='Healthcare', title_ar='الرعاية الصحية',
        lead='Clinic and hospital work delivered with clinical context — and with the compliance vocabulary in the room.',
        lead_ar='عمل العيادات والمستشفيات بسياق سريري حقيقي — وبمفردات الامتثال حاضرة في الغرفة.',
        who='Clinic owners, hospital groups, medical investors', who_ar='أصحاب العيادات ومجموعات المستشفيات والمستثمرون الطبيون',
        starts='HC-03 HIS Selection Advisory', starts_ar='HC-03 استشارات اختيار نظام HIS',
        owner='Both founders', owner_ar='المؤسسان معًا',
        anchor='HC-03'),
    'combined': dict(
        id='combined', no='04',
        title='Combined Engagements', title_ar='المشاريع المتكاملة',
        lead='One brief, one accountable team, no hand-off gap between the brand and the build.',
        lead_ar='موجز واحد وفريق واحد مسؤول، وبلا فجوة تسليم بين الهوية والبناء.',
        who='Launching ventures and founder-led SMEs', who_ar='المشاريع التي تُطلق والشركات التي يقودها مؤسسوها',
        starts='CC-01 Digital Launch Package', starts_ar='CC-01 باقة الإطلاق الرقمي',
        owner='Both founders', owner_ar='المؤسسان معًا',
        anchor='CC-01'),
}


def track_table():
    rows = []
    for key in TRACK_ORDER:
        m = TRACK_META[key]
        codes = [c for c in SERVICES if SERVICES[c]['track'] == key]
        lo = min((SERVICES[c]['price'] for c in codes), key=lambda p: 0)
        rows.append(f'''<tr>
              <th scope="row"><a href="#{m['id']}" data-ar="{m['title_ar']}">{m['title']}</a></th>
              <td data-ar="{esc(m['who_ar'])}">{esc(m['who'])}</td>
              <td data-ar="{esc(m['owner_ar'])}">{esc(m['owner'])}</td>
              <td>{len(codes)} <span data-ar="خدمات">services</span></td>
              <td data-ar="{esc(m['starts_ar'])}">{esc(m['starts'])}</td>
            </tr>''')
    return ('<div class="tbl-wrap" data-reveal><table class="tbl">'
            '<caption data-ar="أربعة مسارات — اختر المسار الذي يناسب القرار الذي أمامك الآن.">Four tracks — pick the one that matches the decision in front of you.</caption>'
            '<thead><tr><th scope="col"><span data-ar="المسار">Track</span></th><th scope="col"><span data-ar="لمن؟">Who it is for</span></th>'
            '<th scope="col"><span data-ar="يقودها">Led by</span></th><th scope="col"><span data-ar="الخدمات">Services</span></th>'
            '<th scope="col"><span data-ar="تبدأ من">Typical first step</span></th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>')


def track_index(key):
    m = TRACK_META[key]
    codes = [c for c in SERVICES if SERVICES[c]['track'] == key]
    items = ''.join(svc_index_row(c).replace('<li>', f'<li id="{c.lower()}">', 1) for c in codes)
    return f'''
        <section class="section container section--flush-top" id="{m['id']}" aria-labelledby="{m['id']}-title">
          {sec_head(m['no'], TRACKS[key]['label'].upper() + ' TRACK', TRACKS[key]['label_ar'] + ' · المسار', f'<span id="{m["id"]}-title" data-ar="{m["title_ar"]}">{m["title"]}</span>', m['lead'], m['lead_ar'],
                    aside=f'<a class="text-link" href="{TRACKS[key]["page"]}" data-track="track" data-track-id="{key}"><span data-ar="تفاصيل المسار كاملة">Full track page</span>{icon("arrowUpRight", "flip")}</a>')}
          <ul class="idx" data-reveal>{items}</ul>
        </section>'''


def build():
    body = f'''
      <!-- ░░ Hero ░░ -->
      <section class="phero container phero--left" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('Solutions', 'الحلول', None)])}
        <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="23 خدمة · أربعة مسارات · نطاق ثابت">23 services · four tracks · fixed scope</span></span>
        <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s"><span data-ar="كل خدمة تبدأ">Every service starts</span><br /><span class="grad-text" data-ar="بقرار واضح.">with a clear decision.</span></h1>
        <p class="hero__lead" data-reveal style="--d:.16s" data-ar="لا نبيع ساعات؛ نبيع نطاقًا معلنًا ومخرجًا محددًا. لكل خدمة من الخدمات الـ23: لمن هي، وما الذي تحصل عليه، ومدة التنفيذ، والنطاق السعري — كله منشور قبل أن تتحدث معنا.">We don’t sell hours; we sell published scope and a defined deliverable. For each of the 23 services you can read who it is for, what you keep, how long it takes and the price range — all before you talk to us.</p>
        <div class="hero__ctas" data-reveal style="--d:.24s">
          {btn('Book a free 30-min call', 'احجز مكالمة مجانية · 30 دقيقة', '/contact/#book')}
          {btn('Prices & payment terms', 'الأسعار وشروط الدفع', '/pricing-faq/', 'glass')}
        </div>
        {facts([('Productized services', 'خدمات مُنتجة', '23', True), ('Tracks', 'مسارات', '4', True),
                ('Engagements', 'نموذج التعاقد', 'Fixed scope', False, 'نطاق ثابت'),
                ('Coverage', 'التغطية', 'KSA + Egypt', True)])}
      </section>

      <!-- ░░ 01 · Start from the problem ░░ -->
      <section class="section container" id="start" aria-labelledby="start-title">
        {sec_head('01', 'STARTING POINT', 'نقطة البداية',
                  '<span id="start-title" data-ar="أربعة مواقف">Four situations</span> <span class="grad-text" data-ar="وأول خطوة في كل منها.">and the first step in each.</span>',
                  'Most conversations begin with one of these. Each one maps to a first engagement you can approve without a procurement cycle.',
                  'معظم المحادثات تبدأ بأحد هذه المواقف. كل موقف يقابل أول مشروع يمكن اعتماده دون دورة مشتريات كاملة.')}
        <div class="grid-4">
          {chal('AB-01', 'TECHNOLOGY', 'التقنية', 'Our systems don’t talk to each other', 'أنظمتنا لا تتحدث مع بعضها',
                ['Three vendors, no single owner', 'Reports retyped by hand every month', 'Every integration turns into a new project'],
                ['ثلاثة مورّدين ولا مالك واحد للقرار', 'تقارير تُعاد كتابتها يدويًا كل شهر', 'كل تكامل يتحول إلى مشروع جديد'],
                '$1,000 – $5,000 · 2–8 weeks', '⁦$1,000 – $5,000⁩ · ⁦2–8⁩ أسابيع')}
          {chal('HC-03', 'HEALTHCARE', 'الرعاية الصحية', 'We’re choosing an HIS or an ERP now', 'نختار نظام HIS أو ERP الآن',
                ['Every vendor demo looks the same', 'Nobody owns the business case', 'The commitment runs for years'],
                ['كل العروض تبدو متطابقة في العرض التجريبي', 'لا أحد يملك دراسة الجدوى', 'الالتزام يمتد سنوات'],
                'From $2,500 · 3–5 weeks', 'من ⁦$2,500⁩ · ⁦3–5⁩ أسابيع', delay=0.05)}
          {chal('MA-03', 'BRAND', 'العلامة', 'Our brand doesn’t match our ambition', 'علامتنا لا تعكس طموحنا',
                ['A logo file, no system', 'Every deck looks like a different company', 'Arabic treated as an afterthought'],
                ['لدينا شعار فقط، بلا نظام', 'كل عرض تقديمي يبدو من شركة أخرى', 'العربية تُعالج كفكرة لاحقة'],
                '$1,490 – $2,975+ · 5–7 weeks', '⁦$1,490 – $2,975+⁩ · ⁦5–7⁩ أسابيع', delay=0.1)}
          {chal('CC-01', 'LAUNCH', 'إطلاق متكامل', 'We’re launching and need both', 'نُطلق منتجًا ونحتاج الاثنين معًا',
                ['Brand, site and product in parallel', 'Two vendors, one deadline', 'No one accountable for the whole'],
                ['العلامة والموقع والمنتج بالتوازي', 'مورّدان وموعد واحد', 'لا أحد مسؤول عن الصورة الكاملة'],
                'From $1,500 · 6–8 weeks', 'من ⁦$1,500⁩ · ⁦6–8⁩ أسابيع', delay=0.15)}
        </div>
      </section>

      <!-- ░░ 02 · Compare the tracks ░░ -->
      <section class="section container" id="tracks" aria-labelledby="tracks-title">
        {sec_head('02', 'COMPARE', 'قارن', '<span id="tracks-title" data-ar="أي مسار يخصّ قرارك؟">Which track owns your decision?</span>',
                  'Each track has one owner, one published price list and one place to start. Combined work is run by both founders under a single contract.',
                  'لكل مسار مالك واحد وقائمة أسعار منشورة ونقطة بداية واحدة. المشاريع المتكاملة يقودها المؤسسان بعقد واحد.')}
        {track_table()}
        <p class="note-quiet" style="margin-top:16px" data-ar="الأسعار المعروضة نطاقات استرشادية بالدولار، وتُثبَّت في عرض مكتوب بعد مكالمة النطاق. لا توجد تكلفة خفية ولا ساعات غير محدودة.">Listed prices are indicative USD ranges, fixed in a written proposal after the scoping call. No hidden cost and no open-ended hours.</p>
      </section>

      <!-- ░░ 03 · The index ░░ -->
      <section class="section container" id="index" aria-labelledby="index-title">
        {sec_head('03', 'THE INDEX', 'الفهرس', '<span id="index-title" data-ar="الخدمات الـ23 كاملة.">All 23 services.</span>',
                  'Scope, deliverables and price per service — full detail lives on the track pages.',
                  'النطاق والمخرجات والسعر لكل خدمة — التفاصيل الكاملة في صفحات المسارات.',
                  aside=f'<a class="text-link" href="/pricing-faq/" data-track="navigation" data-track-to="pricing"><span data-ar="الأسعار وشروط الدفع">Prices &amp; payment terms</span>{icon("arrowUpRight", "flip")}</a>')}
      </section>
      {''.join(track_index(k) for k in TRACK_ORDER)}

      <!-- ░░ 04 · Not sure / next step ░░ -->
      <section class="section container section--tight" id="not-sure" aria-labelledby="fit-title">
        <div class="callout panel" data-reveal>
          <div>
            <p class="sec-head__no" style="border:0;padding:0;margin:0 0 10px"><b>04</b><span data-ar="لست متأكدًا؟">NOT SURE?</span></p>
            <h3 id="fit-title"><span data-ar="اشرح المشكلة">Describe the problem</span> <span class="grad-text" data-ar="وسنقترح أخف مشروع يحلّها.">and we’ll propose the lightest fix.</span></h3>
            <p data-ar="أحيانًا تكون الإجابة خدمة بـ ⁦$170⁩، وأحيانًا تكون «لا تشترِ شيئًا الآن». نقول أيهما في مكالمة واحدة مدتها 30 دقيقة، بلا التزام.">Sometimes the answer is a $170 service; sometimes it is “don’t buy anything yet”. We say which in one 30-minute call, with no obligation.</p>
          </div>
          <div class="callout__actions">
            {btn('Book a free 30-min call', 'احجز مكالمة مجانية · 30 دقيقة', '/contact/#book')}
            <a class="text-link" href="https://wa.me/966545520750" target="_blank" rel="noopener">{icon('chat')}<span data-ar="واتساب · السعودية (التقنية)">WhatsApp · KSA (Technology)</span></a>
            <a class="text-link" href="https://wa.me/201092500454" target="_blank" rel="noopener">{icon('chat')}<span data-ar="واتساب · مصر (الإبداع)">WhatsApp · EG (Creative)</span></a>
          </div>
        </div>
      </section>

      {closing('NEXT STEP', 'الخطوة التالية',
               '<span data-ar="نطاق مكتوب">A written scope</span> <span class="grad-text" data-ar="قبل أي التزام.">before any commitment.</span>',
               'Read how the two practices became one studio, or start with the call and get a written first step.',
               'اقرأ كيف أصبح التخصصان استوديو واحدًا، أو ابدأ بالمكالمة واحصل على خطوة أولى مكتوبة.',
               [btn('Our story', 'قصتنا', '/our-story/'), btn('The methodology', 'المنهجية', '/methodology/', 'glass')])}
'''
    out = page('/services/', title='Solutions — 23 productized services · Code & Canvas',
               title_ar='الحلول — 23 خدمة مُنتجة · Code & Canvas',
               desc='All 23 Code & Canvas services across four tracks: enterprise architecture, healthcare IT and data, brand systems and web, plus combined launch engagements — with who each is for, deliverables, duration and price.',
               desc_ar='كل خدمات Code & Canvas الـ23 عبر أربعة مسارات: العمارة المؤسسية وتقنية الرعاية الصحية والبيانات، وأنظمة العلامة والويب، وباقات الإطلاق المتكاملة — مع شروط كل خدمة ومخرجاتها ومدتها وسعرها.',
               nav='services', body=body, ld=[service_ld(list(SERVICES), 'https://codeandcanvas.net/services/')])
    return [out]
