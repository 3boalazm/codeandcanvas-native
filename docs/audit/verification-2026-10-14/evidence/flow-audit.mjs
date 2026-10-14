import {chromium as pw} from 'playwright';import chromium from '@sparticuz/chromium';import fs from 'node:fs';
const browser=await pw.launch({executablePath:await chromium.executablePath(),args:chromium.args,headless:true});
const c=await browser.newContext({viewport:{width:1440,height:900},reducedMotion:'reduce'});
await c.route('**/*',r=>new URL(r.request().url()).hostname==='localhost'?r.continue():r.abort());
const p=await c.newPage();const out={errors:[],prefill:[],viewports:[],nav:[],checks:[]};p.on('pageerror',e=>out.errors.push(e.message));
const goto=async(path)=>{await p.goto('http://localhost:3000'+path);await p.waitForTimeout(220);};
for(const lang of ['en','ar'])for(const q of ['AB-01','HC-03','MA-09','custom','book-marketing-fundamentals']){
 await goto('/contact/?lang='+lang+'&inquiry='+q);out.prefill.push({q,lang,...await p.evaluate(()=>({value:document.querySelector('#c-inquiry').value,message:document.querySelector('#c-msg').value}))});
}
for(const lang of ['en','ar'])for(const width of [320,560,720,860,1024,1180,1440,1920]){
 await p.setViewportSize({width,height:900});await goto('/?lang='+lang);
 out.viewports.push({lang,width,...await p.evaluate(()=>{const a=document.querySelector('.hero__ctas .btn--primary');const n=document.querySelector('.nav__pill');return {cta:a.getBoundingClientRect().toJSON(),nav:n.getBoundingClientRect().toJSON(),navScrollWidth:n.scrollWidth,scrollWidth:document.documentElement.scrollWidth,heroHeight:document.querySelector('.hero').offsetHeight};})});
}
for(const lang of ['en','ar']){
 await p.setViewportSize({width:390,height:900});await goto('/services/?lang='+lang);
 await p.locator('#burger').click();out.checks.push({test:'mobile menu open '+lang,value:await p.locator('#burger').getAttribute('aria-expanded')});
 await p.keyboard.press('Escape');out.checks.push({test:'mobile menu escape '+lang,value:await p.locator('#burger').getAttribute('aria-expanded')});
 await p.locator('#langBtn').click();await p.waitForFunction(expected=>document.documentElement.lang===expected,lang==='en'?'ar':'en');out.checks.push({test:'language toggle from '+lang,value:await p.locator('html').getAttribute('lang')});
 await goto('/services/?lang='+lang);
 await p.locator('#combined').evaluate(el=>el.scrollIntoView());await p.waitForTimeout(450);
 out.nav.push({lang,...await p.evaluate(()=>{const n=document.querySelector('[data-spy]'),a=n.querySelector('.is-active');return {scrollX:n.scrollLeft,navRect:n.getBoundingClientRect().toJSON(),active:a?.textContent,activeRect:a?.getBoundingClientRect().toJSON(),targetY:document.querySelector('#combined').getBoundingClientRect().top};})});
}
await p.setViewportSize({width:1440,height:900});await goto('/technology-services/?lang=en');
out.serviceCTAs=await p.locator('.sdetail').evaluateAll(es=>es.map(e=>({id:e.id,links:[...e.querySelectorAll('a')].map(a=>({text:a.textContent.trim(),href:a.getAttribute('href'),track:a.dataset.track||null}))})));
await goto('/pricing-faq/?lang=en');await p.locator('.faq__q').nth(1).click();out.checks.push({test:'FAQ second open',value:await p.locator('.faq__q').nth(1).getAttribute('aria-expanded'),first:await p.locator('.faq__q').nth(0).getAttribute('aria-expanded')});
const tabs=p.locator('[data-tabs] .tab');await tabs.nth(1).click();out.checks.push({test:'Pricing second tab',value:await tabs.nth(1).getAttribute('aria-selected')});
await goto('/blog/?lang=en');const filters=p.locator('[data-filter]');await filters.nth(1).click();out.checks.push({test:'Blog filter',value:await filters.nth(1).getAttribute('aria-pressed'),visible:await p.locator('[data-category]:visible').count(),events:await p.evaluate(()=>window.dataLayer||[])});
await goto('/contact/?lang=en&inquiry=HC-03');
await p.evaluate(()=>{window.__opened=[];window.open=(url)=>{window.__opened.push(url);return null;};});
await p.locator('button[type=submit]').click();out.checks.push({test:'Empty contact validation',invalid:await p.locator('[aria-invalid=true]').count(),opened:await p.evaluate(()=>window.__opened.length)});
for(const [s,v]of [['#c-first','Audit'],['#c-last','Test'],['#c-email','audit@example.test'],['#c-msg','Local audit test only — do not send.']])await p.locator(s).fill(v);
await p.locator('button[type=submit]').click();out.checks.push({test:'Contact fallback (window.open intercepted; no message sent)',opened:await p.evaluate(()=>window.__opened.map(u=>new URL(u).hostname)),status:await p.locator('.form__status').innerText(),events:await p.evaluate(()=>window.dataLayer||[])});
await goto('/books/basics-of-visual-identity/?lang=en');await p.locator('[data-add]').first().click();out.checks.push({test:'Add book',cart:await p.evaluate(()=>JSON.parse(localStorage.getItem('cc-cart'))),events:await p.evaluate(()=>window.dataLayer||[])});
await goto('/cart/?lang=en');await p.locator('[data-inc]').click();out.checks.push({test:'Single-licence book quantity can increase',cart:await p.evaluate(()=>JSON.parse(localStorage.getItem('cc-cart')))});await p.locator('[data-dec]').click();
await goto('/checkout/?lang=en');for(const [s,v]of [['#f-name','Local Audit'],['#f-email','audit@example.test'],['#f-phone','0000000000']])await p.locator(s).fill(v);
out.checks.push({test:'Checkout consent before submit',checked:await p.locator('[name=consent]').isChecked(),browserValidity:await p.locator('form').evaluate(f=>f.checkValidity()),customValidity:await p.locator('form').evaluate(f=>CC.validateForm(f))});
await p.locator('[data-pay]').click();await p.waitForURL('**/thank-you/');out.checks.push({test:'Demo checkout without consent',url:p.url(),order:await p.evaluate(()=>JSON.parse(sessionStorage.getItem('cc-last-order'))),library:await p.evaluate(()=>JSON.parse(localStorage.getItem('cc-library'))),note:await p.locator('[data-demo-note]').innerText()});
await goto('/account/?lang=en');out.checks.push({test:'Account counts after one demo purchase',libraryCount:await p.locator('[data-library-count]').innerText(),links:await p.locator('[data-library] a').count()});
await p.locator('[data-acct-link=library]').click();out.checks.push({test:'Library panel',visible:await p.locator('[data-acct-panel=library]').isVisible()});
// Remove local ownership to test the public reader controls.
await p.evaluate(()=>localStorage.removeItem('cc-library'));
for(const lang of ['en','ar']){
 await goto('/books/basics-of-visual-identity/read/?lang='+lang);await p.waitForTimeout(200);
 const before=await p.locator('[data-counter]').innerText();await p.locator('[data-next]').click();const after=await p.locator('[data-counter]').innerText();
 out.checks.push({test:'Reader next '+lang,before,after,label:await p.locator('[data-next]').getAttribute('aria-label')});
 await p.evaluate(()=>localStorage.removeItem('cc-reader-basics-of-visual-identity'));
}
await goto('/contact?lang=ar&inquiry=HC-03');out.checks.push({test:'Slashless query redirect',url:p.url(),prefill:await p.locator('#c-inquiry').inputValue()});
fs.writeFileSync(process.cwd()+'/docs/audit/verification-2026-10-14/evidence/flow-results.json',JSON.stringify(out,null,2));console.log(JSON.stringify(out,null,2));await browser.close();
