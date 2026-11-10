# -*- coding: utf-8 -*-
"""/evidence/ — how the studio decides.

A buyer's real question is not "which service do I buy" but "can these people
reason about my problem". This page answers that with published decisions
instead of new claims: for each challenge it states the decision we would
recommend, what we would refuse to do, which published engagement carries it,
and exactly what evidence exists today.

Every number on this page is copied from the service catalogue or from a
published page, and every claim carries its evidence status — the same rule as
/claims/. Nothing here is a client outcome, and no screenshot is implied.
"""
from h import esc, icon, crumbs, closing, btn, page, sec_head, svc_index_row
from catalog import SERVICES

# (kicker, title, title_ar, body, body_ar, decision, decision_ar, refuse, refuse_ar, codes)
DECISIONS = [
    dict(
        n='01',
        kicker='INTEGRATION', kicker_ar='التكامل',
        title='Our systems don’t talk to each other',
        title_ar='أنظمتنا لا تتحدث مع بعضها',
        body='Three vendors, no single owner, and a monthly report that is retyped by hand. The instinct is to buy another tool; the cause is that no one owns the data contract between the tools you already have.',
        body_ar='ثلاثة مورّدين، ولا مالك واحد للقرار، وتقرير شهري يُعاد كتابته يدويًا. الغريزة تقول «اشترِ أداة أخرى»؛ والسبب الحقيقي أنه لا أحد يملك عقد البيانات بين الأدوات الموجودة عندك.',
        decision='Draw the value stream and the data contracts first, then decide what to integrate, replace or retire — in that order, with the cost of each written down.',
        decision_ar='نرسم تدفق القيمة وعقود البيانات أولًا، ثم نقرر ما يُدمج وما يُستبدل وما يُوقف — بهذا الترتيب، مع تكلفة مكتوبة لكل خيار.',
        refuse='We will not start by demoing a platform. A tool decision made before the data model is a decision someone will pay for twice.',
        refuse_ar='لن نبدأ بعرض منصة. قرار أداة يُتخذ قبل نموذج البيانات هو قرار سيدفعه العميل مرتين.',
        codes=['AB-01', 'AB-04'],
    ),
    dict(
        n='02',
        kicker='HEALTHCARE', kicker_ar='الرعاية الصحية',
        title='We’re choosing an HIS or an ERP',
        title_ar='نختار نظام HIS أو ERP',
        body='Every vendor demo looks the same, and nobody owns the feasibility study or the risk register. The choice is usually made on the demo, then justified for two years.',
        body_ar='كل عرض تجريبي يشبه الآخر، ولا أحد يملك دراسة الجدوى أو سجل المخاطر. القرار يُتخذ عادةً على العرض التجريبي، ثم يُبرَّر لعامين.',
        decision='Score the vendors against your own clinical workflows and the readiness criteria you are actually judged by (EMRAM stage, CBAHI readiness, NORA interoperability), then negotiate from a written gap report.',
        decision_ar='نُقيّم المورّدين مقابل مساراتك السريرية ومعايير الجاهزية التي تُحاسَب عليها فعلًا (مرحلة EMRAM، جاهزية CBAHI، التشغيل البيني NORA)، ثم نتفاوض من تقرير فجوات مكتوب.',
        refuse='We do not take a commission from any vendor, and we do not run a selection we are not willing to lose.',
        refuse_ar='لا نأخذ عمولة من أي مورّد، ولا نقود عملية اختيار غير مستعدين لخسارتها.',
        codes=['HC-03', 'HC-05'],
    ),
    dict(
        n='03',
        kicker='BRAND', kicker_ar='العلامة',
        title='Our brand doesn’t match our ambition',
        title_ar='علامتنا لا تعكس طموحنا',
        body='The logo is fine; the system behind it is missing. Every new deck, post and event re-decides the same things, so the brand drifts while the business grows.',
        body_ar='الشعار جيد؛ لكن المنظومة خلفه غائبة. كل عرض تقديمي ومنشور وفعالية يعيد تقرير الشيء نفسه، فتتآكل العلامة بينما ينمو العمل.',
        decision='Position first, then a system a team can operate without us: type, grid, colour, tone, and the rules that keep Arabic and English consistent.',
        decision_ar='التموضع أولًا، ثم منظومة يستطيع الفريق تشغيلها بدوننا: الخط والشبكة واللون والنبرة والقواعد التي تحفظ اتساق العربية والإنجليزية.',
        refuse='We will not sell a logo sprint as a brand system, and we will not deliver a guideline nobody can apply on a Tuesday.',
        refuse_ar='لن نبيع «سباق شعار» على أنه منظومة علامة، ولن نسلّم دليلًا لا يمكن تطبيقه يوم ثلاثاء عادي.',
        codes=['MA-02', 'MA-03'],
    ),
    dict(
        n='04',
        kicker='LAUNCH', kicker_ar='الإطلاق',
        title='We’re launching and need both',
        title_ar='نُطلق ونحتاج الاثنين',
        body='A new clinic, product or market entry needs identity and a working digital front at the same time — usually with one budget and one date that cannot slip.',
        body_ar='عيادة جديدة أو منتج جديد أو دخول سوق يحتاج الهوية وواجهة رقمية عاملة في الوقت نفسه — عادةً بميزانية واحدة وتاريخ واحد لا يتأخر.',
        decision='One brief, one timeline, two owners: brand and build run in the same weeks, with a single hand-over pack instead of two vendors blaming each other.',
        decision_ar='موجز واحد وجدول واحد ومالكان: الهوية والبناء في الأسابيع نفسها، بحزمة تسليم واحدة بدلًا من مورّدين يتبادلان اللوم.',
        refuse='We will not take a launch date we cannot hold, and we will not hide a dependency inside “phase two”.',
        refuse_ar='لن نقبل تاريخ إطلاق لا نستطيع الالتزام به، ولن نخفي أي اعتماديات داخل «المرحلة الثانية».',
        codes=['CC-01', 'HC-01'],
    ),
]

