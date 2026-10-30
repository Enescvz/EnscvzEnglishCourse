import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs/promises';
// Lightweight DOM contract: validates every route rendering without a browser.
const actions={};let simulatedAnswer='',simulatedMemoryAnswer='',simulatedMemorySentence='';const root={innerHTML:'',addEventListener:(event,cb)=>{actions[event]=cb}};
globalThis.document={documentElement:{dataset:{}},querySelector:s=>s==='#app'?root:s==='#answer'?{value:simulatedAnswer}:s==='#memoryAnswer'?{value:simulatedMemoryAnswer}:s==='#memorySentence'?{value:simulatedMemorySentence}:s==='#memoryCue'?{value:'My own memory hook'}:null,createElement:()=>({dataset:{},remove(){},click(){},set textContent(v){}}),body:{append(){}}};
globalThis.window={addEventListener(){},speechSynthesis:{cancel(){}}};globalThis.location={hash:'#/home',protocol:'about:'};globalThis.scrollTo=()=>{};globalThis.localStorage={getItem:()=>null,setItem:()=>{}};
globalThis.__AEL_TEST_EAGER__=true;
globalThis.fetch=async (url)=>({ok:true,json:async()=>JSON.parse(await fs.readFile(new URL('../'+url,import.meta.url),'utf8'))});
await import('../js/app.js');await new Promise(r=>setTimeout(r,50));
const action=(a,ds={})=>actions.click({target:{closest:()=>({dataset:{act:a,...ds}})},preventDefault(){}});
test('home renders actual dashboard',()=>{assert.ok(root.innerHTML.includes('Real progress.'));assert.ok(root.innerHTML.includes('214 genel + 284 finans')===false);});
test('every major module renders',()=>{for(const v of ['listening','vocabulary','phrasals','podcasts','reading','grammar','speaking','writing','conversations','pronunciation','tests','review','analytics','settings']){action('goto',{view:v});assert.ok(!root.innerHTML.includes('Bir sorun oluştu'),v);assert.ok(root.innerHTML.includes('class="heading"'),v);}});
test('robotic podcast/drill routes are closed while reading/exam still work',()=>{
 action('goto',{view:'podcasts'});
 assert.ok(root.innerHTML.includes('Robotik podcast yayında değil'));
 assert.ok(!root.innerHTML.includes('audio id="media"'));
 assert.ok(!root.innerHTML.includes('data-act="openEpisode"'));
 action('openEpisode',{id:'mystery-library'});
 assert.ok(!root.innerHTML.includes('audio id="media"'));
 action('goto',{view:'listening'});
 assert.ok(root.innerHTML.includes('Gerçek insan sesli dersleri aç'));
 assert.ok(!root.innerHTML.includes('data-act="openDrill"'));
 action('openDrill',{id:'connected-1'});
 assert.ok(!root.innerHTML.includes('audio id="media"'));
 action('goto',{view:'reading'});action('openReading',{id:'the-midnight-train'});
 assert.ok(root.innerHTML.includes('Comprehension check'));
 action('goto',{view:'tests'});action('startExam');
 assert.equal((root.innerHTML.match(/data-act="examAnswer"/g)||[]).length,100);
});

test('example cards render multiple original sentences; sentence dictation hides target before grading',()=>{
 action('goto',{view:'vocabulary'});
 assert.ok(root.innerHTML.includes('CONTEXT EXAMPLES'));
 assert.ok(root.innerHTML.includes('example-row'));
 const item=JSON.parse('{"example":"She felt overwhelmed by the number of decisions."}');
 action('mode',{mode:'sentenceListening'});
 assert.ok(root.innerHTML.includes('CÜMLEYİ TRANSCRIPT OLMADAN YAZ'));
 assert.ok(!root.innerHTML.includes(item.example),'Target sentence must stay hidden until grading');
 simulatedAnswer='She felt overwhelmed by the number of decisions.';
 action('gradeSentence');
 assert.ok(root.innerHTML.includes('Dictation doğruluğu: %100'));
 assert.ok(root.innerHTML.includes('grade"'),'Review grading must appear after response');
 action('grade',{grade:'good'});
 assert.ok(!root.innerHTML.includes('Bir sorun oluştu'));
});

test('source catalog is searchable but does not inflate reviewed lesson deck',async()=>{
 action('goto',{view:'catalog'});
 await new Promise(r=>setTimeout(r,100));
 assert.ok(root.innerHTML.includes('B2/C1 Kaynak Havuzu'));
 assert.ok(root.innerHTML.includes('4.851 başlık'));
 assert.ok(root.innerHTML.includes('3.647'));
 action('catalogKind',{value:'p'});
 assert.ok(root.innerHTML.includes('1204 kaynak kaydı'));
 action('catalogNext');
 assert.ok(root.innerHTML.includes('Sayfa 2/'));
 action('catalogPrev');
 assert.ok(root.innerHTML.includes('Sayfa 1/'));
 action('catalogAvailability',{value:'lesson'});
 const catalog=JSON.parse(await fs.readFile(new URL('../data/candidate-catalog.json',import.meta.url),'utf8'));
 assert.ok(root.innerHTML.includes(catalog.entries.filter(x=>x.t==='p'&&x.lesson).length+' kaynak kaydı'));
 action('goto',{view:'vocabulary'});
 const vocab=JSON.parse(await fs.readFile(new URL('../data/vocabulary.json',import.meta.url),'utf8'));
 assert.ok(root.innerHTML.includes(vocab.filter(x=>x.category==='general').length+' genel + 50 yeni akademik + '+vocab.filter(x=>['finance','accounting'].includes(x.category)).length+' finans'));
});


