# -*- coding: utf-8 -*-
""" /system/ — the owner-safe Phase 2 of the REF UI study, plus the Phase 3
no-go boundary section.

Adapted mechanisms: palette/token cards (004/016), mixed-size bento component
gallery + real-data inventory (023/041), CSS-only slit/accordion gallery (026),
static orbit of tilted art tiles (044) and founder label plates (045). Reference
060 (profile cards with borrowed portraits / follower counts) stays rejected.

Phase 3 in the study is deliberately rejected, so it is published here only as
a bilingual "what we refuse to ship" boundary list, locked by
scripts/check-phase3.mjs and tests/phase3.spec.mjs — never as dashboard chrome,
fabricated metrics, a foreign skin or runtime blur/WebGL.

Provenance contract: every image is our own labelled illustrative WebP, every
number is read from the generator data, and no third-party photo, logo, font,
CDN, chart or fabricated metric is published. No runtime blur, no always-on
animation and no new external dependency.
"""
from h import esc, icon, crumbs, closing, btn, page, sec_head, media_img
from catalog import SERVICES, TRACKS
from data_case_studies import CASE_STUDIES
from data_founder_work import FOUNDER_WORK
from pages_team import AHMED, MUSTAFA

CSS = '    <link rel="stylesheet" href="/assets/css/system.css" />\n'
ILL = 'ILLUSTRATIVE ART · NOT CLIENT WORK'
ILL_AR = 'عمل توضيحي · ليس عمل عميل'
SHORT = 'ILLUSTRATIVE'
SHORT_AR = 'توضيحي'


def _alt(label_en, label_ar):
    return ILL + ' — ' + label_en, ILL_AR + ' — ' + label_ar


def token_card(key, name, name_ar, value, copy_value, aria, aria_ar):
    return f'''
      <article class="sys-token sys-token--{key}" aria-label="{esc(aria)}" data-ar-label="{esc(aria_ar)}">
        <span class="sys-token__swatch" aria-hidden="true"></span>
        <div class="sys-token__body">
          <h3 data-ar="{esc(name_ar)}">{esc(name)}</h3>
          <code class="sys-token__value" dir="ltr">{esc(value)}</code>
          <button type="button" class="sys-token__copy" data-copy="{esc(copy_value)}" aria-label="{esc(aria)}" data-ar-label="{esc(aria_ar)}"><span data-ar="نسخ">Copy</span></button>
        </div>
      </article>'''


def inventory_card(no, value, label, label_ar, note, note_ar):
    return f'''
      <article class="sys-inventory__card" aria-label="{esc(label)}" data-ar-label="{esc(label_ar)}">
        <span class="sys-inventory__no">{no}</span>
        <b class="ltr">{value}</b>
        <h3 data-ar="{esc(label_ar)}">{esc(label)}</h3>
        <p data-ar="{esc(note_ar)}">{esc(note)}</p>
      </article>'''


def slit_item(no, slug, title, title_ar, desc, desc_ar, opened=False):
    alt, alt_ar = _alt(title, title_ar)
    state = ' open' if opened else ''
    return f'''
        <details class="sys-slit__item" name="sys-slit"{state} aria-label="{esc(title)}" data-ar-label="{esc(title_ar)}">
          <summary><span class="sys-slit__no">{no}</span><span data-ar="{esc(title_ar)}">{esc(title)}</span><span class="sys-slit__badge" data-ar="{esc(SHORT_AR)}">{SHORT}</span></summary>
          <figure class="sys-slit__figure">
            {media_img(slug, alt, alt_ar, sizes='(max-width: 720px) 92vw, 760px', width=1200, height=675)}
            <figcaption><span data-ar="{esc(title_ar)}">{esc(title)}</span><span data-ar="{esc(desc_ar)}">{esc(desc)}</span></figcaption>
          </figure>
        </details>'''


def orbit_tile(slug, label, label_ar, pos):
    alt, alt_ar = _alt(label, label_ar)
    return f'''
        <li class="sys-orbit__tile sys-orbit__tile--{pos}" aria-label="{esc(label)}" data-ar-label="{esc(label_ar)}">
          {media_img(slug, alt, alt_ar, sizes='(max-width: 720px) 44vw, 220px', width=480, height=360)}
        </li>'''


