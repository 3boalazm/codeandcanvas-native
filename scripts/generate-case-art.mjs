#!/usr/bin/env node
/* Deterministic illustrative artwork for case studies whose AI-image slot was
   exhausted in the generation turn. Each PNG is a locally generated composite:
   a heavily defocused crop of one of this site's AI-generated abstract images,
   then an original SVG geometry layer unique to the project. No photography,
   client work, product screenshot, logo or text is used. See
   docs/ASSET-AND-CLAIM-REGISTER.md for the asset provenance table. */
import { readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';
import { Resvg } from '@resvg/resvg-js';

const ROOT = fileURLToPath(new URL('../', import.meta.url));
const MEDIA = join(ROOT, 'assets', 'media');
const W = 1600;
const H = 900;

const grid = (color) => Array.from({ length: 17 }, (_, i) => `<line x1="${i * 100}" y1="0" x2="${i * 100}" y2="900" stroke="${color}" stroke-width="1"/>`).join('')
  + Array.from({ length: 10 }, (_, i) => `<line x1="0" y1="${i * 100}" x2="1600" y2="${i * 100}" stroke="${color}" stroke-width="1"/>`).join('');

const defs = (a, b, c) => `<defs>
  <linearGradient id="g1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${a}"/><stop offset=".55" stop-color="${b}"/><stop offset="1" stop-color="${c}"/></linearGradient>
  <linearGradient id="g2" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="${c}"/><stop offset="1" stop-color="${a}"/></linearGradient>
  <radialGradient id="orb"><stop offset="0" stop-color="${b}" stop-opacity=".55"/><stop offset="1" stop-color="${b}" stop-opacity="0"/></radialGradient>
  <radialGradient id="orb2"><stop offset="0" stop-color="${a}" stop-opacity=".4"/><stop offset="1" stop-color="${a}" stop-opacity="0"/></radialGradient>
</defs>`;

const shell = (a, b, c, geometry) => `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
${defs(a, b, c)}
<rect width="${W}" height="${H}" fill="#05051a" opacity=".78"/>
<circle cx="1260" cy="160" r="380" fill="url(#orb)"/>
<circle cx="260" cy="780" r="330" fill="url(#orb2)"/>
<g opacity=".18" stroke="#ffffff">${grid('#ffffff')}</g>
${geometry}
</svg>`;

const wave = (y, color, amp, phase, opacity = '.9') => {
  const pts = Array.from({ length: 65 }, (_, i) => {
    const x = 90 + i * 22;
    const yy = y + Math.sin(i / 5 + phase) * amp + Math.sin(i / 2.3 + phase * 1.7) * amp * .28;
    return `${x},${yy.toFixed(1)}`;
  }).join(' ');
  return `<polyline points="${pts}" fill="none" stroke="${color}" stroke-width="6" stroke-linecap="round" opacity="${opacity}"/>`;
};

const node = (x, y, r, color) => `<circle cx="${x}" cy="${y}" r="${r}" fill="#080824" stroke="${color}" stroke-width="3"/><circle cx="${x}" cy="${y}" r="${r * .32}" fill="${color}"/>`;

const ART = [
  {
    file: 'case-sakanwave.png', base: 'case-stt.png', a: '#25c9b6', b: '#7b5cff', c: '#ee5ba3',
    shapes: `
      <path d="M90 450 C 350 450, 420 450, 620 450" fill="none" stroke="url(#g1)" stroke-width="18" stroke-linecap="round"/>
      ${wave(260, '#25c9b6', 28, 0)}
      ${wave(380, '#7b5cff', 34, 1.1)}
      ${wave(530, '#ee5ba3', 24, 2.2)}
      ${wave(660, '#4f8cff', 30, 3.1)}
      <path d="M620 450 C 820 450, 860 260, 1040 260" fill="none" stroke="#25c9b6" stroke-width="4" stroke-dasharray="12 14" opacity=".7"/>
      <path d="M620 450 C 820 450, 860 380, 1040 380" fill="none" stroke="#7b5cff" stroke-width="4" stroke-dasharray="12 14" opacity=".7"/>
      <path d="M620 450 C 820 450, 860 530, 1040 530" fill="none" stroke="#ee5ba3" stroke-width="4" stroke-dasharray="12 14" opacity=".7"/>
      <path d="M620 450 C 820 450, 860 660, 1040 660" fill="none" stroke="#4f8cff" stroke-width="4" stroke-dasharray="12 14" opacity=".7"/>
      <circle cx="1320" cy="450" r="190" fill="none" stroke="url(#g2)" stroke-width="3" opacity=".55"/>
      <circle cx="1320" cy="450" r="132" fill="none" stroke="url(#g1)" stroke-width="12" opacity=".5"/>
      <rect x="1210" y="360" width="220" height="180" rx="30" fill="#080824" opacity=".7" stroke="url(#g1)" stroke-width="3"/>
    `,
  },
  {
    file: 'case-oltre.png', base: 'case-maqloop.png', a: '#ee5ba3', b: '#7b5cff', c: '#25c9b6',
    shapes: `
      <g opacity=".88">
        <rect x="180" y="150" width="260" height="600" rx="18" fill="#11112e" stroke="url(#g1)" stroke-width="3" transform="rotate(-6 310 450)"/>
        <rect x="540" y="110" width="300" height="650" rx="20" fill="#0d0d28" stroke="url(#g2)" stroke-width="4"/>
        <rect x="940" y="170" width="260" height="570" rx="18" fill="#11112e" stroke="url(#g1)" stroke-width="3" transform="rotate(5 1070 455)"/>
      </g>
      <path d="M640 220 L740 220 L780 300 L760 350 L780 410 L750 680 L610 680 L580 410 L600 350 L580 300 Z" fill="url(#g1)" opacity=".78"/>
      <path d="M620 220 Q690 265 760 220" fill="none" stroke="#ffffff" stroke-width="5" opacity=".55"/>
      <path d="M230 250 L400 220 L430 320 L390 390 L410 700 L220 700 Z" fill="url(#g2)" opacity=".55"/>
      <path d="M990 250 L1160 220 L1180 320 L1140 390 L1160 690 L980 690 Z" fill="url(#g1)" opacity=".5"/>
      <path d="M120 790 C 420 710, 680 840, 1480 720" fill="none" stroke="url(#g1)" stroke-width="8" opacity=".7"/>
      ${[0, 1, 2, 3, 4, 5].map((i) => `<circle cx="${1270 + i * 38}" cy="${230 + (i % 2) * 26}" r="7" fill="${i % 2 ? '#25c9b6' : '#ee5ba3'}"/>`).join('')}
    `,
  },
  {
    file: 'case-continuum.png', base: 'case-axiom.png', a: '#25c9b6', b: '#7b5cff', c: '#4f8cff',
    shapes: `
      <g fill="none" stroke="url(#g1)" stroke-width="3" opacity=".72">
        <path d="M260 450 C 380 240, 590 240, 720 450 S 1060 660, 1200 450"/>
        <path d="M260 450 C 400 660, 600 660, 720 450 S 1040 240, 1200 450"/>
        <path d="M720 450 C 820 340, 940 340, 1040 450 C 940 560, 820 560, 720 450 Z"/>
      </g>
      ${[[260, 450, 34, '#25c9b6'], [470, 300, 24, '#7b5cff'], [470, 600, 24, '#4f8cff'], [720, 450, 42, '#ee5ba3'], [960, 340, 26, '#25c9b6'], [960, 560, 26, '#7b5cff'], [1200, 450, 34, '#4f8cff'], [1340, 300, 18, '#25c9b6'], [1340, 600, 18, '#ee5ba3']].map(([x, y, r, c]) => node(x, y, r, c)).join('')}
      <circle cx="720" cy="450" r="250" fill="none" stroke="url(#g2)" stroke-width="2" stroke-dasharray="8 18" opacity=".55"/>
      <circle cx="720" cy="450" r="178" fill="none" stroke="url(#g1)" stroke-width="12" opacity=".22"/>
      <g opacity=".42">${[0, 1, 2, 3].map((i) => `<rect x="${1080 + i * 46}" y="${150 + i * 32}" width="210" height="120" rx="14" fill="#0d0d28" stroke="url(#g1)" stroke-width="2" transform="rotate(${i * 4 - 6} ${1185 + i * 46} ${210 + i * 32})"/>`).join('')}</g>
    `,
  },
  {
    file: 'case-npf.png', base: 'case-packbox.png', a: '#25c9b6', b: '#4f8cff', c: '#b18cff',
    shapes: `
      <g opacity=".9">
        <rect x="190" y="180" width="330" height="540" rx="18" fill="#0d0d28" stroke="url(#g1)" stroke-width="4"/>
        <rect x="250" y="240" width="210" height="420" rx="10" fill="url(#g1)" opacity=".22"/>
        ${[0, 1, 2, 3, 4, 5].map((i) => `<rect x="270" y="${280 + i * 54}" width="${170 - i * 12}" height="12" rx="6" fill="#ffffff" opacity=".2"/>`).join('')}
        <rect x="590" y="250" width="260" height="400" rx="18" fill="#0d0d28" stroke="url(#g2)" stroke-width="4"/>
        <rect x="630" y="300" width="180" height="300" rx="10" fill="url(#g2)" opacity=".18"/>
        ${[0, 1, 2, 3].map((i) => `<rect x="650" y="${330 + i * 58}" width="${140 - i * 10}" height="10" rx="5" fill="#ffffff" opacity=".22"/>`).join('')}
      </g>
      <path d="M880 450 C 1010 300, 1120 300, 1240 210" fill="none" stroke="#25c9b6" stroke-width="5" stroke-dasharray="12 14"/>
      <path d="M880 450 C 1010 450, 1120 450, 1300 450" fill="none" stroke="#4f8cff" stroke-width="5" stroke-dasharray="12 14"/>
      <path d="M880 450 C 1010 600, 1120 600, 1240 690" fill="none" stroke="#b18cff" stroke-width="5" stroke-dasharray="12 14"/>
      ${[[1240, 210], [1300, 450], [1240, 690]].map(([x, y], i) => `<circle cx="${x}" cy="${y}" r="30" fill="#080824" stroke="${['#25c9b6', '#4f8cff', '#b18cff'][i]}" stroke-width="4"/>`).join('')}
      <path d="M160 760 C 500 700, 900 810, 1450 730" fill="none" stroke="url(#g1)" stroke-width="10" opacity=".55"/>
    `,
  },
  {
    file: 'case-evolve.png', base: 'case-ummah.png', a: '#7b5cff', b: '#25c9b6', c: '#4f8cff',
    shapes: `
      <g opacity=".9">
        <rect x="470" y="190" width="660" height="520" rx="44" fill="#0a0a24" stroke="url(#g1)" stroke-width="4"/>
        <rect x="520" y="240" width="560" height="420" rx="30" fill="#101030" stroke="url(#g2)" stroke-width="3" opacity=".8"/>
        <rect x="580" y="300" width="440" height="300" rx="24" fill="url(#g1)" opacity=".12"/>
      </g>
      <g fill="none" stroke="url(#g1)" stroke-width="3" opacity=".6">
        ${[0, 1, 2, 3, 4].map((i) => `<rect x="${540 + i * 22}" y="${220 + i * 22}" width="${520 - i * 44}" height="${440 - i * 44}" rx="${28 - i * 3}" opacity="${.55 - i * .08}"/>`).join('')}
      </g>
      <circle cx="800" cy="450" r="92" fill="#080824" stroke="url(#g1)" stroke-width="8"/>
      <circle cx="800" cy="450" r="48" fill="url(#g1)" opacity=".35"/>
      <path d="M240 450 C 340 450, 380 450, 470 450" fill="none" stroke="#25c9b6" stroke-width="4" stroke-dasharray="10 16"/>
      <path d="M1130 450 C 1240 450, 1280 450, 1400 450" fill="none" stroke="#7b5cff" stroke-width="4" stroke-dasharray="10 16"/>
      <path d="M800 710 C 800 780, 860 800, 930 800" fill="none" stroke="#4f8cff" stroke-width="4" stroke-dasharray="10 16"/>
      ${[[240, 450], [1400, 450], [930, 800]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="9" fill="#25c9b6"/>`).join('')}
    `,
  },
];

for (const art of ART) {
  const svg = shell(art.a, art.b, art.c, art.shapes);
  const png = new Resvg(svg, { fitTo: { mode: 'width', value: W }, background: 'rgba(5,5,26,0)' }).render().asPng();
  const base = await sharp(readFileSync(join(MEDIA, art.base)))
    .resize(W, H, { fit: 'cover' })
    .blur(24)
    .modulate({ brightness: .52, saturation: .82 })
    .png()
    .toBuffer();
  const out = await sharp(base).composite([{ input: png, blend: 'over' }]).png({ compressionLevel: 9 }).toBuffer();
  writeFileSync(join(MEDIA, art.file), out);
  console.log(`generated ${art.file} from ${art.base} + original SVG geometry`);
}
