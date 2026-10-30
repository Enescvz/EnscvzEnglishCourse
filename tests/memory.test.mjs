import test from 'node:test';
import assert from 'node:assert/strict';
import {memoryPool,memoryQueue,memoryAnswer,memorySentenceContains,memoryGrade,memoryContextQuestion,recordMemoryReview,memoryStageProgress} from '../js/memory.js';
const vocab=[{id:'v1',word:'reluctant',tr:'isteksiz',definition:'Unwilling to act',example:'She was reluctant.',level:'B2',category:'general'},{id:'v2',word:'reliable',tr:'güvenilir',definition:'Can be trusted',example:'A reliable friend.',level:'B2',category:'general'}];
const phrasals=[{id:'p1',word:'figure out',tr:'anlamak',definition:'To understand a problem',example:'I figured it out.',level:'B2'}];
const focus={vocabulary:[{word:'reluctant',status:'context_draft',lessonId:'v1',level:'B2'},{word:'reliable',status:'headword_only',level:'B2'},{word:'bogus',status:'context_draft',lessonId:'not-found',level:'C1'}],phrasals:[{word:'figure out',status:'context_draft',lessonId:'p1'}]};
test('only real contextual cards enter memory coaching; candidate labels never count',()=>{
 const p=memoryPool(focus,vocab,phrasals);assert.deepEqual(p.map(x=>x.id),['word:v1','phrasal:p1']);assert.equal(p[0].contentStatus,'authored_unreviewed');
});
test('due cards first, then unseen, not-yet-due after; scoped C1 filters',()=>{
 const pool=memoryPool(focus,vocab,phrasals),state={cards:{v1:{due:500}},phrasals:{}};
 assert.deepEqual(memoryQueue(pool,state,{now:1000}),['word:v1','phrasal:p1']);
 assert.deepEqual(memoryQueue(pool,state,{scope:'C1',now:1000}),[]);
 assert.deepEqual(memoryQueue(pool,{cards:{v1:{due:3000}},phrasals:{}},{now:1000}),['phrasal:p1']);
});
test('exact typed recall is checked; punctuation normalized but wrong phrases rejected',()=>{
 assert.equal(memoryAnswer('Figure out!','figure out'),true);
 assert.equal(memoryAnswer('figure in','figure out'),false);
 assert.equal(memorySentenceContains('I can figure out the answer.','figure out'),true);
 assert.equal(memorySentenceContains('I can figure outlay this answer.','figure out'),false);
});
test('a correct listening with incorrect recall never advances mastery',()=>{
 assert.equal(memoryGrade({listeningCorrect:true,recallCorrect:false,productionConfirmed:true}),'again');
 assert.equal(memoryGrade({listeningCorrect:false,recallCorrect:true,productionConfirmed:true}),'hard');
 assert.equal(memoryGrade({listeningCorrect:true,recallCorrect:true,contextCorrect:true,productionConfirmed:false}),'good');
 assert.equal(memoryGrade({listeningCorrect:true,recallCorrect:true,contextCorrect:true,productionConfirmed:true}),'good');
 assert.equal(memoryGrade({listeningCorrect:null,recallCorrect:true,contextCorrect:true,productionConfirmed:true}),'good');
 assert.equal(memoryGrade({listeningCorrect:true,recallCorrect:true,contextCorrect:false,productionConfirmed:true}),'hard');
 assert.equal(memoryGrade({listeningCorrect:true,recallCorrect:true,productionConfirmed:true}),'hard');
});
test('one FSRS review, self-reported production distinct from verified modes',()=>{
 const p={cards:{},phrasals:{}},item=memoryPool(focus,vocab,phrasals)[0],now=1750000000000;
 const result=recordMemoryReview(p,item,{listeningCorrect:true,recallCorrect:true,contextCorrect:true,productionConfirmed:true},now);
 assert.equal(result.grade,'good');assert.equal(p.cards.v1.attempts,1);
 assert.equal(p.cards.v1.modeSuccess.listening,undefined);assert.equal(p.cards.v1.ttsRecognitionSuccess,1);assert.equal(p.cards.v1.modeSuccess.context,1);assert.equal(p.cards.v1.modeSuccess.production,undefined);
 assert.equal(p.cards.v1.selfReportedProduction,1);assert.ok(p.cards.v1.due>now);
});

test('meaning-in-context options are distinct, stable, and no fixed answer position',()=>{
 const lesson={id:'word:1',kind:'word',tr:'beklenmedik şekilde',word:'unexpectedly',example:'The meeting ended unexpectedly.',examples:['The meeting ended unexpectedly.','The train unexpectedly stopped.']};
 const pool=[lesson,...['dikkatlice','büyük ölçüde','kesinlikle','hevesle','yavaşça'].map((tr,i)=>({id:'word:'+i,kind:'word',tr,word:'example'+i}))];
 const q=memoryContextQuestion(lesson,pool);
 assert.equal(q.sentence,'The train unexpectedly stopped.');
 assert.equal(q.choices.length,4);
 assert.equal(new Set(q.choices).size,4);
 assert.ok(q.choices.includes(lesson.tr));
 assert.deepEqual(q,memoryContextQuestion(lesson,pool));
 assert.equal(memoryContextQuestion(lesson,[lesson]),null);
});

