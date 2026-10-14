/* Code & Canvas — shop shell (no backend).
   ─────────────────────────────────────────────────────────────────────────
   · Cart lives in localStorage under `cc-cart` → [{id,title,title_ar,price,currency,qty}]
   · [data-add] buttons add an item; [data-cart-count] badges show the quantity.
   · /cart/   renders into [data-cart]            · /checkout/ renders [data-summary]
   · /account/ renders the library from `cc-library` (ids unlocked after purchase).
   INTEGRATION: replace `checkout()` with your payment provider (Moyasar / Tap /
   Paymob / Stripe) — the function receives the cart + the validated form data. */
(() => {
  'use strict';
  const KEY = 'cc-cart', LIB = 'cc-library';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const ar = () => document.documentElement.lang === 'ar';
  const t = (en, a) => (ar() ? a : en);
  const toast = (m) => (window.CC && CC.toast ? CC.toast(m) : console.log(m));
  const fmt = (n, c = 'SAR') => `${n.toLocaleString('en-US')} ${c}`;

  const load = () => { try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch { return []; } };
  const save = (cart) => { localStorage.setItem(KEY, JSON.stringify(cart)); render(); };
  const total = (cart) => cart.reduce((s, i) => s + i.price * i.qty, 0);
  const library = () => { try { return JSON.parse(localStorage.getItem(LIB) || '[]'); } catch { return []; } };

  function add(btn) {
    const cart = load();
    const id = btn.dataset.add;
    const hit = cart.find((i) => i.id === id);
    if (hit) hit.qty = 1; // books are single-licence items
    else cart.push({ id, title: btn.dataset.title, title_ar: btn.dataset.titleAr || btn.dataset.title, price: +btn.dataset.price || 0, currency: btn.dataset.currency || 'SAR', qty: 1 });
    if (window.CC && CC.track) CC.track('add-to-cart', { id, price: +btn.dataset.price || 0 });
    save(cart);
    toast(t('Added to cart', 'تمت الإضافة إلى السلة'));
    btn.classList.add('is-done');
    setTimeout(() => btn.classList.remove('is-done'), 1200);
  }

  function renderBadges(cart) {
    const n = cart.reduce((s, i) => s + i.qty, 0);
    $$('[data-cart-count]').forEach((b) => { b.textContent = n; b.hidden = n === 0; });
  }

  function renderCart(cart) {
    const root = $('[data-cart]');
    if (!root) return;
    const empty = $('[data-cart-empty]');
    const table = $('[data-cart-table]');
    if (!cart.length) { if (empty) empty.hidden = false; if (table) table.hidden = true; return; }
    if (empty) empty.hidden = true; if (table) table.hidden = false;
    const tb = $('tbody', root);
    tb.innerHTML = cart.map((i) => `
      <tr data-id="${i.id}">
        <td><div class="item"><div class="art art--violet"><span class="art__mark" style="font-size:22px">📘</span></div><div><b>${ar() ? i.title_ar : i.title}</b><small>${t('Digital book · lifetime access', 'كتاب رقمي · وصول دائم')}</small></div></div></td>
        <td><span class="qty"><button type="button" data-dec aria-label="−">−</button><output>${i.qty}</output><button type="button" data-inc aria-label="+">+</button></span></td>
        <td class="price" dir="ltr">${fmt(i.price * i.qty, i.currency)}</td>
        <td><button class="btn btn--ghost btn--sm" type="button" data-remove>${t('Remove', 'إزالة')}</button></td>
      </tr>`).join('');
    $$('[data-cart-total]').forEach((el) => { el.textContent = fmt(total(cart)); });
  }

  function renderSummary(cart) {
    const box = $('[data-summary]');
    if (!box) return;
    const list = $('[data-summary-items]', box);
    if (list) list.innerHTML = cart.length ? cart.map((i) => `<div><span>${ar() ? i.title_ar : i.title} × ${i.qty}</span><b>${fmt(i.price * i.qty, i.currency)}</b></div>`).join('') : `<div><span>${t('Your cart is empty.', 'سلتك فارغة.')}</span></div>`;
    $$('[data-cart-total]').forEach((el) => { el.textContent = fmt(total(cart)); });
    const pay = $('[data-pay]');
    if (pay) pay.disabled = !cart.length;
  }

  function renderLibrary() {
    const root = $('[data-library]');
    if (!root) return;
    const ids = library();
    const empty = $('[data-library-empty]');
    if (!ids.length) { if (empty) empty.hidden = false; root.hidden = true; return; }
    root.hidden = false; if (empty) empty.hidden = true;
    root.innerHTML = ids.map((id) => `<a class="card glass book-card" href="/books/${id}/read/"><span class="card__icon">📘</span><h3>${id.replace(/-/g, ' ')}</h3><p>${t('Open in the reader →', 'افتح في القارئ ←')}</p></a>`).join('');
  }

  function render() {
    const cart = load();
    renderBadges(cart); renderCart(cart); renderSummary(cart); renderLibrary(); renderOrder();
  }

  /* INTEGRATION POINT — payment provider */
  async function checkout(cart, data) {
    // Demo flow: pretend the payment succeeded, unlock the books locally.
    const lib = new Set(library());
    cart.forEach((i) => lib.add(i.id));
    localStorage.setItem(LIB, JSON.stringify([...lib]));
    localStorage.removeItem(KEY);
    const now = new Date();
    const order = {
      id: `CC-${now.getFullYear().toString().slice(2)}${String(now.getMonth() + 1).padStart(2, '0')}${String(now.getDate()).padStart(2, '0')}-${Math.random().toString(36).slice(2, 6).toUpperCase()}`,
      date: now.toISOString(), name: data.name || data.first_name || '', email: data.email || '', pay: data.pay || 'card',
      items: cart, subtotal: total(cart), total: total(cart), currency: cart[0]?.currency || 'SAR',
    };
    sessionStorage.setItem('cc-last-order', JSON.stringify(order));
    if (window.CC && CC.track) CC.track('checkout', { id: order.id, total: order.total, currency: order.currency, pay: order.pay, items: cart.length });
    sessionStorage.setItem('cc-demo-note', t(`Payment integration pending — books unlocked in demo mode.`, `تكامل الدفع قيد التجهيز — فُتحت الكتب في وضع العرض.`));
    location.href = '/thank-you/';
  }

  /* /thank-you/ — order summary from the session (no backend) */
  function renderOrder() {
    const root = $('[data-order]');
    if (!root) return;
    let order = null;
    try { order = JSON.parse(sessionStorage.getItem('cc-last-order') || 'null'); } catch { order = null; }
    const set = (sel, v) => { const el = $(sel, root); if (el) el.textContent = v; };
    const note = $('[data-order-note]', root);
    if (!order) { if (note) note.hidden = false; set('[data-order-name]', t('friend', 'صديقنا')); return; }
    const PAY = { card: ['Credit card / mada', 'بطاقة ائتمان / مدى'], transfer: ['Bank transfer', 'تحويل بنكي'], wallet: ['E-wallet (Egypt)', 'محفظة إلكترونية (مصر)'] };
    set('[data-order-name]', (order.name || order.email.split('@')[0] || t('friend', 'صديقنا')).split(' ')[0]);
    set('[data-order-id]', order.id);
    set('[data-order-date]', new Date(order.date).toLocaleDateString(ar() ? 'ar-EG' : 'en-GB', { year: 'numeric', month: 'short', day: 'numeric' }));
    set('[data-order-email]', order.email || '—');
    set('[data-order-pay]', (PAY[order.pay] || PAY.card)[ar() ? 1 : 0]);
    set('[data-order-subtotal]', fmt(order.subtotal, order.currency));
    set('[data-order-total]', fmt(order.total, order.currency));
    const items = $('[data-order-items]', root);
    if (items) items.innerHTML = order.items.map((i) => `<div><span>${ar() ? i.title_ar : i.title} × ${i.qty}</span><b>${fmt(i.price * i.qty, i.currency)}</b></div>`).join('');
  }

  document.addEventListener('click', (e) => {
    const add_ = e.target.closest('[data-add]');
    if (add_) { add(add_); return; }
    const row = e.target.closest('tr[data-id]');
    if (!row) return;
    const cart = load();
    const item = cart.find((i) => i.id === row.dataset.id);
    if (!item) return;
    if (e.target.closest('[data-inc]')) item.qty = Math.min(9, item.qty + 1);
    else if (e.target.closest('[data-dec]')) item.qty = Math.max(1, item.qty - 1);
    else if (e.target.closest('[data-remove]')) cart.splice(cart.indexOf(item), 1);
    else return;
    save(cart);
  });

  const form = $('form[data-checkout]');
  if (form) form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (window.CC && CC.validateForm && !CC.validateForm(form)) return;
    const data = Object.fromEntries(new FormData(form).entries());
    const cart = load();
    if (!cart.length) { toast(t('Your cart is empty.', 'سلتك فارغة.')); return; }
    checkout(cart, data);
  });

  if (window.CC && CC.onLang) CC.onLang(render);
  render();
})();
