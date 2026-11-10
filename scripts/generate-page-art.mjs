#!/usr/bin/env node
/* ==========================================================================
   generate-page-art.mjs — first-party illustrative artwork for the pages that
   had no visual at all.

   PROVENANCE: every pixel here comes from this repository. There is no network
   call, no stock image, no screenshot, no client photo, no third-party mark and
   no fabricated product UI. Each output is one of:

     1. a crop / reframe / re-grade of an already committed studio artwork PNG
        under assets/media/ (the same abstract 3D scenes the site already shows),
     2. an original SVG drawn here from the site's own geometry + the committed
        brand palette, composited over one of those scenes.

   The composites follow the pattern already documented for
   scripts/generate-case-art.mjs. Every visible placement keeps a bilingual
   `alt` / `data-ar-alt`, an on-page qualifier such as
   `ILLUSTRATIVE ARTWORK · NOT CLIENT WORK`, and `scripts/check-claims.mjs`
   stays the enforcement point for wording. See
   docs/ASSET-AND-CLAIM-REGISTER.md for the provenance table.

     node scripts/generate-page-art.mjs
   ========================================================================== */
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';
import { Resvg } from '@resvg/resvg-js';

const ROOT = fileURLToPath(new URL('../', import.meta.url));
const MEDIA = join(ROOT, 'assets', 'media');
const W = 1600;
const H = 900;

/* ---------- palette (assets/css/ds.css) ---------- */
const NAVY = '#05051a';
const VIOLET = '#7b5cff';
const TEAL = '#25c9b6';
const PINK = '#ee5ba3';
const BLUE = '#4f8cff';
const GOLD = '#f0b86a';

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

const defs = (a, b, c) => `<defs>
  <linearGradient id="g1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${a}"/><stop offset=".55" stop-color="${b}"/><stop offset="1" stop-color="${c}"/></linearGradient>
  <linearGradient id="g2" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="${c}"/><stop offset="1" stop-color="${a}"/></linearGradient>
  <radialGradient id="orb"><stop offset="0" stop-color="${b}" stop-opacity=".55"/><stop offset="1" stop-color="${b}" stop-opacity="0"/></radialGradient>
  <radialGradient id="orb2"><stop offset="0" stop-color="${a}" stop-opacity=".42"/><stop offset="1" stop-color="${a}" stop-opacity="0"/></radialGradient>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.4" fill="#ffffff" opacity=".22"/></pattern>
</defs>`;

const shell = (a, b, c, geometry) => `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
${defs(a, b, c)}
<rect width="${W}" height="${H}" fill="${NAVY}" opacity=".72"/>
<circle cx="1290" cy="150" r="400" fill="url(#orb)"/>
<circle cx="240" cy="790" r="360" fill="url(#orb2)"/>
<rect width="${W}" height="${H}" fill="url(#dots)" opacity=".5"/>
${geometry}
</svg>`;

const label = (text, opts = {}) => {
  const { x = 96, y = 806, size = 26, fill = '#ffffff', opacity = '.72', font = 'Poppins', weight = 400, spacing = 6 } = opts;
  return `<text x="${x}" y="${y}" font-family="${font}" font-size="${size}" font-weight="${weight}" letter-spacing="${spacing}" fill="${fill}" opacity="${opacity}">${esc(text)}</text>`;
};

/* ---------- 1. crops / re-grades of our own artwork ----------
   `zoom` crops in on the source (1 = full frame), `grade` shifts the tone,
   `flip` mirrors it so a reuse never looks like the same picture twice.   */
