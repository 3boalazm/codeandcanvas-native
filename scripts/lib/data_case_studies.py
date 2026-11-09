# -*- coding: utf-8 -*-
"""Detailed, bilingual case studies for the founder's live projects (2026-11).

Sources are the live deployments and public repositories supplied by the owner
on 2026-11-08, plus the founder's own case-study index. Every entry states what
is publicly verifiable and what is not. Read the honesty contract below before
adding a project.

Honesty contract
  * These are the co-founder's own projects, documented from public sources.
    They are NOT presented as verified Code & Canvas client engagements, are NOT
    paired with measured business outcomes, and are NOT captioned as our
    deliverables.
  * No testimonial, metric, screenshot, client name or result was invented.
    Where a repository is not publicly reachable, the page says so and limits
    itself to what the live deployment shows.
  * All artwork used on these pages is AI-generated illustrative studio art,
    labelled on the page, never a product screenshot or a photo of real work.
  * Anything stronger requires the permission → evidence → attribution gate on
    /work/ and docs/ASSET-AND-CLAIM-REGISTER.md.
"""

ROLE = (
    'Designed and built by Mustafa Aboalazm. This page documents the publicly visible product and its source; it does not claim a studio engagement, a team, or a commercial result.',
    'صمّمه وبناه مصطفى أبو العزم. توضّح هذه الصفحة المنتج الظاهر للعامة ومصدره، ولا تدّعي تعاقدًا مع الاستوديو أو فريقًا أو نتيجة تجارية.',
)
EVIDENCE = (
    'This page documents what is publicly visible in the live deployment and, where available, the public repository. It is not a client testimonial, a measured outcome or a verified studio engagement. Approved screenshots, client permission and sourced outcomes are required before any stronger claim.',
    'توثّق هذه الصفحة ما يظهر علنًا في الموقع المباشر، ومستودع الكود العام حيثما توفر. ليست شهادة عميل، ولا نتيجة مُقاسة، ولا تعاقدًا مُثبتًا مع الاستوديو. أي ادعاء أقوى يحتاج لقطات معتمدة وإذن العميل ونتائج موثّقة بالمصادر.',
)
ROLE_PENDING = (
    'Repository supplied by the owner; source access is not publicly available. No technical scope, stack or outcome is claimed on this page.',
    'مستودع قدّمه المالك، والوصول إلى مصدره غير متاح للعامة. لا تُقدَّم في هذه الصفحة أي ادعاءات عن النطاق التقني أو الحزمة التقنية أو النتائج.',
)

# Shared bilingual labels for the case-study template (see pages_case_studies.py).
LABELS = {
    'case_eyebrow': ('CASE STUDY · DOCUMENTED WORK', 'دراسة حالة · عمل موثّق'),
    'illustrative': ('ILLUSTRATIVE STUDIO ARTWORK · NOT A PRODUCT SCREENSHOT OR CLIENT PHOTO', 'عمل توضيحي للاستوديو · ليس لقطة منتج ولا صورة عمل عميل'),
    'figure_note': ('Illustrative artwork created for this site. It represents the shape of the work, not a screenshot, a real interface or proof of an outcome.', 'عمل فني توضيحي أُنشئ لهذا الموقع. يعبّر عن شكل العمل، لا عن لقطة شاشة أو واجهة حقيقية أو إثبات نتيجة.'),
    'sec1': ('01', 'WHAT THE WORK HAD TO SOLVE', 'ما الذي كان على العمل حلّه'),
    'sec1_title': ('<span data-ar="المشكلة أولًا.">The problem, first.</span> <span class="grad-text" data-ar="ثم القرار.">Then the decision.</span>'),
    'sec1_lead': ('Why the project exists, the approach taken, and the part the founder actually played.', 'لماذا وُجد المشروع، والمنهج الذي اتُّبع، والدور الفعلي للمؤسس فيه.'),
    'sec2': ('02', 'WHAT WAS BUILT', 'ما الذي بُني'),
    'sec2_title': ('<span data-ar="مخرجات ملموسة.">Concrete deliverables.</span> <span class="grad-text" data-ar="لا صفات.">Not adjectives.</span>'),
    'sec2_lead': ('Each line is something a reader can open, check or keep.', 'كل سطر شيء يستطيع القارئ فتحه أو التحقق منه أو الاحتفاظ به.'),
    'sec3': ('03', 'HOW TO VERIFY IT', 'كيف تتحقق منه'),
    'sec3_title': ('<span data-ar="المصدر قدّامك.">The source is in front of you.</span>'),
    'sec3_lead': ('Live deployment, public repository and the limits of what each one proves.', 'الموقع المباشر، ومستودع الكود العام، وحدود ما يُثبته كلٌّ منهما.'),
    'sec4': ('04', 'EVIDENCE & LIMITS', 'الإثبات والحدود'),
    'sec4_title': ('<span data-ar="ما نقوله، وما لا نقوله.">What we say, and what we do not.</span>'),
    'sec4_lead': ('An attractive image is not evidence. Every claim here keeps its own boundary.', 'الصورة الجميلة ليست إثباتًا. لكل ادعاء هنا حدّه المعلن.'),
    'p_problem': ('PROBLEM', 'المشكلة'),
    'p_approach': ('APPROACH', 'المنهج'),
    'p_role': ('ROLE', 'الدور'),
    'p_build': ('BUILD', 'ما بُني'),
    'p_keeps': ('WHAT YOU CAN CHECK', 'ما يمكنك التحقق منه'),
    'p_stack': ('STACK & DISCIPLINE', 'الحزمة والتخصص'),
    'p_live': ('Open the live deployment ↗', 'افتح الموقع المباشر ↗'),
    'p_repo': ('Open the repository / source link ↗', 'افتح رابط المستودع أو المصدر ↗'),
    'p_live_none': ('No live deployment was supplied for this entry.', 'لم يُقدَّم موقع مباشر لهذا المدخل.'),
    'p_repo_none': ('No public repository could be verified for this entry.', 'لم يمكن التحقق من مستودع عام لهذا المدخل.'),
    'p_index': ('Back to the work index →', 'العودة إلى فهرس الأعمال →'),
    'p_claims': ('Read the claims & evidence register →', 'اقرأ سجل الادعاءات والأدلة →'),
    'p_source': ('SOURCE NOTE', 'ملاحظة المصدر'),
    'p_status': ('STATUS', 'الحالة'),
}


def C(**kw):
    kw.setdefault('repo', None)
    kw.setdefault('live', None)
    status_en, status_ar = kw.pop('status', ('Live deployment', 'موقع مباشر'))
    kw['status'], kw['status_ar'] = status_en, status_ar
    kw.setdefault('source_note', None)
    kw.setdefault('role', ROLE)
    kw.setdefault('evidence', EVIDENCE)
    kw.setdefault('track', 'product')
    return kw


