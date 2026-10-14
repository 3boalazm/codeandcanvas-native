# -*- coding: utf-8 -*-
"""Auth + commerce UI shells — literal field sets from the live WordPress pages
(/login/, /register/, /forgot-password/, /reset-password/, /account-center/,
/cart/, /checkout/, /thank-you/). No backend: forms use data-form="demo" and the
cart is localStorage (assets/js/shop.js). Integration points are in README."""
from h import esc, icon, crumbs, btn, page

SHOP_JS = ('/assets/js/pages.js', '/assets/js/shop.js')


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
    return f'''<a class="btn btn--glass auth__google" href="/login/?provider=google" data-provider="google" aria-disabled="true"><svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><path fill="#EA4335" d="M9 3.5c1.5 0 2.5.6 3.1 1.2l2.3-2.3C13 1.1 11.2.3 9 .3 5.5.3 2.5 2.3 1.1 5.2l2.7 2.1C4.4 5.2 6.5 3.5 9 3.5z"/><path fill="#4285F4" d="M17.6 9.2c0-.7-.1-1.2-.2-1.8H9v3.3h4.9c-.1.8-.6 2-1.8 2.8l2.6 2c1.6-1.4 2.9-3.6 2.9-6.3z"/><path fill="#FBBC05" d="M3.8 10.7c-.2-.6-.3-1.1-.3-1.7s.1-1.2.3-1.7L1.1 5.2C.4 6.3 0 7.6 0 9s.4 2.7 1.1 3.8l2.7-2.1z"/><path fill="#34A853" d="M9 17.7c2.4 0 4.5-.8 6-2.2l-2.6-2c-.8.5-1.8.9-3.4.9-2.5 0-4.6-1.7-5.3-4L1.1 12.5C2.5 15.6 5.5 17.7 9 17.7z"/></svg><span data-ar="المتابعة عبر Google">Continue with Google</span></a>'''


