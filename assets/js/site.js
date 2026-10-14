/* ==========================================================================
   Code & Canvas — shared site runtime (vanilla JS, no dependencies)
   Used by the homepage and the CanvasOne ERP proposal.

   What lives here:
     · language state (AR / EN, RTL / LTR) + persistence + switch animation
     · tiny i18n layer:  data-ar / data-ar-html / data-ar-label / data-ar-title
       (English is whatever the HTML says; Arabic is the attribute)
     · stroke icon set
     · preloader, scroll progress, sticky nav, active-link tracking, burger
     · reveal-on-scroll, count-up, pointer tilt, magnetic buttons, cursor glow
   Pages register a renderer with CC.onLang(fn) and then call CC.boot().
   ========================================================================== */
(() => {
  'use strict';

  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  const store = {
    get: (k) => { try { return localStorage.getItem(k); } catch { return null; } },
    set: (k, v) => { try { localStorage.setItem(k, v); } catch { /* private mode */ } },
  };
  const session = {
    get: (k) => { try { return sessionStorage.getItem(k); } catch { return null; } },
    set: (k, v) => { try { sessionStorage.setItem(k, v); } catch { /* private mode */ } },
  };

  /* ------------------------------------------------------------------ */
  /*  Icons (stroke, 24×24)                                              */
  /* ------------------------------------------------------------------ */
  const ICONS = {
    layers: '<path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/>',
    clock: '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    shield: '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    globe: '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/>',
    wallet: '<path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1"/><path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"/>',
    trend: '<path d="M22 7 13.5 15.5 8.5 10.5 2 17"/><path d="M16 7h6v6"/>',
    cart: '<circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/>',
    box: '<path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/>',
    factory: '<path d="M2 20a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8l-7 5V8l-7 5V4a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/><path d="M17 18h1"/><path d="M12 18h1"/><path d="M7 18h1"/>',
    users: '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    store: '<path d="m2 7 4.41-4.41A2 2 0 0 1 7.83 2h8.34a2 2 0 0 1 1.42.59L22 7"/><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><path d="M15 22v-4a2 2 0 0 0-2-2h-2a2 2 0 0 0-2 2v4"/><path d="M2 7h20"/><path d="M22 7v3a2 2 0 0 1-2 2 2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 16 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 12 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 8 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 4 12a2 2 0 0 1-2-2V7"/>',
    kanban: '<rect width="18" height="18" x="3" y="3" rx="2"/><path d="M8 7v7"/><path d="M12 7v4"/><path d="M16 7v9"/>',
    building: '<rect width="16" height="20" x="4" y="2" rx="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01M16 6h.01M12 6h.01M12 10h.01M12 14h.01M16 10h.01M16 14h.01M8 10h.01M8 14h.01"/>',
    receipt: '<path d="M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1Z"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/><path d="M12 17.5v-11"/>',
    chart: '<path d="M3 3v16a2 2 0 0 0 2 2h16"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/>',
    phone: '<rect width="14" height="20" x="5" y="2" rx="2"/><path d="M12 18h.01"/>',
    heart: '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/><path d="M3.22 12H9.5l.5-1 2 4.5 2-7 1.5 3.5h5.27"/>',
    crane: '<path d="M10 10V5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v5"/><path d="M14 6a6 6 0 0 1 6 6v3"/><path d="M4 15v-3a6 6 0 0 1 6-6"/><rect x="2" y="15" width="20" height="4" rx="1"/>',
    briefcase: '<path d="M16 20V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/><rect width="20" height="14" x="2" y="6" rx="2"/>',
    cup: '<path d="M10 2v2"/><path d="M14 2v2"/><path d="M16 8a1 1 0 0 1 1 1v8a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4V9a1 1 0 0 1 1-1h14a4 4 0 1 1 0 8h-1"/><path d="M6 2v2"/>',
    cloud: '<path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/>',
    lock: '<rect width="18" height="11" x="3" y="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    history: '<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M12 7v5l4 2"/>',
    database: '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14a9 3 0 0 0 18 0V5"/><path d="M3 12a9 3 0 0 0 18 0"/>',
    plug: '<path d="M12 22v-5"/><path d="M9 8V2"/><path d="M15 8V2"/><path d="M18 8v5a4 4 0 0 1-4 4h-4a4 4 0 0 1-4-4V8Z"/>',
    languages: '<path d="m5 8 6 6"/><path d="m4 14 6-6 2-3"/><path d="M2 5h12"/><path d="M7 2h1"/><path d="m22 22-5-10-5 10"/><path d="M14 18h6"/>',
    target: '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    package: '<path d="m7.5 4.27 9 5.15"/><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/>',
    sparkles: '<path d="M9.94 15.5A2 2 0 0 0 8.5 14.06l-6.14-1.58a.5.5 0 0 1 0-.96L8.5 9.94A2 2 0 0 0 9.94 8.5l1.58-6.14a.5.5 0 0 1 .96 0L14.06 8.5A2 2 0 0 0 15.5 9.94l6.14 1.58a.5.5 0 0 1 0 .96L15.5 14.06a2 2 0 0 0-1.44 1.44l-1.58 6.14a.5.5 0 0 1-.96 0z"/><path d="M20 3v4"/><path d="M22 5h-4"/>',
    check: '<path d="M20 6 9 17l-5-5"/>',
    x: '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    arrow: '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    arrowUp: '<path d="m5 12 7-7 7 7"/><path d="M12 19V5"/>',
    mail: '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    copy: '<rect width="14" height="14" x="8" y="8" rx="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>',
    printer: '<path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><path d="M6 9V3a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v6"/><rect x="6" y="14" width="12" height="8" rx="1"/>',
    calendar: '<path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/>',
    chat: '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
    grid: '<rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/>',
    search: '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    alert: '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
    flag: '<path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><path d="M4 22v-7"/>',
    award: '<circle cx="12" cy="8" r="6"/><path d="M15.48 12.89 17 22l-5-3-5 3 1.52-9.11"/>',
    link: '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
  };
  const icon = (name, cls = '') => `<svg class="ico ${cls}" viewBox="0 0 24 24" aria-hidden="true">${ICONS[name] || ''}</svg>`;

  /* Preloader mark (Code & Canvas icon, drawn on load) */
  const MARK = `<svg class="preloader__mark" viewBox="0 0 649.02 649.02" aria-hidden="true"> <path class="pl-a" d="m311.43,445.68c7.16,7.13,7.16,18.73,0,25.86-7.2,7.13-18.82,7.13-26.02,0l-5.11-5.08c-15.54-15.47-28.51-28.42-37.46-40.02-9.39-12.3-16.02-25.29-16.02-40.98s6.64-28.68,16.02-40.98c8.95-11.65,21.92-24.55,37.46-40.02l5.11-5.08c7.2-7.17,18.82-7.17,26.02,0,7.16,7.13,7.16,18.73,0,25.86l-4.24,4.17c-16.68,16.64-27.9,27.81-35.11,37.29-6.94,9-8.51,14.25-8.51,18.77s1.57,9.73,8.51,18.77c7.2,9.43,18.43,20.64,35.11,37.24l4.24,4.22Z"/><path class="pl-a" d="m433.64,272.37l-63.44,235.58c-2.62,9.78-12.71,15.56-22.49,12.95-9.82-2.61-15.63-12.65-13.01-22.42l63.44-235.53c2.62-9.78,12.71-15.56,22.49-12.95,9.82,2.61,15.63,12.65,13.01,22.38Z"/><path class="pl-a" d="m541.54,385.45c0,15.69-6.59,28.68-16.02,40.98-8.91,11.6-21.92,24.55-37.46,40.02l-5.11,5.08c-7.2,7.13-18.82,7.13-25.98,0-7.2-7.13-7.2-18.73,0-25.86l4.19-4.22c16.68-16.6,27.9-27.81,35.15-37.24,6.9-9.04,8.47-14.3,8.47-18.77s-1.57-9.78-8.47-18.77c-7.25-9.47-18.47-20.64-35.15-37.29l-4.19-4.17c-7.2-7.13-7.2-18.73,0-25.86,7.16-7.17,18.78-7.17,25.98,0l5.11,5.08c15.54,15.47,28.56,28.38,37.46,40.02,9.43,12.3,16.02,25.25,16.02,40.98Z"/><path class="pl-b" d="m384.18,649.02c-110.26,0-171.11-15.8-210.04-54.55-38.93-38.75-54.81-99.31-54.81-209.04s15.88-170.29,54.81-209.04c38.93-38.74,99.78-54.55,210.04-54.55s171.11,15.8,210.04,54.55c38.93,38.75,54.81,99.31,54.81,209.04s-15.88,170.29-54.81,209.04c-38.93,38.75-99.78,54.55-210.04,54.55Zm0-487.74c-185.24,0-225.23,39.8-225.23,224.16s39.99,224.16,225.23,224.16,225.23-39.8,225.23-224.16-39.99-224.16-225.23-224.16Z"/><path class="pl-c" d="m108.61,180.72H19.53c-10.79,0-19.53-8.7-19.53-19.44s8.75-19.44,19.53-19.44h89.08c10.79,0,19.53,8.7,19.53,19.44s-8.75,19.44-19.53,19.44Z"/><path class="pl-c" d="m158.95,130.63c-10.79,0-19.53-8.7-19.53-19.44V19.44c0-10.74,8.75-19.44,19.53-19.44s19.53,8.7,19.53,19.44v91.75c0,10.74-8.75,19.44-19.53,19.44Z"/></svg>`;

  Object.assign(ICONS, {
    arrowUpRight: '<path d="M7 7h10v10"/><path d="M7 17 17 7"/>',
    arrowDown: '<path d="M12 5v14"/><path d="m19 12-7 7-7-7"/>',
    phoneCall: '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    pin: '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    compass: '<circle cx="12" cy="12" r="10"/><path d="m16.24 7.76-2.12 6.36-6.36 2.12 2.12-6.36z"/>',
    pen: '<path d="M12 20h9"/><path d="M16.38 3.62a1 1 0 0 1 3 3L7.37 18.64a2 2 0 0 1-.86.5l-3.38.97a.5.5 0 0 1-.62-.62l.97-3.38a2 2 0 0 1 .5-.86z"/>',
    rocket: '<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/>',
    stethoscope: '<path d="M11 2v2"/><path d="M5 2v2"/><path d="M5 3H4a2 2 0 0 0-2 2v4a6 6 0 0 0 12 0V5a2 2 0 0 0-2-2h-1"/><path d="M8 15a6 6 0 0 0 12 0v-3"/><circle cx="20" cy="10" r="2"/>',
  });

  /* ------------------------------------------------------------------ */
  /*  Language                                                           */
  /* ------------------------------------------------------------------ */
  const LANGS = ['ar', 'en'];
  const pickLang = () => {
    const q = new URLSearchParams(location.search).get('lang');
    if (LANGS.includes(q)) return q;
    const saved = store.get('cc-lang') || store.get('c1-lang');
    if (LANGS.includes(saved)) return saved;
    return /^ar/i.test(navigator.language || '') ? 'ar' : 'en';
  };
  let lang = pickLang();
  const listeners = [];
  const frameCallbacks = [];
  const readyCallbacks = [];

  const t = (v) => (v && typeof v === 'object' && ('ar' in v || 'en' in v) ? v[lang] ?? v.ar : v ?? '');
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const num = (n, opts) => new Intl.NumberFormat(lang === 'ar' ? 'ar-EG' : 'en-US', opts).format(n);

  function splitWords(el, text) {
    el.innerHTML = text
      .split(/\s+/)
      .filter(Boolean)
      .map((w, i) => `<span class="w" style="--i:${i}">${esc(w)}</span>`)
      .join(' ');
  }

  /** English = the HTML as authored. Arabic = data-ar* attributes. */
  function applyI18n(root = document) {
    const useAr = lang === 'ar';
    $$('[data-ar],[data-ar-html]', root).forEach((el) => {
      if (!el.__en) el.__en = { text: el.textContent.trim(), html: el.innerHTML };
      if (el.hasAttribute('data-ar-html')) {
        el.innerHTML = useAr ? el.getAttribute('data-ar-html') : el.__en.html;
      } else {
        const txt = useAr ? el.getAttribute('data-ar') : el.__en.text;
        if (el.classList.contains('split')) splitWords(el, txt);
        else el.textContent = txt;
      }
    });
    [['data-ar-label', 'aria-label'], ['data-ar-title', 'title'], ['data-ar-alt', 'alt'], ['data-ar-placeholder', 'placeholder']].forEach(([src, dst]) => {
      $$(`[${src}]`, root).forEach((el) => {
        const key = `__en_${dst}`;
        if (el[key] === undefined) el[key] = el.getAttribute(dst) ?? '';
        el.setAttribute(dst, useAr ? el.getAttribute(src) : el[key]);
      });
    });
  }

  function bindIcons(root = document) {
    $$('[data-icon]', root).forEach((el) => {
      if (!el.querySelector(':scope > .ico')) el.insertAdjacentHTML('afterbegin', icon(el.dataset.icon));
    });
  }

  function applyLang(initial) {
    const d = document.documentElement;
    d.lang = lang;
    d.dir = lang === 'ar' ? 'rtl' : 'ltr';
    const btn = $('#langBtn');
    if (btn) {
      const label = lang === 'ar' ? 'Switch to English' : 'التبديل إلى العربية';
      btn.textContent = lang === 'ar' ? 'EN' : 'ع';
      btn.title = label;
      btn.setAttribute('aria-label', label);
    }
    applyI18n();
    listeners.forEach((fn) => fn(lang, initial));
    bindIcons();
  }

  function setLang(next) {
    if (next === lang || !LANGS.includes(next)) return;
    document.body.classList.add('is-switching');
    setTimeout(() => {
      lang = next;
      store.set('cc-lang', lang);
      const url = new URL(location.href);
      url.searchParams.set('lang', lang);
      history.replaceState(null, '', url);
      applyLang(false);
      refresh();
      $$('[data-reveal]').forEach((el) => {
        const r = el.getBoundingClientRect();
        if (r.top < innerHeight && r.bottom > 0) el.classList.add('is-in');
      });
      requestAnimationFrame(() => document.body.classList.remove('is-switching'));
    }, reduceMotion ? 0 : 280);
  }

  /* ------------------------------------------------------------------ */
  /*  Count-up, reveal, tilt, magnetic                                   */
  /* ------------------------------------------------------------------ */
  let revealIO;
  let countIO;

  function countUp(el) {
    if (el.dataset.done) return;
    el.dataset.done = '1';
    const target = parseFloat(el.dataset.count);
    const dec = +(el.dataset.decimals || 0);
    const suffix = el.dataset.suffix || '';
    const fmtOpts = { minimumFractionDigits: dec, maximumFractionDigits: dec };
    const fmt = (v) => (el.dataset.latin ? new Intl.NumberFormat('en-US', fmtOpts).format(v) : num(v, fmtOpts)) + suffix;
    if (reduceMotion) { el.textContent = fmt(target); return; }
    const dur = 1600 + Math.min(target, 2000) * 0.2;
    const t0 = performance.now();
    const tick = (now) => {
      const p = Math.min(1, (now - t0) / dur);
      const e = 1 - Math.pow(1 - p, 4);
      el.textContent = fmt(dec ? target * e : Math.round(target * e));
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }

  function observe() {
    if (!revealIO) {
      revealIO = new IntersectionObserver(
        (entries) => entries.forEach((e) => {
          if (!e.isIntersecting) return;
          e.target.classList.add('is-in');
          $$('[data-count]', e.target).forEach(countUp);
          revealIO.unobserve(e.target);
        }),
        { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
      );
      countIO = new IntersectionObserver(
        (entries) => entries.forEach((e) => { if (e.isIntersecting) { countUp(e.target); countIO.unobserve(e.target); } }),
        { threshold: 0.4 }
      );
    }
    $$('[data-reveal]:not(.is-in)').forEach((el) => revealIO.observe(el));
    $$('[data-count]:not([data-done])').filter((el) => !el.closest('[data-reveal]')).forEach((el) => countIO.observe(el));
  }

  function bindTilt() {
    if (!finePointer || reduceMotion) return;
    $$('[data-tilt]:not([data-tilt-bound])').forEach((el) => {
      el.dataset.tiltBound = '1';
      el.addEventListener('pointermove', (e) => {
        const r = el.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width;
        const y = (e.clientY - r.top) / r.height;
        el.style.setProperty('--mx', `${x * 100}%`);
        el.style.setProperty('--my', `${y * 100}%`);
        el.style.transform = `perspective(900px) rotateX(${(0.5 - y) * 6}deg) rotateY(${(x - 0.5) * 8}deg) translateY(-4px)`;
      });
      el.addEventListener('pointerleave', () => { el.style.transform = ''; });
    });
  }

  function bindMagnetic() {
    if (!finePointer || reduceMotion) return;
    $$('.magnetic:not([data-mag])').forEach((el) => {
      el.dataset.mag = '1';
      el.addEventListener('pointermove', (e) => {
        const r = el.getBoundingClientRect();
        const x = e.clientX - r.left - r.width / 2;
        const y = e.clientY - r.top - r.height / 2;
        el.style.transform = `translate(${x * 0.18}px, ${y * 0.28}px)`;
      });
      el.addEventListener('pointerleave', () => { el.style.transform = ''; });
    });
  }

  /** Call after a page renders new markup. */
  function refresh() {
    bindIcons();
    observe();
    bindTilt();
    bindMagnetic();
  }

  /* ------------------------------------------------------------------ */
  /*  Global effects: cursor glow, scroll progress, nav, timeline         */
  /* ------------------------------------------------------------------ */
  const pointer = { x: innerWidth / 2, y: innerHeight / 2, nx: 0, ny: 0 };

  function bindPointer() {
    if (!finePointer || reduceMotion) return;
    document.body.classList.add('has-pointer');
    const glow = $('#cursorGlow');
    let gx = pointer.x;
    let gy = pointer.y;
    addEventListener('pointermove', (e) => { pointer.x = e.clientX; pointer.y = e.clientY; }, { passive: true });
    const loop = () => {
      gx += (pointer.x - gx) * 0.12;
      gy += (pointer.y - gy) * 0.12;
      pointer.nx = pointer.x / innerWidth - 0.5;
      pointer.ny = pointer.y / innerHeight - 0.5;
      if (glow) glow.style.transform = `translate3d(${gx - 260}px, ${gy - 260}px, 0)`;
      frameCallbacks.forEach((fn) => fn(pointer));
      requestAnimationFrame(loop);
    };
    loop();
  }

  function bindScroll() {
    const nav = $('#nav');
    const bar = $('#scrollProgress');
    const toTop = $('.to-top--fixed');
    const onScroll = () => {
      const h = document.documentElement.scrollHeight - innerHeight;
      if (bar) bar.style.transform = `scaleX(${h > 0 ? scrollY / h : 0})`;
      nav?.classList.toggle('is-scrolled', scrollY > 20);
      toTop?.classList.toggle('is-visible', scrollY > 680);
      const tl = $('#timeline');
      const fill = $('#timelineFill');
      if (tl && fill) {
        const r = tl.getBoundingClientRect();
        fill.style.transform = `scaleY(${Math.min(1, Math.max(0, (innerHeight * 0.6 - r.top) / r.height))})`;
        $$('.step', tl).forEach((s) => {
          const dot = $('.step__dot', s);
          if (dot) s.classList.toggle('is-lit', dot.getBoundingClientRect().top < innerHeight * 0.6);
        });
      }
    };
    addEventListener('scroll', onScroll, { passive: true });
    addEventListener('resize', onScroll, { passive: true });
    onScroll();

    // Safety net: never leave content hidden if the observer misses a fast jump
    let sweepT = 0;
    const sweep = () => {
      sweepT = 0;
      if (!document.body.classList.contains('is-ready')) return;
      $$('[data-reveal]:not(.is-in)').forEach((el) => {
        if (el.getBoundingClientRect().top < innerHeight * 0.92) {
          el.classList.add('is-in');
          $$('[data-count]', el).forEach(countUp);
        }
      });
    };
    addEventListener('scroll', () => { if (!sweepT) sweepT = setTimeout(sweep, 180); }, { passive: true });

    // Active section link
    const links = $$('#navLinks a[href^="#"]');
    if (links.length) {
      const io = new IntersectionObserver(
        (entries) => entries.forEach((e) => {
          if (e.isIntersecting) links.forEach((a) => a.classList.toggle('is-active', a.getAttribute('href') === '#' + e.target.id));
        }),
        { rootMargin: '-45% 0px -50% 0px' }
      );
      links.forEach((a) => { const s = $(a.getAttribute('href')); if (s) io.observe(s); });
    }
  }

  function bindChrome() {
    $('#langBtn')?.addEventListener('click', () => setLang(lang === 'ar' ? 'en' : 'ar'));

    // Mark the current page in the shared header: <body data-nav="services"> ↔ <a data-key="services">
    const key = document.body.dataset.nav;
    if (key) $$('#navLinks a[data-key]').forEach((a) => { if (a.dataset.key === key) { a.classList.add('is-active'); a.setAttribute('aria-current', 'page'); } });

    const burger = $('#burger');
    const links = $('#navLinks');
    if (burger && links) {
      const close = () => { burger.setAttribute('aria-expanded', 'false'); links.classList.remove('is-open'); };
      burger.addEventListener('click', () => {
        const open = burger.getAttribute('aria-expanded') !== 'true';
        burger.setAttribute('aria-expanded', String(open));
        links.classList.toggle('is-open', open);
      });
      links.addEventListener('click', (e) => { if (e.target.closest('a')) close(); });
      document.addEventListener('keydown', (e) => { if (e.key === 'Escape') close(); });
      document.addEventListener('click', (e) => {
        if (links.classList.contains('is-open') && !links.contains(e.target) && !burger.contains(e.target)) close();
      });
    }
  }

  let toastTimer;
  function toast(msg) {
    const el = $('#toast');
    if (!el) return;
    el.textContent = msg;
    el.classList.add('is-on');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => el.classList.remove('is-on'), 2200);
  }

  /* ------------------------------------------------------------------ */
  /*  Preloader (first visit per browser session only)                   */
  /* ------------------------------------------------------------------ */
  function startPreloader() {
    const pre = $('#preloader');
    const body = document.body;
    // timers (not rAF) so a hidden / background tab can never stay stuck in the loading state
    const ready = () => setTimeout(() => {
      body.classList.remove('is-loading');
      body.classList.add('is-ready');
      readyCallbacks.forEach((fn) => fn());
    }, 60);
    if (!pre || document.documentElement.classList.contains('no-pre')) {
      pre?.remove();
      ready();
      return;
    }
    const [a, b] = (pre.dataset.word || 'Code &|Canvas').split('|');
    pre.innerHTML = `<div class="preloader__inner">${MARK}<div class="preloader__word"><span>${esc(a)}</span><b>${esc(b || '')}</b></div><div class="preloader__bar"><i></i></div><p class="preloader__text">${esc(lang === 'ar' ? pre.dataset.textAr || '' : pre.dataset.textEn || '')}</p></div>`;
    session.set('cc-pre', '1');

    let finished = false;
    const finish = () => {
      if (finished) return;
      finished = true;
      pre.classList.add('is-done');
      body.classList.remove('is-loading');
      body.classList.add('is-ready');
      setTimeout(() => pre.remove(), 1200);
      readyCallbacks.forEach((fn) => fn());
    };
    const minDelay = reduceMotion ? 0 : 1700;
    const t0 = performance.now();
    const go = () => setTimeout(finish, Math.max(0, minDelay - (performance.now() - t0)));
    (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(go);
    setTimeout(finish, 4000); // safety net
  }

  /* ------------------------------------------------------------------ */
  /*  Boot                                                               */
  /* ------------------------------------------------------------------ */
  function boot() {
    applyLang(true);
    refresh();
    bindChrome();
    bindPointer();
    bindScroll();
    startPreloader();
    document.documentElement.classList.remove('i18n-pending');
  }

  window.CC = {
    $, $$, esc, icon, ICONS, reduceMotion, finePointer,
    get lang() { return lang; },
    t, num, splitWords, setLang, toast, refresh, boot, countUp, pointer,
    onLang: (fn) => listeners.push(fn),
    onFrame: (fn) => frameCallbacks.push(fn),
    onReady: (fn) => readyCallbacks.push(fn),
  };
})();
