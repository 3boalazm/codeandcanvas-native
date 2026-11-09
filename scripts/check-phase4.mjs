#!/usr/bin/env node
/* ==========================================================================
   Phase 4 residual-B guard — 2026-11-09.

   Phase 4 (docs/REF-UI-STUDY-2026-11.md §9) ships the last identity-fit B
   mechanisms that need no owner asset: static capability loop (013),
   concentric Why/How/What rings (027), a curved static process path with
   four numbered glass steps (017/037/052), a compact step bar (055) and one
   labelled full-bleed art card with paired CTAs (030). This check locks the
   section counts in both language twins and refuses any CDN/canvas/WebGL
   signature inside the new markup. It complements check-phase3.mjs, which
   keeps the Phase 3 no-go list locked.
   ========================================================================== */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = (p) => { try { return fs.readFileSync(p, 'utf8'); } catch { return ''; } };
const count = (text, re) => (text.match(re) || []).length;
const rel = (p) => path.relative(ROOT, p);
const violations = [];

const study = read(path.join(ROOT, 'docs/REF-UI-STUDY-2026-11.md'));
if (!study) violations.push('study missing: docs/REF-UI-STUDY-2026-11.md');
if (!/## 9\. Phase 4/.test(study)) violations.push('Phase 4 section (§9) missing from the dated study');
if (!/Phase 4 —/.test(study)) violations.push('Phase 4 decision line missing from the dated study');

const forbidden = [
  ['external script', /<script[^>]+src=["'](?:https?:)?\/\//i],
  ['external image', /<img[^>]+src=["'](?:https?:)?\/\/|srcset=["'](?:https?:)?\/\//i],
  ['canvas', /<canvas\b/i],
  ['WebGL context', /getContext\(\s*["'](?:webgl|experimental-webgl)/i],
  ['heavy library', /\bgsap\b|ScrollTrigger|THREE\.|three\.min\.js/i],
];

for (const file of ['system/index.html', 'ar/system/index.html']) {
  const p = path.join(ROOT, file);
  const t = read(p);
  if (!t) { violations.push(`${file}: missing`); continue; }
  if (!t.includes('id="loop"') || !t.includes('id="process"')) violations.push(`${file}: #loop / #process missing`);
  const expected = [
    ['capability pills', /class="sys-loop__pill/g, 8],
    ['concentric rings', /class="sys-concentric__ring/g, 3],
    ['process steps', /class="sys-step"/g, 4],
    ['step-bar nodes', /class="sys-stepbar__node"/g, 4],
    ['art cards', /class="sys-artcard"/g, 1],
    ['paired art CTAs', /class="sys-artcard__ctas"/g, 1],
    ['static curves', /class="sys-process__curve"/g, 1],
  ];
  for (const [name, re, want] of expected) {
    const got = count(t, re);
    if (got !== want) violations.push(`${file}: ${name} = ${got}, expected ${want}`);
  }
  for (const [name, re] of forbidden) {
    if (re.test(t)) violations.push(`${file}: ${name} signature found`);
  }
  const art = t.slice(t.indexOf('class="sys-artcard"'), t.indexOf('</figure>', t.indexOf('class="sys-artcard"')));
  if (/class="btn btn--glass"/.test(art)) violations.push(`${file}: art card reintroduced a desktop glass-blur CTA`);
  if (count(art, /<a class="btn /g) !== 2) violations.push(`${file}: art card must carry exactly two CTA links`);
  if (file.startsWith('ar/') && /\bdata-ar(?:[-=\s]|$)/i.test(t)) violations.push(`${file}: untranslated data-ar* leftover`);
}

if (violations.length) {
  console.error(`phase4 guard: ${violations.length} problem(s):`);
  for (const v of violations) console.error(`  - ${v}`);
  process.exit(1);
}
console.log('phase4 guard: 0 problems · 8 loop pills / 3 rings / 4 steps / 4 step-bar nodes / 1 art card in both twins · §9 locked');
