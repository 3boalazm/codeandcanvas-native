import { test, expect } from '@playwright/test';
import { readFileSync } from 'node:fs';
import { isolate, visit } from './helpers.mjs';
const routes = JSON.parse(readFileSync(new URL('../manus-routes.json',import.meta.url))).routes.map(r=>r.path);
test.beforeEach(async ({page})=>isolate(page));
for(const route of routes) for(const lang of ['en','ar']) for(const width of [390,1440]) {
  test(`route ${route} ${lang} ${width}`,async({page},info)=>{
    await page.setViewportSize({width,height:900});
    const errors=[],badAssets=[];
    page.on('pageerror',e=>errors.push(e.message));
    page.on('response',r=>{if(r.status()>=400&&r.url().includes('/assets/'))badAssets.push(r.url());});
    await visit(page,route,lang);
    await expect(page.locator('h1')).toHaveCount(1);
    const meta=await page.evaluate(()=>{
      const ids=[...document.querySelectorAll('[id]')].map(e=>e.id);
      const clipped=[...document.querySelectorAll('main .btn, main button[type=submit]')].filter(e=>{
        const r=e.getBoundingClientRect();return r.width&&r.height&&!e.closest('.tabs,.reader__thumbs')&&(r.left < -1 || r.right > innerWidth+1);
      }).map(e=>e.textContent.trim());
      const graphs=[...document.querySelectorAll('script[type="application/ld+json"]')].map(e=>JSON.parse(e.textContent));
      return {clipped, duplicateIDs:ids.filter((id,i)=>ids.indexOf(id)!==i),graphs:graphs.length,docWidth:document.documentElement.scrollWidth, viewport:innerWidth, literalTags:/<\/?(?:strong|b|em|i|span)(?:>|\s)/.test(document.querySelector('main')?.innerText||'')};
    });
    expect(errors).toEqual([]);expect(badAssets).toEqual([]);expect(meta.duplicateIDs).toEqual([]);expect(meta.graphs).toBeGreaterThan(0);expect(meta.literalTags).toBe(false);expect(meta.clipped).toEqual([]);expect(meta.docWidth).toBeLessThanOrEqual(width+1);
    await info.attach('route-check',{body:JSON.stringify(meta),contentType:'application/json'});
  });
}
for(const lang of ['en','ar'])for(const width of [320,360,390,480,768,1024,1440,1920])test(`home geometry ${lang} ${width}`,async({page},info)=>{
  await page.setViewportSize({width,height:900});await visit(page,'/',lang);
  const metrics=await page.evaluate(()=>({
    height:document.body.scrollHeight,workTop:document.querySelector('#work').getBoundingClientRect().top,
    cta:[...document.querySelectorAll('.hero__ctas .btn')].map(e=>e.getBoundingClientRect().toJSON()),
    fonts:[...performance.getEntriesByType('resource')].filter(e=>e.initiatorType==='css'&&/woff/.test(e.name)).map(e=>new URL(e.name).pathname),
  }));
  for(const box of metrics.cta){expect(box.left).toBeGreaterThanOrEqual(0);expect(box.right).toBeLessThanOrEqual(width);}
  if(width>=1024)expect(metrics.cta[0].bottom).toBeLessThan(900);
  expect(metrics.fonts.length).toBeGreaterThan(0);
  await info.attach('home-metrics',{body:JSON.stringify(metrics),contentType:'application/json'});
});
