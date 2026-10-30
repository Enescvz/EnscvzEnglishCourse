// Split the startup data pack from large, optional lessons. No card IDs are transformed.
export const CONTENT_FILES=Object.freeze({
 vocabulary:'vocabulary',phrasals:'phrasals',toeflAcademic:'toefl-academic',rapid:'rapid-vocabulary',sentenceSkills:'sentence-skills',
 focus:'fluency-focus',expressions:'daily-expressions',authentic:'authentic-listening',voaLinkedQuizzes:'voa-source-quizzes',voaCatalog:'voa-source-catalog',
 readings:'readings',episodes:'episodes',drills:'drills',grammar:'grammar',toeflCore:'toefl-core',toeflWriting:'toefl-writing-practice',
 toeflReading:'toefl-reading-practice',toeflListening:'toefl-listening-practice',fluency:'fluency-studio'
});
export const INITIAL_KEYS=Object.freeze(['vocabulary','phrasals','toeflAcademic','rapid','sentenceSkills']);
export const VIEW_KEYS=Object.freeze({
 home:[],vocabulary:['toeflCore'],phrasals:['toeflCore'],sentenceSkills:[],listening:['authentic','voaLinkedQuizzes'],
 podcasts:['episodes'],authentic:['authentic','voaLinkedQuizzes','voaCatalog'],reading:['readings','toeflReading'],grammar:['grammar'],
 speaking:[],writing:['toeflWriting'],toefl:['toeflCore','toeflWriting','toeflReading','toeflListening'],
 conversations:['episodes'],pronunciation:[],tests:[],review:[],analytics:[],
 settings:['authentic','voaLinkedQuizzes','readings'],catalog:[],rapid:[],
 expressions:['expressions'],memory:['focus','expressions','toeflCore'],fluencyStudio:['fluency','authentic','voaLinkedQuizzes']
});
export function createContentLoader(fetchFn){
 const cache=new Map();const inFlight=new Map();
 async function loadOne(key){
  if(!Object.hasOwn(CONTENT_FILES,key))throw Error('Bilinmeyen içerik: '+key);
  if(cache.has(key))return cache.get(key);
  if(inFlight.has(key))return inFlight.get(key);
  const promise=(async()=>{
   const res=await fetchFn('data/'+CONTENT_FILES[key]+'.json');
   if(!res.ok)throw Error(CONTENT_FILES[key]+'.json yüklenemedi ('+res.status+')');
   const payload=await res.json();
   if(!payload||typeof payload!=='object')throw Error('Geçersiz ders verisi: '+key);
   cache.set(key,payload);return payload;
  })();
  inFlight.set(key,promise);
  try{return await promise;}finally{inFlight.delete(key);}
 }
 return {
  ready(keys){return keys.every(k=>cache.has(k));},
  async load(keys){const values=await Promise.all(keys.map(loadOne));return Object.fromEntries(keys.map((key,i)=>[key,values[i]]));},
  loadedKeys(){return [...cache.keys()];}
 };
}
