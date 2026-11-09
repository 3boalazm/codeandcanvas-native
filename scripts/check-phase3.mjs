#!/usr/bin/env node
/* ==========================================================================
   Phase 3 no-go guard — 2026-11-09.

   The phased plan in docs/REF-UI-STUDY-2026-11.md §3 marks Phase 3 as
   "deliberately rejected": fabricated metrics/charts, AI/crypto/health
   dashboard chrome, orange/cyan/serif skins, runtime blur/WebGL and
   third-party portraits/logos. Entering Phase 3 therefore means LOCKING the
   rejection list, not publishing any of it. This script fails the check chain
   if a published source re-introduces one of those signatures.

   It does not weaken or replace the existing gates: check-claims.mjs still
   bans guarantee language, optimize-media.mjs --check still validates assets,
   and the Playwright suites still cover axe, RTL, themes and layout.
   ========================================================================== */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SKIP = new Set([
  'REF', 'node_modules', 'dist', 'test-results', 'playwright-report', '.git',
  '.github', '.qa-ref', '.data', '.cache', '.local', '__pycache__', '.venv',
]);
const allowed = (p) => !path.relative(ROOT, p).split(path.sep).some((part) => SKIP.has(part) || part.startsWith('.qa-'));
const read = (p) => { try { return fs.readFileSync(p, 'utf8'); } catch { return ''; } };
const walk = (dir, ext) => {
  const out = [];
  const go = (d) => {
    for (const e of fs.readdirSync(d, { withFileTypes: true })) {
      const p = path.join(d, e.name);
      if (!allowed(p)) continue;
      if (e.isDirectory()) go(p);
      else if (e.isFile() && p.endsWith(ext)) out.push(p);
    }
  };
  go(dir);
  return out;
};
const inDir = (dir, ext) => fs.existsSync(dir)
  ? fs.readdirSync(dir, { withFileTypes: true })
      .filter((e) => e.isFile() && e.name.endsWith(ext))
      .map((e) => path.join(dir, e.name))
  : [];

const html = walk(ROOT, '.html');
const css = inDir(path.join(ROOT, 'assets/css'), '.css');
const js = inDir(path.join(ROOT, 'assets/js'), '.js');
const builders = [
  ...inDir(path.join(ROOT, 'scripts/lib'), '.py'),
  ...inDir(path.join(ROOT, 'partials'), '.html'),
  path.join(ROOT, 'index.html'),
  path.join(ROOT, 'erp/index.html'),
].filter((p) => fs.existsSync(p));
const arHtml = html.filter((p) => path.relative(ROOT, p).startsWith(`ar${path.sep}`));
const phase3Css = path.join(ROOT, 'assets/css/system.css');
const phase3Js = path.join(ROOT, 'assets/js/system.js');
const phase3Py = path.join(ROOT, 'scripts/lib/pages_system.py');

/* Rule → [files, regex, human meaning]. Only unambiguous signatures are used;
   editorial copy that merely *discusses* typography or AI is not a skin. */
