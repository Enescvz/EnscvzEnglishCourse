/** Observational within-user retention checks; no fabricated 7/30-day results.
 * A review only enters the 7- or 30-day cohort if the same item is reviewed
 * again at least that many days after its *first* recorded review.
 * This is NOT a randomized study or TOEFL proficiency estimate.
 */
const DAY=86400000;
export function retentionAudit(history=[],now=Date.now()){
 const rows=new Map();
 for(const r of history){
   if(typeof r?.id!=='string'||!r.id||!Number.isFinite(r.at)||r.at>now||!
     ['again','hard','good','easy'].includes(r.grade))continue;
   if(!rows.has(r.id))rows.set(r.id,[]);
   rows.get(r.id).push({at:r.at,grade:r.grade});
 }
 const windows=[7,30].map(days=>{
  let eligible=0,observed=0,remembered=0,effortful=0,failed=0;
  for(const attempts of rows.values()){
   attempts.sort((a,b)=>a.at-b.at);
   const first=attempts[0];
   if(now-first.at<days*DAY)continue;
   eligible++;
   // First follow-up at or beyond the target lag. An untested item stays
   // unobserved rather than becoming a successful retention result.
   const follow=attempts.find(x=>x.at-first.at>=days*DAY);
   if(!follow)continue;
   observed++;
   if(follow.grade==='again')failed++;else if(follow.grade==='hard')effortful++;else remembered++;
  }
  return {days,eligible,observed,remembered,effortful,failed,
   observedRecallRate:observed?Math.round(100*remembered/observed):null,
   missingFollowUps:eligible-observed};
 });
 return {cardsWithHistory:rows.size,windows,
  notice:'7/30 gün ölçümleri yalnızca gerçekten gözlenen takip tekrarlarını yansıtır. İyi/kolay yanıtlar hatırlama; zor yanıtlar çabalı tekrar olarak ayrı sayılır. Eksik takipler başarı sayılmaz. Bu bilimsel deney veya sınav puanı değildir.'};
}
