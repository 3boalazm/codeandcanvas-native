#!/usr/bin/env node
/* ==========================================================================
   gen-ar.mjs — writes the standalone Arabic site: /ar/<route>/index.html

   Source of truth is the finished English page (chrome already synced), so the
   Arabic twin always matches the English one in structure and content. Run it
   after `gen-pages.py` + `sync-chrome.mjs`:

     npm run generate      # gen-pages → sync → gen-ar

   The output is committed static HTML: it needs no server work, no runtime
   translation and no JavaScript to read or index.
   ========================================================================== */
import { readFileSync, writeFileSync, mkdirSync, rmSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { arize, arPathOf, arabicShare } from './lib/arize.mjs';

const ROOT = join(fileURLToPath(import.meta.url), '..', '..');
const OUT = join(ROOT, 'ar');

// The ERP proposal sheet binds its copy from assets/js/erp-data.js at runtime;
// read the same dictionary so the Arabic twin carries the text in its markup.
const erpDict = (() => {
  try {
    const stub = {};
    new Function('window', readFileSync(join(ROOT, 'assets/js/erp-data.js'), 'utf8'))(stub);
    return stub.PROPOSAL ?? null;
  } catch (err) {
    console.warn(`gen-ar: could not read the ERP dictionary (${err.message})`);
    return null;
  }
})();

const routes = JSON.parse(readFileSync(join(ROOT, 'manus-routes.json'), 'utf8')).routes.map((r) => r.path);
const enFileOf = (route) => (route.endsWith('.html') ? route.replace(/^\//, '') : join(route.replace(/^\//, ''), 'index.html'));

rmSync(OUT, { recursive: true, force: true });

let written = 0;
const skipped = [];
const untranslatedRoutes = [];
for (const route of routes) {
  if (route.startsWith('/ar/')) continue;
  const enFile = join(ROOT, enFileOf(route));
  if (!existsSync(enFile)) {
    skipped.push(route);
    continue;
  }
  const arPath = arPathOf(route);
  const arFile = join(ROOT, arPath.replace(/^\//, '')) + (arPath.endsWith('/') ? 'index.html' : '');
  const source = readFileSync(enFile, 'utf8');
  const options = { enPath: route, arPath, dict: route === '/erp/' ? erpDict : null };
  let html = arize(source, options);
  // Measure the finished Arabic page: if its body is still mostly English the long-form
  // article has not been translated yet, so it is published as-is but not as "Arabic".
  if (arabicShare(html) < 0.45) {
    untranslatedRoutes.push(arPath);
    html = arize(source, { ...options, untranslated: true });
  }
  mkdirSync(dirname(arFile), { recursive: true });
  writeFileSync(arFile, html);
  written += 1;
}

// Sitemap honesty: an Arabic twin that is still English inside is not advertised as Arabic.
if (untranslatedRoutes.length) {
  const sitemapFile = join(ROOT, 'sitemap.xml');
  const lines = readFileSync(sitemapFile, 'utf8').split('\n');
  const kept = lines
    .filter((line) => !untranslatedRoutes.some((p) => line.includes(`<loc>https://codeandcanvas.net${p}</loc>`)))
    .map((line) => untranslatedRoutes.reduce((acc, p) => acc.replace(new RegExp(`<xhtml:link rel="alternate" hreflang="ar" href="[^"]*${p}"\\s*/>`), ''), line));
  writeFileSync(sitemapFile, kept.join('\n'));
}

console.log(`Arabic pages: ${written} written${untranslatedRoutes.length ? ` · ${untranslatedRoutes.length} English-only long-form (noindex, kept out of the sitemap)` : ''}${skipped.length ? ` · ${skipped.length} skipped (no English source: ${skipped.join(', ')})` : ''}`);
