/* Saved book shortlist, not a payment or entitlement system.
   Catalogue data is generated from pages_books.py. Stored values never set prices,
   titles, HTML or access rights. A real commerce release requires a trusted backend. */
(() => {
  'use strict';
  const { $, $$, esc } = CC;
  const KEY = 'cc-cart';
  const books = new Map((window.CC_BOOKS || []).filter(b => b.available).map(b => [b.id, b]));
  const t = (en, ar) => CC.lang === 'ar' ? ar : en;
  const title = b => CC.lang === 'ar' ? b.title_ar : b.title;
  const fmt = n => `${Number(n).toLocaleString('en-US')} SAR`;
  function load() {
    try {
      const raw = JSON.parse(localStorage.getItem(KEY) || '[]');
      if (!Array.isArray(raw)) return [];
      return [...new Set(raw.map(b => b?.id))].filter(id => books.has(id)).map(id => ({ ...books.get(id), qty: 1 }));
    } catch { return []; }
  }
  function save(cart) {
    try { localStorage.setItem(KEY, JSON.stringify(cart.map(b => ({ id: b.id, qty: 1 })))); }
    catch { CC.toast(t('Your browser could not save this list.', 'تعذر حفظ القائمة في هذا المتصفح.')); return false; }
    render(); return true;
  }
  const total = cart => cart.reduce((sum, b) => sum + b.price, 0);
  function render() {
    const cart = load();
    $$('[data-cart-count], [data-cart-count-tile], [data-library-count]').forEach(el => { el.textContent = cart.length; if (el.hasAttribute('data-cart-count')) el.hidden = !cart.length; });
    $$('[data-cart-total]').forEach(el => { el.textContent = fmt(total(cart)); });
    const empty = $('[data-cart-empty]'), table = $('[data-cart-table]');
    if (empty) empty.hidden = !!cart.length;
    if (table) table.hidden = !cart.length;
    const rows = $('[data-cart] tbody');
    if (rows) rows.innerHTML = cart.map(b => `<tr data-id="${esc(b.id)}"><td><div class="item"><div><b>${esc(title(b))}</b><small>${esc(t('Digital book · one personal copy', 'كتاب رقمي · نسخة شخصية واحدة'))}</small></div></div></td><td>1</td><td class="price" dir="ltr">${fmt(b.price)}</td><td><button class="btn btn--ghost btn--sm" type="button" data-remove aria-label="${esc(t('Remove ', 'إزالة ') + title(b))}">${esc(t('Remove', 'إزالة'))}</button></td></tr>`).join('');
    const summary = $('[data-summary-items]');
    if (summary) summary.innerHTML = cart.length ? cart.map(b => `<div><span>${esc(title(b))}</span><b>${fmt(b.price)}</b></div>`).join('') : `<p>${esc(t('No books saved yet.', 'لم تحفظ أي كتب بعد.'))}</p>`;
    const submit = $('[data-pay]'); if (submit) submit.disabled = !cart.length;
    const library = $('[data-library]'), libraryEmpty = $('[data-library-empty]');
    if (libraryEmpty) libraryEmpty.hidden = !!cart.length;
    if (library) {
      library.hidden = !cart.length;
      library.innerHTML = cart.map(b => `<a class="card glass book-card" href="/books/${esc(b.id)}/read/"><h3>${esc(title(b))}</h3><p>${esc(t('Read the free preview →', 'اقرأ المعاينة المجانية ←'))}</p></a>`).join('');
    }
  }
  document.addEventListener('click', e => {
    const add = e.target.closest('[data-add]');
    if (add) {
      const b = books.get(add.dataset.add); if (!b) return;
      const cart = load(); if (!cart.some(x => x.id === b.id)) cart.push(b);
      if (!save(cart)) return;
      CC.track('save-book', { id: b.id });
      CC.toast(t('Saved. Find your shortlist in the library.', 'تم الحفظ. تجد قائمتك في المكتبة.')); return;
    }
    const remove = e.target.closest('[data-remove]');
    if (remove) { const id = remove.closest('[data-id]').dataset.id; if (save(load().filter(b => b.id !== id))) CC.track('remove-book', { id }); }
  });
  const form = $('form[data-checkout]');
  form?.addEventListener('submit', async e => {
    e.preventDefault();
    if (form.dataset.submitting || !CC.validateForm(form)) return;
    const cart = load(); if (!cart.length) return;
    const button = $('[data-pay]', form); form.dataset.submitting = 'true'; button.disabled = true;
    CC.track('form-attempt', { form: 'books' });
    try {
      const fields = Object.fromEntries(new FormData(form));
      await CC.submitContact(form, { name: fields.name, email: fields.email, phone: fields.phone || '', consent: fields.consent,
        inquiry: 'Book availability', message: cart.map(b => `${b.id}: ${title(b)}`).join('\n') });
    } finally { delete form.dataset.submitting; button.disabled = !load().length; }
  });
  addEventListener('storage', e => { if (e.key === KEY || e.key === null) render(); });
  CC.onLang(render); render();
})();
