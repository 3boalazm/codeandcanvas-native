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
 ['extra','أي خدمات إضافية أو ملاحظات على الزيارات (اختياري)','area','اسم الخدمة، سعرها ومدتها لو متاحة، أو أي مدة مختلفة.']]},
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
// Structured controls keep the existing draft key and retain earlier free-text answers.
const duration = ['١٠ دقائق','١٥ دقيقة','٢٠ دقيقة','٣٠ دقيقة','٤٥ دقيقة','٦٠ دقيقة','اختيار آخر'];
const days = ['السبت','الأحد','الاثنين','الثلاثاء','الأربعاء','الخميس','الجمعة'];
const choice = (id,label,options) => [id,label,{options:[...options,'نحدده معًا']}];
groups[1].fields = [
 ['first_price','سعر الكشف أول مرة (جنيه)','number'], choice('first_duration','مدة الكشف أول مرة',duration),
 choice('follow_available','هل المتابعة متاحة؟',['نعم، بسعر منفصل','مشمولة في الكشف بشروط','غير متاحة']),
 ['follow_price','سعر المتابعة لو منفصل (جنيه)','number'], choice('follow_duration','مدة المتابعة',duration),
 choice('follow_window','المتابعة خلال قد إيه؟',['٧ أيام','١٤ يوم','٣٠ يوم','اختيار آخر']),
 ['follow_notes','شروط المتابعة وأي مدد زيارات مختلفة','area','أي استثناءات أو شروط إضافية'],
 groups[1].fields[2], ['online_price','سعر الاستشارة أونلاين لو متاحة (جنيه)','number'],
 choice('online_duration','مدة الاستشارة أونلاين لو متاحة',duration), groups[1].fields[3]
];
groups[1].desc = 'اختار المدة واكتب السعر فقط. سيب غير المتاح فاضي، ولو المدة مختلفة اكتبها في الملاحظات.';
groups[2].fields = [
 ...days.map((day,i)=>['day_'+i,day,'day']),
 ['schedule_notes','إجازات استثنائية، فروع أو فترات عمل إضافية','area','لو فيه فترة صباحية ومسائية، أو مواعيد بعد منتصف الليل، اكتب التفاصيل هنا.'],
 ['daily_capacity','الحد الأقصى للمرضى يوميًا','number'],
 ['period_capacity','الحد الأقصى لكل فترة (لو فيه)','number'],
 choice('slot_rule','طريقة توزيع المواعيد',['كل ١٥ دقيقة','كل ٢٠ دقيقة','كل ٣٠ دقيقة','حسب مدة الخدمة','ترتيب الاستقبال','اختيار آخر']),
 groups[2].fields[2],
 choice('min_notice','أقل وقت بين الحجز والزيارة',['بدون مهلة','ساعة','ساعتان','٦ ساعات','٢٤ ساعة','اختيار آخر']),
 choice('max_notice','الحجز متاح لقدّام لحد',['٧ أيام','١٤ يوم','٣٠ يوم','٦٠ يوم','٩٠ يوم','اختيار آخر']),
 choice('same_day','هل الحجز في نفس اليوم مسموح؟',['نعم','لا']),
 ['same_day_cutoff','آخر ساعة للحجز في نفس اليوم (لو مسموح)','time'],
 groups[2].fields[4],
 choice('cancel_notice','مهلة الإلغاء أو التعديل',['في أي وقت قبل الموعد','قبل ساعتين','قبل ٦ ساعات','قبل ١٢ ساعة','قبل ٢٤ ساعة','قبل ٤٨ ساعة','اختيار آخر']),
 choice('late_rule','في حالة التأخير أو عدم الحضور',['الاستقبال يتواصل ويعيد الترتيب','إلغاء الموعد وإعادة الحجز','حسب الحالة مع الاستقبال','اختيار آخر']),
 ['booking_notes','تفاصيل أو اختيارات مختلفة لقواعد الحجز','area','اكتب أي اختيار مختلف أو استثناء هنا.']
];
groups[2].desc = 'حدّد حالة كل يوم، وبعدها اختار ساعات العمل والراحة. مفيش يوم أو سياسة مختارين مسبقًا. المواعيد بتوقيت العيادة في مصر.';
groups[3].fields = [
 ...groups[3].fields.slice(0,3),
 choice('branches','هل فيه أكثر من فرع؟',['فرع واحد','أكثر من فرع']),
 ['alternate_phone','رقم اتصال بديل','tel'],
 choice('manager','مين المسؤول عن تأكيد وتعديل الحجوزات؟',['الاستقبال','الدكتور','الدكتور والاستقبال','اختيار آخر']),
 choice('closure_manager','مين يقدر يوقف الحجز ويضيف إجازات؟',['الاستقبال','الدكتور فقط','الدكتور والاستقبال','اختيار آخر']),
 choice('reception_hours','مواعيد تواصل الاستقبال',['نفس ساعات العيادة','مواعيد مختلفة']),
 ['reception_notes','مواعيد التواصل المختلفة','area','اسم المسؤول وأي تفاصيل إضافية'],
 groups[3].fields[4],
 choice('current_system','بتديروا الحجوزات حاليًا إزاي؟',['دفتر أو ورق','واتساب أو مكالمات','تقويم Google','نظام حجز موجود','اختيار آخر']),
 ['reminders','وسائل التذكير المطلوبة',{multi:['واتساب','رسالة SMS','مكالمة','بدون تذكيرات','نحددها لاحقًا']}],
 ['operations_notes','تفاصيل الفروع أو الدفع أو النظام الحالي','area','لو فيه عربون: قيمته وشروطه. ولو فيه نظام حالي: اسمه.']
];
groups[4].fields.splice(2,1,
 ['patient_fields','بيانات المريض الضرورية للحجز',{multi:['الاسم','رقم الهاتف','الفئة العمرية','تاريخ الميلاد','نحددها لاحقًا']}],
 ['data_notes','سبب الاحتياج للعمر أو أي بيانات إضافية','area','من غير إضافة بيانات مرضى فعلية.']);
