# -*- coding: utf-8 -*-
"""New article (2026-11): From Brand Identity to Brand Systems.
Bilingual in the markup itself (data-ar*), so /ar/blog/<slug>/ is a real Arabic
article without a separate translation file. No fabricated client results.
"""
POST = dict(
    slug='from-brand-identity-to-brand-systems',
    title='From Brand Identity to Brand Systems',
    title_ar='من هوية العلامة إلى أنظمة العلامة',
    cat='Brand Identity', cat_ar='هوية العلامة', minutes=7, date='November 2026', author='ma', emoji='🏛️',
    featured=False, bilingual=True, og='/assets/brand/og/blog-brand-systems.png',
    excerpt='A static manual is not a brand. The moment a second team touches your identity, the question stops being "does the logo look right" and becomes "does the system make the right decision without us?"',
    excerpt_ar='الدليل الثابت ليس علامة. لحظة أن يلمس فريق ثانٍ الهوية، يتوقّف السؤال عن «هل الشعار صحيح» ويصير: «هل يتخذ النظام القرار الصحيح دوننا؟»',
    card='Why brand manuals go out of date the day they are delivered — and what replaces them.',
    stats=[],
    body='''
<h2 id="manual-problem" data-ar="مشكلة الدليل الثابت">The problem with a static manual</h2>
<p data-ar="يُسلَّم دليل العلامة كملف نهائي: شعار، وألوان، وخطوط، وبعض التطبيقات المثالية. لعدة أسابيع يبدو كل شيء مضبوطًا. ثم تطلق الشركة منتجًا جديدًا، ويحتاج فريق التوظيف إلى قالب عرض، ويتعاقد مورّد مختلف على التغليف، ويفتح مكتب إقليمي صفحة على السوشيال — ولا يجيب الدليل عن أي من هذه الأسئلة.">A brand manual arrives as a finished file: a logo, colours, type and a handful of perfect applications. For a few weeks everything looks controlled. Then the company launches a new product, recruiting needs a deck template, a different supplier produces the packaging, and a regional office opens a social page — and the manual answers none of those questions.</p>
<p data-ar="النتيجة ليست فوضى بصرية فقط، بل قرارات تتخذها الصدفة: من يملك التغيير؟ هل يجوز تعديل التركيب ليتناسب مع مساحة ضيقة؟ هل تُترجم العلامة أم تُعاد صياغتها بالعربية؟ إن لم تكن الإجابة مكتوبة، فالإجابة هي رأي أعلى صوت في الاجتماع.">The result is not only visual drift. It is decisions made by accident: who owns a change, whether the lockup may be adjusted for a narrow space, whether the brand is translated or rebuilt in Arabic. If the answer is not written down, the answer is whoever speaks loudest in the meeting.</p>
<blockquote class="pull" data-ar="الهوية مجموعة أصول. منظومة العلامة مجموعة قرارات.">An identity is a set of assets. A brand system is a set of decisions.</blockquote>

<h2 id="what-is-a-system" data-ar="ما الذي يجعل الهوية نظامًا؟">What makes an identity a system</h2>
<p data-ar="النظام لا يُعرَّف بعدد صفحات الدليل، بل بثلاث خصائص: قواعد قابلة للتكرار، ورموز قابلة للتنفيذ، وحوكمة تُحدّد من يقرّر. حين تتوفر هذه الثلاثة، يستطيع فريق لم يحضر ورشة التأسيس أن ينتج أصلًا جديدًا يبدو وكأنه من المصدر نفسه.">A system is not defined by page count. It is defined by three properties: repeatable rules, executable tokens, and governance that says who decides. With those three, a team that never attended the founding workshop can produce a new asset that looks like it came from the same source.</p>
<ol class="num-list">
<li><strong data-ar="قواعد مشتقة من قرار">Rules derived from a decision</strong><p data-ar="لا يُختار اللون لأنه جميل، بل لأن التموضع يقتضي إشارة معينة في السوق. كل قاعدة بصرية تعود إلى سبب تجاري أو وظيفي معلن.">Colour is not chosen because it is attractive; it is chosen because the positioning needs a particular signal in the market. Every visual rule traces back to a stated commercial or functional reason.</p></li>
<li><strong data-ar="رموز قابلة للتنفيذ">Executable tokens</strong><p data-ar="الفراغات والطبقات والحالات والألوان تُعرَّف مرة واحدة وتُستهلك في Figma والكود وملفات الطباعة. تغيير رمز واحد ينتشر في كل مكان بدل أن يُصحَّح يدويًا في أربعين ملفًا.">Spacing, elevation, states and colour are defined once and consumed in Figma, in code and in print files. Changing one token propagates everywhere instead of being corrected by hand in forty files.</p></li>
<li><strong data-ar="حوكمة وحقوق قرار">Governance and decision rights</strong><p data-ar="من يعتمد تطبيقًا جديدًا؟ ما الذي لا يجوز تغييره أبدًا؟ متى يُعاد فتح التموضع؟ هذه أسئلة تشغيلية، لا أسئلة ذوق.">Who approves a new application? What may never change? When is the positioning reopened? These are operational questions, not questions of taste.</p></li>
</ol>

<h2 id="bilingual-is-structural" data-ar="ثنائية اللغة مسألة بنيوية">Bilingual is structural, not cosmetic</h2>
<p data-ar="في أسواقنا، العربية ليست طبقة تُضاف بعد أن يُنجز التصميم بالإنجليزية. اختلاف اتجاه القراءة، وأطوال الكلمات، وارتفاع الحروف، واتجاه الأرقام، وشكل علامات الترقيم كلها تؤثر على الشبكة نفسها. إن بُني التركيب الإنجليزي أولًا، تصير النسخة العربية إمّا مطوّلة وإمّا مضغوطة — وكلتاهما خطأ.">In our markets, Arabic is not a layer added after the English design is finished. Reading direction, word length, letter height, numeral direction and punctuation all affect the grid itself. If the English lockup is built first, the Arabic version ends up stretched or squeezed — and both are wrong.</p>
<p data-ar="العملية الصحيحة: شبكة هندسية واحدة، وعلاقة نسب معلنة بين التركيبين، وقواعد للحد الأدنى من المقاس عند كل تطبيق. عندها لا تُترجم العلامة؛ بل تُبنى مرتين من القرار نفسه.">The correct process is one geometric grid, a stated proportional relationship between the two lockups, and minimum-size rules for each application. The brand is then not translated; it is built twice from the same decision.</p>

<h2 id="handover" data-ar="التسليم هو المنتج">The handover is the product</h2>
<p data-ar="أكثر ما يُهمّل في مشاريع الهوية هو اليوم التالي للتسليم. الملفات وحدها لا تنقل المنطق. لذلك نعتبر جلسة التسليم، ودليل الحوكمة المختصر، وقائمة «ما الذي لا نفعله» جزءًا من المخرج لا خدمة إضافية.">The most neglected part of identity work is the day after handover. Files alone do not transfer reasoning. That is why the handover session, the short governance guide and an explicit "what we do not do" list are part of the deliverable, not an extra.</p>
<div class="callout-box"><span class="callout-box__icon">✓</span><div><strong data-ar="اختبار بسيط">A simple test</strong><p data-ar="أعطِ فريقًا لم يشارك في المشروع موجزًا لتطبيق جديد لم يرد في الدليل. إن عاد بسؤال «أي درجة زرقاء نستخدم؟» فالنظام ناقص. إن عاد بالتطبيق الصحيح وبسؤال واحد عن الحوكمة، فالنظام يعمل.">Give a team that did not attend the project a brief for an application the manual never covered. If they come back asking "which blue do we use?", the system is incomplete. If they return with the right application and one governance question, the system works.</p></div></div>

<h2 id="where-to-start" data-ar="من أين تبدأ">Where to start</h2>
<p data-ar="ابدأ بجرد كل نقطة تماس تنتجها المؤسسة اليوم، وصنّفها: ما يبقى، وما يتغيّر، وما يُحذف. ثم اكتب التموضع في صفحة واحدة قبل أن تفتح أي ملف تصميم. بعدها فقط تُبنى المنظومة. ترتيب مختلف عن هذا عادةً ما يعني إعادة العمل بعد ستة أشهر.">Start with an inventory of every touchpoint the organization produces today, and classify each: keep, change, remove. Then write the positioning on one page before opening a design file. Only then build the system. A different order usually means rebuilding the work six months later.</p>
<p data-ar="إن أردت رؤية البنية مطبّقة على موجز كامل، افتح دراستنا المفاهيمية عن منظومة علامة ثنائية اللغة — وهي مُعلَّنة بوضوح كدراسة منهج لا كعمل عميل.">To see the structure applied to a full brief, open our bilingual brand-system concept study — clearly labelled as a method study, not client work.</p>
''',
    cta=None, takeaways=None, conclusion=None, faq=None,
    related=['why-most-brands-look-different-but-feel-the-same', 'design-systems-operating-system-modern-digital-products', 'creative-strategy-in-the-age-of-generative-ai'],
    aliases=['brand-identity-to-brand-systems'],
)