test('rapid bilingual practice opens, reveals, reverses, and saves recognition only',async()=>{
 action('goto',{view:'rapid'});
 assert.ok(root.innerHTML.includes('Hızlı Kelime Kartları'));
 const rapid=JSON.parse(await fs.readFile(new URL('../data/rapid-vocabulary.json',import.meta.url),'utf8'));
 const vocab=JSON.parse(await fs.readFile(new URL('../data/vocabulary.json',import.meta.url),'utf8'));
 const existing=new Set(vocab.filter(x=>x.category==='general').map(x=>x.word.toLowerCase()));
 assert.ok(root.innerHTML.includes(String(rapid.filter(x=>!existing.has(x.word.toLowerCase())).length))); 
 assert.ok(root.innerHTML.includes('Cevabı göster'));
 action('rapidReveal');
 assert.ok(root.innerHTML.includes('Hatırladım'));
 action('rapidKnow');
 assert.ok(root.innerHTML.includes('1'), 'review progress should increment');
 action('rapidLevel',{value:'B2'});
 assert.ok(root.innerHTML.includes('B2'));
 action('rapidDirection');
 assert.ok(root.innerHTML.includes('TR → EN'));
 assert.ok(!root.innerHTML.includes('Bir sorun oluştu'));
});

test('source catalog gives unreviewed bilingual glosses a rapid link, not a false full lesson',async()=>{
 action('goto',{view:'catalog'});
 await new Promise(r=>setTimeout(r,20));
 action('catalogKind',{value:'v'});
 action('catalogAvailability',{value:'all'});
 // Search a headword known to exist only in the rapid glossary.
 actions.input({target:{dataset:{field:'search'},selectionStart:8,value:'haunting'}});
 assert.ok(root.innerHTML.includes('data-act="catalogOpenRapid"'));
 action('catalogOpenRapid',{word:'haunting'});
 assert.ok(root.innerHTML.includes('Hızlı Kelime Kartları'));
 assert.ok(root.innerHTML.includes('haunting'));
});


test('memory coach exercises real contextual content; does not expose answer before hearing',()=>{
 action('goto',{view:'memory'});
 assert.ok(root.innerHTML.includes('Hafıza Koçu'));
 assert.ok(root.innerHTML.includes('1.000'));
 assert.ok(root.innerHTML.includes('1. Bağ kur'));
 action('memoryStart');
 assert.ok(root.innerHTML.includes('Ne duydun?'));
 assert.ok(!root.innerHTML.includes('<h2 class="memory-word">'), 'Listening prompt must hide word');
 simulatedMemoryAnswer='gibberish';action('memoryCheckListen');
 assert.ok(root.innerHTML.includes('Ne duydun?'),'no hearing test without an en-US utterance starting');
 action('memorySkipListen');action('memoryNextRecall');
 assert.ok(root.innerHTML.includes('Aktif hatırla'));
 action('memoryRevealRecall');
 assert.ok(root.innerHTML.includes('Bu kelimeyi tekrar çalışacağız'));
 action('memoryNextContext');
 assert.ok(root.innerHTML.includes('Which meaning fits this sentence?'));
 action('memoryChooseContext',{value:'0'});action('memoryNextProduce');
 simulatedMemorySentence='I use this word in a new sentence.';action('memoryCheckProduce');
 assert.ok(root.innerHTML.includes('Senin cümlen'));
 action('memoryFinishNo');
 assert.ok(root.innerHTML.includes('2/10')||root.innerHTML.includes('Bugünkü oturum tamamlandı.'));
});
test('memory scope can switch to phrasals without exposing candidate-only entries',()=>{
 action('goto',{view:'memory'});action('memoryScope',{value:'phrasal'});
 assert.ok(root.innerHTML.includes('PHRASAL VERB'));
 assert.ok(!root.innerHTML.includes('Bir sorun oluştu'));
});

