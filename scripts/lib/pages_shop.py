# -*- coding: utf-8 -*-
"""Auth + commerce UI shells — literal field sets from the live WordPress pages
(/login/, /register/, /forgot-password/, /reset-password/, /account-center/,
/cart/, /checkout/, /thank-you/). No backend: forms use data-form="demo" and the
cart is localStorage (assets/js/shop.js). Integration points are in README.

Heads use the same v3 page hero (.phero) as every other inner page, so these
shells read as one system with the rest of the site instead of as a separate
legacy skin.
"""
from h import esc, icon, crumbs, btn, page

SHOP_JS = ('/assets/js/pages.js', '/assets/js/book-catalog.js', '/assets/js/shop.js')

# One page-level honesty statement for the whole account surface: the pages must
# never imply that a session, an account or a payment actually happened.
ACCOUNT_NOTICE = ('Online accounts are not available yet. These forms do not sign in, create accounts or send passwords. Explore the free previews or contact us.',
                  'الحسابات الإلكترونية غير متاحة حاليًا. هذه النماذج لا تسجّل الدخول ولا تنشئ حسابًا ولا ترسل كلمات مرور. تصفّح المعاينات المجانية أو تواصل معنا.')


def field(name, label, label_ar, typ='text', req=True, auto='', extra='', hint=None, placeholder=''):
    err = {'email': ('Please enter a valid e-mail', 'أدخل بريدًا صحيحًا'), 'password': ('At least 8 characters', '8 أحرف على الأقل'), 'tel': ('Please enter a valid phone', 'أدخل رقمًا صحيحًا')}.get(typ, ('This field is required', 'هذا الحقل مطلوب'))
    attrs = f' required' if req else ''
    if typ == 'password':
        attrs += ' minlength="8"'
    if auto:
        attrs += f' autocomplete="{auto}"'
    if placeholder:
        attrs += f' placeholder="{placeholder}"'
    return f'''<div class="field"><label for="f-{name}" data-ar="{esc(label_ar)}">{esc(label)}</label><input id="f-{name}" name="{name}" type="{typ}"{attrs}{extra} /><span class="field__err" data-ar="{esc(err[1])}">{esc(err[0])}</span>{f'<span class="field__hint" data-ar="{esc(hint[1])}">{esc(hint[0])}</span>' if hint else ''}</div>'''


def google():
    return f'''<button class="btn btn--glass auth__google" type="button" disabled><svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><path fill="#EA4335" d="M9 3.5c1.5 0 2.5.6 3.1 1.2l2.3-2.3C13 1.1 11.2.3 9 .3 5.5.3 2.5 2.3 1.1 5.2l2.7 2.1C4.4 5.2 6.5 3.5 9 3.5z"/><path fill="#4285F4" d="M17.6 9.2c0-.7-.1-1.2-.2-1.8H9v3.3h4.9c-.1.8-.6 2-1.8 2.8l2.6 2c1.6-1.4 2.9-3.6 2.9-6.3z"/><path fill="#FBBC05" d="M3.8 10.7c-.2-.6-.3-1.1-.3-1.7s.1-1.2.3-1.7L1.1 5.2C.4 6.3 0 7.6 0 9s.4 2.7 1.1 3.8l2.7-2.1z"/><path fill="#34A853" d="M9 17.7c2.4 0 4.5-.8 6-2.2l-2.6-2c-.8.5-1.8.9-3.4.9-2.5 0-4.6-1.7-5.3-4L1.1 12.5C2.5 15.6 5.5 17.7 9 17.7z"/></svg><span data-ar="تسجيل الدخول عبر Google غير متاح">Google sign-in unavailable</span></button>'''


