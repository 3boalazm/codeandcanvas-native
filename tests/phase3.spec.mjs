import { test, expect } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { isolate, visit } from './helpers.mjs';

/* Phase 3 of docs/REF-UI-STUDY-2026-11.md §3 is a rejection list, not a build
   backlog. These tests lock that decision in the browser: no CDN/library, no
   canvas/WebGL, no orange/cyan/serif skin, no runtime blur or always-on
   animation, no third-party imagery, no fabricated metric and no untranslated
   AR attribute. They complement scripts/check-phase3.mjs, which scans the
   generated sources statically inside `npm run check`. */

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const study = fs.readFileSync(path.join(ROOT, 'docs/REF-UI-STUDY-2026-11.md'), 'utf8');

test('Phase 3 rejection list stays locked in the dated study', () => {
  expect(study).toMatch(/Phase 3 — deliberately rejected/);
  expect(study).toMatch(/fabricated metrics\/charts/);
  expect(study).toMatch(/orange\/cyan\/serif skins/);
  expect(study).toMatch(/runtime blur\/WebGL/);
  expect(study).toMatch(/REF 060/);
  expect(fs.existsSync(path.join(ROOT, 'scripts/check-phase3.mjs'))).toBe(true);
});

for (const lang of ['en', 'ar']) for (const theme of ['dark', 'light']) {
  test(`phase3 no-go browser contract ${lang}/${theme}`, async ({ page }) => {
    await isolate(page);
    await page.setViewportSize({ width: 390, height: 900 });
    await page.addInitScript((t) => localStorage.setItem('cc-theme', t), theme);
    await visit(page, lang === 'ar' ? '/ar/system/' : '/system/', lang);

    const state = await page.evaluate(() => {
      const abs = (u) => !!u && /^(https?:)?\/\//.test(u);
      const sys = [...document.querySelectorAll('[class*="sys-"]')];
      const stripSans = (f) => String(f).replace(/sans-serif/gi, '');
      return {
        externalScripts: [...document.querySelectorAll('script[src]')]
          .map((s) => s.getAttribute('src')).filter(abs),
        externalCss: [...document.querySelectorAll('link[rel="stylesheet"]')]
          .map((l) => l.getAttribute('href')).filter(abs),
        externalImages: [...document.querySelectorAll('img')]
          .flatMap((i) => [i.getAttribute('src'), i.getAttribute('srcset')]).filter(abs),
        canvas: document.querySelectorAll('canvas').length,
        heavyGlobals: ['gsap', 'ScrollTrigger', 'THREE'].filter((k) => typeof window[k] !== 'undefined'),
        blurred: sys.filter((el) => {
          const c = getComputedStyle(el);
          return c.filter.includes('blur(') || (c.backdropFilter && c.backdropFilter !== 'none');
        }).length,
        infinite: sys.filter((el) => {
          const c = getComputedStyle(el);
          return c.animationName !== 'none' && c.animationIterationCount === 'infinite';
        }).length,
        serifFonts: sys.filter((el) => /\bserif\b/i.test(stripSans(getComputedStyle(el).fontFamily))).length,
        cyanOrangeText: sys.filter((el) => /\b(cyan|orange)\b/i.test(getComputedStyle(el).color)).length,
        fabricated: (document.querySelector('main')?.innerText || '')
          .match(/\b\d+(?:\.\d+)?\s*%|\$\s*\d|\b\d+\s*[KMB]\b/g) || [],
        guardCards: document.querySelectorAll('.sys-guard__card').length,
        guardBadges: [...document.querySelectorAll('.sys-guard__badge')].map((b) => b.textContent.trim()),
        dataAr: document.querySelectorAll('[data-ar], [data-ar-label], [data-ar-html], [data-ar-alt]').length,
        theme: document.documentElement.getAttribute('data-theme'),
      };
    });

    const label = `${lang}/${theme}`;
    expect(state.theme).toBe(theme);
    expect(state.externalScripts, `${label} no CDN scripts`).toEqual([]);
    expect(state.externalCss, `${label} no CDN stylesheets`).toEqual([]);
    expect(state.externalImages, `${label} no third-party images`).toEqual([]);
    expect(state.canvas, `${label} no canvas/WebGL surface`).toBe(0);
    expect(state.heavyGlobals, `${label} no heavy JS library`).toEqual([]);
    expect(state.blurred, `${label} no runtime blur`).toBe(0);
    expect(state.infinite, `${label} no always-on animation`).toBe(0);
    expect(state.serifFonts, `${label} no serif skin`).toBe(0);
    expect(state.cyanOrangeText, `${label} no cyan/orange skin`).toBe(0);
    expect(state.fabricated, `${label} no fabricated metric`).toEqual([]);
    expect(state.guardCards, `${label} six published no-go cards`).toBe(6);
    expect(state.guardBadges, `${label} every no-go card is labelled NO / لا`).toEqual(
      Array(6).fill(lang === 'ar' ? 'لا' : 'NO'),
    );
    if (lang === 'ar') expect(state.dataAr, `${label} no data-ar leftovers`).toBe(0);
  });
}
