#!/usr/bin/env node
/* ==========================================================================
   optimize-media.mjs — converts the studio's illustrative artwork into
   lightweight WebP assets and produces per-route Open Graph cards.

   The generated artwork under assets/media/ is *illustrative studio material*,
   never a client deliverable or a product screenshot. Every use in the site
   carries a visible caption saying so (see docs/ASSET-AND-CLAIM-REGISTER.md).

     node scripts/optimize-media.mjs          # rebuild webp + og/*.png
     node scripts/optimize-media.mjs --check  # verify outputs are current

   Needs devDependencies `sharp` and `@resvg/resvg-js` (npm ci).
   ========================================================================== */
import { readdirSync, readFileSync, writeFileSync, mkdirSync, existsSync, statSync } from 'node:fs';
import { join, basename } from 'node:path';
import { fileURLToPath } from 'node:url';
// `sharp` and `@resvg/resvg-js` are loaded lazily: --check must work without
// native devDependencies (e.g. a static build gate on a minimal runner).

const ROOT = fileURLToPath(new URL('../', import.meta.url));
const MEDIA = join(ROOT, 'assets/media');
const OG = join(ROOT, 'assets/brand/og');
const CHECK = process.argv.includes('--check');
mkdirSync(OG, { recursive: true });
if (!CHECK) {
  var sharp = (await import('sharp')).default;
  var Resvg = (await import('@resvg/resvg-js')).Resvg;
}

/* ---------- 1. Illustrative artwork → WebP ---------- */
const pngs = existsSync(MEDIA) ? readdirSync(MEDIA).filter((f) => f.endsWith('.png')) : [];
let converted = 0;
for (const file of pngs) {
  const src = join(MEDIA, file);
  const dst = join(MEDIA, file.replace(/\.png$/, '.webp'));
  if (CHECK) {
    if (!existsSync(dst)) { console.error(`missing optimized asset: ${dst}`); process.exitCode = 1; }
    continue;
  }
  await sharp(src).resize({ width: 1600, withoutEnlargement: true }).webp({ quality: 82, effort: 6 }).toFile(dst);
  converted += 1;
  console.log(`webp: ${file} → ${basename(dst)}`);
}

/* ---------- 2. Per-route social cards (1200×630) ---------- */
/* Text is rendered from a licensed local TTF; no external fonts or network. */
const FONT = readFileSync(join(ROOT, 'assets/fonts/Raleway-Bold.ttf'));
const FONT_REG = readFileSync(join(ROOT, 'assets/fonts/Poppins-Regular.ttf'));
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

const PALETTES = {
  home: ['#7b5cff', '#25c9b6'], services: ['#6d5bff', '#f05ba3'], work: ['#ee5ba3', '#7b5cff'],
  brand: ['#b18cff', '#ee5ba3'], product: ['#25c9b6', '#7b5cff'], tech: ['#25c9b6', '#4f8cff'],
  health: ['#4f8cff', '#25c9b6'], studio: ['#7b5cff', '#f0b86a'], insights: ['#f05ba3', '#f0b86a'],
  resources: ['#25c9b6', '#f0b86a'], local: ['#f0b86a', '#ee5ba3'], contact: ['#25c9b6', '#7b5cff'],
};

/* slug → [eyebrow, headline, second line, palette] */
const CARDS = {
  'home': ['CODE & CANVAS', 'Brand. Product. System.', 'One business outcome.', 'home'],
  'services': ['SERVICES · 23 OFFERS', 'Four pillars, one studio.', 'Scope, price and timeline.', 'services'],
  'work': ['SELECTED WORK', 'Show the craft,', 'not just the list.', 'work'],
  'case-studies': ['CASE STUDIES', 'Problem · Role · Delivery', 'Evidence, labelled honestly.', 'product'],
  'creative': ['CREATIVE & BRAND', 'Identity that scales', 'into a working system.', 'brand'],
  'technology': ['TECHNOLOGY & DATA', 'Architecture that ships.', 'Not slideware.', 'tech'],
  'healthcare': ['HEALTHCARE', 'Clinical systems,', 'carefully specified.', 'health'],
  'brand-identity-design': ['FLAGSHIP SERVICE', 'Brand Identity Design', 'A system, not a logo.', 'brand'],
  'brand-strategy-systems': ['FLAGSHIP SERVICE', 'Brand Strategy & Systems', 'Decisions before pixels.', 'brand'],
  'packaging-design': ['FLAGSHIP SERVICE', 'Packaging & Print', 'Production-ready artwork.', 'brand'],
  'website-design-development': ['FLAGSHIP SERVICE', 'Websites that convert', 'Bilingual · fast · measurable.', 'product'],
  'product-design-ux': ['FLAGSHIP SERVICE', 'Product Design & UX', 'From problem to interface.', 'product'],
  'healthcare-digital-solutions': ['FLAGSHIP SERVICE', 'Healthcare Digital', 'Interoperability by design.', 'health'],
  'ai-workflow-automation': ['FLAGSHIP SERVICE', 'AI Workflow Automation', 'Automate the right step.', 'tech'],
  'about': ['THE STUDIO', 'Two practices.', 'One table.', 'studio'],
  'team': ['THE PEOPLE', 'The people behind', 'the work.', 'studio'],
  'our-story': ['OUR STORY', 'Why this studio exists.', '', 'studio'],
  'blog': ['INSIGHTS', 'Frameworks and problems', 'from live engagements.', 'insights'],
  'resources': ['RESOURCES', 'Books, guides and', 'free previews.', 'resources'],
  'books': ['DIGITAL LIBRARY', 'Read before you buy', 'the solution.', 'resources'],
  'contact': ['START HERE', 'Tell us the problem.', 'We name the first step.', 'contact'],
  'book': ['BOOK A CALL', '30 minutes, one decision.', 'Arabic or English.', 'contact'],
  'saudi-arabia': ['SAUDI ARABIA', 'Brand, product and', 'systems in KSA.', 'local'],
  'egypt': ['EGYPT', 'Brand, product and', 'systems in Egypt.', 'local'],
  'pricing': ['PRICING & FAQ', 'Indicative ranges.', 'Written scope.', 'services'],
  'methodology': ['METHODOLOGY', 'Listen · Shape · Deliver', 'Milestones in writing.', 'studio'],
  'erp': ['CANVASONE ERP', 'One canvas for', 'the whole operation.', 'tech'],
  'privacy': ['LEGAL', 'Privacy Policy', '', 'studio'],
  'bilingual-brand-system': ['CONCEPT STUDY · BRAND', 'A bilingual brand system', 'Method, not client work.', 'brand'],
  'packaging-print-system': ['CONCEPT STUDY · PRINT', 'Shelf to print-ready', 'Production spec included.', 'brand'],
  'product-ui-system': ['CONCEPT STUDY · PRODUCT', 'One decision, one system.', 'Interface + tokens.', 'product'],
  'web-experience-rebuild': ['CONCEPT STUDY · WEB', 'Before / after a site', 'Proof, then one CTA.', 'product'],
  'blog-brand-systems': ['INSIGHT · BRAND', 'From identity', 'to brand systems.', 'brand'],
  'blog-ai-strategy': ['INSIGHT · AI', 'When options are free,', 'judgment is scarce.', 'insights'],
  'claims': ['PUBLIC REGISTER', 'Every number,', 'with a stated status.', 'studio'],
};

