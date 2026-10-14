/* ==========================================================================
   Code & Canvas homepage — page behaviour (vanilla JS, no deps)
   Shared runtime (language, icons, reveal, tilt, preloader…) lives in site.js.
   English is authored in index.html; Arabic sits beside it in data-ar* attributes.
   ========================================================================== */
(() => {
  'use strict';

  const { $, $$, esc, icon } = CC;

  /* ------------------------------------------------------------------ */
  /*  Document metadata per language                                     */
  /* ------------------------------------------------------------------ */
  const metaDesc = $('meta[name="description"]');
  const META = {
    en: { title: document.title, desc: metaDesc ? metaDesc.content : '' },
    ar: {
      title: 'Code & Canvas — تطوير الأعمال، بالتصميم',
      desc: 'تساعد Code & Canvas المؤسسات في المنطقة على النمو عبر مواءمة الهوية والتقنية والبيانات مع أهداف العمل — بنطاق واضح وتسليم على مراحل بمعالم محددة.',
    },
  };

  /* ------------------------------------------------------------------ */
  /*  CanvasOne ERP orbit — same module set as the /erp/ proposal        */
  /* ------------------------------------------------------------------ */
  const ORBIT = [
    ['wallet', 'Finance & Accounting', 'المالية والمحاسبة'],
    ['trend', 'Sales & CRM', 'المبيعات وإدارة العملاء'],
    ['cart', 'Procurement', 'المشتريات'],
    ['box', 'Inventory & Warehousing', 'المخازن والمستودعات'],
    ['factory', 'Manufacturing', 'التصنيع'],
    ['users', 'HR & Payroll', 'الموارد البشرية والرواتب'],
    ['store', 'Point of Sale', 'نقاط البيع'],
    ['kanban', 'Projects & Services', 'المشاريع والخدمات'],
    ['building', 'Fixed Assets', 'الأصول الثابتة'],
    ['receipt', 'E-Invoicing & Tax', 'الفوترة الإلكترونية والضرائب'],
    ['chart', 'Reports & BI', 'التقارير وذكاء الأعمال'],
    ['phone', 'Portals & Mobile', 'البوابات وتطبيق الجوال'],
  ];

  function renderOrbit() {
    const n = ORBIT.length;
    $('#orbitSpin').innerHTML = ORBIT
      .map(([ico, en, ar], i) => `<div class="orbit__node"><span style="--a:${(360 / n) * i}deg" data-tip="${esc(CC.lang === 'ar' ? ar : en)}">${icon(ico)}</span></div>`)
      .join('');
  }

  /* ------------------------------------------------------------------ */
  /*  Hero parallax (cursor glow / reveal / tilt are shared)             */
  /* ------------------------------------------------------------------ */
  function bindHeroParallax() {
    const dash = $('#dash');
    const chips = $$('.float-chip');
    if (!dash) return;
    CC.onFrame((p) => {
      if (scrollY >= innerHeight) return;
      const base = document.documentElement.dir === 'rtl' ? 8 : -8;
      dash.style.setProperty('--ry', `${base + p.nx * 10}deg`);
      dash.style.setProperty('--rx', `${6 - p.ny * 8}deg`);
      chips.forEach((c) => {
        const d = +c.dataset.depth || 1;
        c.style.transform = `translate(${p.nx * 18 * d}px, ${p.ny * 18 * d}px)`;
      });
    });
  }

  /* ------------------------------------------------------------------ */
  /*  Boot                                                               */
  /* ------------------------------------------------------------------ */
  CC.onLang((lang) => {
    const m = META[lang];
    document.title = m.title;
    if (metaDesc) metaDesc.content = m.desc;
    $$('[data-current-year]').forEach((el) => { el.textContent = String(new Date().getFullYear()); });
    renderOrbit();
  });

  bindHeroParallax();
  CC.boot();
})();
