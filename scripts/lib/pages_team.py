# -*- coding: utf-8 -*-
"""/team/ — the two founders, what each one owns in the service catalogue, and the
engagements that require both. v3 layout: numbered heads, ownership rows, dense index."""
from h import esc, icon, crumbs, closing, btn, page, sec_head, facts, svc_index_row, PERSON_LD
from catalog import SERVICES, TRACKS

AHMED = {
    'id': 'ahmed',
    'name': 'Ahmed M. Bedeer',
    'mono': 'AB',
    'role': 'Co-Founder · Enterprise Architect · Solution Architect',
    'role_ar': 'شريك مؤسس · مهندس معماري مؤسسي · مهندس حلول',
    'kicker': 'THE CODE',
    'kicker_ar': 'الكود',
    'lead': 'Enterprise architecture, healthcare systems and data — the technical half of every engagement.',
    'lead_ar': 'العمارة المؤسسية وأنظمة الرعاية الصحية والبيانات — النصف التقني في كل مشروع.',
    'body': 'Ahmed maps a business goal to the systems, data and governance that can actually deliver it, using TOGAF ADM and ArchiMate on a Business Motivation Model base. In healthcare he works from inside the ecosystem — clinical workflow, HIS selection, EMRAM readiness and CBAHI-aware architecture — so a technology recommendation is defensible to clinicians and to a board.',
    'body_ar': 'يربط أحمد هدف العمل بالأنظمة والبيانات والحوكمة القادرة على تحقيقه فعليًا، مستندًا إلى TOGAF ADM و ArchiMate فوق نموذج دوافع الأعمال. وفي الرعاية الصحية يعمل من داخل المنظومة — مسارات العمل السريرية واختيار HIS وجاهزية EMRAM والعمارة الواعية بـ CBAHI — فتكون التوصية التقنية مقبولة سريريًا وقابلة للدفاع أمام مجلس الإدارة.',
    'quote': '“If it can’t be traced to a business goal, it doesn’t belong in the architecture.”',
    'quote_ar': '«إن لم يكن قابلًا للتتبع إلى هدف عمل، فلا مكان له في العمارة.»',
    'creds': [('TOGAF ADM', None), ('ArchiMate 3.1', None), ('NORA', None), ('CPHIMS', None),
              ('HIMSS EMRAM', None), ('FHIR · HL7', None), ('Data Management', 'إدارة البيانات'),
              ('Cloud Architecture', 'العمارة السحابية'), ('Java · Spring Boot', None)],
    'links': [('LinkedIn', 'linkedin', 'https://linkedin.com/in/ahmed-bedeer'),
              ('Portfolio', 'link', 'https://ahmed-bedeer.vercel.app/'),
              ('GitHub', 'github', 'https://github.com/ahmedbdeer')],
    'track': 'technology',
}

MUSTAFA = {
    'id': 'mustafa',
    'name': 'Mustafa Aboalazm',
    'mono': 'MA',
    'role': 'Co-Founder · Creative Director · Visual Brand Architect',
    'role_ar': 'شريك مؤسس · مدير إبداعي · مهندس هوية بصرية',
    'kicker': 'THE CANVAS',
    'kicker_ar': 'الكانفاس',
    'lead': 'Brand strategy, visual systems and editorial direction — the half that decides how the work is seen.',
    'lead_ar': 'استراتيجية العلامة والأنظمة البصرية والإخراج التحريري — النصف الذي يحدد كيف يُرى العمل.',
    'body': 'Mustafa treats brand work as commercial work: positioning first, then a system — logo, type, grid, colour and the rules that keep it consistent in Arabic and English. He runs the four-act process (Discovery, Strategy, Concept, Refine) because skipping strategy produces a logo file, not a brand a team can operate.',
    'body_ar': 'يتعامل مصطفى مع عمل العلامة كعمل تجاري: التموضع أولًا، ثم نظام كامل — الشعار والخطوط والشبكة واللون وقواعد تحفظ الاتساق بالعربية والإنجليزية. ويدير منهجية الفصول الأربعة (استكشاف، استراتيجية، مفهوم، صقل) لأن تخطّي الاستراتيجية ينتج ملف شعار، لا علامة يستطيع فريق تشغيلها.',
    'quote': '“A brand is the rule set a team can follow when we’re not in the room.”',
    'quote_ar': '«العلامة هي مجموعة القواعد التي يستطيع الفريق اتباعها عندما لا نكون في الغرفة.»',
    'creds': [('Brand Strategy', 'استراتيجية العلامة'), ('Visual Systems', 'الأنظمة البصرية'),
              ('Arabic Typography', 'الطباعة العربية'), ('Design Systems', 'أنظمة التصميم'),
              ('Figma · Webflow', None), ('Art Direction', 'الإخراج الفني'),
              ('Print & Packaging', 'المطبوعات والتغليف'), ('Photography', 'التصوير'), ('Video Production', 'إنتاج الفيديو')],
    'links': [('Behance', 'pen', 'https://behance.net/aboalazm'),
              ('Portfolio', 'link', 'https://aboalazm-os.vercel.app/'),
              ('WhatsApp', 'chat', 'https://wa.me/201092500454')],
    'track': 'creative',
}