test('five-stage progress has clear active step without prematurely marking it completed',()=>{
 const start=memoryStageProgress('learn',0,10);
 assert.equal(start.active,0);assert.equal(start.sessionPercent,0);
 assert.deepEqual(start.stages.map(x=>x.state),['current','upcoming','upcoming','upcoming','upcoming']);
 const later=memoryStageProgress('context',3,10);
 assert.equal(later.sessionPercent,36);
 assert.deepEqual(later.stages.map(x=>x.state),['done','done','done','current','upcoming']);
});


test('future cards cannot be moved forward by empty session capacity',()=>{
 const lessons=[{id:'word:a',kind:'word',lessonId:'a'},{id:'word:b',kind:'word',lessonId:'b'}];
 const state={cards:{a:{due:200_000},b:{due:120_000}},phrasals:{}};
 assert.deepEqual(memoryQueue(lessons,state,{now:100_000,max:10}),[]);
 assert.deepEqual(memoryQueue(lessons,state,{now:130_000,max:10}),['word:b']);
 assert.deepEqual(memoryQueue(lessons,state,{now:210_000,max:10}),['word:b','word:a']);
});
test('synthetic audio is optional, does not count as verified human listening',()=>{
 const p={cards:{},phrasals:{}}, item={kind:'word',lessonId:'x'};
 const now=1750000000000;
 assert.equal(memoryGrade({listeningCorrect:null,recallCorrect:true,contextCorrect:true}),'good');
 const a=recordMemoryReview(p,item,{listeningCorrect:null,recallCorrect:true,contextCorrect:true},now);
 assert.equal(a.grade,'good');assert.equal(a.state.modeSuccess.listening,undefined);
 const b=recordMemoryReview(p,item,{listeningCorrect:true,recallCorrect:true,contextCorrect:true},now+5*86400000);
 assert.equal(b.state.ttsRecognitionSuccess,1);
 assert.equal(b.state.modeSuccess.listening,undefined);
 assert.equal(b.state.selfReportedProduction,undefined);
});
test('self-reported production cannot change memory grade or verified mastery',()=>{
 const x={listeningCorrect:null,recallCorrect:true,contextCorrect:true};
 assert.equal(memoryGrade({...x,productionConfirmed:false}),memoryGrade({...x,productionConfirmed:true}));
 assert.equal(memoryGrade({...x,contextCorrect:false,productionConfirmed:true}),'hard');
 assert.equal(memoryGrade({...x,recallCorrect:false,productionConfirmed:true}),'again');
});

test('TOEFL academic cards join the same FSRS bank without duplicate card identities',()=>{
 const academic={id:'toefl-analyze',word:'analyze',tr:'analiz etmek',definition:'To examine data',example:'We analyze data.',level:'B2',category:'toeflAcademic'};
 const core={wordLessonIds:['v1','toefl-analyze'],phrasalLessonIds:['p1']};
 const pool=memoryPool(focus,[...vocab,academic],phrasals,core);
 assert.deepEqual(pool.map(x=>x.id),['word:v1','phrasal:p1','word:toefl-analyze']);
 assert.deepEqual(memoryQueue(pool,{cards:{},phrasals:{}},{scope:'toefl',now:0}),pool.map(x=>x.id));
 const state={cards:{'toefl-analyze':{attempts:3,due:1000},v1:{due:9000}},phrasals:{p1:{due:9000}}};
 assert.deepEqual(memoryQueue(pool,state,{scope:'toefl',now:2000}),['word:toefl-analyze']);
 assert.equal(getKeys(state.cards).includes('toefl-analyze'),true);
});
function getKeys(obj){return Object.keys(obj);}
test('old records without due time remain recoverable in review queue',()=>{
 const item={id:'word:a',kind:'word',lessonId:'a'};
 assert.deepEqual(memoryQueue([item],{cards:{a:{attempts:3}},phrasals:{}},{now:10000}),['word:a']);
});

test('full shipped TOEFL set is eligible for science-based reviews with no ID duplication', async()=>{
 const {readFileSync}=await import('node:fs');
 const read=name=>JSON.parse(readFileSync(new URL('../data/'+name+'.json',import.meta.url)));
 const pool=memoryPool(read('fluency-focus'),[...read('vocabulary'),...read('toefl-academic')],read('phrasals'),read('toefl-core'));
 assert.equal(pool.length,1550);
 assert.equal(new Set(pool.map(x=>x.id)).size,1550);
 const core=pool.filter(x=>x.toefl);
 assert.equal(core.filter(x=>x.kind==='word').length,400);
 assert.equal(core.filter(x=>x.kind==='phrasal').length,75);
 assert.equal(core.every(x=>x.example&&x.definition&&x.tr),true);
});
