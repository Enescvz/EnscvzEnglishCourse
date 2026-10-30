import test from 'node:test';
import assert from 'node:assert/strict';
import {mergeProgress,validateProgressBackup} from '../js/progress-safety.js';
const item=(last,attempts)=>({last,attempts,due:last+86400000,fsrsVersion:5,stability:2,difficulty:3});
const baseline=()=>({version:1,cards:{'old-id':item(200,5),'untouched-id':item(300,7)},phrasals:{'p-1':item(500,3)},settings:{minutes:30,theme:'dark'},dateLog:{'2026-10-29':12},events:[{at:42,type:'review'},{at:42,type:'review'}],quizHistory:[],toeflAttempts:[{at:300,correct:8}],rapidCards:{'r-1':{attempts:2}},writing:{'w-1':{at:500,text:'my essay'}},memoryCues:{'m-1':'my cue'}});
const wrap=p=>({app:'American English Lab',format:1,progress:p});
test('older backup does not roll back FSRS or erase current card IDs',()=>{
 const current=baseline();const backup=baseline();backup.cards['old-id']=item(100,1);delete backup.cards['untouched-id'];backup.cards['new-id']=item(150,1);backup.phrasals={};
 const merged=mergeProgress(current,wrap(backup));
 assert.equal(merged.cards['old-id'].attempts,5);assert.equal(merged.cards['untouched-id'].attempts,7);
 assert.equal(merged.cards['new-id'].attempts,1);assert.equal(merged.phrasals['p-1'].attempts,3);
 assert.equal(merged.memoryCues['m-1'],'my cue');assert.equal(merged.writing['w-1'].text,'my essay');
});
test('newer card state imports without deleting other progress',()=>{
 const merged=mergeProgress(baseline(),wrap({...baseline(),cards:{'old-id':item(900,10)}}));
 assert.equal(merged.cards['old-id'].attempts,10);assert.ok(merged.cards['untouched-id']);
});
test('re-import is idempotent, but existing identical valid history records are preserved',()=>{
 const current=baseline();const backup={...baseline(),events:[{at:42,type:'review'},{at:42,type:'review'},{at:43,type:'review'}]};
 const once=mergeProgress(current,wrap(backup));const twice=mergeProgress(once,wrap(backup));
 assert.equal(once.events.length,3);assert.equal(twice.events.length,3);
 assert.equal(twice.dateLog['2026-10-29'],12);
});
test('strict shape validation rejects malformed and prototype-polluting backups',()=>{
 assert.throws(()=>validateProgressBackup({app:'Other',format:1,progress:baseline()}));
 assert.throws(()=>mergeProgress(baseline(),wrap({...baseline(),cards:[]})));
 const malicious=JSON.parse('{"app":"American English Lab","format":1,"progress":{"version":1,"settings":{},"cards":{"__proto__":{"polluted":true},"new":{}},"phrasals":{}}}');
 const merged=mergeProgress(baseline(),malicious);
 assert.equal(Object.prototype.polluted,undefined);assert.equal(merged.cards['__proto__'],Object.prototype);
 assert.ok(merged.cards['untouched-id']);
});
test('active writing and reading attempts preserve later session and its answers',()=>{
 const current={...baseline(),toeflActiveReading:{startedAt:800,answers:{q1:2}}};
 const incoming={...baseline(),toeflActiveReading:{startedAt:700,answers:{q1:0}},toeflActiveWriting:{startedAt:600,answers:{x:'essay'}}};
 const merged=mergeProgress(current,wrap(incoming));
 assert.equal(merged.toeflActiveReading.answers.q1,2);
 assert.equal(merged.toeflActiveWriting.answers.x,'essay');
});
