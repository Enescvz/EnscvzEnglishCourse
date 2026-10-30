# AEL Safari Çevrimdışı Geliştirme — 29 Ekim 2026 (ÖZEL, YAYIN DEĞİL)

## Değişiklikler
- `sw.js`: çekirdek HTML, CSS, modül JS ve uygulamanın ihtiyaç duyduğu JSON içerikleri önceden önbelleğe alır. 0,5 MB araştırma kataloğu da dahil edildi.
- İlk Service Worker kurulumunda 42 eski robotik MP3 zorunlu indirme değildir. Bu dosyalar doğrulanmış insan sesi değildir. Gerçek VOA MP3 akışları çevrimdışı sunulmaz.
- Ayarlar > Safari Çevrimdışı kullanım > **İçerikleri indir / doğrula**: zorunlu dosyaların sayısını kontrol eder, eksikleri yeniden indirir; başarısız yüklemeyi başarı olarak göstermez.
- Ağ kesildiğinde çekirdek sayfa önbellekten açılır; yeni/eksik kaynaklar 503 döndürür. Cache temizliği yalnız AEL sürümlerini etkiler; kullanıcı ilerleme localStorage'ına dokunulmaz.
- iOS ana ekran görünümü için meta bilgiler eklendi.

## Gerçek iPhone Safari'de kabul testi (henüz yapılmadı)
1. Uygulamanın **HTTPS** adresini Safari'de aç. ZIP içindeki `index.html` dosyasını `file://` olarak açma.
2. Ayarlar > Safari Çevrimdışı kullanım > **İçerikleri indir / doğrula**. `✓ Çevrimdışı metin içeriği hazır: n/n dosya` görünmeden uçak moduna geçme.
3. Safari Paylaş > Ana Ekrana Ekle. **Ana ekrandan kurulu uygulamayı aç**, internet açıkken aynı doğrulamayı burada **tekrar** yap. Safari sekmesi ve ana ekran uygulamasının depolamasını aynı varsayma.
4. İlerleme oluştur: bir kelime kartını çalış, bir TOEFL Writing taslağı gir. Ayarlardan JSON yedeği al.
5. Uçak modu aç, Wi-Fi'ı da kapat, uygulamayı tamamen kapatıp ana ekrandan yeniden başlat.
6. Kelime, phrasal verb, Grammar, Reading, TOEFL çalışma merkezi, Writing taslağı, kayıtlı deneme ve araştırma kataloğunu aç; şifreli olmayan yeni HTTP isteklerinin olmaması, UI hatası çıkmaması ve ilerlemenin korunması gerekli.
7. VOA çevrimiçi gerçek insan sesi oynatımı **çalışmayabilir**; bu beklenen sınırlamadır. Ses bozulmalarını offline başarı sayma.
8. İnterneti aç, tekrar ders ilerlemesini kontrol et. Depolama sıfırlanırsa JSON yedeğini içeri aktar.
9. Sonuçları iPhone modeli, iOS sürümü, Safari/ana ekran farkı, görev adımları, ekran görüntüsü ve tarih ile QA'ya kaydet.

## Kanıt ve blokajlar
- Otomatik: **71 JS + 164 Python = 235/235 geçti**.
- Service Worker simülasyonu: çekirdek önbellek, veri kaybı olmadan onarım, başarısız onarım, offline navigation, HTTP range, uygulama harici önbelleği koruma geçti.
- Sanal Chromium masaüstü + mobil **yalnızca Ayarlar UI** geçti; iPhone WebKit veya gerçek offline test değildir.
- Gerçek local HTTP Chromium testi `ERR_BLOCKED_BY_ADMINISTRATOR` ile engellendi; geçti olarak yazılmadı.
- Fiziksel iPhone Safari / offline yeniden başlatma / gerçek VOA ses QA **NOT_TESTED**.
- Safari saklama kotası ve depolama temizliği nedeniyle kalıcılık garanti edilemez, JSON yedek önemlidir.
- **Speaking değişmedi.** Kart ve ders ID'leri korundu. **RELEASE LOCKED.**
