/** Publisher-hosted sources are not the same as bundled transcripts/audio. */
export function catalogStats(catalog, imported=[]){
 const ready=new Set(imported.map(x=>x.id));
 const full=catalog.filter(x=>ready.has(x.interactiveLessonId)).length;
 const linked=catalog.filter(x=>x.linkedQuizId&&!ready.has(x.interactiveLessonId)).length;
 return {sources:catalog.length,full,linked,quizEnabled:full+linked,sourceOnly:catalog.length-full-linked};
}
export function filterVoaCatalog(catalog,{filter='all',query='',page=0,pageSize=12}={}){
 const needle=query.toLocaleLowerCase('tr').trim();
 const found=catalog.filter(x=>{
  if(filter==='interactive'&&!x.interactiveLessonId&&!x.linkedQuizId)return false;
  if(filter==='imported'&&!x.interactiveLessonId)return false;
  if(filter==='linked'&&!x.linkedQuizId)return false;
  if(filter==='source'&&(x.interactiveLessonId||x.linkedQuizId))return false;
  if(filter==='level2'&&x.levelGroup!=='Level 2')return false;
  if(filter==='level1'&&x.levelGroup!=='Level 1')return false;
  if(needle&&!(x.title+' '+x.topic+' '+x.sourceSeries).toLocaleLowerCase('tr').includes(needle))return false;
  return true;
 });
 const pages=Math.max(1,Math.ceil(found.length/pageSize)),current=Math.max(0,Math.min(page,pages-1));
 return {items:found.slice(current*pageSize,(current+1)*pageSize),count:found.length,page:current,pages};
}
