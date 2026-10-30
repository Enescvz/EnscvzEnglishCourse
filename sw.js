// Private development build, release locked. Robotik eSpeak MP3 files quarantined and not bundled.
// External human-voice VOA streams require internet and are NOT cached by this worker.
const CACHE='ael-dev-20261030-final-candidate-lazy-v1';
const PREFIX='ael-dev-';
const CORE=['./','./index.html','./styles.css','./js/app.js','./js/content-loader.js','./js/sentence-skills.js','./js/fluency-studio.js','./js/fluency-ui.js','./js/engine.js','./js/catalog.js','./js/voa-catalog.js','./js/toefl-writing.js','./js/toefl-writing-exam.js','./js/toefl-prep.js','./js/rapid.js','./js/memory.js','./data/daily-expressions.json','./manifest.webmanifest','./assets/icon.svg','./data/rapid-vocabulary.json','./data/fluency-focus.json','./data/vocabulary.json','./data/phrasals.json','./data/toefl-academic.json','./data/toefl-core.json','./data/toefl-writing-practice.json','./data/toefl-reading-practice.json','./data/toefl-listening-practice.json','./data/episodes.json','./data/readings.json','./data/drills.json','./data/grammar.json','./data/sentence-skills.json','./data/fluency-studio.json','./data/authentic-listening.json','./data/voa-source-catalog.json','./data/voa-source-quizzes.json','./js/offline.js','./js/retention-audit.js','./js/toefl-human-review.js','./js/offline-device-qa.js','./js/human-audio-status.js','./js/progress-safety.js','./js/progress-integrity.js','./data/candidate-catalog.json'];
const BOOT=['./','./index.html','./styles.css','./js/app.js','./js/content-loader.js','./manifest.webmanifest','./assets/icon.svg',...CORE.filter(x=>x.startsWith('./js/')), './data/vocabulary.json','./data/phrasals.json','./data/toefl-academic.json','./data/rapid-vocabulary.json','./data/sentence-skills.json'];
const AUDIO=[]; // Legacy synthetic recordings are quarantined; never cached.
const resolved=path=>new URL(path,self.registration.scope).href;
async function coreStatus(){
 const cache=await caches.open(CACHE);
 const missing=[];
 for(const path of CORE){if(!await cache.match(resolved(path)))missing.push(path);}
 return {ready:missing.length===0,total:CORE.length,cached:CORE.length-missing.length,missing,cacheVersion:CACHE,
   audio:'No synthetic MP3 bundled; real human-voice VOA recordings require internet.'};
}
async function populateCore(){
 const cache=await caches.open(CACHE);
 // All required files must be cached. Failed update must not delete an older working cache.
 await cache.addAll(CORE.map(resolved));
 return coreStatus();
}
self.addEventListener('install',event=>event.waitUntil((async()=>{
 const cache=await caches.open(CACHE);
 await cache.addAll([...new Set(BOOT)].map(resolved));
 await self.skipWaiting();
})()));
self.addEventListener('activate',event=>event.waitUntil((async()=>{
 // Delete ONLY this application's previous versions; never unrelated origin caches.
 const keys=await caches.keys();
 await Promise.all(keys.filter(k=>k.startsWith(PREFIX)&&k!==CACHE).map(k=>caches.delete(k)));
 await self.clients.claim();
})()));
self.addEventListener('message',event=>{
 const type=event.data?.type;
 if(!['AEL_CACHE_STATUS','AEL_CACHE_REPAIR'].includes(type))return;
 event.waitUntil((async()=>{
  try{
   let state;
   if(type==='AEL_CACHE_REPAIR')state=await populateCore();
   else state=await coreStatus();
   event.ports?.[0]?.postMessage({ok:true,...state});
  }catch(error){
   event.ports?.[0]?.postMessage({ok:false,error:String(error),...await coreStatus().catch(()=>({ready:false}))});
  }
 })());
});
async function mediaResponse(request,cached){
 const range=request.headers.get('range');
 if(!range)return cached;
 const bytes=await cached.arrayBuffer();
 const match=/^bytes=(\d+)-(\d*)$/.exec(range.trim());
 if(!match)return new Response(null,{status:416,headers:{'Content-Range':`bytes */${bytes.byteLength}`}});
 const start=Number(match[1]);
 const end=match[2]?Math.min(Number(match[2]),bytes.byteLength-1):bytes.byteLength-1;
 if(start>=bytes.byteLength||start>end)return new Response(null,{status:416,headers:{'Content-Range':`bytes */${bytes.byteLength}`}});
 return new Response(bytes.slice(start,end+1),{status:206,headers:{'Content-Type':'audio/mpeg','Accept-Ranges':'bytes','Content-Range':`bytes ${start}-${end}/${bytes.byteLength}`,'Content-Length':String(end-start+1)}});
}
self.addEventListener('fetch',event=>{
 const request=event.request;
 if(request.method!=='GET'||new URL(request.url).origin!==self.location.origin)return;
 event.respondWith((async()=>{
  const url=new URL(request.url);
  const cache=await caches.open(CACHE);
  const isAudio=url.pathname.endsWith('.mp3');
  // CacheStorage matches URL and query by default. Versioned/app deep links fall back to index.html.
  const cached=await cache.match(request,{ignoreSearch:true});
  if(cached){return isAudio?mediaResponse(request,cached):cached;}
  if(request.mode==='navigate'){
   try{
    const response=await fetch(request);
    if(response.ok)return response;
   }catch(error){}
   return await cache.match(resolved('./index.html'))||await cache.match(resolved('./'))||new Response('Offline app shell not installed',{status:503});
  }
  try{
   const response=await fetch(request);
   // Never put a partial range response or a third-party stream into CacheStorage.
   if(response.status===200&&response.ok&&url.pathname.startsWith(new URL(self.registration.scope).pathname)){
    event.waitUntil(cache.put(request,response.clone()).catch(()=>{}));
   }
   return response;
  }catch(error){
   return new Response('Offline resource not cached',{status:503,headers:{'Content-Type':'text/plain; charset=utf-8'}});
  }
 })());
});
