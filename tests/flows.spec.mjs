import { test, expect } from '@playwright/test';
import { isolate, visit, configure, fillContact, seedShortlist } from './helpers.mjs';
test.beforeEach(async ({ page }) => isolate(page));

test('slash redirect preserves service and language query', async ({ request }) => {
  const response = await request.get('/contact?inquiry=HC-03&lang=ar', { maxRedirects: 0 });
  expect(response.status()).toBe(301);
  expect(response.headers().location).toBe('/contact/?inquiry=HC-03&lang=ar');
});

test('all service CTA contexts arrive at the contact selector', async ({ page }) => {
  test.setTimeout(120000);
  const codes = ['AB-01','AB-02','AB-03','AB-04','AB-05','AB-06','MA-01','MA-02','MA-03','MA-04','MA-05','MA-06','MA-07','MA-08','MA-09','MA-10','HC-01','HC-02','HC-03','HC-04','HC-05','CC-01','CC-02'];
  for (const route of ['/technology-services/', '/creative-services/', '/healthcare/', '/services/']) {
    await visit(page, route);
    const links = await page.locator('main a[data-track="service-inquiry"]').evaluateAll(els => els.map(e => ({code:e.dataset.trackService, href:e.getAttribute('href')})));
    expect(links.length).toBeGreaterThan(0);
    for(const link of links) expect(link.href).toContain(`inquiry=${link.code}`);
  }
  for (const code of codes) {
    await visit(page, `/contact/?inquiry=${code}`, 'ar');
    expect(await page.locator('#c-inquiry').inputValue()).toMatch(new RegExp(`^${code} `));
  }
  expect(await page.locator('#c-inquiry optgroup').first().getAttribute('label')).toMatch(/[\u0600-\u06ff]/);
});

test('registration consent and password length are validated without fake auth', async ({ page }) => {
  await visit(page, '/register/');
  await page.locator('[name=name]').fill('Test Person');
  await page.locator('[name=email]').fill('qa@example.invalid');
  await page.locator('[name=password]').fill('test-password-123');
  await page.locator('[name=password2]').fill('test-password-123');
  await page.locator('form button[type=submit]').click();
  await expect(page.locator('[name=consent]')).toHaveAttribute('aria-invalid','true');
  await expect(page.locator('[name=consent]')).toBeFocused();
  await page.locator('[name=consent]').check();
  await page.locator('[name=password]').fill('x'); await page.locator('[name=password2]').fill('x');
  await page.locator('form button[type=submit]').click();
  await expect(page.locator('[name=password]')).toHaveAttribute('aria-invalid','true');
  await page.locator('[name=password]').fill('test-password-123'); await page.locator('[name=password2]').fill('test-password-123');
  await page.locator('form button[type=submit]').click();
  await expect(page.locator('.form__status')).toContainText('not available');
  expect(await page.evaluate(() => localStorage.getItem('cc-library'))).toBeNull();
  expect(page.url()).toContain('/register/');
});

test('availability inquiry requires consent and never creates an entitlement', async ({ page }) => {
  await seedShortlist(page);
  await visit(page,'/checkout/');
  await page.locator('[name=name]').fill('Test Person'); await page.locator('[name=email]').fill('qa@example.invalid');
  await page.locator('[data-pay]').click();
  await expect(page.locator('[name=consent]')).toHaveAttribute('aria-invalid','true');
  expect(await page.evaluate(() => window.__drafts.length)).toBe(0);
  await page.locator('[name=consent]').check(); await page.locator('[data-pay]').click();
  await expect(page.locator('.form__status')).toContainText('not been sent');
  expect(await page.evaluate(() => window.__drafts.length)).toBe(1);
  expect(await page.evaluate(() => localStorage.getItem('cc-library'))).toBeNull();
  expect(page.url()).toContain('/checkout/');
});

