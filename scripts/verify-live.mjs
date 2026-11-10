#!/usr/bin/env node
/* ==========================================================================
   verify-live.mjs — production acceptance check against the LIVE DOMAIN.

   A green GitHub Actions run or a successful `hostinger` branch push is NOT
   evidence that the site answers. This script requests the real public URLs,
   checks status/content and a few page-level invariants, and fails loudly.

     npm run verify:live
     CC_BASE_URL=https://codeandcanvas.net npm run verify:live
     node scripts/verify-live.mjs --json

   Network-restricted sandboxes may not be able to reach the domain; in that
   case the script reports SKIPPED with the network error and exits 2 so CI can
   treat "no answer" as a failure rather than a pass.
   ========================================================================== */
import { readdirSync, existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
const ROOT = fileURLToPath(new URL('../', import.meta.url));
const DIST = join(ROOT, 'dist');
const BASE = (process.env.CC_BASE_URL || 'https://codeandcanvas.net').replace(/\/$/, '');
const AS_JSON = process.argv.includes('--json');

const ROUTES = [
  ['/', ['Code & Canvas', 'og:image']],
  ['/ar/', ['Code & Canvas', 'dir="rtl"']],
  ['/services/', ['Services', 'og:image']],
  ['/case-studies/', ['Case', 'og:image']],
  ['/contact/', ['Contact', 'name="consent"']],
  ['/blog/', ['Insights', 'from-brand-identity-to-brand-systems']],
  // The old "Selected" marker went stale when /work/ was rewritten in the
  // overhaul; these strings are present in the current generator output.
  ['/work/', ['CONCEPT STUDY', 'FOUNDER WORK ARCHIVE', 'PROJECT CASE STUDIES', 'work/']],
  ['/book/', ['Book a 30-Minute', 'book-form']],
  ['/saudi-arabia/', ['Saudi Arabia']],
  ['/egypt/', ['Egypt']],
  ['/privacy-policy/', ['Privacy Policy', 'first-party']],
  ['/terms-of-use/', ['Terms of Use']],
  ['/cookie-policy/', ['Cookie Policy']],
  ['/resources/', ['Resources']],
  ['/system/', ['Design System', 'og:image']],
  ['/ar/system/', ['نظام التصميم', 'dir="rtl"']],
  ['/claims/', ['Claims']],
];

/* The core list above is a sample. The real question is "does the site link to
   anything that 404s in production", so the crawl list is derived from dist/ and
   always includes the pages this pass touched (booking, technology, team, story,
   work, claims and their Arabic twins). */
function routesFromDist() {
  const set = new Set();
  const walk = (dir) => {
    for (const entry of readdirSync(dir, { withFileTypes: true })) {
      const full = join(dir, entry.name);
      if (entry.isDirectory()) { walk(full); continue; }
      if (!entry.name.endsWith('.html')) continue;
      const rel = full.slice(DIST.length).replace(/\\/g, '/').replace(/index\.html$/, '');
      set.add(rel.startsWith('/') ? rel : '/' + rel);
    }
  };
  if (existsSync(DIST)) walk(DIST);
  return [...set].sort();
}
const PAGES = (() => {
  const internal = routesFromDist();
  const picked = internal.length
    ? internal.filter((r) => /^\/(ar\/)?(book|technology-services|team|about|our-story|work|claims|contact|services|healthcare|creative-services|pricing-faq)\/$/.test(r))
    : [];
  return { internal, picked };
})();

/* Redirects declared in vercel.json must still resolve to a 200 page. */
function redirectProbes() {
  const file = join(ROOT, 'vercel.json');
  if (!existsSync(file)) return [];
  const conf = JSON.parse(readFileSync(file, 'utf8'));
  return (conf.redirects || [])
    .filter((r) => !r.source.includes(':') && !r.source.includes('*'))
    .slice(0, 12)
    .map((r) => ({ from: r.source, expect: r.destination }));
}

/* ---------------------------------------------------------------- helpers */
const HASHED = /\/assets\/(?:css|js|brand)\/[^"'\s]+\.(?:css|js|svg|png|webp|woff2)\?v=([a-f0-9]{6,})/g;

/** Canonical must be self-referential and the twin must be declared. */
function headProblems(route, html) {
  const problems = [];
  const canon = (html.match(/<link rel="canonical" href="([^"]+)"/) || [])[1] || '';
  if (!canon) problems.push('no canonical');
  else if (!canon.endsWith(route)) problems.push(`canonical points elsewhere (${canon})`);
  const alts = [...html.matchAll(/<link rel="alternate" hreflang="([a-z-]+)" href="([^"]+)"/g)].map((m) => [m[1], m[2]]);
  const langs = alts.map((a) => a[0]).sort().join(',');
  if (!/ar/.test(langs) || !/en/.test(langs) || !/x-default/.test(langs)) problems.push(`hreflang set incomplete (${langs || 'none'})`);
  const ar = route.startsWith('/ar/');
  const twin = alts.find((a) => (ar ? a[0] === 'en' : a[0] === 'ar'))?.[1] || '';
  if (!twin) problems.push('missing twin alternate');
  else if (ar && twin.includes('/ar/')) problems.push('Arabic twin points at Arabic');
  else if (!ar && !/\/ar\//.test(twin)) problems.push('Arabic twin points at English');
  // Stale HTML: the page must not embed a hashed asset the build no longer has.
  if (EXPECTED.length) {
    for (const m of html.matchAll(HASHED)) {
      const known = EXPECTED.some((e) => e.path === new URL(m[0], 'https://x').pathname && e.v === m[1]);
      if (!known) problems.push(`stale asset hash ${new URL(m[0], 'https://x').pathname}?v=${m[1]}`);
    }
  }
  return problems;
}

/** Every hashed asset the fresh build references, from dist/ itself. */
const EXPECTED = (() => {
  if (!existsSync(DIST)) return [];
  const list = [];
  const walk = (dir) => {
    for (const entry of readdirSync(dir, { withFileTypes: true })) {
      const full = join(dir, entry.name);
      if (entry.isDirectory()) { walk(full); continue; }
      if (!entry.name.endsWith('.html')) continue;
      const html = readFileSync(full, 'utf8');
      for (const m of html.matchAll(HASHED)) list.push({ path: new URL(m[0], 'https://x').pathname, v: m[1] });
    }
  };
  walk(DIST);
  return list;
})();

const ROUTES_ALL = [...ROUTES, ...PAGES.picked.map((r) => [r, []])];
const seen = new Set();

async function checkHtml(route, needles = []) {
  const url = BASE + route;
  const res = await fetch(url, { redirect: 'follow', headers: { 'User-Agent': 'cc-live-verify/2.0' } });
  const html = await res.text();
  const problems = [];
  if (res.status !== 200) problems.push(`HTTP ${res.status}`);
  if (!/text\/html/i.test(res.headers.get('content-type') || '')) problems.push('not text/html');
  if (/Lost in the void|404 — Lost/.test(html)) problems.push('404 page body');
  if (/{{OG_IMAGE}}|__ASSET_VERSION__/.test(html)) problems.push('unresolved build placeholder');
  const missing = needles.filter((n) => !html.includes(n));
  if (missing.length) problems.push(`missing markers: ${missing.join(', ')}`);
  problems.push(...headProblems(route, html));
  // Cached HTML must never be served as fresh: the site relies on revalidation.
  const cc = (res.headers.get('cache-control') || '').toLowerCase();
  if (/s-maxage=\d{4,}|max-age=(?:[3-9]\d{4,}|\d{5,})/.test(cc)) problems.push(`HTML cached too long (${cc})`);
  return { route, url, status: res.status, problems };
}

const LOCAL_TARGETS = new Set(PAGES.internal);
const out = [];
let networkError = null;

/* 1 · curated markers */
for (const [route, needles] of ROUTES_ALL) {
  if (seen.has(route)) continue;
  seen.add(route);
  try {
    const r = await checkHtml(route, needles);
    out.push({ ...r, ok: r.problems.length === 0 });
  } catch (e) {
    networkError = e.message;
    out.push({ route, url: BASE + route, status: 0, ok: false, problems: ['network error: ' + e.message] });
  }
}

/* 2 · every internal link published by the site (crawl of dist/, HEAD only) */
const CRAWL = PAGES.internal.filter((r) => !seen.has(r));
if (CRAWL.length && !networkError) {
  const batch = 6;
  for (let i = 0; i < CRAWL.length; i += batch) {
    const chunk = CRAWL.slice(i, i + batch);
    const results = await Promise.all(chunk.map(async (route) => {
      try {
        const res = await fetch(BASE + route, { redirect: 'follow', headers: { 'User-Agent': 'cc-live-verify/2.0' } });
        const bad = res.status !== 200 ? [`HTTP ${res.status}`] : [];
        return { route, url: BASE + route, status: res.status, problems: bad, ok: bad.length === 0 };
      } catch (e) {
        networkError = e.message;
        return { route, url: BASE + route, status: 0, problems: ['network error: ' + e.message], ok: false };
      }
    }));
    out.push(...results);
    seen.add(...chunk);
  }
}

/* 3 · the booking API lives behind the same origin. The published site is a
   static build; if the Node service is not mounted next to it, /book/ silently
   degrades to a manual hand-off while still looking like a working scheduler.
   Report it always; fail only when the release claims a live scheduler
   (CC_REQUIRE_API=1), so the owner can see the truth without a red deploy gate. */
let apiStatus = 'not checked';
try {
  const res = await fetch(`${BASE}/api/health`, { headers: { 'User-Agent': 'cc-live-verify/2.0' } });
  const body = await res.text();
  const live = res.status === 200 && /"ok":\s*true/.test(body);
  apiStatus = live ? `live (${(JSON.parse(body).commit || 'unknown').slice(0, 7)})` : `HTTP ${res.status}`;
  const required = process.env.CC_REQUIRE_API === '1';
  out.push({
    route: '/api/health (booking + CRM)', url: BASE + '/api/health', status: res.status,
    ok: live || !required,
    problems: live ? [] : [required
      ? 'the booking API is not answering on the production origin'
      : 'booking API not answering — /book/ falls back to a manual request (not a booking)'],
    warn: !live && !required,
  });
} catch (e) {
  apiStatus = `unreachable (${e.message})`;
  out.push({ route: '/api/health (booking + CRM)', url: BASE + '/api/health', status: 0, ok: process.env.CC_REQUIRE_API !== '1',
    problems: ['booking API unreachable — /book/ falls back to a manual request'], warn: true });
}

/* 4 · declared redirects must land on a 200, not a chain */
for (const probe of redirectProbes()) {
  if (networkError) break;
  try {
    const res = await fetch(BASE + probe.from, { redirect: 'manual', headers: { 'User-Agent': 'cc-live-verify/2.0' } });
    const loc = res.headers.get('location') || '';
    const isHost = !/^https?:\/\/(127\.0\.0\.1|localhost)/.test(BASE);
    if ([301, 302, 307, 308].includes(res.status)) {
      const ok = !probe.expect || loc.includes(probe.expect.replace(/\/#.*$/, '').replace(/\/$/, ''));
      out.push({ route: `${probe.from} → ${loc}`, url: BASE + probe.from, status: res.status, ok, problems: ok ? [] : [`redirect → ${loc || 'nowhere'}, expected ${probe.expect}`] });
    } else if (!isHost) {
      /* A local server serves files, not host rules: assert the destination is a
         real page and record that the rule itself is unverified here. */
      const clean = (probe.expect || '').replace(/#.*$/, '').replace(/\/?$/, '/');
      const target = LOCAL_TARGETS.has(clean);
      out.push({ route: `${probe.from} → ${probe.expect}`, url: BASE + probe.from, status: res.status, ok: target,
        problems: target ? [] : [`redirect target ${probe.expect} is not in the build`], note: 'host rule not exercised locally' });
    } else {
      out.push({ route: `${probe.from} → ${probe.expect}`, url: BASE + probe.from, status: res.status, ok: false, problems: [`expected a redirect, got ${res.status}`] });
    }
  } catch (e) {
    out.push({ route: probe.from, url: BASE + probe.from, status: 0, ok: false, problems: ['network error: ' + e.message] });
  }
}

const warned = out.filter((r) => r.warn);

if (AS_JSON) {
  console.log(JSON.stringify({ base: BASE, networkError, results: out }, null, 2));
} else {
  console.log(`Live domain verification — ${BASE}`);
  for (const r of out) console.log(`${r.ok ? '✓' : '✗'} ${r.route}  [${r.status}]${r.problems.length ? '  ' + r.problems.join('; ') : ''}`);
  console.log(`\n${out.filter((r) => r.ok).length}/${out.length} routes answered · ${EXPECTED.length} hashed asset reference(s) in the build`);
  if (warned.length) console.log(`${warned.length} warning(s): ` + warned.map((r) => r.route).join(', '));
}

const failed = out.filter((r) => !r.ok && !r.warn);
if (networkError) {
  console.error(`\nCould not reach ${BASE}: ${networkError}. Live verification is REQUIRED; do not treat a green build as deployment.`);
  process.exit(2);
}
if (failed.length) {
  console.error(`\n${failed.length}/${out.length} live route(s) failed. Production deployment is NOT approved.`);
  process.exit(1);
}
console.log(`\nAll ${out.length} live routes answered correctly.`);