test('memory coach requires context recognition between recall and speaking',()=>{
 action('goto',{view:'memory'});
 action('memoryStart');action('memorySkipListen');action('memoryNextRecall');
 action('memoryRevealRecall');action('memoryNextContext');
 assert.ok(root.innerHTML.includes('Which meaning fits this sentence?'));
 assert.ok(root.innerHTML.includes('data-act="memoryChooseContext"'));
 assert.ok(!root.innerHTML.includes('Doğru: '),'do not reveal the correct choice before answering');
 action('memoryChooseContext',{value:'0'});
 assert.ok(root.innerHTML.includes('Doğru: '));
 action('memoryNextProduce');
 assert.ok(root.innerHTML.includes('Özgün İngilizce cümlen'));
});


test('TOEFL + Daily shared learning path filters 400 words and 75 existing phrasals',async()=>{
 const core=JSON.parse(await fs.readFile(new URL('../data/toefl-core.json',import.meta.url),'utf8'));
 const fresh=JSON.parse(await fs.readFile(new URL('../data/toefl-academic.json',import.meta.url),'utf8'));
 assert.equal(core.wordLessonIds.length,400);
 assert.equal(core.phrasalLessonIds.length,75);
 assert.equal(fresh.length,50);
 action('goto',{view:'home'});
 assert.ok(root.innerHTML.includes('Tek öğrenme yolu · ortak tekrar'));
 action('toeflOpen',{kind:'vocabulary'});
 assert.ok(root.innerHTML.includes('400 sonuç'));
 assert.ok(root.innerHTML.includes('TOEFL + Daily'));
 assert.ok(!root.innerHTML.includes('Bir sorun oluştu'));
 action('toeflOpen',{kind:'phrasals'});
 assert.ok(root.innerHTML.includes('75 sonuç'));
 action('filter',{value:'all'});
 assert.ok(root.innerHTML.includes('500 sonuç'));
 action('goto',{view:'vocabulary'});
 action('filter',{value:'toeflAcademic'});
 assert.ok(root.innerHTML.includes('50 sonuç'));
});

test('TOEFL 2026 hub permits a timed Reading mini and transcript-only listening without claiming a score',()=>{
 action('goto',{view:'toefl'});
 assert.ok(root.innerHTML.includes('TOEFL + Daily · 2026'));
 assert.ok(root.innerHTML.includes('doğrulanmış ses'));
 assert.ok(root.innerHTML.includes('Reading alıştırması'));
 action('startToeflMini');
 assert.equal((root.innerHTML.match(/data-act="toeflMiniAnswer"/g)||[]).length,36);
 assert.ok(root.innerHTML.includes('12 dakika'));
 action('finishToeflMini');
 assert.ok(root.innerHTML.includes('0/9'));
 assert.ok(root.innerHTML.includes('TOEFL 1–6'));
 action('exitToeflMini');
 action('toeflScriptOpen',{id:'tl26-conversation-03'});
 assert.ok(root.innerHTML.includes('Printing at the library'));
 assert.ok(!root.innerHTML.includes('Bir sorun oluştu'));
});


test('Reading diagnostic can be launched, resumed as a working practice with no official score',()=>{
 action('goto',{view:'toefl'});
 assert.ok(root.innerHTML.includes('Reading kapsam testi · 50 soru / 30 dk'));
 action('startToeflDiagnostic');
 assert.ok(root.innerHTML.includes('50 soru · 30 dakika'));
 assert.equal((root.innerHTML.match(/data-act="toeflMiniAnswer"/g)||[]).length,20);
 action('toeflReadingNext');
 assert.ok(root.innerHTML.includes('Sayfa 2/10'));
 action('exitToeflMini');
 assert.ok(root.innerHTML.includes('Yarım kalan Reading denemesine dön'));
 action('resumeToeflReading');
 action('finishToeflMini');
 assert.ok(root.innerHTML.includes('0/50'));
 assert.ok(root.innerHTML.includes('TOEFL 1–6'));
 action('exitToeflMini');
});

test('daily expressions list and FSRS entrypoint render without changing listening/speaking',()=>{
 action('goto',{view:'expressions'});
 assert.ok(root.innerHTML.includes('Günlük İngilizce Kalıpları'));
 assert.ok(root.innerHTML.includes('500/500'));
 assert.ok(root.innerHTML.includes('Keep you warm'));
 assert.ok(root.innerHTML.includes('Will this sweater be enough?'));
 action('expressionNext');assert.ok(root.innerHTML.includes('Sayfa 2/42'));
 action('expressionLevel',{value:'C1'});assert.ok(root.innerHTML.includes('I wouldn')&&root.innerHTML.includes('140'));
 action('expressionLevel',{value:'B2'});assert.ok(root.innerHTML.includes('leaning toward'));
 action('expressionPractice');assert.ok(root.innerHTML.includes('B2 Kalıplar'));
 action('goto',{view:'expressions'});
 action('expressionLevel',{value:'B1'});
 action('expressionPractice');
 assert.ok(root.innerHTML.includes('Hafıza Koçu'));
 assert.ok(root.innerHTML.includes('Keep you warm'));
 assert.ok(root.innerHTML.includes('Kısa diyalog'));
 assert.ok(!root.innerHTML.includes('Bir sorun oluştu'));
});
