# -*- coding: utf-8 -*-
"""Legal pages + 404. NOTE: the live WordPress site has NO privacy / terms / cookie
pages (all 404) although the footer links to them. These are concise DRAFTS
written from the site's actual practices (contact form, WhatsApp hand-off,
optional consented measurement, preview-only books) — marked for legal review."""
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
    S = [('Current operation',
  'طريقة التشغيل الحالية',
  '<p>Online accounts and payments are not connected. Contact, career and book inquiries prepare a WhatsApp or email draft unless a first-party form '
  'endpoint is configured. A draft is not sent until you finish in the chosen app.</p>',
  '<p>الحسابات والدفع الإلكتروني غير مربوطين. تُجهّز استفسارات التواصل والتوظيف والكتب مسودة واتساب أو بريد، ما لم تُربط بخدمة نماذج. لا تُرسل '
  'المسودة حتى تُكمل الإرسال في التطبيق المختار.</p>'),
 ('Information you choose to share',
  'المعلومات التي تختار مشاركتها',
  '<p>Forms may include your name, email, company and message. The receiving messaging provider applies its own terms. When a form endpoint is '
  'connected, it receives the fields you submit and must have an approved retention and security policy. Contact info@codeandcanvas.net for access '
  'or deletion requests.</p>',
  '<p>قد تشمل النماذج اسمك وبريدك وشركتك ورسالتك. تسري شروط مزود المراسلة المستقبِل. عند ربط خدمة نماذج تستقبل الحقول التي ترسلها ويلزم اعتماد سياسة '
  'احتفاظ وحماية. تواصل عبر info@codeandcanvas.net لطلبات الاطلاع أو الحذف.</p>'),
 ('Usage measurement',
  'قياس الاستخدام',
  '<p>No analytics provider is connected by default. If a first-party collector is configured, measurement is sent only after your consent, '
  'respecting Do Not Track and Global Privacy Control. Events exclude form values, emails and URL query strings. Change or withdraw your choice '
  'through Measurement settings in the footer. Hosting providers may keep standard security logs separately.</p>',
  '<p>لا يوجد مزود تحليلات مربوط افتراضيًا. عند إعداد مجمّع بيانات خاص بالموقع لا يُرسل القياس إلا بعد موافقتك مع احترام Do Not Track وGlobal '
  'Privacy Control. لا تشمل الأحداث بيانات النماذج أو البريد أو معاملات الروابط. يمكنك تغيير اختيارك أو سحبه من إعدادات القياس بالتذييل. قد يحتفظ '
  'مزود الاستضافة بسجلات أمان منفصلة.</p>')]
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
    S = [(en, ar, '<p>Only public book previews and availability inquiries are offered in this build. Saving a book is not a purchase and grants no paid access. Any future sale requires separately confirmed terms, pricing and access arrangements.</p>' if en == 'Digital books' else eh, '<p>تقدم هذه النسخة معاينات عامة واستفسارات عن التوفر فقط. حفظ الكتاب ليس شراءً ولا يمنح وصولًا مدفوعًا. أي بيع لاحق يتطلب تأكيدًا منفصلًا للشروط والسعر وطريقة الوصول.</p>' if en == 'Digital books' else ah) for en, ar, eh, ah in S]
    return legal('/terms-of-use/', title='Terms of Use', title_ar='شروط الاستخدام', intro='The rules for using codeandcanvas.net, buying our books, and working with us.', intro_ar='قواعد استخدام codeandcanvas.net وشراء كتبنا والعمل معنا.', sections=S)


def cookies():
    S = [('Local preferences',
  'تفضيلات محلية',
  '<p>cc-lang stores your language; cc-cart stores saved book IDs, not purchases; cc-reader-* and cc-notes-* store your reading position and notes '
  'on this device. cc-pre is a session preference for the intro animation. Clear them in browser settings at any time.</p>',
  '<p>يحفظ cc-lang اللغة، وcc-cart معرّفات الكتب المحفوظة لا المشتريات، وcc-reader-* وcc-notes-* موضع القراءة والملاحظات على هذا الجهاز. cc-pre '
  'تفضيل للجلسة خاص بمقدمة الموقع. يمكنك مسحها من إعدادات المتصفح.</p>'),
 ('Optional measurement',
  'قياس اختياري',
  '<p>No third-party analytics or advertising cookies are set by this build. cc-analytics-consent records your choice only when optional measurement '
  'is configured. Declining does not prevent using the site. No account or payment session is created in the current build.</p>',
  '<p>لا تنشئ هذه النسخة ملفات إعلانية أو تحليلات خارجية. يحفظ cc-analytics-consent اختيارك عند إعداد القياس الاختياري فقط. الرفض لا يمنع استخدام '
  'الموقع. لا تُنشأ جلسة حساب أو دفع في النسخة الحالية.</p>')]
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
