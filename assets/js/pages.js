/* ==========================================================================
   Code & Canvas — inner-page behaviour (vanilla JS, no dependencies)
   Shared runtime (language, icons, reveal, tilt, preloader…) lives in site.js.
   English is authored in the HTML; Arabic sits beside it in data-ar* attributes.

   Generic, markup-driven behaviours (nothing page-specific lives here):
     · <html data-title-ar data-desc-ar>   → per-language document title / description
     · .faq                                → accordion (one open item per list)
     · [data-tabs] / .tab[data-tab] / [data-panel]        → tabbed panels
     · [data-filter-group] / [data-filter] / [data-category] → card filters
     · form[data-form]                     → validation + submission (see forms section)
     · .toc                                → active heading tracking
     · [data-copy]                         → copy text to clipboard
     · [data-acct] / [data-acct-panel]     → account dashboard panels (UI shell)
   ========================================================================== */
(() => {
  'use strict';

  const { $, $$, esc } = CC;
  const root = document.documentElement;

  /* ------------------------------------------------------------------ */
  /*  Document metadata per language                                     */
  /* ------------------------------------------------------------------ */
  const metaDesc = $('meta[name="description"]');
  const META = {
    en: { title: document.title, desc: metaDesc ? metaDesc.content : '' },
    ar: { title: root.dataset.titleAr || document.title, desc: root.dataset.descAr || (metaDesc ? metaDesc.content : '') },
  };
  CC.onLang((lang) => {
    document.title = META[lang].title;
    if (metaDesc) metaDesc.content = META[lang].desc;
    $$('[data-current-year]').forEach((el) => { el.textContent = String(new Date().getFullYear()); });
    $$('.tabs').forEach(moveTabIndicator);
  });

  /* ------------------------------------------------------------------ */
  /*  FAQ accordion                                                      */
  /* ------------------------------------------------------------------ */
  $$('.faq').forEach((list) => {
    list.addEventListener('click', (e) => {
      const q = e.target.closest('.faq__q');
      if (!q || !list.contains(q)) return;
      const item = q.closest('.faq__item');
      const open = item.classList.contains('is-open');
      if (!list.hasAttribute('data-multi')) {
        $$('.faq__item', list).forEach((x) => { x.classList.remove('is-open'); $('.faq__q', x)?.setAttribute('aria-expanded', 'false'); });
      }
      item.classList.toggle('is-open', !open);
      q.setAttribute('aria-expanded', String(!open));
    });
  });

  /* ------------------------------------------------------------------ */
  /*  Tabs                                                               */
  /* ------------------------------------------------------------------ */
  function moveTabIndicator(tabs) {
    const ind = $('.tabs__ind', tabs);
    const active = $('.tab.is-active', tabs);
    if (!ind || !active) return;
    ind.style.width = `${active.offsetWidth}px`;
    ind.style.height = `${active.offsetHeight}px`;
    ind.style.transform = `translate(${active.offsetLeft - ind.offsetLeft}px, ${active.offsetTop - ind.offsetTop}px)`;
  }
  $$('[data-tabs]').forEach((tabs) => {
    const scope = tabs.dataset.tabs;
    const panels = $$(`[data-panel][data-scope="${scope}"]`);
    const activate = (key) => {
      $$('.tab', tabs).forEach((t) => { const on = t.dataset.tab === key; t.classList.toggle('is-active', on); t.setAttribute('aria-selected', String(on)); });
      panels.forEach((p) => { p.hidden = p.dataset.panel !== key; if (!p.hidden) CC.refresh(); });
      moveTabIndicator(tabs);
    };
    tabs.addEventListener('click', (e) => { const t = e.target.closest('.tab'); if (t) activate(t.dataset.tab); });
    const first = $('.tab.is-active', tabs) || $('.tab', tabs);
    if (first) activate(first.dataset.tab);
    addEventListener('resize', () => moveTabIndicator(tabs), { passive: true });
  });

  /* ------------------------------------------------------------------ */
  /*  Filters                                                            */
  /* ------------------------------------------------------------------ */
  $$('[data-filter-group]').forEach((group) => {
    const target = $(group.dataset.filterGroup);
    if (!target) return;
    const buttons = $$('[data-filter]', group);
    const items = $$('[data-category]', target);
    const apply = (key) => {
      buttons.forEach((b) => { const on = b.dataset.filter === key; b.classList.toggle('is-active', on); b.setAttribute('aria-pressed', String(on)); });
      items.forEach((it) => {
        const cats = (it.dataset.category || '').split(/\s+/);
        it.hidden = key !== 'all' && !cats.includes(key);
        if (!it.hidden) it.classList.add('is-in');
      });
      $$('[data-filter-empty]').forEach((el) => { el.hidden = items.some((it) => !it.hidden); });
    };
    group.addEventListener('click', (e) => { const b = e.target.closest('[data-filter]'); if (b) apply(b.dataset.filter); });
    const fromHash = location.hash.replace('#', '');
    if (fromHash && buttons.some((b) => b.dataset.filter === fromHash)) apply(fromHash);
  });

  /* ------------------------------------------------------------------ */
  /*  Forms                                                              */
  /*                                                                     */
  /*  <form data-form="contact" data-endpoint="https://…" data-whatsapp="966545520750" data-mail="info@…">
  /*    · data-endpoint  — optional JSON POST target (Formspree, Fluent Forms API, a Worker, …).
  /*                       Leave empty / "#" to use the WhatsApp + e-mail fallback only.
  /*    · data-form="demo" — UI shell (auth / cart / checkout): validates, then shows a
  /*                       "connect a backend" notice instead of sending anything.
  /* ------------------------------------------------------------------ */
  const t = (en, ar) => (CC.lang === 'ar' ? ar : en);

  function validate(form) {
    let ok = true;
    $$('.field', form).forEach((f) => {
      const input = $('input, select, textarea', f);
      if (!input) return;
      let valid = input.checkValidity();
      if (valid && input.dataset.match) { const other = $(input.dataset.match, form); valid = !other || other.value === input.value; }
      f.classList.toggle('is-invalid', !valid);
      input.setAttribute('aria-invalid', String(!valid));
      if (!valid && ok) { input.focus(); ok = false; }
    });
    return ok;
  }

  if (window.CC) CC.validateForm = validate;

  function serialize(form) {
    const data = {};
    new FormData(form).forEach((v, k) => { if (k !== '_hp') data[k] = typeof v === 'string' ? v.trim() : v; });
    return data;
  }

  function composeMessage(data) {
    const skip = new Set(['password', 'password2', 'consent']);
    return Object.entries(data)
      .filter(([k, v]) => v && !skip.has(k))
      .map(([k, v]) => `${k.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())}: ${v}`)
      .join('\n');
  }

  function showStatus(form, kind, html) {
    const box = $('.form__status', form) || form.appendChild(Object.assign(document.createElement('div'), { className: 'form__status' }));
    box.className = `form__status ${kind === 'ok' ? 'is-ok' : 'is-err'}`;
    box.innerHTML = `${CC.icon(kind === 'ok' ? 'check' : 'alert')}<div>${html}</div>`;
    box.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  }

  async function submitContact(form, data) {
    const endpoint = (form.dataset.endpoint || '').trim();
    const wa = (form.dataset.whatsapp || '').replace(/\D/g, '');
    const mail = form.dataset.mail || 'info@codeandcanvas.net';
    const subject = encodeURIComponent(form.dataset.subject || `Website inquiry — ${data.inquiry || 'General'}`);
    const bodyTxt = composeMessage(data);
    const waLink = wa ? `https://wa.me/${wa}?text=${encodeURIComponent(bodyTxt)}` : '';
    const mailLink = `mailto:${mail}?subject=${subject}&body=${encodeURIComponent(bodyTxt)}`;
    const fallback = `<p>${esc(t('You can also send the same message directly:', 'يمكنك أيضًا إرسال الرسالة نفسها مباشرة:'))}</p><p>${waLink ? `<a href="${waLink}" target="_blank" rel="noopener">WhatsApp</a> · ` : ''}<a href="${mailLink}">${esc(mail)}</a></p>`;

    if (endpoint && endpoint !== '#') {
      try {
        const res = await fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify({ ...data, page: location.href, lang: CC.lang }) });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        showStatus(form, 'ok', `<strong>${esc(t('Thank you — your message is in.', 'شكرًا لك — وصلتنا رسالتك.'))}</strong> ${esc(t('We reply within one business day (KSA / Egypt hours).', 'نرد خلال يوم عمل واحد (بتوقيت السعودية / مصر).'))}`);
        form.reset();
        return;
      } catch (err) {
        showStatus(form, 'err', `<strong>${esc(t('The form service did not respond.', 'لم تستجب خدمة النموذج.'))}</strong> ${fallback}`);
        return;
      }
    }
    // No endpoint configured → hand the message to WhatsApp (or e-mail) with the fields pre-filled.
    const target = waLink || mailLink;
    window.open(target, '_blank', 'noopener');
    showStatus(form, 'ok', `<strong>${esc(t('Opening your message…', 'جارٍ فتح رسالتك…'))}</strong> ${esc(t('If nothing opened, use one of these links:', 'إن لم يُفتح شيء، استخدم أحد هذين الرابطين:'))}${fallback}`);
  }

  function submitDemo(form) {
    const next = form.dataset.next;
    const note = form.dataset.note || t('UI shell — this action needs the backend connected (see README › Integration points).', 'واجهة فقط — هذا الإجراء يحتاج ربط الباك-إند (انظر README › Integration points).');
    if (next) {
      try { sessionStorage.setItem('cc-demo-note', note); } catch { /* ignore */ }
      location.href = next;
      return;
    }
    showStatus(form, 'ok', `<strong>${esc(t('Looks good.', 'تمام.'))}</strong> ${esc(note)}`);
    CC.toast(t('UI shell: no backend connected yet', 'واجهة فقط: لم يُربط الباك-إند بعد'));
  }


  /* ------------------------------------------------------------------ */
  /*  Booking hook — <section id="book" data-booking-url="https://calendly.com/…">  */
  /*  When a scheduler URL is set, every [data-book] button opens it.    */
  /* ------------------------------------------------------------------ */
  // Legacy WordPress deep-link: /about#book → booking card now lives on /contact/#book
  if (location.hash === '#book' && !$('#book')) location.replace('/contact/#book');
  const bookUrl = ($('#book')?.dataset.bookingUrl || '').trim();
  if (bookUrl) $$('[data-book]').forEach((a) => { a.href = bookUrl; a.target = '_blank'; a.rel = 'noopener'; });

  $$('form[data-form]').forEach((form) => {
    form.noValidate = true;
    $$('input, select, textarea', form).forEach((i) => i.addEventListener('input', () => { i.closest('.field')?.classList.remove('is-invalid'); i.removeAttribute('aria-invalid'); }));
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      if ($('[name="_hp"]', form)?.value) return; // honeypot
      if (!validate(form)) return;
      const btn = $('[type="submit"]', form);
      btn?.classList.add('is-busy');
      try {
        const data = serialize(form);
        if (form.dataset.form === 'contact') await submitContact(form, data);
        else submitDemo(form, data);
      } finally { btn?.classList.remove('is-busy'); }
    });
  });

  // Session note from a previous demo step (e.g. checkout → thank-you)
  try {
    const note = sessionStorage.getItem('cc-demo-note');
    const slot = $('[data-demo-note]');
    if (note && slot) { slot.textContent = note; slot.hidden = false; sessionStorage.removeItem('cc-demo-note'); }
  } catch { /* ignore */ }

  /* ------------------------------------------------------------------ */
  /*  Article table of contents                                          */
  /* ------------------------------------------------------------------ */
  const toc = $('.toc');
  if (toc) {
    const links = $$('a[href^="#"]', toc);
    const heads = links.map((a) => $(a.getAttribute('href'))).filter(Boolean);
    if (heads.length) {
      const io = new IntersectionObserver((entries) => entries.forEach((en) => {
        if (en.isIntersecting) links.forEach((a) => a.classList.toggle('is-active', a.getAttribute('href') === `#${en.target.id}`));
      }), { rootMargin: '-20% 0px -70% 0px' });
      heads.forEach((h) => io.observe(h));
    }
  }

  /* ------------------------------------------------------------------ */
  /*  Copy buttons                                                       */
  /* ------------------------------------------------------------------ */
  $$('[data-copy]').forEach((b) => b.addEventListener('click', async () => {
    try { await navigator.clipboard.writeText(b.dataset.copy); CC.toast(t('Copied', 'تم النسخ')); } catch { CC.toast(b.dataset.copy); }
  }));

  /* ------------------------------------------------------------------ */
  /*  Account dashboard panels (UI shell)                                */
  /* ------------------------------------------------------------------ */
  const acctNav = $('[data-acct]');
  if (acctNav) {
    const show = (key) => {
      $$('[data-acct-link]', acctNav).forEach((a) => a.classList.toggle('is-active', a.dataset.acctLink === key));
      $$('[data-acct-panel]').forEach((p) => p.classList.toggle('is-active', p.dataset.acctPanel === key));
      CC.refresh();
    };
    acctNav.addEventListener('click', (e) => { const a = e.target.closest('[data-acct-link]'); if (a) { e.preventDefault(); show(a.dataset.acctLink); history.replaceState(null, '', `#${a.dataset.acctLink}`); } });
    const initial = location.hash.replace('#', '');
    show($(`[data-acct-link="${initial}"]`, acctNav) ? initial : $('[data-acct-link]', acctNav)?.dataset.acctLink);
  }

  CC.boot();
})();
