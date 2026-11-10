import { test, expect } from '@playwright/test';
import { isolate, visit } from './helpers.mjs';

/* Regression lock for the home `/system/` band (2026-11-10).

   The band shipped new markup while returning visitors still held an hour-old
   `/assets/css/home.css`, so it rendered as unstyled stacked text: no cards, no
   rail, an empty CTA half. These tests fail if either half of that pairing
   breaks again — the stylesheet must actually reach the browser, and the band
   must lay itself out as three cards, a four-step rail and a two-column CTA. */

const BAND = '#system';

test('the /system/ stylesheet is versioned and actually applied', async ({ page }) => {
  await isolate(page);
  await visit(page, '/', 'en');

  /* 1 · the stylesheet URL carries a content hash, and it loaded successfully. */
  const sheets = await page.evaluate(() => [...document.styleSheets].map((s) => ({
    href: s.href ? new URL(s.href).pathname + new URL(s.href).search : null,
    rules: (() => { try { return s.cssRules.length; } catch { return -1; } })(),
  })).filter((s) => s.href && /home\.css/.test(s.href)));

  expect(sheets.length, 'home.css is linked').toBe(1);
  expect(sheets[0].href, 'home.css is content-hashed').toMatch(/home\.css\?v=[0-9a-f]{6,}/);
  expect(sheets[0].rules, 'home.css parsed (no 404 / empty file)').toBeGreaterThan(50);

  /* 2 · the band's own rules are live in the browser, not just on disk. */
  const applied = await page.evaluate(() => {
    const layer = document.querySelector('.system__layer');
    const venn = document.querySelector('.system__venn');
    const rail = document.querySelector('.system__rail');
    const cta = document.querySelector('.system__cta');
    const cs = (el) => el && getComputedStyle(el);
    return {
      vennDisplay: cs(venn)?.display,
      layerRadius: cs(layer)?.borderTopLeftRadius,
      layerBorder: cs(layer)?.borderTopStyle,
      railDisplay: cs(rail)?.display,
      ctaDisplay: cs(cta)?.display,
    };
  });
  expect(applied.vennDisplay, '.system__venn is a grid/flex container').toMatch(/grid|flex/);
  expect(applied.layerRadius, '.system__layer is a card, not bare text').not.toBe('0px');
  expect(applied.layerBorder, '.system__layer has a visible border').toBe('solid');
  expect(applied.railDisplay).toMatch(/grid|flex/);
  expect(applied.ctaDisplay).toMatch(/grid|flex/);
});

for (const [lang, route] of [['en', '/'], ['ar', '/ar/']]) {
  test(`/system/ band structure and layout — ${lang}`, async ({ page }, info) => {
    await isolate(page);
    for (const width of [1440, 1024, 390, 320]) {
      await page.setViewportSize({ width, height: 900 });
      await visit(page, route, lang);

      const band = page.locator(BAND);
      await expect(band).toBeVisible();

      /* Structure: three layers, four steps, two CTAs — nothing dropped. */
      await expect(band.locator('.system__layer')).toHaveCount(3);
      await expect(band.locator('.system__tag')).toHaveCount(3);
      await expect(band.locator('.system__rail-no')).toHaveCount(4);
      await expect(band.locator('.system__cta .btn')).toHaveCount(2);

      /* Layout: no card is collapsed, overlapping or clipped, and every card
         keeps readable height on every breakpoint. */
      const boxes = await band.locator('.system__layer').evaluateAll((els) => els.map((el) => {
        const r = el.getBoundingClientRect();
        return { w: Math.round(r.width), h: Math.round(r.height), x: Math.round(r.x), y: Math.round(r.y) };
      }));
      await info.attach(`system-${lang}-${width}`, { body: JSON.stringify(boxes), contentType: 'application/json' });
      for (const b of boxes) {
        expect(b.w, `${route} @${width}: card width`).toBeGreaterThan(120);
        /* A card carries number + heading + a 3–4 line paragraph + a tag rule,
           so anything under 120px tall means the stylesheet collapsed it. */
        expect(b.h, `${route} @${width}: card height`).toBeGreaterThan(120);
      }
      /* No vertical overlap between consecutive cards (stacked on phones,
         side by side on desktop — either way their boxes must not collide). */
      for (let i = 1; i < boxes.length; i += 1) {
        const a = boxes[i - 1];
        const c = boxes[i];
        const overlaps = a.x < c.x + c.w && c.x < a.x + a.w && a.y < c.y + c.h - 2 && c.y < a.y + a.h - 2;
        expect(overlaps, `${route} @${width}: cards ${i} and ${i + 1} overlap`).toBe(false);
      }

      /* Copy must not overflow its card. */
      const clipped = await band.locator('.system__layer').evaluateAll((els) => els.filter((el) => el.scrollHeight > el.clientHeight + 2).length);
      expect(clipped, `${route} @${width}: cards clipping their copy`).toBe(0);
    }
  });
}
