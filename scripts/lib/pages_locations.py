# -*- coding: utf-8 -*-
"""Local-market landing pages (KSA / Egypt), a Resources hub that separates
digital products from the main studio journey, and the public claims register.

Local pages publish only the contact details already present on the site — no
invented street address, no fake map pin, no unapproved branch. A Google
Business Profile link is deliberately omitted until the owner confirms it.
"""
from h import esc, icon, crumbs, closing, btn, page, sec_head, facts, ORG_ID, SITE, media_img
from data_growth import LOCATIONS, EVIDENCE, EVIDENCE_AR, SERVICE_LANDINGS, PILLARS

MEDIA = '/assets/media/'


def local(x):
    needs = ''.join(f'''<article class="case-step" data-reveal style="--d:{i * .06:.2f}s"><span>0{i + 1}</span><h3 data-ar="{esc(a[0])}">{esc(e[0])}</h3><p data-ar="{esc(a[1])}">{esc(e[1])}</p></article>''' for i, (e, a) in enumerate(zip(x['needs'], x['needs_ar'])))
    ld_local = {'@type': 'ProfessionalService', '@id': f'{SITE}/{x["slug"]}/#business',
                'name': 'Code & Canvas — ' + x['city'], 'url': f'{SITE}/{x["slug"]}/',
                'image': f'{SITE}{MEDIA}{x["media"]}.webp', 'telephone': x['phone'], 'email': 'info@codeandcanvas.net',
                'priceRange': 'Indicative ranges published in the service catalogue',
                'address': {'@type': 'PostalAddress', 'addressLocality': x['city'].split(' · ')[0], 'addressCountry': x['country']},
                'areaServed': x['city'], 'parentOrganization': {'@id': ORG_ID},
                'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday'], 'opens': '09:00', 'closes': '18:00'}]}
    city_closing_title = ('<span data-ar="مشروعك في">Your project in</span> '
                          '<span class="grad-text" data-ar="' + esc(x['city_ar']) + '">' + esc(x['city']) + '.</span>')
    body = f'''
      <section class="phero container phero--left" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('Locations', 'مواقعنا', None), (x['title'].replace('Code & Canvas in ', ''), x['title_ar'].replace('Code & Canvas في ', ''), None)])}
        <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="استوديو في منطقتك · عربي/إنجليزي">LOCAL STUDIO · ARABIC / ENGLISH</span></span>
        <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s" data-ar="{esc(x['title_ar'])}">{esc(x['title'])}</h1>
        <p class="hero__lead" data-reveal style="--d:.16s" data-ar="{esc(x['lead_ar'])}">{esc(x['lead'])}</p>
        <div class="hero__ctas" data-reveal style="--d:.24s">{btn('Book a 30-min call', 'احجز مكالمة 30 دقيقة', '/book/', 'primary', 'calendar')}{btn('Start a scoped inquiry', 'ابدأ استفسارًا بنطاق', '/contact/#message', 'glass', 'mail')}</div>
      </section>

      <section class="section container section--tight" aria-label="Local visual" data-ar-label="صورة السوق">
        <figure class="live-figure live-figure--wide">
          {media_img(x['media'], 'Abstract illustrative artwork for ' + x['city'], 'عمل فني تجريدي توضيحي — ' + x['city_ar'], sizes='(max-width: 720px) 92vw, 1200px', eager=True, fetchpriority='high')}
          <figcaption><span data-ar="{esc(x['city_ar'])}">{esc(x['city'])}</span><span class="live-figure__disclaimer" data-ar="عمل توضيحي مجرّد، ليس صورة مقر">ABSTRACT ILLUSTRATION · NOT AN OFFICE PHOTO</span></figcaption>
        </figure>
        <p class="live-media-note" data-ar="لا ننشر عنوان شارع أو خريطة أو ملف أعمال محلي قبل اعتماد المالك. بيانات الاتصال أدناه هي البيانات المنشورة فعلًا على الموقع.">No street address, map pin or business profile is published before owner approval. The contact details below are the ones already published on this site.</p>
      </section>

      <section class="section container section--flush-top" id="context" aria-labelledby="ctx-title">
        {sec_head('01', 'THE LOCAL CONTEXT', 'السياق المحلي',
                  '<span id="ctx-title" data-ar="ما نراه في هذا السوق.">What we see in this market.</span>',
                  'Written from the work we quote on this site — not from generic market statistics.',
                  'مكتوب من واقع الأعمال التي نعرضها في هذا الموقع — لا من إحصاءات سوق عامة.')}
        <div class="panel panel--deep" data-reveal><p class="lead" style="margin:0" data-ar="{esc(x['context_ar'])}">{esc(x['context'])}</p></div>
      </section>

      <section class="section container section--flush-top" id="needs" aria-labelledby="needs-title">
        {sec_head('02', 'WHAT TEAMS ASK FOR', 'ما تطلبه الفرق',
                  '<span id="needs-title" data-ar="ثلاثة أنماط عمل متكررة.">Three recurring briefs.</span>',
                  'Each one maps to a published service with a written scope.',
                  'كل نمط يقابل خدمة منشورة بنطاق مكتوب.')}
        <div class="case-steps">{needs}
        </div>
      </section>

      <section class="section container section--flush-top" id="contact" aria-labelledby="nap-title">
        {sec_head('03', 'CONTACT & HOURS', 'التواصل وساعات العمل',
                  '<span id="nap-title" data-ar="بيانات اتصال موحّدة.">One consistent contact record.</span>',
                  'The same phone number, email and hours appear across every page of the site.',
                  'رقم الهاتف والبريد وساعات العمل نفسها تظهر في كل صفحات الموقع.')}
        <div class="book-shell">
          <ul class="local-nap" data-reveal>
            <li><span data-ar="الموقع">Location</span><b data-ar="{esc(x['city_ar'])}">{esc(x['city'])}</b></li>
            <li><span data-ar="الهاتف">Phone</span><b><a class="ltr" href="tel:{esc(x['phone'].replace(' ', ''))}">{esc(x['phone'])}</a></b></li>
            <li><span data-ar="البريد">Email</span><b><a class="ltr" href="mailto:info@codeandcanvas.net">info@codeandcanvas.net</a></b></li>
            <li><span data-ar="واتساب">WhatsApp</span><b><a class="ltr" href="https://wa.me/966545520750" target="_blank" rel="noopener">+966 54 552 0750</a></b></li>
            <li><span data-ar="ساعات العمل">Office hours</span><b class="ltr" data-ar="{esc(x['hours_ar'])}">{esc(x['hours'])}</b></li>
            <li><span data-ar="اللغات">Languages</span><b data-ar="العربية · الإنجليزية">Arabic · English</b></li>
          </ul>
          <aside class="sls-side">
            <div class="panel tier" data-reveal><h3 data-ar="ابدأ من هنا">Start here</h3><p style="margin:8px 0" data-ar="مكالمة 30 دقيقة تحدّد النطاق والملاءمة والخطوة التالية.">A 30-minute call to fix scope, fit and the next step.</p>{btn('Book a call', 'احجز مكالمة', '/book/', 'primary', 'calendar')}</div>
            <div class="panel tier" data-reveal style="--d:.06s"><h3 data-ar="السوق الآخر">The other market</h3><p style="margin:8px 0" data-ar="الفريق نفسه، ووثيقة نطاق واحدة، وخطة تسليم واحدة عبر السوقين.">The same team, one scope document and one delivery plan across both markets.</p><a class="text-link" href="{'/egypt/' if x['slug'] == 'saudi-arabia' else '/saudi-arabia/'}"><span data-ar="{'مصر ←' if x['slug'] == 'saudi-arabia' else 'السعودية ←'}">{'Egypt →' if x['slug'] == 'saudi-arabia' else 'Saudi Arabia →'}</span></a></div>
          </aside>
        </div>
      </section>

      {closing('WORK WITH THE STUDIO', 'اعمل مع الاستوديو',
              city_closing_title,
              'Send the problem, or pick a slot. We reply with a clear scope and one next step.',
              'أرسل المشكلة أو اختر موعدًا. نرد بنطاق واضح وخطوة واحدة تالية.',
              [btn('Start an inquiry', 'ابدأ استفسارًا', '/contact/', 'primary', 'mail'), btn('Explore services', 'استكشف الخدمات', '/services/', 'glass', 'layers')])}
'''
    return page(f'/{x["slug"]}/', title=f'{x["title"]} — Brand, Product & Systems · Code & Canvas',
                title_ar=f'{x["title_ar"]} — العلامة والمنتج والأنظمة · Code & Canvas',
                desc=x['lead'], desc_ar=x['lead_ar'], nav='about', body=body,
                og_image=f'/assets/brand/og/{x["og"]}.png', view_track='service_view', ld=[ld_local])