def tag_soft(en, ar=None):
    """Credential chip: Arabic variant only when one exists (no empty data-ar)."""
    if ar:
        return f'<span class="tag-soft" data-ar="{esc(ar)}">{esc(en)}</span>'
    return f'<span class="tag-soft">{esc(en)}</span>'


def owns(track):
    """Services a person owns, straight from the catalogue (no invented capability list)."""
    return [c for c, s in SERVICES.items() if TRACKS[s['track']]['owner'] == ('Ahmed Bedeer' if track == 'technology' else 'Mustafa Aboalazm')]


def person(p, delay=0):
    creds = ''.join(tag_soft(e, a) for e, a in p['creds'])
    links = ''.join(
        f'<a class="text-link" href="{u}" target="_blank" rel="noopener">{icon(ic)}<span>{esc(label)}</span></a>'
        for label, ic, u in p['links'])
    codes = owns(p['track'])
    owned = ''.join(
        f'<li><a href="/{TRACKS[SERVICES[c]["track"]]["page"].strip("/")}/#{c.lower()}" data-track="service-detail" data-track-id="{c}">'
        f'<span class="idx__code">{c}</span><span class="idx__title" data-ar="{esc(SERVICES[c]["title_ar"])}">{esc(SERVICES[c]["title"])}</span></a></li>'
        for c in codes)
    return f'''
        <section class="section container work-case" id="{p['id']}" aria-labelledby="{p['id']}-title" data-reveal{' style="--d:%.2fs"' % delay if delay else ''}>
          <div class="who">
            <div class="who__side">
              <span class="who__mono" aria-hidden="true">{p['mono']}</span>
              <p class="kicker"><span data-ar="{esc(p['kicker_ar'])}">{p['kicker']}</span></p>
              <h2 class="who__name" id="{p['id']}-title">{esc(p['name'])}</h2>
              <p class="who__role" data-ar="{esc(p['role_ar'])}">{esc(p['role'])}</p>
              <div class="who__links">{links}</div>
            </div>
            <div class="who__body">
              <p class="lead" data-ar="{esc(p['lead_ar'])}">{esc(p['lead'])}</p>
              <p data-ar="{esc(p['body_ar'])}">{esc(p['body'])}</p>
              <blockquote class="who__quote" data-ar="{esc(p['quote_ar'])}">{esc(p['quote'])}</blockquote>
              <div class="who__creds">{creds}</div>
              <p class="who__owns-label"><b data-ar="يقود من الكتالوج">Owns in the catalogue</b><span>{len(codes)} <span data-ar="خدمة">services</span></span></p>
              <ul class="idx idx--compact">{owned}</ul>
            </div>
          </div>
        </section>'''


