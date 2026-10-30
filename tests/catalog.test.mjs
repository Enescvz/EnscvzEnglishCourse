import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import {filterCandidates} from '../js/catalog.js';
const data=JSON.parse(await fs.readFile(new URL('../data/candidate-catalog.json',import.meta.url),'utf8'));
test('complete source inventory, no invented phrasal CEFR',()=>{
 assert.equal(data.entries.length,4851);
 assert.equal(new Set(data.entries.map(e=>e.t+e.w)).size,4851);
 assert.equal(data.entries.filter(e=>e.t==='p').length,1204);
 assert.ok(data.entries.filter(e=>e.t==='p').every(e=>e.l===null));
 assert.equal(data.meta.lessonOverlaps,data.entries.filter(e=>Boolean(e.lesson)).length);
});
test('catalog filters and pagination do not mutate original corpus',()=>{
 const count=data.entries.length;
 const b2=filterCandidates(data.entries,{kind:'v',level:'B2'});
 assert.ok(b2.count>2000);assert.ok(b2.items.every(e=>e.t==='v'&&e.l==='B2'));
 const phrasals=filterCandidates(data.entries,{kind:'p',level:'all'});
 assert.equal(phrasals.count,1204);
 const missing=filterCandidates(data.entries,{availability:'unmade'});
 assert.equal(missing.count,4851-data.meta.lessonOverlaps);
 const first=filterCandidates(data.entries,{query:'comply'});
 assert.ok(first.items.some(e=>e.w==='comply'));
 const last=filterCandidates(data.entries,{page:999999});
 assert.equal(last.page,last.pageCount-1);
 assert.equal(data.entries.length,count);
});
