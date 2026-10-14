# -*- coding: utf-8 -*-
"""/contact/ — live copy of codeandcanvas.net/contact/ + the #book section that
every "Book an Appointment" button on the live site pointed at (it never existed).

Integration points (see README › Integration points):
  · form[data-form="contact"] data-endpoint="" → set a JSON POST URL to deliver
    messages server-side; empty = WhatsApp / e-mail hand-off with pre-filled text.
  · #book  data-booking-url="" → set a Calendly / Cal.com / TidyCal URL and the
    "Book a Free Strategy Call" button opens it; empty = WhatsApp + form.
"""
from catalog import SERVICES
from h import esc, icon, crumbs, closing, btn, page

INQUIRY_GROUPS = [
    ('Brand & Creative', 'الهوية والإبداع', ['MA-01', 'MA-02', 'MA-03', 'MA-04', 'MA-05', 'MA-06', 'MA-07', 'MA-08', 'MA-09', 'MA-10']),
    ('Technology & EA', 'التقنية والعمارة المؤسسية', ['AB-01', 'AB-02', 'AB-03', 'AB-04', 'AB-05', 'AB-06']),
    ('Combined', 'متكاملة', ['CC-01', 'CC-02']),
    ('Healthcare', 'الرعاية الصحية', ['HC-01', 'HC-02', 'HC-03', 'HC-04', 'HC-05']),
]


