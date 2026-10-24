/* Private-link intake; deliberately client-only. Never claims delivery or stores patient data. */
(() => {
'use strict';
const KEY = 'cc-clinic-review-amro-v1';
const groups = [
 {name:'انطباعك', title:'أولًا، إيه رأي حضرتك؟', desc:'افتح نسخة التطبيق وجرّب تحجز كأنك مريض. وبعدها احكي لنا ببساطة.', fields:[
 ['impression','التجربة كانت عاملة إزاي؟',['سهلة وواضحة','حلوة، مع شوية تعديلات','محتاجة تبسيط','لسه ما جربتش']],
 ['liked','إيه أكتر حاجة عجبتك؟','text','الشكل، طريقة الحجز، ترتيب المعلومات…'],
 ['change','وإيه اللي تحب نغيّره أو نضيفه؟','area','لو في خطوة مش واضحة، قول لنا اسم الشاشة أو وصفها.']]},
 {name:'الزيارات', title:'كل زيارة، ولها تفاصيلها', desc:'الأسعار بالجنيه المصري. اللي مش متاح اكتبه «غير متاح»، واللي لسه مش محدد سيبه فاضي.',fields:[
 ['first','الكشف أول مرة: السعر والمدة؟','text','مثلًا: ٥٠٠ جنيه — ٣٠ دقيقة'],
 ['follow','المتابعة: السعر والمدة وشروطها؟','area','خلال كام يوم؟ وهل في متابعة مشمولة في الكشف؟'],
 ['online','هل الاستشارة أونلاين متاحة؟',['نعم','لا','نقرر بعدين']],
 ['extra','تفاصيل الأونلاين أو أي خدمة إضافية','area','لو متاحة: اسم الخدمة، سعرها، ومدتها.']]},
 {name:'المواعيد', title:'نظبطها على إيقاع العيادة', desc:'ممكن الدكتور أو الاستقبال يكمّل الجزء ده. التفاصيل دي هتساعدنا نمنع تضارب المواعيد.',fields:[
 ['hours','أيام ومواعيد العمل، والراحة والإجازات؟','area','مثلًا: السبت والاثنين ٥–٩ مساءً، راحة ٧–٧:٣٠. الجمعة إجازة.'],
 ['capacity','عدد المرضى وطريقة توزيع المواعيد؟','area','الحد الأقصى يوميًا أو لكل فترة؟ كل ١٥/٣٠ دقيقة، حسب مدة الخدمة، ولا ترتيب استقبال؟'],
 ['confirmation','أهم نقطة: الحجز يتأكد إزاي؟',['تلقائيًا فور الحجز','بعد موافقة الاستقبال','لسه محتاجين نقرر']],
 ['window','مسموح الحجز قبل الموعد بقد إيه؟','text','أقل مهلة، أقصى عدد أيام، والحجز في نفس اليوم لحد الساعة كام؟'],
 ['changes','الإلغاء والتعديل من المريض؟',['مسموح من التطبيق','عن طريق الاستقبال فقط','نحددها سوا']],
 ['policy','مهلة التعديل والإلغاء، والتأخير أو عدم الحضور؟','area','مثلًا: قبل الموعد بـ٢٤ ساعة. وإيه اللي يحصل لو المريض اتأخر؟']]},
 {name:'العيادة', title:'نخلّي الوصول لحضرتك أسهل', desc:'بيانات التواصل هنا خاصة بالعيادة والاستقبال، مش بيانات مرضى.',fields:[
 ['clinic','اسم العيادة الرسمي والعنوان والفروع','area','المنطقة، الشارع، الدور، الوحدة، علامة مميزة. ولو فيه فروع، مواعيد كل فرع.'],
 ['maps','رابط موقع العيادة على Google Maps','url','https://maps.google.com/…'],
 ['phone','واتساب الاستقبال بكود الدولة','tel','مثلًا: +20…'],
 ['reception','رقم بديل ومواعيد الاستقبال والمسؤول عن الحجز','area','مين يؤكد ويعدل المواعيد؟ ومين يقدر يوقف الحجز أو يضيف إجازة؟'],
 ['payment','طريقة الدفع المتاحة فعلًا؟',['في العيادة فقط','دفع إلكتروني','عربون والباقي في العيادة','لسه هنحدد']],
 ['operations','بتديروا الحجز حاليًا إزاي؟ والتذكيرات المطلوبة؟','area','دفتر، نظام، تقويم؟ تذكير بواتساب/رسالة/مكالمة؟ ولو فيه دفع أو عربون، إيه شروطه؟']]},
 {name:'اللمسات', title:'آخر لمسة، وتبقى شبه حضرتك', desc:'الجزء ده اختياري وممكن نكمّله بعدين. الصورة والمؤهلات ممكن تبعتها مع الرسالة على واتساب.',fields:[
 ['profile','الاسم والمسمى المهني والنبذة اللي نظهرها','area','التخصص والمؤهلات والخبرات المعتمدة، بالطريقة اللي تحب المرضى يشوفوها.'],
 ['instructions','تعليمات قبل الزيارة أو أسئلة بتتكرر؟','area','تقارير سابقة؟ الحضور قبل الموعد بكام دقيقة؟ شروط المتابعة؟'],
 ['data','إيه بيانات المريض الضرورية للحجز؟','area','مثلًا: الاسم ورقم الهاتف فقط. وهل هناك ضرورة لتاريخ الميلاد؟ من غير بيانات مرضى فعلية.'],
 ['privacy','مين يراجع سياسة الخصوصية والموافقة على التواصل؟','text','اسم المسؤول، وأي متطلبات خاصة لاستخدام بيانات الحجز.'],
 ['last','أي حاجة تانية تحب تقولها لفريق الاستوديو؟','area','ملاحظة صغيرة، فكرة، أو حاجة مش حاببها… إحنا سامعينك.']]}
];
let answers = {}, step = 0, storageOK = true;
try { const saved = JSON.parse(localStorage.getItem(KEY) || 'null'); if(saved && typeof saved.answers === 'object' && saved.answers) { for(const g of groups) for(const [id] of g.fields) if(typeof saved.answers[id] === 'string') answers[id]=saved.answers[id].slice(0,1500); step = Math.min(groups.length, Math.max(0, Number.isInteger(saved.step)?saved.step:0)); }} catch { storageOK=false; }
const $ = id => document.getElementById(id);
const esc = s => String(s).replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function save() { try {localStorage.setItem(KEY,JSON.stringify({answers,step}));storageOK=true;}catch{storageOK=false;} $('saved').textContent=storageOK?'المسودة محفوظة على جهازك ✓':'الحفظ غير متاح — نزّل إجاباتك قبل ما تقفل'; }
function field([id,label,type,placeholder]) {
 const val=answers[id]||'';
 if(Array.isArray(type)) return `<fieldset class="field"><legend>${esc(label)}</legend><div class="choices">${type.map(option=>`<label class="choice"><input type="radio" name="${id}" value="${esc(option)}" ${val===option?'checked':''}><span>${esc(option)}</span></label>`).join('')}</div></fieldset>`;
 return `<div class="field"><label for="${id}">${esc(label)}</label>${type==='area'?`<textarea id="${id}" name="${id}" maxlength="1500" placeholder="${esc(placeholder)}">${esc(val)}</textarea>`:`<input id="${id}" name="${id}" type="${type}" ${['url','tel'].includes(type)?'dir="ltr"':''} maxlength="1500" placeholder="${esc(placeholder)}" value="${esc(val)}">`}</div>`;
}
function report() {return 'مراجعة تطبيق دكتور عمرو — Code & Canvas\n\n'+groups.map(g=>g.name+'\n'+g.fields.map(([id,label])=>label+'\n'+(answers[id]?.trim()||'نحدده معًا')).join('\n\n')).join('\n\n────────\n\n');}
function render(focus=false){
 const review=step===groups.length;
 $('step-count').textContent=`${step+1} / ${groups.length+1} — ${review?'مراجعة وإرسال':'خطوة صغيرة ونقرّب أكتر'}`;
 $('progress').style.width=`${(step+1)/(groups.length+1)*100}%`;
 $('steps').innerHTML=[...groups.map(g=>g.name),'المراجعة'].map((n,i)=>`<button type="button" data-step="${i}" ${step===i?'aria-current="step"':''}>${i<step?'✓ ':''}${n}</button>`).join('');
 $('back').hidden=step===0; $('next').hidden=review;
 $('next').textContent=step===groups.length-1?'نراجع الإجابات ←':'نكمل ←';
 if(!review){const g=groups[step];$('panel').innerHTML=`<span class="kicker">${String(step+1).padStart(2,'0')} / LET’S MAKE IT YOURS</span><h2 tabindex="-1">${g.title}</h2><p class="description">${g.desc}</p>${g.fields.map(field).join('')}`;}
 else {$('panel').innerHTML=`<span class="kicker">READY WHEN YOU ARE</span><h2 tabindex="-1">كده الصورة وضحت. شكرًا لحضرتك ✳</h2><p class="description">راجع إجاباتك، وارجع لأي خطوة لتعديلها. الأسئلة اللي سيبتها هنحددها سوا. لسه ما اتبعتش أي إجابات للاستوديو.</p>${groups.map(g=>`<section class="summary-group"><h3>${g.name}</h3><dl>${g.fields.map(([id,label])=>`<dt>${esc(label)}</dt><dd>${esc(answers[id]?.trim()||'نحدده معًا')}</dd>`).join('')}</dl></section>`).join('')}<div class="delivery"><button type="button" class="primary" id="whatsapp">فتح واتساب الاستوديو ↗</button><button type="button" class="secondary" id="copy">نسخ الإجابات</button><button type="button" class="secondary" id="download">تنزيل ملف الإجابات</button></div><p class="hint">واتساب الاستوديو: <b dir="ltr">+20 109 250 0454</b>. فتح واتساب لا يعني الإرسال؛ اضغط إرسال هناك. لو الرسالة طويلة، نزّل الملف وأرفقه في المحادثة.</p><p id="delivery-status" role="status"></p>`;}
 if(focus)$('panel').querySelector('h2').focus();
}
$('review-form').addEventListener('input', e=>{if(e.target.name){answers[e.target.name]=e.target.value;save();}});
$('review-form').addEventListener('submit',e=>{e.preventDefault();if(step<groups.length){step++;save();render(true);}});
$('back').addEventListener('click',()=>{if(step>0){step--;save();render(true);}});
$('steps').addEventListener('click',e=>{const button=e.target.closest('[data-step]');if(button){step=Number(button.dataset.step);save();render(true);}});
$('clear').addEventListener('click',()=>{if(confirm('نمْسح الإجابات المحفوظة على الجهاز ده؟ الإجراء ده مش بيرجع.')){answers={};step=0;try{localStorage.removeItem(KEY);}catch{}render(true);$('saved').textContent='تم مسح المسودة من الجهاز';}});
$('panel').addEventListener('click',async e=>{
 if(e.target.id==='whatsapp'){
 const text=report();const long=text.length>3500;
 window.open('https://wa.me/201092500454?text='+encodeURIComponent(long?'أهلًا فريق Code & Canvas، دي مراجعتي لتطبيق دكتور عمرو. هرفق ملف الإجابات في المحادثة.':text),'_blank','noopener,noreferrer');
 $('delivery-status').textContent=long?'الإجابات طويلة: نزّل ملف الإجابات وأرفقه في واتساب. لم يتم إرسال شيء تلقائيًا.':'كمّل الإرسال داخل واتساب. لو ما فتحش، انسخ الإجابات أو نزّلها.';
 }
 if(e.target.id==='copy'){try{await navigator.clipboard.writeText(report());$('delivery-status').textContent='تم النسخ ✓ ابعت الإجابات لفريق الاستوديو في محادثتك.';}catch{$('delivery-status').textContent='النسخ مش متاح في المتصفح ده. تقدر تنزّل الملف بدلًا منه.';}}
 if(e.target.id==='download'){const url=URL.createObjectURL(new Blob(['\uFEFF'+report()],{type:'text/plain;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download='dr-amro-review.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);$('delivery-status').textContent='تم تجهيز الملف للتنزيل. أرفقه في محادثة الاستوديو لإرسال إجاباتك.';}
});
render();if(!storageOK)$('saved').textContent='الحفظ غير متاح في المتصفح ده';
})();
