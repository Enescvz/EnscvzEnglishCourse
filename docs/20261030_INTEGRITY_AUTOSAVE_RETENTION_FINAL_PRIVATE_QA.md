# American English Lab — Son eksikler, düzeltmeler ve QA raporu

**Tarih:** 30 Ekim 2026  
**Sürüm:** Private development backup / **DO NOT DEPLOY**  
**Temel sürüm:** `AEL_PRIVATE_DEV_20261030_FLUENCY_STUDIO_8_MODULES_QA_DO_NOT_DEPLOY.zip`

## 1. Kod taraması sonucu

Başlangıç paketinde 8 Fluency Studio modülü ve 34 ders / 340 alıştırma vardı. İlgili verileri yeniden üretmedim veya öğrenme ID'lerini değiştirmedim. Önceki ZIP'in tüm dosyaları korunuyor. Speaking işlevi kaynak kodunda **birebir aynı** bırakıldı; veritabanı/senkronizasyon ve canlı yayın işlemleri yapılmadı.

### Düzeltilen somut konular

1. **Bozuk kayıtların sessiz sıfırlanması (kritik):** Eski `localStorage` JSON'u bozuksa uygulama artık üzerine yazmıyor. Ekranda koruma uyarısı gösteriyor, ham içeriği `.txt` indirilebiliyor, geçerli v1 JSON yedeği yalnızca açık onayla yüklenebiliyor. Yanlış sürüm ve liste/nesne tipi hataları da korunuyor.
2. **Depolama dolduğunda yanlış başarı bildirimi (yüksek):** Genel `save()` yolu başarısız olunca son kalıcı duruma geri dönüyor; önemli çalışma akışları başarı bildirimi göstermiyor. Fluent/skill modüllerinin doğrudan yazma yolları da kurtarma kilidine tabi.
3. **Writing taslak kaybı (yüksek):** Fluency Writing'de tuşlama sonrasında gecikmeli otomatik kaydetme, alan değişimi, sekme gizlenmesi ve gezinti öncesi koruma eklendi. Kaydetme başarısızsa uyarı görünür ve uygulama ilgili yazıdan başka çalışma ekranına geçmez. Kaydedilen taslak JSON ilerleme yedeğine dahil.
4. **Kalıcılık oranının şişmesi (orta):** 7 ve 30 gün raporlarında `hard` artık başarılı hatırlama sayılmıyor; `effortful` olarak ayrı gösteriliyor. `good/easy` gözlenen bağımsız hatırlama; `again` başarısızlık. Takip edilmeyenler başarıya dahil edilmez.
5. **Zamanlı Writing ve kaynak önbellek güvenliği (orta):** Writing oturumunu başlatıp duraklatırken kalıcı kayıt başarısızsa sessiz başarı gösterilmiyor. Yeni bütünlük kontrol dosyası sürümlü service-worker önbelleğine eklendi.
6. **Kurtarma QA kapsamı:** Sürüm değişikliği, bozuk JSON, zararlı anahtar, eski kart ID'leri, otomatik yazı kaydı, kota hatası, ham kurtarma indirme ve geçerli yedekten onaylı geri yükleme test edildi.

## 2. Gerçek test sonuçları

| Kontrol | Sonuç |
| --- | --- |
| JavaScript otomatik test | **134/134 PASS** |
| Python içerik / kod test | **200/200 PASS** |
| Toplam | **334/334** |
| Yeni Chromium masaüstü taslak/kurtarma E2E | PASS |
| Yeni Chromium 390px mobil taslak/kurtarma E2E | PASS |
| Önceki Fluency Studio masaüstü E2E | PASS |
| Önceki Fluency Studio mobil E2E | PASS |
| Fiziksel iPhone Safari ve uçak modu | **YAPILMADI** |
| Harici insan sesi oynatma doğrulaması | **YAPILMADI** |
| Bağımsız dil editörü | **YAPILMADI** |
| Yayın kriterleri | **KİLİTLİ** |

### Kaynak bütünlüğü

