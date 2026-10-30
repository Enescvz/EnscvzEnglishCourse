# American English Lab — VOA Sorulu Listening Genişlemesi

**Durum: geliştirme sürümü, yayımlanamaz.** 28 Ekim 2026.

## Sayılar ve ayrım

| Kapsam | Önce | Şimdi |
|---|---:|---:|
| Resmî VOA kaynak sayfası | 50 | 50 |
| Uygulama içinde tam transkript + özgün sorular | 3 | 3 |
| VOA üzerinden dinlenip uygulamada çözülen özgün soru seti | 0 | **17** |
| Sorulu Listening toplamı | 3 | **20** |
| Özgün sorular | 16 | **84** (68 yeni) |
| Sadece kaynak bağlantısı bulunan ders | 47 | **30** |
| Bu tur indirilen/yeniden paketlenen VOA MP3 | 0 | **0** |
| Gerçek cihazda doğrulanmış yeni ses oynatımı | 0 | **0** |

17 ek ders, VOA **Let's Learn English Level 2** bölüm 3–9 ve 11–20'den seçildi. Bölüm 10, önceki 3 tam içeri aktarılmış dersten biridir.

## Nasıl çalışıyor?

1. **Real Voices · VOA → Sorulu dersler** filtresinden kaynağa gir.
2. Yeni 17 kaynak bağlantılı derste **VOA'da sesi ve transkripti aç** bağlantısına bas. Tam transkript ve insan sesi orijinal yayıncı sitesinde kalır. Bu derste uygulamada doğrudan ses oynatma ve tam transkript iddiası yoktur.
3. Metin kapalı dinledikten sonra uygulamaya dönüp dört seçenekli özgün soruları çöz.
4. Tamamlama düğmesi ancak dört cevap da girilmişse sonucu `authenticLessons` içine kaydeder. Dinlemenin fiilen yapıldığı doğrulanamaz; bu yüzden kayda `audioPlaybackSelfReported:true` eklenir.

## Kaynak ve doğrulama

- Orijinal VOA Conversation metinleri 28 Ekim 2026'da kaynak sayfalarından okunarak **68 yeni ve birbirinden farklı özgün soru** yazıldı. Her sorunun doğru yanıtı, açıklaması ve üç yanlış seçeneği mevcut; VOA sitesindeki hazır quiz kopyalanmadı.
- `data/voa-source-quizzes.json`: yeni 17 ders / 68 soru ve kaynak bağlantısı.
- `data/authentic-listening.json`: değişmemiş mevcut 3 tam transkriptli ders / 16 soru.
- `data/voa-source-catalog.json`: 50 kaynak, üç durum: `interactive_transcript_quiz`, `source_linked_quiz`, `publisher_source_only`.
- `tools/build_voa_source_quizzes.py`: kaynak içeriği yeniden yazmadan, deterministik soru verisi ve katalog durumları üretir. Kaynakların tam transkriptini **indirmez**.
- 128 kbps MP3'lerin mevcut olduğu sayfalarda görülmüştür ama 17 MP3 dosyasının cihazda oynatımı veya uzaktan dosya ömrü garanti edilmez.
- 42 eski eSpeak sentetik kayıt **değiştirilmedi**. İnsan seslerinin öne çıkarılması hâlâ eksik bir yayın kriteridir.
- Serbest erişim ile uygulamaya yeniden dağıtım hakkını karıştırmayın; VOA'nın kullanım koşulları ve üçüncü taraf materyallerin hakları yayına çıkmadan önce ayrıca yeniden denetlenmelidir.

## Kaynaklar (orijinal)

- Level 2 bölüm 3: https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-3/4027340.html
- Level 2 bölüm 4: https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-4-run-away-with-the-circus/4034187.html
- Level 2 bölüm 5: https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-5-greatest-vacation/4035571.html
- Level 2 bölüm 6: https://learningenglish.voanews.com/a/lesson-6-will-it-float/4064553.html
- Level 2 bölüm 7: https://learningenglish.voanews.com/a/lesson-7-tip-your-tour-guide/4064769.html
- Level 2 bölüm 8: https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-8-best-barbecue/4073994.html
- Level 2 bölüm 9: https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-9-pets-are-family-too/4074883.html
- Level 2 bölüm 11–20: tam URL'ler `data/voa-source-catalog.json` içinde.

## Açık işler

- 30 kaynak için sorular bulunmuyor.
- 17 yeni sorulu dersin transkripti uygulama içinde değil; kaynağa yönlendirilir.
- Yeni MP3'lerin yerel kopyaları, transkript sesle eşleşmesi, iPhone Safari ve masaüstü browser E2E doğrulaması yapılmadı.
- Kullanıcı henüz dinlemeden soruların çözülebilmesi eğitim amaçlı öz-beyan olarak saklanıyor; bu resmî dinleme yeterlilik ölçümü değildir.
- Yayın kilidi aktif kalmalı; **GitHub'a yüklenmemeli, nihai sürüm olarak paketlenmemeli**.

## QA sonucu, 28 Ekim

- `npm run test:all`: **49/49 Node.js + 99/99 Python = 148/148 başarılı**.
- `tests/e2e_voa_linked_quizzes.py`: sanal Chromium masaüstü ve mobil boyut testleri **PASS**. Yeni dört sorulu derse girme, dış yayıncı bağlantısı, dört soruyu yanıtlama ve yerel sonuç kaydı doğrulandı.
- Bu iki test, **gerçek iPhone Safari** veya VOA sitesindeki MP3'ün gerçekten oynadığını doğrulamaz.
- `rapid-vocabulary.json` eski çakışmaları düzeltildi: tam genel kelime dersleriyle çakışan 415, arşive alınmış kelimelerle çakışan 91 hızlı kart kaldırıldı; son durumda 399 bağımsız hızlı kart var. `tools/rapid_gloss_import.py` TSV bulunmadığında `--upstream-json` ile çalışabilir.
