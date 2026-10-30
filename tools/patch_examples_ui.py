from pathlib import Path
p=Path(__file__).resolve().parents[1]/'js/app.js'
s=p.read_text(encoding='utf8')
s=s.replace("['listening','Dinleme'],['context','Bağlam']", "['listening','Kelime dinle'],['sentenceListening','Cümle dinle'],['context','Bağlam']")
anchor="function studyCard(item,isPhrasal){"
helper='''function sentenceExamples(item){
 const examples=(item.examples?.length?item.examples:[item.example]).filter(Boolean);
 return `<div class="examples" aria-label="Bağlam içinde örnek cümleler"><div class="small-label">AMERICAN ENGLISH · CONTEXT EXAMPLES</div>${examples.map((text,i)=>`<div class="example-row"><span class="example-number">${i+1}</span><p>${E(text)}</p>${button('🔊','speak','small soft',`aria-label="${i+1}. cümleyi Amerikan İngilizcesiyle dinle" data-text="${encodeURIComponent(text)}"`)}</div>`).join('')}</div>`;
}
'''
assert anchor in s
s=s.replace(anchor,helper+anchor)
old='<div class="ex">“${E(item.example)}”</div>'
assert old in s
s=s.replace(old,'${sentenceExamples(item)}',1)
anchor=" else if(ui.mode==='recall'){"
new=''' else if(ui.mode==='sentenceListening'){main=`<p class="small-label">LISTEN & DECODE · CÜMLEYİ TRANSCRIPT OLMADAN YAZ</p><h3>Örnek cümleyi dinle, duyduğunu İngilizce yaz.</h3><p class="mini">İlk dinlemede yazılı cümle görünmez. Kontrol sonrasında kelime sırası ve eksik kelimeler gösterilir. Tarayıcında en-US ses bulunmalıdır.</p>${button('▶ Amerikan aksanıyla cümleyi dinle','speak','primary',`data-text="${encodeURIComponent(item.example)}"`)}${typeInput('Duyduğun cümleyi yaz', 'gradeSentence')}`;}
'''
assert anchor in s
s=s.replace(anchor,new+anchor)
s=s.replace("ui.mode==='listening'?'Listen carefully':E(item.word)","['listening','sentenceListening'].includes(ui.mode)?'Listen carefully':E(item.word)")
s=s.replace("ui.mode!=='listening'?button('🔊'", "!['listening','sentenceListening'].includes(ui.mode)?button('🔊'")
old="<div class=\"notice\">${E(item.example)}</div><div class=\"flash-actions\">${button('🔊 Dinle'"
assert old in s
s=s.replace(old,"${sentenceExamples(item)}<div class=\"flash-actions\">${button('🔊 Dinle'",1)
anchor="function gradeReview(grade){"
new='''function gradeSentence(answer){
 const item=curr();const result=diffWords(answer,item.example);
 const pct=accuracy(answer,item.example);
 ui.checked=pct>=90;
 ui.feedback=`<b>${ui.checked?'✓ Cümleyi başarıyla çözdün!':'✕ Cümlenin bazı bölümleri eksik veya farklı.'}</b><p><strong>Dictation doğruluğu: %${pct}</strong></p><p>${result.map(x=>x.ok?`<span class="highlight">${E(x.word)}</span>`:`<span class="badword">${E(x.word)}</span>`).join(' ')}</p><p class="mini">Eksik duydukların kırmızı gösterilir; cümle sırası da kontrol edilir. Bu çalışmanın sesi tarayıcı en-US TTS özelliğidir.</p>`;
 ui.entry=answer;render();
}
'''
assert anchor in s
s=s.replace(anchor,new+anchor)
s=s.replace("mode==='listening'?'listening'", "['listening','sentenceListening'].includes(mode)?'listening'")
anchor=" case 'gradeWord':gradeWord(document.querySelector('#answer')?.value||'');break;"
assert anchor in s
s=s.replace(anchor,anchor+"\n case 'gradeSentence':gradeSentence(document.querySelector('#answer')?.value||'');break;")
old="const b=document.querySelector('[data-act=\"gradeWord\"], [data-act=\"checkDrill\"], [data-act=\"checkDictation\"]');"
assert old in s
s=s.replace(old,"const b=document.querySelector('[data-act=\"gradeWord\"], [data-act=\"gradeSentence\"], [data-act=\"checkDrill\"], [data-act=\"checkDictation\"]');")
p.write_text(s,encoding='utf8')
css=Path(__file__).resolve().parents[1]/'styles.css'
s=css.read_text(encoding='utf8')+'''\n/* Multiple authored context sentences per study card */
.examples{display:grid;gap:9px;margin:16px 0}.example-row{background:var(--raised);padding:10px 12px;border-radius:12px;display:flex;align-items:center;gap:10px}.example-row p{flex:1;line-height:1.55;margin:0;font-size:14px}.example-number{background:var(--mint-d);color:var(--mint);border-radius:9px;min-width:27px;height:27px;display:grid;place-items:center;font-size:12px;font-weight:800}.example-row .btn{flex-shrink:0}
'''
css.write_text(s,encoding='utf8')
sw=Path(__file__).resolve().parents[1]/'sw.js'
s=sw.read_text(encoding='utf8').replace("ael-dev-20261027-3","ael-dev-20261027-4")
sw.write_text(s,encoding='utf8')
print('Patched app.js, styles.css and sw.js for multiple example sentences and sentence dictation.')
