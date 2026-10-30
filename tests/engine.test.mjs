import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';
import {normalize,accuracy,diffWords,analyzeDictation,defaultProgress,reviewItem,dueItems,dailyPlan,dailyAssignments,quizBank,buildExam} from '../js/engine.js';
const read=k=>JSON.parse(fs.readFileSync(new URL('../data/'+k+'.json',import.meta.url)));
const vocab=read('vocabulary'),phrasals=read('phrasals'),episodes=read('episodes'),drills=read('drills'),readings=read('readings'),grammar=read('grammar');
test('vocabulary IDs unique; B2/C1 or explicitly specialist',()=>{assert.ok(vocab.length>=400);assert.equal(new Set(vocab.map(x=>x.id)).size,vocab.length);assert.ok(vocab.filter(x=>x.category==='finance'||x.category==='accounting').length>=200);for(let v of vocab){assert.ok(v.word&&v.tr&&v.example&&v.definition);assert.ok(v.category!=='general'||['B2','C1'].includes(v.level));}});
test('phrasals unique, sensible syntax and examples',()=>{assert.ok(phrasals.length>=60);assert.equal(new Set(phrasals.map(x=>x.id)).size,phrasals.length);for(const v of phrasals){assert.ok(['separable','inseparable','intransitive'].includes(v.syntax));assert.ok(v.example&&v.tr&&v.note);}});
test('robotic podcast/drill metadata remains but MP3s are quarantined; scripts and quizzes remain consistent',()=>{
 for(const ep of episodes){assert.ok(ep.audioType===undefined||ep.audioType==='synthetic');assert.equal(fs.existsSync(new URL('../'+ep.audio,import.meta.url)),false);assert.equal(ep.timings.length,ep.turns.length);for(let i=0;i<ep.turns.length;i++){const t=ep.timings[i];assert.ok(t.end>t.start);if(i)assert.ok(t.start>=ep.timings[i-1].end);}for(const q of ep.questions){assert.equal(new Set(q.options).size,4);assert.ok(q.options[q.answer]);}}
 for(const d of drills){assert.ok(d.audioType===undefined||d.audioType==='synthetic');assert.equal(fs.existsSync(new URL('../'+d.audio,import.meta.url)),false);}
});
test('reading & grammar keys valid',()=>{for(let r of readings){assert.equal(r.questions.length,5);for(let q of r.questions){assert.equal(new Set(q.options).size,4);assert.ok(Number.isInteger(q.answer)&&q.answer>=0&&q.answer<4);}}for(let g of grammar){assert.equal(g.options.length,4);assert.equal(new Set(g.options).size,4);assert.equal(g.answer,g.options[g.answerIndex??0]);}});
test('normalization and word-level dictation',()=>{assert.equal(normalize('  Acknowledged!  '),'acknowledged');assert.equal(accuracy('I am here','I am here'),100);assert.equal(accuracy('I here','I am here'),67);assert.equal(diffWords('I here','I am here').filter(x=>!x.ok).length,1);assert.ok(diffWords('dog bites man','man bites dog').some(x=>!x.ok),'Dictation word order must be assessed');});
test('spaced review punishes lapses and awards cross-modality mastery',()=>{let p=reviewItem({},'good','recognition',100000);assert.ok(p.due>100000);assert.equal(p.status,'Öğreniliyor');p=reviewItem(p,'again','recall',p.due);assert.equal(p.status,'Tekrar gerekli');assert.deepEqual(p.modeSuccess,{},'A lapse invalidates previous mastery evidence');let now=100000; p={}; for(let i=0;i<7;i++){p=reviewItem(p,'good',i===3?'production':i===4?'listening':i===5?'context':'recall',now);now=p.due;}assert.equal(p.status,'Pekişmiş');});
test('recall-only practice does not grant production mastery',()=>{let p={},now=0;for(let i=0;i<10;i++){p=reviewItem(p,'good','recognition',now);now=p.due;}assert.notEqual(p.status,'Pekişmiş');assert.notEqual(p.status,'Aktif kullanılabiliyor');});
test('due queue and adaptive day plan',()=>{const items=[{id:'a'},{id:'b'}],prog={a:{due:10},b:{due:200}};assert.deepEqual(dueItems(items,prog,100).map(x=>x.id),['a']);let p=defaultProgress();let result=dailyPlan(p,60);assert.equal(result.reduce((a,x)=>a+x.mins,0),60);p.listenHistory=[{accuracy:90}];assert.ok(dailyPlan(defaultProgress(),60)[0].mins>dailyPlan(p,60)[0].mins);});
test('exam never leaks answer position, has 25 unique questions and 4 distinct choices',()=>{const bank=quizBank(vocab,phrasals);assert.ok(bank.length>=550);for(const q of bank){assert.equal(new Set(q.options).size,4,q.id);assert.ok(q.options.includes(q.answer),q.id);for(const option of q.options)assert.ok(q.optionExplanations?.[option]?.length>15,`${q.id}: missing option-specific explanation for ${option}`);}const set=buildExam(bank,[],123456);assert.equal(set.length,25);assert.equal(new Set(set.map(x=>x.id)).size,25);const second=buildExam(bank,set.map(x=>x.id),123457);assert.ok(second.every(x=>!set.some(y=>y.id===x.id)));});

