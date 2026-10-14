/* ==========================================================================
   CanvasOne ERP proposal — rendering + page interactions (vanilla JS, no deps)
   Shared runtime (language, icons, reveal, tilt, preloader…) lives in site.js.
   ========================================================================== */
(() => {
  'use strict';

  const P = window.PROPOSAL;
  const { $, $$, esc, icon, t, num, reduceMotion } = CC;
  let lang = CC.lang;

  const get = (path) => path.split('.').reduce((o, k) => (o ? o[k] : undefined), P);
  const pad2 = (n) => (lang === 'ar' ? num(n, { minimumIntegerDigits: 2 }) : String(n).padStart(2, '0'));
  const moduleById = (id) => P.modules.find((m) => m.id === id);

  /* ------------------------------------------------------------------ */
  /*  State                                                              */
  /* ------------------------------------------------------------------ */
  const state = {
    module: 0,
    sector: 0,
    market: 0,
    compare: 'after',
    builder: { market: 'both', size: 'm', deploy: 'cloud', sector: 'retail', modules: new Set(['finance', 'einvoice', 'bi', ...P.sectors[0].modules]) },
  };

  /* ------------------------------------------------------------------ */
  /*  Static text binding                                                */
  /* ------------------------------------------------------------------ */
  function bindText() {
    $$('[data-t]').forEach((el) => {
      const v = t(get(el.dataset.t));
      if (el.classList.contains('split')) CC.splitWords(el, v);
      else el.textContent = v;
    });
    $$('[data-t-title]').forEach((el) => {
      const v = t(get(el.dataset.tTitle));
      el.title = v;
      el.setAttribute('aria-label', v);
    });
  }

  /* ------------------------------------------------------------------ */
  /*  Renderers                                                          */
  /* ------------------------------------------------------------------ */
  function renderHero() {
    $('#heroChips').innerHTML = P.hero.chips.map((c) => `<li>${icon('check')}${esc(t(c))}</li>`).join('');

    $('#dashKpis').innerHTML = P.hero.dash.kpis
      .map((k) => {
        const down = k.trend < 0;
        const trend = num(k.trend / 100, { style: 'percent', signDisplay: 'always', minimumFractionDigits: 1 });
        return `<div class="kpi"><p class="kpi__label">${esc(t(k.label))}</p>
          <p class="kpi__value" data-count="${k.value}" data-suffix="${esc(t(k.suffix))}" data-decimals="${String(k.value).includes('.') ? 1 : 0}">0</p>
          <span class="kpi__trend ${down ? 'down' : 'up'}">${trend}</span></div>`;
      })
      .join('');

    const inv = [
      ['INV-2041', true],
      ['INV-2040', true],
      ['INV-2039', false],
    ];
    $('#dashInv').innerHTML = inv
      .map(([no, ok]) => `<li><span class="inv__no">${no}</span><span class="inv__st ${ok ? '' : 'is-pending'}">${ok ? icon('check') : icon('clock')}${ok ? esc(t(P.hero.dash.cleared)) : '…'}</span></li>`)
      .join('');

    // chart bars (static shape)
    const bars = [38, 52, 46, 64, 58, 76, 70, 88, 82, 98];
    $('.chart__bars').innerHTML = bars
      .map((h, i) => `<rect x="${i * 30 + 6}" y="${120 - h}" width="18" height="${h}" rx="4" style="transition-delay:${0.4 + i * 0.06}s"/>`)
      .join('');
  }

  function renderStats() {
    $('#stats').innerHTML = P.stats
      .map((s) => {
        const prefix = s.prefix ? (lang === 'ar' ? s.prefix.replace(/\d/g, (d) => num(+d)) : s.prefix) : '';
        return `<div class="stat"><span class="stat__num">${prefix}<span data-count="${s.value}">0</span>${s.suffix || ''}</span><p class="stat__label">${esc(t(s.label))}</p></div>`;
      })
      .join('');
  }

  function renderMarquee() {
    const items = P.modules.map((m) => `<span class="marquee__item">${icon(m.icon)}${esc(t(m.name))}</span>`).join('');
    $('#marquee').innerHTML = items + items;
  }

  function renderChallenge() {
    $('#pains').innerHTML = P.challenge.pains
      .map(
        (p, i) => `<article class="card glass" data-reveal data-tilt style="--d:${i * 0.08}s">
          <span class="card__num">${pad2(i + 1)}</span>
          <div class="card__icon">${icon(p.icon)}</div>
          <h3>${esc(t(p.title))}</h3><p>${esc(t(p.text))}</p></article>`
      )
      .join('');
    renderCompare(false);
  }

  function renderCompare(animate = true) {
    const list = $('#compareList');
    const sw = $('#compareSwitch');
    const mode = state.compare;
    sw.dataset.mode = mode;
    $$('button', sw).forEach((b) => {
      const on = b.dataset.mode === mode;
      b.classList.toggle('is-active', on);
      b.setAttribute('aria-selected', on);
    });
    const draw = () => {
      list.dataset.mode = mode;
      list.innerHTML = P.challenge.compare.rows
        .map((r) => `<li><span class="mark">${icon(mode === 'after' ? 'check' : 'x')}</span><span class="txt">${esc(t(r[mode]))}</span></li>`)
        .join('');
    };
    if (!animate || reduceMotion) return draw();
    list.classList.add('is-swapping');
    setTimeout(() => {
      draw();
      list.classList.add('is-swapping');
      requestAnimationFrame(() => requestAnimationFrame(() => list.classList.remove('is-swapping')));
    }, 260);
  }

  function renderPlatform() {
    $('#platformPoints').innerHTML = P.platform.points.map((p) => `<li>${icon('check')}<span>${esc(t(p))}</span></li>`).join('');
    const n = P.modules.length;
    $('#orbitSpin').innerHTML = P.modules
      .map((m, i) => `<div class="orbit__node"><span style="--a:${(360 / n) * i}deg" data-tip="${esc(t(m.name))}">${icon(m.icon)}</span></div>`)
      .join('');
  }

  function renderModules() {
    $('#modGrid').innerHTML = P.modules
      .map(
        (m, i) => `<button class="mod-btn" role="tab" type="button" data-i="${i}" aria-selected="${i === state.module}" aria-controls="modPanel">
          <span class="mod-btn__idx">${pad2(i + 1)}</span>
          <span class="mod-btn__ico">${icon(m.icon)}</span>
          <span class="mod-btn__name">${esc(t(m.name))}</span></button>`
      )
      .join('');
    renderModulePanel(false);

    $('#modPrint').innerHTML = P.modules
      .map((m) => `<div class="pm"><h3>${esc(t(m.name))}</h3><p>${esc(t(m.desc))}</p><ul>${m.features.map((f) => `<li>${esc(t(f))}</li>`).join('')}</ul></div>`)
      .join('');
  }

  function renderModulePanel(animate = true) {
    const m = P.modules[state.module];
    $$('.mod-btn').forEach((b, i) => {
      b.classList.toggle('is-active', i === state.module);
      b.setAttribute('aria-selected', i === state.module);
      b.tabIndex = i === state.module ? 0 : -1;
    });
    const panel = $('#modPanel');
    panel.innerHTML = `<div class="${animate ? 'mp-anim' : ''}">
      <div class="mp__top"><span class="mp__icon">${icon(m.icon)}</span>
        <span class="mp__count"><b>${pad2(state.module + 1)}</b> / ${pad2(P.modules.length)}</span></div>
      <h3 class="mp__name">${esc(t(m.name))}</h3>
      <p class="mp__desc">${esc(t(m.desc))}</p>
      <ul class="mp__features">${m.features.map((f, i) => `<li style="--i:${i}">${icon('check')}<span>${esc(t(f))}</span></li>`).join('')}</ul>
      <div class="mp__outcome">${icon('award')}<div><small>${esc(t(P.modulesSection.outcomeLabel))}</small><strong>${esc(t(m.outcome))}</strong></div></div>
    </div>`;
  }

  function renderSectors() {
    $('#sectorTabs').innerHTML =
      P.sectors
        .map((s, i) => `<button class="tab" role="tab" type="button" data-i="${i}" aria-selected="${i === state.sector}">${icon(s.icon)}<span>${esc(t(s.name))}</span></button>`)
        .join('') + '<span class="tabs__ind" aria-hidden="true"></span>';
    renderSectorPanel(false);
  }

  function renderSectorPanel(animate = true) {
    const s = P.sectors[state.sector];
    const S = P.sectorsSection;
    $$('#sectorTabs .tab').forEach((b, i) => {
      b.classList.toggle('is-active', i === state.sector);
      b.setAttribute('aria-selected', i === state.sector);
    });
    moveIndicator();
    const panel = $('#sectorPanel');
    panel.classList.remove('sector-anim');
    panel.innerHTML = `
      <div class="sector__col sector__col--pain">
        <h3 class="sector__name">${icon(s.icon)}${esc(t(s.name))}</h3>
        <h4><i></i>${esc(t(S.painLabel))}</h4><p>${esc(t(s.pain))}</p>
      </div>
      <div class="sector__col sector__col--fix"><h4><i></i>${esc(t(S.fixLabel))}</h4><p>${esc(t(s.fix))}</p></div>
      <div class="sector__col sector__col--mods"><h4><i></i>${esc(t(S.modulesLabel))}</h4>
        <div class="pill-list">${s.modules.map((id) => { const m = moduleById(id); return `<span class="pill">${icon(m.icon)}${esc(t(m.name))}</span>`; }).join('')}</div>
      </div>`;
    if (animate) { void panel.offsetWidth; panel.classList.add('sector-anim'); }
  }

  function moveIndicator() {
    const wrap = $('#sectorTabs');
    const active = $('.tab.is-active', wrap);
    const ind = $('.tabs__ind', wrap);
    if (!active || !ind) return;
    ind.style.width = active.offsetWidth + 'px';
    ind.style.height = active.offsetHeight + 'px';
    ind.style.left = active.offsetLeft + 'px';
    ind.style.top = active.offsetTop + 'px';
  }

  function renderCompliance() {
    const C = P.compliance;
    $('#marketSwitch').innerHTML =
      C.markets.map((m, i) => `<button type="button" role="tab" data-i="${i}" aria-selected="${i === state.market}"><b>${m.flag}</b><small>${esc(t(m.name))}</small></button>`).join('') +
      '<span class="ms-thumb" aria-hidden="true"></span>';
    renderMarket();
  }

  function renderMarket() {
    const m = P.compliance.markets[state.market];
    const sw = $('#marketSwitch');
    sw.dataset.m = state.market;
    $$('button', sw).forEach((b, i) => {
      b.classList.toggle('is-active', i === state.market);
      b.setAttribute('aria-selected', i === state.market);
    });
    $('#complianceHeadline').innerHTML = `${icon('shield')}<span>${esc(t(m.headline))}</span>`;
    $('#complianceGrid').innerHTML = m.items
      .map((it, i) => `<div class="c-item" style="--i:${i}"><span class="c-item__n">${pad2(i + 1)}</span><h3>${esc(t(it.title))}</h3><p>${esc(t(it.text))}</p></div>`)
      .join('');
  }

  function renderTech() {
    $('#techGrid').innerHTML = P.tech.items
      .map((it, i) => `<article class="card glass" data-reveal data-tilt style="--d:${(i % 3) * 0.08}s"><div class="card__icon">${icon(it.icon)}</div><div><h3>${esc(t(it.title))}</h3><p>${esc(t(it.text))}</p></div></article>`)
      .join('');
  }

  function renderJourney() {
    const rail = '<span class="timeline__rail"><i id="timelineFill"></i></span>';
    $('#timeline').innerHTML =
      rail +
      P.journey.steps
        .map(
          (s, i) => `<li class="step" data-reveal>
            <span class="step__dot">${pad2(i + 1)}</span>
            <div class="step__card card glass" data-tilt style="grid-column:${i % 2 ? 2 : 1}">
              <span class="step__time">${icon('clock')}${esc(t(s.time))}</span>
              <h3>${esc(t(s.title))}</h3><p>${esc(t(s.text))}</p>
              <p class="step__deliv">${icon('flag')}<span>${esc(t(s.deliverable))}</span></p>
            </div></li>`
        )
        .join('');
  }

  function renderWhy() {
    $('#pillars').innerHTML = P.why.pillars
      .map(
        (p, i) => `<article class="card glass" data-reveal data-tilt style="--d:${i * 0.1}s">
          <span class="card__big">${pad2(i + 1)}</span>
          <div class="card__icon">${icon(p.icon)}</div><h3>${esc(t(p.title))}</h3><p>${esc(t(p.text))}</p></article>`
      )
      .join('');
    $('#promises').innerHTML = P.why.promises.map((p) => `<li>${icon('check')}<span>${esc(t(p))}</span></li>`).join('');
  }

  /* ----- Builder ----- */
  function renderBuilder() {
    const B = P.builder;
    const seg = (el, opts, key) => {
      $(el).innerHTML = opts.map((o) => `<button type="button" data-k="${key}" data-v="${o.id}" aria-pressed="${state.builder[key] === o.id}">${esc(t(o.label))}</button>`).join('');
    };
    seg('#bMarket', B.marketOpts, 'market');
    seg('#bSize', B.sizeOpts, 'size');
    seg('#bDeploy', B.deployOpts, 'deploy');
    $('#bSector').innerHTML = P.sectors
      .map((s) => `<button type="button" data-k="sector" data-v="${s.id}" aria-pressed="${state.builder.sector === s.id}">${icon(s.icon)}${esc(t(s.name))}</button>`)
      .join('');
    $('#bModules').innerHTML = P.modules
      .map((m) => `<button type="button" data-k="modules" data-v="${m.id}" aria-pressed="${state.builder.modules.has(m.id)}">${icon(m.icon)}${esc(t(m.name))}</button>`)
      .join('');
    renderSummary();
  }

  function estimateWeeks() {
    const n = state.builder.modules.size;
    const sizeAdd = { s: 0, m: 1, l: 3, xl: 5 }[state.builder.size];
    const marketAdd = state.builder.market === 'both' ? 1 : 0;
    const deployAdd = state.builder.deploy === 'onprem' ? 1 : 0;
    const low = Math.max(4, Math.round(3 + n * 0.55 + sizeAdd + marketAdd + deployAdd));
    const high = low + Math.max(2, Math.round(n * 0.3 + sizeAdd / 2));
    return [low, high];
  }

  function summaryText() {
    const B = P.builder;
    const b = state.builder;
    const label = (opts, id) => t(opts.find((o) => o.id === id).label);
    const sector = P.sectors.find((s) => s.id === b.sector);
    const [lo, hi] = estimateWeeks();
    const mods = [...b.modules].map((id) => '• ' + t(moduleById(id).name)).join('\n');
    return [
      `${t(B.mailSubject)}`,
      '',
      `${t(B.marketQ)}: ${label(B.marketOpts, b.market)}`,
      `${t(B.sizeQ)}: ${label(B.sizeOpts, b.size)}`,
      `${t(B.deployQ)}: ${label(B.deployOpts, b.deploy)}`,
      `${t(B.sectorQ)}: ${t(sector.name)}`,
      `${t(B.timeline)}: ${num(lo)}–${num(hi)} ${counted(hi, B.weeks, B.weeksFew)}`,
      '',
      `${t(B.modulesQ)} (${num(b.modules.size)}):`,
      mods,
    ].join('\n');
  }

  // Arabic counted nouns: 3–10 take the plural, 11+ the singular
  const counted = (n, many, few, one) => (n === 1 && one ? t(one) : lang === 'ar' && n >= 2 && n <= 10 ? t(few) : t(many));

  function renderSummary() {
    const B = P.builder;
    const b = state.builder;
    const label = (opts, id) => t(opts.find((o) => o.id === id).label);
    const sector = P.sectors.find((s) => s.id === b.sector);
    const [lo, hi] = estimateWeeks();
    const brand = P.brand;
    const wa = brand.whatsapp
      ? `<a class="btn btn--glass" target="_blank" rel="noopener" href="https://wa.me/${brand.whatsapp}?text=${encodeURIComponent(summaryText())}">${icon('chat')}<span>${esc(t(B.whatsapp))}</span></a>`
      : '';
    $('#builderSummary').innerHTML = `
      <h3 class="bs__title"><span>${esc(t(B.summaryTitle))}</span><span class="bs__count">${num(b.modules.size)} ${esc(counted(b.modules.size, B.selected, B.selectedFew, B.selectedOne))}</span></h3>
      <div class="bs__rows">
        <div class="bs__row"><span>${esc(t(B.marketQ))}</span><span>${esc(label(B.marketOpts, b.market))}</span></div>
        <div class="bs__row"><span>${esc(t(B.sizeQ))}</span><span>${esc(label(B.sizeOpts, b.size))}</span></div>
        <div class="bs__row"><span>${esc(t(B.deployQ))}</span><span>${esc(label(B.deployOpts, b.deploy))}</span></div>
        <div class="bs__row"><span>${esc(t(B.sectorQ))}</span><span>${esc(t(sector.name))}</span></div>
      </div>
      <div class="bs__mods">${[...b.modules].map((id) => `<span>${esc(t(moduleById(id).name))}</span>`).join('')}</div>
      <div class="bs__time"><small>${esc(t(B.timeline))}</small><span><b>${num(lo)}–${num(hi)}</b><em>${esc(counted(hi, B.weeks, B.weeksFew))}</em></span></div>
      <div class="bs__actions">
        <a class="btn btn--primary magnetic" id="sendMail" href="${mailHref()}">${icon('mail')}<span>${esc(t(B.send))}</span></a>
        ${wa}
        <button class="btn btn--glass" type="button" id="copySummary">${icon('copy')}<span>${esc(t(B.copy))}</span></button>
      </div>
      <p class="bs__note">${esc(t(B.note))}</p>`;
  }

  const mailHref = () => `mailto:${P.brand.email}?subject=${encodeURIComponent(t(P.builder.mailSubject))}&body=${encodeURIComponent(summaryText())}`;

  function renderFaq() {
    $('#faqList').innerHTML = P.faq
      .map(
        (f, i) => `<div class="faq__item${i === 0 ? ' is-open' : ''}" data-reveal style="--d:${i * 0.05}s">
          <button class="faq__q" type="button" aria-expanded="${i === 0}" aria-controls="faq-a-${i}" id="faq-q-${i}"><span>${esc(t(f.q))}</span><span class="pm" aria-hidden="true"></span></button>
          <div class="faq__a" id="faq-a-${i}" role="region" aria-labelledby="faq-q-${i}"><div><p>${esc(t(f.a))}</p></div></div></div>`
      )
      .join('');
  }

  function renderClosing() {
    const b = P.brand;
    const items = [`<a href="${b.websiteUrl}" target="_blank" rel="noopener">${icon('globe')}${esc(b.website)}</a>`, `<a href="mailto:${b.email}">${icon('mail')}${esc(b.email)}</a>`];
    if (b.whatsapp) items.push(`<a href="https://wa.me/${b.whatsapp}" target="_blank" rel="noopener">${icon('chat')}+${esc(b.whatsapp)}</a>`);
    $('#closingContact').innerHTML = items.join('');
    $('#footerYear').textContent = lang === 'ar' ? num(b.year, { useGrouping: false }) : b.year;
    $$('.js-book').forEach((a) => {
      a.href = b.bookingUrl || `mailto:${b.email}?subject=${encodeURIComponent(t(P.hero.primary))}`;
      if (b.bookingUrl) { a.target = '_blank'; a.rel = 'noopener'; }
    });
  }

  /* ------------------------------------------------------------------ */
  /*  Render all                                                         */
  /* ------------------------------------------------------------------ */
  function renderAll() {
    document.title = lang === 'ar' ? 'CanvasOne ERP · عرض Code & Canvas' : 'CanvasOne ERP — Code & Canvas proposal';
    bindText();
    renderHero();
    renderStats();
    renderMarquee();
    renderChallenge();
    renderPlatform();
    renderModules();
    renderSectors();
    renderCompliance();
    renderTech();
    renderJourney();
    renderWhy();
    renderBuilder();
    renderFaq();
    renderClosing();
    CC.refresh();
  }

  /* ------------------------------------------------------------------ */
  /*  Hero parallax (page specific; cursor glow / reveal / tilt are shared) */
  /* ------------------------------------------------------------------ */
  function bindHeroParallax() {
    const dash = $('#dash');
    const chips = $$('.float-chip');
    CC.onFrame((p) => {
      if (scrollY >= innerHeight) return;
      const base = document.documentElement.dir === 'rtl' ? 8 : -8;
      dash.style.setProperty('--ry', `${base + p.nx * 10}deg`);
      dash.style.setProperty('--rx', `${6 - p.ny * 8}deg`);
      chips.forEach((c) => { const d = +c.dataset.depth || 1; c.style.transform = `translate(${p.nx * 18 * d}px, ${p.ny * 18 * d}px)`; });
    });
    addEventListener('resize', () => moveIndicator(), { passive: true });
  }

  /* ------------------------------------------------------------------ */
  /*  Event delegation                                                   */
  /* ------------------------------------------------------------------ */
  function bindEvents() {
    $('#printBtn').addEventListener('click', () => {
      $$('[data-reveal]').forEach((el) => el.classList.add('is-in'));
      window.print();
    });

    // Compare
    $('#compareSwitch').addEventListener('click', (e) => {
      const b = e.target.closest('button');
      if (!b || b.dataset.mode === state.compare) return;
      state.compare = b.dataset.mode;
      renderCompare();
    });

    // Modules
    const grid = $('#modGrid');
    grid.addEventListener('click', (e) => {
      const b = e.target.closest('.mod-btn');
      if (!b) return;
      state.module = +b.dataset.i;
      renderModulePanel();
      if (innerWidth <= 1024) $('#modPanel').scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'nearest' });
    });
    grid.addEventListener('keydown', (e) => {
      const keys = { ArrowRight: 1, ArrowLeft: -1, ArrowDown: 3, ArrowUp: -3 };
      if (!(e.key in keys)) return;
      e.preventDefault();
      let d = keys[e.key];
      if (document.documentElement.dir === 'rtl' && Math.abs(d) === 1) d = -d;
      state.module = (state.module + d + P.modules.length) % P.modules.length;
      renderModulePanel();
      $$('.mod-btn')[state.module].focus();
    });

    // Sectors
    $('#sectorTabs').addEventListener('click', (e) => {
      const b = e.target.closest('.tab');
      if (!b) return;
      state.sector = +b.dataset.i;
      renderSectorPanel();
    });

    // Compliance
    $('#marketSwitch').addEventListener('click', (e) => {
      const b = e.target.closest('button');
      if (!b || +b.dataset.i === state.market) return;
      state.market = +b.dataset.i;
      renderMarket();
    });

    // Builder
    $('#builderForm').addEventListener('click', (e) => {
      const b = e.target.closest('button[data-k]');
      if (!b) return;
      const { k, v } = b.dataset;
      const st = state.builder;
      if (k === 'modules') {
        if (st.modules.has(v)) { if (st.modules.size > 1) st.modules.delete(v); } else st.modules.add(v);
        b.setAttribute('aria-pressed', st.modules.has(v));
      } else {
        st[k] = v;
        $$(`button[data-k="${k}"]`).forEach((x) => x.setAttribute('aria-pressed', x.dataset.v === v));
        if (k === 'sector') {
          P.sectors.find((s) => s.id === v).modules.forEach((id) => st.modules.add(id));
          $$('button[data-k="modules"]').forEach((x) => x.setAttribute('aria-pressed', st.modules.has(x.dataset.v)));
        }
      }
      renderSummary();
      CC.refresh();
    });
    $('#builderSummary').addEventListener('click', async (e) => {
      const b = e.target.closest('#copySummary');
      if (!b) return;
      try {
        await navigator.clipboard.writeText(summaryText());
      } catch {
        const ta = document.createElement('textarea');
        ta.value = summaryText();
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        ta.remove();
      }
      CC.toast(t(P.builder.copied));
    });

    // FAQ
    $('#faqList').addEventListener('click', (e) => {
      const q = e.target.closest('.faq__q');
      if (!q) return;
      const item = q.parentElement;
      const open = !item.classList.contains('is-open');
      $$('.faq__item').forEach((x) => { x.classList.remove('is-open'); $('.faq__q', x).setAttribute('aria-expanded', 'false'); });
      if (open) { item.classList.add('is-open'); q.setAttribute('aria-expanded', 'true'); }
    });
  }

  /* ------------------------------------------------------------------ */
  /*  Boot                                                               */
  /* ------------------------------------------------------------------ */
  CC.onLang((l, initial) => {
    lang = l;
    renderAll();
    if (!initial) requestAnimationFrame(moveIndicator);
  });
  CC.onReady(moveIndicator);
  bindEvents();
  bindHeroParallax();
  CC.boot();
})();
