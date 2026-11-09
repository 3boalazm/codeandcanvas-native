#!/usr/bin/env node
/* Deterministic PWA / home-screen icons, rendered from the site's own brand SVG.

   No photography, client mark or third-party artwork is used. Every icon is a
   navy field with the white Code & Canvas squircle, so iOS (which does not show
   transparency) and Android maskable masks both keep a readable mark inside the
   safe zone. Run after changing assets/brand/icon-white.svg:

       node scripts/generate-app-icons.mjs

   Output: assets/brand/app/*.png  (see docs/PWA.md)
*/
import { readFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const ROOT = fileURLToPath(new URL('../', import.meta.url));
const OUT = join(ROOT, 'assets', 'brand', 'app');
const MARK = readFileSync(join(ROOT, 'assets', 'brand', 'icon-white.svg'));
mkdirSync(OUT, { recursive: true });

const NAVY = '#05051a';

/* A very soft violet halo keeps the flat navy from looking like a dead square,
   while staying subtle enough that a maskable crop still reads as one mark. */
const backdrop = (size) => Buffer.from(
  `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}">
     <defs><radialGradient id="g" cx="50%" cy="42%" r="65%">
       <stop offset="0%" stop-color="#241a5e"/><stop offset="62%" stop-color="#0c0a30"/><stop offset="100%" stop-color="${NAVY}"/>
     </radialGradient></defs>
     <rect width="${size}" height="${size}" fill="url(#g)"/>
   </svg>`);

async function icon(file, size, ratio) {
  const mark = Math.round(size * ratio);
  const markBuf = await sharp(MARK, { density: 300 })
    .resize(mark, mark, { fit: 'contain', background: 'rgba(0,0,0,0)' })
    .png().toBuffer();
  await sharp(backdrop(size))
    .composite([{ input: markBuf, left: Math.round((size - mark) / 2), top: Math.round((size - mark) / 2) }])
    .png({ compressionLevel: 9, palette: true })
    .toFile(join(OUT, file));
  console.log('icon', file, `${size}x${size}`);
}

// `any` icons: the mark can fill more of the tile.
await icon('icon-192.png', 192, 0.66);
await icon('icon-512.png', 512, 0.66);
// `maskable` icons: the platform may crop to a circle of ~80% diameter, so the
// mark is kept well inside that safe zone.
await icon('icon-maskable-192.png', 192, 0.46);
await icon('icon-maskable-512.png', 512, 0.46);
// iOS home-screen icon (opaque, no alpha).
await icon('apple-touch-icon.png', 180, 0.62);
