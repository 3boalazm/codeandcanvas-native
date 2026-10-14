/* ==========================================================================
   make-og.mjs — renders assets/brand/og-default.png (1200×630) from the
   brand icon SVG + Poppins. Needs `@resvg/resvg-js` (not a site dependency):
     npx -y -p @resvg/resvg-js node scripts/make-og.mjs
   or `npm i -D @resvg/resvg-js` then `node scripts/make-og.mjs`.
   ========================================================================== */
import { Resvg } from '@resvg/resvg-js';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { readFileSync, writeFileSync } from 'node:fs';
const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const icon = readFileSync(`${ROOT}/assets/brand/icon-white.svg`, 'utf8');
const inner = icon.slice(icon.indexOf('<g id="Layer_1-2"'), icon.lastIndexOf('</svg>')).replace(/class="cls-[12]"/g, 'fill="#fff"');
const W = 1200, H = 630;
const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a0a2e"/><stop offset="1" stop-color="#05051a"/></linearGradient>
    <radialGradient id="glowA" cx="0.18" cy="0.2" r="0.5"><stop offset="0" stop-color="#4f3fd8" stop-opacity=".55"/><stop offset="1" stop-color="#4f3fd8" stop-opacity="0"/></radialGradient>
    <radialGradient id="glowB" cx="0.88" cy="0.9" r="0.5"><stop offset="0" stop-color="#3fd6c4" stop-opacity=".35"/><stop offset="1" stop-color="#3fd6c4" stop-opacity="0"/></radialGradient>
    <radialGradient id="glowC" cx="0.7" cy="0.15" r="0.35"><stop offset="0" stop-color="#ee5ba3" stop-opacity=".22"/><stop offset="1" stop-color="#ee5ba3" stop-opacity="0"/></radialGradient>
    <linearGradient id="brand" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8b6cff"/><stop offset=".55" stop-color="#3fd6c4"/><stop offset="1" stop-color="#f3c77a"/></linearGradient>
    <pattern id="grid" width="60" height="60" patternUnits="userSpaceOnUse"><path d="M60 0H0V60" fill="none" stroke="#fff" stroke-opacity=".045"/></pattern>
  </defs>
  <rect width="${W}" height="${H}" fill="url(#bg)"/>
  <rect width="${W}" height="${H}" fill="url(#grid)"/>
  <rect width="${W}" height="${H}" fill="url(#glowA)"/>
  <rect width="${W}" height="${H}" fill="url(#glowB)"/>
  <rect width="${W}" height="${H}" fill="url(#glowC)"/>
  <g transform="translate(96 92) scale(0.2)">${inner}</g>
  <text x="248" y="150" font-family="Poppins" font-weight="700" font-size="44" fill="#ffffff" letter-spacing="-0.5">Code &amp; Canvas</text>
  <text x="250" y="190" font-family="Poppins" font-weight="500" font-size="20" fill="#9a9ac0" letter-spacing="4">BUSINESS · TECHNOLOGY · DESIGN</text>
  <text x="96" y="332" font-family="Poppins" font-weight="700" font-size="64" fill="#ffffff" letter-spacing="-1.5">Brand, technology and data,</text>
  <text x="96" y="410" font-family="Poppins" font-weight="700" font-size="64" fill="url(#brand)" letter-spacing="-1.5">built around a business outcome.</text>
  <text x="96" y="478" font-family="Poppins" font-weight="400" font-size="22" fill="#b7b7d6">Two-founder studio · KSA + Egypt · 23 productized services · fixed scope · milestone-based payment</text>
  <rect x="96" y="540" width="1008" height="1" fill="#ffffff" fill-opacity=".14"/>
  <text x="96" y="580" font-family="Poppins" font-weight="600" font-size="20" fill="#ffffff">codeandcanvas.net</text>
  <text x="1104" y="580" text-anchor="end" font-family="Poppins" font-weight="500" font-size="20" fill="#9a9ac0">Enterprise architecture · Healthcare IT · Brand systems</text>
</svg>`;
const r = new Resvg(svg, { fitTo: { mode: 'width', value: W }, font: { fontFiles: [`${ROOT}/assets/fonts/Poppins-Bold.ttf`, `${ROOT}/assets/fonts/Poppins-SemiBold.ttf`, `${ROOT}/assets/fonts/Poppins-Medium.ttf`, `${ROOT}/assets/fonts/Poppins-Regular.ttf`], loadSystemFonts: false, defaultFontFamily: 'Poppins' } });
const png = r.render().asPng();
writeFileSync(`${ROOT}/assets/brand/og-default.png`, png);
console.log('og-default.png', png.length, 'bytes');
