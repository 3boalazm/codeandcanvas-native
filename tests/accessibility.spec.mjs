import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import { isolate, visit } from './helpers.mjs';

/* Accessibility matrix: every core journey (including the new growth layer)
   in both languages, plus the standalone Arabic twins. /ar/ routes lock their
   own language in the markup, so they are checked as Arabic only. */
const routes = [
  '/', '/about/', '/our-story/', '/services/', '/technology-services/', '/creative-services/',
  '/healthcare/', '/contact/', '/pricing-faq/', '/case-studies/', '/books/',
  '/books/marketing-fundamentals/read/', '/register/', '/checkout/', '/blog/', '/team/',
  '/system/', '/work/', '/work/bilingual-brand-system/', '/work/packaging-print-system/', '/work/zad/',
  '/services/brand-identity-design/', '/services/website-design-development/',
  '/book/', '/resources/', '/claims/', '/saudi-arabia/', '/egypt/',
  '/privacy-policy/', '/terms-of-use/', '/cookie-policy/',
  '/blog/from-brand-identity-to-brand-systems/', '/blog/creative-strategy-in-the-age-of-generative-ai/',
];
const lockedArabic = ['/ar/', '/ar/book/', '/ar/work/', '/ar/work/zad/', '/ar/services/', '/ar/erp/', '/ar/system/'];

for (const route of routes) for (const lang of ['en', 'ar']) test(`axe ${route} ${lang}`, async ({ page }, info) => {
  await isolate(page);
  await page.setViewportSize({ width: lang === 'ar' ? 390 : 1440, height: 900 });
  await visit(page, route, lang);
  // Reveal all below-fold sections through actual scrolling before scanning.
  await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 700) { scrollTo(0, y); await new Promise(r => setTimeout(r, 16)); } scrollTo(0, 0); });
  const result = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze();
  await info.attach('axe-summary', { body: JSON.stringify({ route, lang, violations: result.violations.map(v => ({ id: v.id, impact: v.impact, nodes: v.nodes.map(n => ({ target: n.target, summary: n.failureSummary })) })), incomplete: result.incomplete.map(v => ({ id: v.id, nodes: v.nodes.length })), passes: result.passes.length }), contentType: 'application/json' });
  expect(result.violations.map(v => ({ id: v.id, nodes: v.nodes.map(n => ({ target: n.target, summary: n.failureSummary })) }))).toEqual([]);
});

for (const route of lockedArabic) test(`axe locked Arabic twin ${route}`, async ({ page }, info) => {
  await isolate(page);
  await page.setViewportSize({ width: 390, height: 900 });
  await visit(page, route, 'ar');
  await expect(page.locator('html')).toHaveAttribute('lang', 'ar');
  await expect(page.locator('html')).toHaveAttribute('dir', 'rtl');
  const result = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze();
  await info.attach('axe-summary', { body: JSON.stringify({ route, lang: 'ar-locked', violations: result.violations.map(v => ({ id: v.id, nodes: v.nodes.map(n => ({ target: n.target, summary: n.failureSummary })) })), passes: result.passes.length }), contentType: 'application/json' });
  expect(result.violations.map(v => v.id)).toEqual([]);
});