CASE_STUDIES = [
    C(
        slug='maqloop', title='MAQLOOB', title_ar='مقلوب', year='2026', track='product',
        kicker='INDEPENDENT APPAREL · ARABIC FIRST', kicker_ar='أزياء مستقلة · عربية أولًا',
        lede='Numbered apparel releases with honest specs, labelled concept visuals and tools that let a visitor play with the graphic before deciding.',
        lede_ar='إصدارات ملابس مرقّمة بمواصفات صريحة، وتصوّرات بصرية مُعلَّنة، وأدوات تتيح للزائر اللعب بالجرافيك قبل القرار.',
        media='case-maqloop',
        alt='Abstract layered fabric panels and numbered-edition marks in violet, teal and pink — illustrative, not product photography',
        alt_ar='طبقات قماش مجردة ورموز إصدارات مرقّمة بالبنفسجي والتركوازي والوردي — توضيحي، وليس تصوير منتج',
        live='https://maqloop.vercel.app/',
        problem='An independent label needs to explain fabric weight, cut and limited-run availability without passing concept art off as real product photography.',
        problem_ar='علامة مستقلة تحتاج أن تشرح وزن الخامة والقَصّة وكمية الإصدار المحدود من دون أن تقدّم التصوّرات الفنية كصور حقيقية للمنتج.',
        approach='Arabic-first editorial commerce: every piece has its own spec page, every visual is labelled a concept study, and the playful parts run entirely in the browser.',
        approach_ar='تجارة تحريرية عربية أولًا: لكل قطعة صفحة مواصفات، وكل تصوّر مُعلَّن كدراسة مفاهيمية، والأجزاء التفاعلية تعمل بالكامل داخل المتصفح.',
        build=[
            ('Numbered drops with stated quantities and a release story.', 'إصدارات مرقّمة بكميات معلنة وقصة لكل إصدار.'),
            ('Per-piece detail pages: GSM, cut, fabric and flat-garment measurements.', 'صفحات تفاصيل لكل قطعة: الوزن والقَصّة والخامة وقياسات القطعة مفرودة.'),
            ('A remix wall with draggable, keyboard-movable stickers and a locally downloaded poster.', 'جدار إعادة تشكيل بملصقات قابلة للسحب والتحريك بلوحة المفاتيح، وتنزيل بوستر محليًا.'),
            ('A fit comparison measured against a garment the visitor already owns.', 'مقارنة مقاسات مقابل قطعة يملكها الزائر بالفعل، بدل تخمين مقاسات الجسم.'),
        ],
        keeps=[
            ('Bilingual product copy and an explicit "concept, not actual product" label on every illustration.', 'نصوص منتجات ثنائية اللغة وتسمية صريحة «تصوّر، ليس المنتج الفعلي» على كل رسم.'),
            ('Client-side remix and fit flows that store or send nothing to a server.', 'تدفقات إعادة التشكيل والمقاسات تعمل على الجهاز ولا تحفظ ولا ترسل شيئًا لخادم.'),
            ('A public release index with the quantities shown.', 'فهرس إصدارات عام بالكميات المعلنة.'),
        ],
        stack=[('Arabic-first RTL', 'عربية أولًا · RTL'), ('Client-side canvas', 'رسم داخل المتصفح'), ('No backend', 'بلا خادم'), ('Labelled concept art', 'فن توضيحي مُعلَّن')],
    ),
    C(
        slug='packbox-studio', title='PackBox Studio', title_ar='PackBox Studio', year='2026', track='product',
        kicker='LOCAL PACKAGING TOOL · MIT', kicker_ar='أداة تغليف محلية · MIT',
        lede='A local packaging design app: parametric dielines, artwork placement and a 3D folding preview, with no cloud account and no upload of your artwork.',
        lede_ar='تطبيق تغليف يعمل محليًا: قوالب قصّ بارامترية، ووضع التصميم، ومعاينة طيّ ثلاثية الأبعاد، بلا حساب سحابي ولا رفع لأعمالك.',
        media='case-packbox',
        alt='Abstract exploded cardboard box geometry with glowing cut and fold lines on a dark navy field — illustrative, not software UI',
        alt_ar='هندسة كرتون مبسّطة مفكّكة بخطوط قصّ وطيّ متوهجة على خلفية كحلية داكنة — توضيحي، وليس واجهة برنامج',
        live='https://azm-box.vercel.app/', repo='https://github.com/3boalazm/AZM-Box',
        problem='Packaging designers need accurate dielines and a fold preview without sending client artwork to a hosted service.',
        problem_ar='يحتاج مصمّمو التغليف إلى قوالب قصّ دقيقة ومعاينة للطيّ من دون إرسال أعمال العملاء إلى خدمة مستضافة.',
        approach='Parametric geometry generates SVG cut, fold, seam and dimension layers in the browser; a 3D preview shows the box folding; the manual is rendered from the same geometry code.',
        approach_ar='تُولّد هندسة بارامترية طبقات SVG للقصّ والطيّ واللحامات والأبعاد داخل المتصفح، مع معاينة ثلاثية الأبعاد للطيّ، ودليل مستخدم مُولَّد من كود الهندسة نفسه.',
        build=[
            ('Ten parametric box styles, including Straight Tuck End and RSC shipping cartons.', 'عشرة أنماط صناديق بارامترية، منها علبة الطيّ المستقيم وكرتون الشحن RSC.'),
            ('Separate SVG layers for cut lines, fold lines, seam marks and dimension labels.', 'طبقات SVG منفصلة لخطوط القصّ والطيّ وعلامات اللحام وبيانات الأبعاد.'),
            ('Artwork placement plus a 3D folding preview, entirely local.', 'وضع التصميم ومعاينة طيّ ثلاثية الأبعاد، بالكامل على الجهاز.'),
            ('A full user manual (PDF, DOCX, Markdown) with a worked Card Deck Box example and print/cut/assembly guidance.', 'دليل مستخدم كامل (PDF وDOCX وMarkdown) مع مثال عملي لصندوق بطاقات وإرشادات الطباعة والقصّ والتجميع.'),
        ],
        keeps=[
            ('MIT-licensed source and a manual whose figures come from the repository geometry code.', 'مصدر بترخيص MIT ودليل رسومه مولّدة من كود الهندسة في المستودع.'),
            ('Editable dieline templates with dimensions in millimetres.', 'قوالب قصّ قابلة للتعديل بأبعاد بالمليمتر.'),
            ('A documented no-upload, no-account workflow.', 'مسار عمل موثّق بلا رفع ملفات ولا حساب.'),
        ],
        stack=[('TypeScript', 'TypeScript'), ('Parametric SVG geometry', 'هندسة SVG بارامترية'), ('3D fold preview', 'معاينة طيّ 3D'), ('MIT license', 'ترخيص MIT')],
    ),
    C(
        slug='ummah-academy', title='Ummah Academy', title_ar='أكاديمية الأمّة', year='2026', track='product',
        kicker='LIVE 1-ON-1 LEARNING · MULTILINGUAL', kicker_ar='تعلّم مباشر فردي · متعدد اللغات',
        lede='A goal-first learning site for one-to-one Qur’an, Tajweed, Arabic and Islamic studies: four paths, a placement test, teacher vetting and transparent plans.',
        lede_ar='موقع تعلّم يبدأ بالهدف لدروس فردية في القرآن والتجويد والعربية والدراسات الإسلامية: أربعة مسارات، اختبار تحديد مستوى، وتحقق من المدرّسين، وخطط معلنة.',
        media='case-ummah',
        alt='Abstract open book pages with glowing knowledge paths and a soft teal-violet gradient — illustrative, not a screenshot',
        alt_ar='صفحات كتاب مفتوحة مجردة بمسارات معرفة متوهجة وتدرّج تركوازي بنفسجي — توضيحي، وليس لقطة شاشة',
        live='https://ummahacademy.net/', repo='https://github.com/3boalazm/Ummah-academy',
        status=('Live deployment', 'موقع مباشر'),
        problem='A live teaching service has to explain several learning paths, how teachers are vetted, and what a plan costs — without promising any particular outcome.',
        problem_ar='على خدمة تعليم مباشر أن تشرح مسارات تعلّم متعددة، وكيف يُتحقَّق من المدرّسين، وتكلفة كل خطة، من دون الوعد بنتيجة بعينها.',
        approach='Navigation starts with who is learning and what they want, then moves to courses, a placement test, a documented teacher-vetting process and plan tables.',
        approach_ar='يبدأ التنقّل بمن يتعلّم وماذا يريد، ثم ينتقل إلى المسارات واختبار المستوى وشرح موثّق لآلية التحقق من المدرّسين وجداول الخطط.',
        build=[
            ('Four course paths: Qur’an & Tajweed, Arabic Language, Ummah Cubs and Islamic Studies.', 'أربعة مسارات: القرآن والتجويد، اللغة العربية، أشبال الأمّة، والدراسات الإسلامية.'),
            ('A placement test, site search and a "who is learning" chooser.', 'اختبار تحديد مستوى، وبحث داخل الموقع، واختيار «من المتعلّم».'),
            ('A documented four-stage teacher check and a chain-of-transmission explanation.', 'شرح موثّق لفحص المدرّسين على أربع مراحل، وتوضيح سلسلة السند.'),
            ('Transparent 30- and 60-minute plan tables, session reports and a family portal.', 'جداول خطط معلنة لجلسات 30 و60 دقيقة، وتقارير بعد كل جلسة، وبوابة للأسرة.'),
        ],
        keeps=[
            ('Multilingual, Arabic/RTL-ready static pages and an installable PWA layer.', 'صفحات ثابتة متعددة اللغات تدعم العربية وRTL، وطبقة PWA قابلة للتثبيت.'),
            ('Course, pricing and FAQ content structures.', 'بنى محتوى للمسارات والأسعار والأسئلة الشائعة.'),
            ('Consent-gated measurement rather than default third-party tracking.', 'قياس مشروط بالموافقة بدل تتبّع طرف ثالث افتراضي.'),
        ],
        stack=[('Astro', 'Astro'), ('Multilingual · RTL', 'متعدد اللغات · RTL'), ('PWA · offline', 'PWA · دون اتصال'), ('Static content', 'محتوى ثابت')],
        source_note=('The founder’s earlier case study describes an in-progress Astro build with 5 languages and 23 routes at ummah-academy.vercel.app; the owner-supplied live domain ummahacademy.net now publishes a fuller course, teacher-vetting and pricing site. Both are recorded here as separate points in time.', 'تصف دراسة المؤسس السابقة نسخة Astro قيد التنفيذ بخمس لغات و23 مسارًا على ummah-academy.vercel.app؛ وينشر الدومين المباشر الذي قدّمه المالك ummahacademy.net حاليًا موقعًا أوسع للمسارات والتحقق من المدرّسين والأسعار. الاثنان موثّقان هنا كنقطتين زمنيتين مختلفتين.'),
    ),
    C(
        slug='zad', title='Zad', title_ar='زاد', year='2025–26', track='product',
        kicker='OFFLINE-FIRST WORSHIP COMPANION', kicker_ar='رفيق عبادة يعمل دون اتصال',
        lede='An ad-free, offline-first Islamic companion covering prayer times, Qur’an plans, adhkar, a digital tasbih and seasonal guides, with optional cloud sync.',
        lede_ar='رفيق إسلامي بلا إعلانات يعمل دون اتصال: مواقيت الصلاة، وخطط القرآن، والأذكار، ومسبحة رقمية، وأدلة المواسم، مع مزامنة سحابية اختيارية.',
        media='case-zad',
        alt='Abstract crescent of light over layered glass panels and quiet prayer-time arcs — illustrative, not an app screen',
        alt_ar='هلال ضوء مجرد فوق طبقات زجاجية وأقواس مواقيت هادئة — توضيحي، وليس شاشة تطبيق',
        live='https://zadullmuslim.vercel.app/', repo='https://github.com/3boalazm/zad',
        problem='A daily worship companion must work with no connection, carry no advertising, and keep optional sync clearly separate from the core experience.',
        problem_ar='رفيق عبادة يومي يجب أن يعمل بلا اتصال، بلا إعلانات، مع فصل المزامنة الاختيارية بوضوح عن التجربة الأساسية.',
        approach='A PWA with a service worker and local-first content, an optional Node/TypeScript sync API over PostgreSQL, and Arabic-first content with documented sources.',
        approach_ar='تطبيق PWA مع Service Worker ومحتوى محلي أولًا، وواجهة مزامنة اختيارية بـ Node/TypeScript على PostgreSQL، ومحتوى عربي أولًا بمصادر موثّقة.',
        build=[
            ('Prayer times, Qur’an completion plans, documented adhkar and a digital tasbih.', 'مواقيت الصلاة، وخطط ختم القرآن، وأذكار موثّقة، ومسبحة رقمية.'),
            ('A daily worship checklist, badges, inheritance, missed-prayer and zakat tools.', 'جدول عبادات يومي، وأوسمة، وأدوات للميراث والفوائت وزكاة المال المستجد.'),
            ('A 4,273-hadith offline text library and 26 rotating audio items.', 'مكتبة نصوص بـ٤٢٧٣ حديثًا تعمل دون اتصال، و٢٦ مادة صوتية متبدّلة.'),
            ('A daily worship schedule and seasonal guides for Dhul-Hijjah, Arafah and Hajj.', 'جدول عبادات يومي وأدلة مواسم لعشر ذي الحجة ويوم عرفة ومناسك الحج.'),
            ('A kids mode and a large multi-screen Arabic interface.', 'وضع للأطفال وواجهة عربية واسعة متعددة الشاشات.'),
            ('An optional, separately documented cloud-sync API — never required to use the app.', 'واجهة مزامنة سحابية اختيارية موثّقة بشكل منفصل، ولا تُشترط لاستخدام التطبيق.'),
        ],
        keeps=[
            ('A working offline PWA and service-worker cache.', 'تطبيق PWA يعمل دون اتصال وذاكرة تخزين مؤقت عبر Service Worker.'),
            ('A documented 64-screen Arabic interface and offline text library.', 'واجهة عربية موثّقة بـ64 شاشة ومكتبة نصوص تعمل دون اتصال.'),
            ('Arabic content structures for plans, adhkar and seasons.', 'بنى محتوى عربي للخطط والأذكار والمواسم.'),
            ('A clearly separated sync layer with its own API contract.', 'طبقة مزامنة منفصلة بوضوح ولها عقد API خاص.'),
        ],
        stack=[('PWA', 'PWA'), ('Service Worker', 'Service Worker'), ('Firebase', 'Firebase'), ('Node/TypeScript · PostgreSQL', 'Node/TypeScript · PostgreSQL'), ('64 screens', '64 شاشة')],
    ),
    C(
        slug='ibrahim-taha-axiom', title='Ibrahim Taha Axiom', title_ar='إبراهيم طه · Axiom', year='2026', track='product',
        kicker='ACADEMIC IDENTITY · SOURCED NUMBERS', kicker_ar='هوية أكاديمية · أرقام بمصادرها',
        lede='A bilingual academic platform where every metric states what it counts, publications link to evidence, and an interactive lab states what it does not prove.',
        lede_ar='منصة أكاديمية ثنائية اللغة: كل رقم يوضّح ماذا يحصي، وكل بحث مرتبط بدليله، ومختبر تفاعلي يصرّح بما لا يُثبته.',
        media='case-axiom',
        alt='Abstract normal distribution curve and linked research nodes in teal and violet glass — illustrative, not a chart from the site',
        alt_ar='منحنى توزيع طبيعي مجرد وعقد بحثية مترابطة بزجاج تركوازي وبنفسجي — توضيحي، وليس رسمًا من الموقع',
        live='https://ibrahim-taha-axiom.vercel.app/', repo='https://github.com/3boalazm/-Ibrahim-Taha-Axiom',
        problem='An academic profile mixes incomparable platform counters, unsourced claims and a temptation to present simulations as published results.',
        problem_ar='تخلط الصفحة الأكاديمية عادةً بين عدّادات منصات غير قابلة للمقارنة، وادعاءات بلا مصادر، وإغراء تقديم المحاكاة كأنها نتائج منشورة.',
        approach='Content counts are generated from approved data, reference templates stay read-only, and each metric carries its source, retrieval date and a plain-language definition.',
        approach_ar='تُولَّد أعداد المحتوى من بيانات معتمدة، وتبقى قوالب المراجع للقراءة فقط، وكل رقم يحمل مصدره وتاريخ استرجاعه وتعريفًا بلغة واضحة.',
        build=[
            ('A bilingual EN/AR site with research areas, publications and academic profiles.', 'موقع ثنائي اللغة عربي/إنجليزي يضم مجالات البحث والمنشورات والملفات الأكاديمية.'),
            ('A knowledge graph linking areas, methods, publications and projects.', 'خريطة معرفة تربط المجالات والمناهج والمنشورات والمشاريع.'),
            ('Sourced metric panels that explain what each platform counter actually counts.', 'لوحات أرقام بمصادر تشرح ماذا يحصي عدّاد كل منصة فعليًا.'),
            ('An interactive normal-distribution lab and a multicollinearity experiment with explicit limits.', 'مختبر تفاعلي للتوزيع الطبيعي وتجربة تعدد الخطية، مع حدود معلنة صراحةً.'),
        ],
        keeps=[
            ('Generated inventory commands instead of hand-edited counts.', 'أوامر توليد جرد بدل الأعداد المكتوبة يدويًا.'),
            ('Read-only reference snapshots of three academic templates and their comparison.', 'نسخ مرجعية للقراءة فقط من ثلاثة قوالب أكاديمية مع تحليل المقارنة.'),
            ('Source links with retrieval dates and a "not an official metric" notice.', 'روابط مصادر بتواريخ استرجاع وتنبيه «ليس مقياسًا مؤسسيًا رسميًا».'),
        ],
        stack=[('Static site', 'موقع ثابت'), ('Generated inventories', 'جرد مولَّد'), ('Bilingual EN/AR', 'ثنائي اللغة عربي/إنجليزي'), ('SVG / canvas charts', 'رسوم SVG / Canvas')],
    ),
    C(
        slug='nile-bed', title='Nile Bed', title_ar='نايل بد', year='2026', track='product',
        kicker='B2B INDUSTRIAL CATALOGUE · ARABIC FIRST', kicker_ar='كتالوج صناعي B2B · عربية أولًا',
        lede='A bilingual catalogue for a mattress-spring manufacturer and wholesaler: product groups, a full direction flip for English, and WhatsApp enquiry instead of a fake checkout.',
        lede_ar='كتالوج ثنائي اللغة لمصنّع سوست مراتب وتاجر جملة: مجموعات منتجات، وانقلاب كامل للاتجاه عند الإنجليزية، واستفسار عبر واتساب بدل سلة شراء وهمية.',
        media='case-nile-bed',
        alt='Abstract coiled spring geometry and industrial catalogue grid in teal and violet — illustrative, not a product photo',
        alt_ar='هندسة سوست حلزونية مجردة وشبكة كتالوج صناعي بالتركوازي والبنفسجي — توضيحي، وليس صورة منتج',
        live='https://nile-bed.vercel.app/', repo='https://github.com/3boalazm/Nile-Bed',
        problem='An industrial supplier needs a catalogue Arabic buyers can actually use, with no authentication or external image service standing between them and an enquiry.',
        problem_ar='يحتاج مورّد صناعي إلى كتالوج يستخدمه المشتري العربي فعليًا، بلا مصادقة أو خدمة صور خارجية تحول بينه وبين الاستفسار.',
        approach='Arabic is the default, the entire layout direction flips for English, the theme is applied before first paint, and enquiries route straight to WhatsApp.',
        approach_ar='العربية هي الافتراضية، وينقلب اتجاه التخطيط بالكامل للإنجليزية، ويُطبَّق الثيم قبل أول رسم، وتوجَّه الاستفسارات مباشرة إلى واتساب.',
        build=[
            ('A product-led catalogue with 68 items across eight product groups.', 'كتالوج يبدأ بالمنتج، بـ68 صنفًا في ثماني مجموعات.'),
            ('A one-tap Arabic/English switch that flips the whole page.', 'مفتاح عربي/إنجليزي بلمسة واحدة يقلب الصفحة بالكامل.'),
            ('Light and dark themes following the system, remembered locally and applied before first paint.', 'ثيم فاتح وداكن يتبع النظام، ويُحفظ محليًا، ويُطبَّق قبل أول رسم لتجنّب وميض الخاطئ.'),
            ('A two-step catalogue → order flow: initial selection, then quantities and contact.', 'تدفق من خطوتين «الكتالوج ← الطلب»: اختيار أولي، ثم كميات وبيانات تواصل.'),
            ('Official brand artwork in both variants and direct WhatsApp enquiry flows.', 'هوية بصرية رسمية بنسختيها، وتدفقات استفسار مباشرة عبر واتساب.'),
        ],
        keeps=[
            ('Bilingual content and a documented RTL/LTR direction switch.', 'محتوى ثنائي اللغة وتبديل اتجاه RTL/LTR موثّق.'),
            ('A design-token system with WCAG foreground/background pair checks.', 'نظام رموز تصميم مع فحص أزواج تباين WCAG للون النص والخلفية.'),
            ('Theme logic with no flash of the wrong mode.', 'منطق ثيم بلا وميض للوضع الخاطئ.'),
            ('A catalogue structure with no login, Firebase or external image dependency.', 'بنية كتالوج بلا تسجيل دخول ولا Firebase ولا اعتماد على خدمة صور خارجية.'),
        ],
        stack=[('Next.js', 'Next.js'), ('TypeScript', 'TypeScript'), ('Bilingual AR/EN · RTL', 'عربي/إنجليزي · RTL'), ('WhatsApp enquiry', 'استفسار واتساب')],
    ),
    C(
        slug='craft-egypt', title='Craft Egypt', title_ar='حِرَف مصر', year='2026', track='product',
        kicker='HERITAGE CRAFTS · MADE TO ORDER', kicker_ar='حِرَف تراثية · طلب حسب الطلب',
        lede='An Arabic RTL storefront and regional craft atlas for Egyptian copperware, textiles, pottery and decor, built around a made-to-order enquiry flow.',
        lede_ar='متجر عربي RTL وأطلس للحِرَف الإقليمية للمشغولات النحاسية والمنسوجات والخزف والديكور، مبني حول تدفق طلبات حسب الطلب.',
        media='case-craft-egypt',
        alt='Abstract hammered copper vessels, woven threads and pottery silhouettes in warm gold and teal — illustrative, not a craft photograph',
        alt_ar='أوانٍ نحاسية مجردة وخيوط منسوجة وصور ظلية للخزف بذهبي دافئ وتركوازي — توضيحي، وليس صورة حِرَفية',
        live='https://craft-egypt.vercel.app/',
        problem='Heritage products need provenance and regional context, but a conventional cart implies stock and pricing that a made-to-order workshop cannot honestly promise.',
        problem_ar='تحتاج المنتجات التراثية إلى مصدر وسياق إقليمي، لكن سلة الشراء التقليدية توحي بمخزون وأسعار لا يقدر ورشة «حسب الطلب» على الوعد بها بصدق.',
        approach='An editorial storefront pairs product categories with a regional craft atlas, and the transaction is an enquiry about the piece rather than a checkout.',
        approach_ar='متجر تحريري يجمع فئات المنتجات مع أطلس للحِرَف المناطقية، وتكون المعاملة استفسارًا عن القطعة لا إتمام شراء.',
        build=[
            ('An Arabic-first RTL storefront with copper, porcelain, pottery and handmade categories.', 'متجر عربي أولًا بتخطيط RTL لفئات النحاسيات والبورسلين والفخار والهاند ميد.'),
            ('A regional craft atlas and heritage catalogue.', 'أطلس إقليمي للحِرَف وكتالوج تراثي.'),
            ('Product stories that lead into a made-to-order enquiry flow.', 'قصص منتجات تنتهي بتدفق طلب حسب الطلب.'),
            ('A workshop journal explaining made-to-order, leather and Qena clay.', 'مجلة ورشة تشرح الطلب حسب الطلب، والجلد الطبيعي، وقلل قنا.'),
            ('A visual language built around material, maker and place.', 'لغة بصرية تدور حول الخامة والصانع والمكان.'),
        ],
        keeps=[
            ('A bilingual content model for crafts, regions and pieces.', 'نموذج محتوى ثنائي اللغة للحِرَف والمناطق والقطع.'),
            ('An RTL storefront layout and inquiry-first flow.', 'تخطيط متجر RTL وتدفق يبدأ بالاستفسار.'),
            ('Heritage category and atlas structures.', 'بنى فئات تراثية وأطلس مناطقي.'),
        ],
        stack=[('Arabic RTL', 'عربية RTL'), ('Static storefront', 'متجر ثابت'), ('Made-to-order flow', 'طلب حسب الطلب'), ('Regional atlas', 'أطلس إقليمي')],
        source_note=('The supplied repository URL is not publicly reachable (404/403), so this page documents only what the live deployment shows. No code-level claim is made.', 'رابط المستودع المُقدَّم غير متاح للعامة (404/403)، لذا توثّق هذه الصفحة ما يظهر في الموقع المباشر فقط، دون أي ادعاء على مستوى الكود.'),
    ),
    C(
        slug='speech-to-text-studio', title='Speech to Text Studio', title_ar='استوديو تحويل الكلام إلى نص', year='2026', track='product',
        kicker='RESILIENT TRANSCRIPTION · SERVER-SIDE FAILOVER', kicker_ar='نسخ مرن · تبديل تلقائي من الخادم',
        lede='Upload a file or record live and get an editable transcript — four transcription engines sit behind one API route, with automatic failover the user never sees.',
        lede_ar='ارفع ملفًا أو سجّل مباشرة واحصل على نص قابل للتحرير — أربعة محرّكات نسخ خلف مسار API واحد، مع تبديل تلقائي لا يراه المستخدم.',
        media='case-stt',
        alt='Abstract layered audio waveforms converging into one clean text ribbon in teal and violet — illustrative, not a software UI',
        alt_ar='موجات صوتية مجردة متعددة تتقاطع في شريط نص واحد نظيف بالتركوازي والبنفسجي — توضيحي، وليس واجهة برنامج',
        live='https://mahtool.vercel.app/', repo='https://github.com/3boalazm/MahmoudTC-tool',
        problem='A single transcription provider fails on rate limits, exhausted credit or an empty result; the user should not have to notice or retry.',
        problem_ar='أي مزوّد نسخ واحد يفشل عند حدّ الطلبات أو نفاد الرصيد أو نتيجة فارغة؛ ولا يجب أن يلاحظ المستخدم أو يعيد المحاولة.',
        approach='One server-side route owns an ordered engine chain. Keys never reach the browser, and each engine is tried in turn until a usable transcript comes back.',
        approach_ar='مسار واحد على الخادم يملك سلسلة محرّكات مرتّبة. المفاتيح لا تصل للمتصفح، ويُجرَّب كل محرّك بدوره حتى يعود نص صالح.',
        build=[
            ('File upload, in-browser microphone recording and a real waveform preview.', 'رفع ملفات، وتسجيل مباشر داخل المتصفح، ومعاينة موجة صوتية حقيقية.'),
            ('An ordered four-engine chain with failover on 429/402/401, 5xx, timeout and empty transcript.', 'سلسلة من أربعة محرّكات مرتّبة، مع تبديل عند 429/402/401 و5xx والمهلة والنص الفارغ.'),
            ('A Next.js route handler that keeps every API key server-side.', 'مسار Next.js يُبقي جميع مفاتيح API على الخادم.'),
            ('Editable, exportable transcripts as .txt and .srt in an installable PWA.', 'نصوص قابلة للتحرير والتصدير بصيغتي txt وsrt داخل PWA قابل للتثبيت.'),
            ('Public usage, engines and FAQ pages explaining limits, privacy and failure trails.', 'صفحات عامة للاستخدام والمحرّكات والأسئلة الشائعة تشرح الحدود والخصوصية ومسار المحاولات.'),
        ],
        keeps=[
            ('A documented ENGINE_ORDER and failover contract.', 'ترتيب محرّكات ENGINE_ORDER موثّق وعقد تبديل تلقائي.'),
            ('An editable transcript editor and export.', 'محرّر نصوص قابل للتحرير وتصدير.'),
            ('A public 4-engine / 20+ language / 25 MB+ / 0-files-stored status strip.', 'شريط حالة عام: 4 محرّكات، أكثر من 20 لغة، أكثر من 25 ميجابايت، صفر ملفات مخزّنة.'),
            ('A server-only secrets boundary.', 'حدّ واضح للأسرار على الخادم فقط.'),
        ],
        stack=[('Next.js', 'Next.js'), ('TypeScript', 'TypeScript'), ('4 STT engines', '4 محرّكات نسخ'), ('PWA', 'PWA')],
    ),
    C(
        slug='pharmacy-saas', title='Pharmacy SaaS — Web Frontend', title_ar='صيدليتي · واجهة الويب', year='2026', track='product',
        kicker='BOUNDED CONTEXTS · FRONTEND ONLY', kicker_ar='سياقات محدودة · واجهة فقط',
        lede='A production pharmacy frontend that mirrors backend bounded contexts with strict module boundaries, Arabic RTL and precision money handling — explicitly frontend only.',
        lede_ar='واجهة صيدلية إنتاجية تعكس السياقات المحدودة للخادم بحدود استيراد صارمة، وتخطيط عربي RTL، ومعالجة دقيقة للمبالغ — ومُعلَّنة صراحةً كواجهة فقط.',
        media='case-pharmacy',
        alt='Abstract modular pharmacy grid with medicine rows and precise ledger lines in teal and blue — illustrative, not a product screenshot',
        alt_ar='شبكة صيدلية معيارية مجردة بصفوف أدوية وخطوط دفاتر دقيقة بالتركوازي والأزرق — توضيحي، وليس لقطة منتج',
        live='https://drassmaaaboalazmpharmacy.vercel.app/', repo='https://github.com/3boalazm/pharmacy-web',
        problem='Pharmacy operations split into POS, inventory, customers and purchasing; a generic admin template quietly mixes them and mishandles money.',
        problem_ar='تنقسم عمليات الصيدلية بين نقطة البيع والمخزون والعملاء والمشتريات، وأي قالب إدارة عام يخلطها بهدوء ويُسيء معالجة المبالغ.',
        approach='The frontend follows the CTO architecture decision and API contract documents: one module per bounded context, strict import boundaries, and a token-driven Arabic RTL design system.',
        approach_ar='تتبع الواجهة وثيقة قرار المعمارية وعقد API: وحدة لكل سياق محدود، وحدود استيراد صارمة، ونظام تصميم عربي RTL قائم على الرموز.',
        build=[
            ('An auth-guarded app shell with a sidebar per the design system.', 'هيكل تطبيق محمي بالمصادقة بشريط جانبي وفق نظام التصميم.'),
            ('Bounded modules for catalog, POS, inventory/GRN, customers and dashboard.', 'وحدات محدودة للكتالوج ونقطة البيع والمخزون/إذن الاستلام والعملاء واللوحة الرئيسية.'),
            ('TanStack Query for server state and Zustand confined to the POS cart.', 'TanStack Query لحالة الخادم، وZustand محصور في سلة نقطة البيع فقط.'),
            ('Token-driven Tailwind styling and the Cairo typeface in Arabic RTL.', 'تنسيق Tailwind قائم على الرموز وخط Cairo بتخطيط عربي RTL.'),
        ],
        keeps=[
            ('An architecture decision document and API contract specification.', 'وثيقة قرار معماري ومواصفة عقد API.'),
            ('A documented module map with strict boundaries.', 'خريطة وحدات موثّقة بحدود صارمة.'),
            ('An explicit frontend-only scope note — no backend or patient-data claim.', 'تسمية صريحة «واجهة فقط»، دون ادعاء بخادم أو بيانات مرضى.'),
        ],
        stack=[('Next.js 14', 'Next.js 14'), ('TypeScript strict', 'TypeScript صارم'), ('Tailwind tokens', 'رموز Tailwind'), ('TanStack Query · Zustand', 'TanStack Query · Zustand'), ('Arabic RTL', 'عربية RTL')],
        source_note=('The live URL currently redirects to a login screen, so the public interface is limited. This page documents the repository contract and the founder’s case study, not a live patient workflow.', 'يُعيد الموقع المباشر حاليًا التوجيه إلى شاشة دخول، لذا الواجهة العامة محدودة. توثّق هذه الصفحة عقد المستودع ودراسة المؤسس، لا سير عمل مرضى مباشر.'),
    ),
    C(
        slug='farm-console', title='Farm Console', title_ar='لوحة المزرعة', year='2025–26', track='product',
        kicker='OFFLINE-CAPABLE LIVESTOCK PLATFORM', kicker_ar='منصة ثروة حيوانية تعمل دون اتصال',
        lede='An Arabic RTL livestock console tracking herd records, breeding lineages, veterinary schedules, feed costs and net profit, designed to survive poor connectivity.',
        lede_ar='لوحة عربية RTL لإدارة الثروة الحيوانية تتتبّع سجلات القطيع وسلالات التربية وجداول الطب البيطري وتكاليف العلف وصافي الربح، مصمّمة لتعمل مع ضعف الاتصال.',
        media='case-farm',
        alt='Abstract herd record cards, lineage lines and quiet cost charts in teal and green — illustrative, not a dashboard screenshot',
        alt_ar='بطاقات سجلات قطيع مجردة وخطوط سلالات ورسوم تكلفة هادئة بالتركوازي والأخضر — توضيحي، وليس لقطة لوحة بيانات',
        live='https://farm-project-puce.vercel.app/', repo='https://github.com/3boalazm/farm-project',
        problem='Farm records are entered in the field, often offline, and need to stay usable in Arabic with costs and lineage readable at a glance.',
        problem_ar='تُدخل سجلات المزرعة في الحقل وغالبًا دون اتصال، وتحتاج أن تبقى صالحة بالعربية مع تكاليف وسلالات مقروءة بنظرة واحدة.',
        approach='An offline-capable RTL PWA keeps records locally, syncs optionally, and presents cost and profit views rather than raw tables.',
        approach_ar='تطبيق PWA عربي RTL يعمل دون اتصال، يحفظ السجلات محليًا، ويزامن اختياريًا، ويعرض التكلفة والربح بدل جداول خام.',
        build=[
            ('Herd registry with breeding lineages and animal records.', 'سجل قطيع بسلالات التربية وسجلات لكل رأس.'),
            ('Veterinary schedules and feed-cost tracking.', 'جداول الطب البيطري وتتبّع تكاليف العلف.'),
            ('A net-profit view with charted costs and returns.', 'عرض صافي الربح مع رسوم للتكاليف والعوائد.'),
            ('An offline-capable PWA layer with optional realtime sync.', 'طبقة PWA تعمل دون اتصال مع مزامنة فورية اختيارية.'),
        ],
        keeps=[
            ('Arabic RTL record structures.', 'بنى سجلات عربية RTL.'),
            ('Offline data and chart views.', 'بيانات دون اتصال وعروض رسومية.'),
            ('A documented optional sync configuration.', 'إعداد مزامنة اختياري موثّق.'),
        ],
        stack=[('PWA', 'PWA'), ('Firebase', 'Firebase'), ('Realtime DB', 'Realtime DB'), ('Chart.js', 'Chart.js')],
        source_note=('The live URL currently redirects to a login screen, so the public interface is limited. This page also draws on the repository reference and the founder’s published case study; it does not claim a live, open farm dashboard.', 'يُعيد الموقع المباشر حاليًا التوجيه إلى شاشة دخول، لذا الواجهة العامة محدودة. تعتمد هذه الصفحة أيضًا على مرجع المستودع ودراسة المؤسس المنشورة، ولا تدّعي لوحة مزرعة مباشرة مفتوحة.'),
    ),
    C(
        slug='sakanwave', title='SakanWave', title_ar='SakanWave', year='2026', track='product',
        kicker='BROWSER-LOCAL AUDIO SEPARATION', kicker_ar='فصل صوتي محلي داخل المتصفح',
        lede='Split any track into vocals, drums, bass and other instruments entirely inside the browser — no upload, no server, nothing leaves the device.',
        lede_ar='افصل أي مقطع إلى غناء وطبول وباص وباقي الآلات بالكامل داخل المتصفح — بلا رفع ولا خادم ولا شيء يخرج من الجهاز.',
        media='case-sakanwave',
        alt='Abstract four glowing audio stems separating from a single waveform in violet and teal — illustrative, not an audio workspace',
        alt_ar='أربعة مسارات صوتية متوهجة مجردة تنفصل عن موجة واحدة بالبنفسجي والتركوازي — توضيحي، وليس مساحة عمل صوتي',
        live='https://mdp.vercel.app/', repo='https://github.com/3boalazm/MDP',
        problem='Musicians want stems from a track but should not have to upload copyrighted audio to a third-party service to get them.',
        problem_ar='يريد الموسيقيون فصل مسارات أغنية، لكن لا يجب أن يضطروا لرفع مادة محمية حقوقها إلى خدمة طرف ثالث.',
        approach='ONNX Runtime Web and Web Workers run source separation locally; the site only offers a file picker, a workspace and a plain-language how-it-works page.',
        approach_ar='يعمل ONNX Runtime Web مع Web Workers محليًا لفصل المصادر؛ والموقع لا يقدّم سوى اختيار ملف ومساحة عمل وصفحة شرح بلغة واضحة.',
        build=[
            ('Local separation into four stems: vocals, drums, bass and other.', 'فصل محلي إلى أربعة مسارات: الغناء والطبول والباص والباقي.'),
            ('A browser workspace with MP3, WAV and M4A input.', 'مساحة عمل في المتصفح تقبل MP3 وWAV وM4A.'),
            ('A how-it-works page that states the no-upload guarantee.', 'صفحة شرح توضّح بوضوح أن الملفات لا تُرفع.'),
            ('In-browser inference with Web Workers so the interface stays responsive.', 'استدلال داخل المتصفح عبر Web Workers لتبقى الواجهة مستجيبة.'),
        ],
        keeps=[
            ('A local inference pipeline and worker setup.', 'مسار استدلال محلي وإعداد Workers.'),
            ('An Arabic-first product explanation.', 'شرح منتج عربي أولًا.'),
            ('An explicit zero-upload privacy claim that the architecture supports.', 'ادعاء خصوصية صريح بلا رفع، تدعمه المعمارية.'),
        ],
        stack=[('Next.js', 'Next.js'), ('ONNX Runtime Web', 'ONNX Runtime Web'), ('Web Workers', 'Web Workers'), ('Audio AI', 'ذكاء صوتي')],
        source_note=('The founder’s index called this project StemForge; the live deployment now publishes the name SakanWave. Both names are recorded here so the entry stays traceable.', 'أطلق فهرس المؤسس على المشروع اسم StemForge؛ وينشر الموقع المباشر حاليًا اسم SakanWave. الاسمان موثّقان هنا ليبقى المدخل قابلًا للتتبّع.'),
    ),
    C(
        slug='oltre-collective', title='OLTRÈ Collective', title_ar='OLTRÈ Collective', year='2026', track='product',
        kicker='BILINGUAL STREETWEAR · COMMERCE', kicker_ar='أزياء شارعية ثنائية اللغة · تجارة',
        lede='A bilingual streetwear storefront and admin dashboard pairing editorial lookbooks with cart, wishlist, loyalty and order flows.',
        lede_ar='متجر أزياء شارعية ثنائي اللغة ولوحة إدارة تجمع عروضًا تحريرية مع السلة والمفضلة والولاء وتدفقات الطلبات.',
        media='case-oltre',
        alt='Abstract editorial lookbook panels and flowing garment silhouettes in violet and pink — illustrative, not a fashion photograph',
        alt_ar='لوحات عروض تحريرية مجردة وصور ظلية لملابس بالبنفسجي والوردي — توضيحي، وليس تصوير أزياء',
        live='https://momo-shop.vercel.app/', repo='https://github.com/3boalazm/momo-shop',
        problem='Streetwear needs editorial storytelling, but the story has to sit on top of real cart, loyalty and order mechanics rather than replace them.',
        problem_ar='تحتاج أزياء الشارع إلى سرد تحريري، لكن السرد يجب أن يُبنى فوق آليات حقيقية للسلة والولاء والطلبات لا أن يحلّ محلها.',
        approach='Lookbook-led categories lead into a conventional storefront, with a separate role-aware admin dashboard for catalogue and orders.',
        approach_ar='تقود فئات قائمة على عروض Lookbooks إلى متجر تقليدي، مع لوحة إدارة منفصلة تراعي الصلاحيات للكتالوج والطلبات.',
        build=[
            ('A bilingual storefront with editorial lookbooks and product categories.', 'متجر ثنائي اللغة بعروض Lookbooks تحريرية وفئات منتجات.'),
            ('Cart, wishlist and loyalty mechanics.', 'آليات السلة والمفضلة والولاء.'),
            ('Order flows and a role-aware admin dashboard.', 'تدفقات الطلبات ولوحة إدارة تراعي الصلاحيات.'),
            ('A bilingual EN/AR content model shared across storefront and admin.', 'نموذج محتوى ثنائي اللغة عربي/إنجليزي مشترك بين المتجر والإدارة.'),
        ],
        keeps=[
            ('Storefront and admin interfaces.', 'واجهتا المتجر والإدارة.'),
            ('A documented cart, loyalty and order data model.', 'نموذج بيانات موثّق للسلة والولاء والطلبات.'),
            ('Bilingual copy across both surfaces.', 'نصوص ثنائية اللغة على الواجهتين.'),
        ],
        stack=[('React + Vite', 'React + Vite'), ('Drizzle + Postgres', 'Drizzle + Postgres'), ('Payments', 'المدفوعات'), ('Loyalty & roles', 'الولاء والصلاحيات')],
    ),
    C(
        slug='continuum', title='Continuum', title_ar='Continuum', year='2026', track='product',
        kicker='LOCAL-FIRST MEMORY OS · NO BUILD STEP', kicker_ar='نظام ذاكرة محلي أولًا · بلا خطوة بناء',
        lede='A capture → link → work → snapshot → resume loop across many views, stored on the device in localStorage, with optional cloud sync and a bilingual interface.',
        lede_ar='حلقة «التقاط ← ربط ← عمل ← لقطة ← استئناف» عبر عروض متعددة، محفوظة على الجهاز في localStorage، مع مزامنة سحابية اختيارية وواجهة ثنائية اللغة.',
        media='case-continuum',
        alt='Abstract linked thought nodes, timeline threads and a resume loop in teal and violet glass — illustrative, not an app screen',
        alt_ar='عقد أفكار مترابطة مجردة وخيوط زمنية وحلقة استئناف بزجاج تركوازي وبنفسجي — توضيحي، وليس شاشة تطبيق',
        live='https://aboalazmcontinuum.vercel.app/', repo='https://github.com/3boalazm/Continuum',
        problem='Personal knowledge tools lose the context of a session between visits, and a build step makes small changes expensive.',
        problem_ar='تفقد أدوات المعرفة الشخصية سياق الجلسة بين الزيارات، وتجعل خطوة البناء أي تعديل صغير مكلفًا.',
        approach='One HTML page per view shares a single stylesheet and script, with local state, an i18n dictionary and an explicit resume loop — no bundler at all.',
        approach_ar='صفحة HTML واحدة لكل عرض تتشارك ملف CSS وملف JS واحدًا، مع حالة محلية وقاموس ترجمة وحلقة استئناف صريحة — بلا أي أداة تجميع.',
        build=[
            ('Separate pages for projects, tasks, journal, timeline, knowledge, bookmarks, courses, prompts, servers, repos, assistant, search and settings.', 'صفحات منفصلة للمشاريع والمهام واليومية والخط الزمني والمعرفة والإشارات والدورات والموجّهات والخوادم والمستودعات والمساعد والبحث والإعدادات.'),
            ('Shared state, i18n, render, actions and particle logic in one app.js.', 'حالة مشتركة وترجمة وعرض وإجراءات ومنطق جسيمات في ملف app.js واحد.'),
            ('A capture → link → work → snapshot → resume loop.', 'حلقة «التقاط ← ربط ← عمل ← لقطة ← استئناف».'),
            ('Bilingual EN/AR switching, dark mode and optional Firebase sync.', 'تبديل عربي/إنجليزي، ووضع داكن، ومزامنة Firebase اختيارية.'),
        ],
        keeps=[
            ('LocalStorage data that stays on the device by default.', 'بيانات localStorage تبقى على الجهاز افتراضيًا.'),
            ('Shared CSS/JS modules and a page contract (window.__PAGE__).', 'وحدات CSS/JS مشتركة وعقد صفحة window.__PAGE__.'),
            ('A bilingual dictionary and a documented view map.', 'قاموس ثنائي اللغة وخريطة عروض موثّقة.'),
        ],
        stack=[('HTML · CSS · JavaScript', 'HTML · CSS · JavaScript'), ('LocalStorage', 'LocalStorage'), ('No build step', 'بلا خطوة بناء'), ('Optional Firebase sync', 'مزامنة Firebase اختيارية')],
    ),
    C(
        slug='nile-pharma-food', title='Nile Pharma Food', title_ar='نايل فارما فود', year='2020–26', track='identity',
        kicker='BRAND SYSTEM → LIVE PRODUCT SITE', kicker_ar='منظومة علامة ← موقع منتج مباشر',
        lede='One brand arc: a governed bilingual identity, then a live Arabic-first product site that starts with a question, cites its sources and keeps medical advice with the specialist.',
        lede_ar='مسار علامة واحد: هوية ثنائية اللغة محكومة، ثم موقع منتج عربي أولًا يبدأ بالسؤال، ويذكر مصادره، ويُبقي المشورة الطبية عند المختص.',
        media='case-npf',
        alt='Abstract pharmaceutical packaging panels, leaflet typography and care ribbons in teal and violet — illustrative, not a pack photograph',
        alt_ar='لوحات تغليف دوائية مجردة وطباعة نشرات وشرائط رعاية بالتركوازي والبنفسجي — توضيحي، وليس صورة عبوة',
        live='https://nilepharmafood.com/',
        problem='Health products are usually sold before they are explained; a brand system alone does not fix that, and a storefront alone does not keep the identity coherent.',
        problem_ar='تُباع المنتجات الصحية غالبًا قبل أن تُشرح؛ ومنظومة العلامة وحدها لا تصلح ذلك، والمتجر وحده لا يحفظ تماسك الهوية.',
        approach='Govern the bilingual identity first, then publish a question-led site where product information comes from original leaflets, claims cite their source, and measurement is consent-gated.',
        approach_ar='حوكمة الهوية ثنائية اللغة أولًا، ثم نشر موقع يبدأ بالسؤال، تُؤخذ معلومات المنتج من نشراته الأصلية، وتُذكر مصادر الادعاءات، ويكون القياس مشروطًا بالموافقة.',
        build=[
            ('A bilingual brand system covering packaging, shelf presence and campaign governance.', 'منظومة علامة ثنائية اللغة للتغليف والحضور على الأرفف وحوكمة الحملات.'),
            ('A live Arabic-first site with six question-led learning paths and an eight-product index.', 'موقع مباشر عربي أولًا بستة مسارات معرفية تبدأ بالسؤال، وفهرس لثمانية منتجات.'),
            ('Product pages, health-basics cards, quality-sourcing and scientific-collaboration areas.', 'صفحات منتجات، وكروت «الصحة ببساطة»، ومناطق للمصدر والجودة والتعاون العلمي.'),
            ('Consent-gated analytics and an explicit "not a substitute for a doctor or pharmacist" boundary.', 'تحليلات مشروطة بالموافقة، وحدّ صريح «لا تغني عن الطبيب أو الصيدلي».'),
        ],
        keeps=[
            ('A bilingual brand and content model.', 'نموذج علامة ومحتوى ثنائي اللغة.'),
            ('Product records with sourcing references.', 'سجلات منتجات بإحالات إلى مصادرها.'),
            ('A published privacy/consent interface.', 'واجهة خصوصية وموافقة منشورة.'),
        ],
        stack=[('Arabic RTL', 'عربية RTL'), ('Brand governance', 'حوكمة علامة'), ('CMS-driven content', 'محتوى عبر CMS'), ('Consent-gated analytics', 'تحليلات مشروطة بالموافقة')],
        source_note=('The supplied NPF repository URL is not publicly reachable (404/403). This page documents the live site and the founder’s brand-system case study; no code-level claim is made.', 'رابط مستودع NPF المُقدَّم غير متاح للعامة (404/403). توثّق هذه الصفحة الموقع المباشر ودراسة منظومة العلامة للمؤسس، دون أي ادعاء على مستوى الكود.'),
    ),
    C(
        slug='evolve-system', title='Evolve System', title_ar='Evolve System', year='2026', track='product',
        kicker='SOURCE ACCESS PENDING', kicker_ar='الوصول للمصدر قيد الانتظار',
        lede='A repository reference supplied by the owner. Source access is not publicly available, so this page documents the reference only and makes no technical or outcome claims.',
        lede_ar='مرجع مستودع قدّمه المالك. الوصول إلى المصدر غير متاح للعامة، لذا توثّق هذه الصفحة المرجع فقط ولا تُقدّم أي ادعاءات تقنية أو نتائج.',
        media='case-evolve',
        alt='Abstract closed source vault with layered panels and a soft violet-teal glow — illustrative, not a product reference',
        alt_ar='خزنة مصدر مغلقة مجردة بطبقات ووهج بنفسجي تركوازي هادئ — توضيحي، وليس مرجع منتج',
        repo='https://github.com/3boalazm/evolve-system',
        status=('Source access pending', 'الوصول للمصدر قيد الانتظار'),
        role=ROLE_PENDING,
        problem='No public source is available, so no problem statement can be verified. This page deliberately does not invent one.',
        problem_ar='لا يوجد مصدر عام متاح، لذلك لا يمكن التحقق من أي صياغة للمشكلة. هذه الصفحة لا تخترع صياغة عن قصد.',
        approach='Once the owner grants repository access or supplies a brief, the same documented structure used across these case studies can be filled in from verifiable material.',
        approach_ar='عندما يتيح المالك الوصول إلى المستودع أو يزوّدنا بموجز، يمكن ملء البنية الموثّقة نفسها المستخدمة في هذه الدراسات من مادة قابلة للتحقق.',
        build=[
            ('Repository reference recorded as supplied by the owner.', 'تسجيل مرجع المستودع كما قدّمه المالك.'),
            ('No architecture, stack or feature claim until the source is accessible.', 'لا ادعاءات عن المعمارية أو الحزمة أو المزايا حتى يتاح المصدر.'),
            ('No screenshots, metrics or results published.', 'لا لقطات شاشة ولا أرقام ولا نتائج منشورة.'),
        ],
        keeps=[
            ('An explicit access-status record.', 'سجل صريح لحالة الوصول.'),
            ('A link back to the supplied repository URL.', 'رابط إلى عنوان المستودع المُقدَّم.'),
            ('The same evidence rules applied to every other case study.', 'قواعد الإثبات ذاتها المطبّقة على بقية الدراسات.'),
        ],
        stack=[('Source access pending', 'الوصول للمصدر قيد الانتظار')],
        evidence=('Only the repository URL supplied by the owner is documented here. The GitHub repository is not publicly reachable (404/403), and no live deployment was supplied. No scope, stack, authorship, client or result is claimed. Detail can be added after owner access.', 'يُوثَّق هنا عنوان المستودع الذي قدّمه المالك فقط. المستودع غير متاح للعامة على GitHub (404/403)، ولم يُقدَّم موقع مباشر. لا ادعاءات عن النطاق أو الحزمة أو التأليف أو عميل أو نتيجة. يمكن إضافة التفاصيل بعد إتاحة الوصول.'),
        source_note=('Supplied repository URL returns 404/403 to unauthenticated requests. Recorded as a pending source, not as a completed case study.', 'يُعيد رابط المستودع المُقدَّم 404/403 للطلبات غير المصادَق عليها. مُسجَّل كمصدر قيد الانتظار، لا كدراسة حالة مكتملة.'),
    ),
]

