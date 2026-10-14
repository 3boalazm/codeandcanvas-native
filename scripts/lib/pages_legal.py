# -*- coding: utf-8 -*-
"""Legal pages + 404. NOTE: the live WordPress site has NO privacy / terms / cookie
pages (all 404) although the footer links to them. These are concise DRAFTS
written from the site's actual practices (contact form, WhatsApp hand-off,
analytics-free static hosting, book purchases) — marked for legal review."""
from h import esc, icon, crumbs, btn, page

UPDATED = 'October 2026'


def legal(path, *, title, title_ar, intro, intro_ar, sections, nav=''):
    toc = ''.join(f'<a href="#s{i + 1}" data-ar="{esc(ar)}">{esc(en)}</a>' for i, (en, ar, _, __) in enumerate(sections))
    secs = ''.join(f'<h2 id="s{i + 1}" data-ar="{esc(ar)}">{esc(en)}</h2><div class="legal__en">{en_html}</div><div class="legal__ar" lang="ar" dir="rtl">{ar_html}</div>' for i, (en, ar, en_html, ar_html) in enumerate(sections))
    body = f'''
      <section class="section container" style="padding-top:calc(var(--nav-h) + 40px)" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), (title, title_ar, None)])}
        <div class="legal">
          <h1 class="section__title" id="page-title" data-ar="{esc(title_ar)}">{esc(title)}</h1>
          <div class="legal__meta"><span>{icon('calendar')}<span data-ar="آخر تحديث: {UPDATED}">Last updated: {UPDATED}</span></span><span>{icon('mail')}<a href="mailto:info@codeandcanvas.net">info@codeandcanvas.net</a></span><span class="badge badge--gold" data-ar="مسودة — للمراجعة القانونية">Draft — pending legal review</span></div>
          <p class="hero__lead" data-ar="{esc(intro_ar)}">{esc(intro)}</p>
          <nav class="toc glass" style="margin:24px 0" aria-label="Sections" data-ar-label="الأقسام"><h4 data-ar="الأقسام">Sections</h4>{toc}</nav>
          <div class="prose">{secs}</div>
        </div>
      </section>
'''
    return page(path, title=f'{title} — Code & Canvas', title_ar=f'{title_ar} — Code & Canvas', desc=intro, desc_ar=intro_ar, nav=nav, body=body)


def privacy():
    S = [
        ('Who we are', 'من نحن',
         '<p>Code &amp; Canvas is a digital product studio and advisory firm operating from Riyadh, Saudi Arabia and Al Obour, Egypt. This policy explains what personal data we collect through codeandcanvas.net and how we use it.</p>',
         '<p>Code &amp; Canvas استوديو منتجات رقمية وشركة استشارات تعمل من الرياض (السعودية) والعبور (مصر). توضح هذه السياسة البيانات الشخصية التي نجمعها عبر codeandcanvas.net وكيفية استخدامها.</p>'),
        ('What we collect', 'ما نجمعه',
         '<ul><li><strong>Contact &amp; booking forms:</strong> name, e-mail, phone, company, and the message you send us.</li><li><strong>Accounts &amp; purchases:</strong> name, e-mail, phone (optional), billing country, and your order history for digital books.</li><li><strong>Newsletter:</strong> your e-mail address.</li><li><strong>Technical data:</strong> standard server logs (IP address, browser, pages requested) kept by our hosting provider for security.</li></ul>',
         '<ul><li><strong>نماذج التواصل والحجز:</strong> الاسم والبريد الإلكتروني والهاتف والشركة ورسالتك.</li><li><strong>الحسابات والمشتريات:</strong> الاسم والبريد والهاتف (اختياري) ودولة الفوترة وسجل طلبات الكتب الرقمية.</li><li><strong>النشرة البريدية:</strong> بريدك الإلكتروني.</li><li><strong>بيانات تقنية:</strong> سجلات الخادم القياسية (عنوان IP والمتصفح والصفحات المطلوبة) يحتفظ بها مزود الاستضافة لأغراض الأمان.</li></ul>'),
        ('How we use it', 'كيف نستخدمها',
         '<p>To answer your inquiry, schedule discovery calls, deliver purchased books, send the newsletter you subscribed to, issue invoices, and keep the site secure. We do not sell personal data and we do not run advertising profiles.</p>',
         '<p>للرد على استفسارك، وجدولة المكالمات الاستكشافية، وتسليم الكتب المشتراة، وإرسال النشرة التي اشتركت فيها، وإصدار الفواتير، والحفاظ على أمان الموقع. لا نبيع البيانات الشخصية ولا ننشئ ملفات إعلانية.</p>'),
        ('Messaging channels', 'قنوات المراسلة',
         '<p>When you choose WhatsApp or e-mail from our contact page, your message is handled by that provider (Meta / your mail provider) under its own terms. Payment details are processed by the payment gateway and never stored on our servers.</p>',
         '<p>عند اختيارك واتساب أو البريد الإلكتروني من صفحة التواصل، تُعالج رسالتك عبر ذلك المزود (Meta / مزود بريدك) وفق شروطه. تُعالج بيانات الدفع عبر بوابة الدفع ولا تُخزَّن على خوادمنا.</p>'),
        ('Retention & your rights', 'الاحتفاظ وحقوقك',
         '<p>Inquiry data is kept for up to 24 months; account and invoice data for as long as required by law. You may request access, correction, or deletion of your data at any time by writing to <a href="mailto:info@codeandcanvas.net">info@codeandcanvas.net</a>.</p>',
         '<p>نحتفظ ببيانات الاستفسارات حتى 24 شهرًا، وببيانات الحسابات والفواتير للمدة التي يفرضها القانون. يمكنك طلب الاطلاع على بياناتك أو تصحيحها أو حذفها في أي وقت عبر <a href="mailto:info@codeandcanvas.net">info@codeandcanvas.net</a>.</p>'),
    ]
    return legal('/privacy-policy/', title='Privacy Policy', title_ar='سياسة الخصوصية', intro='How Code & Canvas collects, uses, and protects your personal data.', intro_ar='كيف تجمع Code & Canvas بياناتك الشخصية وتستخدمها وتحميها.', sections=S)


