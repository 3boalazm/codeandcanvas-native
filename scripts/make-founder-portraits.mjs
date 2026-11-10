#!/usr/bin/env node
/* ==========================================================================
   make-founder-portraits.mjs — crop the owner's founder photographs into the
   two WebP sizes the site serves.

   The originals live in assets/brand/Brand Owners/ and are committed as
   supplied. This script does not retouch, retint, composite or generate
   anything: it only extracts a 4:5 region and writes two widths, so the crop
   is reproducible instead of being a hand-made file nobody can regenerate.

     node scripts/make-founder-portraits.mjs          # write the WebP files
     node scripts/make-founder-portraits.mjs --check  # fail if they are stale

   Provenance and the open question about the printed emblem on both garments
   are recorded in docs/ASSET-AND-CLAIM-REGISTER.md.
   ========================================================================== */
import { existsSync, statSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = fileURLToPath(new URL('../', import.meta.url));
const SRC = join(ROOT, 'assets/brand/Brand Owners');
const OUT = join(ROOT, 'assets/media');
const CHECK = process.argv.includes('--check');

/* 4:5 crops. The face stays in the upper third and the printed emblem on the
   garment stays in frame, because it is visible in both photographs and the
   crop must not imply it was removed. */
const JOBS = [
  {
    id: 'founder-ahmed', file: 'Ahmed Bedeer.jpeg',
    region: { left: 96, top: 30, width: 832, height: 1040 },
    alt: 'Ahmed M. Bedeer, co-founder, photographed in the studio',
  },
  {
    id: 'founder-mustafa', file: 'Mustafa Aboalazm.png',
    region: { left: 24, top: 0, width: 720, height: 900 },
    alt: 'Mustafa Aboalazm, co-founder, photographed in profile against a warm backdrop',
  },
];

const VARIANTS = [
  { suffix: '', width: 800, quality: 84 },
  { suffix: '-sm', width: 400, quality: 78 },
];

mkdirSync(OUT, { recursive: true });
let missing = 0;
for (const job of JOBS) {
  const src = join(SRC, job.file);
  if (!existsSync(src)) { console.error(`missing supplied photograph: assets/brand/Brand Owners/${job.file}`); missing += 1; continue; }
  for (const v of VARIANTS) {
    const dst = join(OUT, `${job.id}${v.suffix}.webp`);
    if (CHECK) {
      if (!existsSync(dst)) { console.error(`missing portrait variant: assets/media/${job.id}${v.suffix}.webp`); missing += 1; continue; }
      // The photograph must not be older than the crop, or the crop is stale.
      if (statSync(dst).mtimeMs + 1000 < statSync(src).mtimeMs) {
        console.error(`stale portrait: assets/media/${job.id}${v.suffix}.webp predates ${job.file}`);
        missing += 1;
      }
      continue;
    }
    const sharp = (await import('sharp')).default;
    await sharp(src).extract(job.region).resize({ width: v.width })
      .webp({ quality: v.quality, effort: 6 }).toFile(dst);
    console.log(`portrait: ${job.file} → ${job.id}${v.suffix}.webp (${v.width}px)`);
  }
}
if (missing) { console.error(`make-founder-portraits: ${missing} problem(s)`); process.exit(1); }
console.log(CHECK
  ? `make-founder-portraits: ok — ${JOBS.length * VARIANTS.length} portrait variants current`
  : `make-founder-portraits: wrote ${JOBS.length * VARIANTS.length} variants`);