def auth_shell(path, *, title, title_ar, head, head_ar, eyebrow, eyebrow_ar, sub_html, form_html, nav='', desc='', desc_ar=''):
    body = f'''
      <section class="phero container phero--center phero--tight" aria-labelledby="auth-title">
        <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="{esc(eyebrow_ar)}">{esc(eyebrow)}</span></span>
        <h1 class="phero__title" id="auth-title" data-reveal style="--d:.08s" data-ar="{esc(head_ar)}">{esc(head)}</h1>
        <p class="hero__lead auth__sub" data-reveal style="--d:.16s">{sub_html}</p>
        <p class="notice" role="note" data-reveal style="--d:.24s" data-ar="{esc(ACCOUNT_NOTICE[1])}">{ACCOUNT_NOTICE[0]}</p>
      </section>
      <section class="auth container" aria-label="Account form" data-ar-label="نموذج الحساب">
        <div class="auth__card glass glass--deep">
          {form_html}
        </div>
      </section>
'''
    return page(path, title=title, title_ar=title_ar, desc=desc or f'{head} — Code & Canvas account.', desc_ar=desc_ar or f'{head_ar} — حساب Code & Canvas.', nav=nav, body=body, body_class='is-auth', scripts=SHOP_JS)


def login():
    form = f'''
          <form class="form" data-form="demo" data-next="/account/" novalidate>
            <input type="text" name="_hp" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px" />
            {field('email', 'Email', 'البريد الإلكتروني', 'email', auto='email')}
            {field('password', 'Password', 'كلمة المرور', 'password', auto='current-password')}
            <div class="form__row form__row--between"><label class="check"><input type="checkbox" name="remember" value="1" /><span data-ar="تذكرني">Remember me</span></label><a class="text-link" href="/forgot-password/"><span data-ar="نسيت كلمة المرور؟">Forgot password?</span></a></div>
            <button class="btn btn--primary magnetic btn--block" type="submit"><span data-ar="تسجيل الدخول">Sign In</span></button>
            <div class="form__status" role="status" aria-live="polite"></div>
            <p class="auth__or"><span data-ar="أو سجّل الدخول عبر">or sign in with</span></p>
            {google()}
          </form>
          <details class="auth__2fa">
            <summary><span data-ar="لديك تحقق بخطوتين؟ أدخل الرمز">Using two-factor authentication? Enter your code</span></summary>
            <form class="form" data-form="demo" data-next="/account/" novalidate>
              <p class="form__hint">🔐 <span data-ar="أدخل الرمز المكوّن من 6 أرقام من تطبيق المصادقة، أو رمز استرداد.">Enter the 6-digit code from your authenticator app, or a recovery code.</span></p>
              {field('otp', 'Authentication code', 'رمز المصادقة', 'text', auto='one-time-code', extra=' inputmode="numeric" pattern="[0-9A-Za-z-]{6,16}"')}
              <button class="btn btn--glass btn--block" type="submit"><span data-ar="تحقق">Verify</span></button>
              <a class="text-link" href="/login/"><span data-ar="← العودة لتسجيل الدخول">← Back to sign in</span></a>
            </form>
          </details>'''
    sub = '<span data-ar="ليس لديك حساب؟">Don’t have an account?</span> <a href="/register/" data-ar="أنشئ حسابًا مجانًا">Create one for free</a>'
    return auth_shell('/login/', title='Login - Code & Canvas', title_ar='تسجيل الدخول - Code & Canvas', head='Welcome back', head_ar='أهلًا بعودتك', eyebrow='Accounts · preview only', eyebrow_ar='الحسابات · معاينة فقط', sub_html=sub, form_html=form)


