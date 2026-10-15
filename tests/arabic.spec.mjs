import { test, expect } from '@playwright/test';
import { readFileSync } from 'node:fs';
import { isolate, visit } from './helpers.mjs';

/* /ar/… is a real Arabic site, not a client-side translation:
   self-canonical, reciprocal hreflang + x-default, Arabic markup with no
   `data-ar*` leftovers, and a language pill that links back to the English twin. */
const routes = JSON.parse(readFileSync(new URL('../manus-routes.json', import.meta.url))).routes
  .filter((r) => r.lang === 'ar')
  .map((r) => r.path);
const english = (route) => route.replace(/^\/ar/, '') || '/';
const absolute = (route) => `https://codeandcanvas.net${route}`;

for (const route of routes) {
  test(`arabic twin ${route}`, async ({ page }, info) => {
    await isolate(page);
    await page.goto(route);
    await expect(page.locator('html')).toHaveAttribute('lang', 'ar');
    await expect(page.locator('html')).toHaveAttribute('dir', 'rtl');
    const meta = await page.evaluate(() => ({
      canonical: document.querySelector('link[rel=canonical]')?.href,
      alternates: [...document.querySelectorAll('link[rel=alternate][hreflang]')].map((l) => [l.hreflang, l.href]),
      leftovers: document.querySelectorAll('[data-ar],[data-ar-html],[data-ar-label],[data-ar-title],[data-ar-alt],[data-ar-placeholder]').length,
      arabicLetters: (document.querySelector('main')?.innerText.match(/[\u0600-\u06FF]/g) ?? []).length,
      arabicAnywhere: (document.body.innerText.match(/[\u0600-\u06FF]/g) ?? []).length,
      langLink: document.querySelector('#langBtn')?.getAttribute('href') ?? null,
      h1: document.querySelectorAll('h1').length,
      graphs: [...document.querySelectorAll('script[type="application/ld+json"]')].map((e) => e.textContent.length),
    }));
    await info.attach('ar-check', { body: JSON.stringify(meta), contentType: 'application/json' });
    expect(meta.leftovers).toBe(0);
    expect(meta.h1).toBe(1);
    expect(meta.graphs.length).toBeGreaterThan(0);
    expect(meta.canonical).toBe(absolute(route));
    const map = Object.fromEntries(meta.alternates);
    expect(map.ar).toBe(absolute(route));
    expect(map.en).toBe(absolute(english(route)));
    expect(map['x-default']).toBe(map.en);
    if (!['/ar/'].includes(route)) expect(meta.langLink).toBe(english(route));
    // Tool routes (/read/, the ERP sheet) render their workspace from JavaScript in both
    // languages; there the Arabic lives in the chrome and in the markup the tools bind to.
    const tool = /\/(read|erp)\/$/.test(route);
    expect(meta.arabicAnywhere).toBeGreaterThan(120);
    if (!tool) expect(meta.arabicLetters).toBeGreaterThan(120);
  });
}

test('arabic twin keeps its language even when the query asks for English', async ({ page }) => {
  await isolate(page);
  await visit(page, '/ar/services/?lang=en', 'ar');
  await expect(page.locator('html')).toHaveAttribute('lang', 'ar');
  await expect(page.locator('main')).toContainText('الخدمات');
});

test.describe('arabic twin without JavaScript', () => {
  test.use({ javaScriptEnabled: false });
  test('the markup alone carries the Arabic content', async ({ page }) => {
    await page.goto('/ar/services/');
    const text = await page.locator('main').innerText();
    expect((text.match(/[\u0600-\u06FF]/g) ?? []).length).toBeGreaterThan(1500);
    await expect(page.locator('html')).toHaveAttribute('dir', 'rtl');
  });
});

test('the language pill navigates to the Arabic twin and keeps the query', async ({ page }) => {
  await isolate(page);
  await visit(page, '/contact/?inquiry=HC-03');
  await page.locator('#langBtn').click();
  await page.waitForURL((u) => u.pathname === '/ar/contact/' && u.searchParams.get('inquiry') === 'HC-03');
  await expect(page.locator('html')).toHaveAttribute('lang', 'ar');
  await expect(page.locator('html')).toHaveAttribute('dir', 'rtl');
  await expect(page.locator('#c-inquiry')).toHaveValue(/^HC-03 /);
  await page.locator('#langBtn').click();
  await page.waitForURL((u) => u.pathname === '/contact/' && u.searchParams.get('inquiry') === 'HC-03');
  await expect(page.locator('html')).toHaveAttribute('lang', 'en');
});
