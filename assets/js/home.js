/* ==========================================================================
   Code & Canvas homepage — page behaviour (vanilla JS, no deps)
   Shared runtime (language, icons, reveal, tilt, preloader…) lives in site.js.
   English is authored in index.html; Arabic sits beside it in data-ar* attributes.
   ========================================================================== */
(() => {
  'use strict';

  const { $, $$ } = CC;

  /* ------------------------------------------------------------------ */
  /*  Document metadata per language                                     */
  /* ------------------------------------------------------------------ */
  const metaDesc = $('meta[name="description"]');
  const META = {
    en: { title: document.title, desc: metaDesc ? metaDesc.content : '' },
    ar: {
      title: 'Code & Canvas — الهوية والتقنية والبيانات، مبنية حول نتيجة أعمال',
      desc: 'تساعد Code & Canvas المؤسسات في المنطقة على النمو عبر مواءمة الهوية والتقنية والبيانات مع أهداف العمل — بنطاق واضح وتسليم على مراحل بمعالم محددة.',
    },
  };

  /* ------------------------------------------------------------------ */
  /*  Boot                                                               */
  /* ------------------------------------------------------------------ */
  CC.onLang((lang) => {
    const m = META[lang];
    document.title = m.title;
    if (metaDesc) metaDesc.content = m.desc;
    $$('[data-current-year]').forEach((el) => { el.textContent = String(new Date().getFullYear()); });
  });

  CC.boot();
})();