# Evidence status for each case, stated in plain language.
STATUS = [
    ('Documented scope', 'نطاق موثّق',
     'Brief, constraints, role, approach and artifacts are published on /work/.',
     'الموجز والقيود والدور والمنهج والمخرجات منشورة على /work/.', 'ok'),
    ('No client screenshot', 'لا لقطة من العميل',
     'Screens contain client data, so none is published. Diagrams are scope illustrations and say so.',
     'الشاشات تحتوي بيانات عميل، لذلك لا تُنشر. الرسوم توضيحية للنطاق ومعلَنة كذلك.', 'warn'),
    ('No measured outcome', 'لا نتيجة مُقاسة',
     'No independent, measured commercial result has been supplied for publication. We do not invent one.',
     'لا توجد نتيجة تجارية مُقاسة ومستقلة مُعتمدة للنشر. ولا نختلق واحدة.', 'warn'),
    ('Public evidence', 'دليل عام',
     'Where a project is public (Zad), the live app itself is the evidence — anyone can open it.',
     'حيث يكون المشروع عامًا (زاد)، فالتطبيق الحي نفسه هو الدليل — يمكن لأي شخص فتحه.', 'ok'),
]

TIERS = [
    ('Entry', 'مدخل',
     'A single asset with a fixed checklist: logo sprint, one-page site, social kit.',
     'أصل واحد بقائمة تحقق ثابتة: سباق شعار، موقع من صفحة واحدة، حزمة سوشيال.',
     'MA-01 · MA-05 · MA-09'),
    ('Professional', 'احترافي',
     'A system that a team can operate: identity essentials, full brand system, custom platform.',
     'منظومة يستطيع الفريق تشغيلها: أساسيات الهوية، منظومة العلامة الكاملة، منصة مخصصة.',
     'MA-02 · MA-03 · MA-06'),
    ('Strategic', 'استراتيجي',
     'Decisions and architecture: enterprise architecture, data, healthcare transformation, launch.',
     'قرارات وعمارة: العمارة المؤسسية، البيانات، التحول الصحي، الإطلاق.',
     'AB-01 · AB-03 · HC-02 · CC-01'),
    ('Enterprise', 'مؤسسي',
     'Multi-phase, multi-stakeholder programmes quoted individually after a scoped assessment.',
     'برامج متعددة المراحل وأصحاب المصلحة تُسعَّر فرديًا بعد تقييم بنطاق محدد.',
     'AB-02 · AB-05 · HC-05'),
]