test('phrasal English explanations are not gloss templates; unique senses are taught in context',()=>{
 assert.ok(phrasals.length>=135);
 for(const p of phrasals){
   assert.ok(p.definition.length>=35,p.id);
   assert.ok(!p.definition.startsWith(p.word+':'),p.id);
   assert.ok(['B1','B2','C1'].includes(p.level),p.id);if(p.level==='B1')assert.equal(p.placementCheckFirst,true,p.id);
   assert.ok(p.senses?.length>=1,p.id);
   assert.ok(p.editorialStatus==='authored_unreviewed',p.id);
 }
});

test('listening diagnosis separates observable misses from unsupported assumptions',()=>{
 const v=[{word:'resilience',id:'g-resilience'},{word:'mitigate',id:'g-mitigate'}];
 const known={'g-resilience':{modeSuccess:{recall:2}},'g-mitigate':{modeSuccess:{recognition:3}}};
 const r=analyzeDictation('We appreciate your today','We appreciate your resilience today',v,known);
 assert.equal(r.accuracy,80);
 assert.deepEqual(r.missedWords,['resilience']);
 assert.deepEqual(r.previouslyRecalledButMissed,['resilience']);
 assert.ok(r.observation.includes('kanıtlamaz'));
 const r2=analyzeDictation('We appreciate your today','We appreciate your resilience today',v,{});
 assert.deepEqual(r2.previouslyRecalledButMissed,[]);
});

test('multi-sense phrasal uses become distinct exam questions with context',()=>{
 const bank=quizBank(vocab,phrasals),take=bank.filter(x=>x.question.includes('“take off”'));
 assert.ok(take.length>=3);
 assert.equal(new Set(take.map(x=>x.id)).size,take.length);
 assert.ok(take.some(x=>x.answer.includes('uçak')));
 assert.ok(take.some(x=>x.answer.includes('kıyafeti')));
});

test('daily missions prioritise due and then unseen; listening chooses an unfinished drill',()=>{
 const v=[{id:'new1',priority:0},{id:'late',priority:100},{id:'new2',priority:1}],ph=[{id:'pv1',priority:0}];
 const result=dailyAssignments(v,ph,[{title:'Used'},{title:'Fresh'}],{cards:{late:{due:0}},phrasals:{},listenHistory:[{title:'Used'}]},100,3,1);
 assert.deepEqual(result.words.map(x=>x.id),['late','new1','new2']);
 assert.equal(result.drill.title,'Fresh');
});

test('all learning cards have a visible original US-English example and consistent examples schema',()=>{
 const bad=/^(The investor considered|The finance department documented|The investment analyst discussed)\s/i;
 for(const v of [...vocab,...phrasals]){
   assert.ok(Array.isArray(v.examples)&&v.examples.length>=1,`${v.id}: missing examples array`);
   assert.equal(v.examples[0],v.example,`${v.id}: canonical example differs`);
   assert.equal(new Set(v.examples).size,v.examples.length,`${v.id}: repeated example`);
   assert.ok(v.examples.every(s=>s.length>=20&&/[.!?]$/.test(s)),`${v.id}: malformed context`);
   assert.ok(!v.examples.some(s=>bad.test(s)),`${v.id}: placeholder sentence detected`);
   assert.equal(v.editorialStatus,'authored_unreviewed',`${v.id}: do not misrepresent unreviewed copy`);
 }
});

test('multiple examples cover independent contexts without repeated primary sentences',()=>{
 assert.ok(vocab.filter(x=>x.examples.length>=2).length>=70);
 assert.ok(phrasals.filter(x=>x.examples.length>=2).length>=30);
 const domain=vocab.filter(x=>['finance','accounting'].includes(x.category));
 assert.equal(domain.length,284);
 assert.ok(domain.every(x=>x.examples[0].toLowerCase().includes(x.word.toLowerCase())),
  'Every specialist primary example must contain the study term in context');
});
