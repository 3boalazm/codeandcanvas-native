# -*- coding: utf-8 -*-
"""/books/ library + /books/<slug>/ landing pages + /books/<slug>/read/ reader shell.

Live sources: /books/ (Arabic-first: "المكتبة الرقمية · كتب Code & Canvas"),
/basics-of-brand-identity/ (full 16-chapter landing — copied literally),
Woo Store API (prices in SAR). Paid book content is NOT copied: the reader loads
/assets/books/<slug>/manifest.json when the owner publishes it (see README) and
otherwise shows the free preview + purchase gate."""
from h import esc, icon, crumbs, closing, btn, page

BOOKS = [
    dict(slug='marketing-fundamentals', n='الكتاب الأول', title_ar='أساسيات التسويق', title='Marketing Fundamentals', code='MF', cat='marketing', cat_label='Marketing', cat_label_ar='تسويق',
         price=249, edition='1st Edition · 2026 · v1.0', author='Code & Canvas · 2026',
         lede_ar='دليل شامل في التسويق الحديث — من فهم العميل إلى الاستراتيجية والنمو والبيانات. 15 جزءًا و258 شريحة تفاعلية بواجهة عربية.',
         lede='A comprehensive guide to modern marketing — from understanding the customer to strategy, growth, and data. 15 parts and 258 interactive slides with an Arabic interface.',
         stats=[('15', 'جزءًا', 'Parts'), ('258', 'شريحة', 'Slides'), ('2026', 'إصدار', 'Edition')], chips=['فهم العميل', 'الاستراتيجية', 'النمو', 'البيانات'],
         art='art--violet', available=True, aliases=['/product/marketing-fundamentals/']),
    dict(slug='basics-of-visual-identity', n='الكتاب الثاني', title_ar='أساسيات الهوية البصرية', title='Basics of Visual Identity', code='VI', cat='design', cat_label='Brand & Design', cat_label_ar='علامة وتصميم',
         price=199, edition='1st Edition · 2026 · v1.0', author='Mustafa Aboalazm · 2026',
         lede_ar='رحلة من اللوجو للنظام الكامل — إزاي تبني هوية بصرية بتتعرف، وتتفكر، وتفضل في دماغ الناس. من الاستراتيجية، للحرفة، للتطبيق.',
         lede='A journey from the logo to the complete system — how to build a visual identity that gets recognised, remembered, and stays in people’s minds. From strategy, to craft, to application.',
         stats=[('16', 'فصلاً', 'Chapters'), ('3', 'رحلات', 'Journeys'), ('2026', 'إصدار', 'Edition')], chips=['الاستراتيجية', 'الحرفة البصرية', 'المهنة'],
         art='art--pink', available=True, aliases=['/basics-of-brand-identity/', '/product/basics-of-visual-identity/']),
    dict(slug='basics-of-graphic-design', n='الكتاب الثالث', title_ar='أساسيات التصميم الجرافيكي', title='Basics of Graphic Design', code='GD', cat='design', cat_label='Brand & Design', cat_label_ar='علامة وتصميم',
         price=199, edition='1st Edition · 2026 · v1.0', author='Mustafa Aboalazm · 2026',
         lede_ar='مدخل عملي لأساسيات التصميم الجرافيكي — المبادئ والتكوين واللون والخط — للمحترفين والمبتدئين على حد سواء.',
         lede='A practical introduction to the fundamentals of graphic design — principles, composition, colour, and type — for professionals and beginners alike.',
         stats=[('1', 'إصدار أول', '1st edition'), ('AR', 'واجهة عربية', 'Arabic UI'), ('2026', 'إصدار', 'Edition')], chips=['المبادئ', 'التكوين', 'اللون', 'الخط'],
         art='art--mint', available=True, aliases=['/product/basics-of-graphic-design/']),
    dict(slug='ui-ux-handbook', n='الكتاب الرابع', title_ar='دليل تجربة وواجهة المستخدم', title='UI/UX Handbook', code='UX', cat='technology', cat_label='Technology', cat_label_ar='تكنولوجيا',
         price=299, edition='Coming soon · 2026', author='Code & Canvas · 2026',
         lede_ar='دليل عملي لتصميم تجارب وواجهات المستخدم — من البحث إلى النماذج الأولية إلى أنظمة التصميم. قريبًا.',
         lede='A hands-on handbook for UX and UI design — from research to prototypes to design systems. Coming soon.',
         stats=[('—', 'فصول', 'Chapters'), ('AR', 'واجهة عربية', 'Arabic UI'), ('2026', 'إصدار', 'Edition')], chips=['البحث', 'النماذج الأولية', 'أنظمة التصميم'],
         art='art--gold', available=False, aliases=['/product/%d8%af%d9%84%d9%8a%d9%84-%d8%aa%d8%ac%d8%b1%d8%a8%d8%a9-%d9%88%d9%88%d8%a7%d8%ac%d9%87%d8%a9-%d8%a7%d9%84%d9%85%d8%b3%d8%aa%d8%ae%d8%af%d9%85/']),
]

