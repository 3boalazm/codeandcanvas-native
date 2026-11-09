import { test, expect } from '@playwright/test';
import { existsSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

/* The rest of the suite blocks service workers so its 676 assertions stay
   deterministic. This file explicitly opts back in and exercises the app shell. */
test.use({ serviceWorkers: 'allow' });

const ROOT = fileURLToPath(new URL('../', import.meta.url));

test('installable manifest, icons and home-screen chrome on EN + AR', async ({ page, request }) => {
  for (const path of ['/', '/ar/']) {
    await page.goto(path);
    await expect(page.locator('link[rel=manifest]')).toHaveAttribute('href', '/manifest.webmanifest');
    await expect(page.locator('meta[name="mobile-web-app-capable"]')).toHaveAttribute('content', 'yes');
    await expect(page.locator('meta[name="apple-mobile-web-app-capable"]')).toHaveAttribute('content', 'yes');
    await expect(page.locator('link[rel="apple-touch-icon"]')).toHaveAttribute('href', '/assets/brand/app/apple-touch-icon.png');
  }
  await page.goto('/');
  expect(await page.locator('meta[name="apple-mobile-web-app-title"]').getAttribute('content')).toBe('Code & Canvas');
  await page.goto('/ar/');
  expect(await page.locator('meta[name="apple-mobile-web-app-title"]').getAttribute('content')).toBe('كود آند كانفاس');

  const res = await request.get('/manifest.webmanifest');
  expect(res.status()).toBe(200);
  expect(res.headers()['content-type']).toContain('manifest+json');
  const m = await res.json();
  expect(m.display).toBe('standalone');
  expect(m.start_url).toBe('/');
  expect(m.scope).toBe('/');
  expect(m.icons.length).toBeGreaterThanOrEqual(4);
  expect(m.icons.some((i) => i.purpose === 'maskable')).toBe(true);
  for (const icon of m.icons) {
    expect(existsSync(join(ROOT, icon.src.replace(/^\//, ''))), `${icon.src} exists`).toBe(true);
    expect((await request.get(icon.src)).status(), `${icon.src} is served`).toBe(200);
  }
  expect((await request.get('/offline.html')).status()).toBe(200);
  const sw = await request.get('/sw.js');
  expect(sw.status()).toBe(200);
  expect(sw.headers()['content-type']).toContain('javascript');
});

test('install affordance only appears when the browser offers a prompt', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('#installApp')).toBeHidden();
  const state = await page.evaluate(async () => {
    let prompted = false;
    const ev = new Event('beforeinstallprompt', { cancelable: true });
    ev.prompt = async () => { prompted = true; return { outcome: 'accepted' }; };
    ev.userChoice = Promise.resolve({ outcome: 'accepted' });
    window.dispatchEvent(ev);
    await new Promise((r) => setTimeout(r, 20));
    const btn = document.querySelector('#installApp');
    const visible = !btn.hidden;
    btn.click();
    await new Promise((r) => setTimeout(r, 50));
    return { visible, prompted, hiddenAfter: btn.hidden };
  });
  expect(state.visible).toBe(true);
  expect(state.prompted).toBe(true);
  expect(state.hiddenAfter).toBe(true);
});

test('an unvisited page falls back to a fully self-contained bilingual offline screen', async ({ page, context }) => {
  await page.goto('/');
  await page.evaluate(() => navigator.serviceWorker.ready);
  const subresources = [];
  page.on('request', (r) => { if (!r.isNavigationRequest()) subresources.push(r.url()); });
  await context.setOffline(true);
  try {
    await page.goto('/never-visited-pwa-page/', { waitUntil: 'domcontentloaded', timeout: 15000 });
    await expect(page.locator('h1')).toContainText("You're offline");
    expect(await page.title()).toContain('Offline');
    expect(await page.locator('main > svg').count()).toBe(1);
    // EN + AR copy in the same standalone document, with no external requests.
    await expect(page.locator('[lang=ar] h2')).toContainText('أنت غير متصل');
    expect(subresources).toEqual([]);
  } finally {
    await context.setOffline(false);
  }
});

test('app shell installs and reopens a visited page while offline', async ({ page, context }) => {
  await page.goto('/');
  await page.waitForFunction(() => window.CC && document.body.classList.contains('is-ready'));
  const reg = await page.evaluate(async () => {
    await navigator.serviceWorker.ready;
    const r = await navigator.serviceWorker.getRegistration();
    return { active: !!r?.active, scope: r?.scope || '' };
  });
  expect(reg.active).toBe(true);
  expect(reg.scope.endsWith(':3000/')).toBe(true);

  // This navigation is controlled by the worker and caches its HTML.
  await page.reload();
  await page.waitForFunction(() => window.CC && document.body.classList.contains('is-ready'));
  await context.setOffline(true);
  try {
    await page.reload({ waitUntil: 'domcontentloaded', timeout: 15000 });
    await expect(page.locator('h1')).toBeVisible();
    expect(await page.title()).toContain('Code & Canvas');
  } finally {
    await context.setOffline(false);
  }
});
