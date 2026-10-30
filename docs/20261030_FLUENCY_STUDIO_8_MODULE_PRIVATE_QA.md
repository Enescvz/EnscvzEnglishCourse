# American English Lab — Fluency Studio (8 Modül) / Özel Geliştirme QA

**Tarih:** 30 Ekim 2026  
**Paket:** PRIVATE DEV / DO NOT DEPLOY  
**Durum:** Kod entegrasyonu ve otomatik kontroller tamamlandı; cihaz/ses/editör QA'sı eksik olduğu için **yayına uygun değil**.

## Kapsam ve gerçekten eklenenler

| Modül | Uygulamada işlev | Gerçek kapsam ve sınır |
| --- | --- | --- |
| Listening Master | Dinleme soruları, transkripti sonradan gösterme, kayıtlı tekrar | Mevcut 30 VOA transkriptli kaynağın 124 anlama sorusunu kullanır; 29 çevrimiçi ses URL'si var. Dış sesler gerçek cihazda oynatılıp eşleştirilmedi. |
| Dictation Lab | Duyulan cümleyi yazma, kelime düzeyinde Levenshtein karşılaştırma, öz-değerlendirme | 30 VOA içinden 120 transkript satırı adayı; bağımsız zaman kodlu ses klibi yok. Tam kayıtta cümleyi kullanıcı bulur; dikte pilotudur. |
| Real-Life Simulator | Otel/kafe/seyahat vb. dallanan 3 adımlı diyalog ve açıklamalı yanıt kontrolü | 12 özgün senaryo, 36 karar noktası; metin tabanlı, konuşma tanıma yok. |
| Personal Error Coach | Hatalı/zorlanılan yanıt kategorileri, doğrudan tekrar görevine dönüş | Gerçek yerel cevap geçmişine dayanır; konuşma/gramer için model tabanlı teşhis yok. |
| Writing Coach | 12 görev, taslak kaydetme, kelime/paragraf/cümle/bağlaç/tekrar ölçümleri | Otomatik semantik/dil bilgisi analizi veya TOEFL/CEFR puanı yok. |
| Reading + Listening Bridge | VOA metninin ilk replikleriyle okuma, ardından aynı kaynakta dinleme/anlama | İnsan sesli linkli 30 kaynak; satır-ses zaman eşleştirmesi ve offline ses yok. |
| English Thinking Trainer | Türkçe çeviri adımı olmadan İngilizce görev ve örnek cevap | 24 özgün görev, serbest üretim öz değerlendirmesi. |
| Adaptive Learning Path | Yerel hata/tekrar kayıtlarından 15–60 dakikalık günlük rota | Kural tabanlı plan, kişisel etkinliği klinik veya öğrenme deneyleriyle kanıtlanmadı. |

## Teknik entegrasyon

- Yeni `js/fluency-studio.js`, `js/fluency-ui.js` ve `data/fluency-studio.json`; ana uygulama `js/app.js` içinde 8 sekme.
- `fluencyCards`, `fluencyHistory`, `fluencyDrafts` cihazda tutulur, JSON yedek içe aktarma/birleştirme için `js/progress-safety.js` güncellendi.
- Eski sözlük, phrasal verb, günlük kalıp, Soru & Cümle Atölyesi içerikleri **silinmedi**. Önceki ZIP'le dosya bazlı karşılaştırmada hiçbir dosya kaldırılmadı.
- `sw.js`: yeni JS/JSON dosyaları önbellek listesine eklendi. **Dış VOA sesleri önbelleğe alınmıyor.**
- Yazma taslakları analiz edilince ekranın yeniden çizilip yazının silinmesi önlendi. Yerel depolama başarısızlığında olumlu kayıt bildirimi gösterilmiyor.
- Tek kaynak akışında soru soru ilerleme var; hata koçunun tıklama ile ilgili göreve dönüşü test edildi.
- Önceki ZIP'in `function speaking(...)` bloğu yeni ZIP'le birebir aynı. TOEFL çalışma blokları da korunuyor. 42 eski sentetik kayıt oynatılabilir pakette yok.

## Otomatik QA (30.10.2026)

- `npm test`: **128/128 geçti**.
- `python3 -m unittest discover -s tests -p 'test_*.py' -q`: **200/200 geçti**.
- `python3 tests/e2e_fluency_virtual.py --desktop`: **PASS**.
- `python3 tests/e2e_fluency_mobile_debug.py`: **PASS**, mobil 390px, temel 8 akış.
- `python3 tests/e2e_fluency_virtual.py`: iki arayüzü ayrı süreçlerde çalıştırdığında **PASS** kaydı var, ancak birleşik koşu başka bir tekrarda masaüstünden sonra bağlantı/süreç takılması gösterdi. Bu aralıklı test altyapısı problemi henüz çözülmüş kabul edilmez; bağımsız cihaz koşuları temel kanıttır.
- İlerleme yedeğinin birleştirilmesi, depolama hata güvenliği, dinleme öncesi başarı bildirimi engeli, içerik ID kontrolü, dikte karşılaştırması ve örneklerin yapısal kontrolleri otomatik testlerde mevcut.
- `python3 tools/release_gate.py`: **beklenen şekilde başarısız**, 14 yayın kriteri açık (11 kriter geçiyor).
- `python3 tools/audio_quality_gate.py`: 42 eski ses kaydı karantinada, 0 onaylı doğal insan sesli paket MP3.

## Kritik kalan QA ve ürün sınırları

1. **Gerçek iPhone Safari:** Airplane Mode yeniden açılış, Indexed/Local storage dayanıklılığı, önbellek ve JSON yedek gerçek cihazda doğrulanmadı.
2. **Ses:** 29 dış ses URL'sinin oynatılması, lisans/attribution, satır düzeyinde zaman kodu, transkript-ses eşleşmesi ve offline kullanım doğrulanmadı. Dinledim işareti kullanıcı beyanıdır; teknik ses tamamlama kanıtı değildir.
3. **İçerik editörü:** Yeni 36 diyalog adımı, 24 düşünme görevi, 12 yazma görevi ve eski içeriklerin bağımsız B2/ABD İngilizcesi editoryal kontrolü yapılmadı.
4. **Değerlendirme:** Writing Coach yalnızca sayılabilir metin özelliklerini kontrol eder; özgün serbest cümlelerin doğruluğu otomatik puanlanmaz.
5. **Kalıcılık:** 7 ve 30 günlük gerçek kullanıcı verisi/tekrar deneyleri yoktur.
6. **Dikte kullanılabilirliği:** Satıra özel lisanslı ses veya güvenilir zaman kodu olmadan 120 dikte örneği tam bağımsız dinleme sınavı sayılamaz.
7. **E2E test kararlılığı:** Tek koşuda art arda Chromium bağlamlarını açıp kapatan test altyapısı kimi zaman takılır. Her cihaz simülasyonu ayrı süreçte çalıştırılmalıdır.

**Sonuç:** Kod ve arayüzde sekiz modül entegre edilmiş **özel geliştirme pilotu** hazırdır. 328 otomatik birim/içerik testi başarılı; genel yayın, iPhone offline ve tam insan sesli öğrenim için onay verilemez.

**Korunan kısıtlar:** Speaking modülüne dokunma; Google Drive/GitHub'a yükleme yapma; yayın ZIP'i üretme; sentetik sesi insan sesi diye sunma; çalışma kayıtlarını silme. Bu dosya **private development backup** niteliğindedir.