# Literal chapter copy from the live /basics-of-brand-identity/ landing page.
VI_JOURNEYS = [
    dict(k='الرحلة الأولى · 4 فصول · التفكير قبل التصميم', name='الاستراتيجية', desc='الهوية القوية بتبدأ في الدماغ — في فهم البراند والسوق والناس — قبل ما تفتح أي برنامج.', chapters=[
        ('أ', 'إيه هي الهوية البصرية؟', 'الفصل الأول · اللوجو مش البراند', 'خمس مصطلحات بتتلخبط مع بعض طول الوقت — البراند، البراندنج، هوية البراند، الهوية البصرية، واللوجو — وكل واحدة حاجة مختلفة.', 'الهوية البصرية هي النظام البصري المتكامل اللي بيمثّل البراند من خلال عناصر تصميم متّسقة بتخلّي الناس تتعرف عليه، وتفتكره، وتثق فيه.', ['البراند = إحساس', 'الهوية = نظام كامل', 'اللوجو = عنصر واحد']),
        ('ب', 'ليه الناس بتشتري البراندات؟', 'الفصل الثاني · الشراء قرار عاطفي', 'في رفّ المحل، عشرة منتجات بنفس الجودة وبنفس السعر. ليه إيد المستهلك بتمتدّ لواحد بالذات؟ مش عشان هو الأحسن — عشان هو البراند اللي بيحسّه.', 'البراند مش موجود على المنتج — هو موجود في عقل العميل. الحضور الذهني أهم من الولاء.', ['الثقة', 'الألفة', 'الإدراك', 'الرابط العاطفي']),
        ('ج', 'استراتيجية البراند', 'الفصل الثالث · قبل أي بكسل', 'التموضع هو المكان اللي البراند بياخده في عقل العميل مقارنةً بالمنافسين. مش اللي إنت بتقوله عن نفسك — اللي العميل بيفتكره عنك.', 'بدء التصميم قبل الاستراتيجية = لو مش عارف البراند واقف فين، أي لوجو هترسمه هيبقى تخمين. الاستراتيجية هي البوصلة.', ['مين جمهورك؟', 'ليه أنت مختلف؟', 'خريطة التموضع']),
        ('د', 'شخصية وصوت البراند', 'الفصل الرابع · لو البراند كان شخص', 'الشخصية هي اللي بتخلّي البراند إنسان بدل شعار جامد. وأسهل طريقة تحدّدها: حرّك البراند على مجموعة مؤشّرات بين طرفين.', 'لما تحتار في لون أو خط، ارجع للشخصية — هي إجابتك. براند مرِح + عصري مستحيل يبقى لونه رمادي وخطّه كلاسيكي.', ['النبرة', 'الرسالة', 'مؤشّرات الشخصية']),
    ]),
    dict(k='الرحلة الثانية · 7 فصول · بناء النظام البصري', name='الحرفة البصرية', desc='من الفكرة للنظام — شعار، ألوان، خطوط، ولغة بصرية كاملة. هنا بنحوّل الاستراتيجية لعناصر ملموسة.', chapters=[
        ('01', 'الاكتشاف والبحث', 'الفصل الخامس · التصميم يبدأ بالبحث', 'قبل ما تفتح أي برنامج، لازم تفهم الأرض اللي واقف عليها. تحليل المنافسين بصرياً على تلات محاور: شعاراتهم، ألوانهم، وخطوطهم.', 'لو كل المنافسين أزرق، الأزرق هيخلّيك تايه — هنا فرصة التميّز.', ['ديموجرافيكس', 'سيكوجرافيك', 'سلوك', 'شخصيات الجمهور']),
        ('02', 'الاتجاه الإبداعي', 'الفصل السادس · الموودبورد أداة تفكير', 'الموودبورد مش مجرد صور حلوة مجمّعة — هو أداة تفكير. والأقاليم البصرية بتقدّم 2-3 اتجاهات مختلفة جذرياً لنفس البراند فالعميل بيختار الروح قبل التفاصيل.', 'كلمات التصميم هي الجسر بين الاستراتيجية والفيجوال — اختَر 3-5 كلمات وخلّي كل عنصر يخدمها.', ['بساطة نوردية', 'حِرفي عتيق', 'فخامة بوتيك']),
        ('03', 'تصميم الشعار', 'الفصل السابع · اللوجو وشّ البراند', 'خمسة أنواع للشعار، وستة مبادئ بتفصل اللوجو اللي بيعيش سنين عن اللي بيتنسى بعد شهر.', 'اختبر قبل ما تسلّم: التحجيم (واضح في 16بكسل؟) — التعرّف (يتفرق عن المنافس؟) — الوضوح (يشتغل أبيض وأسود؟).', ['الكلمة', 'الحرف', 'الرمز', 'المركّب', 'الخاتم']),
        ('04', 'أنظمة الألوان', 'الفصل الثامن · اللون يوصل للإحساس', 'اللون بيوصل للإحساس قبل ما العقل يقرا أي كلمة. قاعدة 60/30/10: توزيع متوازن بيمنع التشتّت.', 'التباين شرط — معيار 4.5:1 للنص العادي على الأقل. لون جميل مش مقروء = فشل.', ['60٪ أساسي', '30٪ ثانوي', '10٪ مميِّز']),
        ('05', 'التايبوجرافي في الهوية', 'الفصل التاسع · الخط بيتكلم', 'اختيار الخط مش جمالي بس — هو قرار في صوت البراند. القاعدة الذهبية: تباين مش تشابه — ادمج خطّين مختلفين بوضوح لكن من نفس المزاج.', None, ['Serif = تقليدي', 'Sans = عصري', 'Script = أنيق', 'Display = معبّر']),
        ('06', 'اللغة البصرية', 'الفصل العاشر · تعرّف بلا لوجو', 'لما تشوف بوست وتعرف صاحبه قبل ما تقرا الاسم — دي اللغة البصرية شغّالة. خمسة عناصر: أشكال، ملامس، أنماط، أيقونات، وعناصر مساندة.', None, ['سُمك ثابت', 'زوايا موحَّدة', 'وزن بصري واحد']),
        ('07', 'اتجاه التصوير', 'الفصل الحادي عشر · الصور بتحكي', 'أسلوب التصوير جزء من الهوية بنفس قوة اللون. صورتين بنفس المنتج بأسلوبين مختلفين بيدّوا إحساسين متناقضين.', 'ثبّت أربع حاجات: الإضاءة · المعالجة اللونية · التكوين · معالجة الموضوع. لما كل ده واحد، الصور بتبان من نفس العائلة.', ['مؤسسي', 'حياتي', 'تحريري']),
    ]),
    dict(k='الرحلة الثالثة · 5 فصول · التطبيق والتقديم', name='المهنة', desc='النظام في الواقع — تطبيق الهوية، توثيقها في دليل، تقديمها للعميل، وبناء مشروع كامل من الصفر.', chapters=[
        ('08', 'تطبيقات الهوية', 'الفصل الثاني عشر · الهوية في الشارع', 'اللحظة الحقيقية للهوية مش في الملف — في الكارت اللي العميل بيمسكه، الباكدج اللي بيتفتح، والبوست اللي بيتشاف وسط مية بوست.', 'اختبر الهوية على أصعب تطبيق من البداية: لو اللوجو شغّال على أيقونة موبايل 24 بكسل وعلى لافتة 3 متر — يبقى نظامك متين.', ['كروت العمل', 'اللافتات', 'السوشيال', 'الموك أب']),
        ('09', 'دليل الهوية', 'الفصل الثالث عشر · دستور الاتساق', 'من غير دليل، الهوية بتتفكّك بعد أول شهر. لما الهوية تخرج من إيدك لإيد ناس تانية — سوشيال، مطبعة، فريق ماركتنج — لازم قواعد تحميها.', None, ['استخدام اللوجو', 'المسموح والممنوع', 'التخطيطات', 'أصول السوشيال']),
        ('10', 'تقديم الهوية', 'الفصل الرابع عشر · أحسن هوية ممكن تتقتل', 'دي نقطة نادراً ما تتغطّى — مع إنها بتفرق بين قبول المشروع ورفضه. العميل مش بيشتري التصميم، بيشتري القصة.', 'اخترت اللون ده عشان حلو = ضعف. اخترت اللون ده عشان بيميّزك عن 3 منافسين كلهم أزرق = احتراف. كل قرار لازم يرجع للاستراتيجية.', ['السياق أولاً', 'المنطق', 'الكشف', 'الدفاع']),
        ('11', 'أنظمة العالم الحقيقي', 'الفصل الخامس عشر · لما البراند يكبر', 'معمار البراند هو إزاي تنظّم العلاقة بين البراند الأم ومنتجاته. تلات نماذج رئيسية: بيت العلامات، البراند المعبّر، والبراند الموحَّد.', 'الهوية الناجحة بتتصمّم عشان تكبر — رمز بسيط بيتمدّد على آلاف التطبيقات أحسن من رسمة معقّدة.', []),
        ('12', 'المشروع + ورش العمل', 'الفصل السادس عشر · مشروع كامل', 'الخلاصة والتحدّي — تطبيق كل ما اتعلّمته في مشروع هوية بصرية كاملة من الصفر: من الاستراتيجية للدليل.', 'اختر براند بتحبّه، وكمّل إطار التحليل عليه. هتتعلم من تحليل الناجحين أكتر من أي كتاب.', ['تحليل البراند', 'بناء النظام', 'التوثيق', 'التقديم']),
    ]),
]