def auth_shell(path, *, title, title_ar, head, head_ar, sub_html, form_html, aside_html='', nav='', desc='', desc_ar=''):
    body = f'''
      <section class="auth container" aria-labelledby="auth-title">
        <div class="auth__card glass glass--deep">
          <a class="auth__brand" href="/"><img src="/assets/brand/icon-white.svg" alt="" width="28" height="28" />Code &amp; Canvas</a>
          <h1 class="auth__title" id="auth-title" data-ar="{esc(head_ar)}">{esc(head)}</h1>
          <p class="auth__sub">{sub_html}</p>
          {form_html}
        </div>
        {aside_html}
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
    return auth_shell('/login/', title='Login - Code & Canvas', title_ar='تسجيل الدخول - Code & Canvas', head='Welcome back', head_ar='أهلًا بعودتك', sub_html=sub, form_html=form)


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
    return auth_shell('/register/', title='Register - Code & Canvas', title_ar='إنشاء حساب - Code & Canvas', head='Create your account', head_ar='أنشئ حسابك', sub_html=sub, form_html=form)


def forgot():
    form = f'''
          <form class="form" data-form="demo" novalidate data-note="If an account exists for this e-mail, a reset link has been sent (backend pending).">
            <input type="text" name="_hp" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px" />
            {field('email', 'Email', 'البريد الإلكتروني', 'email', auto='email')}
            <button class="btn btn--primary magnetic btn--block" type="submit"><span data-ar="إرسال رابط إعادة التعيين">Send reset link</span></button>
            <div class="form__status" role="status" aria-live="polite"></div>
            <a class="text-link" href="/login/"><span data-ar="← العودة لتسجيل الدخول">← Back to sign in</span></a>
          </form>'''
    sub = '<span data-ar="أدخل بريدك الإلكتروني وسنرسل لك رابطًا لإعادة تعيين كلمة المرور.">Enter your e-mail and we’ll send you a link to reset your password.</span>'
    return auth_shell('/forgot-password/', title='Forgot Password - Code & Canvas', title_ar='نسيت كلمة المرور - Code & Canvas', head='Forgot your password?', head_ar='نسيت كلمة المرور؟', sub_html=sub, form_html=form)


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
    return auth_shell('/reset-password/', title='Reset Password - Code & Canvas', title_ar='إعادة تعيين كلمة المرور - Code & Canvas', head='Reset your password', head_ar='إعادة تعيين كلمة المرور', sub_html=sub, form_html=form)


def account():
    nav_items = [('overview', 'Overview', 'نظرة عامة', 'grid'), ('library', 'My Library', 'مكتبتي', 'box'), ('orders', 'Orders', 'الطلبات', 'cart'), ('profile', 'Profile', 'الملف الشخصي', 'users'), ('security', 'Security', 'الأمان', 'lock')]
    navh = ''.join(f'<a href="#{k}" data-acct-link="{k}" class="{"is-active" if k == "overview" else ""}">{icon(ic)}<span data-ar="{esc(ar)}">{esc(en)}</span></a>' for k, en, ar, ic in nav_items)
    body = f'''
      <section class="section container" style="padding-top:calc(var(--nav-h) + 40px)" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('Account Center', 'مركز الحساب', None)])}
        <div class="head-split"><h1 class="section__title" id="page-title" data-ar="مركز الحساب">Account Center</h1><p class="notice notice--inline" data-demo-note hidden></p></div>
        <div class="acct">
          <nav class="acct__nav glass" aria-label="Account" data-ar-label="الحساب" data-acct>
            <div class="acct__user"><span class="avatar">CC</span><div><b data-acct-name>Guest</b><small data-acct-email>guest@codeandcanvas.net</small></div></div>
            {navh}
            <a href="/login/" data-acct-logout>{icon('arrow')}<span data-ar="تسجيل الخروج">Sign out</span></a>
          </nav>
          <div>
            <section class="acct__panel is-active" id="overview" data-acct-panel="overview">
              <div class="grid grid--3">
                <div class="tile tile--mini"><span class="tile__num" data-library-count>0</span><span class="tile__sub" data-ar="كتب في مكتبتك">Books in your library</span></div>
                <div class="tile tile--mini"><span class="tile__num" data-cart-count-tile>0</span><span class="tile__sub" data-ar="عناصر في السلة">Items in cart</span></div>
                <div class="tile tile--mini"><span class="tile__num">—</span><span class="tile__sub" data-ar="طلبات سابقة">Past orders</span></div>
              </div>
              <div class="notice glass" style="margin-top:18px">{icon('alert')}<div><b data-ar="واجهة الحساب جاهزة — الباك-إند قيد الربط">Account UI ready — backend pending</b><p data-ar="هذه الصفحة واجهة كاملة لمركز الحساب (المكتبة، الطلبات، الملف الشخصي، الأمان). تُربط بخدمة المصادقة عبر نقاط التكامل الموثقة في README.">This is the complete Account Center UI (library, orders, profile, security). Connect it to your auth service via the integration points documented in the README.</p></div></div>
            </section>
            <section class="acct__panel" id="library" data-acct-panel="library">
              <h2 class="section__title" style="font-size:24px" data-ar="مكتبتي">My Library</h2>
              <div class="grid grid--3" data-library hidden></div>
              <div class="notice glass" data-library-empty>{icon('box')}<div><b data-ar="مكتبتك فارغة">Your library is empty</b><p data-ar="الكتب التي تشتريها تظهر هنا وتُفتح في القارئ التفاعلي.">Books you purchase appear here and open in the interactive reader.</p>{btn('Browse the library', 'تصفّح المكتبة', '/books/', 'glass')}</div></div>
            </section>
            <section class="acct__panel" id="orders" data-acct-panel="orders">
              <h2 class="section__title" style="font-size:24px" data-ar="الطلبات">Orders</h2>
              <div class="notice glass">{icon('cart')}<div><b data-ar="لا توجد طلبات بعد">No orders yet</b><p data-ar="سجل طلباتك وفواتيرك سيظهر هنا.">Your order history and invoices will appear here.</p></div></div>
            </section>
            <section class="acct__panel" id="profile" data-acct-panel="profile">
              <h2 class="section__title" style="font-size:24px" data-ar="الملف الشخصي">Profile</h2>
              <form class="form form-card glass" data-form="demo" novalidate>
                <div class="form__row">{field('name', 'Full name', 'الاسم الكامل', auto='name')}{field('email', 'Email', 'البريد الإلكتروني', 'email', auto='email')}</div>
                <div class="form__row">{field('phone', 'Phone', 'الهاتف', 'tel', req=False, auto='tel')}{field('company', 'Company (optional)', 'الشركة (اختياري)', req=False, auto='organization')}</div>
                <div class="form__actions"><button class="btn btn--primary" type="submit"><span data-ar="حفظ التغييرات">Save changes</span></button></div>
                <div class="form__status" role="status" aria-live="polite"></div>
              </form>
            </section>
            <section class="acct__panel" id="security" data-acct-panel="security">
              <h2 class="section__title" style="font-size:24px" data-ar="الأمان">Security</h2>
              <form class="form form-card glass" data-form="demo" novalidate>
                {field('current', 'Current password', 'كلمة المرور الحالية', 'password', auto='current-password')}
                <div class="form__row">{field('password', 'New password', 'كلمة المرور الجديدة', 'password', auto='new-password')}{field('password2', 'Confirm new password', 'تأكيد كلمة المرور الجديدة', 'password', auto='new-password', extra=' data-match="#f-password"')}</div>
                <div class="form__actions"><button class="btn btn--primary" type="submit"><span data-ar="تحديث كلمة المرور">Update password</span></button></div>
                <div class="form__status" role="status" aria-live="polite"></div>
              </form>
              <div class="notice glass" style="margin-top:14px">{icon('shield')}<div><b data-ar="التحقق بخطوتين (2FA)">Two-factor authentication (2FA)</b><p data-ar="أضف تطبيق مصادقة لحماية حسابك — يُفعَّل عند ربط الباك-إند.">Add an authenticator app to protect your account — enabled once the backend is connected.</p><button class="btn btn--glass" type="button" disabled><span data-ar="تفعيل 2FA">Enable 2FA</span></button></div></div>
            </section>
          </div>
        </div>
      </section>
