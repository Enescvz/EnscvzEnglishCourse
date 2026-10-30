/** Development-only bilingual rapid deck. These are NOT context-complete lessons. */
export function normalizeRapidDeck(cards,fullLessons=[]) {
  const existing=new Set(fullLessons.filter(x=>x.category==='general').map(x=>x.word.toLocaleLowerCase('en-US')));
  const seen=new Set();
  return cards.filter(x=>{
    const word=String(x.word||'').toLocaleLowerCase('en-US').trim();
    if(!word||!String(x.tr||'').trim()||!['B2','C1'].includes(x.level)||existing.has(word)||seen.has(word))return false;
    seen.add(word);return true;
  });
}
export function rapidDue(cardState,now=Date.now()){
  return !!cardState && Number(cardState.dueAt||0)<=now;
}
export function rapidFiltered(cards,{query='',level='all',status='all',page=0,pageSize=25}={},progress={},now=Date.now()){
  const q=String(query).trim().toLocaleLowerCase('tr');
  const items=cards.filter(x=> (level==='all'||x.level===level) &&
   (!q||x.word.toLocaleLowerCase('tr').includes(q)||x.tr.toLocaleLowerCase('tr').includes(q)) &&
   (status==='all'||(status==='new'?!progress[x.id]:status==='due'?rapidDue(progress[x.id],now):!!progress[x.id])));
  const pages=Math.max(1,Math.ceil(items.length/pageSize));
  const selectedPage=Math.max(0,Math.min(pages-1,Math.floor(Number(page)||0)));
  return {items:items.slice(selectedPage*pageSize,(selectedPage+1)*pageSize),total:items.length,page:selectedPage,pages};
}
/** Lightweight rapid recognition schedule; NOT full FSRS mastery. */
export function rapidRecord(previous,known,now=Date.now()) {
  const record=previous||{seen:0,correct:0,streak:0};
  const streak=known?Math.min((record.streak||0)+1,8):0;
  const days=[0,1,3,7,14,30,60,90];
  return {seen:(record.seen||0)+1,correct:(record.correct||0)+(known?1:0),streak,
    reviewedAt:now,dueAt:now+(known?days[streak]*86400000:600000),
    // A bilingual recognition success must not be counted as productive mastery.
    lastAnswer:known?'remembered':'missed'};
}