def register():
    form = f'''
          <form class="form" data-form="demo" data-next="/account/" novalidate>
            <input type="text" name="_hp" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px" />
            {google()}
            <p class="auth__or"><span data-ar="أو سجّل بالبريد الإلكتروني">or register with email</span></p>
            {field('name', 'Full name', 'الاسم الكامل', auto='name')}
            {field('email', 'Email', 'البريد الإلكتروني', 'email', auto='email')}
            {field('phone', 'Phone (optional)', 'الهاتف (اختياري)', 'tel', req=False, auto='tel', placeholder='+966 5x xxx xxxx')}
            {field('password', 'Password', 'كلمة المرور', 'password', auto='new-password', hint=('At least 8 characters.', '8 أحرف على الأقل.'))}
            {field('password2', 'Confirm password', 'تأكيد كلمة المرور', 'password', auto='new-password', extra=' data-match="#f-password"')}
            <label class="check"><input type="checkbox" name="consent" value="1" required /><span data-ar-html="أوافق على &lt;a href=&quot;/terms-of-use/&quot;&gt;شروط الاستخدام&lt;/a&gt; و&lt;a href=&quot;/privacy-policy/&quot;&gt;سياسة الخصوصية&lt;/a&gt;.">I agree to the <a href="/terms-of-use/">Terms of Use</a> and <a href="/privacy-policy/">Privacy Policy</a>.</span></label>
            <button class="btn btn--primary magnetic btn--block" type="submit"><span data-ar="إنشاء الحساب">Create Account</span></button>
            <div class="form__status" role="status" aria-live="polite"></div>
          </form>'''
    sub = '<span data-ar="لديك حساب بالفعل؟">Already have one?</span> <a href="/login/" data-ar="سجّل الدخول">Sign in</a>'
    return auth_shell('/register/', title='Register - Code & Canvas', title_ar='إنشاء حساب - Code & Canvas', head='Create your account', head_ar='أنشئ حسابك', eyebrow='New account · preview only', eyebrow_ar='حساب جديد · معاينة فقط', sub_html=sub, form_html=form)


def forgot():
    form = f'''
          <form class="form" data-form="demo" novalidate data-note="Online password reset is not available yet.">
            <input type="text" name="_hp" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px" />
            {field('email', 'Email', 'البريد الإلكتروني', 'email', auto='email')}
            <button class="btn btn--primary magnetic btn--block" type="submit"><span data-ar="إرسال رابط إعادة التعيين">Send reset link</span></button>
            <div class="form__status" role="status" aria-live="polite"></div>
            <a class="text-link" href="/login/"><span data-ar="← العودة لتسجيل الدخول">← Back to sign in</span></a>
          </form>'''
    sub = '<span data-ar="إعادة تعيين كلمة المرور غير مربوطة. تواصل معنا إذا احتجت مساعدة.">Password reset is not connected. Contact us if you need help.</span>'
    return auth_shell('/forgot-password/', title='Forgot Password - Code & Canvas', title_ar='نسيت كلمة المرور - Code & Canvas', head='Forgot your password?', head_ar='نسيت كلمة المرور؟', eyebrow='Password reset · preview only', eyebrow_ar='استعادة كلمة المرور · معاينة فقط', sub_html=sub, form_html=form)


def reset():
    form = f'''
          <form class="form" data-form="demo" data-next="/login/" novalidate>
            <input type="text" name="_hp" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px" />
            <input type="hidden" name="token" value="" data-from-query="token" />
            {field('password', 'New password', 'كلمة المرور الجديدة', 'password', auto='new-password', hint=('At least 8 characters.', '8 أحرف على الأقل.'))}
            {field('password2', 'Confirm new password', 'تأكيد كلمة المرور الجديدة', 'password', auto='new-password', extra=' data-match="#f-password"')}
            <button class="btn btn--primary magnetic btn--block" type="submit"><span data-ar="تعيين كلمة المرور">Set new password</span></button>
            <div class="form__status" role="status" aria-live="polite"></div>
          </form>'''
    sub = '<span data-ar="اختر كلمة مرور جديدة لحسابك.">Choose a new password for your account.</span>'
    return auth_shell('/reset-password/', title='Reset Password - Code & Canvas', title_ar='إعادة تعيين كلمة المرور - Code & Canvas', head='Reset your password', head_ar='إعادة تعيين كلمة المرور', eyebrow='New password · preview only', eyebrow_ar='كلمة مرور جديدة · معاينة فقط', sub_html=sub, form_html=form)


