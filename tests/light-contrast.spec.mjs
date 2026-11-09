import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import { isolate, visit } from './helpers.mjs';

/* Lock the 2026-11-09 light-theme contrast pass. The default suite runs dark,
   which is the brand default; these two tests scan the opt-in light theme in
   both languages on the main marketing and evidence routes. Bright navy-only
   accent inks are re-inked in ds.css / home.css / live.css / case-study.css. */
const routes = [
  '/', '/about/', '/services/', '/technology-services/', '/creative-services/',
  '/healthcare/', '/contact/', '/pricing-faq/', '/case-studies/', '/books/',
  '/methodology/', '/claims/', '/blog/', '/team/', '/resources/', '/book/',
  '/work/', '/work/zad/',
];

for (const lang of ['en', 'ar']) test(`light-theme axe matrix ${lang}`, async ({ page }, info) => {
  test.setTimeout(180000);
  await isolate(page);
  await page.setViewportSize({ width: 390, height: 900 });
  await page.addInitScript(() => localStorage.setItem('cc-theme', 'light'));
  const findings = [];
  for (const route of routes) {
    const path = lang === 'ar' ? (route === '/' ? '/ar/' : `/ar${route}`) : route;
    await visit(page, path, lang);
    await expect(page.locator('html')).toHaveAttribute('data-theme', 'light');
    await page.evaluate(async () => {
      for (let y = 0; y < document.body.scrollHeight; y += 700) {
        scrollTo(0, y);
        await new Promise(r => setTimeout(r, 8));
      }
      scrollTo(0, 0);
    });
    const result = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze();
    for (const v of result.violations) for (const n of v.nodes) {
      findings.push({ lang, path, id: v.id, target: n.target.join(' | '), summary: n.failureSummary.replace(/\s+/g, ' ').slice(0, 240) });
    }
  }
  await info.attach('axe-light-summary', { body: JSON.stringify({ lang, routes: routes.length, findings }), contentType: 'application/json' });
  expect(findings).toEqual([]);
});