def terms():
    S = [
        ('Scope', 'النطاق',
         '<p>These terms govern your use of codeandcanvas.net, our digital books, and our services. By using the site or placing an order you agree to them.</p>',
         '<p>تحكم هذه الشروط استخدامك لموقع codeandcanvas.net وكتبنا الرقمية وخدماتنا. باستخدامك الموقع أو تقديم طلب فإنك توافق عليها.</p>'),
        ('Services & engagements', 'الخدمات والتعاقدات',
         '<p>All service prices on the site are indicative ranges in USD; the final scope, timeline, and price are fixed in a written proposal. Payment milestones: Brand &amp; Creative work 50% / 25% / 25%; Technology &amp; Advisory work 50% / 50%. Final files are released on 100% payment. Late payments accrue 2% per month after 14 days. SAR / EGP equivalents are set at contract.</p>',
         '<p>كل أسعار الخدمات على الموقع نطاقات استرشادية بالدولار الأمريكي؛ يُثبَّت النطاق والجدول والسعر النهائي في عرض مكتوب. دفعات السداد: أعمال العلامة والإبداع 50٪ / 25٪ / 25٪؛ أعمال التكنولوجيا والاستشارات 50٪ / 50٪. تُسلَّم الملفات النهائية عند سداد 100٪. يُحتسب 2٪ شهريًا على المتأخرات بعد 14 يومًا. يُحدد المعادل بالريال/الجنيه عند التعاقد.</p>'),
        ('Digital books', 'الكتب الرقمية',
         '<p>Books are licensed to the purchaser for personal use, accessible through the online reader from your account. Redistribution, resale, or public screening is not permitted. Because access is granted immediately, purchases are non-refundable except where required by law.</p>',
         '<p>تُرخَّص الكتب للمشتري للاستخدام الشخصي عبر القارئ الإلكتروني من حسابه. لا يُسمح بإعادة التوزيع أو البيع أو العرض العام. ولأن الوصول يُمنح فورًا، فإن المشتريات غير قابلة للاسترداد إلا حيث يفرض القانون ذلك.</p>'),
        ('Intellectual property', 'الملكية الفكرية',
         '<p>Site content, frameworks, and book material are © Code &amp; Canvas. Client deliverables transfer to the client upon full payment as defined in each proposal; we retain the right to showcase the work unless an NDA says otherwise.</p>',
         '<p>محتوى الموقع والأطر ومواد الكتب حقوقها محفوظة لـ Code &amp; Canvas. تنتقل مخرجات العميل إليه عند السداد الكامل وفق كل عرض؛ ونحتفظ بحق عرض العمل ما لم تنص اتفاقية سرية على خلاف ذلك.</p>'),
        ('Liability & law', 'المسؤولية والقانون',
         '<p>The site is provided “as is”. To the extent permitted by law, our liability is limited to the fees paid for the specific service or product. These terms are governed by the laws of the Kingdom of Saudi Arabia for KSA engagements and the Arab Republic of Egypt for Egypt engagements.</p>',
         '<p>يُقدَّم الموقع «كما هو». وفي الحدود التي يسمح بها القانون، تقتصر مسؤوليتنا على الرسوم المدفوعة للخدمة أو المنتج المحدد. تخضع هذه الشروط لقوانين المملكة العربية السعودية للتعاقدات في السعودية، وجمهورية مصر العربية للتعاقدات في مصر.</p>'),
    ]
    return legal('/terms-of-use/', title='Terms of Use', title_ar='شروط الاستخدام', intro='The rules for using codeandcanvas.net, buying our books, and working with us.', intro_ar='قواعد استخدام codeandcanvas.net وشراء كتبنا والعمل معنا.', sections=S)


