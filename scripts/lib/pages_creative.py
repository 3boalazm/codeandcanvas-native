# -*- coding: utf-8 -*-
"""/creative-services/ — live copy of codeandcanvas.net/creative-services/."""
from catalog import SERVICES
from h import esc, t, icon, crumbs, closing, btn, page, service_ld, PERSON_LD
from pages_technology import detail, tags


ALACARTE = [
    ('Business Card', 'بطاقة عمل', 'Two-sided · 2 versions · 3 revisions', 'وجهان · نسختان · 3 تعديلات', '$22'),
    ('Brochure', 'بروشور', '4 pages · A4/A5 · up to 4 folds', '4 صفحات · A4/A5 · حتى 4 طيّات', '$34'),
    ('Flyer', 'نشرة', 'Bi / Tri / Quad fold', 'طيّتان / ثلاث / أربع', '$26 – $38'),
    ('Promotional Poster', 'ملصق ترويجي', 'Digital or print · 3 revisions', 'رقمي أو مطبوع · 3 تعديلات', '$26 – $43'),
    ('Standard Roll-Up', 'رول-أب قياسي', '80×200 / 85×200 / 90×200 cm', '80×200 / 85×200 / 90×200 سم', '$30'),
    ('Single Social Post', 'منشور سوشيال واحد', 'Facebook · Instagram · LinkedIn', 'فيسبوك · إنستغرام · لينكدإن', '$11'),
    ('Social Post Pack × 10', 'حزمة 10 منشورات', 'Save $25 on the single rate', 'وفّر ⁦$25⁩ عن سعر القطعة', '$85'),
    ('Landing Page', 'صفحة هبوط', 'Single conversion-focused page · responsive', 'صفحة واحدة موجّهة للتحويل · متجاوبة', '$170 – $340'),
]

ACTS = [
    ('01', 'Discovery & Research', 'الاستكشاف والبحث', 'Days 1–6', 'الأيام ⁦1–6⁩', 'Brand audit · competitor analysis · color-gap mapping · audience persona · cultural research', 'تدقيق العلامة · تحليل المنافسين · رسم فجوات الألوان · شخصية الجمهور · بحث ثقافي'),
    ('02', 'Brand Strategy', 'استراتيجية العلامة', 'Days 5–9', 'الأيام ⁦5–9⁩', 'Purpose · positioning · archetype · voice & tone · value proposition — approved before any design', 'الغاية · التموضع · النموذج الأصلي · الصوت والنبرة · عرض القيمة — تُعتمد قبل أي تصميم'),
    ('03', 'Concept & Design', 'المفهوم والتصميم', 'Days 9–27', 'الأيام ⁦9–27⁩', 'Sketches → 2–3 directions → logo system · color · typography · brand elements · applications', 'اسكتشات ← 2–3 اتجاهات ← منظومة الشعار · الألوان · الخطوط · عناصر العلامة · التطبيقات'),
    ('04', 'Refine & Deliver', 'الصقل والتسليم', 'Days 27–38', 'الأيام ⁦27–38⁩', '2 revision rounds · sign-off · full file delivery · brand guidelines PDF · handover call', 'جولتا تعديل · اعتماد · تسليم كامل للملفات · دليل العلامة PDF · مكالمة تسليم'),
]


