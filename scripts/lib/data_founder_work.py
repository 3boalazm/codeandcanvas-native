# -*- coding: utf-8 -*-
"""Founder work archive — the 25 entries published on Mustafa Aboalazm's own
portfolio (/work, /work/design, /work/development), re-indexed for our /work/.

Sources (read 2026-11-08):
  https://aboalazm-os.vercel.app/work
  https://aboalazm-os.vercel.app/work/design        (8 identity projects)
  https://aboalazm-os.vercel.app/work/development   (17 digital products)
  https://github.com/3boalazm?tab=repositories     (public source repos)

Honesty contract — read before editing:
  * These are the co-founder's own published projects. Code & Canvas links to
    them as documentation; it does NOT present them as verified studio client
    engagements, does NOT claim measured outcomes, and does NOT republish his
    imagery without permission. Every card points back to his case study, the
    live deployment or the public repository so a reader can check it.
  * Descriptions are adapted (not always verbatim) to our bilingual, evidence-
    limited voice. Stale counts from his case studies (e.g. an older page
    total) were removed rather than asserted against this site's real build.
  * Adding a new client case is a different process: docs/PUBLISH-GATE.md and
    the permission/evidence/attribution gate on the /work/ page itself.
  * Titles that are proper nouns stay in Latin in both languages; tech stack
    names stay in Latin (normal practice in Arabic technical UI).
"""

PREFIX = 'https://aboalazm-os.vercel.app/case-studies/'
GH = 'https://github.com/3boalazm/'


def W(**kw):
    kw.setdefault('case', None)
    kw.setdefault('live', None)
    kw.setdefault('repo', None)
    kw.setdefault('own', None)
    kw.setdefault('status', None)
    kw.setdefault('status_ar', None)
    return kw