function svgFor([kicker, line1, line2, palette]) {
  const [a, b] = PALETTES[palette] || PALETTES.home;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#080824"/><stop offset="1" stop-color="#05051a"/></linearGradient>
    <linearGradient id="glow" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="${a}"/><stop offset="1" stop-color="${b}"/></linearGradient>
    <radialGradient id="orb"><stop offset="0" stop-color="${a}" stop-opacity=".55"/><stop offset="1" stop-color="${a}" stop-opacity="0"/></radialGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#bg)"/>
  <circle cx="980" cy="140" r="330" fill="url(#orb)"/>
  <circle cx="1080" cy="520" r="260" fill="url(#orb)" opacity=".45"/>
  <g opacity=".22" stroke="#ffffff" stroke-width="1">
    ${Array.from({ length: 13 }, (_, i) => `<line x1="${i * 100}" y1="0" x2="${i * 100}" y2="630"/>`).join('')}
    ${Array.from({ length: 7 }, (_, i) => `<line x1="0" y1="${i * 100}" x2="1200" y2="${i * 100}"/>`).join('')}
  </g>
  <g fill="none" stroke="url(#glow)" stroke-width="3" opacity=".85">
    <rect x="880" y="300" width="230" height="230" rx="18" transform="rotate(-9 995 415)"/>
    <rect x="930" y="350" width="230" height="230" rx="18" transform="rotate(7 1045 465)" opacity=".6"/>
  </g>
  <rect x="72" y="72" width="46" height="46" rx="12" fill="url(#glow)"/>
  <text x="136" y="105" font-family="Raleway" font-size="22" font-weight="700" letter-spacing="3" fill="#ffffff">CODE &amp; CANVAS</text>
  <text x="72" y="238" font-family="Poppins" font-size="19" font-weight="400" letter-spacing="4" fill="${b}">${esc(kicker)}</text>
  <text x="72" y="330" font-family="Raleway" font-size="62" font-weight="700" fill="#ffffff">${esc(line1)}</text>
  ${line2 ? `<text x="72" y="410" font-family="Raleway" font-size="62" font-weight="700" fill="url(#glow)">${esc(line2)}</text>` : ''}
  <line x1="72" y1="486" x2="650" y2="486" stroke="url(#glow)" stroke-width="2" opacity=".7"/>
  <text x="72" y="540" font-family="Poppins" font-size="20" fill="#a9a9c8">Strategy · Design · Technology  |  codeandcanvas.net</text>
</svg>`;
}

let ogCount = 0;
for (const [slug, card] of Object.entries(CARDS)) {
  const out = join(OG, `${slug}.png`);
  if (CHECK) { if (!existsSync(out)) { console.error(`missing OG card: ${out}`); process.exitCode = 1; } continue; }
  const png = new Resvg(svgFor(card), {
    fitTo: { mode: 'width', value: 1200 },
    font: { fontFiles: ['assets/fonts/Raleway-Bold.ttf', 'assets/fonts/Poppins-Regular.ttf'], loadSystemFonts: false, defaultFontFamily: 'Raleway' },
    background: '#05051a',
  }).render().asPng();
  writeFileSync(out, png);
  ogCount += 1;
}
console.log(CHECK ? `media check: ${pngs.length} source(s), ${Object.keys(CARDS).length} OG card(s)` : `done: ${converted} WebP, ${ogCount} OG cards`);
