import test from 'node:test';import assert from 'node:assert/strict';import {readFileSync} from 'node:fs';
import {validateFluencyData,humanSources,dictationTargets,compareDictation,writingAudit,errorReport,adaptivePlan,persistFluencyReview,persistFluencyDraft} from '../js/fluency-studio.js';
import {defaultProgress} from '../js/engine.js';import {mergeProgress} from '../js/progress-safety.js';
const content=JSON.parse(readFileSync(new URL('../data/fluency-studio.json',import.meta.url)));
const voa=JSON.parse(readFileSync(new URL('../data/authentic-listening.json',import.meta.url)));
test('12 original branching scenarios, 36 decisions, 24 thinking, 12 writing with stable noncolliding IDs',()=>{
 assert.deepEqual(validateFluencyData(content),{scenarios:12,decisions:36,thinking:24,writing:12});
 assert.equal(content.meta.audioBundled,false);assert.equal(content.meta.autoEssayScoring,false);
 for(const s of content.realLife)for(const step of s.steps)assert.ok(step.options[step.correct].length>10);
});
test('30 genuine-source references reused; transcripts not mislabeled as independently audio checked',()=>{
 const src=humanSources(voa),targets=dictationTargets(voa);assert.equal(src.length,30);assert.ok(targets.length>=30);
 assert.ok(targets.every(t=>src.some(s=>s.id===t.sourceId&&s.turns[t.turnIndex]?.text.trim().replace(/\s+/g,' ')===t.target)));
 assert.ok(src.every(s=>s.offlineReady===false&&s.transcriptVerifiedAgainstAudio===false));
 assert.ok(targets.every(t=>t.target.split(/\s+/).length>=7));
});
test('dikte edit distance handles missing words, punctuation, insertions and zero input',()=>{
 assert.equal(compareDictation('I have arrived.','I have arrived!').accuracy,100);
 assert.equal(compareDictation('I arrived','I have arrived').accuracy,67);
 assert.equal(compareDictation('I have just arrived','I have arrived').accuracy,75);
 assert.equal(compareDictation('   ','I have arrived').submitted,false);
});
test('writing coach only exposes countable surface metrics; no fabricated essay score',()=>{
 const x=writingAudit('Although it was raining, we went outside.\n\nWe enjoyed the walk because it was quiet.',content.writing[0]);
 assert.equal(x.paragraphs,2);assert.equal(x.connectors,2);assert.equal(x.withinSuggestedRange,false);
 assert.ok(x.disclaimer.includes('puanı ölçülmez'));assert.equal('score' in x,false);
});
test('storage failure never commits fluency review or writing draft; old vocab remains intact',()=>{
 const p=defaultProgress();p.cards['original-card']={reps:3,last:100};const before=JSON.stringify(p);
 const fail={setItem(){throw Error('QuotaExceededError')}};
 assert.throws(()=>persistFluencyReview(p,{id:'rl-hotel-1',type:'realLife',category:'hotel',grade:'good'},fail));
 assert.throws(()=>persistFluencyDraft(p,'write-email','draft',fail));assert.equal(JSON.stringify(p),before);
});
test('no listening credit without explicit self-report; durable review and draft merge into backup',()=>{
 const p=defaultProgress(),storage={value:'',setItem(k,v){assert.equal(k,'ael-progress');this.value=v;}};
 assert.throws(()=>persistFluencyReview(p,{id:'dict-1',type:'dictation',category:'dictation',grade:'good',requiresAudio:true,listened:false},storage));
 assert.equal(storage.value,'');
 const a=persistFluencyReview(p,{id:'dict-1',type:'dictation',category:'dictation',grade:'hard',accuracy:60,requiresAudio:true,listened:true},storage,1720000000000);
 assert.equal(a.fluencyHistory[0].audioVerified,false);assert.ok(a.fluencyCards['dict-1'].due>1720000000000);
 const b=persistFluencyDraft(a,'write-email','My email draft.',storage,1720000001000);
 const old={...defaultProgress(),cards:{preserve:{at:1,last:1}}};const merged=mergeProgress(old,{app:'American English Lab',format:1,progress:b});
 assert.equal(merged.fluencyDrafts['write-email'].text,'My email draft.');assert.equal(merged.fluencyHistory.length,1);assert.ok(merged.cards.preserve);
 assert.equal(mergeProgress(merged,{app:'American English Lab',format:1,progress:b}).fluencyHistory.length,1);
});
test('error analytics and adaptive minutes are based only on observed answers',()=>{
 const p=defaultProgress();const start=adaptivePlan(p,Date.now(),30);assert.equal(start.minutes,30);assert.equal(start.items.reduce((n,x)=>n+x.mins,0),30);assert.equal(errorReport(p).attempts,0);
 const h=persistFluencyReview(p,{id:'rl-hotel-1',type:'realLife',category:'hotel',grade:'again'}, {setItem(){}},Date.now());
 assert.equal(errorReport(h).groups[0].category,'hotel');assert.equal(errorReport(h).attempts,1);
 assert.ok(adaptivePlan(h).items.some(x=>x.tab==='errors'));
});