IDENTITY = [
    W(track='identity', no='01',
      title='GAD Heart & Lungs Institute', title_ar='معهد GAD للقلب والرئتين', year='2023',
      desc='A specialized cardiac and pulmonary institute needed an authoritative yet warm bilingual identity to govern architectural signage and patient care.',
      desc_ar='احتاج معهد متخصص في أمراض القلب والرئة إلى هوية ثنائية اللغة تجمع بين الهيبة والدفء، لتحكم لافتات المبنى وتجربة رعاية المرضى.',
      tags=['Brand Strategy', 'Bilingual Identity', 'Guidelines'], tags_ar=['استراتيجية العلامة', 'هوية ثنائية اللغة', 'دليل الهوية'],
      case=PREFIX + 'gad-institute'),
    W(track='identity', no='02',
      title='Ahmed Bedeer', title_ar='أحمد بدير', year='2025',
      desc='A healthcare IT leader needed a personal brand with executive gravitas, geometric monogram precision, and zero corporate stiffness.',
      desc_ar='احتاج قائد في تقنية المعلومات الصحية إلى علامة شخصية بحضور تنفيذي ودقة هندسية في المونوجرام، من دون جمود مؤسسي.',
      tags=['Personal Brand', 'Brand Guidelines', 'Monogram'], tags_ar=['علامة شخصية', 'دليل الهوية', 'مونوجرام'],
      case=PREFIX + 'ahmed-bedeer'),
    W(track='identity', no='03',
      title='Nile Pharma Food', title_ar='نايل فارما فود', year='2020–25',
      desc='A pharma-food brand operating without visual governance needed consumer packaging authority and cohesive bilingual shelf presence.',
      desc_ar='علامة أغذية صيدلانية كانت تعمل بلا حوكمة بصرية، واحتاجت حضورًا قويًا على الأرفف وتغليفًا استهلاكيًا متماسكًا ثنائي اللغة.',
      tags=['Brand System', 'WordPress', 'Rebrand'], tags_ar=['منظومة علامة', 'WordPress', 'إعادة بناء العلامة'],
      case=PREFIX + 'nile-pharma'),
    W(track='identity', no='04',
      title='Code & Canvas', title_ar='Code & Canvas', year='2024 →',
      desc='A two-track brand and engineering studio needed a unified visual system capable of governing strategy decks, guidelines, and digital products.',
      desc_ar='استوديو يجمع التصميم والهندسة احتاج نظامًا بصريًا موحَّدًا يحكم عروض الاستراتيجية وأدلة الهوية والمنتجات الرقمية.',
      tags=['Studio Identity', 'Brand System', 'Guidelines'], tags_ar=['هوية الاستوديو', 'منظومة علامة', 'دليل الهوية'],
      case=PREFIX + 'code-canvas', repo=GH + 'codeandcanvas-native', own='/'),
    W(track='identity', no='05',
      title='Reflection', title_ar='Reflection', year='2022',
      desc='An art and print studio needed a warm, airy editorial identity distinct from cheap poster shops and sterile art galleries.',
      desc_ar='استوديو للفن والطباعة احتاج هوية تحريرية دافئة وخفيفة، بعيدة عن متاجر البوسترات الرخيصة وبرود صالات العرض.',
      tags=['Identity', 'Art & Print', 'Guidelines'], tags_ar=['هوية', 'فن وطباعة', 'دليل الهوية'],
      case=PREFIX + 'reflection'),
    W(track='identity', no='06',
      title='Egypt SEG Field Camp', title_ar='معسكر Egypt SEG الحقلي', year='2020',
      desc='An annual geoscience field camp needed an energetic student-led identity that unifies apparel, field guides, badges, and event media.',
      desc_ar='معسكر جيولوجي سنوي احتاج هوية شبابية نشطة تقودها الطلاب وتوحّد الملابس وأدلة الحقل والشارات وإعلام الفعالية.',
      tags=['Identity', 'Print', 'Event'], tags_ar=['هوية', 'مطبوعات', 'فعالية'],
      case=PREFIX + 'esfc'),
    W(track='identity', no='07',
      title='Learn in Arabic', title_ar='تعلّم بالعربية', year='2020–21',
      desc='An educational initiative needed a bold typographic mark and content system that makes technical learning in Arabic feel modern and clear.',
      desc_ar='مبادرة تعليمية احتاجت علامة طباعية جريئة ونظام محتوى يجعل التعلّم التقني بالعربية يبدو حديثًا وواضحًا.',
      tags=['Identity', 'Studio Build', 'Motion'], tags_ar=['هوية', 'بناء الاستوديو', 'موشن'],
      case=PREFIX + 'learn-in-arabic'),
    W(track='identity', no='08',
      title='Youth Scope', title_ar='Youth Scope', year='2019–21',
      desc='A youth community program needed a modular visual identity built for fast volunteer publishing across workshops, stages, and social channels.',
      desc_ar='برنامج مجتمعي للشباب احتاج هوية بصرية معيارية تسمح بنشر سريع على يد المتطوعين عبر الورش والمنصّات وقنوات التواصل.',
      tags=['Identity', 'Campaigns', 'Team Lead'], tags_ar=['هوية', 'حملات', 'قيادة الفريق'],
      case=PREFIX + 'youth-scope'),
]

