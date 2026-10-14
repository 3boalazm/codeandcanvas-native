/* Code & Canvas — interactive book reader (slide deck shell).
   ─────────────────────────────────────────────────────────────────────────
   Content source, in order:
     1. data-manifest  → /assets/books/<slug>/manifest.json
        { "parts":[{ "title":"…", "slides":[{ "kicker":"…", "title":"…", "html":"…" }] }], "free_parts": 2 }
        (publish this file for buyers only — e.g. behind your auth proxy)
     2. the inline <script data-reader-sample> JSON (free preview built from the
        public landing page copy) when the manifest is missing (404).
   Access: slides beyond `free_parts` are gated unless the book id is in the
   local `cc-library` (set by the demo checkout) — swap for a real entitlement
   check when the backend exists. Keyboard: ← → Home End, F = fullscreen. */
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const root = $('[data-reader]');
  if (!root) return;
  const slug = root.dataset.reader;
  const stage = $('[data-slide]', root), parts = $('[data-parts]', root), thumbs = $('[data-thumbs]', root);
  const counter = $('[data-counter]', root), gate = $('[data-gate]', root), notes = $('[data-notes]', root);
  const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  let deck = [], idx = 0, freeUntil = Infinity;
  const owned = () => { try { return JSON.parse(localStorage.getItem('cc-library') || '[]').includes(slug); } catch { return false; } };

  function fromSample(sample) {
    const slides = [];
    slides.push({ part: 0, kicker: sample.author, title: sample.title, html: `<p>${esc(sample.title_en)}</p><p>معاينة مجانية — استخدم الأسهم للتنقل.</p>` });
    (sample.preview || []).forEach((c, i) => {
      slides.push({ part: i + 1, kicker: c.sub, title: `${c.k} · ${c.title}`, html: `<p>${esc(c.p)}</p>${c.q ? `<p><em>${esc(c.q)}</em></p>` : ''}${c.chips && c.chips.length ? `<ul>${c.chips.map((x) => `<li>${esc(x)}</li>`).join('')}</ul>` : ''}` });
    });
    const total = sample.parts_total || slides.length;
    for (let i = slides.length; i < Math.max(total, slides.length); i++) slides.push({ part: i, kicker: 'محتوى الكتاب', title: `الجزء ${i}`, html: '<p>يُفتح بعد الشراء.</p>', locked: true });
    const names = ['الغلاف'].concat((sample.preview || []).map((c) => `${c.k} · ${c.title}`));
    while (names.length < slides.length) names.push(`الجزء ${names.length}`);
    return { slides, names, free: Math.min(3, slides.length) };
  }

  function fromManifest(m) {
    const slides = [], names = [];
    (m.parts || []).forEach((p, pi) => {
      names.push(p.title);
      (p.slides || []).forEach((s) => slides.push({ part: pi, kicker: s.kicker || p.title, title: s.title, html: s.html || '' }));
    });
    return { slides, names, free: slides.filter((s) => s.part < (m.free_parts ?? 1)).length };
  }

  function render() {
    const s = deck[idx];
    const locked = !owned() && (idx >= freeUntil || s.locked);
    stage.innerHTML = `<span class="slide__kicker">${esc(s.kicker)}</span><h2>${esc(s.title)}</h2>${locked ? '<p>🔒 هذا الجزء متاح بعد الشراء.</p>' : s.html}`;
    gate.hidden = !locked;
    counter.textContent = `${idx + 1} / ${deck.length}`;
    parts.querySelectorAll('button').forEach((b) => b.classList.toggle('is-active', +b.dataset.part === s.part));
    thumbs.querySelectorAll('button').forEach((b, i) => b.classList.toggle('is-active', i === idx));
    thumbs.querySelector('.is-active')?.scrollIntoView({ block: 'nearest', inline: 'center', behavior: 'smooth' });
    try { localStorage.setItem(`cc-reader-${slug}`, String(idx)); } catch { /* ignore */ }
  }

  function go(n) { idx = Math.max(0, Math.min(deck.length - 1, n)); render(); }

  function mount(data) {
    deck = data.slides; freeUntil = data.free;
    parts.innerHTML = data.names.map((n, i) => `<button type="button" data-part="${i}" class="${!owned() && deck.findIndex((s) => s.part === i) >= freeUntil ? 'is-locked' : ''}"><i>${String(i + 1).padStart(2, '0')}</i><span>${esc(n)}</span></button>`).join('');
    thumbs.innerHTML = deck.map((_, i) => `<button type="button" aria-label="${i + 1}">${i + 1}</button>`).join('');
    parts.addEventListener('click', (e) => { const b = e.target.closest('button'); if (b) go(deck.findIndex((s) => s.part === +b.dataset.part)); });
    thumbs.addEventListener('click', (e) => { const b = e.target.closest('button'); if (b) go([...thumbs.children].indexOf(b)); });
    let start = 0; try { start = +localStorage.getItem(`cc-reader-${slug}`) || 0; } catch { /* ignore */ }
    go(start);
  }

  $('[data-prev]', root).addEventListener('click', () => go(idx + (document.documentElement.dir === 'rtl' ? 1 : -1)));
  $('[data-next]', root).addEventListener('click', () => go(idx + (document.documentElement.dir === 'rtl' ? -1 : 1)));
  $('[data-fullscreen]', root).addEventListener('click', () => { root.classList.toggle('is-fullscreen'); if (root.classList.contains('is-fullscreen') && root.requestFullscreen) root.requestFullscreen().catch(() => {}); else if (document.fullscreenElement) document.exitFullscreen(); });
  root.querySelectorAll('[data-notes-toggle]').forEach((b) => b.addEventListener('click', () => { notes.hidden = !notes.hidden; }));
  const ta = $('[data-notes-text]', root);
  if (ta) { try { ta.value = localStorage.getItem(`cc-notes-${slug}`) || ''; } catch { /* ignore */ } ta.addEventListener('input', () => { try { localStorage.setItem(`cc-notes-${slug}`, ta.value); } catch { /* ignore */ } }); }
  document.addEventListener('keydown', (e) => {
    if (e.target.matches('textarea, input')) return;
    if (e.key === 'ArrowRight') go(idx + 1); else if (e.key === 'ArrowLeft') go(idx - 1);
    else if (e.key === 'Home') go(0); else if (e.key === 'End') go(deck.length - 1);
    else if (e.key.toLowerCase() === 'f') $('[data-fullscreen]', root).click();
  });

  const sample = (() => { try { return JSON.parse($('[data-reader-sample]')?.textContent || '{}'); } catch { return {}; } })();
  fetch(root.dataset.manifest, { cache: 'no-store' })
    .then((r) => (r.ok ? r.json() : Promise.reject(r.status)))
    .then((m) => mount(fromManifest(m)))
    .catch(() => mount(fromSample(sample)));
})();
