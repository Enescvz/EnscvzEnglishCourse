> **LATEST UPDATE (after this sprint, 28 October 2026):** VOA in-app publisher transcripts **7** (up from 4), publisher-only source quizzes **43** (down from 46), all **50** quiz-enabled, **204** questions. Three source texts (Lessons 4–6) and 12 turn-bound question evidence annotations added. In-app and external quiz paths both require listening self-report; no actual audio playback verification. **49 JS + 113 Python** automated tests passed, virtual Chromium desktop/mobile QA passed, publish gate remains LOCKED. See [`VOA_7_REVIEWED_TRANSCRIPTS_20261028.md`](VOA_7_REVIEWED_TRANSCRIPTS_20261028.md). The earlier 4/46 figures below describe the baseline **before** this update.

# American English Lab — Speaking hariç kalite revizyonu (28 Ekim 2026)

## Gerçekten tamamlanan değişiklikler

- 50 resmî VOA insan sesli kaynağın tümü için uygulama içinde bir soru seti bulunuyor: toplam **204 özgün soru**.
- VOA Level 2 / Lesson 3, **He Said – She Said**, yayımlanmış Conversation bölümü temel alınarak uygulama içine **25 konuşmacı repliği** ve **4 soru** ile alındı. Böylece **4 tam transkriptli ders + 46 VOA'ya bağlı sorulu ders** bulunuyor. Yeni kaydın ID'si `voa-linked-2-03` korunarak eski soru ilerleme kaydıyla uyumluluk sağlandı.
- Harici kaynakta dinleme bitirildiğine dair **kullanıcının kendi onayı** olmadan bir kaynak-bağlantılı quiz tamamlandı olarak kaydedilmiyor. Bu, ses oynatmanın teknik doğrulaması DEĞİLDİR.
- **30 Reading dersi / 150 soru** ve **20 Grammar dersi** mevcut. Grammar sorularının doğru seçenekleri A-B-C-D arasında 5'er kez; Reading cevapları 38/38/37/37 olacak şekilde dağıtıldı. Cevap anlamı veya soru metni değiştirilmedi.
- İçe alma / katalog kurma komutları tekrar çalıştığında yeni dersi silmiyor ve eski 47 sorulu kataloğa geri dönmüyor.
- Reading/Grammar ve VOA içeriği için regresyon testleri ve kalite raporu eklendi. Sanal Chromium masaüstü ve mobil akışında kaynak dinleme beyanı dahil arayüz kontrolü yapıldı; gerçek ses oynatma testi yapılmadı.
- Yayın kontrolü insan sesli kaynakları ayrı ölçüyor; robotik MP3'leri lisanslı doğal konuşma olarak saymıyor.

## Henüz tamamlanmamış önemli işler

1. 46 kaynak-bağlantılı VOA dersinin tam yayıncı transkriptlerinin uygulamaya aktarılması ve cümle/cevap bazında kontrolü.
2. Gerçek Amerikan seslerinin özellikle iPhone Safari'de çalındığının, bağlantıların ve gerekiyorsa izin/atfın doğrulanması; 0 yerel lisanslı insan sesli MP3.
3. Eski **42 eSpeak** dosyasını doğal Listening örnekleri olarak sunmamak ve uygun alternatifleri kalite onayından geçirmek.
4. 204 VOA sorusunun tamamının bağımsız dil editörü tarafından ses/metinle kontrolü; 46 kaynağın soru açıklamalarında genel kaynak atfı var, birebir kanıt dökümü henüz tamamlanmış değil.
5. 1.000 kelime + 500 phrasal verb için ABD konuşma frekansı, CEFR ve anlam kontrolünün tamamlanması; Reading/Grammar metinlerinin de dil editörü onayı.
6. iPhone Safari ve gerçek ağ/çevrimdışı kullanım testleri; sanal Chromium geçmesi bu testler yerine geçmez.
7. Eski 18 podcast ve 24 drill sayı/kalite eksikleri. 50 VOA kaynak sayfası 50 adet yerel podcast MP3 değildir.

## Doğrulama komutları

- `npm run test:all`
- `python tests/e2e_non_speaking_sprint.py` (virtual origin Chromium only)
- `python tools/audit_non_speaking_quality.py`
- `npm run qa:audio-quality`
- `npm run release:check` → bilerek **başarısız** olmalı; yayın kilitli.

**Speaking bu turda değiştirilmedi.** Google Drive, GitHub ve yayımlama işlemi yapılmadı. Bu bir geliştirme yedeğidir, tamamlanmış ürün değil.
