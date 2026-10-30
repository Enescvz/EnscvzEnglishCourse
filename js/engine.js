// A transparent, tested adaptive interval scheduler. Not FSRS.
export const LEVELS = ['Yeni','Öğreniliyor','Tanınıyor','Hatırlanıyor','Aktif kullanılabiliyor','Pekişmiş','Tekrar gerekli'];
export const MS_DAY = 86400000;
export function normalize(s='') { return String(s).toLocaleLowerCase('en-US').trim().normalize('NFKD').replace(/[\u0300-\u036f]/g,'').replace(/[’']/g,"'").replace(/[^a-z0-9' ]/g,'').replace(/\s+/g,' '); }
export function words(s='') { return normalize(s).split(' ').filter(Boolean); }
export function accuracy(answer, target) {
 const a=words(answer), b=words(target);
 if (!b.length) return 0;
 let dp=Array.from({length:a.length+1},()=>new Array(b.length+1).fill(0));
 for(let i=1;i<=a.length;i++) for(let j=1;j<=b.length;j++) dp[i][j]=a[i-1]===b[j-1]?dp[i-1][j-1]+1:Math.max(dp[i-1][j],dp[i][j-1]);
 return Math.round(100*dp[a.length][b.length]/Math.max(a.length,b.length));
}
// Align words in their spoken order. A bag-of-words comparison incorrectly
// marks reordered dictation ("dog bites man" vs "man bites dog") as correct.
export function diffWords(answer,target) {
 const a=words(answer), b=words(target);
 const dp=Array.from({length:a.length+1},()=>Array(b.length+1).fill(0));
 for(let i=a.length-1;i>=0;i--)for(let j=b.length-1;j>=0;j--)
   dp[i][j]=a[i]===b[j]?1+dp[i+1][j+1]:Math.max(dp[i+1][j],dp[i][j+1]);
 const matched=new Set();let i=0,j=0;
 while(i<a.length&&j<b.length){
   if(a[i]===b[j]){matched.add(j);i++;j++;}
   else if(dp[i+1][j]>=dp[i][j+1])i++;else j++;
 }
 return b.map((w,k)=>({word:w,ok:matched.has(k)}));
}
// Observational diagnosis only. No claim about a learner's hidden cognitive causes.
// Correct/incorrect word sequence is measurable; whether the word has been
// retrieved successfully in another mode is observable from local history.
export function analyzeDictation(answer, target, vocabulary=[], knownCards={}) {
 const result=diffWords(answer,target);
 const missed=result.filter(x=>!x.ok).map(x=>x.word);
 const dictionary=new Map(vocabulary.filter(x=>!x.word.includes(' ')).map(x=>[normalize(x.word),x]));
 const independentlyRecalled=[];
 for(const w of new Set(missed)) {
   const item=dictionary.get(w);
   if(item && (knownCards[item.id]?.modeSuccess?.recall||0)>0)
     independentlyRecalled.push(w);
 }
 return {
  accuracy:accuracy(answer,target),
  missedWords:missed,
  previouslyRecalledButMissed:independentlyRecalled,
  observation:independentlyRecalled.length
   ?'Önceki kelime hatırlama çalışmasında doğru bildiğin bazı ifadeler bu dinlemede eksik kaldı. Bu tek başına bir dinleme güçlüğünün nedenini kanıtlamaz.'
   :'Bu alıştırmada eşleşmeyen kelimeler var. Hatanın nedeni yalnızca yazılı yanıtından belirlenemez.'
 };
}
export function defaultProgress(){return {version:1,cards:{},phrasals:{},expressions:{},lessons:{},listenHistory:[],quizHistory:[],events:[],writing:{},skillCards:{},skillHistory:[],settings:{minutes:60,goal:10,theme:'dark',dailyMinutes:20},dateLog:{},reviewHistory:[]};}
// FSRS-5, public default weights (open-spaced-repetition/awesome-fsrs wiki,
// "The Algorithm", FSRS-5, edited 2026-07-28). No user-specific optimizer.
// Memory state: stability in days, difficulty in [1,10], retrievability in [0,1].
// Existing progress (without FSRS state) is migrated conservatively on next review.
export const FSRS_VERSION = 5;
export const FSRS_WEIGHTS = Object.freeze([
  0.40255,1.18385,3.173,15.69105,7.1949,0.5345,1.4604,0.0046,
  1.54575,0.1192,1.01925,1.9395,0.11,0.29605,2.2698,0.2315,
  2.9898,0.51655,0.6621
]);
export const DESIRED_RETENTION = 0.90;
const FSRS_DECAY = -0.5, FSRS_FACTOR = 19/81;
const clip = (x,lo,hi)=>Math.max(lo,Math.min(hi,x));
const grades={again:1,hard:2,good:3,easy:4};
export function fsrsRetrievability(elapsedDays,stability){
  if(!Number.isFinite(stability)||stability<=0)throw Error('Stability must be positive');
  return (1+FSRS_FACTOR*Math.max(0,elapsedDays)/stability)**FSRS_DECAY;
}
export function fsrsInterval(stability,retention=DESIRED_RETENTION){
  if(!Number.isFinite(stability)||stability<=0||retention<=0||retention>=1)throw Error('Invalid FSRS inputs');
  return clip(stability/FSRS_FACTOR*(retention**(1/FSRS_DECAY)-1),1/1440,36500);
}
export function fsrsInitialDifficulty(grade){
  if(![1,2,3,4].includes(grade))throw Error('Invalid FSRS grade');
  const w=FSRS_WEIGHTS;
  return clip(w[4]-Math.exp(w[5]*(grade-1))+1,1,10);
}
export function fsrsState(old={},grade,now=Date.now()){
  const g=grades[grade], w=FSRS_WEIGHTS;
  if(!g)throw Error('Invalid review grade');
  const hasPrevious=old.attempts>0 && Number.isFinite(old.last) && old.last<=now;
  const legacy=hasPrevious && !(old.fsrsVersion===FSRS_VERSION&&old.stability>0&&old.difficulty>0);
  const S=hasPrevious?(legacy?clip(old.interval||1,0.1,36500):old.stability):null;
  const D=hasPrevious?(legacy?5:old.difficulty):null;
  let stability,difficulty;
  if(!hasPrevious){
    stability=w[g-1];
    difficulty=fsrsInitialDifficulty(g);
  }else{
    const elapsedDays=Math.max(0,(now-old.last)/MS_DAY);
    const R=fsrsRetrievability(elapsedDays,S);
    const damped=D-w[6]*(g-3)*(10-D)/9;
    difficulty=clip(w[7]*fsrsInitialDifficulty(4)+(1-w[7])*damped,1,10);
    if(g===1){
      stability=w[11]*difficulty**(-w[12])*((S+1)**w[13]-1)*Math.exp(w[14]*(1-R));
    }else if(elapsedDays<1){
      stability=Math.max(S,S*Math.exp(w[17]*(g-3+w[18])));
    }else{
      const hard=g===2?w[15]:1, easy=g===4?w[16]:1;
      stability=S*(1+Math.exp(w[8])*(11-difficulty)*S**(-w[9])*(Math.exp(w[10]*(1-R))-1)*hard*easy);
    }
  }
  stability=clip(stability,0.01,36500);
  // Failed cards need an in-session 15 minute learning step. The FSRS memory
  // state is stored separately; this short step is not a 90% retention forecast.
  const interval=g===1?15/1440:fsrsInterval(stability);
  return {fsrsVersion:FSRS_VERSION,stability,difficulty,interval,
          due:now+Math.ceil(interval*MS_DAY),last:now};
}
export function reviewItem(old={}, grade, mode='recall', now=Date.now()) {
  if(!Object.hasOwn(grades,grade))throw Error('Invalid review grade');
  const p={...old,...fsrsState(old,grade,now)};
  p.attempts=(old.attempts||0)+1;
  p.reps=grade==='again'?0:(old.reps||0)+1;
  if(grade==='again'){
    p.lapses=(old.lapses||0)+1;
    p.status='Tekrar gerekli';
    // Previously successful modes do not count as current demonstrated mastery.
    p.modeSuccess={};
  }else{
    p.modeSuccess={...(old.modeSuccess||{})};
    p.modeSuccess[mode]=(p.modeSuccess[mode]||0)+1;
    const m=p.modeSuccess;
    p.status=p.reps>=6&&m.production>=1&&m.listening>=1&&m.recall>=2&&m.context>=1?'Pekişmiş':
      p.reps>=4&&m.production>=1&&m.recall>=1?'Aktif kullanılabiliyor':
      p.reps>=3?'Hatırlanıyor':p.reps>=2?'Tanınıyor':'Öğreniliyor';
  }
  return p;
}
export function dueItems(items,progress,now=Date.now()){
 return items.filter(x=>progress[x.id] && (progress[x.id].due||0)<=now);
}
export function priority(items,progress,now=Date.now()){
 return [...items].sort((a,b)=>{
   const p=progress[a.id],q=progress[b.id];
   const score=x=>!x?1e12:(x.due<=now?1e11+now-x.due: -x.due);
   return score(p)-score(q)>0?-1:score(p)-score(q)<0?1:0;
 });
}
// A small actionable daily queue, not a decorative list of study minutes.
// Due reviews come first; unseen items fill remaining slots in editorial priority order.
export function dailyAssignments(vocab,phrasals,drills,progress,now=Date.now(),limitWords=5,limitPhrasals=3){
 const select=(items,bank,count)=>{
   const due=dueItems(items,bank,now).sort((a,b)=>(bank[a.id].due||0)-(bank[b.id].due||0));
   const fresh=items.filter(x=>!bank[x.id]).sort((a,b)=>(a.priority??Infinity)-(b.priority??Infinity));
   return [...due,...fresh].slice(0,count);
 };
 const listened=new Set((progress.listenHistory||[]).map(x=>x.title));
 const drill=drills.find(x=>!listened.has(x.title))||drills[0]||null;
 return {words:select(vocab,progress.cards||{},limitWords),phrasals:select(phrasals,progress.phrasals||{},limitPhrasals),drill};
}
export function dailyPlan(progress, minutes=60) {
 const bad=(progress.listenHistory||[]).slice(-12);
 const avg=bad.length?bad.reduce((s,x)=>s+x.accuracy,0)/bad.length:55;
 const listen=avg<70?0.44:0.33, vocab=0.25, phrasal=0.15;
 const p=[{key:'listening',label:'Listening & Dictation',mins:Math.round(minutes*listen)},{key:'vocabulary',label:'Vocabulary',mins:Math.round(minutes*vocab)},{key:'phrasals',label:'Phrasal Verbs',mins:Math.round(minutes*phrasal)}];
 p.push({key:'reading',label:'Reading / Dialogue',mins:Math.max(2,minutes-p.reduce((s,x)=>s+x.mins,0)-Math.round(minutes*.1))});
 p.push({key:'review',label:'Smart Review',mins:minutes-p.reduce((s,x)=>s+x.mins,0)});
 return p;
}
export function quizBank(vocab,phrasals){
 const all=[];
 const pick=(items,target,field)=>items.filter(x=>x.id!==target.id&&x[field]!==target[field]).slice(0,4).map(x=>x[field]);
 vocab.forEach((v,i)=>{
   const pool=vocab.filter(x=>x.category===v.category&&x.id!==v.id).slice(i+1,i+5);
   const others=pool.length>=3?pool:vocab.filter(x=>x.id!==v.id&&x.tr!==v.tr).slice(0,4);
   const distractors=others.slice(0,3);
   all.push({id:'v-'+v.id,kind:'Vocabulary',category:v.category,question:`“${v.word}” ifadesinin bu dersteki anlamı nedir?`,answer:v.tr,options:[v.tr,...distractors.map(x=>x.tr)],optionExplanations:{[v.tr]:`Bu derste doğru anlamdır. ${v.definition} Örnek: ${v.example}`,...Object.fromEntries(distractors.map(x=>[x.tr,`Bu anlam “${x.word}” ifadesine aittir: ${x.definition}`]))},explanation:`${v.word}: ${v.definition}. Örnek: ${v.example}`});
 });
 phrasals.forEach((v,i)=>{
   const senses=v.senses?.length?v.senses:[{tr:v.tr,example:v.example,definition:v.definition}];
   senses.forEach((sense,j)=>{
     const distractors=phrasals.filter(x=>x.id!==v.id&&x.tr!==sense.tr).slice((i+5)%Math.max(1,phrasals.length)).concat(phrasals.filter(x=>x.id!==v.id&&x.tr!==sense.tr)).filter((x,k,a)=>a.findIndex(y=>y.tr===x.tr)===k).slice(0,3);
     if(distractors.length!==3)throw Error('Not enough distinct phrasal distractors for '+v.word);
     const meaning=sense.definition||v.definition;
     all.push({id:'p-'+v.id+'-s'+j,kind:'Phrasal Verb',category:'phrasal',question:`“${v.word}” bu cümlede hangi anlamda kullanılıyor? ${sense.example}`,answer:sense.tr,options:[sense.tr,...distractors.map(x=>x.tr)],optionExplanations:{[sense.tr]:`Bu bağlamda doğru anlamdır. ${meaning}`,...Object.fromEntries(distractors.map(x=>[x.tr,`Bu anlam “${x.word}” kalıbının başka bir kullanımını açıklar: ${x.definition}`]))},explanation:`${v.word}: ${meaning} Örnek: ${sense.example}`});
   });
 });
 return all;
}
export function buildExam(bank,seen=[],seed=Date.now()){
 let x=(Math.floor(seed)>>>0)||1;
 const rnd=()=>{x^=x<<13;x^=x>>>17;x^=x<<5;return (x>>>0)/4294967296;};
 const shuffle=a=>a.map(v=>({v,r:rnd()})).sort((u,v)=>u.r-v.r).map(o=>o.v);
 const unique=[...new Map(bank.map(q=>[q.id,q])).values()];
 const selected=[];
 // Balanced exam: 10 general vocabulary, 7 accounting/finance, 8 phrasal verbs.
 for(const [category,count] of [['general',10],['finance',7],['phrasal',8]]){
  const eligible=unique.filter(q=>category==='finance'?['finance','accounting'].includes(q.category):q.category===category);
  const notSeen=shuffle(eligible.filter(q=>!seen.includes(q.id)));
  const older=shuffle(eligible.filter(q=>seen.includes(q.id)));
  selected.push(...[...notSeen,...older].slice(0,count));
 }
 if(selected.length<25)selected.push(...shuffle(unique.filter(q=>!selected.includes(q))).slice(0,25-selected.length));
 return shuffle(selected).map(q=>({...q,options:shuffle([...new Set(q.options)]).slice(0,4)}));
}
export function escapeHTML(v=''){return String(v).replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));}
