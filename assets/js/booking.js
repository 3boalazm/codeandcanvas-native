/* ==========================================================================
   /book/ — first-party scheduler UI. Vanilla JS, no dependencies.
   Contract: GET  /api/booking/slots  → { dates, date, slots:[{time,available}] }
             POST /api/booking        → { accepted:true, id, calendarUrl, … }
   Any failure keeps the inputs and offers an explicit manual hand-off. A click
   is never reported as a confirmed booking.
   ========================================================================== */
(() => {
  'use strict';
  const { $, $$ } = CC;
  const cfg = window.CC_CONFIG || {};
  const form = $('#book-form');
  if (!form) return;

  const ar = () => CC.lang === 'ar';
  const L = (en, a) => (ar() ? a : en);
  const dateEl = $('#b-date'), slotsEl = $('#b-slots'), timeEl = $('#b-time');
  const statusEl = $('#b-status'), confirmEl = $('#b-confirm'), submitEl = $('#b-submit');
  const specialtyEl = $('#b-specialty'), tzEl = $('#b-tz');
  // Preselect the visitor's zone when it is one of the two markets we publish.
  try {
    const zone = Intl.DateTimeFormat().resolvedOptions().timeZone || '';
    const guess = /Riyadh|Asia\/(?:Riyadh|Qatar|Bahrain|Kuwait|Dubai|Aden)/.test(zone) ? 'AST'
      : /Cairo|Africa\/Cairo/.test(zone) ? 'EET' : '';
    if (guess && [...tzEl.options].some((o) => o.value === guess)) tzEl.value = guess;
  } catch { /* keep the published default */ }
  const params = new URLSearchParams(location.search);
  const specialtyParam = params.get('specialty');
  const serviceParam = (params.get('service') || '').toUpperCase();
  if (specialtyParam && [...specialtyEl.options].some((o) => o.value === specialtyParam)) specialtyEl.value = specialtyParam;
  if (/^(AB|MA|HC|CC)-\d{2}$/.test(serviceParam)) {
    const hidden = document.createElement('input');
    hidden.type = 'hidden'; hidden.name = 'service'; hidden.value = serviceParam;
    form.appendChild(hidden);
    const inq = document.createElement('input');
    inq.type = 'hidden'; inq.name = 'inquiry'; inq.value = serviceParam;
    form.appendChild(inq);
  }

  const setStatus = (html, ok = false) => {
    statusEl.className = `form__status ${ok ? 'is-ok' : 'is-err'}`;
    statusEl.innerHTML = `${CC.icon(ok ? 'check' : 'alert')}<div>${html}</div>`;
  };
  const manual = () => `<p>${L('We could not confirm the booking automatically.', 'لم نتمكن من تأكيد الحجز آليًا.')}</p><p><a href="https://wa.me/966545520750?text=${encodeURIComponent(L('I would like to book a 30-minute discovery call.', 'أرغب في حجز مكالمة استكشافية 30 دقيقة.'))}" target="_blank" rel="noopener">WhatsApp</a> · <a href="mailto:info@codeandcanvas.net?subject=Discovery%20call">info@codeandcanvas.net</a></p><p>${L('Nothing was reserved yet — please finish the request in your chosen app.', 'لم يُحجز شيء بعد — أكمل الطلب في التطبيق الذي تختاره.')}</p>`;

  const fmtDate = (iso) => {
    try {
      const d = new Date(iso + 'T12:00:00Z');
      return new Intl.DateTimeFormat(ar() ? 'ar' : 'en-GB', { weekday: 'short', day: 'numeric', month: 'short', timeZone: 'UTC' }).format(d);
    } catch { return iso; }
  };
  const setStep = (n) => $$('[data-step]').forEach((li) => li.classList.toggle('is-active', Number(li.dataset.step) <= n));

  let days = [];
  let lastSlots = [];
  async function loadDays() {
    try {
      const res = await fetch(cfg.slotsEndpoint || '/api/booking/slots', { headers: { Accept: 'application/json' } });
      if (!res.ok) throw new Error('slots unavailable');
      const data = await res.json();
      days = data.dates || [];
      if (!days.length) throw new Error('no dates');
      const placeholder = CC.esc(L('Choose a day', 'اختر يومًا'));
      dateEl.innerHTML = `<option value="">${placeholder}</option>` +
        days.map((d) => `<option value="${d}">${CC.esc(fmtDate(d))}</option>`).join('');
      if (days.length) { dateEl.value = days[0]; await loadSlots(days[0]); }
      setStep(1);
    } catch {
      dateEl.innerHTML = `<option value="">${CC.esc(L('Scheduler unavailable', 'جدول المواعيد غير متاح'))}</option>`;
      slotsEl.innerHTML = `<p class="field__hint">${CC.esc(L('The live scheduler is not reachable right now. You can still request a call manually.', 'جدول المواعيد غير متاح حاليًا. يمكنك طلب مكالمة يدويًا.'))}</p>`;
      setStatus(manual());
    }
  }
  async function loadSlots(date) {
    timeEl.value = '';
    setStep(2);
    try {
      const url = new URL(cfg.slotsEndpoint || '/api/booking/slots', location.origin);
      url.searchParams.set('date', date);
      /* The schedule is published in both office timezones; asking the API for
         the visitor's choice means the labels they read are the ones stored. */
      if (tzEl?.value) url.searchParams.set('timezone', tzEl.value);
      const res = await fetch(url, { headers: { Accept: 'application/json' } });
      if (!res.ok) throw new Error('slots unavailable');
      const data = await res.json();
      lastSlots = data.slots || [];
      const list = lastSlots;
      if (!list.length) { slotsEl.innerHTML = `<p class="field__hint">${CC.esc(L('No slots on this day.', 'لا مواعيد في هذا اليوم.'))}</p>`; return; }
      const tzLabel = tzEl?.value || 'AST';
      slotsEl.innerHTML = list.map((s) => `<button class="slot" type="button" data-time="${s.time}" aria-pressed="false"${s.available ? '' : ' disabled'} aria-label="${CC.esc(s.time + ' ' + tzLabel)}">${CC.esc(s.time)}<small>${CC.esc(tzLabel)}</small></button>`).join('');
    } catch {
      slotsEl.innerHTML = `<p class="field__hint">${CC.esc(L('Slots could not be loaded. Try again or request a call manually.', 'تعذّر تحميل المواعيد. حاول مجددًا أو اطلب مكالمة يدويًا.'))}</p>`;
    }
  }
  dateEl?.addEventListener('change', () => { if (dateEl.value) loadSlots(dateEl.value); });
  tzEl?.addEventListener('change', () => { if (dateEl.value) loadSlots(dateEl.value); });
  slotsEl?.addEventListener('click', (e) => {
    const b = e.target.closest('.slot'); if (!b || b.disabled) return;
    $$('.slot', slotsEl).forEach((x) => { x.classList.remove('is-selected'); x.setAttribute('aria-pressed', 'false'); });
    b.classList.add('is-selected'); b.setAttribute('aria-pressed', 'true');
    timeEl.value = b.dataset.time; setStep(2);
    CC.track('service_view', { from: 'booking-slot' });
  });

  let started = false;
  form.addEventListener('focusin', () => {
    if (started) return; started = true;
    CC.track('form_start', { form: 'booking' });
  }, { passive: true });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (form.dataset.submitting === 'true') return;
    statusEl.innerHTML = '';
    if ($('#_hp', form)?.value || $('[name="_hp"]', form)?.value) return;
    const data = Object.fromEntries(new FormData(form).entries());
    data.lang = CC.lang;
    data.page = location.pathname;
    const missing = [];
    if (!data.specialty) missing.push(specialtyEl);
    if (!data.date) missing.push(dateEl);
    if (!data.time) missing.push(slotsEl);
    if (!data.name || !data.name.trim()) missing.push($('#b-name'));
    if (!/^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]{2,}$/.test(data.email || '')) missing.push($('#b-email'));
    if (!data.consent) missing.push($('#b-consent'));
    if (missing.length) {
      setStatus(`<strong>${CC.esc(L('Please complete the highlighted fields, choose a slot and confirm consent.', 'أكمل الحقول المطلوبة، واختر موعدًا، وأكّد الموافقة.'))}</strong>`);
      missing[0]?.focus?.();
      return;
    }
    form.dataset.submitting = 'true';
    submitEl.disabled = true; submitEl.classList.add('is-busy');
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), cfg.requestTimeoutMs || 12000);
    try {
      const endpoint = cfg.bookingEndpoint || '/api/booking';
      if (!endpoint.startsWith('/api/')) throw new Error('invalid endpoint');
      const res = await fetch(endpoint, {
        method: 'POST', credentials: 'same-origin', signal: controller.signal,
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(data),
      });
      const result = await res.json();
      if (!res.ok || result.accepted !== true) throw new Error(result.error || 'not accepted');
      CC.track('booking_confirmed', { id: result.id, service: serviceParam });
      CC.track('form_submit', { form: 'booking', id: result.id });
      setStep(3);
      form.hidden = true;
      confirmEl.hidden = false;
      $('#b-ref').textContent = `${L('Reference', 'المرجع')}: ${result.id}`;
      const rows = [
        [L('Specialty', 'التخصص'), specialtyEl.options[specialtyEl.selectedIndex].text],
        [L('Date', 'اليوم'), fmtDate(result.date)],
        [L('Time', 'الوقت'), `${result.time} · ${result.timezone}`],
        [L('Duration', 'المدة'), L('30 minutes', '30 دقيقة')],
        [L('With', 'مع'), L('A Code & Canvas founder', 'أحد مؤسسي Code & Canvas')],
      ];
      $('#b-summary').innerHTML = rows.map(([k, v]) => `<div><span>${CC.esc(k)}</span><b>${CC.esc(v)}</b></div>`).join('');
      $('#b-ics').href = result.calendarUrl || '#';
      if (result.duplicate) { setStatus(`<strong>${CC.esc(L('This booking was already recorded — nothing was duplicated.', 'هذا الحجز مسجّل بالفعل — لم يتكرر شيء.'))}</strong>`, true); }
      $('#b-confirm').scrollIntoView({ block: 'start', behavior: 'smooth' });
    } catch (err) {
      setStatus(`<strong>${CC.esc(L('We could not confirm the booking.', 'لم نتمكن من تأكيد الحجز.'))}</strong>${manual()}<p class="field__hint">${CC.esc(err.message === 'slot unavailable' ? L('That slot was just taken — please pick another.', ' هذا الموعد حُجز للتو — اختر موعدًا آخر.') : '')}</p>`);
      if (/slot unavailable/i.test(err.message)) loadSlots(data.date);
    } finally {
      clearTimeout(timer);
      delete form.dataset.submitting;
      submitEl.disabled = false; submitEl.classList.remove('is-busy');
    }
  });

  loadDays();
})();
