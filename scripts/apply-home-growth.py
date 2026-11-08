# -*- coding: utf-8 -*-
"""One-shot homepage rewrite (2026-11 growth layer).

Keeps every section id and class the regression suite depends on, while making
the first screen value-first, visual and conversion-oriented. Re-run idempotent:
it refuses to apply twice.
"""
import re
from pathlib import Path

p = Path(__file__).resolve().parents[1] / 'index.html'
s = p.read_text(encoding='utf-8')
if 'hero--value' in s:
    print('homepage growth already applied')
    raise SystemExit(0)

# ---------- head: per-route OG card, new title, honest description ----------
s = s.replace('data-lang-mirror="/ar/">', 'data-lang-mirror="/ar/" data-og="/assets/brand/og/home.png">', 1)
s = s.replace('<title>Code &amp; Canvas — Business Development, By Design</title>',
              '<title>Code &amp; Canvas — Brand, Product &amp; System, Built Around One Business Outcome</title>', 1)
s = s.replace('content="Code &amp; Canvas helps organizations across MENA grow by aligning brand, technology, and data to business goals—with clear scope and milestone-based delivery."',
              'content="Code & Canvas is a bilingual studio in KSA and Egypt. We build the brand, the digital product and the system behind one clear business outcome — with written scope and milestone delivery."', 1)
s = s.replace('content="A two-founder studio in KSA + Egypt: enterprise architecture, healthcare transformation and data · brand systems and digital products. 23 fixed-scope services, milestone-based, from $170."',
              'content="Strategy. Design. Technology. Explore labelled creative work, seven flagship services and a real 30-minute discovery call."', 1)
s = s.replace('"image":"https://codeandcanvas.net/assets/brand/og-default.png"', '"image":"https://codeandcanvas.net/assets/brand/og/home.png"', 1)
s = s.replace('"url":"https://codeandcanvas.net/assets/brand/og-default.png","width":1200', '"url":"https://codeandcanvas.net/assets/brand/og/home.png","width":1200', 1)
s = s.replace('<link rel="preload" href="/assets/fonts/signategrotesk-black.woff2" as="font" type="font/woff2" crossorigin />',
              '<link rel="preload" href="/assets/fonts/space-grotesk-latin-700.woff2" as="font" type="font/woff2" crossorigin />\n    <link rel="preload" href="/assets/media/hero-system.webp" as="image" type="image/webp" />', 1)

