import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {memoryPool,memoryQueue,memoryContextQuestion,recordMemoryReview} from '../js/memory.js';
import {defaultProgress} from '../js/engine.js';
import {mergeProgress} from '../js/progress-safety.js';
const read=name=>JSON.parse(fs.readFileSync(new URL('../data/'+name+'.json',import.meta.url),'utf8'));
const bank=read('daily-expressions');
const existing=[...read('vocabulary'),...read('phrasals')];
const normalize=s=>s.normalize('NFKC').toLocaleLowerCase('en-US').replace(/[^a-z0-9]/g,'');
test('B1/B2/C1 everyday expressions: exact 150/210/140 unique stable lesson IDs',()=>{
 assert.equal(bank.meta.targetTotal,500);
 assert.deepEqual(bank.meta.targetByLevel,{B1:150,B2:210,C1:140});
 assert.equal(bank.cards.length,500);assert.equal(new Set(bank.cards.map(x=>x.id)).size,500);
 assert.equal(new Set(bank.cards.map(x=>normalize(x.expression))).size,500);
 for(const [lvl,n] of [['B1',150],['B2',210],['C1',140]]){
   const found=bank.cards.filter(x=>x.level===lvl);assert.equal(found.length,n);
   assert.deepEqual(found.map(x=>x.id),Array.from({length:n},(_,i)=>`ex-${lvl.toLowerCase()}-${String(i+1).padStart(3,'0')}`));
 }
 assert.equal(bank.cards[0].expression,'Keep you warm');
 assert.equal(bank.meta.independentEditorApproved,false);
 assert.equal(bank.meta.approvedHumanVoiceCount,0);
});
test('all daily chunks have natural-context teaching fields and no licensed-audio claims',()=>{
 const used=new Set(existing.map(x=>normalize(x.word)));
 for(const x of bank.cards){
  assert.ok(x.expression.length>3&&x.tr.length>2,x.id);
  assert.ok(x.usageNote.length>18,x.id);
  assert.equal(x.examples.length,2,x.id);
  assert.notEqual(x.examples[0].toLowerCase(),x.examples[1].toLowerCase(),x.id);
  assert.ok(x.examples.every(s=>/[a-z]/i.test(s)&&s.trim().endsWith('.')||s.trim().endsWith('!')||s.trim().endsWith('?')),x.id);
  assert.equal(x.dialogue.length,2,x.id);
  assert.deepEqual(x.dialogue.map(x=>x.speaker),['A','B']);
  assert.ok(x.dialogue.every(v=>v.text.length>=7),x.id);
  assert.equal(x.audioStatus,'not_provided',x.id);
  assert.equal(x.editorialStatus,'authored_pending_independent_review',x.id);
  assert.ok(!used.has(normalize(x.expression)),`existing vocabulary/phrasal collision ${x.expression}`);
 }
});
test('expressions join memory studio but FSRS progress never pollutes old word or phrasal IDs',()=>{
 const pool=memoryPool({vocabulary:[],phrasals:[]},[],[],null,bank.cards);
 assert.equal(pool.length,500);
 const state=defaultProgress();
 const ids=memoryQueue(pool,state,{scope:'expression',now:1750000000000,max:10});
 assert.deepEqual(ids,pool.slice(0,10).map(x=>x.id));
 assert.equal(memoryQueue(pool,state,{scope:'expression-b1',max:250}).length,150);
 assert.equal(memoryQueue(pool,state,{scope:'expression-b2',max:250}).length,210);
 assert.equal(memoryQueue(pool,state,{scope:'expression-c1',max:250}).length,140);
 const first=pool[0];const graded=recordMemoryReview(state,first,{recallCorrect:true,contextCorrect:true,listeningCorrect:null},1750000000000);
 assert.equal(graded.grade,'good');assert.equal(state.expressions[first.lessonId].attempts,1);
 assert.deepEqual(state.cards,{});assert.deepEqual(state.phrasals,{});
 assert.ok(!memoryQueue(pool,state,{scope:'expression',now:1750000000001,max:100}).includes(first.id));
 const question=memoryContextQuestion(first,pool);
 assert.equal(question.choices.length,4);assert.ok(question.choices.includes(first.tr));
});
test('legacy backups merge without wiping new daily-expression review progress',()=>{
 const state=defaultProgress();state.expressions['ex-b1-001']={last:400,due:700,attempts:3};
 const old=defaultProgress();delete old.expressions;old.cards['old-id']={last:500,due:900,attempts:8};
 const merged=mergeProgress(state,{app:'American English Lab',format:1,progress:old});
 assert.equal(merged.expressions['ex-b1-001'].attempts,3);
 assert.equal(merged.cards['old-id'].attempts,8);
});
test('data is offline pre-cached and UI includes a distinct daily expressions entrypoint',()=>{
 const sw=fs.readFileSync(new URL('../sw.js',import.meta.url),'utf8');
 const ui=fs.readFileSync(new URL('../js/app.js',import.meta.url),'utf8');
 assert.ok(sw.includes("'./data/daily-expressions.json'"));
 assert.ok(ui.includes("['expressions','💬','Günlük Kalıplar']"));
 assert.ok(ui.includes("case 'expressionPractice'"));
 assert.ok(ui.includes('data.expressions?.cards'));
});

test('independent review and human audio are not misrepresented as completed',()=>{
  assert.equal(bank.meta.approvedHumanVoiceCount,0);
  assert.equal(bank.meta.independentEditorApproved,false);
  assert.ok(bank.cards.every(x=>x.audioStatus==='not_provided'&&x.editorialStatus==='authored_pending_independent_review'));
});

test('200 additions are 80 transitions, 70 collocations, 50 sentence starters; legacy is preserved',()=>{
 const fresh=bank.cards.slice(300);assert.equal(fresh.length,200);
 for(const [category,n] of [['connectors',80],['collocations',70],['conversation_starters',50]])
  assert.equal(fresh.filter(x=>x.category===category).length,n);
 assert.equal(bank.cards[99].expression,'I owe you one');
 assert.equal(bank.cards[299].expression,"I'll cross that bridge when I come to it");
 assert.equal(bank.meta.legacyToeflDailyIds.length,42);
 assert.ok(bank.meta.legacyToeflDailyIds.every(id=>bank.cards.slice(0,300).some(x=>x.id===id)));
 assert.ok(fresh.every(x=>x.contexts.includes('daily')));
 assert.ok(fresh.some(x=>x.contexts.includes('toefl')));
});
test('TOEFL + Daily is a curriculum tag, not a second FSRS identity',()=>{
 const enriched=bank.cards.map(x=>({...x,contexts:x.contexts|| (bank.meta.legacyToeflDailyIds.includes(x.id)?['daily','toefl']:['daily'])}));
 const pool=memoryPool({vocabulary:[],phrasals:[]},[],[],null,enriched);
 const state=defaultProgress();
 const toefl=memoryQueue(pool,state,{scope:'expression-toefl',max:1000});
 const daily=memoryQueue(pool,state,{scope:'expression-daily',max:1000});
 assert.equal(toefl.length+daily.length,500);
 assert.equal(toefl.length,new Set(toefl).size);
 assert.equal(memoryQueue(pool,state,{scope:'expression-toefl',expressionLevel:'B1',max:1000}).length,toefl.filter(id=>pool.find(x=>x.id===id).level==='B1').length);
 assert.equal(new Set(pool.map(x=>x.id)).size,500);
});