test('shortlist ignores forged prices, titles, duplicates and unknown IDs; counts update', async ({ page }) => {
  await seedShortlist(page,[{id:'marketing-fundamentals',qty:4,price:1,title:'<img src=x onerror=alert(1)>'},{id:'marketing-fundamentals'}, {id:'fake'}]);
  await visit(page,'/cart/');
  await expect(page.locator('.cart-table tbody tr')).toHaveCount(1);
  expect(await page.locator('.cart-table').textContent()).not.toContain('onerror');
  expect(await page.locator('.cart-table tbody').textContent()).toContain('249 SAR');
  await visit(page,'/account/'); await expect(page.locator('[data-library-count]')).toHaveText('1');
  await page.evaluate(() => { localStorage.setItem('cc-cart','[]'); dispatchEvent(new StorageEvent('storage',{key:'cc-cart'})); });
  await expect(page.locator('[data-library-count]')).toHaveText('0');
  await expect(page.locator('[data-library-empty]')).toBeVisible();
});

for (const lang of ['en','ar']) test(`reader buttons, RTL keyboard, notes and preview gate — ${lang}`, async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('cc-library',JSON.stringify([{id:'marketing-fundamentals'}])));
  const missing=[]; page.on('response',r=>{if(r.status()===404)missing.push(r.url());});
  await visit(page,'/books/marketing-fundamentals/read/',lang);
  await expect(page.locator('[data-counter]')).toHaveText(/^1 \//);
  await expect(page.locator('[data-prev]')).toBeDisabled();
  await page.locator('[data-next]').click(); await expect(page.locator('[data-counter]')).toHaveText(/^2 \//);
  await page.locator('[data-prev]').click(); await expect(page.locator('[data-counter]')).toHaveText(/^1 \//);
  await page.locator('[data-next]').focus(); await page.keyboard.press('ArrowLeft');
  await expect(page.locator('[data-counter]')).toHaveText(/^2 \//);
  await page.keyboard.press('End'); await expect(page.locator('[data-next]')).toBeDisabled(); await expect(page.locator('[data-gate]')).toBeVisible();
  await page.keyboard.press('Home'); await page.locator('[data-notes-toggle]').first().click();
  await page.locator('[data-notes-text]').fill('Private note'); await page.locator('[data-notes-text]').press('ArrowLeft');
  await expect(page.locator('[data-counter]')).toHaveText(/^1 \//); expect(missing).toEqual([]);
});

test('manual contact handoff is not lead success and preserves input', async ({ page }) => {
  await visit(page,'/contact/'); await fillContact(page); await page.locator('form button[type=submit]').click();
  await expect(page.locator('.form__status')).toContainText('not been sent');
  await expect(page.locator('#c-email')).toHaveValue('qa@example.invalid');
  const events=await page.evaluate(()=>window.dataLayer.map(e=>e.name));
  expect(events).toContain('form-handoff'); expect(events).not.toContain('form-success');
});

for (const mode of ['accepted','rejected','http-error','invalid-json','timeout','network-error']) test(`form API contract — ${mode}`, async ({ page }) => {
  await configure(page,{contactEndpoint:'/api/contact',requestTimeoutMs:250});
  let submitted;
  await page.route('**/api/contact',async r=>{
    submitted=r.request().postDataJSON();
    if(mode==='timeout') { await new Promise(resolve=>setTimeout(resolve,650)); return r.abort().catch(()=>{}); }
    if(mode==='network-error') return r.abort();
    return r.fulfill({status:mode==='http-error'?500:200,contentType:'application/json',body:mode==='invalid-json'?'no':JSON.stringify({accepted:mode==='accepted'})});
  });
  await visit(page,'/contact/'); await fillContact(page); await page.locator('form button[type=submit]').click();
  await expect(page.locator('.form__status')).toContainText(mode==='accepted'?'was received':'could not confirm');
  expect(submitted.email).toBe('qa@example.invalid'); expect(submitted.kind).toBe('contact');
  await expect(page.locator('form button[type=submit]')).toBeEnabled();
  await expect(page.locator('#c-email')).toHaveValue(mode==='accepted'?'':'qa@example.invalid');
  expect(await page.evaluate(()=>window.dataLayer.some(e=>e.name==='form-success'))).toBe(mode==='accepted');
});

test('invalid external endpoint is never posted to; malformed scheduler fails safely', async ({ page }) => {
  await configure(page,{contactEndpoint:'https://example.invalid/collect',bookingUrl:'https://'});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await visit(page,'/contact/'); await fillContact(page); await page.locator('form button[type=submit]').click();
  await expect(page.locator('.form__status')).toContainText('could not confirm'); expect(errors).toEqual([]);
});

test('configured scheduler carries service context', async ({ page }) => {
  await configure(page,{bookingUrl:'https://example.invalid/book'});
  await visit(page,'/contact/?inquiry=HC-03');
  await expect(page.locator('[data-book]')).toHaveAttribute('href','https://example.invalid/book?service=HC-03');
});

test('analytics requires consent, excludes PII, bounds queue and allows withdrawal', async ({ page }) => {
  await configure(page,{analyticsEndpoint:'/api/events'});
  const sent=[];await page.route('**/api/events',r=>{sent.push(r.request().postDataJSON());return r.fulfill({status:204});});
  await visit(page,'/?email=private@example.invalid');
  await page.evaluate(()=>CC.track('test',{email:'private@example.invalid',message:'Private message',service:'HC-03'}));
  expect(sent).toHaveLength(0);
  await page.locator('[data-choice=denied]').click();
  await page.evaluate(()=>CC.track('test')); expect(sent).toHaveLength(0);
  await page.getByRole('button',{name:'Measurement settings'}).click(); await page.locator('[data-choice=granted]').click();
  await expect.poll(()=>sent.length).toBe(1); // landing view after consent
  await page.evaluate(()=>CC.track('test',{email:'private@example.invalid',service:'HC-03',from:'test'}));
  await expect.poll(()=>sent.length).toBe(2); expect(JSON.stringify(sent)).not.toContain('private'); expect(sent[0].path).toBe('/');
  await page.getByRole('button',{name:'Measurement settings'}).click();await page.locator('[data-choice=denied]').click();
  await page.evaluate(()=>{for(let i=0;i<150;i++)CC.track('test');}); expect(sent).toHaveLength(2);
  expect(await page.evaluate(()=>window.dataLayer.length)).toBe(100);
});

for(const pref of ['doNotTrack','globalPrivacyControl']) test(`privacy signal suppresses analytics — ${pref}`,async({page})=>{
  await configure(page,{analyticsEndpoint:'/api/events'});
  await page.addInitScript(pref=>{localStorage.setItem('cc-analytics-consent','granted');Object.defineProperty(navigator,pref,{get:()=>pref==='doNotTrack'?'1':true});},pref);
  let sent=0;await page.route('**/api/events',r=>{sent++;return r.fulfill({status:204});});
  await visit(page);await page.evaluate(()=>CC.track('test'));expect(sent).toBe(0);await expect(page.locator('.consent-bar')).toBeHidden();
});

test('Arabic markup, mobile menu, tabs, FAQ and book filters',async({page})=>{
  for(const route of ['/about/','/our-story/']){await visit(page,route,'ar');expect(await page.locator('main').innerText()).not.toMatch(/<\/?(?:b|i|em|strong|span|a)(?:>|\s)/);}
  await page.setViewportSize({width:390,height:844});await visit(page,'/pricing-faq/','ar');
  await page.locator('#burger').click();await expect(page.locator('#burger')).toHaveAttribute('aria-expanded','true');await page.keyboard.press('Escape');await expect(page.locator('#burger')).toHaveAttribute('aria-expanded','false');
  await page.locator('#langBtn').click();await expect(page.locator('html')).toHaveAttribute('lang','en');
  const tab=page.locator('[data-tabs] .tab').first();await tab.focus();await page.keyboard.press('ArrowRight');
  await expect(page.locator('[data-tabs] .tab').nth(1)).toHaveAttribute('aria-selected','true');
  const faq=page.locator('.faq__q').nth(1);await faq.click();await expect(faq).toHaveAttribute('aria-expanded','true');
  await visit(page,'/books/');await page.locator('[data-filter=technology]').click();await expect(page.locator('#book-list .book:visible')).toHaveCount(1);
});

test('malformed and blocked local storage fail safely',async({page})=>{
  await page.addInitScript(()=>localStorage.setItem('cc-cart','not-json'));
  await visit(page,'/cart/');await expect(page.locator('[data-cart-empty]')).toBeVisible();
  await page.addInitScript(()=>{Object.defineProperty(window,'localStorage',{get(){throw new Error('Storage blocked');}});});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await visit(page,'/books/marketing-fundamentals/');await page.locator('[data-add]').first().click();
  await expect(page.locator('#toast')).toContainText('could not save');expect(errors).toEqual([]);
});

test('one form request at a time; newsletter and career use their own endpoints',async({page})=>{
  await configure(page,{contactEndpoint:'/api/contact',newsletterEndpoint:'/api/newsletter',careerEndpoint:'/api/career'});
  let count=0;const kinds=[];
  await page.route('**/api/*',async r=>{count++;kinds.push(r.request().postDataJSON().kind);await new Promise(resolve=>setTimeout(resolve,200));return r.fulfill({contentType:'application/json',body:'{"accepted":true}'});});
  await visit(page,'/contact/');await fillContact(page);
  await page.locator('form').evaluate(f=>{f.requestSubmit();f.requestSubmit();});
  await expect(page.locator('.form__status')).toContainText('was received');expect(count).toBe(1);
  for(const [route,kind] of [['/blog/','newsletter'],['/team/','career']]){
    await visit(page,route);await page.locator(`form[data-integration=${kind}]`).evaluate(f=>CC.submitContact(f,{email:'qa@example.invalid'}));
    await expect(page.locator('form .form__status')).toContainText('was received');
  }
  expect(kinds).toEqual(['contact','newsletter','career']);
});

test('index policy and pricing schema match public capability',async({page,request})=>{
  const xml=await (await request.get('/sitemap.xml')).text();
  expect(xml).not.toMatch(/\/(account|checkout|cart|login|register|thank-you)\//);expect(xml).not.toContain('/read/');
  for(const route of ['/login/','/checkout/','/books/marketing-fundamentals/read/']){
    await visit(page,route);await expect(page.locator('meta[name=robots]')).toHaveAttribute('content','noindex, follow');
  }
  await visit(page,'/pricing-faq/');const graph=await page.locator('script[type="application/ld+json"]').evaluateAll(els=>els.flatMap(e=>JSON.parse(e.textContent)['@graph']||[JSON.parse(e.textContent)]));
  expect(graph.find(n=>n['@type']==='FAQPage').mainEntity.length).toBe(await page.locator('.faq__q').count());
  expect(graph.find(n=>n['@type']==='OfferCatalog').itemListElement).toHaveLength(23);
  await visit(page,'/books/marketing-fundamentals/');expect(await page.locator('script[type="application/ld+json"]').allTextContents()).not.toEqual(expect.arrayContaining([expect.stringContaining('InStock')]));
});

test('development preview does not expose repository internals',async({request})=>{
  for(const path of ['/.git/config','/node_modules/@playwright/test/package.json','/scripts/gen-pages.py','/docs/INTEGRATIONS.md'])expect((await request.get(path)).status()).toBe(403);
});

test('no-JavaScript fallback keeps content visible and prevents native form submission',async({browser})=>{
  const context=await browser.newContext({javaScriptEnabled:false});
  const page=await context.newPage();await isolate(page);await page.goto('http://127.0.0.1:3000/contact/');
  await expect(page.locator('h1')).toBeVisible();await expect(page.locator('form')).toBeHidden();
  await expect(page.getByRole('link',{name:'Email us instead'})).toBeVisible();await context.close();
});

test('reader mobile notes open, persist and close with Escape',async({page})=>{
  await page.setViewportSize({width:390,height:844});await visit(page,'/books/basics-of-visual-identity/read/','ar');
  await page.locator('[data-notes-toggle]').first().click();await expect(page.locator('[data-notes]')).toBeVisible();
  await expect(page.locator('[data-notes-text]')).toBeFocused();await page.locator('[data-notes-text]').fill('ملاحظة اختبار محلية');
  await page.keyboard.press('Escape');await expect(page.locator('[data-notes]')).toBeHidden();await expect(page.locator('[data-notes-toggle]').first()).toBeFocused();
  await page.reload();await page.locator('[data-notes-toggle]').first().click();await expect(page.locator('[data-notes-text]')).toHaveValue('ملاحظة اختبار محلية');
});