def cookies():
    S = [
        ('What we use', 'ما نستخدمه',
         '<p>This site is a static, tracker-free build. We do not set advertising or third-party analytics cookies.</p>',
         '<p>هذا الموقع بناء ثابت خالٍ من أدوات التتبع. لا نضع ملفات تعريف إعلانية أو تحليلات طرف ثالث.</p>'),
        ('Local storage', 'التخزين المحلي',
         '<ul><li><code>cc-lang</code> — your language choice (EN / AR).</li><li><code>cc-cart</code>, <code>cc-library</code> — your shopping cart and purchased books.</li><li><code>cc-reader-*</code>, <code>cc-notes-*</code> — your reading position and private notes inside the book reader.</li></ul><p>These values stay in your browser and are never sent to us.</p>',
         '<ul><li><code>cc-lang</code> — اختيارك للغة (EN / AR).</li><li><code>cc-cart</code> و<code>cc-library</code> — سلة التسوق والكتب المشتراة.</li><li><code>cc-reader-*</code> و<code>cc-notes-*</code> — موضع القراءة وملاحظاتك الخاصة داخل القارئ.</li></ul><p>تبقى هذه القيم في متصفحك ولا تُرسل إلينا.</p>'),
        ('Session cookies', 'ملفات الجلسة',
         '<p>If you sign in to your account, a strictly necessary session cookie keeps you logged in. Payment providers may set their own cookies during checkout.</p>',
         '<p>عند تسجيل الدخول إلى حسابك، يُبقيك ملف جلسة ضروري مسجلًا. قد تضع بوابات الدفع ملفاتها الخاصة أثناء إتمام الشراء.</p>'),
        ('Your choices', 'خياراتك',
         '<p>You can clear local storage and cookies from your browser settings at any time; the site keeps working, you will simply be asked for your language again.</p>',
         '<p>يمكنك مسح التخزين المحلي وملفات تعريف الارتباط من إعدادات متصفحك في أي وقت؛ سيستمر الموقع في العمل وسيُطلب منك اختيار اللغة مجددًا.</p>'),
    ]
    return legal('/cookie-policy/', title='Cookie Policy', title_ar='سياسة ملفات تعريف الارتباط', intro='What this site stores in your browser — and what it does not.', intro_ar='ما يخزنه هذا الموقع في متصفحك — وما لا يخزنه.', sections=S)


def not_found():
    body = f'''
      <section class="oops" aria-labelledby="page-title">
        <div>
          <p class="oops__code grad-text" aria-hidden="true">404</p>
          <p class="kicker"><span data-ar="404 — تائه · Code &amp; Canvas">404 — Lost · Code &amp; Canvas</span></p>
          <h1 id="page-title" data-ar="تائه في الفراغ">Lost in the void</h1>
          <p data-ar="الصفحة التي تبحث عنها انتقلت أو لم توجد قط. نكمل؟">The page you’re looking for has moved or never existed. Continue?</p>
          <div class="oops__links">{btn('Return home', 'العودة للرئيسية', '/')}{btn('Send a signal', 'أرسل إشارة', '/contact/', 'glass', 'chat')}{btn('Our services', 'خدماتنا', '/services/', 'ghost', 'arrow')}</div>
        </div>
      </section>
'''
    return page('404.html', title='404 — Lost · Code & Canvas', title_ar='404 — تائه · Code & Canvas', desc='Page not found.', desc_ar='الصفحة غير موجودة.', nav='', body=body, canonical='https://codeandcanvas.net/404.html')


def build():
    return [privacy(), terms(), cookies(), not_found()]