def price_html(b, big=False):
    if not b['available']:
        return f'<span class="book__price book__price--free" data-ar="قريبًا">Coming soon</span>'
    return f'<span class="book__price" dir="ltr">{b["price"]} <small data-ar="ريال سعودي · دفعة واحدة · وصول دائم">SAR · one-time · lifetime access</small></span>'


def add_btn(b, kind='primary'):
    if not b['available']:
        return f'<button class="btn btn--glass" type="button" disabled><span data-ar="قريبًا">Coming soon</span></button>'
    return (f'<button class="btn btn--{kind}" type="button" data-add="{b["slug"]}" data-title="{esc(b["title"])}" data-title-ar="{esc(b["title_ar"])}" data-price="{b["price"]}" data-currency="SAR">'
            f'{icon("cart")}<span data-ar="أضف إلى السلة">Add to cart</span></button>')


def cover(b, size='48px', extra=''):
    return (f'<div class="art {b["art"]} {extra}" data-slot="books/{b["slug"]}/cover" aria-hidden="true"><span class="art__mark" style="font-size:{size};font-family:var(--f-num);font-style:italic;font-weight:800">{b["code"]}</span>'
            f'<span class="art__cap">{esc(b["title"])} · {esc(b["author"])}</span></div>')


def book_card(b, i):
    chips = ''.join(f'<span>{esc(c)}</span>' for c in b['chips'])
    return f'''
          <article class="card glass book{'' if b['available'] else ' is-soon'}" data-category="{b['cat']}" data-reveal style="--d:{(i % 3) * .06:.2f}s">
            <a href="/books/{b['slug']}/" aria-label="{esc(b['title'])}">{cover(b)}</a>
            <div class="book__body">
              <div class="post-card__meta"><span class="badge" data-ar="{esc(b['cat_label_ar'])}">{esc(b['cat_label'])}</span><span>{esc(b['edition'])}</span></div>
              <h3><a href="/books/{b['slug']}/"><span lang="ar" dir="rtl">{esc(b['title_ar'])}</span><br /><small class="grad-text">{esc(b['title'])}</small></a></h3>
              <p data-ar="{esc(b['lede_ar'])}">{esc(b['lede'])}</p>
              <div class="book__chips">{chips}</div>
              <div class="book__foot">{price_html(b)}<a class="text-link" href="/books/{b['slug']}/"><span data-ar="التفاصيل ←">Details →</span></a></div>
            </div>
          </article>'''