HERO = '''      <!-- ░░ Hero — value first, one CTA, real artwork, verifiable trust strip ░░ -->
      <section class="hero hero--value container" id="top" aria-labelledby="hero-title">
        <div class="hero__copy">
          <p class="eyebrow" data-reveal><span class="eyebrow__dot"></span><span data-ar="الخبر · العبور · عربي / إنجليزي">AL KHOBAR · AL OBOUR · ARABIC / ENGLISH</span></p>
          <h1 class="hero__value-title" id="hero-title">
            <span class="line" data-ar="العلامة. المنتج. المنظومة.">Brand. Product. System.</span>
            <span class="line"><span class="grad-text" data-ar="حول نتيجة عمل واحدة.">One business outcome.</span></span>
          </h1>
          <p class="hero__lead" data-reveal style="--d:.2s" data-ar="نصمّم الهوية، ونبني المنتج الرقمي، ونربط المنظومة التي تقف خلفهما — في استوديو واحد، بوثيقة نطاق واحدة، ومعالم تسليم مكتوبة. لا نبدأ بقائمة خدمات؛ نبدأ بالقرار الذي تريد أن يتغيّر.">We design the identity, build the digital product and wire the systems behind both — in one studio, with one scope document and written milestones. We do not start with a service list; we start with the decision you need to change.</p>
          <div class="hero__ctas" data-reveal style="--d:.35s">
            <a class="btn btn--primary btn--lg magnetic" href="/book/" data-track="cta_click" data-track-id="hero-book"><span data-ar="احجز مكالمة مجانية · 30 دقيقة">Book a free 30-min call</span><i class="flip" data-icon="calendar" aria-hidden="true"></i></a>
            <a class="btn btn--glass btn--lg" href="/work/" data-track="cta_click" data-track-id="hero-work"><span data-ar="شاهد الأعمال">See our work</span><i class="flip" data-icon="arrowUpRight" aria-hidden="true"></i></a>
          </div>
          <ul class="hero__proof" aria-label="What we can verify" data-ar-label="ما نستطيع إثباته" data-reveal style="--d:.5s">
            <li><i data-icon="check" aria-hidden="true"></i><b data-ar="23 خدمة مُنتجة">23 productized services</b><span data-ar="من كتالوج واحد">from one catalogue</span></li>
            <li><i data-icon="check" aria-hidden="true"></i><b data-ar="عربي / إنجليزي">Arabic / English</b><span data-ar="صفحات مستقلة وRTL حقيقي">standalone pages · real RTL</span></li>
            <li><i data-icon="check" aria-hidden="true"></i><b data-ar="السعودية + مصر">KSA + Egypt</b><span data-ar="قناتا اتصال موحّدتان">one contact record</span></li>
            <li><i data-icon="check" aria-hidden="true"></i><a href="/claims/" data-ar="سجل الادعاءات والأدلة ↗">Claims &amp; evidence register ↗</a></li>
          </ul>
        </div>

        <div class="hero__visual hero__visual--media">
          <figure class="live-figure live-figure--hero" data-reveal style="--d:.28s">
            <img src="/assets/media/hero-system.webp" alt="Abstract illustrative studio artwork: layered glass panels and gradient ribbons" data-ar-alt="عمل فني تجريدي توضيحي: طبقات زجاجية وشرائط لونية متدرّجة" width="1600" height="1200" fetchpriority="high" decoding="async" />
            <span class="live-figure__float" data-ar="الاستراتيجية · التصميم · التقنية">STRATEGY · DESIGN · TECHNOLOGY</span>
            <figcaption><span data-ar="دراسة بصرية للاستوديو">STUDIO VISUAL STUDY</span><span class="live-figure__disclaimer" data-ar="توضيحي — ليس عمل عميل">ILLUSTRATIVE · NOT CLIENT WORK</span></figcaption>
          </figure>
          <div class="float-chip glass float-chip--1" data-depth="1.6"><i data-icon="check" aria-hidden="true"></i><span><small data-ar="الخطوة الأولى">FIRST STEP</small><strong data-ar="نستمع قبل أن نبني">Listen before we build</strong></span></div>
          <div class="float-chip glass float-chip--2" data-depth="2.2"><i data-icon="arrowUpRight" aria-hidden="true"></i><span><small data-ar="طريقة عملنا">HOW WE WORK</small><strong data-ar="النطاق قبل المعالم">Scope before milestones</strong></span></div>
        </div>
      </section>

      <!-- ░░ Verifiable trust strip (no unevidenced numbers) ░░ -->
      <section class="section container section--tight" id="trust" aria-label="Studio at a glance" data-ar-label="الاستوديو في سطور">
        <div class="live-strip" data-reveal>
          <div><b class="ltr">4</b><span data-ar="مسارات عمل واضحة">Clear pillars</span><small data-ar="23 خدمة تحتها">23 services beneath them</small></div>
          <div><b class="ltr">7</b><span data-ar="صفحات خدمات مستقلة">Flagship service pages</span><small data-ar="نطاق · مخرجات · أسئلة">Scope · deliverables · FAQ</small></div>
          <div><b class="ltr">3</b><span data-ar="دراسات حالة منشورة">Published case studies</span><small data-ar="بحدود إثبات معلنة">With stated evidence limits</small></div>
          <div><b class="ltr">30′</b><span data-ar="مكالمة حقيقية محجوزة">Real booked call</span><small data-ar="تأكيد + دعوة تقويم">Confirmation + calendar</small></div>
        </div>
        <p class="live-media-note" data-ar="كل رقم هنا قابل للتحقق من الكود أو من صفحة منشورة. سجل الادعاءات الكامل في /claims/.">Every number here is verifiable from the code or a published page. Full register: <a href="/claims/">/claims/</a>.</p>
      </section>
'''
start = s.index('      <!-- ░░ Hero ░░ -->')
end = s.index('      <!-- ░░ 01 · Start from the problem ░░ -->')
s = s[:start] + HERO + '\n' + s[end:]