'''
    return page('/account/', title='Account Center - Code & Canvas', title_ar='مركز الحساب - Code & Canvas', desc='Your Code & Canvas account: library, orders, profile, and security.', desc_ar='حسابك في Code & Canvas: المكتبة والطلبات والملف الشخصي والأمان.', nav='', body=body, scripts=SHOP_JS)


def cart():
    body = f'''
      <section class="section container" style="padding-top:calc(var(--nav-h) + 40px)" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('Books', 'الكتب', '/books/'), ('Cart', 'السلة', None)])}
        <h1 class="section__title" id="page-title" data-ar="سلة التسوق">Your Cart</h1>
        <div class="grid grid--side" data-cart>
          <div>
            <div class="table-wrap" data-cart-table hidden>
              <table class="cart-table">
                <thead><tr><th data-ar="المنتج">Product</th><th data-ar="الكمية">Qty</th><th data-ar="السعر">Price</th><th></th></tr></thead>
                <tbody></tbody>
              </table>
            </div>
            <div class="notice glass" data-cart-empty>{icon('cart')}<div><b data-ar="سلتك فارغة">Your cart is empty</b><p data-ar="تصفّح المكتبة وأضف كتابًا للبدء.">Browse the library and add a book to get started.</p>{btn('Browse books', 'تصفّح الكتب', '/books/', 'glass')}</div></div>
          </div>
          <aside class="summary glass">
            <h3 data-ar="الملخص">Summary</h3>
            <div><span data-ar="المجموع الفرعي">Subtotal</span><b data-cart-total>0 SAR</b></div>
            <div><span data-ar="الضريبة">VAT</span><b data-ar="تُحسب عند الدفع">Calculated at checkout</b></div>
            <div class="total"><span data-ar="الإجمالي">Total</span><b data-cart-total>0 SAR</b></div>
            {btn('Proceed to checkout', 'إتمام الشراء', '/checkout/')}
            <small class="form__hint" data-ar="الأسعار بالريال السعودي · دفع آمن">Prices in SAR · secure checkout</small>
          </aside>
        </div>
      </section>