def hub():
    cards = ''.join(book_card(b, i) for i, b in enumerate(BOOKS))
    filt = ''.join(f'<button class="filter{" is-active" if k == "all" else ""}" type="button" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}"><span data-ar="{esc(ar)}">{esc(en)}</span></button>'
                   for k, en, ar in [('all', 'All', 'الكل'), ('design', 'Brand & Design', 'علامة وتصميم'), ('marketing', 'Marketing', 'تسويق'), ('technology', 'Technology', 'تكنولوجيا')])
    body = f'''
      <section class="phero container phero--center" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('Books', 'الكتب', None)])}
        <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="المكتبة الرقمية">The Digital Library</span></span>
        <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s"><span data-ar="كتب">Code &amp; Canvas</span> <span class="grad-text" data-ar="Code &amp; Canvas">Books</span></h1>
        <p class="hero__lead" data-reveal style="--d:.16s" data-ar="أدلة عملية في التصميم، التسويق، والتكنولوجيا — للمحترفين والمبتدئين على حد سواء.">Practical guides in design, marketing, and technology — for professionals and beginners alike.</p>
        <div class="filters filters--center" role="group" aria-label="Filter books" data-ar-label="تصفية الكتب" data-filter-group="#book-list" data-reveal style="--d:.22s">{filt}</div>
      </section>

      <section class="section container section--flush-top" aria-label="Books" data-ar-label="الكتب">
        <div class="book-grid" id="book-list">{cards}
        </div>
        <ul class="promises" data-reveal>
          <li>{icon('lock')}<span data-ar="دفع آمن · ريال سعودي">Secure checkout · SAR</span></li>
          <li>{icon('globe')}<span data-ar="قارئ تفاعلي عربي RTL">Interactive Arabic RTL reader</span></li>
          <li>{icon('check')}<span data-ar="وصول دائم بعد الشراء">Lifetime access after purchase</span></li>
          <li>{icon('users')}<span data-ar="مكتبتك في حسابك">Your library lives in your account</span></li>
        </ul>
      </section>

      {closing("CAN'T WAIT TO HEAR FROM YOU", 'نتطلع لسماعك',
               '<span data-ar="لا نطيق الانتظار">Can’t Wait To</span><br /><span class="grad-text" data-ar="لنسمع منك.">Hear From You.</span>',
               'Questions about a book, bulk licences for a team, or a custom training edition? Talk to us.',
               'أسئلة عن كتاب أو تراخيص جماعية لفريقك أو نسخة تدريبية مخصصة؟ كلمنا.',
               [btn('Book an Appointment', 'احجز موعدًا', '/contact/#book'), btn('Get Started', 'ابدأ الآن', '/contact/', 'glass'), btn('Full Services', 'كل الخدمات', '/services/', 'ghost', 'arrow')])}
'''
    return page('/books/', title='Books Library — Arabic Design & Brand References · Code & Canvas', title_ar='المكتبة — مراجع عربية في التصميم والعلامة · Code & Canvas',
                desc='Code & Canvas digital library: practical Arabic guides in design, marketing, and technology — Marketing Fundamentals, Basics of Visual Identity, Basics of Graphic Design, and the UI/UX Handbook.',
                desc_ar='المكتبة الرقمية لـ Code & Canvas: أدلة عربية عملية في التصميم والتسويق والتكنولوجيا — أساسيات التسويق، أساسيات الهوية البصرية، أساسيات التصميم الجرافيكي، ودليل تجربة وواجهة المستخدم.',
                nav='books', body=body, scripts=('/assets/js/pages.js', '/assets/js/shop.js'))


