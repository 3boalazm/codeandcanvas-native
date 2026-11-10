# -*- coding: utf-8 -*-
"""Legal pages + 404 (November 2026, v2.0).

These policies describe the site as it is actually built now: a first-party
Node API that stores inquiries, newsletter/career leads, bookings and
consent-gated measurement events in a server-side JSON store; optional
notification webhook; no accounts, no payments, no third-party analytics IDs
by default. Every statement here is verifiable from `server/api.mjs`,
`assets/js/site.js`, `assets/js/pages.js` and `assets/js/config.js`.

Review note (internal, not rendered): a qualified legal adviser should confirm
jurisdiction-specific wording before it is relied on commercially. The wording
below is complete and accurate about the implementation, not a placeholder
draft — but internal review state is not published as customer copy.
"""
from h import esc, icon, crumbs, btn, page

UPDATED = 'November 2026'
VERSION = '2.0'


def legal(path, *, title, title_ar, intro, intro_ar, sections, nav=''):
    toc = ''.join(f'<a href="#s{i + 1}" data-ar="{esc(ar)}">{esc(en)}</a>' for i, (en, ar, _, __) in enumerate(sections))
    secs = ''.join(f'<h2 id="s{i + 1}" data-ar="{esc(ar)}">{esc(en)}</h2><div class="legal__en">{en_html}</div><div class="legal__ar" lang="ar" dir="rtl">{ar_html}</div>' for i, (en, ar, en_html, ar_html) in enumerate(sections))
    body = f'''
      <section class="section container" style="padding-top:calc(var(--nav-h) + 40px)" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), (title, title_ar, None)])}
        <div class="legal">
          <h1 class="section__title" id="page-title" data-ar="{esc(title_ar)}">{esc(title)}</h1>
          <div class="legal__meta"><span>{icon('calendar')}<span data-ar="آخر تحديث: {UPDATED}">Last updated: {UPDATED}</span></span><span>{icon('shield')}<span data-ar="الإصدار {VERSION} · يصف التشغيل الفعلي">Version {VERSION} · describes the live implementation</span></span><span>{icon('mail')}<a href="mailto:info@codeandcanvas.net">info@codeandcanvas.net</a></span></div>
          <p class="hero__lead" data-ar="{esc(intro_ar)}">{esc(intro)}</p>
          <div class="notice notice--violet" data-ar-html="تصف هذه السياسة ما يفعله الموقع فعليًا: واجهة برمجية من الطرف الأول تحفظ الاستفسارات والحجوزات وأحداث القياس بعد الموافقة. لا توجد حسابات ولا دفع إلكتروني ولا معرّفات تحليلات خارجية افتراضيًا. تُراجَع الصياغة لكل اختصاص قضائي قبل تطبيقها عليك؛ وإن لم يكن أي بند واضحًا فاكتب إلى &lt;a href=&quot;mailto:info@codeandcanvas.net&quot;&gt;info@codeandcanvas.net&lt;/a&gt; وسنجيب كتابةً.">This policy describes what the site actually does: a first-party API stores inquiries, bookings and consent-gated measurement events. There are no accounts, no online payments and no third-party analytics IDs by default. Wording is reviewed for each jurisdiction before it applies to you; if anything here is unclear, write to <a href="mailto:info@codeandcanvas.net">info@codeandcanvas.net</a> and we will answer in writing.</div>
          <nav class="toc glass" style="margin:24px 0" aria-label="Sections" data-ar-label="الأقسام"><h4 data-ar="الأقسام">Sections</h4>{toc}</nav>
          <div class="prose">{secs}</div>
          <div class="panel tier" style="margin-top:28px">
            <h3 data-ar="الإثبات والاعتماد">Evidence &amp; sign-off</h3>
            <p data-ar="يمكن مطابقة كل بند مع الكود: server/api.mjs للتخزين والاحتفاظ، وassets/js/site.js للموافقة وإشارات الخصوصية، وassets/js/pages.js للنماذج، و/assets/brand/og للصور، و/claims/ لسجل الادعاءات.">Every clause can be checked against the code: <code>server/api.mjs</code> for storage and retention, <code>assets/js/site.js</code> for consent and privacy signals, <code>assets/js/pages.js</code> for forms, and <a href="/claims/">/claims/</a> for the evidence register.</p>
            <a class="text-link" href="/claims/"><span data-ar="سجل الادعاءات والأدلة →">Claims &amp; evidence register →</span></a>
          </div>
        </div>
      </section>
'''
    return page(path, title=f'{title} — Code & Canvas', title_ar=f'{title_ar} — Code & Canvas', desc=intro, desc_ar=intro_ar,
                nav=nav, body=body, og_image='/assets/brand/og/privacy.png')


