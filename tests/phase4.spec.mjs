import { test, expect } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { isolate, visit } from './helpers.mjs';

/* Phase 4 of docs/REF-UI-STUDY-2026-11.md §9: the remaining identity-fit B
   mechanisms that need no owner asset. Locks the static loop, concentric rings,
   process path, step bar and labelled art card in EN/AR × dark/light ×
   320/390/1440, with no CDN, canvas, blur, always-on animation, foreign skin
   or fabricated metric. Complements scripts/check-phase4.mjs. */

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const study = fs.readFileSync(path.join(ROOT, 'docs/REF-UI-STUDY-2026-11.md'), 'utf8');

const NEW_SEL = [
  '.sys-loop', '.sys-loop__pill', '.sys-loop__core',
  '.sys-concentric', '.sys-concentric__ring', '.sys-concentric__label', '.sys-concentric__note',
  '.sys-process', '.sys-process__curve', '.sys-steps', '.sys-step',
  '.sys-stepbar', '.sys-stepbar__node',
  '.sys-artcard', '.sys-artcard__caption', '.sys-artcard__ctas', '.sys-artcard__ctas .btn',
].join(', ');

test('Phase 4 plan stays locked in the dated study', () => {
  expect(study).toMatch(/## 9\. Phase 4/);
  expect(study).toMatch(/Phase 4 —/);
  expect(study).toMatch(/static capability loop/);
  expect(study).toMatch(/017\/037\/052/);
  expect(fs.existsSync(path.join(ROOT, 'scripts/check-phase4.mjs'))).toBe(true);
});

test('Phase 4 sections: EN/AR × dark/light × 320/390/1440, no no-go signature', async ({ page }) => {
  test.setTimeout(180000);
  await isolate(page);
  for (const lang of ['en', 'ar']) {
    for (const theme of ['dark', 'light']) {
      for (const width of [320, 390, 1440]) {
        await page.setViewportSize({ width, height: 900 });
        await page.addInitScript((t) => localStorage.setItem('cc-theme', t), theme);
        await visit(page, lang === 'ar' ? '/ar/system/' : '/system/', lang);
        await page.evaluate(() => {
          for (const el of document.querySelectorAll('[data-reveal]')) el.classList.add('is-in');
        });
        const state = await page.evaluate((sel) => {
          const abs = (u) => !!u && /^(https?:)?\/\//.test(u);
          const stripSans = (f) => String(f).replace(/sans-serif/gi, '');
          const els = [...document.querySelectorAll(sel)];
          return {
            h1: document.querySelectorAll('h1').length,
            overflow: document.documentElement.scrollWidth > innerWidth + 1,
            theme: document.documentElement.getAttribute('data-theme'),
            loopPills: document.querySelectorAll('.sys-loop__pill').length,
            concentricRings: document.querySelectorAll('.sys-concentric__ring').length,
            steps: document.querySelectorAll('.sys-step').length,
            stepbar: document.querySelectorAll('.sys-stepbar__node').length,
            artcards: document.querySelectorAll('.sys-artcard').length,
            artCtas: document.querySelectorAll('.sys-artcard__ctas .btn').length,
            curves: document.querySelectorAll('.sys-process__curve').length,
            externalScripts: [...document.querySelectorAll('script[src]')].map((s) => s.getAttribute('src')).filter(abs),
            externalCss: [...document.querySelectorAll('link[rel="stylesheet"]')].map((l) => l.getAttribute('href')).filter(abs),
            externalImages: [...document.querySelectorAll('img')].flatMap((i) => [i.getAttribute('src'), i.getAttribute('srcset')]).filter(abs),
            canvas: document.querySelectorAll('canvas').length,
            heavyGlobals: ['gsap', 'ScrollTrigger', 'THREE'].filter((k) => typeof window[k] !== 'undefined'),
            blurred: els.filter((el) => {
              const c = getComputedStyle(el);
              return c.filter.includes('blur(') || (c.backdropFilter && c.backdropFilter !== 'none');
            }).length,
            infinite: els.filter((el) => {
              const c = getComputedStyle(el);
              return c.animationName !== 'none' && c.animationIterationCount === 'infinite';
            }).length,
            serifFonts: els.filter((el) => el.tagName !== 'svg' && /\bserif\b/i.test(stripSans(getComputedStyle(el).fontFamily))).length,
            cyanOrangeText: els.filter((el) => /\b(cyan|orange)\b/i.test(getComputedStyle(el).color)).length,
            fabricated: (document.querySelector('main')?.innerText || '')
              .match(/\b\d+(?:\.\d+)?\s*%|\$\s*\d|\b\d+\s*[KMB]\b/g) || [],
            dataAr: document.querySelectorAll('[data-ar], [data-ar-label], [data-ar-html], [data-ar-alt]').length,
          };
        }, NEW_SEL);

        const label = `${lang}/${theme}/${width}`;
        expect(state.h1, `${label} one H1`).toBe(1);
        expect(state.overflow, `${label} no horizontal overflow`).toBe(false);
        expect(state.theme).toBe(theme);
        expect(state.loopPills, `${label} eight static capability pills`).toBe(8);
        expect(state.concentricRings, `${label} three concentric rings`).toBe(3);
        expect(state.steps, `${label} four process steps`).toBe(4);
        expect(state.stepbar, `${label} four step-bar nodes`).toBe(4);
        expect(state.artcards, `${label} one labelled art card`).toBe(1);
        expect(state.artCtas, `${label} paired CTAs`).toBe(2);
        expect(state.curves, `${label} one static SVG curve`).toBe(1);
        expect(state.externalScripts, `${label} no CDN scripts`).toEqual([]);
        expect(state.externalCss, `${label} no CDN stylesheets`).toEqual([]);
        expect(state.externalImages, `${label} no third-party images`).toEqual([]);
        expect(state.canvas, `${label} no canvas`).toBe(0);
        expect(state.heavyGlobals, `${label} no heavy JS library`).toEqual([]);
        expect(state.blurred, `${label} no runtime blur on Phase 4 elements`).toBe(0);
        expect(state.infinite, `${label} no always-on animation`).toBe(0);
        expect(state.serifFonts, `${label} no serif skin`).toBe(0);
        expect(state.cyanOrangeText, `${label} no cyan/orange skin`).toBe(0);
        expect(state.fabricated, `${label} no fabricated metric`).toEqual([]);
        if (lang === 'ar') expect(state.dataAr, `${label} no data-ar leftovers`).toBe(0);
      }
    }
  }
});
