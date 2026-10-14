// Curated viewport evidence, not a production/device performance benchmark.
import { chromium } from '@playwright/test';
import { mkdirSync, writeFileSync } from 'node:fs';
const dir='docs/completion-2026-10-14/evidence';mkdirSync(dir,{recursive:true});
const browser=await chromium.launch({headless:true,...(process.env.PW_EXECUTABLE_PATH?{executablePath:process.env.PW_EXECUTABLE_PATH,args:JSON.parse(process.env.PW_BROWSER_ARGS||'["--no-sandbox"]')}:{})});
const context=await browser.newContext({reducedMotion:'reduce'});
await context.route('**/*',r=>['localhost','127.0.0.1'].includes(new URL(r.request().url()).hostname)?r.continue():r.abort());
await context.addInitScript(()=>{sessionStorage.setItem('cc-pre','1');window.open=()=>null;});
const page=await context.newPage();const base=process.env.TEST_BASE_URL||'http://127.0.0.1:3000';const shots=[];
for(const shot of [
 ['home-en-desktop','/','en',1440,900,null],
 ['home-ar-mobile','/','ar',390,844,null],
 ['home-ar-320','/','ar',320,900,null],
 ['home-work-en','/','en',1440,900,'#work'],
 ['case-study-ar','/case-studies/','ar',390,844,'.case-visual'],
 ['contact-ar','/contact/?inquiry=HC-03','ar',390,844,'#message'],
 ['reader-ar','/books/marketing-fundamentals/read/','ar',1440,900,null],
]){
 const [name,route,lang,width,height,target]=shot;await page.setViewportSize({width,height});
 await page.goto(base+route+(route.includes('?')?'&':'?')+'lang='+lang);
 await page.waitForFunction(()=>window.CC&&document.body.classList.contains('is-ready'));await page.evaluate(()=>document.fonts.ready);
 if(target)await page.locator(target).first().evaluate(e=>scrollTo(0,e.getBoundingClientRect().top+scrollY-110));
 if(name==='reader-ar')await page.locator('[data-next]').click();
 await page.waitForTimeout(350);await page.screenshot({path:`${dir}/${name}.png`});
 shots.push({name,route,lang,width,height,scrollY:await page.evaluate(()=>scrollY)});
}
writeFileSync(`${dir}/screenshots.json`,JSON.stringify({browser:browser.version(),shots,note:'Viewport captures with real self-hosted fonts, reduced motion, external network aborted. No production or physical-device claim.'},null,2)+'\n');
await browser.close();console.log(`Saved ${shots.length} viewport captures.`);
