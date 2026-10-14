// Export only curated test results; traces/cache remain ignored.
import fs from 'node:fs';
const raw=JSON.parse(fs.readFileSync('test-results/results.json'));const tests=[];
function walk(s){for(const spec of s.specs||[])for(const t of spec.tests)tests.push({title:spec.title,file:spec.file,status:t.status,results:t.results.map(r=>({status:r.status,duration:r.duration,attachments:(r.attachments||[]).filter(a=>a.contentType==='application/json'&&a.body).map(a=>({name:a.name,data:JSON.parse(Buffer.from(a.body,'base64').toString())}))}))});for(const sub of s.suites||[])walk(sub);}
walk(raw);
const dir='docs/completion-2026-10-14/evidence';fs.mkdirSync(dir,{recursive:true});
const out={sprint:'2026-10-14',branch:'arena/e48bf0e9-codeandcanvas-native',scope:'Local static server. External traffic aborted; APIs mocked. Browser identity and screenshot conditions in screenshots.json. Not real-device, production or provider acceptance.',stats:raw.stats,tests};
fs.writeFileSync(`${dir}/regression-results.json`,JSON.stringify(out,null,2)+'\n');
const metrics=tests.filter(t=>t.title.startsWith('home geometry')).map(t=>({test:t.title,...t.results[0].attachments.find(a=>a.name==='home-metrics')?.data}));
fs.writeFileSync(`${dir}/home-geometry.json`,JSON.stringify(metrics,null,2)+'\n');
console.log(JSON.stringify(raw.stats));
