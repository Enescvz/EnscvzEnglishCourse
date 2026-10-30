# Günlük Amerikan İngilizcesi Kalıpları — B1/100 (Özel geliştirme)

## Kapsam

- Kullanıcının belirlediği toplam hedef **300 günlük kalıp**: **B1 100**, **B2 120**, **C1 80**.
- Bu ilk parti **yalnızca B1 grubundaki 100 özgün kalıbı** ekler. B2 ve C1 **0**; tamamlanmış gösterilmiyor.
- Kaynak: bu geliştirme sırasında özgün olarak yazılmış örnekler. Harici metin/kitap/transkript kopyalanmadı. Kalıplar günlük kullanıma göre seçilen editoryal taslaktır; dış korpus sıklığı ya da bağımsız CEFR derecelendirmesi doğrulanmadı.
- Her kayıt: kalıcı `ex-b1-###` kimliği, Türkçe karşılık, İngilizce kullanım notu, 2 ayrı orijinal İngilizce örnek, A/B kısa diyalog, açık ses ve editör onay durumu.
- Var olan `vocabulary.json` ve `phrasals.json` başlıklarıyla birebir aynı ifade tespit edilmedi. Kısmi anlamsal örtüşmeler insan editörü kontrolünde ayrıca değerlendirilmeli.

## Kod entegrasyonu

- `data/daily-expressions.json`: 100 kalıp + 300 hedefinin gerçek ilerleme durumu.
- `js/app.js`: menüden **Günlük Kalıplar** modülü; B1/B2/C1 filtreleme, 12'li sayfalama, örnek/diyalog gösterimi ve Hafıza Koçu'na geçiş. Ana sayfada doğrudan erişim.
- `js/memory.js`: benzersiz `expression:<id>` kayıtları için orijinal FSRS tekrar sistemi; öğretilen anlam, aktif yazılı hatırlama, bağlam sorusu, isteğe bağlı cihaz TTS, öz değerlendirmeli cümle çalışması.
- `js/engine.js`, `js/progress-safety.js`: `progress.expressions` alanı, eski JSON yedeklerinin yeni kayıtları silmeden güvenli birleştirilmesi.
- `sw.js`: yeni JSON dosyası önbellek çekirdeğine eklendi, cache sürümü güncellendi.

## Mutlak korumalar

- Speaking dosyaları ve Listening ders/ses verileri **değiştirilmedi**.
- Eski kelime / phrasal verb ID'leri, TOEFL 400/75 seçkisi ve mevcut ilerleme anahtarları **silinmedi / yeniden yazılmadı**.
- Gerçek insan sesi eklenmedi. Hafıza Koçu'nda ses varsa yalnızca **cihaz sentetik en-US TTS**; insan sesli dinleme başarısı olarak işlenmez.
- Fiziksel iPhone Safari offline QA yapılmadı, bağımsız dil editörü onayı yok. Özellikle B1/B2/C1 seviyeleri öğretim gruplaması olup sertifikalı ölçüm değildir.
- Yayın ve GitHub yükleme yapılmadı; yalnızca özel geliştirme yedeği. `python tools/release_gate.py` **LOCKED**.

## Sonraki parti

- B2 için 120 doğal ve eşsiz kalıp, ardından C1 için 80; her partide anlamsal çakışma, ifade doğallığı, iki örnek, diyalog, FSRS ve yedek testi.
- İnsana ait lisanslı ses dosyaları temin edildikçe kalıp bazlı eklenebilir; yalnızca kaynak bağlantısı olması gerçek oynatma veya offline onayı sayılmaz.
