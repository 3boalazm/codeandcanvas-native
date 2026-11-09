import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import { isolate, visit } from './helpers.mjs';

/* Acceptance for the owner-safe Phase 2 of the REF study: /system/.
   See docs/REF-UI-STUDY-2026-11.md §7. No reference pixels, no external
   assets, no fabricated metrics, no runtime blur and no always-on motion. */

test('design-system page: bilingual, both themes, 320→1440, component contracts', async ({ page }) => {
  test.setTimeout(120000);
  await isolate(page);
  await page.context().grantPermissions(['clipboard-read', 'clipboard-write'], { origin: 'http://127.0.0.1:3000' }).catch(() => {});
  for (const lang of ['en', 'ar']) {
    for (const theme of ['dark', 'light']) {
      for (const width of [320, 390, 1440]) {
        await page.setViewportSize({ width, height: 900 });
        await page.addInitScript((t) => localStorage.setItem('cc-theme', t), theme);
        await visit(page, lang === 'ar' ? '/ar/system/' : '/system/', lang);
        await page.evaluate(() => {
          for (const el of document.querySelectorAll('[data-reveal]')) el.classList.add('is-in');
        });
        const state = await page.evaluate(() => ({
          h1: document.querySelectorAll('h1').length,
          overflow: document.documentElement.scrollWidth > innerWidth + 1,
          theme: document.documentElement.getAttribute('data-theme'),
          tokens: document.querySelectorAll('.sys-token').length,
          bento: document.querySelectorAll('.sys-bento__card').length,
          inventory: document.querySelectorAll('.sys-inventory__card').length,
          slits: document.querySelectorAll('.sys-slit__item').length,
          orbit: document.querySelectorAll('.sys-orbit__tile').length,
          profiles: document.querySelectorAll('.sys-profile').length,
          core: !!document.querySelector('.sys-orbit__core'),
          dataAr: document.querySelectorAll('[data-ar], [data-ar-label], [data-ar-html], [data-ar-alt]').length,
          externalImages: [...document.querySelectorAll('main img')].filter((i) => !String(i.getAttribute('src') || '').startsWith('/assets/media/')).map((i) => i.getAttribute('src')),
          externalCss: [...document.querySelectorAll('link[rel="stylesheet"]')].filter((l) => !String(l.getAttribute('href') || '').startsWith('/assets/css/')).map((l) => l.getAttribute('href')),
          // The shared footer always loads Vercel's first-party insights script;
          // only third-party absolute URLs count as external here.
          externalScripts: [...document.querySelectorAll('script[src]')].filter((s) => {
            const src = String(s.getAttribute('src') || '');
            return !src.startsWith('/assets/js/') && src !== '/_vercel/insights/script.js';
          }).map((s) => s.getAttribute('src')),
          infinite: [...document.querySelectorAll('.sys-token, .sys-bento__card, .sys-inventory__card, .sys-slit__item, .sys-orbit__tile, .sys-profile')].filter((el) => {
            const c = getComputedStyle(el);
            return c.animationName !== 'none' && c.animationIterationCount === 'infinite';
          }).length,
          blurred: [...document.querySelectorAll('.sys-token, .sys-bento__card, .sys-inventory__card, .sys-slit__item, .sys-orbit, .sys-profile')].filter((el) => {
            const c = getComputedStyle(el);
            return c.backdropFilter !== 'none' || c.filter.includes('blur(');
          }).length,
        }));
        const label = `${lang}/${theme}/${width}`;
        expect(state.h1, `${label} one H1`).toBe(1);
        expect(state.overflow, `${label} no horizontal overflow`).toBe(false);
        expect(state.theme).toBe(theme);
        expect(state.tokens).toBe(6);
        expect(state.bento).toBe(6);
        expect(state.inventory).toBe(6);
        expect(state.slits).toBe(4);
        expect(state.orbit).toBe(8);
        expect(state.profiles).toBe(2);
        expect(state.core).toBe(true);
        expect(state.externalImages).toEqual([]);
        expect(state.externalCss).toEqual([]);
        expect(state.externalScripts).toEqual([]);
        expect(state.infinite).toBe(0);
        expect(state.blurred).toBe(0);
        if (lang === 'ar') expect(state.dataAr, `${label} Arabic twin has no data-ar leftovers`).toBe(0);
      }
    }
  }
});

test('design-system interactions: CSS-only accordion and token copy', async ({ page }) => {
  await isolate(page);
  await page.context().grantPermissions(['clipboard-read', 'clipboard-write'], { origin: 'http://127.0.0.1:3000' }).catch(() => {});
  await page.setViewportSize({ width: 390, height: 844 });
  await visit(page, '/system/', 'en');
  const slit = page.locator('.sys-slit__item').nth(1);
  await slit.locator('summary').click();
  await expect(slit).toHaveAttribute('open', '');
  const third = page.locator('.sys-slit__item').nth(2);
  await third.locator('summary').focus();
  await page.keyboard.press('Enter');
  await expect(third).toHaveAttribute('open', '');
  const copy = page.locator('.sys-token__copy').first();
  await copy.click();
  // The clipboard write is asynchronous; wait for the live region, never race it.
  await expect(page.locator('#sys-copy-status')).toHaveText(/Copied|Copy unavailable|تم النسخ|تعذّر/, { timeout: 5000 });
});

for (const lang of ['en', 'ar']) for (const theme of ['dark', 'light']) test(`axe ${lang} ${theme} /system/`, async ({ page }, info) => {
  await isolate(page);
  await page.setViewportSize({ width: 390, height: 900 });
  await page.addInitScript((t) => localStorage.setItem('cc-theme', t), theme);
  await visit(page, lang === 'ar' ? '/ar/system/' : '/system/', lang);
  await page.evaluate(async () => {
    for (let y = 0; y < document.body.scrollHeight; y += 700) { scrollTo(0, y); await new Promise(r => setTimeout(r, 12)); }
    scrollTo(0, 0);
  });
  const result = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze();
  await info.attach('axe-summary', { body: JSON.stringify({ lang, theme, violations: result.violations.map(v => ({ id: v.id, nodes: v.nodes.map(n => ({ target: n.target, summary: n.failureSummary })) })) }), contentType: 'application/json' });
  expect(result.violations.map(v => ({ id: v.id, nodes: v.nodes.map(n => ({ target: n.target, summary: n.failureSummary })) }))).toEqual([]);
});
