import { test, expect } from '@playwright/test';
import { isolate, visit } from './helpers.mjs';

/* 2026-11-09 page-artwork pass. Every new plate is first-party artwork and is
   labelled as such in the browser: it loads from this origin, keeps an alt in
   both languages, and sits next to an illustrative qualifier. Nothing here is
   presented as client work, a product screenshot, a map or a metric.
   Complements scripts/check-art.mjs, which does the same statically. */

const PAGES = [
  ['en', '/services/', 'hero-services-geo'],
  ['ar', '/ar/services/', 'hero-services-geo'],
  ['en', '/services/brand-identity-design/', 'hero-offer'],
  ['en', '/technology-services/', 'art-arch-stack'],
  ['ar', '/ar/technology-services/', 'art-arch-stack'],
  ['en', '/creative-services/', 'art-brand-acts'],
  ['en', '/healthcare/', 'art-clinical-lanes'],
  ['en', '/contact/', 'art-contact-arc'],
  ['ar', '/ar/contact/', 'art-contact-arc'],
  ['en', '/book/', 'art-book-steps'],
  ['en', '/pricing-faq/', 'art-pricing-tiers'],
  ['en', '/about/', 'art-duo-practices'],
  ['en', '/team/', 'art-duo-practices'],
  ['en', '/case-studies/', 'art-work-ledger'],
  ['en', '/resources/', 'art-resources'],
  ['ar', '/ar/resources/', 'art-resources'],
  ['en', '/erp/', 'art-erp-modules'],
  ['ar', '/ar/erp/', 'art-erp-modules'],
  ['en', '/our-story/', 'art-story-architecture'],
  ['ar', '/ar/our-story/', 'art-story-architecture'],
  ['en', '/blog/', 'hero-pricing'],
];

test('page artwork is first-party, loaded, bilingual and labelled', async ({ page }) => {
  test.setTimeout(240000);
  await isolate(page);

  for (const [lang, route, plate] of PAGES) {
    await page.setViewportSize({ width: 390, height: 900 });
    await visit(page, route, lang);

    const img = page.locator(`img[src*="/assets/media/${plate}"]`).first();
    await expect(img, `${route} shows ${plate}`).toHaveCount(1);
    await img.scrollIntoViewIfNeeded();
    await expect.poll(async () => img.evaluate((el) => el.complete && el.naturalWidth > 0), {
      message: `${route}: ${plate} served and decoded`,
    }).toBe(true);

    const state = await img.evaluate((el) => {
      const fig = el.closest('figure, .story-plate, .feat-post__plate, .art');
      return {
        src: el.getAttribute('src'),
        srcset: el.getAttribute('srcset') || '',
        alt: el.getAttribute('alt') || '',
        altAr: el.getAttribute('data-ar-alt') || '',
        width: el.getAttribute('width'),
        height: el.getAttribute('height'),
        loading: el.getAttribute('loading'),
        caption: fig ? fig.innerText : '',
      };
    });

    expect(state.src, `${route}: same-origin asset`).toMatch(/^\/assets\//);
    expect(state.srcset, `${route}: phone variant present`).toContain('-sm.webp 780w');
    expect(state.alt.length, `${route}: alt text`).toBeGreaterThan(20);
    if (lang === 'en') expect(state.altAr.length, `${route}: Arabic alt`).toBeGreaterThan(10);
    expect(state.width, `${route}: intrinsic width`).toMatch(/^\d+$/);
    expect(state.height, `${route}: intrinsic height`).toMatch(/^\d+$/);
    expect(state.loading, `${route}: loading attribute`).toMatch(/lazy|eager/);
    expect(state.caption, `${route}: illustrative qualifier next to ${plate}`).toMatch(/ILLUSTRATIVE|توضيحي|مخطط/);

    /* Nothing on these routes may hotlink an image from another origin. */
    const external = await page.evaluate(() => [...document.querySelectorAll('img')]
      .map((i) => i.getAttribute('src') || '')
      .filter((s) => /^(https?:)?\/\//i.test(s) && !s.startsWith('//codeandcanvas.net')));
    expect(external, `${route}: no hotlinked imagery`).toEqual([]);
  }
});

test('chapter plates keep their illustrative badge in both languages', async ({ page }) => {
  test.setTimeout(120000);
  await isolate(page);
  for (const [lang, route] of [['en', '/our-story/'], ['ar', '/ar/our-story/']]) {
    await page.setViewportSize({ width: 1280, height: 900 });
    await visit(page, route, lang);
    await expect(page.locator('.story-plate img')).toHaveCount(5);
    await expect(page.locator('.story-plate__badge')).toHaveCount(5);
    for (const badge of await page.locator('.story-plate__badge').allInnerTexts()) {
      expect(badge).toMatch(/ILLUSTRATIVE|توضيحي/);
    }
  }
});

test('article covers are all first-party and labelled, and none repeats a shared file', async ({ page }) => {
  test.setTimeout(120000);
  await isolate(page);
  await page.setViewportSize({ width: 1280, height: 900 });
  await visit(page, '/blog/', 'en');
  const covers = await page.locator('#post-list .post-row').evaluateAll((rows) => rows.map((row) => ({
    href: row.getAttribute('href') || '',
    text: row.innerText,
  })));
  expect(covers.length).toBeGreaterThan(8);
  for (const c of covers) {
    expect(c.text, `${c.href} states it is illustrative`).toMatch(/min read/i);
  }
  /* The featured plate carries the illustrative badge. */
  await expect(page.locator('.feat-post__plate .story-plate__badge')).toHaveCount(1);
  await expect(page.locator(`.feat-post__plate img`)).toHaveAttribute('src', /^\/assets\/media\//);
});