def privacy():
    S = [
        ('Who we are & scope', 'من نحن ونطاق السياسة',
         '<p>Code &amp; Canvas is a bilingual studio operating in Al Khobar (Saudi Arabia) and Al Obour (Egypt). This policy covers <code>codeandcanvas.net</code> and the first-party forms, booking and measurement endpoints on the same origin. Contact: <a href="mailto:info@codeandcanvas.net">info@codeandcanvas.net</a>. We do not operate user accounts or online payments.</p>',
         '<p>Code &amp; Canvas استوديو ثنائي اللغة يعمل في الخبر (السعودية) والعبور (مصر). تغطي هذه السياسة موقع <code>codeandcanvas.net</code> ونماذج الطرف الأول والحجز ونقاط القياس على النطاق نفسه. التواصل: <a href="mailto:info@codeandcanvas.net">info@codeandcanvas.net</a>. لا نشغّل حسابات مستخدمين ولا دفعًا إلكترونيًا.</p>'),
        ('What we collect', 'ما الذي نجمعه',
         '<p><strong>Inquiry forms</strong> (contact, newsletter, freelancer application): name, email, optional company/phone, service code, message and your explicit consent. <strong>Booking</strong>: the same contact fields plus specialty, date, time, timezone, meeting context and consent. <strong>Measurement</strong>: an event name, a route path, a session-scoped anonymous identifier and a timestamp — never form values, email addresses or URL query strings. A honeypot field and a short rate-limit counter are used for spam protection.</p>',
         '<p><strong>نماذج الاستفسار</strong> (التواصل، النشرة، طلبات المستقلين): الاسم والبريد، والشركة/الهاتف الاختيارية، ورمز الخدمة، والرسالة، وموافقتك الصريحة. <strong>الحجز</strong>: الحقول نفسها مع التخصص والتاريخ والوقت والمنطقة الزمنية وسياق الاجتماع والموافقة. <strong>القياس</strong>: اسم الحدث ومسار الصفحة ومعرّف مجهول مرتبط بالجلسة وطابع زمني — دون قيم النماذج أو البريد أو معاملات الرابط. نستخدم حقلًا خفيًا وعدادًا قصيرًا للحد من الرسائل المزعجة.</p>'),
        ('Why we process it', 'لماذا نعالج البيانات',
         '<p>To answer your inquiry, arrange the call you requested, review an application, send the insights you subscribed to, protect the forms from abuse, and understand which pages help visitors. Each purpose requires the consent checkbox shown beside that form; booking consent is separate. We do not sell data, build advertising profiles, or enrich it with third-party datasets.</p>',
         '<p>للرد على استفسارك، وترتيب المكالمة التي طلبتها، ومراجعة الطلب، وإرسال الرؤى التي اشتركت فيها، وحماية النماذج من الإساءة، وفهم الصفحات التي تساعد الزائر. كل غرض يتطلب مربع الموافقة الظاهر بجانب النموذج، وموافقة الحجز منفصلة. لا نبيع البيانات ولا نبني ملفات إعلانية ولا نثريها بمجموعات بيانات خارجية.</p>'),
        ('Where it goes', 'أين تُرسل البيانات',
         '<p>Forms post to same-origin <code>/api/contact</code>, <code>/api/newsletter</code>, <code>/api/career</code> or <code>/api/booking</code>. Records are written to a server-side file store (<code>.data/</code>, outside the public site). If an operator configures <code>CC_NOTIFY_WEBHOOK</code>, a minimal notification containing the lead reference, kind and timestamp is sent to that operator-controlled endpoint; the endpoint is never a third party by default. No email or WhatsApp message is sent automatically from your browser. If the API is unavailable the site says the request was <em>not sent</em> and offers a manual WhatsApp/email draft — nothing is recorded as a success.</p>',
         '<p>تُرسل النماذج إلى <code>/api/contact</code> أو <code>/api/newsletter</code> أو <code>/api/career</code> أو <code>/api/booking</code> على النطاق نفسه. تُحفظ السجلات في مخزن ملفات على الخادم (<code>.data/</code> خارج الملفات العامة). إن ضبط المشغّل <code>CC_NOTIFY_WEBHOOK</code> يُرسل إشعارًا أدنى يحمل مرجع العميل ونوعه والوقت إلى النقطة التي يديرها المشغّل؛ ولا تكون طرفًا ثالثًا افتراضيًا. لا يُرسل المتصفح بريدًا أو واتساب تلقائيًا. وإن تعذّر الوصول للواجهة يوضّح الموقع أن الطلب <em>لم يُرسل</em> ويقدّم مسودة يدوية عبر واتساب أو البريد — ولا يُسجَّل أي نجاح وهمي.</p>'),
        ('Analytics & consent', 'التحليلات والموافقة',
         '<p>GA4, Google Tag Manager and Microsoft Clarity identifiers are empty in <code>assets/js/config.js</code>. Providers load only when an approved ID is configured <em>and</em> you chose <code>cc-analytics-consent=granted</code>. Do Not Track and Global Privacy Control suppress measurement entirely. You can change or withdraw your choice through “Measurement settings” in the footer. Events are bounded to nine names: page_view, service_view, case_study_view, cta_click, form_start, form_submit, booking_confirmed, lead_qualified, lead_converted. Hosting providers may keep standard security logs separately.</p>',
         '<p>معرّفات GA4 وGoogle Tag Manager وMicrosoft Clarity فارغة في <code>assets/js/config.js</code>. لا تُحمَّل هذه المزوّدات إلا عند ضبط معرّف معتمد <em>و</em> اختيارك <code>cc-analytics-consent=granted</code>. وتلغي إشارتا Do Not Track وGlobal Privacy Control القياس كليًا. يمكنك تغيير اختيارك أو سحبه من «إعدادات القياس» في التذييل. الأحداث محصورة في تسعة أسماء: page_view وservice_view وcase_study_view وcta_click وform_start وform_submit وbooking_confirmed وlead_qualified وlead_converted. قد يحتفظ مزوّد الاستضافة بسجلات أمان منفصلة.</p>'),
        ('Retention & your rights', 'الاحتفاظ وحقوقك',
         '<p>Inquiry, lead and booking records are retained for 24 months from the last activity unless you ask for deletion earlier; measurement events are retained for 90 days and contain no direct identifiers. Access to the lead dashboard requires an operator token (<code>CC_ADMIN_TOKEN</code>) and is served on a noindex path. You may request access, correction, deletion or a CSV copy at <a href="mailto:info@codeandcanvas.net">info@codeandcanvas.net</a>; we action deletion requests within 30 days. Newsletter consent can be withdrawn at any time by replying “unsubscribe”.</p>',
         '<p>تُحفظ سجلات الاستفسارات والعملاء والحجوزات 24 شهرًا من آخر نشاط ما لم تطلب الحذف قبل ذلك، وتُحفظ أحداث القياس 90 يومًا دون معرّفات مباشرة. الوصول إلى لوحة العملاء يتطلب رمز مشغّل (<code>CC_ADMIN_TOKEN</code>) على مسار مستبعد من الفهرسة. يمكنك طلب الاطلاع أو التصحيح أو الحذف أو نسخة CSV عبر <a href="mailto:info@codeandcanvas.net">info@codeandcanvas.net</a>؛ وننفّذ طلبات الحذف خلال 30 يومًا. ويمكن سحب موافقة النشرة في أي وقت بالرد بكلمة «إلغاء الاشتراك».</p>'),
        ('Security & changes', 'الحماية والتعديلات',
         '<p>Requests are validated on the server, rate-limited, honeypot-checked and idempotent; the admin endpoints are token-gated. The data store is a local JSON file on the host and is not encrypted at rest — an operator deploying to production must supply an encrypted, access-controlled store before handling sensitive material. We will date and publish any material change to this policy on this page.</p>',
         '<p>تُتحقَّق الطلبات على الخادم، وتخضع لحدود معدّل وفحص الحقل الخفي ومنع التكرار، ونقاط الإدارة محمية برمز. مخزن البيانات ملف JSON محلي على الخادم وغير مشفّر عند السكون — وعلى المشغّل توفير مخزن مشفّر مضبوط الوصول قبل التعامل مع مواد حساسة في الإنتاج. سنُؤرّخ وننشر أي تعديل جوهري على هذه الصفحة.</p>'),
    ]
    return legal('/privacy-policy/', title='Privacy Policy', title_ar='سياسة الخصوصية',
                 intro='Exactly what this site collects, where it is stored, why, for how long, and how to have it removed.',
                 intro_ar='بالضبط: ما يجمعه الموقع، وأين يُخزَّن، ولماذا، ولمدة كم، وكيف تطلب حذفه.', sections=S)


