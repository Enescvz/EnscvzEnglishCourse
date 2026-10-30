# American English Lab — Finalizasyon Adayı (Özel Geliştirme, YAYINLAMA)

Tarih: 30 Ekim 2026  
Temel paket: `AEL_PRIVATE_DEV_20261030_INTEGRITY_AUTOSAVE_RETENTION_QA_DO_NOT_DEPLOY.zip`  
Durum: **RELEASE CANDIDATE / DO_NOT_DEPLOY**. **Genel yayın için uygun değildir.**

## Bu turda gerçekten uygulanan kod iyileştirmeleri

1. İlk açılışta 19 JSON yerine 5 temel JSON istenir. Diğer dersler ilk ziyaret sırasında, eşzamanlı istekler tekilleştirilerek yüklenir. Modül yükleme hatası görünür ve yeniden denenebilir.
2. Service Worker ilk kurulumda yalnızca uygulama kabuğu ve temel içerikleri önbellekler; tüm çevrimdışı metin paketini yüklemek için **Settings > İçerikleri indir / doğrula** gereklidir. Bu işlemin tamamlandığı ayrı doğrulanır. İnsan sesli harici VOA bağlantıları offline değildir.
3. Normal Writing ve TOEFL Writing alanlarına 650 ms otomatik kayıt, ekran değişiminden önce kaydetme, görünür durum bildirimi ve depolama hatasında yazıyı koruma eklendi. Fluency Writing'in eski kaydı yerinde bırakıldı.
4. TOEFL yarım kalan okuma/yazma denemeleri ilgili veri dosyaları hazırlandıktan sonra geri yüklenir. Kaydedilmiş ilerleme ID'leri değişmedi.
5. Yeni yükleme katmanı ve tüm menüler için ayrıca testler eklendi.

## Test sonuçları

- **138/138 Node.js testi başarılı.** Yeni 4 içerik yükleyici testi dahil.
- **200/200 Python testi başarılı.** Toplam **338/338**.
- Simüle Chromium masaüstü ve mobil Fluency Studio E2E: başarılı.
- Simüle Chromium 390px mobilde 23 bölüm navigasyonu, 5 JSON'la ilk açılış, art arda modül değiştirme, Writing otomatik kayıt ve depolama kotası hatasında metin koruma: başarılı.
- Service Worker kurulum ve kullanıcı isteğiyle tam metin önbellekleme: Node tabanlı simülasyon testi başarılı.
- **Gerçek iPhone Safari, sesin cihazda çalması ve gerçek internet bağlantısı üzerinden Lighthouse: yapılmadı.**

## İlk açılış — önceki raporla karşılaştırma

| Sanal ölçüm | Önceki paket | Bu aday |
|---|---:|---:|
| İlk yüklenen kaynaklar (sıkıştırılmamış) | 3.439.844 B | 1.976.831 B |
| Miktardaki azalma | — | **%42.5** |
| Masaüstü açılış süresi (tek sanal koşu) | 1.459 ms | 1.521 ms |
| CPU 4× yavaşlatılmış mobil (tek sanal koşu) | 5.268 ms | 5.436 ms |

**Yorum:** Kaynak miktarı azaldı; bu ölçümlerde açılış süresinin iyileştiği kanıtlanmadı. Yeni bir **85/100** veya Lighthouse puanı iddia edilmez. Önceki 72/100 öznel değerlendirme bu sürüm için tekrar doğrulanmış puan değildir. Gerçek cihaz ve HTTP ölçümü gerekir.

## Yayın engelleri

Mevcut yayın kapısı hâlâ **14 kriteri engelliyor**. Teknik kod değişiklikleri, şu dış doğrulamaların yerine geçmez:

- **20 VOA kaynağı:** Kaynakta bulunan ses/transkript uygulama içine alınmadı. Tüm kaynaklar ve boş editör/onay alanları `qa/finalization_voa_manual_queue.csv` içinde listelendi. Yayıncıdan alınacak metin ve ses hakları ile transkript-ses eşleşmesi ayrıca teyit edilmelidir.
- **Gerçek insan sesi:** Onaylı ve paketlenmiş insan sesli MP3 sayısı 0; yapay/sentetik ses yeniden eklenmedi. Gerçek iPhone ve Windows üzerinde harici seslerin çalışması ayrıca doğrulanmalı.
- **Bağımsız editör:** Mevcut kelime, phrasal verb, günlük kalıp, TOEFL ve yeni 340 soru materyali için onaylı en-US editörü tarafından anlam, doğallık, seviye, örnek ve cevap alternatifleri gözden geçirilmelidir. Testlerin geçmesi dilsel doğruluğu garanti etmez.
- **iPhone Safari gerçek offline:** HTTPS test adresinde kurulum, tam metin paketi indirme, uçak modunda yeniden başlatma, Writing ve kart kayıtlarının korunması, yedek ve geri yükleme fiziksel cihazda yapılmalı.
- **Ölçüm:** TOEFL Writing resmi puanlaması yok; 7/30 günlük gerçek öğrenme kalıcılığı pilotu tamamlanmadı.
- **Eski nicel yayın hedefleri:** 50 yeni özgün podcast, 40 doğrulanmış insan sesli içerik, 60 dinleme alıştırması ve 10 lisanslı paketlenmiş insan kaydı gibi kriterler hâlâ sağlanmıyor. Bunları tutarsızlık gizlemek için kaldırmadım.

Tüm bloke kriterler `qa/finalization_release_blockers.csv` dosyasında açık olarak yer alır.

## Bütünlük ve yayın kararı

- Speaking işlevi **bayt düzeyinde aynı kod metniyle** korundu.
- 11 temel veri/motor dosyası önceki ZIP ile birebir aynı.
- Kart/çalışma ID'leri değiştirilmedi; içerik/öğrenme verileri sıfırlanmadı.
- GitHub, Google Drive veya başka bir canlı ortama yükleme **yapılmadı**.
- Bu ZIP, son **özel geliştirme adayıdır**; ürünün tamamen yayına hazır olduğu anlamına gelmez.

## Bir sonraki gerçek onay adımı

Kısa süreli gerçek cihaz pilotu ve uzman editoryal QA. `qa/finalization_release_blockers.csv` ve `qa/finalization_voa_manual_queue.csv` doldurulmadan `DO_NOT_DEPLOY` kaldırılmamalıdır.
