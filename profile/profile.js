/* ==========================================================================
   Code & Canvas — Company Profile 2026
   Filtering, search, TOC tracking and print-to-PDF.
   Progressive enhancement only: the page reads fine without it.
   ========================================================================== */
(function () {
  'use strict';

  var state = { pillar: 'all', q: '' };

  /* ---------- Filters + search ---------- */
  var filters = Array.prototype.slice.call(document.querySelectorAll('[data-filter]'));
  var search = document.getElementById('pSearch');
  var pillars = Array.prototype.slice.call(document.querySelectorAll('.pillar'));
  var cards = Array.prototype.slice.call(document.querySelectorAll('.svc'));

  function normalise(s) {
    return (s || '')
      .toLowerCase()
      .replace(/[\u064B-\u065F\u0670]/g, '')   /* Arabic diacritics */
      .replace(/[أإآ]/g, 'ا')
      .replace(/ى/g, 'ي')
      .replace(/ة/g, 'ه')
      .replace(/\s+/g, ' ')
      .trim();
  }

  function apply() {
    var q = normalise(state.q);

    cards.forEach(function (card) {
      var byPillar = state.pillar === 'all' || card.getAttribute('data-pillar') === state.pillar;
      var haystack = normalise(card.textContent + ' ' + (card.getAttribute('data-pillar') || ''));
      var byText = !q || haystack.indexOf(q) !== -1;
      card.hidden = !(byPillar && byText);
    });

    pillars.forEach(function (pillar) {
      var visible = pillar.querySelectorAll('.svc:not([hidden])').length > 0;
      pillar.hidden = !visible;
    });

    var empty = document.getElementById('pEmpty');
    if (empty) empty.hidden = cards.some(function (c) { return !c.hidden; });
  }

  filters.forEach(function (btn) {
    btn.addEventListener('click', function () {
      filters.forEach(function (b) { b.classList.remove('is-on'); });
      btn.classList.add('is-on');
      state.pillar = btn.getAttribute('data-filter') || 'all';
      apply();
    });
  });

  if (search) {
    var timer;
    search.addEventListener('input', function () {
      clearTimeout(timer);
      timer = setTimeout(function () {
        state.q = search.value;
        apply();
      }, 90);
    });
  }

  /* ---------- TOC tracking ---------- */
  var toc = document.getElementById('pToc');
  if (toc && 'IntersectionObserver' in window) {
    var links = Array.prototype.slice.call(toc.querySelectorAll('a'));
    var map = {};
    links.forEach(function (a) {
      var id = a.getAttribute('href').slice(1);
      var section = document.getElementById(id);
      if (section) map[id] = a;
    });
    var current = null;
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          if (current) current.classList.remove('is-active');
          current = map[entry.target.id] || null;
          if (current) {
            current.classList.add('is-active');
            if (toc.scrollWidth > toc.clientWidth) {
              var left = current.offsetLeft - toc.clientWidth / 2 + current.offsetWidth / 2;
              toc.scrollTo({ left: left, behavior: 'smooth' });
            }
          }
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px', threshold: 0 });
    Object.keys(map).forEach(function (id) {
      var section = document.getElementById(id);
      if (section) observer.observe(section);
    });
  }

  /* ---------- Print / PDF ---------- */
  function printProfile() {
    /* never print a filtered subset: reset to the full catalogue first */
    state = { pillar: 'all', q: '' };
    filters.forEach(function (b) { b.classList.toggle('is-on', b.getAttribute('data-filter') === 'all'); });
    if (search) search.value = '';
    apply();
    window.print();
  }
  Array.prototype.forEach.call(document.querySelectorAll('[data-print]'), function (btn) {
    btn.addEventListener('click', printProfile);
  });

  /* ---------- Deep link: /profile/#services etc. ---------- */
  if (location.hash) {
    var target = document.getElementById(location.hash.slice(1));
    if (target) setTimeout(function () { target.scrollIntoView({ behavior: 'smooth', block: 'start' }); }, 60);
  }
})();
