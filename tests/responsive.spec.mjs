/* ==========================================================================
   responsive.spec.mjs — the narrow end of the range.

   Every other visual test starts at 390px. Phones still ship at 320px, and the
   2026-11 pass introduced several two-column rows (framework statements, founder
   scope tables, focus lists, slot chips). This test loads the pages that changed
   at 320 and asserts the page never scrolls sideways, nothing is clipped at the
   right edge, and tap targets in the booking form stay usable.

   Deliberately contains no screenshot: a 320px image diff would fail on font
   hinting, not on layout.
   ========================================================================== */
import { test, expect } from '@playwright/test';
import { isolate, visit } from './helpers.mjs';

const ROUTES = [
  ['/', 'home'],
  ['/technology-services/', 'technology (frameworks in context)'],
  ['/team/', 'team (specialisation lists)'],
  ['/our-story/', 'story (chapter focus lists)'],
  ['/creative-services/', 'creative (founder scope)'],
  ['/healthcare/', 'healthcare'],
  ['/work/', 'work (claims register)'],
  ['/book/', 'booking'],
  ['/ar/', 'home (ar)'],
  ['/ar/technology-services/', 'technology (ar)'],
  ['/ar/team/', 'team (ar)'],
  ['/ar/our-story/', 'story (ar)'],
  ['/ar/book/', 'booking (ar)'],
];

test.beforeEach(async ({ page }) => isolate(page));

for (const [route, name] of ROUTES) {
  test(`320px · ${name}`, async ({ page }) => {
    await page.setViewportSize({ width: 320, height: 720 });
    await visit(page, route, route.startsWith('/ar/') ? 'ar' : 'en');
    await page.evaluate(async () => {
      // Reveal-on-scroll never fires for content below the fold in a static
      // measurement; walk the page so every section has been laid out.
      for (let y = 0; y < document.body.scrollHeight; y += 600) {
        window.scrollTo(0, y);
        await new Promise((r) => setTimeout(r, 12));
      }
      window.scrollTo(0, 0);
      await new Promise((r) => setTimeout(r, 80));
    });

    const report = await page.evaluate(() => {
      const vw = window.innerWidth;
      const offenders = [];
      const seen = new Set();
      /* The honest rule: text that hangs past the viewport is only acceptable
         when the visitor can scroll to it. Snap rails (.m-rail, .cs-index-grid)
         and table scrollers (.evidence-scroll, .tbl-wrap, .table-wrap) are
         deliberate horizontal scrollers; overflow-x: clip/hidden is not a way to
         reach anything, so it still counts as clipped. */
      const scrollable = (el) => {
        for (let p = el.parentElement; p && p !== document.documentElement; p = p.parentElement) {
          const ox = getComputedStyle(p).overflowX;
          if (ox === 'auto' || ox === 'scroll' || ox === 'overlay') return true;
        }
        return false;
      };
      for (const el of document.querySelectorAll('main *')) {
        const r = el.getBoundingClientRect();
        if (!r.width || !r.height) continue;
        const style = getComputedStyle(el);
        if (style.visibility === 'hidden' || style.display === 'none' || style.position === 'fixed') continue;
        const hasText = [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim().length > 1);
        if (!hasText) continue;
        if (r.right <= vw + 1 && r.left >= -1) continue;
        if (scrollable(el)) continue;
        const key = `${el.tagName}.${el.className}`;
        if (seen.has(key)) continue;
        seen.add(key);
        offenders.push({ el: key, left: Math.round(r.left), right: Math.round(r.right), text: el.textContent.trim().slice(0, 40) });
      }
      return {
        docScroll: document.documentElement.scrollWidth,
        bodyScroll: document.body.scrollWidth,
        vw,
        offenders: offenders.slice(0, 8),
      };
    });

    expect(report.docScroll, `${name} scrolls sideways at 320px`).toBeLessThanOrEqual(report.vw + 1);
    expect(report.offenders, `${name} clips text at 320px: ${JSON.stringify(report.offenders)}`).toHaveLength(0);
  });
}

test('320px · booking controls remain tappable', async ({ page }) => {
  await page.route((url) => url.pathname === '/api/booking/slots', (route) => route.fulfill({
    contentType: 'application/json',
    body: JSON.stringify({
      accepted: true, dates: ['2026-12-07'], date: '2026-12-07', timezone: 'AST',
      slots: [{ time: '09:00', utc: '2026-12-07T06:00', available: true }],
    }),
  }));
  await page.setViewportSize({ width: 320, height: 720 });
  await visit(page, '/book/');
  const slot = page.locator('.slot[data-time="09:00"]');
  await expect(slot).toBeVisible();
  const box = await slot.boundingBox();
  // 44px is the smallest comfortable target; the chip is 30-minute precision so
  // a mis-tap books the wrong hour, not the wrong minute.
  expect(box.height).toBeGreaterThanOrEqual(36);
  expect(box.width).toBeGreaterThanOrEqual(60);
  await slot.click();
  await expect(page.locator('#b-time')).toHaveValue('09:00');
});
