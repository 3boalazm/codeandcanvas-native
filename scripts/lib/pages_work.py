# -*- coding: utf-8 -*-
"""/case-studies/ — live copy of codeandcanvas.net/case-studies/ (title "Our Work —
Case Studies & Delivered Projects"). The three projects are Arabic-first on the
live page; we keep the Arabic as primary copy and add the English twin."""
from h import esc, icon, crumbs, closing, btn, page

PROJECTS = [
    dict(n='01', meta='Healthcare · SaaS · Multi-tenant · 2026', meta_ar='رعاية صحية · SaaS · متعدد المستأجرين · 2026',
         name_ar='صيدليتي —', name='Pharmacy OS', client_ar='صيدلية دكتور', client='Doctor Pharmacy',
         desc_ar='نظام تشغيل متكامل للصيدليات يجمع نقطة البيع والمخزون والروشتات والمالية والورديات في منصة واحدة. Multi-tenant SaaS بواجهة عربية RTL-first كاملة.',
         desc='An integrated operating system for pharmacies that brings POS, inventory, prescriptions, finance, and shifts into one platform. Multi-tenant SaaS with a fully RTL-first Arabic interface.',
         stack=['Next.js 14', 'NestJS', 'TypeScript', 'Prisma', 'Neon Postgres', 'Zustand', 'PWA', 'Tailwind'],
         feats=[('نقطة البيع (POS) + الفواتير', 'Point of sale (POS) + invoicing'), ('المخزون + استلام البضاعة (GRN)', 'Inventory + goods receipt (GRN)'), ('الروشتات + إدارة العملاء', 'Prescriptions + customer management'), ('التقارير + التحليلات + التنبيهات', 'Reports + analytics + alerts')],
         link=None, link_label='Live Demo coming soon ↗', link_label_ar='العرض الحي قريبًا ↗', emoji='💊', stat='14', stat_label='Modules shipped', stat_label_ar='وحدة مُسلَّمة', art='art--mint', slot='work/pharmacy-os'),
    dict(n='02', meta='PWA · Islamic · Offline-first · 2026', meta_ar='PWA · إسلامي · يعمل دون اتصال · 2026',
         name_ar='زاد —', name='Worship Companion', client_ar='مشروع شخصي / مفتوح', client='Personal / Open project',
         desc='Islamic worship PWA built for the ten days of Dhul-Hijjah — prayer times, Quran, adhkar, tasbih counter, Ramadan & Hajj tools. Fully offline-first, bilingual AR/EN.',
         desc_ar='تطبيق ويب تقدمي للعبادات بُني لعشر ذي الحجة — مواقيت الصلاة والقرآن والأذكار وعدّاد التسبيح وأدوات رمضان والحج. يعمل دون اتصال بالكامل، ثنائي اللغة عربي/إنجليزي.',
         stack=['PWA / Service Worker', 'GSAP', 'Vanilla JS', 'localStorage', 'canvas-confetti', 'Vercel', 'IBM Plex Sans Arabic'],
         feats=[('مواقيت الصلاة + القبلة', 'Prayer times + Qibla'), ('المصحف + الأذكار + الأربعون النووية', 'Quran Mushaf + Adhkar + 40 Nawawi'), ('عدّاد التسبيح + الرقية + أسماء الله الحسنى', 'Tasbih counter + Ruqyah + Asmaa Allah'), ('رمضان + الحج + قسم الأطفال', 'Ramadan + Hajj + Kids section')],
         link='https://zadullashr.vercel.app/', link_label='View Live ↗', link_label_ar='شاهد مباشرة ↗', emoji='🕌', stat='12', stat_label='Worship modules', stat_label_ar='وحدة عبادات', art='art--violet', slot='work/zad'),
    dict(n='03', meta='Healthcare · ERP · Pharma · 2026', meta_ar='رعاية صحية · ERP · أدوية · 2026',
         name_ar='نايل فارما —', name='ERP Platform', client_ar='النيل للأدوية والأغذية والمكملات', client='Nile Pharma, Food & Supplements',
         desc_ar='منصة ERP صيدلانية تغطي دورة البيع الكاملة — من تخصيص المخزون بنظام FEFO ومخزون الأمانة حتى الفوترة والتحصيل وحساب حوافز المناديب.',
         desc='A pharmaceutical ERP platform covering the full sales cycle — from FEFO stock allocation and consignment inventory to invoicing, collections, and sales-rep incentive calculation.',
         stack=['React 18', 'RTL', 'Babel Standalone', 'IBM Plex Sans Arabic', 'FEFO Logic', 'CDN Deploy'],
         feats=[('كتالوج المنتجات + المخزون + أمانة', 'Product catalogue + inventory + consignment'), ('أوامر البيع بنظام FEFO', 'FEFO sales orders'), ('الفواتير + التحصيل', 'Invoicing + collections'), ('حوافز المناديب + الترتيب', 'Rep incentives + ranking')],
         link=None, link_label='Internal system — NDA', link_label_ar='نظام داخلي — اتفاقية سرية', emoji='📊', stat='10', stat_label='ERP modules', stat_label_ar='وحدة ERP', art='art--gold', slot='work/nile-pharma-erp'),
]