const CROPS = [
  {
    file: 'hero-creative.png', base: 'brand-system.png',
    zoom: 1.2, x: 0.5, y: 0.48, flip: false, brightness: 0.95, saturation: 1.16, hue: 10,
    label: 'BRAND SYSTEM · BILINGUAL AR / EN',
  },
  {
    file: 'art-story-architecture.png', base: 'case-evolve.png',
    zoom: 1.28, x: 0.5, y: 0.44, flip: false, brightness: 0.88, saturation: 1.04, hue: -8,
    label: 'PRACTICE 01 · TECHNOLOGY & ARCHITECTURE',
  },
  {
    file: 'art-story-identity.png', base: 'case-packbox.png',
    zoom: 1.26, x: 0.46, y: 0.5, flip: true, brightness: 0.9, saturation: 1.14, hue: 12,
    label: 'PRACTICE 02 · BRAND IDENTITY & CREATIVE',
  },
  {
    file: 'art-story-healthcare.png', base: 'case-pharmacy.png',
    zoom: 1.34, x: 0.34, y: 0.36, flip: false, brightness: 0.86, saturation: 1.02, hue: 0,
    label: 'PRACTICE 03 · HEALTHCARE VERTICAL',
  },
  {
    file: 'art-story-data.png', base: 'case-sakanwave.png',
    zoom: 1.3, x: 0.62, y: 0.5, flip: false, brightness: 0.84, saturation: 1.06, hue: 8,
    label: 'PRACTICE 04 · DATA & ANALYTICS',
  },
  {
    file: 'art-story-media.png', base: 'case-stt.png',
    zoom: 1.24, x: 0.5, y: 0.58, flip: true, brightness: 0.88, saturation: 1.1, hue: -6,
    label: 'PRACTICE 05 · MEDIA & CONTENT PRODUCTION',
  },
  {
    file: 'hero-work.png', base: 'case-axiom.png',
    zoom: 1.2, x: 0.55, y: 0.5, flip: true, brightness: 0.92, saturation: 1.08, hue: 6,
    label: 'DOCUMENTED WORK · LABELLED EVIDENCE',
  },
  {
    file: 'art-resources.png', base: 'case-ummah.png',
    zoom: 1.22, x: 0.42, y: 0.52, flip: false, brightness: 0.94, saturation: 1.1, hue: 14,
    label: 'BOOKS · GUIDES · FREE PREVIEWS',
  },
  {
    file: 'hero-pricing.png', base: 'case-npf.png',
    zoom: 1.24, x: 0.5, y: 0.5, flip: true, brightness: 0.9, saturation: 1.05, hue: -4,
    label: 'PUBLISHED SCOPE · PUBLISHED PRICE',
  },
];

/* ---------- 2. original geometry composited over our own scenes ----------
   Same technique as scripts/generate-case-art.mjs: a defocused, darkened
   crop of a committed artwork plus an SVG layer drawn from scratch.       */
const column = (x, y, h, color, heights) => {
  const bw = 44;
  const gap = 18;
  const bars = heights.map((v, i) => `<rect x="${x}" y="${y + h - v}" width="${bw}" height="${v}" rx="8" fill="${color}" opacity="${.28 + i * .09}"/>`).join('');
  return `<g>${bars}<line x1="${x - 12}" y1="${y + h}" x2="${x + heights.length * (bw + gap)}" y2="${y + h}" stroke="#ffffff" stroke-width="2" opacity=".28"/></g>`;
};