WORK = '''      <!-- ░░ 02 · Selected work — visual, labelled, honest ░░ -->
      <section class="section container" id="work" aria-labelledby="work-title">
        <header class="sec-head" data-reveal>
          <div>
            <p class="sec-head__no"><b>02</b><span data-ar="أعمال مختارة">SELECTED WORK</span></p>
            <h2 id="work-title"><span data-ar="اعرض الحرفة،">Show the craft,</span> <span class="grad-text" data-ar="لا قائمة الخدمات.">not the service list.</span></h2>
            <p class="lead" data-ar="دراسات مُعلَّنة لأنظمة العلامة والتغليف والمنتجات الرقمية وتجارب الويب، مع أعمال عملاء منشورة بحدود إثبات واضحة.">Labelled studies across brand systems, packaging, digital products and web experiences — alongside published client work with explicit evidence limits.</p>
          </div>
          <div class="sec-head__aside"><a class="text-link" href="/work/" data-track="cta_click" data-track-id="home-work-all"><span data-ar="البورتفوليو الكامل">Full portfolio</span><i class="flip" data-icon="arrowUpRight"></i></a></div>
        </header>
        <div class="work-strip">
          <a class="work-card panel" href="/work/bilingual-brand-system/" data-reveal data-track="case_study_view" data-track-id="bilingual-brand-system">
            <div class="work-card__art"><figure class="live-figure live-figure--plain" style="aspect-ratio:16/10;border:0;border-radius:0"><img src="/assets/media/brand-system.webp" alt="Illustrative brand-system artwork — not client work" data-ar-alt="عمل فني توضيحي لمنظومة علامة — ليس عمل عميل" width="1600" height="900" loading="lazy" decoding="async" /></figure></div>
            <div class="work-card__body"><span class="work-card__meta" data-ar="دراسة مفاهيمية · أنظمة العلامة">CONCEPT STUDY · BRAND SYSTEMS</span><h3 data-ar="منظومة علامة ثنائية اللغة">A bilingual brand system</h3><p data-ar="استراتيجية، وتركيب عربي/إنجليزي، ومكتبة رموز، ودليل حوكمة.">Strategy, a bilingual lockup, a token library and a governance guide.</p><span class="work-card__foot"><span data-ar="المشكلة · الدور · التنفيذ · النتيجة">Problem · Role · Execution · Outcome</span><b data-ar="افتح ↗">Open ↗</b></span></div>
          </a>
          <a class="work-card panel" href="/work/packaging-print-system/" data-reveal style="--d:.06s" data-track="case_study_view" data-track-id="packaging-print-system">
            <div class="work-card__art"><figure class="live-figure live-figure--plain" style="aspect-ratio:16/10;border:0;border-radius:0"><img src="/assets/media/packaging.webp" alt="Illustrative packaging artwork — not a client pack" data-ar-alt="عمل فني توضيحي للتغليف — ليس عبوة عميل" width="1600" height="900" loading="lazy" decoding="async" /></figure></div>
            <div class="work-card__body"><span class="work-card__meta" data-ar="دراسة مفاهيمية · التغليف والمطبوعات">CONCEPT STUDY · PACKAGING</span><h3 data-ar="من الرفّ إلى ملف الطباعة">Shelf to print-ready file</h3><p data-ar="قوالب قصّ، وCMYK، وهوامش، وحزمة تسليم للمطبعة.">Dielines, CMYK, bleed and a supplier hand-off pack.</p><span class="work-card__foot"><span data-ar="مواصفة إنتاج حقيقية">Real production spec</span><b data-ar="افتح ↗">Open ↗</b></span></div>
          </a>
          <a class="work-card panel" href="/work/web-experience-rebuild/" data-reveal style="--d:.12s" data-track="case_study_view" data-track-id="web-experience-rebuild">
            <div class="work-card__art"><figure class="live-figure live-figure--plain" style="aspect-ratio:16/10;border:0;border-radius:0"><img src="/assets/media/web-experience.webp" alt="Illustrative web-experience artwork — not a real site screenshot" data-ar-alt="عمل فني توضيحي لتجربة ويب — ليس لقطة موقع حقيقي" width="1600" height="900" loading="lazy" decoding="async" /></figure></div>
            <div class="work-card__body"><span class="work-card__meta" data-ar="دراسة مفاهيمية · تجارب الويب">CONCEPT STUDY · WEB</span><h3 data-ar="قبل / بعد: موقع يستحق المكالمة">Before / after a conversion site</h3><p data-ar="تراتبية الرسالة، وموضع الإثبات، ودعوة واحدة، ومسار قابل للقياس.">Message hierarchy, proof placement, one CTA and a measurable funnel.</p><span class="work-card__foot"><span data-ar="خطة قياس معلنة">Published measurement plan</span><b data-ar="افتح ↗">Open ↗</b></span></div>
          </a>
        </div>
        <p class="live-media-note" data-ar="هذه الأعمال توضيحية ومُعلَّنة كدراسات مفاهيمية، وليست أعمال عملاء. أعمال العملاء الحقيقية في /case-studies/ مع حدود الإثبات المنشورة.">These are labelled concept studies, not client work. Published client engagements are at <a href="/case-studies/">/case-studies/</a> with their evidence limits.</p>
      </section>
'''
start = s.index('      <!-- ░░ 02 · Selected work ░░ -->')
end = s.index('      <!-- ░░ 03 · The studio ░░ -->')
s = s[:start] + WORK + '\n' + s[end:]

