#!/usr/bin/env node
/* ==========================================================================
   check-asset-versioning.mjs — the home `/system/` band regression guard.

   Bug this locks (2026-11-10): index.html shipped the new three-layer cards
   while returning visitors still held an hour-old `/assets/css/home.css`, so
   the section rendered as unstyled stacked text. Two independent things have
   to stay true to prevent a repeat:

     1. every CSS/JS reference on every page — and in the shared partials —
        carries a `?v=<content-hash>` that matches the file's CURRENT bytes;
     2. the home band's markup and the stylesheet that styles it agree: each
        class used in `#system` must be selected in some CSS file, and the
        stylesheet must not silently drop the rules the markup depends on.

   It runs after version-assets.mjs in `npm run check`.
   ========================================================================== */
import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = (p) => fs.readFileSync(path.join(ROOT, p), 'utf8');

const problems = [];

/* ---------- 1 · hashes are current ---------- */
const REF = /(?:\/assets\/[a-z]+\/[A-Za-z0-9._/-]+\.(?:css|js))\?v=([0-9a-f]{6,})/g;
const hashCache = new Map();
const currentHash = (url) => {
  const clean = url.split('?')[0];
  if (!hashCache.has(clean)) {
    const abs = path.join(ROOT, clean);
    hashCache.set(clean, fs.existsSync(abs)
      ? createHash('sha256').update(fs.readFileSync(abs)).digest('hex').slice(0, 10)
      : null);
  }
  return hashCache.get(clean);
};

const pages = [];
(function walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (['node_modules', 'dist', '.git', 'docs', 'scripts', 'assets', 'test-results', 'playwright-report'].includes(e.name)) continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p);
    else if (e.name.endsWith('.html')) pages.push(path.relative(ROOT, p));
  }
})(ROOT);

let refs = 0;
for (const rel of [...pages, 'partials/head.html', 'partials/bottom.html']) {
  for (const m of read(rel).matchAll(REF)) {
    refs += 1;
    const want = currentHash(m[0]);
    if (!want) { problems.push(`${rel}: references a missing file ${m[0]}`); continue; }
    if (want !== m[1]) problems.push(`${rel}: stale hash on ${m[0].split('?')[0]} (${m[1]} ≠ ${want}) — run npm run sync`);
  }
}
/* A bare, unversioned stylesheet/script reference is the exact failure mode. */
for (const rel of [...pages, 'partials/head.html', 'partials/bottom.html']) {
  for (const m of read(rel).matchAll(/(?:href|src)="(\/assets\/(?:css|js)\/[^"?#]+\.(?:css|js))"/g)) {
    problems.push(`${rel}: unversioned asset ${m[1]} — every CSS/JS reference needs ?v=<hash>`);
  }
}

/* ---------- 2 · home band: markup ↔ stylesheet agreement ---------- */
const home = read('index.html');
const band = home.slice(home.indexOf('<section class="section container system"'), home.indexOf('id="solutions"'));
if (!band) problems.push('index.html: the /system/ band is missing entirely');

const css = ['ds', 'pages', 'live', 'home', 'system'].map((f) => read(`assets/css/${f}.css`)).join('\n');
const CLASSES = [
  'system', 'system__head', 'system__venn', 'system__layer',
  'system__layer--brand', 'system__layer--product', 'system__layer--system',
  'system__tag', 'system__no', 'system__rail', 'system__rail-no',
  'system__cta', 'system__cta-copy', 'system__cta-actions', 'system__cta-facts',
];
for (const cls of CLASSES) {
  if (!band.includes(cls)) problems.push(`index.html: #system markup lost .${cls}`);
  if (!new RegExp(`\\.${cls.replace(/[-_]/g, '\\$&')}(?![\\w-])`).test(css)) {
    problems.push(`CSS: .${cls} is used by the /system/ band but no stylesheet selects it`);
  }
}

/* Counts keep the band's structure honest (three cards, four steps, two CTAs). */
const count = (t, re) => (t.match(re) || []).length;
const expected = [
  ['layer cards', /class="system__layer /g, 3],
  ['layer tags', /class="system__tag"/g, 3],
  ['rail steps', /class="system__rail-no"/g, 4],
  ['cta buttons', /class="btn btn--/g, 2],
  ['cta facts', /<li><b>/g, 3],
];
for (const [name, re, want] of expected) {
  const got = count(band, re);
  if (got !== want) problems.push(`index.html: #system ${name} = ${got}, expected ${want}`);
}

/* The Arabic twin must carry the same band, not an older copy. */
const ar = read('ar/index.html');
const arBand = ar.slice(ar.indexOf('<section class="section container system"'), ar.indexOf('id="solutions"'));
for (const [name, re, want] of expected) {
  const got = count(arBand, re);
  if (got !== want) problems.push(`ar/index.html: #system ${name} = ${got}, expected ${want}`);
}

/* ---------- 3 · the service worker version moves with the CSS ---------- */
const sw = read('sw.js');
const swVersion = (sw.match(/const VERSION = '([^']+)'/) || [])[1];
if (!swVersion) problems.push('sw.js: VERSION is missing');
else if (!/^cc-app-\d{4}-\d{2}-\d{2}-\d+$/.test(swVersion)) problems.push(`sw.js: VERSION "${swVersion}" does not follow cc-app-YYYY-MM-DD-N`);

if (problems.length) {
  console.error(`asset versioning: ${problems.length} problem(s):`);
  for (const p of problems) console.error('  - ' + p);
  process.exit(1);
}
console.log(`asset versioning: ok — ${refs} hashed CSS/JS refs current across ${pages.length} pages, /system/ band wired in EN+AR, sw ${swVersion}`);