def profile_card(person, kind, name_ar):
    return f'''
      <article class="sys-profile sys-profile--{kind}" aria-label="{esc(person['name'])}" data-ar-label="{esc(name_ar)}">
        <span class="sys-profile__mono" aria-hidden="true">{esc(person['mono'])}</span>
        <div class="sys-profile__plate">
          <span class="sys-profile__kicker" data-ar="{esc(person['kicker_ar'])}">{esc(person['kicker'])}</span>
          <h3 data-ar="{esc(name_ar)}">{esc(person['name'])}</h3>
          <p data-ar="{esc(person['role_ar'])}">{esc(person['role'])}</p>
        </div>
        <p class="sys-profile__lead" data-ar="{esc(person['lead_ar'])}">{esc(person['lead'])}</p>
        <a class="text-link sys-profile__link" href="/team/"><span data-ar="افتح صفحة الفريق">Meet the team</span>{icon('arrowUpRight')}</a>
      </article>'''


def guard_card(no, title, title_ar, note, note_ar):
    return f'''
      <article class="sys-guard__card" aria-label="{esc(title)}" data-ar-label="{esc(title_ar)}">
        <span class="sys-guard__no">{no}</span>
        <span class="sys-guard__badge" data-ar="لا">NO</span>
        <h3 data-ar="{esc(title_ar)}">{esc(title)}</h3>
        <p data-ar="{esc(note_ar)}">{esc(note)}</p>
      </article>'''


