#!/usr/bin/env node
/* Inventory helper for docs/REF-UI-STUDY.md.

   Walks a folder of UI references and emits one row per file so the study can
   be done "one by one" instead of by eyeballing a file tree. It never copies,
   executes or imports any reference file — it only reads bytes for hints.

   Usage:
     node scripts/ref-inventory.mjs                      # scans ./REF
     node scripts/ref-inventory.mjs path/to/folder      # any folder, in or out of the repo
     node scripts/ref-inventory.mjs REF --write         # also writes docs/REF-INVENTORY.md

   The "study" column is intentionally left as TODO: it gets filled after each
   file is actually read and scored against the rubric in docs/REF-UI-STUDY.md.
*/
import { readdirSync, readFileSync, statSync, existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { join, relative, extname, basename, dirname } from 'node:path';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';

const ROOT = fileURLToPath(new URL('../', import.meta.url));
const WRITE = process.argv.includes('--write');
const args = process.argv.slice(2).filter((a) => a !== '--write');
const input = args[0] || 'REF';
const DIR = input.startsWith('/') ? input : join(ROOT, input);
const MAX_TEXT = 2 * 1024 * 1024;

if (!existsSync(DIR)) {
  console.error(`REF inventory: folder not found → ${DIR}`);
  console.error('Push the sources into main/REF, or pass a path: node scripts/ref-inventory.mjs <folder>');
  process.exit(1);
}
if (!statSync(DIR).isDirectory()) {
  console.error(`REF inventory: not a folder → ${DIR}`);
  process.exit(1);
}

const SKIP = new Set(['.git', 'node_modules', '.DS_Store', 'Thumbs.db']);
const KINDS = {
  '.html': 'HTML', '.htm': 'HTML', '.xhtml': 'HTML',
  '.css': 'CSS', '.scss': 'CSS', '.sass': 'CSS', '.less': 'CSS',
  '.js': 'JS', '.mjs': 'JS', '.cjs': 'JS', '.ts': 'JS', '.tsx': 'JS', '.jsx': 'JS',
  '.vue': 'component', '.svelte': 'component',
  '.json': 'data', '.svg': 'SVG', '.png': 'image', '.jpg': 'image', '.jpeg': 'image',
  '.webp': 'image', '.avif': 'image', '.gif': 'image', '.ico': 'image',
  '.woff': 'font', '.woff2': 'font', '.ttf': 'font', '.otf': 'font',
  '.mp4': 'video', '.webm': 'video', '.mov': 'video',
  '.md': 'doc', '.txt': 'doc', '.pdf': 'doc',
  '.zip': 'archive', '.rar': 'archive', '.7z': 'archive', '.gz': 'archive',
};
const EXTERNAL = /(?:cdnjs|unpkg|jsdelivr|cdn\.|fonts\.googleapis|fonts\.gstatic|tailwindcss|codepen\.io|@import\s+url\(\s*["']?https?:)/i;
const LIBS = /(?:gsap|three\.js|threejs|jquery|react|vue|svelte|framer|lenis|anime\.js|lottie|swiper|bootstrap|tailwind|alpine|barba|locomotive)/i;
const HEAVY = /(?:backdrop-filter|filter:\s*blur|will-change|requestAnimationFrame|addEventListener\(\s*['"]scroll|@keyframes|animation:|mix-blend-mode)/i;
const RTL = /(?:dir\s*=\s*["']rtl|direction:\s*rtl|[\u0600-\u06FF])/;

function walk(dir, out = []) {
  for (const ent of readdirSync(dir, { withFileTypes: true })) {
    if (SKIP.has(ent.name)) continue;
    const p = join(dir, ent.name);
    if (ent.isDirectory()) walk(p, out);
    else out.push(p);
  }
  return out;
}

const sizeOf = (n) => n < 1024 ? `${n} B` : n < 1024 ** 2 ? `${(n / 1024).toFixed(1)} KB` : `${(n / 1024 ** 2).toFixed(1)} MB`;

function hints(file, kind, size) {
  const out = [];
  if (!['HTML', 'CSS', 'JS', 'component', 'data', 'SVG', 'doc'].includes(kind) || size > MAX_TEXT) return out;
  let text;
  try { text = readFileSync(file, 'utf8'); } catch { return ['binary/unreadable']; }
  const title = text.match(/<title[^>]*>([\s\S]{0,90}?)<\/title>/i)?.[1]?.trim().replace(/\s+/g, ' ');
  if (title) out.push(`title="${title.slice(0, 60)}"`);
  if (EXTERNAL.test(text)) out.push('⚠ external CDN/import');
  if (LIBS.test(text)) out.push(`lib:${(text.match(LIBS)?.[0] || '').toLowerCase()}`);
  if (HEAVY.test(text)) out.push('⚠ heavy/motion');
  if (RTL.test(text)) out.push('RTL/Arabic present');
  const colours = [...new Set((text.match(/#[0-9a-fA-F]{6}\b/g) || []).map((c) => c.toLowerCase()))].slice(0, 4);
  if (colours.length) out.push(`colours ${colours.join(',')}`);
  if (kind === 'HTML') {
    const classes = [...new Set([...text.matchAll(/class=["']([^"']+)["']/g)].flatMap((m) => m[1].split(/\s+/)).filter(Boolean))].slice(0, 6);
    if (classes.length) out.push(`classes ${classes.join('.')}`);
  }
  if (kind === 'CSS') {
    const rules = (text.match(/\{/g) || []).length;
    out.push(`~${rules} rules`);
    if (/!important/.test(text)) out.push('⚠ !important');
  }
  if (['JS', 'component'].includes(kind)) {
    if (/IntersectionObserver/.test(text)) out.push('IntersectionObserver');
    if (/matchMedia/.test(text)) out.push('matchMedia');
  }
  return out.slice(0, 6);
}

const files = walk(DIR).sort((a, b) => relative(DIR, a).localeCompare(relative(DIR, b)));
if (!files.length) {
  console.error(`REF inventory: folder is empty → ${DIR}`);
  process.exit(1);
}

const rows = [];
const byKind = new Map();
const warnings = [];
for (const [i, file] of files.entries()) {
  const rel = relative(DIR, file).split('\\').join('/');
  const ext = extname(file).toLowerCase();
  const kind = KINDS[ext] || 'other';
  const st = statSync(file);
  const hash = createHash('sha256').update(readFileSync(file)).digest('hex').slice(0, 8);
  const h = hints(file, kind, st.size);
  byKind.set(kind, (byKind.get(kind) || 0) + 1);
  if (st.size > 500 * 1024) warnings.push(`${rel} — ${sizeOf(st.size)} (>500 KB, check first-load budget)`);
  if (h.some((x) => x.startsWith('⚠'))) warnings.push(`${rel} — ${h.filter((x) => x.startsWith('⚠')).join(' · ')}`);
  if (['font', 'archive'].includes(kind)) warnings.push(`${rel} — ${kind} needs licence/provenance review`);
  rows.push(`| ${i + 1} | \`${rel}\` | ${kind} | ${sizeOf(st.size)} | ${hash} | ${h.join(' · ') || '—'} | TODO |`);
}

const summary = [...byKind.entries()].sort((a, b) => b[1] - a[1]).map(([k, n]) => `${k} ${n}`).join(' · ');
const md = `# REF inventory — generated ${new Date().toISOString().slice(0, 19)}Z

Folder: \`${DIR}\` · **${files.length} file(s)** · ${summary}

This is a triage list, **not** the study. Each \`TODO\` is replaced with the
per-file assessment from the template in \`docs/REF-UI-STUDY.md\` after the file
is actually read. ⚠ flags are review triggers, not automatic rejections.

| # | File | Kind | Size | sha256 | Hints | Study |
| --- | --- | --- | --- | --- | --- | --- |
${rows.join('\n')}

## Review triggers

${warnings.length ? warnings.map((w) => `- ${w}`).join('\n') : '- none detected by the automated scan (still check licences and claims manually)'}
`;

console.log(md);
if (WRITE) {
  const out = join(ROOT, 'docs', 'REF-INVENTORY.md');
  mkdirSync(dirname(out), { recursive: true });
  writeFileSync(out, md);
  console.error(`wrote ${out}`);
}
