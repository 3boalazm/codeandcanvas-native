#!/usr/bin/env node
/* ==========================================================================
   sync-chrome.mjs — keeps the shared page chrome identical on every page.

   Every HTML page in the site carries three marker pairs:

     <!-- cc:head -->   …  <!-- /cc:head -->    (partials/head.html)
     <!-- cc:top -->    …  <!-- /cc:top -->     (partials/top.html  — preloader, ambient, header)
     <!-- cc:bottom --> …  <!-- /cc:bottom -->  (partials/bottom.html — footer, to-top, toast, site.js)

   Running `npm run sync` (node scripts/sync-chrome.mjs) rewrites what sits
   between the markers from the partials, so the committed HTML stays 100 %
   static — no runtime includes, no build step required to serve the site.

   Usage:
     node scripts/sync-chrome.mjs           # rewrite in place
     node scripts/sync-chrome.mjs --check   # exit 1 if any page is out of date (CI)
   ========================================================================== */
import { readFileSync, writeFileSync, readdirSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(fileURLToPath(import.meta.url), '..', '..');
const CHECK = process.argv.includes('--check');
const SKIP_DIRS = new Set(['node_modules', 'dist', '.git', 'partials', 'docs', 'scripts', 'assets', 'Unselected files', 'test-results', 'playwright-report']);

const PARTIALS = {
  head: readFileSync(join(ROOT, 'partials/head.html'), 'utf8'),
  top: readFileSync(join(ROOT, 'partials/top.html'), 'utf8'),
  bottom: readFileSync(join(ROOT, 'partials/bottom.html'), 'utf8'),
};

function walk(dir, out = []) {
  for (const name of readdirSync(dir)) {
    if (SKIP_DIRS.has(name)) continue;
    const p = join(dir, name);
    if (statSync(p).isDirectory()) walk(p, out);
    else if (name.endsWith('.html')) out.push(p);
  }
  return out;
}

let changed = 0;
let touched = 0;
for (const file of walk(ROOT)) {
  // ar/** is derived output: gen-ar.mjs rewrites it from the synced English page,
  // so syncing English partials into it would undo the Arabic chrome.
  if (relative(ROOT, file).split(/[\\/]/)[0] === 'ar') continue;
  const src = readFileSync(file, 'utf8');
  let out = src;
  let hasMarkers = false;
  for (const [key, body] of Object.entries(PARTIALS)) {
    const re = new RegExp(`(<!-- cc:${key} -->)[\\s\\S]*?(<!-- /cc:${key} -->)`);
    if (!re.test(out)) continue;
    hasMarkers = true;
    out = out.replace(re, (_, open, close) => `${open}\n${body.replace(/\s+$/, '')}\n    ${close}`);
  }
  if (!hasMarkers) continue;
  touched++;
  if (out !== src) {
    changed++;
    if (CHECK) console.log(`out of date: ${relative(ROOT, file)}`);
    else { writeFileSync(file, out); console.log(`synced: ${relative(ROOT, file)}`); }
  }
}
console.log(`${touched} page(s) carry chrome markers · ${changed} ${CHECK ? 'out of date' : 'rewritten'}`);
if (CHECK && changed) process.exit(1);