def account():
    body = f'''
      <section class="phero container phero--left" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('Saved books', 'الكتب المحفوظة', None)])}
        <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="قائمة محلية · بلا حساب">A local list · no account</span></span>
        <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s" data-ar="كتبك المحفوظة">Your saved books</h1>
        <p class="hero__lead" data-reveal style="--d:.16s" data-ar="قائمة على هذا الجهاز فقط، وليست مكتبة مشتريات أو حسابًا مسجّلًا. المعاينات مجانية؛ الشراء الإلكتروني غير متاح حاليًا.">A shortlist on this device, not a purchase library or signed-in account. Previews are free; online purchasing is not available yet.</p>
      </section>
      <section class="section container section--flush-top" id="library" aria-label="Saved previews" data-ar-label="المعاينات المحفوظة">
        <p class="notice"><b data-library-count>0</b> <span data-ar="كتب محفوظة">saved books</span></p>
        <div class="grid grid--3" data-library hidden></div>
        <p data-library-empty data-ar="قائمتك فارغة. احفظ كتابًا من المكتبة للعودة إليه هنا.">Your list is empty. Save a book from the library to return to it here.</p>
        <div class="btn-row" style="margin-top:24px">{btn('Explore books', 'تصفّح الكتب', '/books/')}{btn('Manage shortlist', 'إدارة القائمة', '/cart/', 'glass')}</div>
      </section>'''
    return page('/account/', title='Saved books — Code & Canvas', title_ar='الكتب المحفوظة — Code & Canvas', desc='Your local book shortlist and free previews.', desc_ar='قائمة كتبك المحلية والمعاينات المجانية.', nav='books', body=body, scripts=SHOP_JS)


def cart():
    body = f'''
      <section class="phero container phero--left" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('Books', 'الكتب', '/books/'), ('Shortlist', 'القائمة', None)])}
        <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="قائمة محلية · ليست طلب شراء">A local list · not an order</span></span>
        <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s" data-ar="قائمة الكتب المحفوظة">Your book shortlist</h1>
        <p class="hero__lead" data-reveal style="--d:.16s" data-ar="محفوظة على هذا الجهاز فقط. الشراء الإلكتروني غير متاح حاليًا، والأسعار استرشادية حتى تُؤكَّد في عرض مكتوب.">Saved on this device only. Online purchasing is not available yet, and the prices stay indicative until they are confirmed in a written offer.</p>
      </section>
      <section class="section container section--flush-top" aria-label="Shortlist" data-ar-label="القائمة">
        <div class="grid grid--side" data-cart>
          <div>
            <div class="table-wrap" data-cart-table hidden>
              <table class="cart-table">
                <thead><tr><th data-ar="المنتج">Product</th><th data-ar="الكمية">Qty</th><th data-ar="السعر">Price</th><th></th></tr></thead>
                <tbody></tbody>
              </table>
            </div>
            <div class="notice glass" data-cart-empty>{icon('cart')}<div><b data-ar="قائمتك فارغة">Your list is empty</b><p data-ar="تصفّح المكتبة وأضف كتابًا للبدء.">Browse the library and add a book to get started.</p>{btn('Browse books', 'تصفّح الكتب', '/books/', 'glass')}</div></div>
          </div>
          <aside class="summary glass">
            <h3 data-ar="الملخص">Summary</h3>
            <div><span data-ar="المجموع الفرعي">Subtotal</span><b data-cart-total>0 SAR</b></div>
            <div><span data-ar="الضريبة">VAT</span><b data-ar="تُؤكد في العرض المكتوب">Confirmed in a written offer</b></div>
            <div class="total"><span data-ar="الإجمالي">Total</span><b data-cart-total>0 SAR</b></div>
            {btn('Ask about availability', 'استفسار عن التوفر', '/checkout/')}
            <small class="form__hint" data-ar="أسعار استرشادية بالريال · لا يتم تحصيل أي مبلغ">Indicative prices in SAR · no payment collected</small>
          </aside>
        </div>
      </section>
'''
    return page('/cart/', title='Saved book shortlist — Code & Canvas', title_ar='قائمة الكتب المحفوظة — Code & Canvas', desc='Your local shortlist, not a purchase order.', desc_ar='قائمة كتبك المحلية، وليست طلب شراء.', nav='books', body=body, scripts=SHOP_JS)