def vi_chapters():
    out = ''
    for j in VI_JOURNEYS:
        items = ''
        for k, title, sub, p1, p2, chips in j['chapters']:
            chip_html = ''.join(f'<span class="pill">{esc(c)}</span>' for c in chips)
            items += f'''
            <div class="faq__item"><button class="faq__q" type="button" aria-expanded="false"><span><i class="chapter__k">{esc(k)}</i> {esc(title)} <small>{esc(sub)}</small></span><span class="pm" aria-hidden="true"></span></button><div class="faq__a"><div><p>{esc(p1)}</p>{f'<p class="quote quote--sm">{esc(p2)}</p>' if p2 else ''}{f'<div class="pill-list">{chip_html}</div>' if chips else ''}</div></div></div>'''
        out += f'''
        <div class="chapter" data-reveal>
          <p class="kicker"><span>{esc(j['k'])}</span></p>
          <h3 class="section__title" style="font-size:clamp(22px,2.4vw,30px)">{esc(j['name'])}</h3>
          <p class="section__lead" style="margin-bottom:16px">{esc(j['desc'])}</p>
          <div class="faq faq--chapters">{items}
          </div>
        </div>'''
    return out


def book_page(b, idx):
    nxt = BOOKS[(idx + 1) % len(BOOKS)]
    stats = ''.join(f'<div class="stat"><span class="stat__num stat__num--ltr">{esc(n)}</span><p class="stat__label" data-ar="{esc(ar)}">{esc(en)}</p></div>' for n, ar, en in b['stats'])
    chips = ''.join(f'<span class="pill">{esc(c)}</span>' for c in b['chips'])
    if b['slug'] == 'basics-of-visual-identity':
        toc = f'''
      <section class="section container section--flush-top" id="chapters" aria-labelledby="toc-title">
        <div class="section__head" data-reveal><p class="kicker"><span data-ar="الفهرس">TABLE OF CONTENTS</span></p><h2 class="section__title" id="toc-title" lang="ar" dir="rtl">ثلاث رحلات · 16 فصلاً</h2></div>
        <div class="grid grid--side-l" dir="rtl" lang="ar" style="display:block;max-width:900px">{vi_chapters()}</div>
      </section>'''
    elif b['slug'] == 'marketing-fundamentals':
        toc = f'''
      <section class="section container section--flush-top" id="chapters" aria-labelledby="toc-title">
        <div class="section__head" data-reveal><p class="kicker"><span data-ar="الجزء الافتتاحي · معاينة مجانية">OPENING PART · FREE PREVIEW</span></p><h2 class="section__title" id="toc-title"><span lang="ar" dir="rtl">الجزء 01 · مقدمة في التسويق</span><br /><span class="grad-text" style="font-size:.6em">Part 01 — Introduction to Marketing</span></h2><p class="section__lead" lang="ar" dir="rtl">مقدمة في التسويق — الأساس الذي يبدأ منه كل شيء قبل الإعلانات والمحتوى والعلامة التجارية.</p></div>
        <div class="grid grid--3" data-reveal>
          <article class="card glass tile"><span class="chapter__k">01</span><h3>What Is Marketing?</h3><p lang="ar" dir="rtl">ما هو التسويق؟</p></article>
          <article class="card glass tile"><span class="chapter__k">02</span><h3>The Evolution</h3><p lang="ar" dir="rtl">تطوّر التسويق</p></article>
          <article class="card glass tile"><span class="chapter__k">03</span><h3>The Ecosystem</h3><p lang="ar" dir="rtl">منظومة التسويق</p></article>
        </div>
        <div class="notice glass" data-reveal style="margin-top:18px">{icon('box')}<div><b data-ar="A MODERN GUIDE · 2026 — 15 جزءًا · 258 شريحة">A MODERN GUIDE · 2026 — 15 parts · 258 slides</b><p data-ar="يُعرض الفهرس الكامل داخل القارئ بعد الشراء — افتح المعاينة المجانية للاطلاع على الجزء الأول. اختصارات القارئ: ← → للتنقل · F للشاشة الكاملة.">The full table of contents is shown inside the reader after purchase — open the free preview to browse Part 01. Reader shortcuts: ← → to navigate · F for fullscreen.</p></div></div>
      </section>'''
    else:
        toc = f'''
      <section class="section container section--flush-top" id="chapters" aria-labelledby="toc-title">
        <div class="notice glass" data-reveal>{icon('box')}<div><b id="toc-title" data-ar="الفهرس التفصيلي">Detailed table of contents</b><p data-ar="{'يُعرض الفهرس الكامل داخل القارئ بعد الشراء — افتح المعاينة المجانية للاطلاع على الأجزاء الأولى.' if b['available'] else 'هذا الكتاب قيد الإعداد — سجّل اهتمامك وسنخبرك عند صدوره.'}">{'The full table of contents is shown inside the reader after purchase — open the free preview to browse the opening parts.' if b['available'] else 'This book is in preparation — register your interest and we will let you know when it ships.'}</p></div></div>
      </section>'''
    buy = f'''
            <div class="book-hero__buy glass">
              {price_html(b, True)}
              {add_btn(b)}
              {f'<a class="btn btn--glass" href="/books/{b["slug"]}/read/">{icon("grid")}<span data-ar="افتح المعاينة المجانية">Open the free preview</span></a>' if b['available'] else f'<a class="btn btn--glass" href="/contact/?inquiry=book-{b["slug"]}"><span data-ar="أبلغني عند الصدور">Notify me at launch</span></a>'}
              <small class="form__hint" data-ar="بعد الشراء يُفتح الكتاب كاملًا في القارئ التفاعلي من حسابك.">After purchase the full book unlocks in the interactive reader from your account.</small>
            </div>'''
    body = f'''
      <section class="phero container" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('Books', 'الكتب', '/books/'), (b['title'], b['title_ar'], None)])}
        <div class="book-hero">
          <div data-reveal>{cover(b, '96px')}</div>
          <div>
            <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="المكتبة · {esc(b['n'])}">Library · {esc(b['title'])}</span></span>
            <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s"><span lang="ar" dir="rtl">{esc(b['title_ar'])}</span><br /><span class="grad-text" style="font-size:.6em">{esc(b['title'])}</span></h1>
            <p class="person__tag" data-reveal style="--d:.12s">{esc(b['edition'])} · {esc(b['author'])}</p>
            <p class="hero__lead" data-reveal style="--d:.16s" data-ar="{esc(b['lede_ar'])}">{esc(b['lede'])}</p>
            <div class="stats__inner glass" style="margin-top:20px;grid-template-columns:repeat(3,1fr)" data-reveal style="--d:.2s">{stats}</div>
            <div class="pill-list" style="margin-top:16px" data-reveal>{chips}</div>
            {buy}
          </div>
        </div>
      </section>

      {toc}

      <section class="section container section--tight" aria-labelledby="next-title">
        <div class="callout glass glass--deep" data-reveal>
          <div>
            <p class="kicker"><span data-ar="الكتاب التالي في المكتبة">NEXT IN THE LIBRARY</span></p>
            <h3 id="next-title"><span lang="ar" dir="rtl">{esc(nxt['title_ar'])}</span> <span class="grad-text">· {esc(nxt['title'])}</span></h3>
            <p data-ar="{esc(nxt['lede_ar'])}">{esc(nxt['lede'])}</p>
          </div>
          <div class="callout__actions">{btn('← The Library', '← المكتبة', '/books/', 'glass')}{btn(nxt['title'] + ' →', nxt['title_ar'] + ' ←', f'/books/{nxt["slug"]}/')}</div>
        </div>
      </section>

      {closing("CAN'T WAIT TO HEAR FROM YOU", 'نتطلع لسماعك',
               '<span data-ar="لا نطيق الانتظار">Can’t Wait To</span><br /><span class="grad-text" data-ar="لنسمع منك.">Hear From You.</span>',
               'Questions about this book, bulk licences, or a custom training edition? Talk to us.',
               'أسئلة عن هذا الكتاب أو تراخيص جماعية أو نسخة تدريبية مخصصة؟ كلمنا.',
               [btn('Book an Appointment', 'احجز موعدًا', '/contact/#book'), btn('Get Started', 'ابدأ الآن', '/contact/', 'glass'), btn('Full Services', 'كل الخدمات', '/services/', 'ghost', 'arrow')])}
'''
    return page(f'/books/{b["slug"]}/', title=f'{b["title"]} — {b["title_ar"]} · Code & Canvas', title_ar=f'{b["title_ar"]} — {b["title"]} · Code & Canvas',
                desc=b['lede'], desc_ar=b['lede_ar'], nav='books', body=body, og_type='book', scripts=('/assets/js/pages.js', '/assets/js/shop.js'))