PRODUCT = [
    W(track='product', no='01',
      title='Code & Canvas — Platform', title_ar='Code & Canvas — المنصة', year='2026',
      desc='A zero-dependency static studio platform generating bilingual EN/AR pages for 23 fixed-scope services with transparent fee bands.',
      desc_ar='منصة استوديو ثابتة بلا تبعيات خارجية تُولّد صفحات ثنائية اللغة عربية/إنجليزية لـ23 خدمة محدّدة النطاق مع شرائح أسعار معلنة.',
      tags=['Bilingual EN/AR', 'Service Catalog', 'Two-Track Studio'], tags_ar=['ثنائي اللغة عربي/إنجليزي', 'كتالوج الخدمات', 'استوديو ثنائي المسار'],
      case=PREFIX + 'code-canvas-dev', live='https://codeandcanvas.net/', repo=GH + 'codeandcanvas-native', own='/'),
    W(track='product', no='02',
      title='Nile Pharma ERP', title_ar='نايل فارما ERP', year='2025–26',
      desc='An Arabic RTL operations and commercial ERP console uniting sales orders, collection KPIs, inventory alerts, and rep leaderboards.',
      desc_ar='لوحة تشغيل وتجارة عربية RTL توحّد أوامر البيع ومؤشرات التحصيل وتنبيهات المخزون ولوائح مندوبي المبيعات.',
      tags=['NestJS', 'Prisma', 'Postgres', 'Kafka'], tags_ar=['NestJS', 'Prisma', 'Postgres', 'Kafka'],
      case=PREFIX + 'nile-pharma-erp', own='/case-studies/'),
    W(track='product', no='03',
      title='Nile Pharma Food — Storefront', title_ar='نايل فارما فود — المتجر', year='2026',
      desc='A bilingual storefront pairing Payload CMS editorial storytelling with a headless Vendure product catalog, pricing, and orders.',
      desc_ar='متجر ثنائي اللغة يجمع السرد التحريري عبر Payload CMS مع كتالوج منتجات وأسعار وطلبات عبر Vendure.',
      tags=['Next.js', 'Payload CMS', 'Vendure', 'PostgreSQL'], tags_ar=['Next.js', 'Payload CMS', 'Vendure', 'PostgreSQL'],
      case=PREFIX + 'nile-pharma-storefront', live='https://nile-vercel-seven.vercel.app/ar', repo=GH + 'NILE-VERCEL'),
    W(track='product', no='04',
      title='OLTRÈ Collective', title_ar='OLTRÈ Collective', year='2026',
      desc='A bilingual urban streetwear storefront and admin dashboard pairing editorial lookbooks with cart, wishlist, loyalty, and order flows.',
      desc_ar='متجر أزياء شارعية ثنائي اللغة ولوحة إدارة تجمع عروضًا تحريرية مع السلة والمفضلة والولاء وتدفقات الطلبات.',
      tags=['React + Vite', 'Drizzle + Postgres', 'Payments', 'Loyalty & Roles'], tags_ar=['React + Vite', 'Drizzle + Postgres', 'المدفوعات', 'الولاء والصلاحيات'],
      case=PREFIX + 'momo-collective', live='https://momo-shop.vercel.app/', repo=GH + 'momo-shop'),
    W(track='product', no='05',
      title='Zad', title_ar='زاد', year='2025–26',
      desc='An ad-free, offline-first Islamic worship companion covering 64 screens across prayer times, Quran plans, adhkar, and a kids mode.',
      desc_ar='رفيق إسلامي بلا إعلانات يعمل دون اتصال، يغطي 64 شاشة لمواقيت الصلاة وخطط ختم القرآن والأذكار ووضعًا للأطفال.',
      tags=['PWA', 'Firebase', 'Service Worker', 'Push Notifications'], tags_ar=['PWA', 'Firebase', 'Service Worker', 'إشعارات فورية'],
      case=PREFIX + 'zad', live='https://zadullmuslim.vercel.app/', repo=GH + 'zad', own='/case-studies/'),
    W(track='product', no='06',
      title='Farm Console', title_ar='لوحة المزرعة', year='2025–26',
      desc='An offline-capable Arabic RTL livestock platform tracking herd records, breeding lineages, veterinary schedules, feed costs, and net profit.',
      desc_ar='منصة عربية RTL لإدارة الثروة الحيوانية تعمل دون اتصال، تتتبّع سجلات القطيع وسلالات التربية وجداول الطب البيطري وتكاليف العلف وصافي الربح.',
      tags=['PWA', 'Firebase', 'Realtime DB', 'Chart.js'], tags_ar=['PWA', 'Firebase', 'Realtime DB', 'Chart.js'],
      case=PREFIX + 'farm-console', live='https://farm-project-puce.vercel.app/', repo=GH + 'farm-project'),
    W(track='product', no='07',
      title='Speech to Text Studio', title_ar='استوديو تحويل الكلام إلى نص', year='2026',
      desc='A resilient transcription studio routing uploads and mic recordings across four STT engines with automatic server-side failover.',
      desc_ar='استوديو نسخ مرن يوجّه الملفات والتسجيلات المباشرة عبر أربعة محرّكات تحويل كلام مع تبديل تلقائي من جهة الخادم.',
      tags=['Next.js', 'TypeScript', '4 STT Engines', 'PWA'], tags_ar=['Next.js', 'TypeScript', '4 محرّكات نسخ', 'PWA'],
      case=PREFIX + 'speech-to-text-studio', live='https://mahtool.vercel.app/', repo=GH + 'MahmoudTC-tool'),
    W(track='product', no='08',
      title='Mini Exam', title_ar='الاختبار المصغّر', year='2026',
      desc='A bilingual teacher-to-student assessment studio generating validated AI questions, grading on the server, and formatting WhatsApp reports.',
      desc_ar='استوديو تقييم ثنائي اللغة من المعلّم إلى الطالب يولّد أسئلة مُتحقَّقة بالذكاء الاصطناعي، ويصحّح على الخادم، ويهيّئ تقارير واتساب.',
      tags=['Next.js', 'Firebase', 'Groq', 'WhatsApp'], tags_ar=['Next.js', 'Firebase', 'Groq', 'واتساب'],
      case=PREFIX + 'mini-exam', live='https://mraboqamarexams.vercel.app/', repo=GH + 'Exam'),
    W(track='product', no='09',
      title='Ahmed Kamar', title_ar='أحمد قمر', year='2026',
      desc='A bilingual executive portfolio framing restaurant and delivery-platform analytics case studies with SQL-first clarity and clean hierarchy.',
      desc_ar='بورتفوليو تنفيذي ثنائي اللغة يعرض دراسات تحليلية للمطاعم ومنصّات التوصيل بوضوح يبدأ من SQL وتراتبية نظيفة.',
      tags=['Next.js 15', 'React 19', 'TypeScript', 'Tailwind CSS v4'], tags_ar=['Next.js 15', 'React 19', 'TypeScript', 'Tailwind CSS v4'],
      case=PREFIX + 'ahmed-kamar', live='https://ahmed-kamar-portfolio.vercel.app/', repo=GH + 'Ahmed-Kamar-Portfolio'),
    W(track='product', no='10',
      title='Continuum', title_ar='Continuum', year='2026',
      desc='A local-first personal memory operating system across 21 views to reconstruct session context, track decisions, and sync cleanly with Firebase.',
      desc_ar='نظام ذاكرة شخصية يعمل محليًا أولًا عبر 21 عرضًا، لإعادة بناء سياق الجلسات وتتبّع القرارات والمزامنة النظيفة مع Firebase.',
      tags=['HTML · CSS · JavaScript', 'LocalStorage', 'Optional Firebase Sync'], tags_ar=['HTML · CSS · JavaScript', 'LocalStorage', 'مزامنة Firebase اختيارية'],
      case=PREFIX + 'continuum', live='https://continuum-khaki.vercel.app/', repo=GH + 'Continuum'),
    W(track='product', no='11',
      title='Pharmacy Web', title_ar='واجهة الصيدلية', year='2026',
      desc='A token-driven Arabic RTL pharmacy frontend structured around 15 bounded-context modules, strict import boundaries, and precision money handling.',
      desc_ar='واجهة صيدلية عربية RTL قائمة على الرموز، منظّمة حول 15 وحدة سياقية محدودة، بحدود استيراد صارمة ومعالجة دقيقة للمبالغ.',
      tags=['Next.js', 'TypeScript', 'Tailwind CSS', 'Frontend only'], tags_ar=['Next.js', 'TypeScript', 'Tailwind CSS', 'واجهة فقط'],
      case=PREFIX + 'pharmacy-web', live='https://pharmacy-web-eight.vercel.app/', repo=GH + 'pharmacy-web'),
    W(track='product', no='12',
      title='Youssef Guba', title_ar='يوسف جوبا', year='2026',
      desc='A bilingual personal operating system for a mobile product engineer uniting case studies, courses, technical writing, and Sanity CMS publishing.',
      desc_ar='نظام تشغيل شخصي ثنائي اللغة لمهندس منتجات محمول يوحّد دراسات الحالة والدورات والكتابة التقنية والنشر عبر Sanity CMS.',
      tags=['Next.js', 'React', 'TypeScript', 'Sanity CMS'], tags_ar=['Next.js', 'React', 'TypeScript', 'Sanity CMS'],
      case=PREFIX + 'youssef-guba', live='https://youssefguba-os.vercel.app/', repo=GH + 'Youssefguba-os'),
    W(track='product', no='13',
      title='Ummah Academy', title_ar='أكاديمية الأمّة', year='2026',
      desc='A multilingual Astro learning platform spanning 5 languages, native RTL typography, 23 routes, and offline-ready PWA delivery.',
      desc_ar='منصة تعلّم متعددة اللغات بـ Astro تمتد إلى 5 لغات وطباعة RTL أصلية و23 مسارًا وتسليم PWA جاهز للعمل دون اتصال.',
      tags=['Astro', '5 languages · RTL', 'PWA · Offline'], tags_ar=['Astro', '5 لغات · RTL', 'PWA · دون اتصال'],
      case=PREFIX + 'ummah-academy', live='https://ummah-academy.vercel.app/', repo=GH + 'Ummah-academy',
      status='In progress', status_ar='قيد التنفيذ'),
    W(track='product', no='14',
      title='StemForge', title_ar='StemForge', year='2026',
      desc='A zero-upload browser audio workspace using ONNX Runtime Web and Web Workers to isolate vocals, drums, and bass locally.',
      desc_ar='مساحة صوت داخل المتصفح بلا رفع ملفات، تستخدم ONNX Runtime Web وWeb Workers لعزل الغناء والطبول والباص محليًا.',
      tags=['Next.js', 'ONNX Runtime', 'Web Workers', 'Audio AI'], tags_ar=['Next.js', 'ONNX Runtime', 'Web Workers', 'ذكاء صوتي'],
      case=PREFIX + 'stemforge', live='https://mdp-opal.vercel.app/', repo=GH + 'MDP'),
    W(track='product', no='15',
      title='Nile Bed', title_ar='Nile Bed', year='2026',
      desc='A bilingual B2B industrial catalogue for a mattress-spring manufacturer organizing 69 items across 8 product groups with WhatsApp enquiry flows.',
      desc_ar='كتالوج B2B صناعي ثنائي اللغة لمصنّع سوست مراتب وتوريد، يضم 69 صنفًا في 8 مجموعات مع تدفقات استفسار مباشرة عبر واتساب.',
      tags=['Next.js', 'TypeScript', 'Bilingual AR/EN · RTL', '69-Item B2B Catalog'], tags_ar=['Next.js', 'TypeScript', 'عربي/إنجليزي · RTL', 'كتالوج B2B بـ69 صنفًا'],
      live='https://nile-bed.vercel.app/', repo=GH + 'Nile-Bed', status='Live product', status_ar='منتج مباشر'),
    W(track='product', no='16',
      title='Craft Egypt', title_ar='حِرَف مصر', year='2026',
      desc='An Arabic RTL storefront and regional craft atlas showcasing Egyptian handmade copperware, textiles, pottery, and decor with a made-to-order flow.',
      desc_ar='متجر عربي RTL وأطلس للحِرَف الإقليمية يعرض المشغولات المصرية اليدوية من نحاسيات ومنسوجات وخزف وديكور مع تدفق طلبات حسب الطلب.',
      tags=['Arabic RTL Storefront', 'Heritage Catalogue', 'Regional Atlas', 'Made-to-Order'], tags_ar=['متجر عربي RTL', 'كتالوج تراث', 'أطلس إقليمي', 'طلب حسب الطلب'],
      live='https://craft-egypt.vercel.app/', status='Live product', status_ar='منتج مباشر'),
    W(track='product', no='17',
      title='Clinic Appointment System', title_ar='نظام حجوزات العيادة', year='2026',
      desc='An Arabic RTL patient booking interface, installable PWA layer, and operational setup on top of the open-source Easy!Appointments (GPL-3.0) platform.',
      desc_ar='واجهة حجز مرضى عربية RTL وطبقة PWA قابلة للتثبيت وإعداد تشغيلي فوق منصة Easy!Appointments مفتوحة المصدر (GPL-3.0).',
      tags=['Easy!Appointments (GPL-3.0)', 'Arabic RTL Layer', 'PWA Setup', 'REST API'], tags_ar=['Easy!Appointments (GPL-3.0)', 'طبقة عربية RTL', 'إعداد PWA', 'REST API'],
      live='https://aboalazm-os.vercel.app/contact?service=digital-product&source=/work/development',
      status='Demo', status_ar='عرض تجريبي'),
]

FOUNDER_WORK = IDENTITY + PRODUCT