def project(p, i):
    stack = ''.join(f'<span class="pill">{esc(s)}</span>' for s in p['stack'])
    feats = ''.join(f'<li data-ar="{esc(ar)}">{esc(en)}</li>' for ar, en in p['feats'])
    if p['link']:
        link = f'<a class="btn btn--glass" href="{p["link"]}" target="_blank" rel="noopener"><span data-ar="{esc(p["link_label_ar"])}">{esc(p["link_label"])}</span><i class="flip" data-icon="arrowUpRight"></i></a>'
    else:
        link = f'<span class="badge badge--violet" data-ar="{esc(p["link_label_ar"])}">{esc(p["link_label"])}</span>'
    flip = i % 2 == 1
    text = f'''
          <div>
            <p class="kicker"><span class="kicker__num">{p['n']}</span><span data-ar="{esc(p['meta_ar'])}">{esc(p['meta'])}</span></p>
            <h2 class="section__title cs__title" id="cs-{p['n']}-title"><span class="cs__ar" lang="ar" dir="rtl">{esc(p['name_ar'])}</span><br /><span class="grad-text">{esc(p['name'])}</span></h2>
            <p class="person__tag" data-ar="{esc(p['client_ar'])}">{esc(p['client'])}</p>
            <p data-ar="{esc(p['desc_ar'])}">{esc(p['desc'])}</p>
            <div class="pill-list" style="margin-top:16px">{stack}</div>
            <ul class="ticks ticks--dense" style="margin-top:18px">{feats}</ul>
            <div class="hero__ctas" style="margin-top:22px">{link}</div>
          </div>'''
    visual = p['slot'].split('/')[-1]
    art = f'''
          <figure class="case-visual">
            <img src="/assets/brand/work/{visual}.svg" width="960" height="600" loading="lazy" alt="{esc(p['name'])} — conceptual scope diagram" data-ar-alt="{esc(p['name_ar'])} مخطط توضيحي للنطاق" />
            <figcaption data-ar="رسم توضيحي مبني على النطاق الموثق في الموقع، وليس لقطة من واجهة المنتج أو إثباتًا لنتيجة تجارية.">Conceptual illustration of the documented scope, not a product screenshot or evidence of a business outcome.</figcaption>
          </figure>'''
    text += f'''<div class="case-evidence"><b data-ar="حالة العرض">Access &amp; evidence</b><p data-ar="{esc(p['link_label_ar'])}">{esc(p['link_label'])}</p><p data-ar="يمكن مناقشة النطاق والدور وحدود المشاركة في مكالمة. لا ننشر مواد عميل محمية باتفاقية سرية.">Discuss scope, role and sharing restrictions with us. Client material protected by an NDA is not published here.</p>{btn('Discuss a similar challenge', 'ناقش تحديًا مشابهًا', '/contact/?inquiry=custom', 'glass')}</div>'''
    return f'''
      <section class="section container section--flush-top cs" id="project-{p['n']}" aria-labelledby="cs-{p['n']}-title">
        <div class="grid grid--2 grid--center" data-reveal>{(art + text) if flip else (text + art)}
        </div>
      </section>'''