'''
    return page('/cart/', title='Cart - Code & Canvas', title_ar='السلة - Code & Canvas', desc='Your Code & Canvas cart.', desc_ar='سلة التسوق في Code & Canvas.', nav='books', body=body, scripts=SHOP_JS)


def checkout():
    body = f'''
      <section class="section container" style="padding-top:calc(var(--nav-h) + 40px)" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('Cart', 'السلة', '/cart/'), ('Checkout', 'الدفع', None)])}
        <h1 class="section__title" id="page-title" data-ar="إتمام الشراء">Checkout</h1>
        <form class="grid grid--side form" data-checkout novalidate>
          <div class="form-card glass">
            <h3 data-ar="بيانات الفاتورة">Billing details</h3>
            <div class="form__row">{field('name', 'Full name', 'الاسم الكامل', auto='name')}{field('email', 'Email', 'البريد الإلكتروني', 'email', auto='email')}</div>
            <div class="form__row">{field('phone', 'Phone', 'الهاتف', 'tel', auto='tel', placeholder='+966 5x xxx xxxx')}<div class="field"><label for="f-country" data-ar="الدولة">Country</label><select id="f-country" name="country" required><option value="SA">Saudi Arabia</option><option value="EG">Egypt</option><option value="AE">United Arab Emirates</option><option value="KW">Kuwait</option><option value="QA">Qatar</option><option value="BH">Bahrain</option><option value="OM">Oman</option><option value="JO">Jordan</option><option value="OTHER">Other</option></select><span class="field__err" data-ar="اختر الدولة">Choose a country</span></div></div>
            <h3 style="margin-top:22px" data-ar="طريقة الدفع">Payment method</h3>
            <div class="pay-methods">
              <label><input type="radio" name="pay" value="card" checked /><div><b data-ar="بطاقة ائتمان / مدى">Credit card / mada</b><small data-ar="Visa · Mastercard · mada · Apple Pay">Visa · Mastercard · mada · Apple Pay</small></div></label>
              <label><input type="radio" name="pay" value="transfer" /><div><b data-ar="تحويل بنكي">Bank transfer</b><small data-ar="نرسل لك بيانات الحساب بعد الطلب">We send account details after the order</small></div></label>
              <label><input type="radio" name="pay" value="wallet" /><div><b data-ar="محفظة إلكترونية (مصر)">E-wallet (Egypt)</b><small>Vodafone Cash · InstaPay</small></div></label>
            </div>
            <label class="check" style="margin-top:16px"><input type="checkbox" name="consent" value="1" required /><span data-ar-html="أوافق على &lt;a href=&quot;/terms-of-use/&quot;&gt;شروط الاستخدام&lt;/a&gt;.">I agree to the <a href="/terms-of-use/">Terms of Use</a>.</span></label>
          </div>
          <aside class="summary glass" data-summary>
            <h3 data-ar="طلبك">Your order</h3>
            <div data-summary-items></div>
            <div class="total"><span data-ar="الإجمالي">Total</span><b data-cart-total>0 SAR</b></div>
            <button class="btn btn--primary magnetic" type="submit" data-pay>{icon('lock')}<span data-ar="ادفع الآن">Pay now</span></button>
            <small class="form__hint" data-ar="بوابة الدفع تُربط عبر shop.js › checkout() — انظر README.">Payment gateway connects via shop.js › checkout() — see README.</small>
            <a class="text-link" href="/cart/"><span data-ar="← العودة للسلة">← Back to cart</span></a>
          </aside>
        </form>
      </section>
'''
    return page('/checkout/', title='Checkout - Code & Canvas', title_ar='إتمام الشراء - Code & Canvas', desc='Secure checkout — Code & Canvas books.', desc_ar='دفع آمن — كتب Code & Canvas.', nav='books', body=body, scripts=SHOP_JS)


def thank_you():
    body = f'''
      <section class="oops" aria-labelledby="page-title">
        <div>
          <span class="card__icon" style="margin:0 auto 18px">✅</span>
          <h1 id="page-title"><span data-ar="شكرًا لك —">Thank you —</span> <span class="grad-text" data-ar="وصلنا طلبك.">we’ve got it.</span></h1>
          <p data-ar="سنعود إليك خلال 24 ساعة عمل. الكتب المشتراة تظهر في مكتبتك فورًا.">We’ll get back to you within 24 business hours. Purchased books appear in your library immediately.</p>
          <p class="notice notice--inline" data-demo-note hidden style="margin:18px auto 0;max-width:560px"></p>
          <div class="oops__links">{btn('Open my library', 'افتح مكتبتي', '/account/#library')}{btn('Back to home', 'العودة للرئيسية', '/', 'glass')}{btn('WhatsApp us', 'راسلنا واتساب', 'https://wa.me/966545520750', 'ghost', 'chat')}</div>
        </div>
      </section>
'''
    return page('/thank-you/', title='Thank you - Code & Canvas', title_ar='شكرًا لك - Code & Canvas', desc='Thank you — your request has been received.', desc_ar='شكرًا لك — تم استلام طلبك.', nav='', body=body, scripts=SHOP_JS)


def build():
    return [login(), register(), forgot(), reset(), account(), cart(), checkout(), thank_you()]