POSITIONING = '''      <!-- ░░ 04 · The positioning pyramid (all 23 services, 4 pillars) ░░ -->
      <section class="section container" id="positioning" aria-labelledby="positioning-title">
        <header class="sec-head" data-reveal>
          <div>
            <p class="sec-head__no"><b>04</b><span data-ar="التموضع">THE POSITIONING</span></p>
            <h2 id="positioning-title"><span data-ar="أربعة مسارات.">Four pillars.</span> <span class="grad-text" data-ar="استوديو واحد.">One studio.</span></h2>
            <p class="lead" data-ar="بدل ظهور 23 خدمة بالوزن نفسه، يُنظَّم كل عرض تحت المسار الذي يملك قراره. لا نحذف خدمة؛ نجعل الخيار مفهومًا.">Instead of 23 equally weighted offers, every service sits under the pillar that owns its decision. We removed nothing; we made the choice legible.</p>
          </div>
          <div class="sec-head__aside"><a class="text-link" href="/services/"><span data-ar="كتالوج الخدمات الـ23">All 23 services</span><i class="flip" data-icon="arrowUpRight"></i></a></div>
        </header>
        <div class="pillars">
          <article class="pillar" data-reveal><span class="pillar__no">01</span><h3 data-ar="أنظمة العلامة">Brand Systems</h3><p data-ar="التموضع والهوية وأنظمة التصميم والتغليف والإخراج الفني — لغة بصرية واحدة تصمد أمام التوسّع.">Positioning, identity, design systems, packaging and creative direction — one visual language that survives scale.</p><ul class="pillar__list"><li data-ar="استراتيجية">Strategy</li><li data-ar="هوية">Identity</li><li data-ar="تغليف">Packaging</li><li data-ar="أنظمة تصميم">Design systems</li></ul><span class="pillar__count" data-ar="10 خدمات">10 offers</span><a class="pillar__link" href="/creative-services/"><span data-ar="استكشف المسار →">Explore the pillar →</span></a></article>
          <article class="pillar" data-reveal style="--d:.06s"><span class="pillar__no">02</span><h3 data-ar="المنتجات والمنصات الرقمية">Digital Products &amp; Platforms</h3><p data-ar="تصميم المنتجات والمواقع ومنتجات SaaS والأدوات الداخلية ولوحات المؤشرات — واجهات حول قرار لا حول شاشة.">Product design, websites, SaaS, internal tools and dashboards — interfaces built around a decision, not a screen.</p><ul class="pillar__list"><li data-ar="تصميم منتجات">Product UX</li><li data-ar="مواقع">Websites</li><li data-ar="SaaS">SaaS</li><li data-ar="لوحات مؤشرات">Dashboards</li></ul><span class="pillar__count" data-ar="6 خدمات">6 offers</span><a class="pillar__link" href="/services/product-design-ux/"><span data-ar="صفحة المنتجات →">Product design page →</span></a></article>
          <article class="pillar" data-reveal style="--d:.12s"><span class="pillar__no">03</span><h3 data-ar="التقنية والأتمتة">Technology &amp; Automation</h3><p data-ar="العمارة والتكاملات ومسارات الذكاء الاصطناعي وأتمتة الأعمال — المنظومة التي تقف خلف التجربة.">Architecture, integrations, AI workflows and business automation — the system behind the experience.</p><ul class="pillar__list"><li data-ar="عمارة مؤسسية">Architecture</li><li data-ar="تكاملات">Integrations</li><li data-ar="أتمتة">Automation</li><li data-ar="بيانات">Data</li></ul><span class="pillar__count" data-ar="6 خدمات">6 offers</span><a class="pillar__link" href="/services/ai-workflow-automation/"><span data-ar="صفحة الأتمتة →">Automation page →</span></a></article>
          <article class="pillar" data-reveal style="--d:.18s"><span class="pillar__no">04</span><h3 data-ar="الحلول المتخصصة">Specialist Solutions</h3><p data-ar="تقنية الرعاية الصحية والعمارة المؤسسية والبيانات والتحول — أعمال قطاعية بقيود معلنة.">Healthcare IT, enterprise architecture, data and transformation — domain work with published constraints.</p><ul class="pillar__list"><li data-ar="تقنية صحية">Healthcare IT</li><li data-ar="استشارات HIS">HIS advisory</li><li data-ar="منصات بيانات">Data platforms</li><li data-ar="تحوّل">Transformation</li></ul><span class="pillar__count" data-ar="7 خدمات">7 offers</span><a class="pillar__link" href="/services/healthcare-digital-solutions/"><span data-ar="صفحة الحلول الصحية →">Healthcare page →</span></a></article>
        </div>
      </section>

'''
s = s.replace('      <!-- ░░ 04 · Services ░░ -->', POSITIONING + '      <!-- ░░ 05 · Services ░░ -->', 1)