# The founder archive and these detailed pages overlap on 12 entries. Map by
# source case URL first, then by title for rows with no case URL. One detailed
# page can serve two archive rows when the same project appears twice there.
ARCHIVE_CASE_BY_URL = {
    'https://aboalazm-os.vercel.app/case-studies/nile-pharma': 'nile-pharma-food',
    'https://aboalazm-os.vercel.app/case-studies/nile-pharma-storefront': 'nile-pharma-food',
    'https://aboalazm-os.vercel.app/case-studies/momo-collective': 'oltre-collective',
    'https://aboalazm-os.vercel.app/case-studies/zad': 'zad',
    'https://aboalazm-os.vercel.app/case-studies/farm-console': 'farm-console',
    'https://aboalazm-os.vercel.app/case-studies/speech-to-text-studio': 'speech-to-text-studio',
    'https://aboalazm-os.vercel.app/case-studies/continuum': 'continuum',
    'https://aboalazm-os.vercel.app/case-studies/pharmacy-web': 'pharmacy-saas',
    'https://aboalazm-os.vercel.app/case-studies/ummah-academy': 'ummah-academy',
    'https://aboalazm-os.vercel.app/case-studies/stemforge': 'sakanwave',
}
ARCHIVE_CASE_BY_TITLE = {
    'Nile Bed': 'nile-bed',
    'Craft Egypt': 'craft-egypt',
}


def archive_case_slug(w):
    return ARCHIVE_CASE_BY_URL.get(w.get('case')) or ARCHIVE_CASE_BY_TITLE.get(w.get('title'))