groups[3].fields.push(
 ['branch_details','عناوين ومواعيد الفروع الإضافية','area','اسم كل فرع، عنوانه ومواعيده.'],
 ['payment_details','تفاصيل الدفع الإلكتروني أو العربون','area','الوسيلة، وقيمة العربون وشروطه لو مطلوب.'],
 ['system_details','اسم نظام الحجز الحالي','text','اسم النظام المستخدم حاليًا']
);
// Older drafts remain visible/editable rather than silently discarded.
const legacy = [
 [1,'first','إجابتك السابقة عن الكشف'],[1,'follow','إجابتك السابقة عن المتابعة'],
 [2,'hours','إجابتك السابقة عن الجدول'],[2,'capacity','إجابتك السابقة عن السعة'],
 [2,'window','إجابتك السابقة عن مهلة الحجز'],[2,'policy','إجابتك السابقة عن الإلغاء'],
 [3,'reception','إجابتك السابقة عن الاستقبال'],[3,'operations','إجابتك السابقة عن الإدارة'],[4,'data','إجابتك السابقة عن بيانات المريض']
];
let answers = {}, step = 0, storageOK = true;
try { const saved = JSON.parse(localStorage.getItem(KEY) || 'null'); if(saved && typeof saved.answers === 'object' && saved.answers) { for(const [index,id,label] of legacy) if(typeof saved.answers[id] === 'string' && saved.answers[id]) groups[index].fields.push([id,label,'area']); for(const g of groups) for(const [id,,type] of g.fields) for(const key of (type==='day'?[id,...['start','end','break_start','break_end'].map(k=>id+'_'+k)]:[id])) if(typeof saved.answers[key] === 'string') answers[key]=saved.answers[key].slice(0,1500); step = Math.min(groups.length, Math.max(0, Number.isInteger(saved.step)?saved.step:0)); }} catch { storageOK=false; }
const $ = id => document.getElementById(id);
const esc = s => String(s).replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function save() { try {localStorage.setItem(KEY,JSON.stringify({answers,step}));storageOK=true;}catch{storageOK=false;} $('saved').textContent=storageOK?'المسودة محفوظة على جهازك ✓':'الحفظ غير متاح — نزّل إجاباتك قبل ما تقفل'; }
// Hidden details stay in the local draft, but are disabled and excluded from exports.
const followEnabled = () => ['نعم، بسعر منفصل','مشمولة في الكشف بشروط'].includes(answers.follow_available);
const conditions = {
 follow_price: () => answers.follow_available === 'نعم، بسعر منفصل',
 follow_duration: followEnabled, follow_window: followEnabled, follow_notes: followEnabled,
 online_price: () => answers.online === 'نعم', online_duration: () => answers.online === 'نعم',
 same_day_cutoff: () => answers.same_day === 'نعم',
 cancel_notice: () => ['مسموح من التطبيق','عن طريق الاستقبال فقط'].includes(answers.changes),
 reception_notes: () => answers.reception_hours === 'مواعيد مختلفة',
 branch_details: () => answers.branches === 'أكثر من فرع',
 payment_details: () => ['دفع إلكتروني','عربون والباقي في العيادة'].includes(answers.payment),
 system_details: () => answers.current_system === 'نظام حجز موجود',
 data_notes: () => (answers.patient_fields || '').split(' | ').some(v => ['الفئة العمرية','تاريخ الميلاد'].includes(v))
};
function visible(id) { return !conditions[id] || conditions[id](); }
function activeFields(group) { return group.fields.filter(([id]) => visible(id)); }
function field(def) {
 return `<div data-field="${def[0]}" ${visible(def[0])?'':'hidden'}>${fieldControl(def)}</div>`;
}
function syncConditions() {
 document.querySelectorAll('[data-field]').forEach(wrapper => {
  const show = visible(wrapper.dataset.field);
  wrapper.hidden = !show;
  wrapper.querySelectorAll('input,select,textarea,button').forEach(control => { control.disabled = !show; });
 });
}
function fieldControl([id,label,type,placeholder]) {
 const val=answers[id]||'';
 if(type==='day') return `<fieldset class="field day-row"><legend>${esc(label)}</legend><label class="hint" for="${id}">حالة يوم ${esc(label)}</label><select id="${id}" name="${id}" data-day="${id}">${['','عمل','إجازة','نحدده معًا'].map(o=>`<option value="${o}" ${val===o?'selected':''}>${o||'اختار حالة اليوم'}</option>`).join('')}</select><div id="${id}_hours" class="day-hours" ${val==='عمل'?'':'hidden'}>${[['start','بداية العمل'],['end','نهاية العمل'],['break_start','بداية الراحة (اختياري)'],['break_end','نهاية الراحة (اختياري)']].map(([key,title])=>`<div><label for="${id}_${key}">${title} — ${esc(label)}</label><input type="time" id="${id}_${key}" name="${id}_${key}" value="${esc(answers[id+'_'+key]||'')}"></div>`).join('')}<button type="button" class="text-button copy-day" data-copy="${id}">تطبيق ساعات اليوم على باقي أيام العمل</button></div></fieldset>`;
 if(type && type.options) return `<div class="field"><label for="${id}">${esc(label)}</label><select id="${id}" name="${id}"><option value="">اختار أو سيبها لبعدين</option>${type.options.map(o=>`<option value="${esc(o)}" ${val===o?'selected':''}>${esc(o)}</option>`).join('')}</select></div>`;
 if(type && type.multi) return `<fieldset class="field"><legend>${esc(label)} — ممكن أكتر من اختيار</legend><div class="choices">${type.multi.map(o=>`<label class="choice"><input type="checkbox" name="${id}" value="${esc(o)}" ${val.split(' | ').includes(o)?'checked':''}><span>${esc(o)}</span></label>`).join('')}</div></fieldset>`;

 if(Array.isArray(type)) return `<fieldset class="field"><legend>${esc(label)}</legend><div class="choices">${type.map(option=>`<label class="choice"><input type="radio" name="${id}" value="${esc(option)}" ${val===option?'checked':''}><span>${esc(option)}</span></label>`).join('')}</div></fieldset>`;
 return `<div class="field"><label for="${id}">${esc(label)}</label>${type==='area'?`<textarea id="${id}" name="${id}" maxlength="1500" placeholder="${esc(placeholder)}">${esc(val)}</textarea>`:`<input id="${id}" name="${id}" type="${type}" ${['url','tel'].includes(type)?'dir="ltr"':''} ${type==='number'?'min="0" max="100000" step="1" inputmode="numeric"':''} maxlength="1500" placeholder="${esc(placeholder||'')}" value="${esc(val)}">`}</div>`;
}
function displayAnswer(id,type) {
 if(type !== 'day') return answers[id]?.trim()||'نحدده معًا';
 if(answers[id]!=='عمل') return answers[id]||'نحدده معًا';
 const time=k=>answers[id+'_'+k]||'غير محدد';
 const rest=answers[id+'_break_start']||answers[id+'_break_end'];
 return `عمل: ${time('start')} – ${time('end')}`+(rest?`، راحة: ${time('break_start')} – ${time('break_end')}`:'، بدون راحة محددة');
}
function validSchedule(only) {
 const error=$('schedule-error');
 if(error) error.remove();
 if(step!==2)return true;
 for(let i=0;i<7;i++) {
 const id='day_'+i;if((only&&id!==only)||answers[id]!=='عمل')continue;
 const a=answers[id+'_start'],b=answers[id+'_end'],c=answers[id+'_break_start'],d=answers[id+'_break_end'];
 let message='';
 if(a&&b&&a>=b)message='نهاية العمل لازم تكون بعد البداية. الفترات بعد منتصف الليل اكتبها في الملاحظات.';
 else if((c&&d&&c>=d)||(a&&c&&c<a)||(b&&d&&d>b))message='اختار بداية ونهاية الراحة بالترتيب وداخل ساعات العمل.';
 if(message){const p=document.createElement('p');p.id='schedule-error';p.className='schedule-error';p.setAttribute('role','alert');p.textContent=days[i]+': '+message;$(id+'_hours').append(p);$(id+'_start').focus();return false;}
 }
 return true;
}
function report() {return 'مراجعة تطبيق دكتور عمرو — Code & Canvas\n\n'+groups.map(g=>g.name+'\n'+activeFields(g).map(([id,label,type])=>label+'\n'+displayAnswer(id,type)).join('\n\n')).join('\n\n────────\n\n');}
function render(focus=false){
 const review=step===groups.length;
 $('step-count').textContent=`${step+1} / ${groups.length+1} — ${review?'مراجعة وإرسال':'خطوة صغيرة ونقرّب أكتر'}`;
 $('progress').style.width=`${(step+1)/(groups.length+1)*100}%`;
 $('steps').innerHTML=[...groups.map(g=>g.name),'المراجعة'].map((n,i)=>`<button type="button" data-step="${i}" ${step===i?'aria-current="step"':''}>${i<step?'✓ ':''}${n}</button>`).join('');
 $('back').hidden=step===0; $('next').hidden=review;
 $('next').textContent=step===groups.length-1?'نراجع الإجابات ←':'نكمل ←';
 if(!review){const g=groups[step];$('panel').innerHTML=`<span class="kicker">${String(step+1).padStart(2,'0')} / LET’S MAKE IT YOURS</span><h2 tabindex="-1">${g.title}</h2><p class="description">${g.desc}</p>${g.fields.map(field).join('')}`;}
 else {$('panel').innerHTML=`<span class="kicker">READY WHEN YOU ARE</span><h2 tabindex="-1">كده الصورة وضحت. شكرًا لحضرتك ✳</h2><p class="description">راجع إجاباتك، وارجع لأي خطوة لتعديلها. الأسئلة اللي سيبتها هنحددها سوا. لسه ما اتبعتش أي إجابات للاستوديو.</p>${groups.map(g=>`<section class="summary-group"><h3>${g.name}</h3><dl>${activeFields(g).map(([id,label,type])=>`<dt>${esc(label)}</dt><dd>${esc(displayAnswer(id,type))}</dd>`).join('')}</dl></section>`).join('')}<div class="delivery"><button type="button" class="primary" id="whatsapp">فتح واتساب الاستوديو ↗</button><button type="button" class="secondary" id="copy">نسخ الإجابات</button><button type="button" class="secondary" id="download">تنزيل ملف الإجابات</button></div><p class="hint">واتساب الاستوديو: <b dir="ltr">+20 109 250 0454</b>. فتح واتساب لا يعني الإرسال؛ اضغط إرسال هناك. لو الرسالة طويلة، نزّل الملف وأرفقه في المحادثة.</p><p id="delivery-status" role="status"></p>`;}
 syncConditions();
 if(focus)$('panel').querySelector('h2').focus();
}
$('review-form').addEventListener('input', e=>{if(e.target.name){const el=e.target; answers[el.name]=el.type==='checkbox'?[...$('review-form').querySelectorAll(`input[name="${el.name}"]:checked`)].map(n=>n.value).join(' | '):el.value;if(el.dataset.day)$(el.name+'_hours').hidden=el.value!=='عمل';syncConditions();save();}});
$('review-form').addEventListener('submit',e=>{e.preventDefault();if(!$('review-form').reportValidity()||!validSchedule())return;if(step<groups.length){step++;save();render(true);}});
$('back').addEventListener('click',()=>{if(step>0){step--;save();render(true);}});
$('steps').addEventListener('click',e=>{const button=e.target.closest('[data-step]');if(button){if(!validSchedule()||!$('review-form').reportValidity())return;step=Number(button.dataset.step);save();render(true);}});
$('clear').addEventListener('click',()=>{if(confirm('نمْسح الإجابات المحفوظة على الجهاز ده؟ الإجراء ده مش بيرجع.')){answers={};step=0;try{localStorage.removeItem(KEY);}catch{}render(true);$('saved').textContent='تم مسح المسودة من الجهاز';}});
$('panel').addEventListener('click',async e=>{
 if(e.target.dataset.copy){
 const source=e.target.dataset.copy;
 if(!validSchedule(source))return;
 for(let i=0;i<7;i++){const id='day_'+i;if(id===source||answers[id]!=='عمل')continue;for(const k of ['start','end','break_start','break_end'])answers[id+'_'+k]=answers[source+'_'+k]||'';}
 save();render();$('saved').textContent='تم تطبيق الساعات على أيام العمل المختارة فقط ✓';
 }

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