def decision_block(d, i):
    eng = ''.join(
        f'<li><a href="/{SERVICES[c]["track"] and {"technology": "technology-services", "creative": "creative-services", "healthcare": "healthcare", "combined": "services"}[SERVICES[c]["track"]]}/#{c.lower()}">'
        f'<span class="idx__code">{c}</span>'
        f'<span class="idx__title" data-ar="{esc(SERVICES[c]["title_ar"])}">{esc(SERVICES[c]["title"])}</span>'
        f'<span class="idx__price ltr">{esc(SERVICES[c]["price"])}</span></a></li>'
        for c in d['codes'])
    return f'''
      <article class="decision" id="decision-{d['n']}" data-reveal{' style="--d:%.2fs"' % (i * .05) if i else ''}>
        <header class="decision__head">
          <span class="decision__no">{d['n']}</span>
          <p class="kicker"><span data-ar="{esc(d['kicker_ar'])}">{d['kicker']}</span></p>
          <h3 class="decision__title" data-ar="{esc(d['title_ar'])}">{esc(d['title'])}</h3>
          <p class="decision__situation" data-ar="{esc(d['body_ar'])}">{esc(d['body'])}</p>
        </header>
        <div class="decision__grid">
          <div class="decision__cell decision__cell--do">
            <b data-ar="القرار الذي سنوصي به">What we would decide</b>
            <p data-ar="{esc(d['decision_ar'])}">{esc(d['decision'])}</p>
          </div>
          <div class="decision__cell decision__cell--refuse">
            <b data-ar="ما نرفض فعله">What we refuse</b>
            <p data-ar="{esc(d['refuse_ar'])}">{esc(d['refuse'])}</p>
          </div>
          <div class="decision__cell decision__cell--carry">
            <b data-ar="الخدمات المنشورة التي تحمل القرار">Published services that carry it</b>
            <ul class="idx idx--compact">{eng}</ul>
          </div>
        </div>
      </article>'''


