# -*- coding: utf-8 -*-
"""/book/ — a real first-party booking flow.

Specialty → published business date → 30-minute slot → details + consent →
durable booking record + CRM lead + ICS calendar invite. If the API is not
available, the page says so and offers an explicit manual hand-off; it never
pretends a booking happened. An approved external scheduler can still replace
this path through CC_CONFIG.bookingUrl (see pages.js).
"""
from h import esc, icon, crumbs, closing, btn, page, sec_head, ORG_ID, SITE, media_img

SPECIALTIES = [
    ('brand', 'Brand & identity systems', 'العلامة وأنظمة الهوية'),
    ('product', 'Digital products & websites', 'المنتجات الرقمية والمواقع'),
    ('technology', 'Technology & automation', 'التقنية والأتمتة'),
    ('healthcare', 'Healthcare digital solutions', 'الحلول الرقمية للرعاية الصحية'),
    ('general', 'Not sure yet — help me choose', 'لست متأكدًا بعد — ساعدني أختار'),
]


def build():
    opts = ''.join(f'<option value="{v}" data-ar="{esc(a)}">{esc(e)}</option>' for v, e, a in SPECIALTIES)
    ld = {'@type': 'Service', '@id': SITE + '/book/#service', 'name': 'Free 30-minute discovery call',
          'description': 'A 30-minute remote discovery call with a Code & Canvas founder, in Arabic or English, with a written next step.',
          'provider': {'@id': ORG_ID}, 'areaServed': ['Saudi Arabia', 'Egypt', 'MENA'], 'url': SITE + '/book/'}
    body = f'''
      <section class="phero container phero--left" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('Contact', 'تواصل معنا', '/contact/'), ('Book a call', 'احجز مكالمة', None)])}
        <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="حجز حقيقي · 30 دقيقة · عن بُعد">REAL BOOKING · 30 MIN · REMOTE</span></span>
        <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s"><span data-ar="30 دقيقة،">30 minutes,</span><br /><span class="grad-text" data-ar="وقرار واحد واضح.">one clear decision.</span></h1>
        <p class="hero__lead" data-reveal style="--d:.16s" data-ar="اختر التخصص، ثم موعدًا من ساعات العمل المعلنة، ثم اترك بياناتك. تُسجَّل المكالمة فعليًا، ويُنشأ سجل عميل، وتحصل على تأكيد وملف دعوة تقويم — لا مجرد رابط واتساب.">Choose a specialty, pick a slot inside our published office hours, then leave your details. The call is actually recorded, a CRM lead is created, and you get a confirmation plus a calendar invite — not just a WhatsApp link.</p>
        <div class="hero__ctas" data-reveal style="--d:.24s">{btn('Go to the scheduler', 'اذهب إلى جدول المواعيد', '#scheduler', 'primary', 'arrowDown')}{btn('Prefer a message?', 'تفضّل رسالة؟', '/contact/#message', 'glass', 'mail')}</div>
      </section>

      <section class="section container section--tight" aria-label="SPECIALTY · SLOT · CONFIRMATION" data-ar-label="التخصص · الموعد · التأكيد">
        <figure class="live-figure live-figure--wide live-figure--plate" data-reveal>
          {media_img('art-book-steps', 'Abstract illustrative plate of three settled steps toward one call — not a product screenshot', 'لوحة توضيحية تجريدية لثلاث خطوات منتهية نحو مكالمة واحدة — ليست لقطة منتج', sizes='(max-width: 720px) 92vw, 1200px')}
          <figcaption><span data-ar="التخصص · الموعد · التأكيد">SPECIALTY · SLOT · CONFIRMATION</span><span class="live-figure__disclaimer" data-ar="عمل توضيحي للاستوديو، وليس صورة أشخاص أو عمل عميل">ILLUSTRATIVE STUDIO ARTWORK · NOT A PEOPLE OR CLIENT PHOTO</span></figcaption>
        </figure>
        <p class="live-media-note" data-ar="عمل فني توضيحي: يصف خطوات الحجز الثلاث وليس لقطة من جدول المواعيد ولا إثبات حجز.">Illustrative artwork: it describes the three booking steps and is not a screenshot of the scheduler or evidence of a booked call.</p>
      </section>

      <section class="section container section--flush-top" id="scheduler" aria-labelledby="sched-title">
        <div class="book-shell">
          <div class="book-panel" data-reveal>
            <h2 id="sched-title" style="font-size:clamp(22px,2.3vw,30px);margin:0 0 14px" data-ar="احجز مكالمتك">Book your call</h2>
            <ol class="book-steps" aria-label="Booking steps" data-ar-label="خطوات الحجز">
              <li class="is-active" data-step="1"><b>01</b><span data-ar="التخصص">Specialty</span></li>
              <li data-step="2"><b>02</b><span data-ar="الموعد">Date &amp; time</span></li>
              <li data-step="3"><b>03</b><span data-ar="التأكيد">Confirmation</span></li>
            </ol>

            <form id="book-form" novalidate aria-label="Discovery call booking" data-ar-label="حجز مكالمة استكشافية">
              <input type="text" name="_hp" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px" />
              <label class="book-label" for="b-specialty" data-ar="ما الذي تريد مناقشته؟ *">What do you want to discuss? *</label>
              <select class="book-select" id="b-specialty" name="specialty" required><option value="" data-ar="اختر تخصصًا">Select a specialty</option>{opts}</select>

              <label class="book-label" for="b-date" data-ar="اليوم *">Day *</label>
              <select class="book-select" id="b-date" name="date" required><option value="" data-ar="جارٍ تحميل الأيام المتاحة…">Loading available days…</option></select>

              <label class="book-label" for="b-tz" data-ar="المنطقة الزمنية *">Timezone *</label>
              <select class="book-select" id="b-tz" name="timezone" required>
                <option value="AST" data-ar="توقيت السعودية (AST · UTC+3)">Saudi Arabia (AST · UTC+3)</option>
                <option value="EET" data-ar="توقيت مصر (EET · UTC+2)">Egypt (EET · UTC+2)</option>
                <option value="UTC" data-ar="UTC">UTC</option>
              </select>

              <span class="book-label" id="slots-label" data-ar="اختر موعدًا مدته 30 دقيقة *">Pick a 30-minute slot *</span>
              <div class="slot-grid" id="b-slots" role="group" aria-labelledby="slots-label"><p class="field__hint" data-ar="اختر يومًا أولًا.">Choose a day first.</p></div>
              <input type="hidden" id="b-time" name="time" value="" />

              <div class="form__row" style="margin-top:18px">
                <div class="field" style="margin:0"><label class="book-label" for="b-name" style="margin-top:0" data-ar="الاسم الكامل *">Full name *</label><input class="book-input" id="b-name" name="name" type="text" required autocomplete="name" /></div>
                <div class="field" style="margin:0"><label class="book-label" for="b-email" style="margin-top:0" data-ar="البريد الإلكتروني *">Email *</label><input class="book-input" id="b-email" name="email" type="email" required autocomplete="email" /></div>
              </div>
              <div class="form__row">
                <div class="field" style="margin:0"><label class="book-label" for="b-org" style="margin-top:0" data-ar="المؤسسة (اختياري)">Organization (optional)</label><input class="book-input" id="b-org" name="organization" type="text" autocomplete="organization" /></div>
                <div class="field" style="margin:0"><label class="book-label" for="b-phone" style="margin-top:0" data-ar="الهاتف (اختياري)">Phone (optional)</label><input class="book-input" id="b-phone" name="phone" type="tel" autocomplete="tel" /></div>
              </div>
              <label class="book-label" for="b-notes" data-ar="ما الذي يجب أن نعرفه قبل المكالمة؟ (اختياري)">What should we know before the call? (optional)</label>
              <textarea class="book-textarea" id="b-notes" name="notes" rows="3" data-ar-placeholder="المشكلة، أو النظام الحالي، أو الموعد المستهدف…" placeholder="The problem, your current system, or a target date…"></textarea>

              <label class="book-consent" for="b-consent">
                <input id="b-consent" name="consent" type="checkbox" required />
                <span data-ar-html="أوافق على تخزين بياناتي لمعالجة هذا الطلب والتواصل بشأن المكالمة، وفق &lt;a href=&quot;/privacy-policy/&quot;&gt;سياسة الخصوصية&lt;/a&gt;. يمكنني طلب الحذف عبر info@codeandcanvas.net.">I agree that my details are stored to process this request and contact me about the call, as described in the <a href="/privacy-policy/">Privacy Policy</a>. I can request deletion at info@codeandcanvas.net.</span>
              </label>
              <div class="hero__ctas" style="margin-top:20px">
                <button class="btn btn--primary magnetic" type="submit" id="b-submit"><span data-ar="تأكيد الحجز">Confirm booking</span><i class="flip" data-icon="calendar"></i></button>
                <a class="btn btn--glass" href="/contact/#message"><span data-ar="أرسل رسالة بدلًا من ذلك">Send a message instead</span></a>
              </div>
              <div class="form__status" id="b-status" role="status" aria-live="polite"></div>
            </form>

            <div class="book-confirm" id="b-confirm" hidden>
              <p class="kicker"><span data-ar="تم تأكيد الحجز">BOOKING CONFIRMED</span></p>
              <h2 data-ar="ميعادك مسجّل.">Your slot is reserved.</h2>
              <p class="book-confirm__ref" id="b-ref"></p>
              <div class="book-summary" id="b-summary" style="margin-top:18px"></div>
              <div class="hero__ctas" style="margin-top:20px">
                <a class="btn btn--primary" id="b-ics" href="#"><span data-ar="أضف إلى التقويم (.ics)">Add to calendar (.ics)</span><i class="flip" data-icon="calendar"></i></a>
                <a class="btn btn--glass" href="/contact/"><span data-ar="أضف تفاصيل المشروع">Add project details</span></a>
              </div>
              <p class="book-status" data-ar="سُجّل الحجز في نظام العملاء لدينا. ملف التقويم يتضمن الموعد والتخصص والمرجع. أي إشعار بريدي يعتمد على مزوّد معتمد من جانب الخادم؛ إن لم يصلك بريد، احتفظ برقم المرجع أو راسلنا.">Your booking is recorded in our lead system. The calendar file carries the time, specialty and reference. Email notification depends on an approved server-side provider; if you receive no email, keep the reference or contact us directly.</p>
            </div>
          </div>

          <aside class="sls-side">
            <div class="panel tier" data-reveal>
              <span class="card__icon">{icon('calendar')}</span>
              <h3 data-ar="ملخص المكالمة">Your call</h3>
              <div class="book-summary" style="margin-top:12px">
                <div><span data-ar="المدة">Duration</span><b data-ar="30 دقيقة">30 minutes</b></div>
                <div><span data-ar="اللغة">Language</span><b data-ar="العربية أو الإنجليزية">Arabic or English</b></div>
                <div><span data-ar="المكان">Where</span><b data-ar="عن بُعد">Remote</b></div>
                <div><span data-ar="التكلفة">Cost</span><b data-ar="مجانية">Free</b></div>
              </div>
              <p class="field__hint" style="margin-top:14px" data-ar="نأتي مستعدين: نحدد النطاق ونؤكد الملاءمة ونعطيك الخطوة التالية أو نقول بصراحة إننا لسنا المناسبين.">We come prepared: scope, fit, and one next step — or an honest “not the right fit”.</p>
            </div>
            <div class="panel tier" data-reveal style="--d:.06s">
              <p class="kicker"><span data-ar="ساعات العمل">Office hours</span></p>
              <ul class="kv">
                <li><span data-ar="السعودية">KSA</span><b class="ltr">Sun – Thu · 9:00 – 18:00 AST</b></li>
                <li><span data-ar="مصر">Egypt</span><b class="ltr">Sun – Thu · 9:00 – 18:00 EET</b></li>
              </ul>
              <p class="field__hint" style="margin-top:10px" data-ar="المواعيد المعروضة أيام الأحد–الخميس، وتُحجز لمرة واحدة فقط.">Slots are published for Sun–Thu and each one can be booked only once.</p>
            </div>
            <div class="panel tier" data-reveal style="--d:.12s">
              <h3 data-ar="تحتاج مساعدة قبل الحجز؟">Need help before booking?</h3>
              <p style="margin:8px 0" data-ar="راسلنا على واتساب أو اتصل؛ سنوجّهك للتخصص الصحيح.">Message us on WhatsApp or call — we will point you to the right specialty.</p>
              <a class="text-link" href="https://wa.me/966545520750" target="_blank" rel="noopener"><span data-ar="واتساب ↗">WhatsApp ↗</span></a>
            </div>
          </aside>
        </div>
      </section>

      <section class="section container section--flush-top" id="how" aria-labelledby="how-title">
        {sec_head('01', 'WHAT HAPPENS NEXT', 'ماذا يحدث بعد الحجز', '<span id="how-title" data-ar="من الطلب إلى سجل العميل.">From request to lead record.</span>',
                  'The pipeline is explicit: validation, spam protection, consent, a durable record, a notification and a stage in the CRM.',
                  'المسار معلن: تحقّق، وحماية من الرسائل المزعجة، وموافقة، وسجل دائم، وإشعار، ومرحلة في نظام العملاء.')}
        <div class="case-steps">
          <article class="case-step" data-reveal><span>01 · VALIDATE</span><h3 data-ar="التحقّق">Validation</h3><p data-ar="التحقّق من الحقول والبريد والموعد وساعات العمل والموافقة، مع تحديد معدل الطلبات ومصيدة سبام.">Fields, email, slot, office hours and consent are checked, with rate limiting and a spam honeypot.</p></article>
          <article class="case-step" data-reveal style="--d:.06s"><span>02 · RECORD</span><h3 data-ar="التسجيل">Record &amp; notify</h3><p data-ar="يُحفظ الحجز وينشأ سجل عميل بمرحلة «مؤهّل»، ثم يُطلق إشعار من جانب الخادم.">The booking is stored, a qualified CRM lead is created, and a server-side notification is fired.</p></article>
          <article class="case-step" data-reveal style="--d:.12s"><span>03 · SYNC</span><h3 data-ar="المزامنة">Calendar sync</h3><p data-ar="تحصل على ملف .ics بالموعد والتخصص والمرجع وتذكير قبل ساعة.">You get an .ics file with the time, specialty, reference and a one-hour reminder.</p></article>
        </div>
      </section>

      {closing('OR JUST TALK TO US', 'أو كلّمنا مباشرة',
              '<span data-ar="تحب تبدأ برسالة؟">Prefer to start with a message?</span> <span class="grad-text" data-ar="رسالة واحدة تكفي.">One message is enough.</span>',
              'Tell us the problem and we reply within one business day with a clear next step.',
              'أخبرنا بالمشكلة ونرد خلال يوم عمل واحد بخطوة واضحة.',
              [btn('Send a message', 'أرسل رسالة', '/contact/#message', 'primary', 'mail'), btn('See our services', 'اطّلع على الخدمات', '/services/', 'glass', 'layers')])}
'''
    return [page('/book/', title='Book a 30-Minute Discovery Call — Code & Canvas',
                title_ar='احجز مكالمة استكشافية 30 دقيقة — Code & Canvas',
                desc='Book a real 30-minute discovery call: choose a specialty, pick a published slot, get a confirmation, a CRM record and a calendar invite.',
                desc_ar='احجز مكالمة استكشافية حقيقية مدتها 30 دقيقة: اختر التخصص والموعد، واحصل على تأكيد وسجل عميل ودعوة تقويم.',
                nav='contact', body=body, og_image='/assets/brand/og/book.png', view_track='service_view',
                scripts=('/assets/js/pages.js', '/assets/js/booking.js'), ld=[ld])]
