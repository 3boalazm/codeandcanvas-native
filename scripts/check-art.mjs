#!/usr/bin/env node
/* ==========================================================================
   check-art.mjs — every published plate is ours and is labelled.

   2026-11-09 page-artwork pass. The generator scripts/generate-page-art.mjs
   derives plates from assets already committed here; this check fails the
   build chain if that promise breaks:

     1. every generated plate has both a full-size and a `-sm` WebP variant
        (a missing phone variant would silently ship 1600px to phones);
     2. no published page hotlinks an image from another origin — the only
        allowed sources are /assets/… on this origin;
     3. every plate sits inside a figure that carries the illustrative
        disclaimer text, in both language twins.

   It complements check-claims.mjs (wording), optimize-media.mjs --check
   (derivatives exist) and check-phase3.mjs (no third-party assets).
   ========================================================================== */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = (p) => { try { return fs.readFileSync(p, 'utf8'); } catch { return ''; } };
const exists = (p) => fs.existsSync(path.join(ROOT, p));

/* Plates produced by scripts/generate-page-art.mjs. Keep in sync with ART there. */
const PLATES = [
  'hero-creative', 'hero-work', 'hero-pricing', 'art-resources',
  'art-story-architecture', 'art-story-identity', 'art-story-healthcare',
  'art-story-data', 'art-story-media', 'hero-services-geo', 'hero-offer',
  'art-contact-arc', 'art-book-steps', 'art-pricing-tiers', 'art-erp-modules',
  'art-duo-practices', 'art-clinical-lanes', 'art-arch-stack', 'art-brand-acts',
  'art-work-ledger',
];

/* Pages that must carry a plate + disclaimer. */
const PLACEMENTS = [
  ['services/index.html', 'hero-services-geo'],
  ['ar/services/index.html', 'hero-services-geo'],
  ['services/brand-identity-design/index.html', 'hero-offer'],
  ['technology-services/index.html', 'art-arch-stack'],
  ['ar/technology-services/index.html', 'art-arch-stack'],
  ['creative-services/index.html', 'art-brand-acts'],
  ['ar/creative-services/index.html', 'art-brand-acts'],
  ['healthcare/index.html', 'art-clinical-lanes'],
  ['ar/healthcare/index.html', 'art-clinical-lanes'],
  ['contact/index.html', 'art-contact-arc'],
  ['ar/contact/index.html', 'art-contact-arc'],
  ['book/index.html', 'art-book-steps'],
  ['ar/book/index.html', 'art-book-steps'],
  ['pricing-faq/index.html', 'art-pricing-tiers'],
  ['ar/pricing-faq/index.html', 'art-pricing-tiers'],
  ['about/index.html', 'art-duo-practices'],
  ['ar/about/index.html', 'art-duo-practices'],
  ['team/index.html', 'art-duo-practices'],
  ['ar/team/index.html', 'art-duo-practices'],
  ['case-studies/index.html', 'art-work-ledger'],
  ['resources/index.html', 'art-resources'],
  ['ar/resources/index.html', 'art-resources'],
  ['erp/index.html', 'art-erp-modules'],
  ['ar/erp/index.html', 'art-erp-modules'],
  ['our-story/index.html', 'art-story-architecture'],
  ['ar/our-story/index.html', 'art-story-architecture'],
  ['blog/index.html', 'hero-pricing'],
];

/* Every visible plate keeps an illustrative qualifier, EN or AR. */
const DISCLAIMER = /ILLUSTRATIVE|NOT A MAP|NOT A PRODUCT SCREENSHOT|توضيحي/;

const problems = [];

for (const plate of PLATES) {
  for (const variant of ['', '-sm']) {
    const webp = `assets/media/${plate}${variant}.webp`;
    const png = `assets/media/${plate}.png`;
    if (!exists(webp)) problems.push(`missing derivative ${webp}`);
    if (!exists(png)) problems.push(`missing source ${png} (generate-page-art.mjs)`);
  }
}

for (const [page, plate] of PLACEMENTS) {
  const html = read(path.join(ROOT, page));
  if (!html) { problems.push(`${page}: missing page`); continue; }
  if (!html.includes(`/assets/media/${plate}.webp`)) problems.push(`${page}: expected plate ${plate}`);
  /* The image and its qualifier must stay together: look in the enclosing
     <figure>, or failing that in a plate container / the next 600 characters,
     so a later edit cannot move the caption away from the artwork. */
  const idx = html.indexOf(`/assets/media/${plate}.webp`);
  const figStart = html.lastIndexOf('<figure', idx);
  const figEnd = html.indexOf('</figure>', idx);
  const inFigure = figStart !== -1 && figEnd !== -1 && html.slice(0, idx).lastIndexOf('<figure') > html.slice(0, idx).lastIndexOf('</figure>');
  const window = inFigure
    ? html.slice(figStart, figEnd)
    : html.slice(Math.max(0, idx - 400), idx + 600);
  if (!inFigure) {
    const container = /class="[^"]*(?:story-plate|feat-post__plate|art--map)[^"]*"/.test(window);
    if (!container) problems.push(`${page}: ${plate} is not inside a <figure> or a labelled plate container`);
  }
  if (!DISCLAIMER.test(window)) problems.push(`${page}: ${plate} has no illustrative qualifier next to it`);
}

/* No hotlinked imagery anywhere in the published tree. */
const walk = (dir) => {
  const out = [];
  const skip = new Set(['node_modules', 'dist', 'REF', '.git', '.qa-ref', 'test-results', 'playwright-report']);
  const go = (d) => {
    for (const e of fs.readdirSync(d, { withFileTypes: true })) {
      if (skip.has(e.name)) continue;
      const p = path.join(d, e.name);
      if (e.isDirectory()) go(p);
      else if (e.name.endsWith('.html')) out.push(p);
    }
  };
  go(dir);
  return out;
};
for (const file of walk(ROOT)) {
  const html = read(file);
  const rel = path.relative(ROOT, file);
  for (const m of html.matchAll(/<img\b[^>]*\bsrc="([^"]+)"/gi)) {
    const src = m[1];
    if (/^(?:https?:)?\/\//i.test(src) && !src.startsWith('//codeandcanvas.net')) {
      problems.push(`${rel}: hotlinked image ${src}`);
    }
  }
}

if (problems.length) {
  console.error(`art check: ${problems.length} problem(s):`);
  for (const p of problems) console.error('  - ' + p);
  process.exit(1);
}
console.log(`art check: ok — ${PLATES.length} first-party plates (2 variants each), ${PLACEMENTS.length} labelled placements, 0 hotlinked images`);