def build():
    decisions = ''.join(decision_block(d, i) for i, d in enumerate(DECISIONS))
    status_rows = ''.join(
        f'<tr><td data-ar="{esc(a)}">{esc(e)}</td>'
        f'<td><span class="st st--{"ok" if cls == "ok" else "pending"}">{cls == "ok" and "Published" or "Stated limit"}</span></td>'
        f'<td data-ar="{esc(ar)}">{esc(en)}</td></tr>'
        for e, a, en, ar, cls in STATUS)
    tiers = ''.join(
        f'<article class="tiercta" data-reveal><p class="kicker"><span data-ar="{esc(a)}">{e}</span></p>'
        f'<p data-ar="{esc(desc_ar)}">{esc(desc)}</p><span class="tiercta__codes ltr">{codes}</span></article>'
        for e, a, desc, desc_ar, codes in TIERS)

    body = f'''
      <!-- ░░ Hero ░░ -->
      <section class="phero container phero--left" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('Evidence', 'الإثبات', None)])}
        <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="كيف نقرر · وما الذي نرفضه">HOW WE DECIDE · WHAT WE REFUSE</span></span>
        <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s"><span data-ar="الحكم قبل الحرفة.">Judgement before craft.</span><br /><span class="grad-text" data-ar="بالقرارات، لا بالشعارات.">Stated as decisions, not claims.</span></h1>
        <p class="hero__lead" data-reveal style="--d:.16s" data-ar="أصعب سؤال أمام أي استوديو ليس «ماذا تعملون؟» بل «هل تفكرون في مشكلتي بنفس الطريقة التي أفكر بها؟». هذه الصفحة تجيب بأربعة قرارات مكتوبة: ما الذي سنوصي به، وما الذي نرفض فعله، وأي خدمة منشورة تحمل القرار، وما الدليل المتاح اليوم بالضبط.">The hardest question to ask a studio is not “what do you do?” but “do you reason about my problem the way I do?”. This page answers it with four written decisions: what we would recommend, what we refuse to do, which published service carries it, and exactly what evidence exists today.</p>
        <div class="hero__ctas" data-reveal style="--d:.24s">{btn('Open the work index', 'افتح فهرس الأعمال', '/work/', 'glass')}{btn('Read the claims register', 'اقرأ سجل الادعاءات', '/claims/', 'ghost')}</div>
      </section>

      <!-- ░░ Decisions ░░ -->
      <section class="section container" id="decisions" aria-labelledby="decisions-title">
        {sec_head('01', 'FOUR DECISIONS', 'أربعة قرارات',
                  '<span id="decisions-title" data-ar="المشكلة، القرار، والرفض.">The situation, the decision, and the refusal.</span>',
                  'Each block is the shape of a real conversation: how we read the situation, what we would actually do, what we will not do, and which published engagement delivers it.',
                  'كل بلوك بشكل محادثة حقيقية: كيف نقرأ الموقف، وما الذي سنفعله فعلًا، وما الذي لن نفعله، وأي مشروع منشور ينفّذه.')}
        <div class="decisions">{decisions}
        </div>
      </section>

      <!-- ░░ Evidence status ░░ -->
      <section class="section container section--flush-top" id="status" aria-labelledby="status-title">
        {sec_head('02', 'EVIDENCE STATUS', 'حالة الدليل',
                  '<span id="status-title" data-ar="ما هو منشور، وما هو حدّ مقصود.">What is published, and what is a stated limit.</span>',
                  'A portfolio is only useful if you can tell the difference between proof and illustration. This is the honest split for the work currently shown.',
                  'الأعمال لا تنفع إلا إذا استطعت التمييز بين الدليل والرسم التوضيحي. هذا هو الفصل الأمين للعمل المعروض حاليًا.')}
        <div class="evidence-scroll" data-reveal tabindex="0" role="region" aria-label="Evidence status table" data-ar-label="جدول حالة الدليل"><table class="evidence-table">
            <thead><tr><th data-ar="الحالة">Item</th><th data-ar="الحالة">Status</th><th data-ar="التفصيل">Detail</th></tr></thead>
            <tbody>{status_rows}</tbody>
          </table>
        </div>
        <p class="live-media-note" data-ar="هذا الجدول يصف حدود الإثبات لا جودة العمل. أي نتيجة تجارية ستُضاف هنا فقط بمصدر مقاس وفترة وفاتورة عميل.">This table describes the limits of evidence, not the quality of the work. Any commercial result will be added here only with a measured source, a period, and client permission.</p>
      </section>

      <!-- ░░ Engagement tiers ░░ -->
      <section class="section container section--flush-top" id="tiers" aria-labelledby="tiers-title">
        {sec_head('03', 'ENGAGEMENT TIERS', 'مستويات التعاقد',
                  '<span id="tiers-title" data-ar="سعر واحد لا يصف استوديو.">One price does not describe a studio.</span>',
                  'Published catalogue prices start low because a logo sprint is a small job — it is not the studio. Four tiers, so you can place yourself without guessing.',
                  'أسعار الكتالوج تبدأ منخفضة لأن سباق الشعار مهمة صغيرة — لكنه ليس الاستوديو. أربعة مستويات حتى تحدد موقعك بلا تخمين.')}
        <div class="tiers">{tiers}
        </div>
      </section>

      <!-- ░░ Next step ░░ -->
{closing('NEXT STEP', 'الخطوة التالية',
         '<span data-ar="قولوا لنا أين تظنون أن المشكلة —">Tell us where you think the problem is —</span> <span class="grad-text" data-ar="وسنقول لكم بصراحة إن كنا الخطأ.">and we will say plainly if we are the wrong fit.</span>',
         'A 30-minute call, in Arabic or English. You get a written next step whether or not we work together.',
         'مكالمة 30 دقيقة، بالعربية أو الإنجليزية. تحصل على خطوة تالية مكتوبة سواء عملنا معًا أو لا.',
         [btn('Book a 30-min call', 'احجز مكالمة 30 دقيقة', '/book/'), btn('Read the methodology', 'اقرأ المنهجية', '/methodology/', 'glass')])}
'''
    return [page('/evidence/', title='Evidence — how we decide — Code & Canvas',
                 title_ar='الإثبات — كيف نقرر — Code & Canvas',
                 desc='Four written decisions: how Code & Canvas reads a situation, what it would recommend, what it refuses, which published service carries it, and what evidence exists today.',
                 desc_ar='أربعة قرارات مكتوبة: كيف يقرأ Code & Canvas الموقف، وما يوصي به، وما يرفضه، وأي خدمة منشورة تحمله، وما الدليل المتاح اليوم.',
                 nav='work', body=body, og_image='/assets/brand/og/work.png')]