def checkout():
    body = f'''
      <section class="phero container phero--left" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('Shortlist', 'القائمة', '/cart/'), ('Availability', 'التوفر', None)])}
        <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="استفسار توفر · بلا دفع">Availability inquiry · no payment</span></span>
        <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s" data-ar="استفسر عن توفر الكتب">Ask about book availability</h1>
        <p class="hero__lead" data-reveal style="--d:.16s" data-ar="الشراء الإلكتروني غير متاح حاليًا. هذه رسالة استفسار فقط: لا ندفع ولا نفتح محتوى مدفوعًا، والسعر النهائي والتوفر يُؤكدان قبل أي اتفاق.">Online purchasing is not available yet. This is an inquiry only: no payment or paid access. Availability and final pricing are confirmed before any agreement.</p>
      </section>
      <section class="section container section--flush-top" aria-label="Availability inquiry" data-ar-label="استفسار التوفر">
        <form class="grid grid--side form" data-checkout data-integration="books" data-whatsapp="201092500454" data-mail="info@codeandcanvas.net" data-subject="Book availability" novalidate>
          <div class="form-card glass">
            <h2 data-ar="بيانات التواصل">Contact details</h2>
            {field('name', 'Full name', 'الاسم الكامل', auto='name')}
            {field('email', 'Email', 'البريد الإلكتروني', 'email', auto='email')}
            {field('phone', 'Phone (optional)', 'الهاتف (اختياري)', 'tel', req=False, auto='tel')}
            <label class="check"><input type="checkbox" name="consent" value="1" required /><span data-ar-html="أوافق على &lt;a href=&quot;/terms-of-use/&quot;&gt;الشروط&lt;/a&gt; ومعالجة بيانات الاستفسار وفق &lt;a href=&quot;/privacy-policy/&quot;&gt;سياسة الخصوصية&lt;/a&gt;.">I agree to the <a href="/terms-of-use/">terms</a> and use of my inquiry details under the <a href="/privacy-policy/">privacy policy</a>.</span></label>
            <div class="form__status" role="status" aria-live="polite"></div>
          </div>
          <aside class="summary glass" data-summary>
            <h2 data-ar="الكتب المختارة">Selected books</h2>
            <div data-summary-items></div>
            <div class="total"><span data-ar="إجمالي استرشادي فقط">Indicative total only</span><b data-cart-total>0 SAR</b></div>
            <button class="btn btn--primary" type="submit" data-pay><span data-ar="جهّز رسالة الاستفسار">Prepare availability inquiry</span></button>
            <p class="form__hint" data-ar="في الوضع الحالي، أكمل الإرسال في واتساب. لن يتم تأكيد طلب أو اشتراك تلقائيًا.">In the current mode, finish sending in WhatsApp. No order or subscription is automatically confirmed.</p>
            <a class="text-link" href="/cart/" data-ar="العودة للقائمة">Back to shortlist</a>
          </aside>
        </form>
      </section>'''
    return page('/checkout/', title='Book availability — Code & Canvas', title_ar='توفر الكتب — Code & Canvas', desc='Ask about book availability. No online payment is collected.', desc_ar='استفسر عن توفر الكتب. لا يتم تحصيل أي دفع إلكتروني.', nav='books', body=body, scripts=SHOP_JS)


def thank_you():
    body = f'''
      <section class="phero container phero--center phero--tight" aria-labelledby="page-title">
        <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="خطوة الاستفسار · ليست إيصالًا">Inquiry step · not a receipt</span></span>
        <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s" data-ar="نتابع معك عبر قناتك المختارة">Continue in your chosen channel</h1>
        <p class="notice" role="note" data-reveal style="--d:.16s" data-ar="هذه الصفحة ليست إيصال شراء أو تأكيد حجز. إذا جهزت رسالة، أكمل إرسالها في واتساب أو البريد وانتظر رد الفريق. لم يتم تحصيل أي مبلغ هنا.">This page is not a purchase receipt or booking confirmation. If you prepared a message, finish sending it in WhatsApp or email and wait for the team to reply. No payment was collected here.</p>
        <div class="hero__ctas hero__ctas--center" data-reveal style="--d:.24s">{btn('Contact the team', 'تواصل مع الفريق', '/contact/')}{btn('Read free previews', 'اقرأ المعاينات المجانية', '/books/', 'glass')}</div>
      </section>'''
    return page('/thank-you/', title='Request information — Code & Canvas', title_ar='معلومات الطلب — Code & Canvas', desc='How to follow up on your inquiry.', desc_ar='كيفية متابعة استفسارك.', nav='', body=body)


def build():
    return [login(), register(), forgot(), reset(), account(), cart(), checkout(), thank_you()]