MARKETS = '''      <!-- ░░ Local markets & content funnel ░░ -->
      <section class="section container section--tight" id="markets" aria-labelledby="markets-title">
        <header class="sec-head" data-reveal><div><p class="sec-head__no"><b>07</b><span data-ar="الأسواق والمحتوى">MARKETS &amp; CONTENT</span></p><h2 id="markets-title"><span data-ar="اقرأ، قارن، ثم">Read, compare, then</span> <span class="grad-text" data-ar="اتخذ خطوة.">take a step.</span></h2></div></header>
        <div class="funnel">
          <div class="funnel__item"><small data-ar="المقال">01 · ARTICLE</small><a href="/blog/" data-ar="مركز الرؤى">Insights hub</a><p data-ar="10 مقالات ثنائية اللغة تشرح المشكلة قبل الحل.">10 bilingual articles that frame the problem first.</p></div>
          <div class="funnel__item"><small data-ar="الخدمة">02 · SERVICE</small><a href="/services/" data-ar="صفحة الخدمة">Standalone service page</a><p data-ar="النطاق والمخرجات والخطوات والأسئلة الشائعة.">Scope, deliverables, steps and FAQ.</p></div>
          <div class="funnel__item"><small data-ar="الأعمال">03 · WORK</small><a href="/work/" data-ar="دراسة حالة">Case study</a><p data-ar="المنهج والأدلة مُعلَّنة بوضوح.">Method and evidence, labelled.</p></div>
          <div class="funnel__item"><small data-ar="العميل المحتمل">04 · LEAD</small><a href="/book/" data-track="cta_click" data-track-id="funnel-book" data-ar="احجز مكالمة">Book a call</a><p data-ar="تأكيد حقيقي، وسجل عميل، ودعوة تقويم.">Real confirmation, CRM record and calendar invite.</p></div>
        </div>
        <div class="live-crosslinks" style="margin-top:16px">
          <div class="live-crosslink"><b data-ar="السعودية">Saudi Arabia</b><span data-ar="الخبر · نطاق جاهز للتوريد، ومحتوى عربي أولًا.">Al Khobar · procurement-ready scope, Arabic-first content.</span><a href="/saudi-arabia/"><span data-ar="الصفحة المحلية →">Local page →</span></a></div>
          <div class="live-crosslink"><b data-ar="مصر">Egypt</b><span data-ar="العبور · حرفة بصرية وهندسة في دورة إطلاق واحدة.">Al Obour · brand craft and engineering in one release.</span><a href="/egypt/"><span data-ar="الصفحة المحلية →">Local page →</span></a></div>
          <div class="live-crosslink"><b data-ar="المصادر">Resources</b><span data-ar="الكتب والمعاينات المجانية بعيدًا عن مسار التعاقد.">Books and free previews, separate from the sales journey.</span><a href="/resources/"><span data-ar="المصادر →">Resources →</span></a></div>
        </div>
      </section>

'''
s = s.replace('      <!-- ░░ 07 · CanvasOne ERP ░░ -->', MARKETS + '      <!-- ░░ 08 · CanvasOne ERP ░░ -->', 1)
s = s.replace('      <!-- ░░ 08 · Next step ░░ -->', '      <!-- ░░ 09 · Next step ░░ -->', 1)

# Primary closing CTA: point at the real booking flow.
s = s.replace('href="/contact/#book"', 'href="/book/"')
p.write_text(s, encoding='utf-8')
print('homepage growth applied')
