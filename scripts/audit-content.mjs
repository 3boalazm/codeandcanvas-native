#!/usr/bin/env node
/* ==========================================================================
   audit-content.mjs — read-only, whole-site content & payload audit.

   Unlike scripts/check-*.mjs (which are hard gates that must pass), this is a
   diagnostic: it reports everything it finds and always exits 0. Use it to
   take a lap around the site before a content refresh:

     npm run audit:content                 # human-readable report
     node scripts/audit-content.mjs --json # machine-readable findings

   It checks the committed HTML (EN + the generated /ar/ twins), the media
   register and the homepage's shipped weight. It never writes to the repo.
   ========================================================================== */
import { readdirSync, readFileSync, existsSync, statSync } from 'node:fs';
import { join, relative, sep, basename } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = fileURLToPath(new URL('../', import.meta.url));
const JSON_OUT = process.argv.includes('--json');
const TODAY = new Date('2026-11-08T00:00:00Z');
const findings = [];
const note = (group, file, message) => findings.push({ group, file, message });
const SKIP_DIRS = new Set(['assets', 'scripts', 'tests', 'node_modules', 'docs', 'partials', 'server', 'dist', '.git', '.data', 'test-results', 'coverage']);

function walk(dir, out = []) {
  for (const ent of readdirSync(dir, { withFileTypes: true })) {
    if (ent.name.startsWith('.') && ent.name !== 'ar') continue;
    const p = join(dir, ent.name);
    if (ent.isDirectory()) {
      if (!SKIP_DIRS.has(ent.name)) walk(p, out);
    } else if (ent.name === 'index.html') out.push(p);
  }
  return out;
}
const pages = walk(ROOT).sort();
const rel = (f) => '/' + relative(ROOT, f).split(sep).join('/').replace(/\/index\.html$/, '/');
const strip = (html) => html
  .replace(/<(script|style|noscript|template)[\s\S]*?<\/\1>/gi, ' ')
  .replace(/<!--[\s\S]*?-->/g, ' ')
  .replace(/<[^>]+>/g, ' ')
  .replace(/&[a-z#0-9]+;/gi, ' ')
  .replace(/\s+/g, ' ')
  .trim();
const words = (s) => s ? s.split(/\s+/).length : 0;
/* Arabic twins are built from a <template data-ar-swap> embedded in the EN
   page. That markup is unrendered in EN but carries duplicate ids / headings,
   so it must be excluded from structural checks. */
const visibleHtml = (html) => html.replace(/<template\b[\s\S]*?<\/template>/gi, ' ');

/* Patterns that mean unfinished or unverifiable copy. The claims register is
   allowed to quote removed claims, so it is excluded from claim matches. */
const PLACEHOLDERS = [
  [/\{\{[^}]+\}\}/, 'unresolved template token'],
  [/\bTODO\b|\bFIXME\b|\bTBD\b/i, 'TODO/TBD marker'],
  [/\bLorem ipsum\b/i, 'lorem ipsum'],
  [/Draft\s*[—-]\s*pending legal review|مسودة\s*[—-]\s*بانتظار المراجعة القانونية/i, 'legal draft marker'],
  [/\bundefined\b|\[object Object\]|\bNaN%/, 'serialisation artefact'],
];
/* Deliberate roadmap state, not unfinished copy: one book is published as
   "Coming soon" and its detail page says so plainly. */
const ROADMAP = [[/\bCOMING[ _-]?SOON\b/i, 'labelled coming-soon item (intentional — one unpublished book)']];
const CLAIMS = [
  [/\b(?:we guarantee|guaranteed (?:results?|outcomes?|ROI)|نضمن لك|مضمونة النتيجة)\b/i, 'guarantee language'],
  [/\b(?:award[- ]winning|best[- ]in[- ]class|world[- ]class|#1|number one|الأفضل|الأول عالميًا)\b/i, 'superlative'],
  [/\b(?:9|10)\+\s*(?:years?|سنوات?|سنة)\b/i, 'unverified years of experience'],
  [/\b(?:20|40)\+\s*(?:brands?|علامة)/i, 'unverified brand count'],
  [/\b12\+\s*(?:sectors?|قطاع)/i, 'unverified sector count'],
  [/\b\d{2,3}%\s*(?:increase|growth|ROI|conversion)/i, 'unquantified outcome percentage'],
];
const CLAIM_EXEMPT = /\/claims\/|\/evidence|\/proof/;

const titles = new Map(), descriptions = new Map(), bodyHashes = new Map();
const mediaRefs = new Map();
let imgTotal = 0, imgEager = 0, imgNoAlt = 0, imgNoArAlt = 0, imgNoDims = 0, imgNoLoading = 0;

for (const file of pages) {
  const r = rel(file);
  const html = readFileSync(file, 'utf8');
  const rendered = visibleHtml(html);
  /* Claims quoted as "Removed" in the public evidence register are honest. */
  const claimText = rendered.replace(/<tr>[\s\S]*?st--removed[\s\S]*?<\/tr>/gi, ' ');
  const text = strip(rendered);
  const isAr = r.startsWith('/ar/');

  /* 1 · unfinished / unverifiable copy */
  for (const [re, label] of PLACEHOLDERS) if (re.test(rendered)) note('placeholders', r, label);
  for (const [re, label] of ROADMAP) if (re.test(rendered)) note('roadmap', r, label);
  if (!CLAIM_EXEMPT.test(r)) for (const [re, label] of CLAIMS) {
    const m = claimText.match(re);
    if (m) note('claims', r, `${label} — «${claimText.slice(Math.max(0, m.index - 45), m.index + 65).replace(/\s+/g, ' ')}»`);
  }

  /* 2 · document metadata */
  const title = (html.match(/<title>([\s\S]*?)<\/title>/i) || [])[1]?.trim();
  const desc = (html.match(/<meta\s+name="description"\s+content="([^"]*)"/i) || [])[1]?.trim();
  if (!title) note('metadata', r, 'missing <title>');
  if (!desc) note('metadata', r, 'missing meta description');
  if (title) { const a = titles.get(title) || []; a.push(r); titles.set(title, a); }
  if (desc) { const a = descriptions.get(desc) || []; a.push(r); descriptions.set(desc, a); }
  const indexed = !/name="robots" content="[^"]*noindex/i.test(html);
  if (indexed && !/rel="canonical"/.test(html)) note('metadata', r, 'missing canonical');
  if (indexed && !/hreflang=/.test(html)) note('metadata', r, 'missing hreflang set');

  /* 3 · heading structure & ids */
  const h1 = (rendered.match(/<h1\b/gi) || []).length;
  if (h1 !== 1) note('structure', r, `${h1} <h1> elements (expected 1)`);
  const levels = [...rendered.matchAll(/<h([1-6])\b/gi)].map((m) => +m[1]);
  for (let i = 1; i < levels.length; i++) if (levels[i] > levels[i - 1] + 1) { note('structure', r, `advisory heading jump h${levels[i - 1]} → h${levels[i]} (axe WCAG2 A/AA passes)`); break; }
  const ids = [...rendered.matchAll(/\sid="([^"]+)"/g)].map((m) => m[1]);
  const dup = ids.filter((id, i) => ids.indexOf(id) !== i);
  if (dup.length) note('structure', r, `duplicate ids: ${[...new Set(dup)].slice(0, 5).join(', ')}`);

  /* 4 · language twin */
  if (isAr) {
    const leftovers = (html.match(/\sdata-ar(?:-html|-label|-title|-alt|-placeholder)?=/g) || []).length;
    if (leftovers) note('arabic', r, `${leftovers} unconsumed data-ar* attribute(s)`);
    const arabic = (text.match(/[\u0600-\u06FF]/g) || []).length;
    if (arabic < 120 && !/\/(?:read|erp)\//.test(r)) note('arabic', r, `only ${arabic} Arabic letters`);
    if (!/lang="ar"/.test(html) || !/dir="rtl"/.test(html)) note('arabic', r, 'missing lang=ar / dir=rtl');
  }

  /* 5 · thin content */
  const wc = words(text);
  if (wc < 120 && !/data-t="/.test(rendered)) note('thin', r, `${wc} words of visible text`);
  if (wc < 120 && /data-t="/.test(rendered)) note('dynamic', r, `${wc} static words — copy is injected by JS (verified in the browser tour)`);

  /* 6 · images */
  for (const m of html.matchAll(/<img\b[^>]*>/gi)) {
    const tag = m[0]; imgTotal += 1;
    const src = (tag.match(/src="([^"]+)"/) || [])[1] || '?';
    const decorative = /\/assets\/brand\//.test(src);
    if (!/\balt="/.test(tag)) { imgNoAlt += 1; note('images', r, `img without alt attribute: ${src}`); }
    if (!isAr && !decorative && !/\bdata-ar-alt=/.test(tag)) imgNoArAlt += 1;
    if (!/\bwidth="\d+"/.test(tag) || !/\bheight="\d+"/.test(tag)) { imgNoDims += 1; note('images', r, 'img without intrinsic dimensions'); }
    if (!decorative && !/\bloading=/.test(tag)) { imgNoLoading += 1; note('images', r, 'img without loading attribute'); }
    if (/loading="eager"/.test(tag)) imgEager += 1;
    if (src && src !== '?') mediaRefs.set(src, (mediaRefs.get(src) || 0) + 1);
    /* Every srcset candidate must exist — a missing phone variant would silently
       fall back to the full-size image on a slow connection. */
    const srcset = (tag.match(/srcset="([^"]+)"/) || [])[1];
    if (srcset) for (const cand of srcset.split(',')) {
      const u = cand.trim().split(/\s+/)[0];
      if (!u.startsWith('/assets/media/')) continue;
      mediaRefs.set(u, (mediaRefs.get(u) || 0) + 1);
      if (!existsSync(join(ROOT, u.slice(1)))) note('images', r, `missing srcset asset ${u}`);
    }
  }

  /* 7 · internal links & anchors */
  const localIds = new Set(ids);
  for (const m of html.matchAll(/\s(?:href|src)="([^"]*)"/g)) {
    const url = m[1];
    if (!url || /^(?:https?:|mailto:|tel:|data:|javascript:|#|\/_vercel\/)/.test(url)) continue;
    const clean = url.split('#')[0].split('?')[0];
    if (!clean) continue;
    const candidate = clean.endsWith('/') ? join(ROOT, clean.slice(1), 'index.html') : join(ROOT, clean.slice(1));
    if (!existsSync(candidate)) note('links', r, `dangling ${url}`);
    if (url.startsWith('#') && url.slice(1) && url.slice(1) !== 'top' && !localIds.has(url.slice(1))) note('links', r, `missing anchor ${url}`);
  }

  /* 8 · duplicate main copy (boilerplate twins are expected, so hash only the
         first 400 characters of the visible body) */
  const key = text.slice(0, 400);
  if (key.length > 80) { const a = bodyHashes.get(key) || []; a.push(r); bodyHashes.set(key, a); }

  /* 9 · stale / future dates in visible copy */
  const seenYears = new Set();
  for (const m of text.matchAll(/\b(20\d{2})\b/g)) {
    const y = +m[1];
    if (y >= 2026 && y <= 2027) continue;
    if (seenYears.has(y)) continue;
    if (/INV-|№|#/.test(text.slice(Math.max(0, m.index - 4), m.index))) continue; // sample invoice/order numbers
    seenYears.add(y);
    const ctx = text.slice(Math.max(0, m.index - 55), m.index + 55).replace(/\s+/g, ' ');
    note('dates', r, `${y < 2026 ? 'historical / citation' : 'future'} year ${y} — «${ctx}…»`);
  }
}

const noindexRoutes = new Set();
for (const file of pages) {
  const html = readFileSync(file, 'utf8');
  if (/name="robots" content="[^"]*noindex/i.test(html)) noindexRoutes.add(rel(file));
}
for (const [t, files] of titles) if (files.length > 1 && !files.some((f) => f.startsWith('/ar/') || noindexRoutes.has(f))) note('metadata', files.join(' '), `duplicate title: ${t.slice(0, 70)}`);
for (const [d, files] of descriptions) if (files.length > 1 && !files.every((f) => noindexRoutes.has(f))) note('metadata', files.join(' '), `duplicate description: ${d.slice(0, 70)}`);
for (const [k, files] of bodyHashes) if (files.length > 2) note('duplication', files.join(' '), `${files.length} pages open with the same copy`);

/* 10 · media register */
const mediaDir = join(ROOT, 'assets/media');
const webps = readdirSync(mediaDir).filter((f) => f.endsWith('.webp'));
for (const f of webps) {
  const src = '/assets/media/' + f;
  const uses = mediaRefs.get(src) || 0;
  if (!uses) note('media', src, 'unused WebP asset');
  const png = join(mediaDir, basename(f).replace(/-sm\.webp$/, '.png').replace(/\.webp$/, '.png'));
  if (!existsSync(png)) note('media', src, 'no .png source (cannot regenerate)');
}
const ogDir = join(ROOT, 'assets/brand/og');
const ogs = readdirSync(ogDir).filter((f) => f.endsWith('.png'));
const ogUsed = new Set([...pages].flatMap((f) => [...readFileSync(f, 'utf8').matchAll(/\/assets\/brand\/og\/([a-z0-9-]+\.png)/g)].map((m) => m[1])));
for (const f of ogs) if (!ogUsed.has(f)) note('media', '/assets/brand/og/' + f, 'unused OG card');

/* 11 · homepage shipped weight */
const home = readFileSync(join(ROOT, 'index.html'), 'utf8');
const homeRefs = [...home.matchAll(/(?:src|href)="(\/assets\/[^"?#]+|\/_vercel\/[^"?#]+)"/g)].map((m) => m[1]);
let bytes = 0; const assetSizes = [];
for (const a of new Set(homeRefs)) {
  const p = join(ROOT, a.replace(/^\//, ''));
  if (!existsSync(p)) continue;
  const size = statSync(p).size; bytes += size; assetSizes.push([a, size]);
}
const homeImgs = [...home.matchAll(/<img\b[^>]*src="([^"]+)"/gi)].map((m) => m[1]);
/* What a 390px phone actually downloads for homepage artwork: srcset picks
   the 780w variant. Compare that with the 1600w file the old markup served. */
const imgSrcset = [...home.matchAll(/(?:^|\s)srcset="([^"]+)"/g)]
  .flatMap((m) => m[1].split(',').map((c) => c.trim().split(/\s+/)[0]))
  .filter((u) => u.startsWith('/assets/media/'));
const sizeOf = (u) => { const p = join(ROOT, u.replace(/^\//, '')); return existsSync(p) ? statSync(p).size : 0; };
const mobileImageBytes = imgSrcset.filter((u) => u.endsWith('-sm.webp')).reduce((n, u) => n + sizeOf(u), 0);
const desktopImageBytes = imgSrcset.filter((u) => !u.endsWith('-sm.webp')).reduce((n, u) => n + sizeOf(u), 0);
const payload = {
  htmlBytes: Buffer.byteLength(home),
  mobileImageBytes, desktopImageBytes,
  imageSavingPct: desktopImageBytes ? Math.round((1 - mobileImageBytes / desktopImageBytes) * 100) : 0,
  referencedAssetBytes: bytes,
  assetCount: assetSizes.length,
  imageCount: homeImgs.length,
  eagerImages: homeImgs.length ? [...home.matchAll(/<img\b[^>]*>/gi)].filter((m) => /loading="eager"/.test(m[0])).length : 0,
  domElements: (home.match(/<[a-zA-Z][^>]*>/g) || []).length,
  sections: (home.match(/<section\b/g) || []).length,
  visibleWords: words(strip(home)),
  largestAssets: assetSizes.sort((a, b) => b[1] - a[1]).slice(0, 8).map(([a, s]) => `${a} ${(s / 1024).toFixed(0)} KiB`),
};

if (JSON_OUT) {
  console.log(JSON.stringify({ pages: pages.length, findings, payload, media: { webp: webps.length, og: ogs.length, references: Object.fromEntries(mediaRefs) } }, null, 2));
} else {
  const byGroup = {};
  for (const f of findings) (byGroup[f.group] ||= []).push(f);
  console.log(`CONTENT AUDIT — ${pages.length} HTML pages\n`);
  console.log('HOME PAYLOAD');
  for (const [k, v] of Object.entries(payload)) console.log(`  ${k}: ${Array.isArray(v) ? v.join(', ') : v}`);
  console.log(`\nMEDIA REGISTER — ${webps.length} WebP, ${ogs.length} OG cards`);
  for (const [k, v] of [...mediaRefs].sort((a, b) => b[1] - a[1])) console.log(`  ${v.toString().padStart(3)} refs  ${k}`);
  console.log(`\nFINDINGS — ${findings.length}`);
  for (const [group, list] of Object.entries(byGroup).sort()) {
    console.log(`\n  [${group}] ${list.length}`);
    for (const f of list.slice(0, 60)) console.log(`    ${f.file}: ${f.message}`);
    if (list.length > 60) console.log(`    … ${list.length - 60} more`);
  }
  console.log(`\nTotals: ${imgTotal} <img> tags · ${imgEager} eager · ${imgNoAlt} missing alt · ${imgNoDims} missing dimensions · ${imgNoLoading} missing loading · ${imgNoArAlt} EN images missing data-ar-alt`);
}
