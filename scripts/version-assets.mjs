#!/usr/bin/env node
/* ==========================================================================
   version-assets.mjs — content-hash every first-party CSS/JS reference.

   Why: HTML is served `must-revalidate` while `/assets/**` is served with a
   1-hour `stale-while-revalidate` window AND is cached by name in the service
   worker. A stylesheet change that keeps the same URL therefore reaches
   returning visitors late — the new markup arrives first and renders as
   unstyled text (this is exactly what happened to the home `/system/` band:
   new cards, old `home.css`).

   Fix: link every stylesheet and script as `/assets/css/home.css?v=<hash>`
   where <hash> is a sha256 of that file's bytes. The URL changes whenever the
   file changes, which:
     · busts the browser cache deterministically,
     · makes the service worker's by-URL cache key a new entry,
     · costs nothing when the file did not change (stable hash).

   The canonical references live in partials/head.html and partials/bottom.html
   and are hashed THERE as well, so `sync-chrome.mjs` copies an already-versioned
   <link>/<script> into every page. Both files and every page are then swept, so
   `--check` never disagrees with what `npm run sync` would write (CI).

     node scripts/version-assets.mjs          # rewrite in place
     node scripts/version-assets.mjs --check  # verify
   ========================================================================== */
import { readFileSync, writeFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(fileURLToPath(import.meta.url), '..', '..');
const CHECK = process.argv.includes('--check');
const SKIP_DIRS = new Set(['node_modules', 'dist', '.git', 'docs', 'scripts', 'assets', 'Unselected files', 'test-results', 'playwright-report']);

const hashOf = (assetPath) => {
  const abs = join(ROOT, assetPath);
  if (!existsSync(abs)) throw new Error(`missing asset referenced by a page: ${assetPath}`);
  return createHash('sha256').update(readFileSync(abs)).digest('hex').slice(0, 10);
};

/* /assets/css/x.css  →  /assets/css/x.css?v=ab12cd34ef */
const REF_RE = /(\/(?:assets\/[a-z]+|assets)\/[A-Za-z0-9._/-]+\.(?:css|js))(\?v=[0-9a-f]+)?(?=["')\s])/g;

function walk(dir, out = []) {
  for (const name of readdirSync(dir)) {
    if (SKIP_DIRS.has(name)) continue;
    const p = join(dir, name);
    if (statSync(p).isDirectory()) walk(p, out);
    else if (name.endsWith('.html')) out.push(p);
  }
  return out;
}

const hashes = new Map();
const versionOf = (p) => {
  if (!hashes.has(p)) hashes.set(p, hashOf(p));
  return hashes.get(p);
};

let changed = 0;
let touched = 0;
for (const file of walk(ROOT)) {
  const src = readFileSync(file, 'utf8');
  const out = src.replace(REF_RE, (_, asset) => `${asset}?v=${versionOf(asset)}`);
  if (out === src) continue;
  touched += 1;
  if (CHECK) {
    changed += 1;
    console.log(`out of date: ${relative(ROOT, file)}`);
  } else {
    writeFileSync(file, out);
    changed += 1;
  }
}

console.log(
  CHECK
    ? `${hashes.size} hashed asset(s) · ${changed} page(s) out of date`
    : `${hashes.size} hashed asset(s) · ${changed} page(s) updated`,
);
if (CHECK && changed) process.exit(1);
