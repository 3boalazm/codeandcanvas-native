import { expect } from '@playwright/test';
export async function isolate(page) {
  // Never contact production, message providers or payment services during QA.
  await page.context().route('**/*', route => {
    const host = new URL(route.request().url()).hostname;
    return ['localhost', '127.0.0.1'].includes(host) ? route.continue() : route.abort();
  });
  await page.addInitScript(() => {
    sessionStorage.setItem('cc-pre', '1');
    window.__drafts = [];
    window.open = (...args) => { window.__drafts.push(args); return null; };
  });
}
export async function visit(page, route = '/', lang = 'en') {
  await page.goto(`${route}${route.includes('?') ? '&' : '?'}lang=${lang}`);
  await page.waitForFunction(() => window.CC && document.body.classList.contains('is-ready'));
  await page.evaluate(() => document.fonts.ready);
  await expect(page.locator('html')).toHaveAttribute('lang', lang);
}
export async function configure(page, config = {}) {
  await page.route('**/assets/js/config.js', r => r.fulfill({
    contentType: 'application/javascript', body: `window.CC_CONFIG = Object.freeze(${JSON.stringify(config)});`,
  }));
}
export async function fillContact(page) {
  await page.locator('#c-first').fill('Test'); await page.locator('#c-last').fill('Person');
  await page.locator('#c-email').fill('qa@example.invalid');
  await page.locator('#c-inquiry').selectOption({ index: 1 });
  await page.locator('#c-msg').fill('Local automated acceptance test, not a real inquiry.');
}
export async function seedShortlist(page, values = [{ id: 'marketing-fundamentals', qty: 3 }]) {
  await page.addInitScript(values => localStorage.setItem('cc-cart', JSON.stringify(values)), values);
}