def build():
    both = [c for c, s in SERVICES.items() if TRACKS[s['track']]['owner'] == 'Both founders']
    both_rows = ''.join(svc_index_row(c) for c in both)

    body = f'''
      <!-- ░░ Hero ░░ -->
      <section class="phero container phero--left" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('About', 'من نحن', '/about/'), ('Team', 'الفريق', None)])}
        <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="استوديو بشريكين · لا فريق وسيط">Two partners · no account layer</span></span>
        <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s"><span data-ar="من ينفّذ مشروعك فعلًا.">Who actually does your work.</span></h1>
        <p class="hero__lead" data-reveal style="--d:.16s" data-ar-html="لا يوجد فريق حساب بينك وبين من يبني. كل مشروع يقوده أحد المؤسسين — والخدمات التي تحتاج الاثنين معلنة صراحة أدناه. {len(SERVICES)} خدمة موزّعة على ثلاثة نطاقات ملكية: التقنية، والإبداع، وما يتطلب المؤسسين معًا.">There is no account team between you and the people building. Every engagement is led by one of the two founders — and the services that need both are listed explicitly below. {len(SERVICES)} services across three ownership scopes: technology, creative, and both founders.</p>
        <nav class="subnav" aria-label="On this page" data-ar-label="في هذه الصفحة" data-reveal style="--d:.22s"><a href="#ahmed" data-ar="أحمد بدير">Ahmed Bedeer</a><a href="#mustafa" data-ar="مصطفى أبو العزم">Mustafa Aboalazm</a><a href="#both" data-ar="ما يحتاج الاثنين">Needs both</a><a href="#career" data-ar="تطوير الفريق">Freelancers</a></nav>
      </section>

      <!-- ░░ The studio in numbers ░░ -->
      <section class="section container section--tight" aria-label="The studio in numbers" data-ar-label="الاستوديو في أرقام">
        {facts([('Partners delivering the work', 'شريكان ينفّذان العمل', '2', True),
                ('Productized services', 'خدمة مُنتجة', str(len(SERVICES)), True),
                ('Owned by one founder', 'تخص أحد المؤسسين', str(sum(1 for s in SERVICES.values() if TRACKS[s['track']]['owner'] != 'Both founders')), True),
                ('Require both founders', 'تحتاج المؤسسين معًا', str(len(both)), True),
                ('Countries — KSA · Egypt', 'دولتان — السعودية · مصر', '2', True)])}
      </section>

      {person(AHMED)}
      {person(MUSTAFA, .05)}

      <!-- ░░ Needs both ░░ -->
      <section class="section container section--flush-top" id="both" aria-labelledby="both-title">
        {sec_head('03', 'BOTH FOUNDERS', 'المؤسسان معًا',
                  '<span id="both-title" data-ar="ما لا يقدر عليه أحدهما منفردًا.">What neither one does alone.</span>',
                  'Healthcare and combined-launch engagements run on one brief with two owners — clinical and regulatory context from Ahmed, brand and interface from Mustafa, one contract and one accountable timeline.',
                  'مشاريع الرعاية الصحية والإطلاق المتكامل تعمل بموجز واحد ومالكين اثنين — السياق السريري والتنظيمي من أحمد، والعلامة والواجهة من مصطفى، بعقد واحد وجدول زمني واحد مسؤول.',
                  aside=btn('Compare the tracks', 'قارن المسارات', '/services/', 'glass'))}
        <ul class="idx">{both_rows}</ul>
      </section>

      <!-- ░░ Freelancers ░░ -->
      <section class="section container section--flush-top" id="career" aria-labelledby="career-title">
        <div class="grid grid--side-l">
          <header class="sec-head sticky" data-reveal>
            <p class="sec-head__no"><b>04</b><span data-ar="التعاون المستقل">FREELANCE</span></p>
            <h2 id="career-title"><span data-ar="مستقل؟">Freelancer?</span> <span class="grad-text" data-ar="انضم إلى فريق التطوير.">Join the delivery bench.</span></h2>
            <p class="lead" data-ar="نعمل مع مستقلين في التصميم والهندسة والمحتوى داخل المنطقة. أخبرنا بما أنجزته فعلًا — نردّ على كل طلب جادّ، ولو كان الرد لا.">We work with freelancers in design, engineering, and content across the region. Tell us what you have actually shipped — every serious application gets an answer, even when the answer is no.</p>
            <ul class="hero__chips" aria-label="What we look for" data-ar-label="ما الذي نبحث عنه"><li>{icon('pen')}<span data-ar="التصميم">Design</span></li><li>{icon('layers')}<span data-ar="الهندسة">Engineering</span></li><li>{icon('sparkles')}<span data-ar="المحتوى والإنتاج">Content &amp; Production</span></li></ul>
          </header>
          <form class="form-card panel form" data-form="contact" data-integration="career" data-whatsapp="201092500454" data-mail="info@codeandcanvas.net" data-subject="Freelancer application — Code &amp; Canvas" data-endpoint="" novalidate data-reveal>
            <h3 data-ar="الطلب">Application</h3>
            <p class="lead" data-ar="نموذج مختصر — املأ ما ينطبق عليك وأرسل.">Short form — fill what applies and send.</p>
            <input class="hp" type="text" name="_hp" tabindex="-1" autocomplete="off" aria-hidden="true" />
            <input type="hidden" name="inquiry" value="Freelancer / Career" />
            <div class="form__row">
              <div class="field"><label for="f-name" data-ar-html="اسمك &lt;i&gt;*&lt;/i&gt;">Your Name <i>*</i></label><input id="f-name" name="name" type="text" required autocomplete="name" /><span class="field__err" data-ar="أدخل اسمك">Please enter your name</span></div>
              <div class="field"><label for="f-city" data-ar="تعيش في؟">Live in?</label><input id="f-city" name="live_in" type="text" autocomplete="address-level2" /></div>
            </div>
            <div class="field"><label for="f-email" data-ar-html="البريد الإلكتروني &lt;i&gt;*&lt;/i&gt;">Email <i>*</i></label><input id="f-email" name="email" type="email" required autocomplete="email" /><span class="field__err" data-ar="أدخل بريدًا صحيحًا">Please enter a valid e-mail</span></div>
            <div class="field"><label for="f-spark" data-ar="مجال تخصّصك">Your Discipline</label><input id="f-spark" name="skill_spark" type="text" placeholder="Brand design · Next.js · Motion · Copywriting…" data-ar-placeholder="تصميم هوية · Next.js · موشن · كتابة محتوى…" /></div>
            <div class="field"><label for="f-growth" data-ar="ما أنجزته فعلًا">What you have shipped</label><textarea id="f-growth" name="chapters_of_growth" rows="3" placeholder="Where you started, what you have shipped, what you are learning now." data-ar-placeholder="من أين بدأت، وماذا أنجزت، وماذا تتعلم الآن."></textarea></div>
            <div class="form__row">
              <div class="field"><label for="f-portfolio" data-ar="رابط الأعمال">Portfolio URL</label><input id="f-portfolio" name="portfolio_url" type="url" placeholder="https://" /></div>
              <div class="field"><label for="f-cv" data-ar="رابط السيرة الذاتية">CV URL</label><input id="f-cv" name="cv_url" type="url" placeholder="https://" /></div>
            </div>
            <div class="field"><label for="f-time" data-ar="وقت فراغك اليومي">Your Daily free time</label>
              <select id="f-time" name="daily_free_time"><option value="" data-ar="- اختر -">- Select -</option><option value="Daytime" data-ar="نهارًا">Daytime</option><option value="Nighttime" data-ar="ليلًا">Nighttime</option></select></div>
            <div class="field"><label for="f-note" data-ar="ملاحظتك">Your note</label><textarea id="f-note" name="message" rows="3"></textarea></div>
            <div class="form__actions">
              <button class="btn btn--primary magnetic" type="submit"><span data-ar="إرسال">Submit</span><i class="flip" data-icon="arrowUpRight"></i></button>
              <span class="field__hint" data-ar="يُفتح طلبك في واتساب أو البريد حتى يُربط النموذج بخدمة إرسال.">Opens in WhatsApp or e-mail until a form endpoint is connected.</span>
            </div>
            <div class="form__status" role="status" aria-live="polite"></div>
          </form>
        </div>
      </section>

      {closing('ONE BRIEF, TWO DISCIPLINES', 'موجز واحد، تخصصان',
               '<span data-ar="موجز واحد. مالكَان.">One brief. Two owners.</span><br /><span class="grad-text" data-ar="بلا فجوات تسليم.">No handoff gaps.</span>',
               'One shared brief means the brand desk and the architecture board never lose each other’s context. Tell us where your problem sits and we will point you to the founder who leads it.',
               'موجز واحد مشترك يعني أن مكتب العلامة ولوحة العمارة لا يفقدان سياق بعضهما. أخبرنا أين تقع مشكلتك وسنوجّهك إلى المؤسس الذي يقودها.',
               [btn('Contact', 'تواصل معنا', '/contact/'), btn('Services', 'الخدمات', '/services/', 'glass', 'arrow')])}
'''
    return [page('/team/', title='Team — Code & Canvas', title_ar='الفريق — Code & Canvas',
                 desc='Two founders deliver the work and there is no account layer between them. Ahmed M. Bedeer leads technology and healthcare engagements; Mustafa Aboalazm leads creative and brand systems — with a published list of the services that require both.',
                 desc_ar='مؤسسان ينفّذان العمل بلا فريق حساب وسيط. يقود أحمد بدير مشاريع التقنية والرعاية الصحية، ويقود مصطفى أبو العزم مشاريع الإبداع وأنظمة العلامة — مع قائمة معلنة للخدمات التي تتطلب المؤسسين معًا.',
                 nav='about', body=body, ld=[PERSON_LD['ahmed'], PERSON_LD['mustafa']])]