def resources():
    posts = ''.join(f'<div class="live-crosslink"><b data-ar="مقال">Insight</b><span data-ar="إطار أو مسألة من مشاريع فعلية.">A framework or a problem from live engagements.</span><a href="/blog/"><span data-ar="مركز الرؤى →">Insights hub →</span></a></div>' for _ in range(1))
    landings = ''.join(f'<a class="pill" href="/services/{esc(x["slug"])}/" data-ar="{esc(x["title_ar"])}">{esc(x["title"])}</a>' for x in SERVICE_LANDINGS)
    body = f'''
      <section class="phero container phero--left" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('Resources', 'المصادر', None)])}
        <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="مصادر · كتب · رؤى · أعمال">RESOURCES · BOOKS · INSIGHTS · WORK</span></span>
        <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s"><span data-ar="اقرأ قبل أن">Read before</span><br /><span class="grad-text" data-ar="تشتري الحل.">you buy the solution.</span></h1>
        <p class="hero__lead" data-reveal style="--d:.16s" data-ar="جمعنَا المصادر التعليمية في مكان واحد بعيدًا عن مسار التعاقد الأساسي: كتب بمعاينات مجانية، ومقالات، ودراسات حالة، وصفحات خدمات. الشراء الإلكتروني والحسابات غير متاحين حاليًا، ولن نعرض عربة أو دفعًا وهميًا.">Educational resources now live in one place, separate from the main studio journey: books with free previews, articles, case studies and service pages. Online purchasing and accounts are not available yet, and we do not show a pretend cart or checkout.</p>
        <div class="hero__ctas" data-reveal style="--d:.24s">{btn('Browse the books', 'تصفّح الكتب', '/books/', 'primary', 'book')}{btn('Read the insights', 'اقرأ الرؤى', '/blog/', 'glass', 'layers')}{btn('See the work', 'شاهد الأعمال', '/work/', 'ghost', 'arrowUpRight')}</div>
      </section>

      <section class="section container section--tight" aria-label="Resources visual" data-ar-label="صورة المصادر">
        <figure class="live-figure live-figure--wide">
          {media_img('studio-atmosphere', 'Illustrative studio artwork for the resources library', 'عمل فني توضيحي لمكتبة المصادر', sizes='(max-width: 720px) 92vw, 1200px', eager=True)}
          <figcaption><span data-ar="مكتبة المصادر">RESOURCES LIBRARY</span><span class="live-figure__disclaimer" data-ar="عمل توضيحي">ILLUSTRATIVE ARTWORK</span></figcaption>
        </figure>
      </section>

      <section class="section container section--flush-top" id="library" aria-labelledby="lib-title">
        {sec_head('01', 'WHAT IS AVAILABLE', 'المتاح الآن', '<span id="lib-title" data-ar="أربعة مسارات للمعرفة.">Four paths into the material.</span>',
                  'Everything here is public and free to read. No account is required.',
                  'كل ما هنا عام ومجاني للقراءة. لا يحتاج حسابًا.')}
        <div class="live-crosslinks" data-reveal>
          <div class="live-crosslink"><b data-ar="4 كتب ومعاينات">4 books &amp; previews</b><span data-ar="صفحات تعريف ومعاينات قارئ عامة؛ المحتوى المدفوع غير منشور.">Landing pages and public reader previews; paid content is not published.</span><a href="/books/"><span data-ar="افتح المكتبة →">Open the library →</span></a></div>
          <div class="live-crosslink"><b data-ar="10 مقالات">10 articles</b><span data-ar="مقالات كاملة بالعربية والإنجليزية، بمسار يصل للخدمة والدراسة والاستفسار.">Full bilingual articles, each linking to a service, a study and an inquiry.</span><a href="/blog/"><span data-ar="مركز الرؤى →">Insights hub →</span></a></div>
          <div class="live-crosslink"><b data-ar="دراسات حالة">Case studies</b><span data-ar="أعمال منتجات مُعلَّنة، ودراسات مفاهيمية إبداعية مُصنَّفة بوضوح.">Labelled product cases and clearly flagged creative concept studies.</span><a href="/work/"><span data-ar="الأعمال →">Work →</span></a></div>
          <div class="live-crosslink"><b data-ar="7 صفحات خدمات رئيسية">7 flagship service pages</b><span data-ar="نطاق ومخرجات وخطوات وأسئلة شائعة ودعوة خاصة بكل خدمة.">Scope, deliverables, steps, FAQ and a dedicated CTA for each.</span><a href="/services/"><span data-ar="الخدمات →">Services →</span></a></div>
        </div>
      </section>

      <section class="section container section--flush-top" id="commerce" aria-labelledby="commerce-title">
        {sec_head('02', 'DIGITAL PRODUCTS — HONEST STATUS', 'المنتجات الرقمية — الحالة بصراحة',
                  '<span id="commerce-title" data-ar="لا حسابات، لا دفع، لا ادّعاء.">No accounts. No payment. No pretence.</span>',
                  'Books, login, cart, checkout and account screens are kept out of the main studio journey until a real commerce release exists.',
                  'صفحات الكتب والدخول والسلة والدفع والحساب مستبعدة من مسار الاستوديو الأساسي حتى يتوفر إصدار تجاري حقيقي.')}
        <div class="case-steps">
          <article class="case-step" data-reveal><span>01 · NOW</span><h3 data-ar="المتاح الآن">Available now</h3><p data-ar="معاينات عامة، وقائمة كتب محفوظة محليًا على جهازك، واستفسار عن التوفر عبر رسالة.">Public previews, a shortlist saved locally on your device, and an availability inquiry by message.</p></article>
          <article class="case-step" data-reveal style="--d:.06s"><span>02 · NOT YET</span><h3 data-ar="غير المتاح">Not available</h3><p data-ar="لا تسجيل دخول، ولا كلمات مرور، ولا ملكية كتب، ولا دفع إلكتروني، ولا فواتير أو إيصالات.">No sign-in, passwords, book ownership, online payment, orders or receipts.</p></article>
          <article class="case-step" data-reveal style="--d:.12s"><span>03 · LATER</span><h3 data-ar="لاحقًا">A real release</h3><p data-ar="يتطلب خوادم مصادقة وجلسات وأسعار من جانب الخادم وتأكيد دفع موقع وتسليم محتوى محمي.">Requires server authentication, sessions, server-side prices, signed payment webhooks and protected content delivery.</p></article>
        </div>
      </section>

      <section class="section container section--flush-top" aria-label="Service links" data-ar-label="روابط الخدمات">
        <p class="kicker"><span data-ar="ابدأ من خدمة">START FROM A SERVICE</span></p>
        <div class="pill-list" style="margin-top:14px">{landings}
        </div>
      </section>

      {closing('NEED A REAL PROJECT?', 'تحتاج مشروعًا حقيقيًا؟',
              '<span data-ar="المصادر للقراءة.">Resources are for reading.</span> <span class="grad-text" data-ar="المشاريع تبدأ بمحادثة.">Projects start with a conversation.</span>',
              'Tell us the problem — or book a 30-minute call with the right specialist.',
              'أخبرنا بالمشكلة — أو احجز مكالمة 30 دقيقة مع المتخصص المناسب.',
              [btn('Contact the studio', 'تواصل مع الاستوديو', '/contact/', 'primary', 'mail'), btn('Book a call', 'احجز مكالمة', '/book/', 'glass', 'calendar')])}
'''
    return page('/resources/', title='Resources & Digital Products — Code & Canvas',
                title_ar='المصادر والمنتجات الرقمية — Code & Canvas',
                desc='Books with free previews, bilingual insights, labelled case studies and standalone service pages — with an explicit, honest status for digital commerce.',
                desc_ar='كتب بمعاينات مجانية ورؤى ثنائية اللغة ودراسات حالة مُعلَّنة وصفحات خدمات مستقلة — مع بيان صريح وصادق لحالة التجارة الرقمية.',
                nav='resources', body=body, og_image='/assets/brand/og/resources.png')


