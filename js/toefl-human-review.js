/** Teacher-reviewed practice only, never an ETS score. No automated meaning/grammar rating. */
export const HUMAN_RUBRIC_CATEGORIES=Object.freeze(['taskFulfillment','coherence','languageUse','development']);
export function compareHumanReviews(a,b){
 const clean=(v)=>v&&HUMAN_RUBRIC_CATEGORIES.every(k=>Number.isInteger(v[k])&&v[k]>=0&&v[k]<=5);
 if(!clean(a)||!clean(b))throw Error('Two complete human rubrics, each category 0–5, required');
 const differences=HUMAN_RUBRIC_CATEGORIES.map(category=>({category,first:a[category],second:b[category],difference:Math.abs(a[category]-b[category])}));
 return {differences,needsAdjudication:differences.some(d=>d.difference>=2),
  provisionalOnly:true,officialTOEFLScore:null,
  notice:'İki bağımsız değerlendirici puanı yalnızca eğitim geri bildirimi sağlar. ETS puanı veya kalibre CEFR seviyesi değildir.'};
}