def build():
    acts = ''.join(f'''
          <li data-reveal style="--d:{i * .06:.2f}s">
            <div><h3 data-ar="{esc(ar)}">{esc(en)}</h3><p data-ar="{esc(dar)}">{esc(den)}</p><div class="steps__meta"><span><b data-ar="{esc(tar)}">{esc(ten)}</b></span></div></div>
          </li>''' for i, (n, en, ar, ten, tar, den, dar) in enumerate(ACTS))
    alacarte = ''.join(f'''
          <div class="tier" data-reveal style="--d:{(i % 4) * .05:.2f}s"><b data-ar="{esc(ar)}">{esc(en)}</b><strong>{esc(p)}</strong><p data-ar="{esc(dar)}">{esc(den)}</p></div>''' for i, (en, ar, den, dar, p) in enumerate(ALACARTE))
    lead_by = ('Mustafa Aboalazm', 'مصطفى أبو العزم')

    body = f'''
      <!-- ░░ Hero ░░ -->
      <section class="phero container" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('Solutions', 'الحلول', '/services/'), ('Creative Studio', 'الاستوديو الإبداعي', None)])}
        <div class="phero__split">
          <div>
            <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="الاستوديو الإبداعي · الهوية · التصميم · الويب · الإعلام">Creative Studio · Brand · Design · Web · Media</span></span>
            <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s"><span data-ar="هوية مبنية">Identity built as</span><br /><span class="grad-text" data-ar="كنظام تشغيل.">an operating system.</span></h1>
            <p class="hero__lead" data-reveal style="--d:.16s" data-ar-html="من أول علامة شعار إلى دليل العلامة الذي يستخدمه فريقك فعلًا — &lt;strong&gt;10 خدمات إبداعية&lt;/strong&gt;، استوديو واحد، وبلا فجوات تسليم. تصميم تقوده الاستراتيجية للمؤسسات التي تحتاج علامتها أن &lt;em&gt;تعمل&lt;/em&gt;، لا أن تبدو جميلة فحسب.">From the first logo mark to the brand guidelines your team actually uses — <strong>10 creative services</strong>, one studio, no handoff gaps. Strategy-led design for organizations that need their brand to <em>work</em>, not just look good.</p>
            <div class="hero__ctas" data-reveal style="--d:.24s">{btn('Start on WhatsApp', 'ابدأ على واتساب', 'https://wa.me/201092500454')}{btn('Send a Brief', 'أرسل موجزًا', '/contact/#book', 'glass')}</div>
          </div>
          <div class="phero__aside" data-reveal style="--d:.2s">
            <div class="stats__inner glass" style="grid-template-columns:repeat(2,1fr)">
              <div class="stat"><span class="stat__num stat__num--ltr"><span data-count="9" data-latin="1">9</span>+</span><p class="stat__label" data-ar-html="سنوات من&lt;br /&gt;الممارسة الإبداعية">Years of<br />creative practice</p></div>
              <div class="stat"><span class="stat__num stat__num--ltr"><span data-count="20" data-latin="1">20</span>+</span><p class="stat__label" data-ar-html="علامة&lt;br /&gt;صُغناها">Brands<br />shaped</p></div>
              <div class="stat"><span class="stat__num stat__num--ltr"><span data-count="6" data-latin="1">6</span></span><p class="stat__label" data-ar-html="قطاعات&lt;br /&gt;صناعية">Industry<br />sectors</p></div>
              <div class="stat"><span class="stat__num stat__num--ltr">$170</span><p class="stat__label" data-ar-html="يبدأ من&lt;br /&gt;سبرنت الشعار">Starts from<br />logo sprint</p></div>
            </div>
          </div>
        </div>
      </section>

      <!-- ░░ Section nav ░░ -->
      <nav class="subnav subnav--sticky container" aria-label="On this page" data-ar-label="في هذه الصفحة" data-spy>
        <a href="#proof"><span data-ar="الدليل">Proof</span></a>
        <a href="#services"><span data-ar="الخدمات">Services</span><b>10</b></a>
        <a href="#a-la-carte"><span data-ar="حسب القطعة">À la carte</span></a>
        <a href="#method"><span data-ar="المنهجية">Method</span></a>
        <a href="#who"><span data-ar="من ينفّذ">Who delivers</span></a>
        <a href="https://wa.me/201092500454" class="subnav__aux" target="_blank" rel="noopener">{icon('chat')}<span data-ar="واتساب">WhatsApp</span></a>
      </nav>

      <!-- ░░ Proof ░░ -->
      <section class="section container section--tight" id="proof" aria-labelledby="proof-title">
        <div class="proof-band glass" data-reveal>
          <div class="proof-band__item"><b>20+</b><span data-ar="علامة صُغناها عبر 6 قطاعات">brands shaped across 6 sectors</span></div>
          <div class="proof-band__item"><b>4</b><span data-ar="فصول في كل مشروع هوية — من البحث إلى التسليم خلال 38 يومًا">acts in every identity engagement — research to delivery in 38 days</span></div>
          <div class="proof-band__item"><b>AR + EN</b><span data-ar="أنظمة شعار ثنائية اللغة — عربي أولًا، إنجليزي بنفس الجودة">bilingual logo systems — Arabic-first, English to the same standard</span></div>
          <div class="proof-band__item"><b>5 <small data-ar="سنوات">yrs</small></b><span data-ar="مدير إعلام في Nile Pharma Food — هوية بُنيت من الصفر وأُطلقت في السوق">Media Director at Nile Pharma Food — an identity built from zero and launched to market</span></div>
          <a class="proof-band__link" href="https://behance.net/aboalazm" target="_blank" rel="noopener" data-track="portfolio" data-track-id="behance"><span data-ar="الأعمال على Behance">Work on Behance</span><i class="flip" data-icon="arrowUpRight"></i></a>
        </div>
      </section>

      <!-- ░░ Services ░░ -->
      <section class="section container" id="services" aria-labelledby="svc-title">
        <header class="section__head" data-reveal>
          <p class="kicker"><span class="kicker__num">01</span><span data-ar="10 خدمات إبداعية">10 Creative Services</span></p>
          <h2 class="section__title" id="svc-title"><span data-ar="استراتيجية، هوية،">Strategy, identity,</span><br /><span class="grad-text" data-ar="أنظمة وإنتاج.">systems &amp; production.</span></h2>
        </header>
        <div class="toolbar" data-reveal>
          <p><span data-ar="تصفية حسب النوع">Filter by type</span> <i data-icon="arrowDown" aria-hidden="true"></i></p>
          <div class="filters" role="group" aria-label="Filter services" data-ar-label="تصفية الخدمات" data-filter-group="#svc-list">
            <button class="filter is-active" type="button" data-filter="all" aria-pressed="true"><span data-ar="الكل">All</span><b>10</b></button>
            <button class="filter" type="button" data-filter="brand" aria-pressed="false"><span data-ar="هوية العلامة">Brand Identity</span><b>4</b></button>
            <button class="filter" type="button" data-filter="web" aria-pressed="false"><span data-ar="الويب والرقمي">Web &amp; Digital</span><b>2</b></button>
            <button class="filter" type="button" data-filter="print" aria-pressed="false"><span data-ar="المطبوعات والإنتاج">Print &amp; Production</span><b>2</b></button>
            <button class="filter" type="button" data-filter="media" aria-pressed="false"><span data-ar="الإعلام والاشتراكات">Media &amp; Retainers</span><b>2</b></button>
          </div>
        </div>
        <div id="svc-list">
        {_d('MA-03', 'brand', featured=True, badge=('Most Popular', 'الأكثر شيوعًا'), lead_by=lead_by,
            tag_list=['Brand Strategy', 'Logo System', 'Bilingual AR/EN', 'Brand Elements', '25–40 pg Guidelines', 'Training Workshop', '30-day Support'],
            included=['Extended discovery & competitor research', 'Purpose · Vision · Mission · Values', 'Positioning · UVP · Personality · Archetype', 'Tone of voice · Brand story', 'Complete logo system (all formats)', 'Bilingual lockup — designed, not translated', 'Brand elements: patterns · icons · photo direction', '8+ applications · Brand training workshop'],
            included_ar=['استكشاف موسّع وبحث في المنافسين', 'الغاية · الرؤية · الرسالة · القيم', 'التموضع · عرض القيمة الفريد · الشخصية · النموذج الأصلي', 'نبرة الصوت · قصة العلامة', 'منظومة شعار كاملة (بكل الصيغ)', 'تركيب ثنائي اللغة — مصمَّم لا مترجَم', 'عناصر العلامة: أنماط · أيقونات · توجيه التصوير', '+8 تطبيقات · ورشة تدريب على العلامة'],
            tiers=[dict(name='Brand Identity System', name_ar='منظومة هوية العلامة', price='$1,500 – $2,500', dur='3–4 weeks · 8-stage V2', dur_ar='⁦3–4⁩ أسابيع · منهجية V2 من 8 مراحل', desc='Logo system (5+ variants) · brand strategy document · color + typography system · brand guidelines (AR + EN) · full stationery kit · social media template pack.', desc_ar='منظومة شعار (+5 نسخ) · وثيقة استراتيجية العلامة · نظام ألوان وخطوط · دليل العلامة (عربي + إنجليزي) · حزمة قرطاسية كاملة · حزمة قوالب سوشيال ميديا.'),
                   dict(name='Full Brand System — flagship', name_ar='منظومة العلامة الكاملة — الباقة الرئيسية', price='$1,490 – $2,975+', dur='5–7 weeks · 50/25/25 payment', dur_ar='⁦5–7⁩ أسابيع · دفعات 50/25/25', desc='Everything above plus the full strategy document, bilingual lockup, brand elements, 25–40 page guidelines, and a training workshop. For launches and re-launches at scale.', desc_ar='كل ما سبق إضافة إلى وثيقة الاستراتيجية الكاملة والتركيب ثنائي اللغة وعناصر العلامة ودليل من 25–40 صفحة وورشة تدريبية. للإطلاقات وإعادة الإطلاق على نطاق واسع.', star=True)],
            price_note='Start Full Brand System → from $1,490', price_note_ar='ابدأ منظومة العلامة الكاملة ← ابتداءً من ⁦$1,490⁩', cta=('Start Full Brand System', 'ابدأ منظومة العلامة الكاملة'))}
        {_d('MA-01', 'brand', lead_by=lead_by, tag_list=['3 concept directions', '1 developed to final', 'Every format you need', 'MVP startups · small businesses'], cta=('Start a Logo Sprint', 'ابدأ سبرنت شعار'))}
        {_d('MA-02', 'brand', lead_by=lead_by, tag_list=['Brand audit', 'Competitor research', 'Full logo system', 'Color + typography', '12–18 page guidelines', '3 applications'],
            tiers=[dict(name='Brand Audit + Refresh', name_ar='تدقيق وتجديد العلامة', price='$500 – $1,500', dur='1–2 weeks', dur_ar='⁦1–2⁩ أسبوع', desc='Brand health diagnosis · stay / update / rebrand decision · targeted refresh delivery · updated guidelines.', desc_ar='تشخيص صحة العلامة · قرار الإبقاء / التحديث / إعادة البناء · تسليم تجديد موجّه · دليل محدَّث.')],
            cta=('Start Brand Identity', 'ابدأ هوية العلامة'))}
        {_d('MA-04', 'brand', lead_by=lead_by, tag_list=['Design tokens', 'Social kits', 'Presentation templates', 'Figma component libraries', 'Reusable assets'])}
        {_d('MA-05', 'web', lead_by=lead_by, tag_list=['Figma → WordPress / Webflow', 'UX-led', 'Mobile-first', 'Bilingual AR + EN · RTL', 'SEO setup', '6-month support'])}
        {_d('MA-06', 'web', lead_by=lead_by, tag_list=['Next.js', 'Performance-first', 'EN/AR + RTL', '90+ Lighthouse', 'Full source ownership'])}
        {_d('MA-07', 'print', lead_by=lead_by, tag_list=['Packaging', 'Brochures · company profiles', 'Banners · roll-ups', 'CMYK · bleed · trim marks', 'Print-ready PDFs'])}
        {_d('MA-08', 'print', lead_by=lead_by, tag_list=['Photography', 'Videography', 'Scripting · voice-over', 'Audio engineering', 'Bilingual scripts'])}
        {_d('MA-09', 'media', lead_by=lead_by, tag_list=['15–20 designs / month', 'Custom templates', 'Bilingual layouts', 'Figma source included', 'Min. 3 months'])}
        {_d('MA-10', 'media', lead_by=lead_by, tag_list=['Social', 'Print', 'Digital', 'Light video', 'Single dedicated designer'])}
        </div>
      </section>

      <!-- ░░ À la carte ░░ -->
      <section class="section container section--flush-top" id="a-la-carte" aria-labelledby="alc-title">
        <div class="head-split">
          <header class="section__head" data-reveal>
            <p class="kicker"><span class="kicker__num">02</span><span data-ar="حسب القطعة — عناصر مستقلة">À la carte — Stand-alone pieces</span></p>
            <h2 class="section__title" id="alc-title"><span data-ar="قطعة واحدة.">Single pieces.</span> <span class="grad-text" data-ar="داخل نظام علامتك.">Inside your brand system.</span></h2>
          </header>
          <div class="head-aside" data-reveal style="--d:.15s">
            <p data-ar="للعناصر الفردية دون مشروع كامل. كل القطع تُطبَّق داخل نظام علامتك.">For single items without a full engagement. All pieces applied within your brand system.</p>
            <a class="text-link" href="https://aboalazm-os.vercel.app/" target="_blank" rel="noopener"><span data-ar="قائمة الأسعار الكاملة ↗">Full pricing list ↗</span></a>
          </div>
        </div>
        <div class="grid grid--4 tiers" style="gap:12px">{alacarte}
        </div>
      </section>

      <!-- ░░ Method ░░ -->
      <section class="section container section--tight" id="method" aria-labelledby="method-title">
        <header class="section__head" data-reveal>
          <p class="kicker"><span class="kicker__num">03</span><span data-ar="منهجية من أربعة فصول · صُقلت على مدى 9 سنوات · متوسط 38 يومًا من الانطلاق إلى التسليم">4-ACT METHOD · REFINED OVER 9 YEARS · AVG. 38 DAYS KICKOFF → DELIVERY</span></p>
          <h2 class="section__title" id="method-title"><span data-ar="أربعة فصول.">Four acts.</span> <span class="grad-text" data-ar="علامة واحدة تعمل.">One brand that works.</span></h2>
        </header>
        <ol class="steps">{acts}
        </ol>
      </section>

      <!-- ░░ Bio ░░ -->
      <section class="section container section--tight" id="who" aria-labelledby="bio-title">
        <header class="section__head" data-reveal>
          <p class="kicker"><span class="kicker__num">04</span><span data-ar="من يقود التنفيذ">WHO DELIVERS</span></p>
          <h2 class="section__title" style="font-size:clamp(26px,3vw,40px)"><span data-ar="مؤسس واحد يقود كل مشروع إبداعي —">One founder leads every creative engagement —</span> <span class="grad-text" data-ar="من الموجز إلى التسليم.">brief to handover.</span></h2>
        </header>
        <article class="card glass person person--big" data-reveal>
          <div class="art art--portrait art--pink" data-slot="team/mustafa-aboalazm"><span class="art__mark">MA</span><span class="art__cap" data-ar="✦ الكانفاس">✦ THE CANVAS</span></div>
          <div>
            <p class="person__role" data-ar="مهندس هويات منهجية">Systemic Identity Architect</p>
            <h2 id="bio-title">Mustafa Aboalazm</h2>
            <p class="person__tag" data-ar="شريك مؤسس · Code &amp; Canvas · العبور، مصر">Co-Founder · Code &amp; Canvas · Al Obour, Egypt</p>
            <p data-ar="مصمم هوية بصرية أول ومستشار تطوير أعمال — أكثر من 9 سنوات، أكثر من 20 علامة، 6 قطاعات. مدير إعلام سابق في Nile Pharma Food. يصمم منظومات هوية متكاملة لمؤسسي منتجات SaaS وشركات الذكاء الاصطناعي الناشئة والمؤسسات التي يقودها التصميم في المنطقة.">Senior brand identity designer and business development consultant — 9+ years, 20+ brands, 6 sectors. Former Media Director at Nile Pharma Food. Designs full-cycle identity systems for SaaS founders, AI startups, and design-driven organizations across MENA.</p>
            <div class="creds" aria-label="Skills" data-ar-label="المهارات"><span data-ar="استراتيجية العلامة">Brand Strategy</span><span data-ar="منظومات الشعار">Logo Systems</span><span data-ar="أنظمة التصميم">Design Systems</span><span>Next.js</span><span>WordPress</span><span data-ar="الإخراج الفني">Art Direction</span><span data-ar="عربي + إنجليزي">AR + EN</span><span data-ar="العبور، مصر">Al Obour, Egypt</span></div>
            <div class="person__links">
              <a href="https://aboalazm-os.vercel.app/" target="_blank" rel="noopener" title="Mustafa's Portfolio">{icon('link')}<span data-ar="الأعمال">Portfolio</span></a>
              <a href="https://behance.net/aboalazm" target="_blank" rel="noopener">{icon('pen')}<span>Behance ↗</span></a>
              <a href="https://wa.me/201092500454" target="_blank" rel="noopener">{icon('chat')}<span>WhatsApp ↗</span></a>
            </div>
          </div>
        </article>
      </section>

      <!-- ░░ CTA ░░ -->
      <section class="section container section--tight" aria-labelledby="cta-title">
        <div class="callout glass glass--deep" data-reveal>
          <div>
            <p class="kicker"><span data-ar="ابدأ تكليفًا">START A COMMISSION</span></p>
            <h3 id="cta-title"><span data-ar="لديك علامة">Have a brand</span> <span class="grad-text" data-ar="تريد صياغتها؟">to shape?</span></h3>
            <p data-ar="أرسل موجزًا عبر واتساب أو البريد — نؤكد النطاق ونرسل عرضًا مخصصًا ونبدأ خلال 24 ساعة من الدفعة المقدمة. لا بداية بلا موجز. لا ملفات بلا سداد نهائي.">Send a brief on WhatsApp or email — we'll confirm scope, send a custom proposal, and start within 24 hours of deposit. No start without a brief. No files without final payment.</p>
          </div>
          <div class="callout__actions">
            {btn('💬 Start on WhatsApp', '💬 ابدأ على واتساب', 'https://wa.me/201092500454')}
            <a class="text-link" href="/contact/#book">{icon('mail')}<span data-ar="✉️ أرسل موجزًا">✉️ Send a Brief</span></a>
          </div>
        </div>
        <ul class="promises glass" data-reveal aria-label="Studio policies" data-ar-label="سياسات الاستوديو" style="grid-template-columns:repeat(5,1fr)">
          <li>{icon('check')}<span data-ar="خصم 10% عند السداد الكامل مقدمًا">10% off full prepayment</span></li>
          <li>{icon('check')}<span data-ar="الملفات المصدرية بعد السداد النهائي">Source files after final payment</span></li>
          <li>{icon('check')}<span data-ar="جولتا تعديل منظمتان">2 structured revision rounds</span></li>
          <li>{icon('check')}<span data-ar="العربية والإنجليزية">Arabic &amp; English</span></li>
          <li>{icon('check')}<span data-ar="العبور، مصر · عن بُعد">Al Obour, Egypt · Remote</span></li>
        </ul>
      </section>


'''
    return [page('/creative-services/', title='Creative Services — Code & Canvas', title_ar='الخدمات الإبداعية — Code & Canvas',
                 desc='Identity built as an operating system: 10 creative services — logo sprint, brand identity essentials, full brand system, design systems, web, print, production, and retainers — led by Mustafa Aboalazm. Bilingual AR/EN.',
                 desc_ar='هوية مبنية كنظام تشغيل: 10 خدمات إبداعية — سبرنت شعار وأساسيات الهوية ومنظومة العلامة الكاملة وأنظمة التصميم والويب والمطبوعات والإنتاج والاشتراكات — بقيادة مصطفى أبو العزم. ثنائية اللغة عربي/إنجليزي.',
                 nav='services', body=body, ld=[service_ld([c for c in SERVICES if c.startswith('MA-')], 'https://codeandcanvas.net/creative-services/'), PERSON_LD['mustafa']])]


def _d(code, cat, **kw):
    """Creative detail block: category for the filter is the family (brand/web/print/media)."""
    html = detail(code, cls='sdetail--creative', **kw)
    return html.replace(f'data-category="{code.lower()}"', f'data-category="{cat}"', 1)
