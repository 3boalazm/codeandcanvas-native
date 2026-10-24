import { test, expect } from '@playwright/test';
for (const path of ['/', '/ar/']) {
 for (const width of [390, 1024, 1440, 1920, 2560]) {
  test(`${path} balanced canvas at ${width}px`, async ({ page }) => {
   await page.setViewportSize({ width, height: 1080 });
   await page.goto(path);
   const geometry = await page.evaluate(() => {
    const hero = document.querySelector('.hero.container').getBoundingClientRect();
    const nav = document.querySelector('.nav__pill').getBoundingClientRect();
    return { hero: { x: hero.x, width: hero.width }, nav: { x: nav.x, width: nav.width }, scroll: document.documentElement.scrollWidth };
   });
   expect(geometry.scroll).toBeLessThanOrEqual(width + 1);
   expect(Math.abs(geometry.hero.x - geometry.nav.x)).toBeLessThan(1);
   expect(Math.abs(geometry.hero.width - geometry.nav.width)).toBeLessThan(1);
   if (width >= 1440 && width <= 1920) expect(geometry.hero.width / width).toBeGreaterThan(.90);
   if (width >= 2560) expect(geometry.hero.width).toBeLessThanOrEqual(1760);
  });
 }
}
