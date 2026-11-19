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
      title: 'Code & Canvas — العلامة والمنتج والمنظومة، حول نتيجة عمل واحدة',
      desc: 'استوديو ثنائي اللغة في السعودية ومصر: نصمّم الهوية، ونبني المنتج الرقمي، ونربط المنظومة خلفهما — بنطاق مكتوب ومعالم تسليم معلنة.',
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
