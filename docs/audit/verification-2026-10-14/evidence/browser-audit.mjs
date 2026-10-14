import { chromium as pw } from 'playwright';
import chromium from '@sparticuz/chromium';
import AxeBuilder from '@axe-core/playwright';
import fs from 'node:fs';
const ROOT=process.cwd();
const out=ROOT+'/docs/audit/verification-2026-10-14/evidence';
const routes=JSON.parse(fs.readFileSync(ROOT+'/manus-routes.json')).routes.map(x=>x.path);
const major=['/','/services/','/technology-services/','/creative-services/','/healthcare/','/about/','/team/','/contact/','/pricing-faq/','/case-studies/','/books/','/checkout/'];
const axeRoutes=['/','/services/','/contact/','/pricing-faq/','/books/','/checkout/','/login/','/books/basics-of-visual-identity/read/'];
const browser=await pw.launch({executablePath:await chromium.executablePath(),args:chromium.args,headless:true});
const ctx=await browser.newContext({reducedMotion:'reduce'});
await ctx.route('**/*',r=>new URL(r.request().url()).hostname==='localhost'?r.continue():r.abort());
const results=[];
for(const [width,lang] of [[1440,'en'],[390,'ar'],[390,'en'],[1440,'ar']]) {
 const page=await ctx.newPage();await page.setViewportSize({width,height:900});
 const errors=[],requests=[];
 page.on('pageerror',e=>errors.push(e.message));
 page.on('response',r=>{if(r.status()>=400&&new URL(r.url()).hostname==='localhost')requests.push({url:r.url(),status:r.status()});});
 for(const path of (width===1440&&lang==='en'||width===390&&lang==='ar'?routes:major)) {
  errors.length=0;requests.length=0;
  const response=await page.goto('http://localhost:3000'+path+'?lang='+lang);
  await page.waitForTimeout(150);
  // Scroll actual document to trigger each reveal observer before inspecting all content.
  await page.evaluate(async()=>{const step=innerHeight;for(let y=0;y<document.body.scrollHeight;y+=step){scrollTo(0,y);await new Promise(r=>setTimeout(r,8));}scrollTo(0,0);});
  await page.waitForTimeout(100);
  const dom=await page.evaluate(()=>{
   const text=e=>(e?.innerText||'').trim().replace(/\s+/g,' ');
   const w=innerWidth;
   const excess=[...document.querySelectorAll('main *,.nav *')].filter(e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return r.width>0&&s.visibility!=='hidden'&&s.display!=='none'&&(r.left<-2||r.right>w+2)&&!e.closest('.subnav,.reader__thumbs,.table-wrap');}).slice(0,16).map(e=>({tag:e.tagName,cls:e.className,text:text(e).slice(0,70),x:Math.round(e.getBoundingClientRect().x),width:Math.round(e.getBoundingClientRect().width)}));
   const nav=document.querySelector('.nav__pill');
   return {title:document.title,lang:document.documentElement.lang,dir:document.documentElement.dir,width:document.documentElement.clientWidth,scrollWidth:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight,h1:[...document.querySelectorAll('h1')].map(text),panels:[...document.querySelectorAll('main > section')].map(e=>({id:e.id,heading:text(e.querySelector('h1,h2,h3')),y:Math.round(e.getBoundingClientRect().top+scrollY)})),excess,nav:nav?{width:nav.offsetWidth,scrollWidth:nav.scrollWidth}:null};
  });
  let axe;
  if(axeRoutes.includes(path)&&(width===1440&&lang==='en'||width===390&&lang==='ar')) {
   const r=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21a','wcag21aa']).analyze();
   axe={violations:r.violations.map(v=>({id:v.id,impact:v.impact,description:v.description,nodes:v.nodes.map(n=>({target:n.target,html:n.html,failureSummary:n.failureSummary}))})),incomplete:r.incomplete.map(x=>({id:x.id,count:x.nodes.length}))};
  }
  results.push({path,width,lang,status:response.status(),...dom,errors:[...errors],failedResponses:[...requests],axe});
  if(['/','/contact/','/creative-services/'].includes(path)&&(width===1440&&lang==='en'||width===390&&lang==='ar')) {
   await page.screenshot({path:out+'/'+(path==='/'?'home':path.replaceAll('/',''))+'-'+width+'-'+lang+'.png',fullPage:false});
  }
  console.log(width,lang,path,'errors',errors.length,'overflow',dom.scrollWidth>width,'axe',axe?.violations.map(x=>x.id).join(',')||'-');
  fs.writeFileSync(out+'/browser-results.json',JSON.stringify({browser:browser.version(),note:'External requests intentionally blocked. Google Arabic fonts unavailable. Reduced-motion enabled. Local dev server, not production.',results},null,2));
 }
 await page.close();
}
await browser.close();
