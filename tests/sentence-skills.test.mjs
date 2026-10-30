import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {validateSentenceSkills,listSkillExercises,sentenceCloze,assessSkillInput,skillNormalize,skillSummary,skillsDue,prepareSkillReview,persistSkillReview} from '../js/sentence-skills.js';
import {defaultProgress} from '../js/engine.js';
import {mergeProgress} from '../js/progress-safety.js';
const data=JSON.parse(readFileSync(new URL('../data/sentence-skills.json',import.meta.url)));
const items=listSkillExercises(data);
test('340 original tasks, unique IDs, expected four skills, accurate metadata',()=>{
 assert.deepEqual(validateSentenceSkills(data),{lessons:34,exercises:340});
 assert.equal(new Set(items.map(x=>x.id)).size,340);
 assert.equal(new Set(items.map(x=>x.modelAnswer.toLowerCase())).size,340);
 assert.deepEqual(Object.fromEntries(Object.keys(data.meta.lessonDistribution).map(area=>[area,data.lessons.filter(x=>x.area===area).length])),data.meta.lessonDistribution);
 assert.equal(data.meta.independentEditorApproved,false);
 assert.ok(items.every(x=>x.independentEditorApproved===false));
});
test('every order card uses valid, unmodified tokens and accepts punctuation variants',()=>{
 for(const x of items.filter(x=>x.mode==='order')){
  const shuffled=x.tokens.join(' ');
  assert.equal(skillNormalize(shuffled).split(' ').sort().join(' '),skillNormalize(x.modelAnswer).split(' ').sort().join(' '),x.id);
  assert.equal(assessSkillInput(x,x.modelAnswer,x.area).matched,true,x.id);
 }
});
test('all 136 cloze tasks get nonempty, hidden expected chunks',()=>{
 const guided=items.filter(x=>x.mode==='guided');assert.equal(guided.length,136);
 for(const x of guided){
  const v=sentenceCloze(x.modelAnswer,x.area,x.id);
  assert.ok(v.prompt.includes('_____')&&v.expected.trim(),x.id);
  assert.equal(v.prompt.replace('_____',v.expected),x.modelAnswer,x.id);
  assert.equal(assessSkillInput(x,v.expected,x.area).matched,true,x.id);
 }
});
test('nonmatches and free prose are not automatically declared ungrammatical',()=>{
 const wrong=assessSkillInput(items[0],'banana',items[0].area);
 assert.deepEqual({automatic:wrong.automatic,matched:wrong.matched},{automatic:true,matched:false});
 const free=items.find(x=>x.mode==='production');
 assert.deepEqual(assessSkillInput(free,'I made a different but valid sentence.',free.area),{submitted:true,automatic:false,matched:null,expected:free.modelAnswer});
 assert.equal(assessSkillInput(free,'  ',free.area).submitted,false);
});
test('wrong auto match cannot be recorded as correct without explicitly switching to self-assessment',()=>{
 const wrong=assessSkillInput(items[0],'banana',items[0].area);
 assert.throws(()=>prepareSkillReview(defaultProgress(),items[0],items[0].area,'good',wrong,5000));
 const alternative={...wrong,automatic:false,matched:null};
 assert.ok(prepareSkillReview(defaultProgress(),items[0],items[0].area,'good',alternative,5000).next.skillCards[items[0].id]);
});
test('failure to write storage never mutates original progress',()=>{
 const progress=defaultProgress();const old=JSON.stringify(progress);const answer=assessSkillInput(items[0],items[0].modelAnswer,items[0].area);
 assert.throws(()=>persistSkillReview(progress,items[0],items[0].area,'good',answer,{setItem(){throw Error('QuotaExceededError');}},Date.now()));
 assert.equal(JSON.stringify(progress),old);
});
test('successful durable review schedules next check, exports and merges without destroying old card IDs',()=>{
 const now=Date.now(),p=defaultProgress(),x=items[0];p.cards['old-vocab']={last:1000,reps:10};
 const answer=assessSkillInput(x,x.modelAnswer,x.area);
 let stored='';const next=persistSkillReview(p,x,x.area,'good',answer,{setItem(k,v){assert.equal(k,'ael-progress');stored=v;}},now);
 assert.deepEqual(JSON.parse(stored),next);assert.ok(next.skillCards[x.id].due>now);assert.equal(next.cards['old-vocab'].reps,10);
 assert.equal(skillsDue(data,next,now).length,0);
 const backup={app:'American English Lab',format:1,progress:next};
 const after=mergeProgress(p,backup);
 assert.ok(after.skillCards[x.id]);assert.ok(after.cards['old-vocab']);assert.equal(after.skillHistory.length,1);
 const twice=mergeProgress(after,backup);assert.equal(twice.skillHistory.length,1);
});
test('7 / 30 day retention only reports genuinely observed reference matches',()=>{
 const now=Date.now(),p=defaultProgress(),x=items[0],answer=assessSkillInput(x,x.modelAnswer,x.area);
 const first=prepareSkillReview(p,x,x.area,'good',answer,now-8*86400000).next;
 const second=prepareSkillReview(first,x,x.area,'good',answer,now).next;
 const sum=skillSummary(data,second,now);assert.equal(sum.practiced,1);
 assert.deepEqual(sum.windows.map(x=>[x.observed,x.rate]),[[1,100],[0,null]]);
});