def build():
    body = f'''
      <!-- ░░ Hero ░░ -->
      <section class="phero container phero--center" aria-labelledby="page-title">
        {crumbs([('Home', 'الرئيسية', '/'), ('Work', 'أعمالنا', None)])}
        <span class="eyebrow" data-reveal><span class="eyebrow__dot" aria-hidden="true"></span><span data-ar="أعمال مختارة · النطاق والأنظمة والتنفيذ">Selected work · Scope, systems & delivery</span></span>
        <h1 class="phero__title" id="page-title" data-reveal style="--d:.08s"><span data-ar="مبنية لتُنجز.">Built to deliver.</span><br /><em class="grad-text" data-ar="لا لتبهر فحسب.">Not just to impress.</em></h1>
        <p class="hero__lead" data-reveal style="--d:.16s" data-ar="كل مشروع هنا بدأ بمشكلة عمل — وانتهى بنظام يعمل أو منتج حي أو علامة في السوق.">Every project here started with a business problem — and ended with a working system, a live product, or a brand in the market.</p>
        <nav class="subnav" aria-label="Projects" data-ar-label="المشاريع" data-reveal style="--d:.22s">{''.join(f'<a href="#project-{p["n"]}">{p["n"]} · {esc(p["name"])}</a>' for p in PROJECTS)}</nav>
      </section>

      {''.join(project(p, i) for i, p in enumerate(PROJECTS))}

      <!-- ░░ Portfolios ░░ -->
      <section class="section container section--tight" aria-labelledby="pf-title">
        <div class="callout glass glass--deep" data-reveal>
          <div>
            <p class="kicker"><span data-ar="المزيد من الأعمال">MORE WORK</span></p>
            <h3 id="pf-title"><span data-ar="أعمال المؤسسين">Founder portfolios</span> <span class="grad-text" data-ar="— العلامات والعمارة.">— brands and architecture.</span></h3>
            <p data-ar="أكثر من 20 علامة صاغها مصطفى وبرامج تحول صممها أحمد — معروضة في محفظتيهما الشخصيتين.">20+ brands shaped by Mustafa and transformation programmes architected by Ahmed — showcased in their personal portfolios.</p>
          </div>
          <div class="callout__actions">
            <a class="btn btn--glass" href="https://aboalazm-os.vercel.app/" target="_blank" rel="noopener"><span data-ar="أعمال مصطفى ↗">Mustafa · Portfolio ↗</span></a>
            <a class="btn btn--glass" href="https://ahmed-bedeer.vercel.app/" target="_blank" rel="noopener"><span data-ar="أعمال أحمد ↗">Ahmed · Portfolio ↗</span></a>
            <a class="text-link" href="https://behance.net/aboalazm" target="_blank" rel="noopener">{icon('pen')}<span>Behance ↗</span></a>
          </div>
        </div>
      </section>

      {closing("CAN'T WAIT TO HEAR FROM YOU", 'نتطلع لسماعك',
               '<span data-ar="لا نطيق الانتظار">Can’t Wait To</span><br /><span class="grad-text" data-ar="لنسمع منك.">Hear From You.</span>',
               'Have a system to build, a product to launch, or a brand to shape? Start with a 30-minute call.',
               'لديك نظام تبنيه أو منتج تطلقه أو علامة تصوغها؟ ابدأ بمكالمة مدتها 30 دقيقة.',
               [btn('Book an Appointment', 'احجز موعدًا', '/contact/#book'), btn('Get Started', 'ابدأ الآن', '/contact/', 'glass'), btn('Full Services', 'كل الخدمات', '/services/', 'ghost', 'arrow')])}
'''
    return [page('/case-studies/', title='Our Work — Case Studies & Delivered Projects · Code & Canvas', title_ar='أعمالنا — دراسات حالة ومشاريع مُسلَّمة · Code & Canvas',
                 desc='Real projects, proven results: Pharmacy OS (multi-tenant healthcare SaaS), Zad worship companion PWA, and the Nile Pharma ERP platform — built by Code & Canvas, 2024–2026.',
                 desc_ar='مشاريع حقيقية ونتائج مثبتة: نظام تشغيل الصيدليات (SaaS صحي متعدد المستأجرين)، تطبيق زاد للعبادات، ومنصة ERP لنايل فارما — من بناء Code & Canvas، 2024–2026.',
                 nav='work', body=body)]
