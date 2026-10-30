/** Original, non-ETS practice: no official TOEFL score or automatic essay grading. */
export function normalizedSentence(s=''){
  return String(s).toLocaleLowerCase('en-US').replace(/[’']/g,"'").replace(/[^a-z0-9' ]+/g,' ').replace(/\s+/g,' ').trim();
}
export function checkBuiltSentence(task,answer){
  if(task.kind!=='build_sentence')throw Error('This is not a sentence-building task');
  const expected=normalizedSentence(task.answer),observed=normalizedSentence(answer);
  return {correct:observed.length>0&&observed===expected,expected:task.answer,graded:'exact_order_only'};
}
export function countWritingWords(text=''){return String(text).trim().split(/\s+/u).filter(Boolean).length;}
export function writingChecklist(task,text){
  const count=countWritingWords(text),range=task.suggestedWords||[0,0];
  return {words:count,suggestedRange:range,inSuggestedRange:count>=range[0]&&count<=range[1],editorReviewed:false,autoScore:null,
    requirements:task.points||[],notice:'Öz değerlendirme: kelime sayısı ve yalnızca yapısal ipuçları gözlenir; gramer, anlam doğruluğu ve TOEFL puanı ölçülmez.',
    observations:writingStructureHints(task,text),observableMetrics:writingDraftMetrics(text),revisionSteps:writingRevisionSteps(task,text)};
}

/** Checklist prompts are NOT automated essay correction or rubric scoring. */
export function writingStructureHints(task,text='') {
 const clean=String(text).trim(), sentences=clean.split(/[.!?]+/).filter(s=>s.trim().length>3);
 if(task.kind==='build_sentence')return ['Kelime sırası yalnızca tam eşleşmeyle kontrol edilir.'];
 const hints=[];
 if(!clean)return ['Metin henüz yazılmadı.'];
 if(task.kind==='write_email') {
  if(!/^(dear|hello|hi|good morning|good afternoon)\b/i.test(clean))hints.push('Alıcıya uygun bir hitap eklemeyi kontrol et.');
  if(!/(thank you|thanks|sincerely|best regards|kind regards|best wishes)/i.test(clean))hints.push('Uygun bir teşekkür/kapanış düşün.');
  hints.push('Gerekli bilgiler ve isteğin karşılanıp karşılanmadığını elle kontrol et.');
 } else if(task.kind==='academic_discussion') {
  if(sentences.length<3)hints.push('Görüşünü, gerekçeni ve örneğini ayrı cümlelerle açıklamayı düşün.');
  hints.push('Diğer öğrencinin görüşüne gerçekten yanıt verip vermediğini elle kontrol et.');
 }
 hints.push('Dil bilgisi ve düşünce kalitesi otomatik olarak değerlendirilmedi.');
 return hints;
}

/** Observable draft features, NOT grammar, communicative success, AI assessment or TOEFL rating. */
export function writingDraftMetrics(text=''){
 const raw=String(text).trim(),words=raw.match(/[\p{L}\p{N}]+(?:['’\-][\p{L}\p{N}]+)*/gu)||[];
 const sentences=raw.split(/[.!?]+(?:\s|$)/u).map(x=>x.trim()).filter(Boolean);
 const paragraphs=raw.split(/\n\s*\n/u).map(x=>x.trim()).filter(Boolean);
 const wordTypes=new Set(words.map(w=>w.toLowerCase()));
 return {wordCount:words.length,sentenceCount:sentences.length,paragraphCount:paragraphs.length,
   distinctWords:wordTypes.size,repeatRatio:words.length?Math.round(100*(1-wordTypes.size/words.length)):0,
   averageSentenceWords:sentences.length?Math.round(words.length/sentences.length):null};
}
export function writingRevisionSteps(task,text=''){
 const m=writingDraftMetrics(text),steps=[];
 if(task.kind==='build_sentence')return ['Sadece hedef kelimelerin doğru sırasını karşılaştır. Noktalama/gramer puanı çıkartılamaz.'];
 if(m.wordCount===0)return ['Önce İngilizce taslağını yaz. Ardından görevin koşullarını tek tek kontrol et.'];
 if(m.sentenceCount<2)steps.push('Fikrini açık bir cümlede kur; ikinci cümlede gerekçe veya uygulanabilir ayrıntı ekle.');
 if(m.averageSentenceWords!==null&&m.averageSentenceWords>32)steps.push('Çok uzun cümleleri anlam kaybetmeden iki kısa cümleye ayırmayı düşün.');
 if(m.wordCount>=50&&m.paragraphCount===1)steps.push('Giriş, açıklama ve kapanışın okunmasını kolaylaştırmak için paragraf ayrımı düşün.');
 if(task.kind==='write_email')steps.push('Alıcının rolünü, yazma amacını, istenen eylemi ve nazik kapanışı kendin kontrol et.');
 if(task.kind==='academic_discussion')steps.push('Görüşünü, gerekçeni, örneğini ve tartışmaya katkını kaynak görevle tek tek karşılaştır.');
 steps.push('Bu analiz yazının anlamını, doğruluğunu, akademik kalitesini veya TOEFL puanını ölçmez.');
 return steps;
}