def build():
    groups = ''
    for g_en, g_ar, codes in INQUIRY_GROUPS:
        opts = ''.join(f'<option value="{c} · {esc(SERVICES[c]["title"])}" data-ar="{c} · {esc(SERVICES[c]["title_ar"])}{" ⭐" if SERVICES[c].get("star") else ""}">{c} · {esc(SERVICES[c]["title"])}{" ⭐" if SERVICES[c].get("star") else ""}</option>' for c in codes)
        groups += f'<optgroup label="{esc(g_en)}" data-ar-label="{esc(g_ar)}">{opts}</optgroup>'

    body = f'''
      <!-- ░░ Hero ░░ -->
      <section class="phero container phero--center" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('Contact', 'تواصل معنا', None)])}
        <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="تواصل معنا">Get In Touch</span></span>
        <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s"><span data-ar="لا نطيق الانتظار">Can’t wait to</span><br /><span class="grad-text" data-ar="لنسمع منك.">hear from you.</span></h1>
        <p class="hero__lead" data-reveal style="--d:.16s" data-ar="كل مشروع يبدأ بمحادثة. اختر القناة الأنسب لك — وسنرد خلال يوم عمل واحد.">Every engagement starts with a conversation. Pick the channel that works best for you — we'll respond within one business day.</p>
      </section>

      <!-- ░░ Channels ░░ -->
      <section class="section container section--tight" aria-label="Contact channels" data-ar-label="قنوات التواصل">
        <div class="contact-grid">
          <article class="card glass contact-card" data-reveal>
            <span class="card__icon">{icon('phoneCall')}</span>
            <h3 data-ar="تواصل مباشر">Direct Contact</h3>
            <ul class="kv">
              <li><span data-ar="الهاتف · السعودية">Phone · KSA</span><a class="ltr" href="tel:+966545520750">+966 545 520 750</a></li>
              <li><span data-ar="الهاتف · مصر">Phone · Egypt</span><a class="ltr" href="tel:+201092500454">+20 109 250 0454</a></li>
              <li><span data-ar="البريد الإلكتروني">Email</span><a href="mailto:info@codeandcanvas.net">info@codeandcanvas.net</a></li>
            </ul>
            <div class="person__links" style="margin-top:auto">
              <a href="https://ahmed-bedeer.vercel.app/" target="_blank" rel="noopener" title="Ahmed's Portfolio">{icon('link')}<span data-ar="أعمال أحمد">Ahmed · Portfolio</span></a>
              <a href="https://aboalazm-os.vercel.app/" target="_blank" rel="noopener" title="Mustafa's Portfolio">{icon('link')}<span data-ar="أعمال مصطفى">Mustafa · Portfolio</span></a>
              <a href="https://linkedin.com/in/ahmed-bedeer" target="_blank" rel="noopener" title="LinkedIn">{icon('linkedin')}<span>LinkedIn</span></a>
              <a href="https://behance.net/aboalazm" target="_blank" rel="noopener" title="Behance">{icon('pen')}<span>Behance</span></a>
            </div>
          </article>
          <article class="card glass contact-card" data-reveal style="--d:.08s">
            <span class="card__icon">{icon('pin')}</span>
            <h3 data-ar="مواقعنا">Our Locations</h3>
            <ul class="kv">
              <li><span data-ar="مكتب السعودية">KSA Office</span><b data-ar="المروج، الرياض · الخبر · السعودية">Al Murouj, Riyadh · Al Khobar · KSA</b></li>
              <li><span data-ar="مكتب مصر">Egypt Office</span><b data-ar="مدينة العبور · القاهرة · مصر">Al Obour City · Cairo · Egypt</b></li>
            </ul>
            <div class="art art--wide art--map" data-slot="contact/map" aria-hidden="true" style="margin-top:auto;aspect-ratio:16/7"><span class="art__cap" data-ar="الرياض · الخبر · القاهرة">RIYADH · AL KHOBAR · CAIRO</span></div>
          </article>
          <article class="card glass contact-card contact-card--wa" data-reveal style="--d:.16s">
            <span class="card__icon">{icon('chat')}</span>
            <h3 data-ar="أسرع استجابة">Fastest Response</h3>
            <a class="wa-big" href="https://wa.me/966545520750" target="_blank" rel="noopener">
              <strong data-ar="راسلنا على واتساب">Message us on WhatsApp</strong>
              <span data-ar="نرد عادةً خلال ساعات قليلة">Usually replies within a few hours</span>
            </a>
            <p class="kicker" style="margin-top:auto"><span data-ar="تابعنا">Follow Us</span></p>
            <div class="person__links">
              <a href="https://behance.net/aboalazm" target="_blank" rel="noopener" title="Behance">{icon('pen')}<span>Behance</span></a>
              <a href="https://linkedin.com/in/ahmed-bedeer" target="_blank" rel="noopener" title="LinkedIn">{icon('linkedin')}<span>LinkedIn</span></a>
              <a href="https://github.com/ahmedbdeer" target="_blank" rel="noopener" title="GitHub">{icon('github')}<span>GitHub</span></a>
            </div>
          </article>
        </div>
      </section>

      <!-- ░░ Form + booking ░░ -->
      <section class="section container section--flush-top" id="message" aria-labelledby="form-title">
        <div class="grid grid--side">
          <form class="form-card glass form" data-form="contact" data-whatsapp="966545520750" data-mail="info@codeandcanvas.net" data-subject="Website inquiry — Code &amp; Canvas" data-endpoint="" novalidate data-reveal>
            <h2 id="form-title" data-ar="أرسل لنا رسالة">Send us a message</h2>
            <p class="lead" data-ar="أخبرنا عن مشروعك أو تحدّيك أو سؤالك — وسنرد عليك بوضوح، لا بعرض مبيعات.">Tell us about your project, challenge, or question — we'll get back to you with clarity, not a sales pitch.</p>
            <input type="text" name="_hp" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px" />
            <div class="form__row">
              <div class="field"><label for="c-first" data-ar-html="الاسم الأول &lt;i&gt;*&lt;/i&gt;">First Name <i>*</i></label><input id="c-first" name="first_name" type="text" required autocomplete="given-name" /><span class="field__err" data-ar="أدخل اسمك الأول.">Please enter your first name.</span></div>
              <div class="field"><label for="c-last" data-ar-html="اسم العائلة &lt;i&gt;*&lt;/i&gt;">Last Name <i>*</i></label><input id="c-last" name="last_name" type="text" required autocomplete="family-name" /><span class="field__err" data-ar="أدخل اسم عائلتك.">Please enter your last name.</span></div>
            </div>
            <div class="form__row">
              <div class="field"><label for="c-email" data-ar-html="البريد الإلكتروني &lt;i&gt;*&lt;/i&gt;">Email Address <i>*</i></label><input id="c-email" name="email" type="email" required autocomplete="email" /><span class="field__err" data-ar="أدخل بريدًا إلكترونيًا صحيحًا.">Please enter a valid email address.</span></div>
              <div class="field"><label for="c-org" data-ar="المؤسسة / الشركة (اختياري)">Organization / Company (optional)</label><input id="c-org" name="organization" type="text" autocomplete="organization" /></div>
            </div>
            <div class="field">
              <label for="c-inquiry" data-ar-html="ما الذي تبحث عنه؟ &lt;i&gt;*&lt;/i&gt;">What are you looking for? <i>*</i></label>
              <select id="c-inquiry" name="inquiry" required>
                <option value="" data-ar="اختر خدمة أو نوع الاستفسار">Select a service or inquiry type</option>
                {groups}
                <option value="General Inquiry / Not Sure Yet" data-ar="استفسار عام / لست متأكدًا بعد">General Inquiry / Not Sure Yet</option>
              </select>
              <span class="field__err" data-ar="اختر نوع الاستفسار.">Please select an inquiry type.</span>
            </div>
            <div class="field"><label for="c-msg" data-ar-html="رسالتك &lt;i&gt;*&lt;/i&gt;">Your Message <i>*</i></label><textarea id="c-msg" name="message" rows="5" required minlength="10"></textarea><span class="field__err" data-ar="اكتب رسالة قصيرة.">Please write a short message.</span></div>
            <div class="form__actions">
              <button class="btn btn--primary magnetic" type="submit"><span data-ar="أرسل الرسالة">Send Message</span><i class="flip" data-icon="mail"></i></button>
              <span class="field__hint" data-ar="نرد خلال يوم عمل واحد · لا رسائل مزعجة أبدًا">We respond within 1 business day · No spam, ever</span>
            </div>
            <div class="form__status" role="status" aria-live="polite"></div>
          </form>

          <aside class="side" id="book" data-booking-url="" data-reveal style="--d:.1s">
            <div class="card glass glass--deep book-card">
              <span class="card__icon">{icon('calendar')}</span>
              <h3 data-ar="تفضّل مكالمة مجدولة؟">Prefer a scheduled call?</h3>
              <p data-ar="احجز جلسة استراتيجية مجانية مدتها 30 دقيقة — نأتي مستعدين، لا بعرض مبيعات.">Book a free 30-min strategy session — we come prepared, not with a pitch.</p>
              <div class="book-card__actions">
                <a class="btn btn--primary" data-book href="https://wa.me/966545520750?text=Hi%20Code%20%26%20Canvas%20%E2%80%94%20I%27d%20like%20to%20book%20a%2030-min%20discovery%20call." target="_blank" rel="noopener"><span data-ar="احجز مكالمة استراتيجية مجانية">Book a Free Strategy Call</span><i class="flip" data-icon="arrowUpRight"></i></a>
                <a class="btn btn--glass" href="/services/"><span data-ar="عرض الخدمات">View Services</span></a>
              </div>
              <ul class="ticks ticks--dense" style="margin-top:18px">
                <li data-ar="30 دقيقة · عن بُعد · بالعربية أو الإنجليزية">30 minutes · remote · Arabic or English</li>
                <li data-ar="نحدد النطاق ونؤكد الملاءمة ونعطيك سعرًا">We define the scope, confirm the fit, and give you a price</li>
                <li data-ar="أو نخبرك بصراحة إن لم نكن الخيار المناسب">— or tell you directly if we’re not the right match</li>
              </ul>
            </div>
            <div class="card glass book-card" style="margin-top:14px">
              <p class="kicker"><span data-ar="ساعات العمل">Office hours</span></p>
              <ul class="kv">
                <li><span data-ar="السعودية">KSA</span><b class="ltr">Sun – Thu · 9:00 – 18:00 AST</b></li>
                <li><span data-ar="مصر">Egypt</span><b class="ltr">Sun – Thu · 9:00 – 18:00 EET</b></li>
              </ul>
              <p class="field__hint" style="margin-top:10px" data-ar="الرسائل خارج ساعات العمل تُجاب في يوم العمل التالي.">Messages outside office hours are answered the next business day.</p>
            </div>
          </aside>
        </div>
      </section>

      {closing("CAN'T WAIT TO HEAR FROM YOU", 'نتطلع لسماعك',
               '<span data-ar="لا نطيق الانتظار">Can’t Wait To</span><br /><span class="grad-text" data-ar="لنسمع منك.">Hear From You.</span>',
               'Book an appointment, start with our story, or browse the services.',
               'احجز موعدًا، أو ابدأ بقصتنا، أو تصفّح الخدمات.',
               [btn('Book an Appointment', 'احجز موعدًا', '#book', 'primary', 'calendar'), btn('Get Started', 'ابدأ الآن', '/our-story/', 'glass'), btn('Services', 'الخدمات', '/services/', 'ghost', 'arrow')], contact=False)}
'''
    return [page('/contact/', title='Contact — Code & Canvas', title_ar='تواصل معنا — Code & Canvas',
                 desc='Every engagement starts with a conversation. Call, e-mail, or WhatsApp Code & Canvas in KSA (+966 545 520 750) or Egypt (+20 109 250 0454), send a message, or book a free 30-minute strategy call.',
                 desc_ar='كل مشروع يبدأ بمحادثة. اتصل أو راسل Code & Canvas عبر البريد أو واتساب في السعودية (+966 545 520 750) أو مصر (+20 109 250 0454)، أو أرسل رسالة، أو احجز مكالمة استراتيجية مجانية مدتها 30 دقيقة.',
                 nav='contact', body=body)]