const COMPOSITES = [
  {
    /* /services/ — four tracks as four connected lanes */
    file: 'hero-services-geo.png', base: 'hero-system.png', a: VIOLET, b: TEAL, c: PINK,
    shapes: `
      ${[0, 1, 2, 3].map((i) => `<path d="M140 ${300 + i * 110} C 480 ${300 + i * 110}, 720 ${330 + i * 60}, 1440 ${280 + i * 96}" fill="none" stroke="${[VIOLET, TEAL, PINK, BLUE][i]}" stroke-width="${7 - i}" opacity="${.85 - i * .12}" stroke-linecap="round"/>`).join('')}
      ${[[300, 300], [560, 410], [900, 480], [1180, 330]].map(([x, y], i) => `<circle cx="${x}" cy="${y}" r="${26 - i * 3}" fill="${NAVY}" stroke="${[VIOLET, TEAL, PINK, BLUE][i]}" stroke-width="4"/><circle cx="${x}" cy="${y}" r="${8 - i}" fill="${[VIOLET, TEAL, PINK, BLUE][i]}"/>`).join('')}
      <rect x="980" y="560" width="420" height="180" rx="22" fill="${NAVY}" opacity=".72" stroke="#ffffff" stroke-opacity=".16"/>
      ${[0, 1, 2, 3].map((i) => `<rect x="1016" y="${600 + i * 34}" width="${340 - i * 54}" height="12" rx="6" fill="${[VIOLET, TEAL, PINK, BLUE][i]}" opacity=".7"/>`).join('')}
      ${label('23 SERVICES · FOUR TRACKS')}`,
  },
  {
    /* /services/<slug>/ landing pages — one orbit per flagship offer */
    file: 'hero-offer.png', base: 'case-axiom.png', a: GOLD, b: VIOLET, c: TEAL,
    shapes: `
      <g fill="none" stroke="url(#g1)" stroke-width="3" opacity=".8">
        <circle cx="1090" cy="430" r="250"/><circle cx="1090" cy="430" r="180" opacity=".7"/><circle cx="1090" cy="430" r="110" opacity=".6"/>
      </g>
      <circle cx="1090" cy="430" r="58" fill="url(#g1)" opacity=".35"/>
      ${[[1090, 180], [1315, 320], [1260, 640], [900, 560], [860, 300]].map(([x, y], i) => `<circle cx="${x}" cy="${y}" r="13" fill="${[GOLD, VIOLET, TEAL, PINK, BLUE][i]}"/>`).join('')}
      ${[0, 1, 2].map((i) => `<rect x="120" y="${280 + i * 74}" width="${420 - i * 90}" height="18" rx="9" fill="#ffffff" opacity="${.3 - i * .07}"/>`).join('')}
      ${label('FLAGSHIP OFFER · PUBLISHED SCOPE')}`,
  },
  {
    /* /contact/ — three cities on one arc (no map tiles, no third-party data) */
    file: 'art-contact-arc.png', base: 'studio-atmosphere.png', a: TEAL, b: GOLD, c: VIOLET,
    shapes: `
      <path d="M200 640 C 460 400, 780 400, 1080 560 S 1320 700, 1420 620" fill="none" stroke="url(#g1)" stroke-width="4" stroke-dasharray="14 16" opacity=".85"/>
      ${[['RIYADH', 340, 470], ['AL KHOBAR', 820, 404], ['CAIRO', 1180, 606]].map(([city, x, y], i) => `<g><circle cx="${x}" cy="${y}" r="26" fill="${NAVY}" stroke="${[TEAL, GOLD, VIOLET][i]}" stroke-width="4"/><circle cx="${x}" cy="${y}" r="9" fill="${[TEAL, GOLD, VIOLET][i]}"/><rect x="${x - 18}" y="${y + 78}" width="${city.length * 15 + 26}" height="40" rx="20" fill="${NAVY}" opacity=".78"/><text x="${x - 4}" y="${y + 106}" font-family="Poppins" font-size="21" letter-spacing="4" fill="#ffffff" opacity=".85">${city}</text></g>`).join('')}
      ${label('ONE MESSAGE · ONE BUSINESS DAY')}`,
  },
  {
    /* /book/ — three settled steps toward one call */
    file: 'art-book-steps.png', base: 'case-continuum.png', a: TEAL, b: VIOLET, c: GOLD,
    shapes: `
      ${[0, 1, 2].map((i) => `<g><rect x="${420 + i * 280}" y="${560 - i * 90}" width="220" height="120" rx="20" fill="${NAVY}" opacity=".8" stroke="${[TEAL, VIOLET, GOLD][i]}" stroke-width="3"/><text x="${492 + i * 280}" y="${636 - i * 90}" font-family="Poppins" font-size="40" font-weight="600" fill="${[TEAL, VIOLET, GOLD][i]}">0${i + 1}</text></g>`).join('')}
      <path d="M560 520 C 700 470, 720 470, 840 430" fill="none" stroke="#ffffff" stroke-width="3" opacity=".45" stroke-dasharray="10 14"/>
      <path d="M840 340 C 980 290, 1000 290, 1120 250" fill="none" stroke="#ffffff" stroke-width="3" opacity=".45" stroke-dasharray="10 14"/>
      ${label('SPECIALTY · SLOT · CONFIRMATION')}`,
  },
  {
    /* /pricing-faq/ — three published tiers */
    file: 'art-pricing-tiers.png', base: 'case-npf.png', a: GOLD, b: PINK, c: VIOLET,
    shapes: `
      ${[0, 1, 2].map((i) => `<g><rect x="${380 + i * 300}" y="${300 + i * 40}" width="240" height="${420 - i * 80}" rx="26" fill="${NAVY}" opacity=".78" stroke="${[TEAL, GOLD, PINK][i]}" stroke-width="3"/><rect x="${412 + i * 300}" y="${340 + i * 40}" width="120" height="14" rx="7" fill="${[TEAL, GOLD, PINK][i]}" opacity=".8"/>${[0, 1, 2, 3].map((j) => `<rect x="${412 + i * 300}" y="${392 + i * 40 + j * 34}" width="${176 - j * 18}" height="10" rx="5" fill="#ffffff" opacity=".24"/>`).join('')}</g>`).join('')}
      ${label('PUBLISHED RANGES · WRITTEN SCOPE')}`,
  },
  {
    /* /erp/ — modules wired to one canvas (SVG only, no fake product UI) */
    file: 'art-erp-modules.png', base: 'digital-product.png', a: VIOLET, b: TEAL, c: BLUE,
    shapes: `
      <g fill="none" stroke="url(#g1)" stroke-width="3" opacity=".55">
        ${[[420, 300], [420, 560], [1180, 300], [1180, 560], [800, 210], [800, 650]].map(([x, y]) => `<path d="M800 430 L ${x} ${y}"/>`).join('')}
      </g>
      <rect x="690" y="320" width="220" height="220" rx="30" fill="${NAVY}" stroke="url(#g2)" stroke-width="4"/>
      <rect x="742" y="372" width="116" height="116" rx="18" fill="url(#g1)" opacity=".3"/>
      ${[[420, 300, 'FINANCE'], [420, 560, 'SALES'], [1180, 300, 'INVENTORY'], [1180, 560, 'HR'], [800, 210, 'E-INVOICING'], [800, 650, 'REPORTING']].map(([x, y, t]) => `<g><rect x="${x - 92}" y="${y - 46}" width="184" height="92" rx="20" fill="${NAVY}" opacity=".82" stroke="#ffffff" stroke-opacity=".22"/><text x="${x - 76}" y="${y + 8}" font-family="Poppins" font-size="19" letter-spacing="2" fill="#ffffff" opacity=".8">${t}</text></g>`).join('')}
      ${label('CANVASONE · MODULES ON ONE CANVAS')}`,
  },
  {
    /* /about/ + /team/ — two disciplines, one table */
    file: 'art-duo-practices.png', base: 'studio-atmosphere.png', a: VIOLET, b: PINK, c: TEAL,
    shapes: `
      <circle cx="600" cy="430" r="215" fill="none" stroke="url(#g1)" stroke-width="4" opacity=".85"/>
      <circle cx="980" cy="430" r="215" fill="none" stroke="url(#g2)" stroke-width="4" opacity=".85"/>
      <circle cx="600" cy="430" r="150" fill="${VIOLET}" opacity=".14"/>
      <circle cx="980" cy="430" r="150" fill="${TEAL}" opacity=".14"/>
      <circle cx="790" cy="430" r="90" fill="${NAVY}" stroke="#ffffff" stroke-opacity=".28" stroke-width="3"/>
      <circle cx="790" cy="430" r="30" fill="url(#g1)" opacity=".6"/>
      ${label('ARCHITECT & ARTIST · ONE SHARED BRIEF')}`,
  },
  {
    /* /healthcare/ — clinical readiness lanes, deliberately unlabelled numbers */
    file: 'art-clinical-lanes.png', base: 'case-pharmacy.png', a: TEAL, b: BLUE, c: VIOLET,
    shapes: `
      ${[0, 1, 2, 3, 4].map((i) => `<rect x="${300 + i * 210}" y="${640 - i * 84}" width="150" height="${84 + i * 84}" rx="18" fill="url(#g1)" opacity="${.16 + i * .1}"/>`).join('')}
      <path d="M300 640 L 1380 260" fill="none" stroke="${TEAL}" stroke-width="3" stroke-dasharray="12 14" opacity=".7"/>
      ${[['ASSESS', 300, 700], ['SCORE', 720, 560], ['GAP', 1140, 420], ['ROADMAP', 1300, 260]].map(([t, x, y]) => `<text x="${x}" y="${y}" font-family="Poppins" font-size="20" letter-spacing="3" fill="#ffffff" opacity=".62">${t}</text>`).join('')}
      ${label('READINESS CRITERIA · NO INVENTED METRICS')}`,
  },
  {
    /* /technology-services/ — one architecture stack, four layers */
    file: 'art-arch-stack.png', base: 'case-nile-bed.png', a: BLUE, b: VIOLET, c: TEAL,
    shapes: `
      ${[0, 1, 2, 3].map((i) => `<g><rect x="${420 - i * 34}" y="${250 + i * 130}" width="${760 + i * 68}" height="96" rx="18" fill="${NAVY}" opacity=".8" stroke="${[BLUE, VIOLET, TEAL, GOLD][i]}" stroke-width="3"/><rect x="${460 - i * 30}" y="${282 + i * 130}" width="${210 - i * 10}" height="14" rx="7" fill="${[BLUE, VIOLET, TEAL, GOLD][i]}" opacity=".7"/></g>`).join('')}
      ${[[300, 300], [1300, 300], [300, 690], [1300, 690]].map(([x, y], i) => `<circle cx="${x}" cy="${y}" r="12" fill="${[BLUE, VIOLET, TEAL, GOLD][i]}"/>`).join('')}
      ${label('BUSINESS · DATA · APPLICATION · TECHNOLOGY')}`,
  },
  {
    /* /creative-services/ — the four-act brand method */
    file: 'art-brand-acts.png', base: 'brand-system.png', a: PINK, b: VIOLET, c: GOLD,
    shapes: `
      ${[0, 1, 2, 3].map((i) => `<g><rect x="${380 + i * 250}" y="${360 - i * 46}" width="190" height="300" rx="24" fill="${NAVY}" opacity=".76" stroke="${[PINK, VIOLET, TEAL, GOLD][i]}" stroke-width="3"/><text x="${400 + i * 250}" y="${420 - i * 46}" font-family="Poppins" font-size="32" font-weight="600" fill="${[PINK, VIOLET, TEAL, GOLD][i]}" opacity=".9">${i + 1}</text>${[0, 1].map((j) => `<rect x="${400 + i * 250}" y="${470 - i * 46 + j * 40}" width="${140 - j * 30}" height="10" rx="5" fill="#ffffff" opacity=".26"/>`).join('')}</g>`).join('')}
      ${label('DISCOVERY · STRATEGY · CONCEPT · REFINE')}`,
  },
  {
    /* /work/ index — a labelled evidence ledger */
    file: 'art-work-ledger.png', base: 'case-maqloop.png', a: TEAL, b: PINK, c: VIOLET,
    shapes: `
      ${[0, 1, 2, 3, 4].map((i) => `<g><rect x="${360 + i * 180}" y="${300 + (i % 2) * 90}" width="150" height="270" rx="20" fill="${NAVY}" opacity=".72" stroke="${[TEAL, PINK, VIOLET, GOLD, BLUE][i]}" stroke-width="3"/><rect x="${386 + i * 180}" y="${336 + (i % 2) * 90}" width="98" height="12" rx="6" fill="${[TEAL, PINK, VIOLET, GOLD, BLUE][i]}" opacity=".8"/>${[0, 1, 2].map((j) => `<rect x="${386 + i * 180}" y="${392 + (i % 2) * 90 + j * 34}" width="${84 - j * 12}" height="9" rx="4" fill="#ffffff" opacity=".2"/>`).join('')}</g>`).join('')}
      ${label('PROBLEM · ROLE · DELIVERY · LIMITS')}`,
  },
];

