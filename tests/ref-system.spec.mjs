import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import { isolate, visit } from './helpers.mjs';

/* Acceptance for the UI ideas adapted from the REF study (2026-11-09).
   See docs/REF-UI-STUDY-2026-11.md. These assertions complement (not replace)
   the full axe matrix in tests/accessibility.spec.mjs. */

test('studio-system section: bilingual, both themes, no overflow 320→1440', async ({ page }) => {
  await isolate(page);
  for (const lang of ['en', 'ar']) {
    for (const theme of ['dark', 'light']) {
      for (const width of [320, 390, 1440]) {
        await page.setViewportSize({ width, height: 900 });
        await page.addInitScript((t) => localStorage.setItem('cc-theme', t), theme);
        // The generated /ar/ twin is a real page with data-ar attributes
        // stripped; /?lang=ar only switches the runtime and keeps them.
        await visit(page, lang === 'ar' ? '/ar/' : '/', lang);
        await page.evaluate(() => {
          // Disable reveal transforms so off-screen geometry is measurable.
          for (const el of document.querySelectorAll('[data-reveal]')) el.classList.add('is-in');
        });
        const state = await page.evaluate(() => ({
          h1: document.querySelectorAll('h1').length,
          overflow: document.documentElement.scrollWidth > innerWidth + 1,
          system: !!document.querySelector('#system'),
          layers: document.querySelectorAll('.system__layer').length,
          rail: document.querySelectorAll('.system__rail li').length,
          cta: document.querySelector('.system__cta a')?.getAttribute('href'),
          wordmark: !!document.querySelector('.footer__wordmark'),
          // The ghost type is decorative CSS-generated content: no DOM text
          // node, so it is never announced or audited as low-contrast copy.
          ghostDomText: document.querySelector('.system__ghost')?.textContent?.trim() ?? '',
          footerGhostDomText: document.querySelector('.footer__wordmark')?.textContent?.trim() ?? '',
          dataAr: document.querySelectorAll('[data-ar], [data-ar-label], [data-ar-html], [data-ar-alt]').length,
          theme: document.documentElement.getAttribute('data-theme'),
        }));
        expect(state.h1, `${lang}/${theme}/${width} one H1`).toBe(1);
        expect(state.overflow, `${lang}/${theme}/${width} no horizontal overflow`).toBe(false);
        expect(state.system, `${lang}/${theme}/${width} section present`).toBe(true);
        expect(state.layers).toBe(3);
        expect(state.rail).toBe(4);
        expect(state.cta).toBe(lang === 'ar' ? '/ar/methodology/' : '/methodology/');
        expect(state.wordmark).toBe(true);
        expect(state.ghostDomText).toBe('');
        expect(state.footerGhostDomText).toBe('');
        expect(state.theme).toBe(theme);
        if (lang === 'ar') expect(state.dataAr, `${lang}/${theme}/${width} Arabic twin has no data-ar leftovers`).toBe(0);
      }
    }
  }
});

test('/work/ case cards become a keyboard-reachable CSS snap rail on phones', async ({ page }) => {
  await isolate(page);
  await page.setViewportSize({ width: 390, height: 844 });
  await visit(page, '/work/', 'en');
  const rail = await page.evaluate(() => {
    const grid = document.querySelector('.cs-index-grid');
    const s = getComputedStyle(grid);
    return {
      display: s.display,
      snap: s.scrollSnapType,
      cards: grid.querySelectorAll('.cs-index-card').length,
      role: grid.getAttribute('role'),
      label: grid.getAttribute('aria-label'),
      tabindex: grid.getAttribute('tabindex'),
      overflow: document.documentElement.scrollWidth > innerWidth + 1,
    };
  });
  expect(rail.display).toBe('flex');
  expect(rail.snap).toContain('mandatory');
  expect(rail.cards).toBe(15);
  expect(rail.role).toBe('region');
  expect(rail.label).toBeTruthy();
  expect(rail.tabindex).toBe('0');
  expect(rail.overflow).toBe(false);
  await expect(page.locator('#installApp')).toBeHidden();
});

for (const lang of ['en', 'ar']) for (const theme of ['dark', 'light']) test(`axe ${lang} ${theme} home with REF components`, async ({ page }, info) => {
  await isolate(page);
  await page.setViewportSize({ width: 390, height: 900 });
  await page.addInitScript((t) => localStorage.setItem('cc-theme', t), theme);
  await visit(page, lang === 'ar' ? '/ar/' : '/', lang);
  await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 700) { scrollTo(0, y); await new Promise(r => setTimeout(r, 16)); } scrollTo(0, 0); });
  const result = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze();
  await info.attach('axe-summary', { body: JSON.stringify({ lang, theme, violations: result.violations.map(v => ({ id: v.id, nodes: v.nodes.map(n => ({ target: n.target, summary: n.failureSummary })) })) }), contentType: 'application/json' });
  expect(result.violations.map(v => ({ id: v.id, nodes: v.nodes.map(n => ({ target: n.target, summary: n.failureSummary })) }))).toEqual([]);
});