const rules = [
  ['external CDN script', html, /<script[^>]+src=["'](?:https?:)?\/\//i, 'CDN / third-party JS'],
  ['external stylesheet', html, /<link[^>]+rel=["']stylesheet["'][^>]+href=["'](?:https?:)?\/\//i, 'CDN / third-party CSS'],
  ['external image', html, /<img[^>]+src=["'](?:https?:)?\/\/|srcset=["'](?:https?:)?\/\//i, 'third-party portrait / logo / screenshot'],
  ['canvas element', html, /<canvas\b/i, 'WebGL / dashboard canvas'],
  // Prose may legitimately *name* WebGL as a rejected item (the Phase 3
  // boundary section does); only an actual context request or a JS/CSS
  // reference counts as a runtime signature.
  ['WebGL context request', html, /getContext\(\s*["'](?:webgl|experimental-webgl)/i, 'runtime WebGL context'],
  ['WebGL in JS/CSS', [...css, ...js], /\bwebgl\b/i, 'runtime WebGL reference'],
  ['heavy JS library', [...html, ...css, ...js], /\bgsap\b|ScrollTrigger|THREE\.|three\.min\.js/i, 'GSAP / three.js library'],
  ['cyan skin token', css, /\bcyan\b/i, 'off-palette cyan skin'],
  ['orange skin token', css, /\borange\b/i, 'off-palette orange skin'],
  ['serif skin token', css, /(?<!sans-)\bserif\b/i, 'off-palette serif skin'],
  ['runtime blur / infinite motion', [phase3Css, phase3Js, phase3Py].filter((p) => fs.existsSync(p)),
    /filter\s*:\s*blur|backdrop-filter|will-change|\banimation(?:-iteration-count)?\s*:[^;]*infinite/i,
    'runtime blur / always-on animation on Phase 3 surfaces'],
  ['AR data-ar leftover', arHtml, /\bdata-ar(?:[-=\s]|$)/i, 'untranslated AR twin'],
];

const violations = [];
for (const [name, files, re, meaning] of rules) {
  for (const file of files) {
    const text = read(file);
    const lines = text.split('\n');
    for (let i = 0; i < lines.length; i += 1) {
      if (!re.test(lines[i])) continue;
      violations.push({ rule: name, meaning, file: path.relative(ROOT, file), line: i + 1, text: lines[i].trim().slice(0, 160) });
      break; // one report per file per rule is enough to fail the gate
    }
  }
}

/* Decision lock: the study must keep saying these items are rejected. */
const studyPath = path.join(ROOT, 'docs/REF-UI-STUDY-2026-11.md');
const study = read(studyPath);
if (!study) violations.push({ rule: 'study missing', meaning: 'rejection list could not be read', file: 'docs/REF-UI-STUDY-2026-11.md', line: 0, text: '' });
if (!/Phase 3 — deliberately rejected/.test(study)) violations.push({ rule: 'phase 3 decision', meaning: 'rejection line was removed', file: 'docs/REF-UI-STUDY-2026-11.md', line: 0, text: '' });
if (!/fabricated metrics\/charts/.test(study)) violations.push({ rule: 'fabricated metrics decision', meaning: 'claims rejection was removed', file: 'docs/REF-UI-STUDY-2026-11.md', line: 0, text: '' });
if (!/REF 060/.test(study)) violations.push({ rule: 'REF 060 decision', meaning: 'portrait/follower-count rejection was removed', file: 'docs/REF-UI-STUDY-2026-11.md', line: 0, text: '' });
if (!fs.existsSync(path.join(ROOT, 'scripts/check-claims.mjs'))) violations.push({ rule: 'claims gate', meaning: 'check-claims.mjs is missing', file: 'scripts/check-claims.mjs', line: 0, text: '' });

/* The Phase 3 boundary section must stay visible in both language twins. */
for (const rel of ['system/index.html', 'ar/system/index.html']) {
  const text = read(path.join(ROOT, rel));
  const cards = (text.match(/class="sys-guard__card"/g) || []).length;
  if (!text.includes('id="guardrails"') || cards !== 6) {
    violations.push({ rule: 'phase 3 boundary section', meaning: `expected 6 guard cards in ${rel}, found ${cards}`, file: rel, line: 0, text: '' });
  }
}

if (violations.length) {
  console.error(`phase3 guard: ${violations.length} no-go signature(s) found:`);
  for (const v of violations) console.error(`  [${v.rule}] ${v.file}:${v.line} — ${v.meaning}\n    ${v.text}`);
  process.exit(1);
}

console.log(`phase3 guard: 0 no-go signatures · ${html.length} HTML · ${css.length + js.length} CSS/JS · ${builders.length} builder files · ${arHtml.length} AR pages · rejection list locked`);