/* ---------- run ---------- */
const done = [];

for (const c of CROPS) {
  const src = join(MEDIA, c.base);
  if (!existsSync(src)) throw new Error(`missing base artwork: ${c.base}`);
  const meta = await sharp(src).metadata();
  const cw = Math.round(meta.width / c.zoom);
  const ch = Math.round(cw * (H / W));
  const left = Math.max(0, Math.min(meta.width - cw, Math.round(meta.width * c.x - cw / 2)));
  const top = Math.max(0, Math.min(meta.height - ch, Math.round(meta.height * c.y - ch / 2)));
  let img = sharp(src).extract({ left, top, width: cw, height: ch }).resize(W, H, { fit: 'cover' });
  if (c.flip) img = img.flop();
  img = img.modulate({ brightness: c.brightness, saturation: c.saturation, hue: c.hue });
  const png = await img.png({ compressionLevel: 9 }).toBuffer();
  /* A hairline caption strip keeps every derived plate identifiable on-page. */
  const strip = new Resvg(`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
    <rect x="0" y="${H - 96}" width="${W}" height="96" fill="${NAVY}" opacity=".42"/>
    ${label(c.label, { y: H - 38, size: 24, opacity: '.82', spacing: 7 })}
  </svg>`, { fitTo: { mode: 'width', value: W }, font: { fontFiles: ['assets/fonts/Poppins-Regular.ttf'], loadSystemFonts: false, defaultFontFamily: 'Poppins' }, background: 'rgba(0,0,0,0)' }).render().asPng();
  const out = await sharp(png).composite([{ input: strip, blend: 'over' }]).png({ compressionLevel: 9 }).toBuffer();
  writeFileSync(join(MEDIA, c.file), out);
  done.push(`${c.file} ← ${c.base} (crop+grade)`);
}

for (const c of COMPOSITES) {
  const src = join(MEDIA, c.base);
  if (!existsSync(src)) throw new Error(`missing base artwork: ${c.base}`);
  const svg = shell(c.a, c.b, c.c, c.shapes);
  const layer = new Resvg(svg, {
    fitTo: { mode: 'width', value: W },
    font: { fontFiles: ['assets/fonts/Poppins-Regular.ttf', 'assets/fonts/Raleway-Bold.ttf'], loadSystemFonts: false, defaultFontFamily: 'Poppins' },
    background: 'rgba(5,5,26,0)',
  }).render().asPng();
  const base = await sharp(src).resize(W, H, { fit: 'cover' }).blur(22).modulate({ brightness: .5, saturation: .85 }).png().toBuffer();
  const out = await sharp(base).composite([{ input: layer, blend: 'over' }]).png({ compressionLevel: 9 }).toBuffer();
  writeFileSync(join(MEDIA, c.file), out);
  done.push(`${c.file} ← ${c.base} (original SVG geometry)`);
}

console.log(`generated ${done.length} first-party artwork file(s):`);
for (const d of done) console.log('  ' + d);
