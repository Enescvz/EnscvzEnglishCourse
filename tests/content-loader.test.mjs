import test from 'node:test';
import assert from 'node:assert/strict';
import {createContentLoader,INITIAL_KEYS,VIEW_KEYS,CONTENT_FILES} from '../js/content-loader.js';

test('startup requests only the minimal data pack, not every lesson',async()=>{
 const calls=[];const loader=createContentLoader(async url=>{calls.push(url);return {ok:true,json:async()=>({id:url})};});
 await loader.load(INITIAL_KEYS);
 assert.equal(calls.length,5);
 assert.equal(calls.includes('data/authentic-listening.json'),false);
 assert.equal(calls.includes('data/voa-source-quizzes.json'),false);
 assert.equal(calls.includes('data/fluency-studio.json'),false);
 assert.equal(calls.includes('data/daily-expressions.json'),false);
 assert.equal(loader.ready(INITIAL_KEYS),true);
});
test('overlapping pages reuse the same in-flight request and preserve original objects',async()=>{
 let count=0;
 const loader=createContentLoader(async url=>{count++;await new Promise(resolve=>setTimeout(resolve,10));return {ok:true,json:async()=>({id:'original',url})};});
 const [a,b]=await Promise.all([loader.load(['authentic','voaLinkedQuizzes']),loader.load(['authentic'])]);
 assert.equal(count,2);
 assert.equal(a.authentic,b.authentic);
 const c=await loader.load(['authentic']);assert.equal(c.authentic,b.authentic);assert.equal(count,2);
});
test('failed optional data is never cached and can be retried without losing good data',async()=>{
 let n=0;const loader=createContentLoader(async url=>({ok:url.includes('readings')?++n>1:true,status:503,json:async()=>({rows:[]})}));
 await assert.rejects(loader.load(['readings']),/yüklenemedi/);
 assert.equal(loader.ready(['readings']),false);
 await loader.load(['readings']);assert.equal(loader.ready(['readings']),true);assert.equal(n,2);
});
test('every navigation view has a defined data dependency list',()=>{
 for(const name of ['home','listening','vocabulary','phrasals','expressions','fluencyStudio','sentenceSkills','podcasts','authentic','reading','grammar','speaking','writing','toefl','conversations','pronunciation','tests','review','analytics','settings','catalog','rapid','memory']){
  assert.ok(Array.isArray(VIEW_KEYS[name]),name);
  for(const item of VIEW_KEYS[name])assert.ok(CONTENT_FILES[item],name+':'+item);
 }
});
