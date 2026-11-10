import { test, expect } from '@playwright/test';
import { isolate, visit } from './helpers.mjs';

/* Locks the 2026-11 buyer-audit fixes. Each test names the promise it protects:

   1. A "Book a call" CTA must land on the real scheduler, not a message draft.
   2. Credentials must never be implied — the frameworks are labeled as context.
   3. Internal delivery state ("owner gate") must not appear in customer copy.
   4. /evidence/ must publish the four decisions plus the honest evidence split.
*/

const ROUTES = ['/', '/ar/', '/pricing-faq/', '/ar/pricing-faq/', '/about/', '/ar/about/', '/team/', '/ar/team/'];

for (const route of ROUTES) test(`no credential badge and no internal state — ${route}`, async ({ page }) => {
  await isolate(page);
  await visit(page, route, route.startsWith('/ar/') ? 'ar' : 'en');
  const text = await page.evaluate(() => document.body.innerText);
  expect(text, 'owner-gate wording is internal').not.toMatch(/owner gate|بانتظار المالك/i);
  expect(text, 'no credential-status FAQ').not.toMatch(/Are your credentials active|هل اعتماداتكم سارية/i);
  /* The framework chips are allowed; a "Credentials" label is not, because it
     reads as a personal certification claim. */
  const labels = await page.evaluate(() => [...document.querySelectorAll('[aria-label]')]
    .map((el) => el.getAttribute('aria-label')).filter(Boolean));
  expect(labels.filter((l) => /^(credentials|الاعتمادات)$/i.test(l.trim()))).toEqual([]);
});

test('every booking CTA resolves to the first-party scheduler', async ({ page }) => {
  await isolate(page);
  for (const route of ['/', '/ar/', '/pricing-faq/', '/about/', '/services/', '/creative-services/', '/technology-services/']) {
    await visit(page, route, route.startsWith('/ar/') ? 'ar' : 'en');
    const hrefs = await page.evaluate(() => [...document.querySelectorAll('a[href]')]
      .map((a) => a.getAttribute('href'))
      .filter((h) => h && /contact\/.*#book/.test(h)));
    expect(hrefs, `${route} still points a booking CTA at the contact form`).toEqual([]);
  }
  await visit(page, '/book/', 'en');
  await expect(page.locator('#book-form')).toBeVisible();
  await expect(page.locator('#b-slots')).toBeVisible();
});

for (const [lang, route] of [['en', '/evidence/'], ['ar', '/ar/evidence/']]) {
  test(`/evidence/ publishes the decisions and the evidence split — ${lang}`, async ({ page }) => {
    await isolate(page);
    await page.setViewportSize({ width: 1440, height: 900 });
    await visit(page, route, lang);
    const band = page.locator('#decisions');
    await expect(band.locator('.decision')).toHaveCount(4);
    await expect(band.locator('.decision__cell--do')).toHaveCount(4);
    await expect(band.locator('.decision__cell--refuse')).toHaveCount(4);
    await expect(page.locator('#status table tbody tr')).toHaveCount(4);
    await expect(page.locator('#tiers .tiercta')).toHaveCount(4);
    /* The page makes no outcome claim: results are always stated as a limit. */
    const text = await page.evaluate(() => document.body.innerText);
    expect(text).toMatch(lang === 'ar' ? /لا نتيجة مُقاسة/ : /No measured outcome/);
  });
}

test('the decision blocks and tiers survive 320px and RTL', async ({ page }) => {
  await isolate(page);
  for (const [width, route, lang] of [[320, '/evidence/', 'en'], [320, '/ar/evidence/', 'ar'], [1024, '/evidence/', 'en']]) {
    await page.setViewportSize({ width, height: 900 });
    await visit(page, route, lang);
    const m = await page.evaluate(() => ({
      overflow: document.documentElement.scrollWidth > innerWidth + 1,
      clipped: [...document.querySelectorAll('.decision, .tiercta')]
        .filter((el) => el.scrollWidth > el.clientWidth + 2).length,
      cards: document.querySelectorAll('.decision').length,
    }));
    expect(m.overflow, `${route} @${width} horizontal overflow`).toBe(false);
    expect(m.clipped, `${route} @${width} clipped decision panels`).toBe(0);
    expect(m.cards).toBe(4);
  }
});
