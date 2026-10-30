import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {filterVoaCatalog,catalogStats} from '../js/voa-catalog.js';
const root=new URL('../data/',import.meta.url);
const src=JSON.parse(readFileSync(new URL('voa-source-catalog.json',root)));
const lessons=JSON.parse(readFileSync(new URL('authentic-listening.json',root)));
test('VOA has 50 publisher sources, 30 imported-transcript lessons and 20 linked quizzes',()=>{
 assert.deepEqual(catalogStats(src,lessons),{sources:50,full:30,linked:20,quizEnabled:50,sourceOnly:0});
});
test('filter preserves source vs completed lesson statuses',()=>{
 assert.equal(filterVoaCatalog(src,{filter:'interactive'}).count,50);
 assert.equal(filterVoaCatalog(src,{filter:'imported'}).count,30);
 assert.equal(filterVoaCatalog(src,{filter:'linked'}).count,20);
 assert.equal(filterVoaCatalog(src,{filter:'source'}).count,0);
 assert.equal(filterVoaCatalog(src,{filter:'level2'}).count,30);
 assert.equal(filterVoaCatalog(src,{filter:'level1'}).count,20);
});
test('searches Turkish-agnostic title, topic and paginates without skipping',()=>{
 assert.equal(filterVoaCatalog(src,{query:'Interview'}).count,1);
 const all=Array.from({length:5},(_,i)=>filterVoaCatalog(src,{page:i,pageSize:12}).items).flat();
 assert.equal(all.length,50);assert.equal(new Set(all.map(x=>x.id)).size,50);
 assert.equal(filterVoaCatalog(src,{page:999,pageSize:12}).items.length,2);
});
