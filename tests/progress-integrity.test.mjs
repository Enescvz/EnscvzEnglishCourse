import test from 'node:test';
import assert from 'node:assert/strict';
import {loadProgressRecord} from '../js/progress-integrity.js';
import {defaultProgress} from '../js/engine.js';
const defaults=()=>defaultProgress();
test('first-time user starts with version 1 without recovery lock',()=>{
 const r=loadProgressRecord(null,defaults());
 assert.equal(r.issue,null);assert.equal(r.protectedRaw,null);assert.equal(r.progress.version,1);
});
test('old progress keeps card IDs, all existing history and defaults missing keys',()=>{
 const p={version:1,cards:{'legacy-id':{attempts:15,due:123}},phrasals:{},settings:{minutes:15},events:[{at:12,type:'memory'}],personalTag:'old-user'};
 const r=loadProgressRecord(JSON.stringify(p),defaults());
 assert.equal(r.progress.cards['legacy-id'].attempts,15);
 assert.equal(r.progress.personalTag,'old-user');assert.equal(r.progress.settings.theme,'dark');
 assert.equal(r.progress.events[0].type,'memory');assert.equal(r.issue,null);
});
test('unparseable progress is protected rather than silently erased',()=>{
 const raw='{"version":1,"cards":{';const r=loadProgressRecord(raw,defaults());
 assert.equal(r.protectedRaw,raw);assert.ok(r.issue.includes('Kayıt okunamadı'));
 assert.deepEqual(r.progress.cards,{});
});
test('future unknown progress version is protected, not migrated destructively',()=>{
 const raw=JSON.stringify({version:2,cards:{x:{attempts:8}}});
 const r=loadProgressRecord(raw,defaults());assert.equal(r.protectedRaw,raw);
});
test('malformed nested collections are protected, not normalized to empty maps',()=>{
 for(const p of [{version:1,cards:[],settings:{}},{version:1,phrasals:{},events:'bad'},{version:1,dateLog:5}]){
  const raw=JSON.stringify(p);assert.equal(loadProgressRecord(raw,defaults()).protectedRaw,raw);
 }
});
test('prototype injection fields cannot be loaded into progress maps',()=>{
 const raw='{"version":1,"cards":{"__proto__":{"polluted":true},"safe":{"attempts":2}},"settings":{"__proto__":{"polluted":true},"theme":"light"}}';
 const r=loadProgressRecord(raw,defaults());assert.equal(r.progress.cards.safe.attempts,2);
 assert.equal(Object.hasOwn(r.progress.cards,'__proto__'),false);assert.equal(Object.hasOwn(r.progress.settings,'__proto__'),false);
 assert.equal(Object.prototype.polluted,undefined);
});