def reader_page(b):
    parts = ''
    if b['slug'] == 'basics-of-visual-identity':
        preview = [dict(k=k, title=t, sub=s, p=p1, q=p2, chips=c) for j in VI_JOURNEYS for (k, t, s, p1, p2, c) in j['chapters']]
    else:
        preview = []
    import json
    sample = json.dumps(dict(slug=b['slug'], title=b['title_ar'], title_en=b['title'], author=b['author'], parts_total=int(b['stats'][0][0]) if b['stats'][0][0].isdigit() else None,
                             preview=preview), ensure_ascii=False).replace('</', '<\\/')
    body = f'''
      <section class="container" style="padding-top:calc(var(--nav-h) + 18px)">
        <div class="reader glass" data-reader="{b['slug']}" data-manifest="/assets/books/{b['slug']}/manifest.json" dir="rtl" lang="ar">
          <aside class="reader__side">
            <div class="reader__side-head"><b>{esc(b['title_ar'])}</b><a class="text-link" href="/books/{b['slug']}/">← الكتاب</a></div>
            <div class="reader__parts" data-parts></div>
          </aside>
          <div class="reader__main">
            <div class="reader__bar">
              <button class="btn btn--ghost btn--sm" type="button" data-prev aria-label="السابق">‹</button>
              <button class="btn btn--ghost btn--sm" type="button" data-next aria-label="التالي">›</button>
              <span class="counter" data-counter>— / —</span>
              <span class="spacer"></span>
              <button class="btn btn--ghost btn--sm" type="button" data-notes-toggle>📝 ملاحظاتي</button>
              <button class="btn btn--ghost btn--sm" type="button" data-fullscreen>⛶ ملء الشاشة</button>
            </div>
            <div class="reader__stage">
              <article class="slide glass" data-slide tabindex="0" aria-live="polite"></article>
              <div class="reader__gate" data-gate hidden>
                <div class="glass">
                  <span class="card__icon">🔒</span>
                  <h3>المعاينة المجانية انتهت</h3>
                  <p>اشترِ الكتاب لفتح كل الأجزاء ({b['stats'][0][0]} {b['stats'][0][1]}) في القارئ التفاعلي — وصول دائم من حسابك.</p>
                  {add_btn(b)}
                  <a class="btn btn--glass" href="/login/?next=/books/{b['slug']}/read/">لديك الكتاب؟ سجّل الدخول</a>
                </div>
              </div>
            </div>
            <div class="reader__thumbs" data-thumbs></div>
          </div>
          <aside class="reader__notes" hidden data-notes>
            <div class="reader__notes-head"><b>ملاحظاتي</b><button class="btn btn--ghost btn--sm" type="button" data-notes-toggle>✕</button></div>
            <textarea placeholder="اكتب ملاحظاتك هنا — تُحفظ على هذا الجهاز." data-notes-text></textarea>
            <div class="reader__notes-foot">تُحفظ محليًا في المتصفح (localStorage).</div>
          </aside>
        </div>
        <script type="application/json" data-reader-sample>{sample}</script>
      </section>
'''
    return page(f'/books/{b["slug"]}/read/', title=f'Reader — {b["title"]} · Code & Canvas', title_ar=f'القارئ — {b["title_ar"]} · Code & Canvas',
                desc=f'Interactive reader for {b["title"]} ({b["title_ar"]}) — free preview; the full book unlocks after purchase.',
                desc_ar=f'القارئ التفاعلي لكتاب {b["title_ar"]} — معاينة مجانية؛ يُفتح الكتاب كاملًا بعد الشراء.',
                nav='books', body=body, body_class='is-reader', scripts=('/assets/js/pages.js', '/assets/js/shop.js', '/assets/js/reader.js'))


def build():
    out = [hub()]
    for i, b in enumerate(BOOKS):
        out.append(book_page(b, i))
        if b['available']:
            out.append(reader_page(b))
    return out
