import { test, expect } from '@playwright/test';
import { isolate, visit } from './helpers.mjs';

/* The header is a dark capsule in both themes. In light mode a stray rule painted
   a near-white sheet behind the desktop link row, so the links rendered light grey
   on off-white (2026-11-10). These tests measure the rendered result instead of
   trusting the cascade: the nav must stay dark, the links must have real contrast
   against what is actually behind them, and the mobile dropdown must be the one
   place that is a light sheet. */

const ROUTES = ['/', '/services/', '/work/', '/pricing-faq/', '/blog/', '/ar/'];

async function navReport(page) {
  return page.evaluate(() => {
    const links = document.querySelector('.nav__links');
    const link = links?.querySelector('a');
    const pill = document.querySelector('.nav__pill');
    const parse = (c) => (c.match(/[\d.]+/g) || []).map(Number);
    const lum = ([r, g, b]) => {
      const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; };
      return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
    };
    const ratio = (a, b) => {
      const [l1, l2] = [lum(a), lum(b)].sort((x, y) => y - x);
      return (l1 + 0.05) / (l2 + 0.05);
    };
    const linkColor = parse(getComputedStyle(link).color).slice(0, 3);
    const rowBg = parse(getComputedStyle(links).backgroundColor);
    return {
      rowBackgroundAlpha: rowBg.length === 4 ? rowBg[3] : 1,
      rowBackground: rowBg,
      linkColor,
      // The capsule is the surface behind the link row; read its painted colour.
      pillBackground: getComputedStyle(pill).backgroundImage,
      contrastAgainstPill: ratio(linkColor, [10, 9, 36]),
      pillIsDark: /rgba?\(\s*(?:[0-9]|1[0-9]|2[0-9]|3[0-9])\s*,/.test(getComputedStyle(pill).backgroundImage),
    };
  });
}

for (const route of ROUTES) {
  test(`light-mode nav keeps the dark capsule · ${route}`, async ({ page }) => {
    await isolate(page);
    await page.addInitScript(() => localStorage.setItem('cc-theme', 'light'));
    await page.setViewportSize({ width: 1440, height: 900 });
    await visit(page, route, route.startsWith('/ar/') ? 'ar' : 'en');
    await expect(page.locator('html')).toHaveAttribute('data-theme', 'light');

    const r = await navReport(page);
    // No sheet behind the desktop link row in light mode.
    expect(r.rowBackgroundAlpha, `${route}: .nav__links paints a background in light mode`).toBeLessThan(0.02);
    // Links must be light text on the dark capsule, not dark-on-white.
    expect(r.linkColor[0] + r.linkColor[1] + r.linkColor[2], `${route}: nav links are too dark for the dark capsule`).toBeGreaterThan(300);
    expect(r.contrastAgainstPill, `${route}: nav link contrast`).toBeGreaterThanOrEqual(4.5);
    expect(r.pillIsDark, `${route}: the nav capsule is not dark in light mode`).toBeTruthy();
  });
}

test('light-mode mobile dropdown is a readable light sheet', async ({ page }) => {
  await isolate(page);
  await page.addInitScript(() => localStorage.setItem('cc-theme', 'light'));
  await page.setViewportSize({ width: 390, height: 844 });
  await visit(page, '/');
  await page.locator('#burger').click();
  await expect(page.locator('#navLinks')).toHaveClass(/is-open/);
  const r = await page.evaluate(() => {
    const box = document.querySelector('.nav__links');
    const a = box.querySelector('a');
    const parse = (c) => (c.match(/[\d.]+/g) || []).map(Number);
    const lum = ([r, g, b]) => {
      const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; };
      return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
    };
    const bg = parse(getComputedStyle(box).backgroundColor).slice(0, 3);
    const fg = parse(getComputedStyle(a).color).slice(0, 3);
    const [l1, l2] = [lum(bg), lum(fg)].sort((x, y) => y - x);
    return { bg, fg, contrast: (l1 + 0.05) / (l2 + 0.05) };
  });
  // A light sheet, with dark text on it.
  expect(r.bg[0] + r.bg[1] + r.bg[2]).toBeGreaterThan(600);
  expect(r.fg[0] + r.fg[1] + r.fg[2]).toBeLessThan(300);
  expect(r.contrast).toBeGreaterThanOrEqual(4.5);
});
