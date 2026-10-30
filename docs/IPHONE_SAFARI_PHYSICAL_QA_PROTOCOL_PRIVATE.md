# Fiziksel iPhone Safari / AEL PWA QA protokolü — henüz uygulanmadı

**Durum: NOT EXECUTED.** Bu kontrol listesini gerçek iPhone üzerinde kullanıcı veya yetkili test uzmanı uygulamalıdır. Kod simülasyonu başarısı gerçek cihaz onayı değildir. Test için uygulamanın **gizli, HTTPS test adresi** gerekir; üretim sürümü yayınlanmaz.

1. Safari'de gizli HTTPS test adresini internet açıkken aç. **Ayarlar → Safari Çevrimdışı Kullanım → İçerikleri indir/doğrula** işlemini tamamla. Önbellekte hata varsa kaydet ve yayını engelle.
2. Safari Paylaş → **Ana Ekrana Ekle**; uygulamayı ana ekrandan aç, tekrar içerik hazır durumunu denetle.
3. Bir TOEFL kelimesinin FSRS tekrarını ve Reading/Grammar alıştırmasını tamamla; aynı kayıt kimlikleri ve puanını ekran görüntüsüyle not et.
4. **Uçak modunu etkinleştir; Wi-Fi/Cellular kesinlikle kapalı olsun.** PWA'yı tamamen kapatıp ana ekrandan tekrar aç. Kelime/Reading/Grammar/Hafıza Koçu akışını dene; kaydı kapatıp tekrar açarak değişmediğini gözle.
5. Aynı testi Safari sekmesinde yap; düşük depolama ve Safari site verisini silme senaryosunun veriyi silebileceğini açıkça doğrula. Önce manuel yedek al ve yeni/eski kaydın güvenli birleştirilmesini kontrol et.
6. VOA sesli bir derste uçak modunda **sesin çalışmadığını açıkça bildiren** mesajı doğrula. Online iken oynatıcıdan gerçek sesin duyulduğunu, hız kontrolünün çalıştığını ve kaynak MP3 URL'sinin yüklenebildiğini fiziksel olarak dene. Doküman metni ile duyulan sesi bir ders boyunca karşılaştır.
7. Fiziksel cihaz modeli, iOS/Safari sürümü, HTTPS test adresi ve deneme tarihi, ses/video kanıtı, beklenen/gerçek sonuç, PASS/FAIL, hata görüntüsü rapora yazılır. **Bu alanlar doldurulmadan gerçek cihaz QA PASS değildir.**

Açık blokajlar: fiziksel iPhone erişimi; lisanslı/bütünlük kontrolü yapılmış lokal insan MP3, gerçek WebKit/network testine erişim. Speaking kapsam dışı.
