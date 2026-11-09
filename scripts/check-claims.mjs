#!/usr/bin/env node
/* ==========================================================================
   check-claims.mjs — mandatory content gate.

   1. Bans unevidenced numeric / credential claims from every public HTML page
      (the claims register itself is allowed to quote them as "Removed").
   2. Requires the consent checkbox on every form that creates a lead record.
   3. Requires the first-party growth routes to exist and to be linked from the
      homepage, so the new work cannot silently disappear from the journey.
   4. Requires each generated page's og:image to be a real file and to differ
      from the default on the key pages.

   Usage: node scripts/check-claims.mjs
   ========================================================================== */
import { readdirSync, readFileSync, existsSync, statSync } from 'node:fs';
import { join, relative, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = fileURLToPath(new URL('../', import.meta.url));
const errors = [];
const fail = (m) => errors.push(m);

function walk(dir, out = []) {
  for (const ent of readdirSync(dir, { withFileTypes: true })) {
    if (ent.name.startsWith('.')) continue;
    const p = join(dir, ent.name);
    if (ent.isDirectory()) {
      if (['assets', 'scripts', 'tests', 'node_modules', 'docs', 'partials', 'server', 'dist'].includes(ent.name)) continue;
      walk(p, out);
    } else if (ent.name === 'index.html') out.push(p);
  }
  return out;
}

const pages = walk(ROOT);
const BANNED = [
  [/\b(?:9|10)\+\s*(?:years?|سنوات?|سنة)\b/i, 'unverified years of experience'],
  [/\b40\+\s*(?:brands?|orgs?|علامة)/i, 'unverified brand count'],
  [/\b12\+\s*(?:sectors?|قطاع)/i, 'unverified sector count'],
  [/\b20\+\s*(?:brands?|علامة)/i, 'unverified brand count'],
  [/4[–—-]7\s*[×x]/i, 'unverified speed multiplier'],
  [/\$?50\s?K\s*[–—-]\s*\$?200\s?K/i, 'unverified risk figure'],
  [/active credentials|worked credentials|اعتمادات فعّالة|اعتمادات يمارسها/i, 'unverified credential wording'],
];
const QUOTE_ALLOWED = /\/claims\/|\/work\/|\/evidence/;

let checked = 0;
for (const file of pages) {
  const rel = '/' + relative(ROOT, file).split(sep).join('/').replace(/\/index\.html$/, '/');
  const html = readFileSync(file, 'utf8');
  checked += 1;
  if (!QUOTE_ALLOWED.test(rel)) {
    for (const [re, label] of BANNED) {
      if (re.test(html)) fail(`${rel}: ${label} (${re})`);
    }
  }
  // Every lead-creating form must contain an explicit consent control.
  if (/data-integration="(?:contact|newsletter|career)"/.test(html) || /id="book-form"/.test(html)) {
    if (!/name="consent"/.test(html)) fail(`${rel}: lead form without a consent checkbox`);
  }
  // OG image must exist on disk.
  const og = html.match(/<meta property="og:image" content="([^"]+)"/)?.[1];
  if (!og) fail(`${rel}: missing og:image meta`);
  else {
    const local = og.replace(/^https?:\/\/[^/]+/, '');
    if (local.startsWith('/') && !existsSync(join(ROOT, local))) fail(`${rel}: missing OG asset ${local}`);
  }
  // No unresolved shared-head placeholder may ship.
  if (html.includes('{{OG_IMAGE}}')) fail(`${rel}: unresolved {{OG_IMAGE}} placeholder`);
  if (html.includes('signategrotesk')) fail(`${rel}: references the unlicensed Signate font`);
  // The installable app shell is shared chrome: every page that loads the site
  // runtime (which registers the worker) must point at the manifest and icon.
  // The three noindex private review surveys have their own standalone head and
  // never load site.js, so they are not app pages.
  if (/<script[^>]+src="\/assets\/js\/site\.js"/.test(html)) {
    if (!/<link rel="manifest" href="\/manifest\.webmanifest"/.test(html)) fail(`${rel}: missing PWA manifest link`);
    if (!/<link rel="apple-touch-icon" href="\/assets\/brand\/app\/apple-touch-icon\.png"/.test(html)) fail(`${rel}: missing apple-touch-icon`);
  }
}