def build():
    tokens = [
        token_card('navy', 'Deep navy', 'كحلي عميق', '#00001e', '#00001e', 'Copy deep-navy token value', 'نسخ قيمة توكين الكحلي العميق'),
        token_card('violet', 'Violet', 'بنفسجي', '#8b6cff', '#8b6cff', 'Copy violet token value', 'نسخ قيمة توكين البنفسجي'),
        token_card('teal', 'Teal', 'تيل', '#3fd6c4', '#3fd6c4', 'Copy teal token value', 'نسخ قيمة توكين التيل'),
        token_card('pink', 'Pink', 'وردي', '#ee5ba3', '#ee5ba3', 'Copy pink token value', 'نسخ قيمة توكين الوردي'),
        token_card('gold', 'Gold', 'ذهبي', '#f3c77a', '#f3c77a', 'Copy gold token value', 'نسخ قيمة توكين الذهبي'),
        token_card('grad', 'Brand gradient', 'تدرّج العلامة', 'teal → violet → pink', 'linear-gradient(120deg, #3fd6c4, #8b6cff, #ee5ba3)', 'Copy brand-gradient token value', 'نسخ قيمة توكين تدرّج العلامة'),
    ]

    inventory = [
        inventory_card('01', len(SERVICES), 'Productized services', 'خدمات مُنتجة', 'Read from the service catalogue.', 'مأخوذ من كتالوج الخدمات.'),
        inventory_card('02', len(TRACKS), 'Service tracks', 'مسارات الخدمة', 'Technology · creative · healthcare · combined.', 'تقنية · إبداع · رعاية صحية · مشاريع متكاملة.'),
        inventory_card('03', len(CASE_STUDIES), 'Project case studies', 'دراسات حالة مشاريع', 'Each page states its source and evidence limit.', 'كل صفحة توضّح مصدرها وحدود إثباتها.'),
        inventory_card('04', len(FOUNDER_WORK), 'Founder archive entries', 'مدخلات أرشيف المؤسس', 'Published projects with links back to their sources.', 'مشروعات منشورة مع روابط إلى مصادرها.'),
        inventory_card('05', 2, 'Founders', 'مؤسسان', 'One brief, two owners, no account layer.', 'موجز واحد، مالكان، بلا فريق حساب وسيط.'),
        inventory_card('06', 2, 'Local market pages', 'صفحتا سوق محلي', 'Al Khobar, KSA · Al Obour, Egypt.', 'الخبر، السعودية · العبور، مصر.'),
    ]

    slits = [
        slit_item('01', 'brand-system', 'Brand systems', 'أنظمة العلامة', 'Composition study, not a client deliverable.', 'دراسة تركيب بصري، ليست تسليم عميل.', True),
        slit_item('02', 'case-maqloop', 'Maqloop', 'مقلوب', 'Numbered apparel-release concept.', 'مفهوم إطلاقات أزياء مرقّمة.'),
        slit_item('03', 'case-packbox', 'Packbox Studio', 'باك بوكس ستوديو', 'Packaging and print system concept.', 'مفهوم نظام تغليف ومطبوعات.'),
        slit_item('04', 'case-pharmacy', 'Pharmacy OS', 'نظام الصيدليات', 'Healthcare workflow concept.', 'مفهوم مسار عمل رعاية صحية.'),
    ]

    orbit = [
        orbit_tile('case-axiom', 'Axiom identity study', 'دراسة هوية أكسيوم', '1'),
        orbit_tile('case-continuum', 'Continuum system study', 'دراسة منظومة كونتينوم', '2'),
        orbit_tile('case-evolve', 'Evolve system study', 'دراسة منظومة إيفولف', '3'),
        orbit_tile('case-farm', 'Farm console study', 'دراسة لوحة المزرعة', '4'),
        orbit_tile('case-oltre', 'Oltre collective study', 'دراسة أولتري كولكتيف', '5'),
        orbit_tile('case-sakanwave', 'Sakanwave study', 'دراسة سكن ويف', '6'),
        orbit_tile('case-stt', 'Speech-to-text study', 'دراسة تحويل الكلام إلى نص', '7'),
        orbit_tile('case-ummah', 'Ummah Academy study', 'دراسة أكاديمية الأمة', '8'),
    ]

    profiles = [
        profile_card(AHMED, 'code', 'أحمد بدير'),
        profile_card(MUSTAFA, 'canvas', 'مصطفى أبو العزم'),
    ]

    guards = [
        guard_card('01', 'Fabricated metrics', 'مؤشرات مُختلقة',
                   'No percentages, growth curves, revenue tooltips or KPI tiles.',
                   'بلا نسب مئوية، منحنيات نمو، تلميحات إيرادات أو بلاطات KPI.'),
        guard_card('02', 'AI / crypto / health dashboards', 'لوحات ذكاء اصطناعي / عملات / صحة',
                   'No dashboard chrome for a product we do not sell.',
                   'بلا واجهة لوحة بيانات لمنتج لا نبيعه.'),
        guard_card('03', 'Orange / cyan / serif skins', 'قشور برتقالية / سماوية / سيريف',
                   'One palette: navy, violet, teal, pink and gold; the amber CTA is the only warm accent.',
                   'بالِت واحدة: كحلي، بنفسجي، تيل، وردي وذهبي؛ زر الكهرمان هو الدفء الوحيد.'),
        guard_card('04', 'Runtime blur / WebGL', 'طمس وقتي / WebGL',
                   'Static gradients only, reduced motion respected, no canvas and no always-on animation.',
                   'تدرّجات ثابتة فقط، احترام تقليل الحركة، بلا canvas وبلا حركة دائمة.'),
        guard_card('05', 'Third-party portraits & logos', 'بورتريهات وشعارات أطراف ثالثة',
                   'Labelled first-party illustrative WebP only; every client screenshot stays out.',
                   'أعمالنا التوضيحية المعلّمة فقط؛ أي لقطة شاشة عميل تظل خارجًا.'),
        guard_card('06', 'REF 060 profile card', 'كارت المرجع 060',
                   'No borrowed portrait, follower count or verified badge. Rejected, not deferred.',
                   'بلا بورتريه مستعار، عدّاد متابعين أو شارة توثيق. مرفوض، مش مؤجّل.'),
    ]

    body = f'''
      <section class="phero container phero--left sys-hero" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('Design system', 'نظام التصميم', None)])}
        <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="نظام التصميم · المرحلة الثانية">DESIGN SYSTEM · PHASE 02</span></span>
        <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s"><span data-ar="لغة واحدة،">One language,</span><br /><span class="grad-text" data-ar="كل الأسطح.">every surface.</span></h1>
        <p class="hero__lead" data-reveal style="--d:.16s" data-ar="فهرس عمل للتوكينات والمكوّنات وجرد الموقع الحقيقي الذي نستخدمه في Code & Canvas. صفحة توثيق، لا عرض بيعي، ولا أرقام أداء مُختلقة.">A working index of the tokens, components and real site inventory behind Code & Canvas. This is documentation, not a pitch — and it contains no invented performance numbers.</p>
        <div class="hero__ctas" data-reveal style="--d:.24s">{btn('Explore the tokens', 'استكشف التوكينات', '#tokens', 'primary', 'arrowDown')}{btn('See the components', 'شاهد المكوّنات', '#components', 'glass', 'grid')}{btn('Read the methodology', 'اقرأ المنهجية', '/methodology/', 'ghost', 'layers')}</div>
      </section>

      <section class="section container section--flush-top" id="tokens" aria-label="Design tokens" data-ar-label="توكينات التصميم">
        {sec_head('01', 'TOKENS', 'التوكينات',
                  '<span id="tokens-title" data-ar="اللون قاعدة،">Colour is a rule,</span> <span class="grad-text" data-ar="مش مزاج.">not a mood.</span>',
                  'The six brand values that drive every surface. Copy a value with the button; no external colour library is loaded.',
                  'قيم العلامة الست التي تحكم كل الأسطح. انسخ القيمة بالزر؛ لا تُحمَّل أي مكتبة ألوان خارجية.',
                  aside='<span class="pill" data-ar="بتوكيناتنا">OUR OWN TOKENS</span>')}
        <div class="sys-tokens">{''.join(tokens)}</div>
        <p class="sys-token__status" id="sys-copy-status" role="status" aria-live="polite"></p>
        <p class="live-media-note" data-ar="القيم معروضة كما هي في ds.css؛ لا درجات لونية من مراجع خارجية.">Values are shown exactly as defined in ds.css; no swatches were borrowed from the references.</p>
      </section>

      <section class="section container section--flush-top" id="components" aria-label="Component gallery" data-ar-label="معرض المكوّنات">
        {sec_head('02', 'COMPONENT GALLERY', 'معرض المكوّنات',
                  '<span id="components-title" data-ar="قطع صغيرة،">Small pieces,</span> <span class="grad-text" data-ar="نظام واحد.">one system.</span>',
                  'A bento of the actual surfaces used across the site: glass, pills, rings, numbered rails, ghost type and status surfaces.',
                  'بينتو للأسطح الحقيقية المستخدمة في الموقع: زجاج، حبوب، حلقات، سكك مرقّمة، كتابة شبحية وأسطح حالة.',
                  aside='<span class="pill" data-ar="CSS فقط">CSS ONLY</span>')}
        <div class="sys-bento">
          <article class="sys-bento__card sys-bento__card--wide" aria-label="Glass panel" data-ar-label="لوح زجاجي">
            <span class="sys-bento__kicker" data-ar="لوح / 01">PANEL / 01</span>
            <h3 data-ar="سطح زجاجي">Glass surface</h3>
            <p data-ar="حدود رقيقة، نصف قطر ثابت، وعمق من تدرّج ثابت بلا طمس وقتي.">A thin border, a fixed radius and depth from a static gradient — no runtime blur.</p>
            <span class="pill" data-ar="999px">999px pill</span>
          </article>
          <article class="sys-bento__card" aria-label="Button pair" data-ar-label="زوج أزرار">
            <span class="sys-bento__kicker" data-ar="أزرار / 02">BUTTONS / 02</span>
            <h3 data-ar="قرار واحد">One decision</h3>
            <span class="btn btn--primary sys-bento__btn" aria-hidden="true" data-ar="الإجراء الأساسي">Primary action</span>
            <span class="btn btn--glass sys-bento__btn" aria-hidden="true" data-ar="الإجراء الثانوي">Secondary action</span>
          </article>
          <article class="sys-bento__card" aria-label="Ring control" data-ar-label="تحكم حلقي">
            <span class="sys-bento__kicker" data-ar="حلقات / 03">RINGS / 03</span>
            <span class="sys-ring" aria-hidden="true">{icon('layers')}</span>
            <h3 data-ar="تحكم دائري">Ring control</h3>
            <p data-ar="خمس حلقات في الرأس؛ هذه نسخة توثيقية ثابتة.">Five rings live in the header; this is a static documentation copy.</p>
          </article>
          <article class="sys-bento__card" aria-label="Numbered rail" data-ar-label="سكة مرقّمة">
            <span class="sys-bento__kicker" data-ar="سكة / 04">RAIL / 04</span>
            <ol class="sys-bento__rail">
              <li><b>01</b><span data-ar="نحدّد القرار">Frame</span></li>
              <li><b>02</b><span data-ar="نصمّم الطبقة">Design</span></li>
              <li><b>03</b><span data-ar="نبني ونختبر">Build</span></li>
              <li><b>04</b><span data-ar="نسلّم الملفات">Hand over</span></li>
            </ol>
          </article>
          <article class="sys-bento__card sys-bento__card--wide" aria-label="Ghost wordmark" data-ar-label="كتابة شبحية">
            <span class="sys-bento__kicker" data-ar="كتابة / 05">TYPE / 05</span>
            <span class="sys-ghost" aria-hidden="true"></span>
            <h3 data-ar="كلمة شبحية">Ghost wordmark</h3>
            <p data-ar="نوع مولّد بالـ CSS، لا عقدة نصية في الـ DOM ولا يُقرأ كنص منخفض التباين.">CSS-generated type, with no DOM text node and no low-contrast body copy.</p>
          </article>
          <article class="sys-bento__card" aria-label="Status surface" data-ar-label="سطح حالة">
            <span class="sys-bento__kicker" data-ar="حالة / 06">STATUS / 06</span>
            <span class="sys-status" data-ar="مُعلَّن">LABELLED</span>
            <h3 data-ar="حدود واضحة">Plain limits</h3>
            <p data-ar="كل عمل توضيحي يحمل وسمًا ظاهرًا.">Every illustrative work carries a visible label.</p>
          </article>
        </div>
      </section>

      <section class="section container section--flush-top" id="inventory" aria-label="Site inventory" data-ar-label="جرد الموقع">
        {sec_head('03', 'SITE INVENTORY', 'جرد الموقع',
                  '<span id="inventory-title" data-ar="أرقام من المولّد،">Counts from the generator,</span> <span class="grad-text" data-ar="مش من لوحة بيانات.">not a dashboard.</span>',
                  'A bento index of real, documented site contents. No percentages, no fabricated growth, no business metrics.',
                  'فهرس بينتو لمحتويات الموقع الحقيقية والموثّقة. بلا نسب مئوية، بلا نمو مُختلق، بلا مؤشرات أداء.',
                  aside='<span class="pill" data-ar="بيانات حقيقية">REAL DATA</span>')}
        <div class="sys-inventory">{''.join(inventory)}</div>
        <p class="live-media-note" data-ar="تُقرأ الأرقام من كتالوج الخدمات وبيانات دراسات الحالة وأرشيف المؤسس وقت التوليد.">Counts are read from the service catalogue, case-study data and founder archive at generation time.</p>
      </section>

      <section class="section container section--flush-top" id="gallery" aria-label="Slit gallery" data-ar-label="معرض الشقائق">
        {sec_head('04', 'SLIT GALLERY', 'معرض الشقائق',
                  '<span id="gallery-title" data-ar="أربع لوحات،">Four panels,</span> <span class="grad-text" data-ar="بلا مكتبة.">no library.</span>',
                  'A CSS-only accordion built from native details/summary. Open a panel by click or keyboard; no scroll listener and no animation.',
                  'أكورديون بـ CSS فقط من عناصر details/summary الأصلية. افتح لوحة بالنقر أو الكيبورد؛ بلا مستمع تمرير وبلا حركة.',
                  aside='<span class="pill" data-ar="الكيبورد جاهز">KEYBOARD READY</span>')}
        <div class="sys-slit" role="group" aria-label="Illustrative artwork accordion" data-ar-label="أكورديون الأعمال التوضيحية">{''.join(slits)}
        </div>
      </section>

      <section class="section container section--flush-top" id="orbit" aria-label="Orbit study" data-ar-label="دراسة المدار">
        {sec_head('05', 'ORBIT STUDY', 'دراسة المدار',
                  '<span id="orbit-title" data-ar="مدار ثابت،">A static orbit,</span> <span class="grad-text" data-ar="مش ادّعاء توليد صور.">not an AI-photo claim.</span>',
                  'Eight tilted tiles from our own labelled artwork around one sentence. No third-party imagery, no animation, no product positioning.',
                  'ثماني بلاطات مائلة من أعمالنا المعلّمة حول عبارة واحدة. بلا صور أطراف ثالثة، بلا حركة، بلا تموضع منتج.',
                  aside='<span class="pill" data-ar="أعمالنا فقط">OUR ART ONLY</span>')}
        <div class="sys-orbit" role="group" aria-label="Static orbit of labelled illustrative artwork" data-ar-label="مدار ثابت من أعمال توضيحية مُعلَّنة">
          <ul class="sys-orbit__ring">{''.join(orbit)}
          </ul>
          <div class="sys-orbit__core">
            <p data-ar="منظومة واحدة">ONE SYSTEM</p>
            <h3 data-ar="ثلاث طبقات، لغة واحدة.">Three layers, one language.</h3>
            <p data-ar="العلامة والمنتج والمنظومة: نفس التوكينات، نفس القواعد، بالعربية والإنجليزية.">Brand, product and system: the same tokens, the same rules, in Arabic and English.</p>
          </div>
        </div>
      </section>

      <section class="section container section--flush-top" id="profiles" aria-label="Founder plates" data-ar-label="لوحات المؤسسين">
        {sec_head('06', 'FOUNDER PLATES', 'لوحات المؤسسين',
                  '<span id="profiles-title" data-ar="لوحة اسم،">A name plate,</span> <span class="grad-text" data-ar="مش بورتريه مستعار.">not a borrowed portrait.</span>',
                  'Monograms and real roles instead of stock faces, follower counts or verification badges. Ref 060 stays rejected.',
                  'مونوجرامات وأدوار حقيقية بدل وجوه ستوك أو عدّاد متابعين أو شارات توثيق. المرجع 060 يظل مرفوضًا.',
                  aside='<span class="pill" data-ar="بلا صور أشخاص">NO STOCK FACES</span>')}
        <div class="sys-profiles">{''.join(profiles)}</div>
      </section>

      <section class="section container section--flush-top" id="guardrails" aria-label="Design system guardrails" data-ar-label="حدود نظام التصميم">
        {sec_head('07', 'GUARDRAILS', 'الحدود',
                  '<span id="guardrails-title" data-ar="قائمة ممنوعات،">A no-go list,</span> <span class="grad-text" data-ar="مش قائمة تنفيذ.">not a backlog.</span>',
                  'Phase 3 of the REF study is documented as deliberately rejected. These six rules are published here as design-system boundaries and locked by an automated check.',
                  'المرحلة الثالثة من دراسة REF موثّقة كمرفوضة عن قصد. القواعد الست منشورة هنا كحدود لنظام التصميم ومُقفلة بفحص آلي.',
                  aside='<span class="pill" data-ar="مُقفل آليًا">AUTO-LOCKED</span>')}
        <div class="sys-guard">{''.join(guards)}</div>
      </section>

      <section class="section container section--tight" aria-label="Phase 2 provenance" data-ar-label="مصدر المرحلة الثانية">
        <div class="work-disclaimer" data-reveal>
          {icon('alert')}
          <div>
            <strong data-ar="اتُخذت الآلية فقط، لا البكسلات.">Only the mechanism was adapted, never the pixels.</strong>
            <p data-ar="المرحلة الثانية مبنية من REF 004 / 016 / 023 / 026 / 041 / 044 / 045. كل الصور من أعمالنا التوضيحية المعلّمة، وكل رقم من بيانات المولّد، ولم تُضف صورة مرخّصة أو لقطة شاشة عميل أو خط أو CDN أو مكتبة جديدة.">Phase 2 adapts REF 004 / 016 / 023 / 026 / 041 / 044 / 045. Every image is our own labelled illustrative artwork, every number comes from generator data, and no licensed photo, client screenshot, font, CDN or new library was added.</p>
          </div>
        </div>
      </section>

      {closing('BUILD ON THE RULES', 'ابنِ على القواعد',
              '<span data-ar="نظام واحد،">One system,</span> <span class="grad-text" data-ar="سطحًا بسطح.">surface by surface.</span>',
              'Read the delivery method, or start with a scoped question. The rules stay the same in both languages.',
              'اقرأ طريقة التسليم، أو ابدأ بسؤال محدّد النطاق. القواعد واحدة باللغتين.',
              [btn('Read the methodology', 'اقرأ المنهجية', '/methodology/', 'primary', 'layers'), btn('Book a 30-min call', 'احجز مكالمة 30 دقيقة', '/book/', 'glass', 'calendar')])}
'''

    return [page('/system/', title='Design System — Tokens, Components & Real Site Inventory · Code & Canvas',
                 title_ar='نظام التصميم — التوكينات والمكوّنات وجرد الموقع · Code & Canvas',
                 desc='A bilingual working index of the Code & Canvas design tokens, CSS components, labelled illustrative artwork and real generator-driven site inventory. No reference pixels or fabricated metrics.',
                 desc_ar='فهرس عمل ثنائي اللغة لتوكينات تصميم Code & Canvas ومكوّنات CSS والأعمال التوضيحية المعلّمة وجرد الموقع الحقيقي من بيانات المولّد. بلا بكسلات مرجعية ولا مؤشرات مُختلقة.',
                 nav='', body=body, body_class='is-system', extra_head=CSS,
                 scripts=('/assets/js/pages.js', '/assets/js/system.js'),
                 og_image='/assets/brand/og/resources.png', view_track='system_view')]
