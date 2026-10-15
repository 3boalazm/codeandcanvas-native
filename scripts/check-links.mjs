#!/usr/bin/env node
/* ==========================================================================
   check-links.mjs — static QA for the site. No dependencies.
     · every internal href/src resolves to a file in the repo (or a listed redirect)
     · every in-page #anchor exists in the target document
     · basic tag balance per HTML file (catches an unclosed <div>/<section>)
   Usage: node scripts/check-links.mjs   (exit 1 on problems)
   ========================================================================== */
import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join, relative, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(fileURLToPath(import.meta.url), '..', '..');
const SKIP = new Set(['node_modules', 'dist', '.git', 'partials', 'docs', 'scripts', 'Unselected files', 'test-results', 'playwright-report']);
const VOID = new Set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr']);

function walk(dir, out = []) {
  for (const name of readdirSync(dir)) {
    if (SKIP.has(name)) continue;
    const p = join(dir, name);
    if (statSync(p).isDirectory()) walk(p, out);
    else if (name.endsWith('.html')) out.push(p);
  }
  return out;
}

const redirects = new Map();
if (existsSync(join(ROOT, '_redirects'))) {
  for (const line of readFileSync(join(ROOT, '_redirects'), 'utf8').split('\n')) {
    const [from, to] = line.trim().split(/\s+/);
    if (from && to && !from.startsWith('#')) redirects.set(from, to);
  }
}

function resolveUrl(url) {
  // returns the file path for an internal url (without hash) or null
  let p = url.split('#')[0].split('?')[0];
  if (!p) return null;
  if (redirects.has(p)) p = redirects.get(p);
  if (p.startsWith('/')) {
    const abs = join(ROOT, p);
    if (p.endsWith('/')) return join(abs, 'index.html');
    if (existsSync(abs) && statSync(abs).isDirectory()) return join(abs, 'index.html');
    return abs;
  }
  return null;
}

const pages = walk(ROOT);
const problems = [];
const idCache = new Map();
function idsOf(file) {
  if (!idCache.has(file)) {
    const src = existsSync(file) ? readFileSync(file, 'utf8') : '';
    idCache.set(file, new Set([...src.matchAll(/\sid="([^"]+)"/g)].map((m) => m[1])));
  }
  return idCache.get(file);
}

for (const file of pages) {
  const rel = relative(ROOT, file);
  const src = readFileSync(file, 'utf8');

  // tag balance
  const stack = [];
  const tagRe = /<\/?([a-zA-Z][a-zA-Z0-9-]*)(\s[^<>]*?)?\/?>/g;
  let m;
  while ((m = tagRe.exec(src))) {
    const [full, name] = m;
    const n = name.toLowerCase();
    if (n === 'script' && !full.startsWith('</')) { // skip script bodies
      const end = src.indexOf('</script>', tagRe.lastIndex);
      if (end > -1) tagRe.lastIndex = end + '</script>'.length;
      continue;
    }
    if (n === 'style' && !full.startsWith('</')) { const end = src.indexOf('</style>', tagRe.lastIndex); if (end > -1) tagRe.lastIndex = end + '</style>'.length; continue; }
    if (full.startsWith('<!')) continue;
    if (full.startsWith('</')) {
      const idx = stack.lastIndexOf(n);
      if (idx === -1) problems.push(`${rel}: stray </${n}> near offset ${m.index}`);
      else { if (idx !== stack.length - 1) problems.push(`${rel}: </${n}> closes while <${stack[stack.length - 1]}> is open (offset ${m.index})`); stack.length = idx; }
    } else if (!VOID.has(n) && !full.endsWith('/>')) stack.push(n);
  }
  if (stack.length) problems.push(`${rel}: unclosed <${stack.join('>, <')}>`);

  // links
  const attrRe = /\s(?:href|src|action)="([^"]*)"/g;
  while ((m = attrRe.exec(src))) {
    const url = m[1];
    if (!url || url.startsWith('http') || url.startsWith('mailto:') || url.startsWith('tel:') || url.startsWith('data:') || url.startsWith('javascript:')) continue;
    if (url.startsWith('#')) {
      const id = url.slice(1);
      if (id && id !== 'top' && !idsOf(file).has(id)) problems.push(`${rel}: missing in-page anchor ${url}`);
      continue;
    }
    if (!url.startsWith('/')) { problems.push(`${rel}: relative url "${url}" (use root-relative)`); continue; }
    const target = resolveUrl(url);
    if (!target || !existsSync(target)) { problems.push(`${rel}: broken link ${url}`); continue; }
    const hash = url.split('#')[1];
    if (hash && hash !== 'top' && target.endsWith('.html') && !idsOf(target).has(hash)) problems.push(`${rel}: ${url} → anchor #${hash} not found`);
  }
}

console.log(`${pages.length} HTML files checked · ${problems.length} problem(s)`);
problems.forEach((p) => console.log('  ' + p));
if (problems.length) process.exit(1);