/* ---- required first-party routes ---- */
const REQUIRED = [
  '/work/index.html', '/services/index.html', '/book/index.html',
  '/resources/index.html', '/claims/index.html', '/saudi-arabia/index.html', '/egypt/index.html',
  '/system/index.html',
  '/work/bilingual-brand-system/index.html', '/work/packaging-print-system/index.html',
  '/work/product-ui-system/index.html', '/work/web-experience-rebuild/index.html',
  '/services/brand-identity-design/index.html', '/services/brand-strategy-systems/index.html',
  '/services/packaging-design/index.html', '/services/website-design-development/index.html',
  '/services/product-design-ux/index.html', '/services/healthcare-digital-solutions/index.html',
  '/services/ai-workflow-automation/index.html',
  '/blog/from-brand-identity-to-brand-systems/index.html',
  '/blog/creative-strategy-in-the-age-of-generative-ai/index.html',
  '/ar/index.html', '/ar/erp/index.html', '/ar/book/index.html', '/ar/work/index.html',
  '/ar/system/index.html',
];
for (const r of REQUIRED) if (!existsSync(join(ROOT, r))) fail(`missing required route: ${r}`);
if (!existsSync(join(ROOT, 'server/crm.html'))) fail('missing lead dashboard: server/crm.html');
if (!existsSync(join(ROOT, 'server/api.mjs'))) fail('missing first-party API: server/api.mjs');
if (!existsSync(join(ROOT, 'docs/LEAD-PIPELINE.md'))) fail('missing pipeline documentation: docs/LEAD-PIPELINE.md');

/* ---- homepage must expose the new journey ---- */
const home = readFileSync(join(ROOT, 'index.html'), 'utf8');
for (const [name, re] of [
  ['primary booking CTA', /class="btn btn--primary btn--lg magnetic" href="\/book\/"/],
  ['real artwork', /\/assets\/media\/hero-system\.webp/],
  ['illustrative disclaimer', /ILLUSTRATIVE · NOT CLIENT WORK|NOT CLIENT WORK/],
  ['selected work links', /href="\/work\/bilingual-brand-system\/"/],
  ['positioning pillars', /id="positioning"/],
  ['claims register link', /href="\/claims\/"/],
  ['local market page link', /href="\/saudi-arabia\/"/],
]) if (!re.test(home)) fail(`homepage: missing ${name}`);

/* ---- legal pages must not be drafts anymore ---- */
for (const r of ['privacy-policy', 'terms-of-use', 'cookie-policy']) {
  const p = join(ROOT, r, 'index.html');
  if (!existsSync(p)) { fail(`missing legal page /${r}/`); continue; }
  const t = readFileSync(p, 'utf8');
  if (/Draft — pending legal review|مسودة — بانتظار المراجعة القانونية/i.test(t)) fail(`/${r}/: still marked as a legal draft`);
}

/* ---- per-route OG images on key pages ---- */
for (const [r, og] of [
  ['index.html', '/assets/brand/og/home.png'],
  ['book/index.html', '/assets/brand/og/book.png'],
  ['work/index.html', '/assets/brand/og/work.png'],
  ['blog/from-brand-identity-to-brand-systems/index.html', '/assets/brand/og/blog-brand-systems.png'],
  ['blog/creative-strategy-in-the-age-of-generative-ai/index.html', '/assets/brand/og/blog-ai-strategy.png'],
]) {
  const p = join(ROOT, r);
  if (!existsSync(p)) continue;
  if (!readFileSync(p, 'utf8').includes(og)) fail(`${r}: expected per-route OG card ${og}`);
}

/* ---- installable app shell ---- */
for (const f of ['manifest.webmanifest', 'sw.js', 'offline.html',
  'assets/brand/app/icon-192.png', 'assets/brand/app/icon-512.png',
  'assets/brand/app/icon-maskable-192.png', 'assets/brand/app/icon-maskable-512.png',
  'assets/brand/app/apple-touch-icon.png']) {
  if (!existsSync(join(ROOT, f))) fail(`missing PWA asset: ${f}`);
}
try {
  const m = JSON.parse(readFileSync(join(ROOT, 'manifest.webmanifest'), 'utf8'));
  for (const key of ['name', 'short_name', 'start_url', 'scope', 'display', 'icons']) {
    if (!(key in m)) fail(`manifest.webmanifest missing ${key}`);
  }
  if (m.display !== 'standalone') fail('manifest.webmanifest is not standalone');
  for (const icon of m.icons || []) {
    if (!existsSync(join(ROOT, String(icon.src || '').replace(/^\//, '')))) fail(`manifest icon missing: ${icon.src}`);
  }
} catch (e) {
  fail(`manifest.webmanifest invalid: ${e.message}`);
}

if (errors.length) {
  console.error(`check-claims: ${errors.length} problem(s) across ${checked} pages:`);
  for (const e of errors.slice(0, 80)) console.error('  ✗ ' + e);
  if (errors.length > 80) console.error(`  … and ${errors.length - 80} more`);
  process.exit(1);
}
console.log(`check-claims: ok — ${checked} HTML pages, claims/consent/OG/routes verified`);
