import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
const ROOT=fileURLToPath(new URL('../',import.meta.url));
const origin='https://offline-test.invalid';
const code=readFileSync(new URL('../sw.js',import.meta.url),'utf8');

function setup(){
 const handlers={},cacheData=new Map(),allCaches=new Map();let networkCalls=0,online=false,forcedFailure=false;
 function key(path){return typeof path==='string'?path:path.url;}
 function store(cacheKey){if(!allCaches.has(cacheKey))allCaches.set(cacheKey,new Map());return allCaches.get(cacheKey);}
 function fromDisk(path){const u=new URL(key(path),origin),rel=u.pathname.substring(1)||'index.html';assert.ok(!rel.includes('..'));
  assert.ok(existsSync(ROOT+rel),`Missing SW precache: ${rel}`);return new Response(readFileSync(ROOT+rel));}
 const caches={
  async open(cacheKey){const storage=store(cacheKey);return {
    async addAll(paths){if(forcedFailure)throw Error('network interrupted');for(const path of paths){storage.set(key(path),fromDisk(path));}},
    async put(path,response){storage.set(key(path),response);},
    async match(path){const result=storage.get(key(path));return result?.clone();}
  };},
  async keys(){return [...allCaches.keys()];},
  async delete(cacheKey){return allCaches.delete(cacheKey);}
 };
 const self={location:{origin},registration:{scope:origin+'/'},addEventListener(type,fn){handlers[type]=fn;},skipWaiting:async()=>{},clients:{claim:async()=>{}}};
 const fetch=async()=>{networkCalls++;throw Error('network disabled');};
 vm.runInNewContext(code,{self,caches,Response,URL,console,fetch});
 const simulate=async(type,request,channel)=>{let task;
  const event={request,data:request,ports:channel?[{postMessage:msg=>channel.push(msg)}]:[],waitUntil(p){task=p;},respondWith(p){task=p;}};
  handlers[type](event);assert.ok(task,`no task for ${type}`);return await task;};
 return {simulate,allCaches,store,caches,get networkCalls(){return networkCalls;},setFailure(v){forcedFailure=v;}};
}

test('boot shell installs offline; full offline pack needs explicit repair',async()=>{
 const c=setup();await c.simulate('install');
 const messages=[];await c.simulate('message',{type:'AEL_CACHE_STATUS'},messages);
 assert.equal(messages[0].ready,false);assert.ok(messages[0].cached>=5);
 const after=[];await c.simulate('message',{type:'AEL_CACHE_REPAIR'},after);
 assert.equal(after[0].ready,true);assert.equal(after[0].cached,after[0].total);assert.ok(after[0].cached>=30);
 for(const path of ['/', '/index.html','/js/app.js','/js/offline.js','/data/candidate-catalog.json','/data/toefl-reading-practice.json','/data/voa-source-quizzes.json']){
  const result=await c.simulate('fetch',new Request(origin+path));assert.equal(result.status,200,path);assert.ok((await result.arrayBuffer()).byteLength>0);
 }
 assert.equal(c.networkCalls,0);
});

test('no synthetic audio downloads or offline caching; stale caches are removed on activate',async()=>{
 const c=setup();await c.simulate('install');const messages=[];
 await c.simulate('message',{type:'AEL_CACHE_STATUS'},messages);
 assert.equal(messages[0].ready,false);assert.match(messages[0].audio,/No synthetic MP3/);
 c.store('ael-dev-previous').set(origin+'/assets/audio/drill-connected-1.mp3',new Response('legacy robot audio'));
 await c.simulate('activate');assert.equal(c.allCaches.has('ael-dev-previous'),false);
 const url=origin+'/assets/audio/drill-connected-1.mp3';
 const response=await c.simulate('fetch',new Request(url));
 assert.equal(response.status,503);assert.equal(c.networkCalls,1);
});

test('offline navigation fallback and scoped cache activation preserve unrelated caches',async()=>{
 const c=setup();await c.simulate('install');
 c.store('ael-dev-previous').set(origin+'/old',new Response('old'));
 c.store('shared-site-cache').set(origin+'/other',new Response('other'));
 await c.simulate('activate');
 assert.deepEqual([...c.allCaches.keys()].filter(x=>x==='shared-site-cache'),['shared-site-cache']);
 assert.equal(c.allCaches.has('ael-dev-previous'),false);
 const result=await c.simulate('fetch',{url:origin+'/lessons/abc',method:'GET',mode:'navigate',headers:new Headers()});
 assert.equal(result.status,200);assert.match(await result.text(),/American English Lab/);
});

test('partial cache loss is reported and repair without disturbing user data',async()=>{
 const c=setup();await c.simulate('install');
 const first=[];await c.simulate('message',{type:'AEL_CACHE_STATUS'},first);
 const key=first[0].cacheVersion;
 c.store(key).delete(origin+'/data/vocabulary.json');
 const broken=[];await c.simulate('message',{type:'AEL_CACHE_STATUS'},broken);
 assert.equal(broken[0].ready,false);
 assert.ok(broken[0].missing.includes('./data/vocabulary.json'));
 const fixed=[];await c.simulate('message',{type:'AEL_CACHE_REPAIR'},fixed);
 assert.equal(fixed[0].ready,true);
 c.setFailure(true);c.store(key).delete(origin+'/data/grammar.json');
 const failed=[];await c.simulate('message',{type:'AEL_CACHE_REPAIR'},failed);
 assert.equal(failed[0].ok,false);assert.equal(failed[0].ready,false);
});