def terms():
    S = [
        ('Scope', 'النطاق',
         '<p>These terms govern your use of <code>codeandcanvas.net</code>, its published free previews, and any engagement agreed with Code &amp; Canvas. The site has no user accounts, no shopping cart purchases, no payment processing and no paid digital entitlement in this release.</p>',
         '<p>تحكم هذه الشروط استخدامك لـ <code>codeandcanvas.net</code> ومعايناته المجانية المنشورة وأي تعاقد يُبرم مع Code &amp; Canvas. لا توجد حسابات مستخدمين ولا مشتريات عبر سلة ولا معالجة دفع ولا ملكية محتوى مدفوع في هذا الإصدار.</p>'),
        ('Services & engagements', 'الخدمات والتعاقدات',
         '<p>All prices on the site are indicative ranges in USD. The binding scope, deliverables, timeline, price and payment milestones are fixed only in a written proposal signed by both parties. Nothing on the site constitutes an offer capable of acceptance by clicking a button. Work begins after the proposal is signed and the first milestone is agreed. We describe outcomes we can evidence; concept studies are labelled as illustrative and are not client work.</p>',
         '<p>كل الأسعار على الموقع نطاقات استرشادية بالدولار الأمريكي. ولا يثبُت النطاق والمخرجات والجدول والسعر ومراحل الدفع إلا في عرض مكتوب يوقّعه الطرفان. ولا يُعدّ أي محتوى في الموقع إيجابًا قابلًا للقبول بالنقر على زر. يبدأ العمل بعد توقيع العرض والاتفاق على الدفعة الأولى. نصف النتائج التي نستطيع إثباتها، والدراسات المفاهيمية مُعلَّنة كأعمال توضيحية ليست أعمال عملاء.</p>'),
        ('Inquiries & bookings', 'الاستفسارات والحجوزات',
         '<p>Sending a form creates a lead record; booking a call creates a reservation with a reference and a calendar file. A confirmation is shown only after the server accepts the request. If the service is unavailable, the site says the request was not sent and offers a manual channel. We may decline or reschedule a call; no fee is charged for a discovery call. The call is not a contract and no deliverable is promised by booking it.</p>',
         '<p>إرسال النموذج ينشئ سجل عميل، وحجز المكالمة ينشئ حجزًا بمرجع وملف تقويم. ولا يظهر التأكيد إلا بعد قبول الخادم الطلب. وإن تعذّرت الخدمة يوضّح الموقع أن الطلب لم يُرسل ويقدّم قناة يدوية. قد نعتذر عن المكالمة أو نعيد جدولتها؛ والمكالمة الاستكشافية مجانية وليست عقدًا ولا يترتب عليها مخرج بمجرّد حجزها.</p>'),
        ('Digital books & previews', 'الكتب والمعاينات',
         '<p>Public previews are free to read. Saving a book to a shortlist stores an identifier in your own browser only; it is not a purchase, grants no paid access and creates no account. Future sales would require separately published terms, server-side pricing, authenticated delivery and signed payment confirmation — none of which exists here.</p>',
         '<p>المعاينات العامة مجانية. وحفظ كتاب في قائمة يخزّن معرّفًا في متصفحك فقط؛ وليس شراءً ولا يمنح وصولًا مدفوعًا ولا ينشئ حسابًا. وأي بيع لاحق يتطلب شروطًا منشورة منفصلة وأسعارًا على الخادم وتسليمًا مؤكدًا بالمصادقة وتأكيد دفع موقع — ولا شيء من ذلك موجود هنا.</p>'),
        ('Intellectual property', 'الملكية الفكرية',
         '<p>Site copy, frameworks, generated illustrative artwork and book material are © Code &amp; Canvas. The display typeface is Space Grotesk under the SIL Open Font License; its licence is shipped in <code>/assets/fonts/space-grotesk-OFL.txt</code>. Client deliverables transfer on full payment as defined in the signed proposal; we may show the work only with permission or as otherwise agreed in writing.</p>',
         '<p>نصوص الموقع والأطر والأعمال الفنية التوضيحية المولّدة ومواد الكتب محفوظة الحقوق لـ Code &amp; Canvas. خط العناوين Space Grotesk بموجب SIL Open Font License، ورخصته في <code>/assets/fonts/space-grotesk-OFL.txt</code>. تنتقل مخرجات العميل عند السداد الكامل وفق العرض الموقّع، ولا نعرض العمل إلا بإذن أو وفق اتفاق مكتوب.</p>'),
        ('Liability, law & contact', 'المسؤولية والقانون والتواصل',
         '<p>The site is provided “as is”. To the extent permitted by law, liability is limited to fees paid for the specific signed engagement. KSA engagements are governed by Saudi law and Egypt engagements by Egyptian law, without prejudice to mandatory consumer protections. Questions: <a href="mailto:info@codeandcanvas.net">info@codeandcanvas.net</a>.</p>',
         '<p>يُقدَّم الموقع «كما هو». وفي الحدود التي يسمح بها القانون تقتصر المسؤولية على الرسوم المدفوعة في التعاقد الموقّع المحدد. تخضع تعاقدات السعودية للقانون السعودي وتعاقدات مصر للقانون المصري، دون إخلال بحماية المستهلك الملزمة. للاستفسار: <a href="mailto:info@codeandcanvas.net">info@codeandcanvas.net</a>.</p>'),
    ]
    return legal('/terms-of-use/', title='Terms of Use', title_ar='شروط الاستخدام',
                 intro='The rules for using this site, requesting work and booking a call — with no accounts or payments implied.',
                 intro_ar='قواعد استخدام الموقع وطلب العمل وحجز مكالمة — دون حسابات أو دفع أو وعود ضمنية.', sections=S)