def claims():
    rows = ''.join(f'''<tr><td data-ar="{esc(EVIDENCE_AR[i][0])}">{esc(e[0])}</td><td><span class="st {"st--ok" if e[1] in ("Published", "Resolved") else "st--pending" if e[1] in ("Qualified", "Editorial") else "st--removed"}">{esc(e[1])}</span></td><td data-ar="{esc(EVIDENCE_AR[i][2])}">{esc(e[2])}</td><td data-ar="{esc(EVIDENCE_AR[i][3])}">{esc(e[3])}</td><td data-ar="{esc(EVIDENCE_AR[i][4])}">{esc(e[4])}</td></tr>''' for i, e in enumerate(EVIDENCE))
    body = f'''
      <section class="phero container phero--left" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('Claims & Evidence', 'الادعاءات والأدلة', None)])}
        <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="سجل عام · يُحدَّث مع كل إصدار">PUBLIC REGISTER · UPDATED WITH EACH RELEASE</span></span>
        <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s"><span data-ar="كل رقم،">Every number,</span><br /><span class="grad-text" data-ar="بحالة معلنة.">with a stated status.</span></h1>
        <p class="hero__lead" data-reveal style="--d:.16s" data-ar="هذا سجل الادعاءات والأدلة للموقع. أي رقم لا يمكن إثباته يُعاد صياغته أو يُحذف، وأي حالة «مقيَّدة» تظل كذلك حتى يعتمدها صاحبها.">This is the site’s claim and evidence register. Any number we cannot evidence is rewritten or removed, and any “qualified” item stays that way until its owner approves it.</p>
        <div class="hero__ctas" data-reveal style="--d:.24s">{btn('Read the register', 'اقرأ السجل', '#register', 'primary', 'arrowDown')}{btn('See the work', 'شاهد الأعمال', '/work/#evidence', 'glass', 'layers')}</div>
      </section>

      <section class="section container section--flush-top" id="register" aria-labelledby="reg-title">
        {sec_head('01', 'THE REGISTER', 'السجل', '<span id="reg-title" data-ar="منشور · مقيَّد · محذوف · محسوم.">Published · Qualified · Removed · Resolved.</span>',
                  'A claim is not a marketing asset until its source exists.',
                  'الادعاء ليس أصلًا تسويقيًا حتى يوجد مصدره.')}
        <div class="evidence-scroll" data-reveal tabindex="0" role="region" aria-label="Claims and evidence table" data-ar-label="جدول الادعاءات والأدلة"><table class="evidence-table">
          <thead><tr><th data-ar="الادعاء">Claim</th><th data-ar="الحالة">Status</th><th data-ar="المعاملة الحالية">Current treatment</th><th data-ar="المطلوب قبل النشر الأقوى">Required before a stronger claim</th><th data-ar="المالك">Owner</th></tr></thead>
          <tbody>{rows}</tbody>
        </table></div>
      </section>

      <section class="section container section--flush-top" id="policy" aria-labelledby="policy-title">
        {sec_head('02', 'OUR PUBLICATION RULE', 'قاعدة النشر', '<span id="policy-title" data-ar="الإثبات قبل الصياغة.">Evidence before wording.</span>',
                  'Four rules applied to every number, certificate, testimonial and image on this site.',
                  'أربع قواعد تُطبَّق على كل رقم وشهادة وصورة في هذا الموقع.')}
        <div class="case-steps">
          <article class="case-step" data-reveal><span>01</span><h3 data-ar="مصدر مؤرّخ">Dated source</h3><p data-ar="خط أساس، ومنهجية، ومقام، وتاريخ، وصاحب. بلا ذلك لا يُنشر الرقم.">A baseline, method, denominator, date and owner. Without them the number is not published.</p></article>
          <article class="case-step" data-reveal style="--d:.06s"><span>02</span><h3 data-ar="تعريف غير متكرر">Non-overlapping definition</h3><p data-ar="العلامة تُحسب مرة واحدة، والقطاع يُصنَّف، وسنوات المؤسسين تُفصل عن عمر الاستوديو.">A brand is counted once, sectors are classified, and founder experience is separated from the studio’s age.</p></article>
          <article class="case-step" data-reveal style="--d:.12s"><span>03</span><h3 data-ar="صورة ≠ إثبات">An image is not evidence</h3><p data-ar="العمل الفني التوضيحي يُعلَّن، ولقطات العملاء تحتاج إذنًا، ونتائج الأعمال تحتاج قياسًا.">Illustrative art is labelled, client screenshots need permission, business outcomes need measurement.</p></article>
          <article class="case-step" data-reveal style="--d:.18s"><span>04</span><h3 data-ar="حذف أو إعادة صياغة">Remove or rewrite</h3><p data-ar="إذا تعذّر الإثبات نُعيد الصياغة إلى وصف نوعي صادق أو نشيل الادعاء بالكامل.">If proof is unavailable, we rewrite into honest qualitative wording or remove the claim entirely.</p></article>
        </div>
      </section>

      {closing('QUESTIONS ABOUT A CLAIM?', 'عندك سؤال عن ادعاء؟',
              '<span data-ar="اسألنا مباشرة.">Ask us directly.</span> <span class="grad-text" data-ar="سنقول لك المصدر.">We’ll name the source.</span>',
              'If a number on this site is unclear, write to us and we will point to its evidence — or correct it.',
              'إن كان رقم في الموقع غير واضح، راسلنا وسنشير إلى مصدره — أو نصحّحه.',
              [btn('Contact the studio', 'تواصل مع الاستوديو', '/contact/', 'primary', 'mail'), btn('Read the policies', 'اقرأ السياسات', '/privacy-policy/', 'glass', 'shield')])}
'''
    return page('/claims/', title='Claims & Evidence Register — Code & Canvas',
                title_ar='سجل الادعاءات والأدلة — Code & Canvas',
                desc='A public register of every number and claim on the site: published, qualified, removed or resolved, with the evidence required to strengthen it.',
                desc_ar='سجل عام لكل رقم وادعاء في الموقع: منشور أو مقيَّد أو محذوف أو محسوم، مع الإثبات المطلوب لتقويته.',
                nav='about', body=body, og_image='/assets/brand/og/claims.png')


def build():
    return [local(x) for x in LOCATIONS] + [resources(), claims()]