- Aynı kalan veri dosyaları: vocabulary, phrasals, daily-expressions, sentence-skills, fluency-studio, authentic-listening, voa-source-quizzes, TOEFL Writing, grammar.
- Aynı kalan kod dosyaları: Speaking işlevi, memory engine, FSRS engine, sentence skill engine, TOEFL engine, önceki backup merge mantığı.
- Önceki ZIP'in hiçbir dosyası kaldırılmadı; bütün eski soru/kart ID'leri dosyalarda yerinde.
- Robotik podcast MP3'leri geri eklenmedi. Testte `audio_quality_gate.py` 42 eski sesin tamamını karantinada gösterdi.

## 3. Tamamlanamayan ve **yayın engeli** olan eksikler

| Öncelik | Eksik | Gerçek onay için gereken |
| --- | --- | --- |
| P0 | **İnsan sesli Listening** | 29 çevrimiçi kayıt bağlantısı gerçek oynatılmalı; her kayıt transkript, telif/atıf ve ses kesitleriyle eşleştirilmeli. Paket içinde onaylı MP3 sayısı 0. |
| P0 | **iPhone Safari offline/veri testi** | HTTPS kurulum, ana ekrandan açma, uçak modunda kapat-aç, JSON yedek geri yükleme, depolama kota ve ses testi gerçek cihazda geçmeli. |
| P0 | **Bağımsız İngilizce editör onayı** | Mevcut kelime, 500 phrasal verb, 500 günlük kalıp, 340 soru ve yeni görevlerin B1–C1 doğruluğu ve en-US doğallığı tek tek gözden geçirilmeli. |
| P1 | **20 eksik VOA transkripti** | İzinli/orijinal yayıncı transkripti, kanıt satırları, açıklamalar ve karşılıklı ses eşleşmesi tamamlanmalı. |
| P1 | **Dictation ses hizalaması** | 120 transkript satırı adayının gerçek zaman kodu/ses klibi yok. Doğrudan bağımsız dikte sınavı olarak sayılmaz. |
| P1 | **Writing değerlendirmesi** | Mevcut Writing Coach yalnızca ölçülebilen kelime, paragraf, bağlaç gibi özellikleri kontrol eder. Anlam/gramer/TOEFL puanı garantisi verilmemeli; insan editör veya kalibreli değerlendirme gerekir. |
| P1 | **7–30 günlük gerçek öğrenme verisi** | Zamanı gelmiş özgün alıştırmalarda gerçek kullanıcının takip yanıtları toplanmalı; bugünden başarı oranı uydurulmamalı. |
| P2 | **E2E istikrarı** | Birleşik Chromium kapanışında önceki sürümde aralıklı takılmalar vardı; bağımsız süreçler geçti, gerçek CI ortamında uzun tekrar koşusu hâlâ gerekli. |

## 4. iPhone için kabul planı

1. Güncel ZIP'i **yayınlamadan** yerel/özel HTTPS test ortamında aç; önce JSON ilerleme yedeği al.
2. İçerik önbelleğini doğrula. Ana ekrana ekleyip en az bir kelime, 1 soru ve bir Writing taslağı kaydet.
3. Uçak moduna al; uygulamayı tamamen kapat/aç; bu kayıtların, arama/alıştırma ekranlarının erişilebilir kaldığını kanıtla. Ses çevrimdışı değildir.
4. Çevrimiçi ol; yeni bir çalışmayı kaydet; JSON dışa aktar, geri yükle, ID ve tarihlerde gerileme olmadığını test et.
5. Telefon depolaması dolu/izin engelli koşulları ile hata ekranını incele. Sistem başarısız kayda başarı işareti vermemeli.
6. Ayrı cihazda ses linklerinin gerçekten açıldığını ve konuşmacı/transkript doğruluğunu insan tarafından kontrol et.

**Sınır:** Buradaki masaüstü/mobil testler Chromium simülasyonudur. Fiziksel iPhone Safari geçtiği iddia edilmez. İnternet bağlantılı ses kaynağı URL'si, tek başına telif hakkı veya doğal ses QA onayı değildir.

## 5. Son karar

Teknik dayanıklılık iyileşti; kişisel kullanım pilotu sürer. **Herkese açık yayın, iPhone offline ve insan sesli Listening kalite onayı verilmedi.** Speaking modülüne dokunulmadı. GitHub ve Google Drive bağlantılarına dosya gönderilmedi.