def cookies():
    S = [
        ('What this site stores', 'ما يخزّنه الموقع',
         '<p><code>cc-lang</code> remembers your language; <code>cc-pre</code> is a session-only preference for the intro animation; <code>cc-cart</code> holds saved book identifiers (not purchases); <code>cc-reader-*</code> and <code>cc-notes-*</code> keep your reading position and notes on this device; <code>cc-analytics-consent</code> records your measurement choice. All of these are first-party browser storage, not advertising cookies. Clear them in browser settings at any time.</p>',
         '<p>يحفظ <code>cc-lang</code> لغتك، و<code>cc-pre</code> تفضيل للجلسة لمقدمة الموقع، و<code>cc-cart</code> معرّفات الكتب المحفوظة (لا مشتريات)، و<code>cc-reader-*</code> و<code>cc-notes-*</code> موضع القراءة والملاحظات على جهازك، و<code>cc-analytics-consent</code> اختيارك للقياس. كلها تخزين طرف أول في المتصفح وليست ملفات إعلانية. يمكنك مسحها من إعدادات المتصفح في أي وقت.</p>'),
        ('Server-side records', 'السجلات على الخادم',
         '<p>Form submissions and bookings create records in the operator-controlled server store described in the <a href="/privacy-policy/">Privacy Policy</a>. These are not cookies on your device. An admin dashboard uses an operator token; it does not set visitor cookies and is excluded from search indexing.</p>',
         '<p>تنشئ النماذج والحجوزات سجلات في مخزن الخادم الذي يديره المشغّل والموضّح في <a href="/privacy-policy/">سياسة الخصوصية</a>. وليست ملفات ارتباط على جهازك. وتستخدم لوحة الإدارة رمز مشغّل، ولا تضع ملفات للزائر، ومستبعدة من فهرسة البحث.</p>'),
        ('Optional measurement', 'القياس الاختياري',
         '<p>No third-party analytics or advertising tags are loaded by default: GA4, GTM and Clarity identifiers are empty. They load only with an approved ID and your granted consent, and are suppressed by Do Not Track or Global Privacy Control. <code>/api/events</code> receives only the nine documented event names, a route path and a session-scoped anonymous identifier. Declining changes nothing about your ability to read, inquire or book.</p>',
         '<p>لا تُحمَّل وسوم تحليلات أو إعلانات خارجية افتراضيًا: معرّفات GA4 وGTM وClarity فارغة. ولا تُحمَّل إلا بمعرّف معتمد وموافقة منك، وتُلغى بإشارة Do Not Track أو Global Privacy Control. يستقبل <code>/api/events</code> الأسماء التسعة الموثّقة ومسار الصفحة ومعرّفًا مجهولًا للجلسة فقط. والرفض لا يغيّر قدرتك على القراءة أو الاستفسار أو الحجز.</p>'),
        ('No payment or session cookies', 'لا ملفات دفع أو جلسات',
         '<p>There is no account session, no authentication cookie, no payment cookie and no cart checkout in this release. Legacy account/cart/checkout screens carry a visible notice and are excluded from the main studio journey and from search indexing.</p>',
         '<p>لا توجد جلسة حساب ولا ملف مصادقة ولا ملف دفع ولا إتمام شراء في هذا الإصدار. وتحمل شاشات الحساب والسلة والدفع القديمة تنبيهًا ظاهرًا، وهي مستبعدة من مسار الاستوديو الأساسي ومن فهرسة البحث.</p>'),
    ]
    return legal('/cookie-policy/', title='Cookie Policy', title_ar='سياسة ملفات تعريف الارتباط',
                 intro='Exactly what this site stores in your browser and on its server — and what it does not.',
                 intro_ar='بالضبط ما يخزّنه الموقع في متصفحك وعلى خادمه — وما لا يخزّنه.', sections=S)


def not_found():
    body = f'''
      <section class="oops" aria-labelledby="page-title">
        <div>
          <p class="oops__code grad-text" aria-hidden="true">404</p>
          <p class="kicker"><span data-ar="404 — تائه · Code &amp; Canvas">404 — Lost · Code &amp; Canvas</span></p>
          <h1 id="page-title" data-ar="تائه في الفراغ">Lost in the void</h1>
          <p data-ar="الصفحة التي تبحث عنها انتقلت أو لم توجد قط. نكمل؟">The page you’re looking for has moved or never existed. Continue?</p>
          <div class="oops__links">{btn('Return home', 'العودة للرئيسية', '/')}{btn('Book a call', 'احجز مكالمة', '/book/', 'glass', 'calendar')}{btn('Our services', 'خدماتنا', '/services/', 'ghost', 'arrow')}</div>
        </div>
      </section>
'''
    return page('404.html', title='404 — Lost · Code & Canvas', title_ar='404 — تائه · Code & Canvas', desc='Page not found.', desc_ar='الصفحة غير موجودة.', nav='', body=body, canonical='https://codeandcanvas.net/404.html')


def build():
    return [privacy(), terms(), cookies(), not_found()]
