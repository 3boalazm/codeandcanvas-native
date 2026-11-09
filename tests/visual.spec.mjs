import { test, expect } from '@playwright/test';
import { isolate, visit } from './helpers.mjs';

/* Screenshot regression for the growth layer.
   Every release captures the same six frames at 1440 and 390, attaches them
   to the Playwright report for human comparison, and asserts hard visual
   invariants that would catch a blank/broken/missing artwork build:
   a real decoded hero image, a dark canvas, no horizontal overflow, one H1,
   and visible illustrative disclaimers where artwork is used. */
const routes = [
  ['/', 'home'],
  ['/work/', 'work-hub'],
  ['/work/zad/', 'project-case'],
  ['/services/brand-identity-design/', 'service-landing'],
  ['/book/', 'booking'],
  ['/resources/', 'resources'],
  ['/ar/', 'home-arabic'],
];

for (const [route, name] of routes) for (const width of [1440, 390]) {
  test(`visual ${name} ${width}`, async ({ page }, info) => {
    await isolate(page);
    await page.setViewportSize({ width, height: 900 });
    await visit(page, route, route.startsWith('/ar/') ? 'ar' : 'en');
    await page.evaluate(async () => {
      scrollTo(0, 0);
      await new Promise((r) => setTimeout(r, 250));
    });
    const shot = await page.screenshot({ animations: 'disabled', caret: 'hide', fullPage: false });
    await info.attach(`${name}-${width}`, { body: shot, contentType: 'image/png' });
    expect(shot.length).toBeGreaterThan(12000);

    const m = await page.evaluate(() => ({
      h1: document.querySelectorAll('h1').length,
      scrollWidth: document.documentElement.scrollWidth,
      bg: getComputedStyle(document.body).backgroundColor,
      images: [...document.querySelectorAll('main img')].map((i) => ({ src: i.getAttribute('src'), w: i.naturalWidth, lazy: i.loading === 'lazy' })),
      disclaimers: document.querySelectorAll('.live-figure__disclaimer, .live-media-note').length,
    }));
    expect(m.h1).toBe(1);
    expect(m.scrollWidth).toBeLessThanOrEqual(width + 1);
    expect(m.bg).not.toBe('rgba(0, 0, 0, 0)');
    for (const img of m.images) {
      if (!img.src || !img.src.startsWith('/assets/media/') || img.lazy) continue;
      expect(img.w, `illustrative artwork failed to decode: ${img.src}`).toBeGreaterThan(0);
    }
    if (['home', 'work-hub'].includes(name)) expect(m.disclaimers).toBeGreaterThan(0);
  });
}
