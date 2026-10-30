# American English Lab — 29 Ekim 2026 — 9/10 hedefi, doğrulanmış mühendislik ilerlemesi

> **PRIVATE DEVELOPMENT ONLY — DO NOT DEPLOY — RELEASE LOCKED.** Bu belge otomatik test ile gerçek cihaz/içerik onayını karıştırmaz.

## Mevcut veriler ve bu turun değişiklikleri

- Başlangıç yedeği: `AEL_PRIVATE_DEV_BACKUP_20261029_VOA24_PUBLIC_DOMAIN_QA_DO_NOT_DEPLOY.zip` (24 tam VOA konuşma metni / 26 dış bağlantılı, 204 kaynak kanıtlı soru). Mevcut kod üzerinde değişiklik yapıldı; proje sıfırdan oluşturulmadı.
- VOA Level 2 Lesson 25–30'un **6 konuşma metni** VOA'nın resmî sayfasındaki yayımlanmış metinlerden aktarılıp mevcut `voa-linked-2-25`–`voa-linked-2-30` kimlikleriyle birleştirildi. Konuşmacı ve sahne yönergesi ayrımı korunuyor. Kayıtların **ses-metni zaman eşleşmesi yapılmadı**. Lesson 30'daki lisansı net olmayan şarkı sözleri aktarılmadı; eksiklik ekranda gösterilir.
- Toplam **30/50** uygulama içi transkript, **20/50** kaynak sayfasında kalan tam metin; 204/204 özgün sorunun yayımlanmış metin kanıtı bulunuyor (**121 konuşma repliği + 3 sahne yönergesi + 80 dış bağlantılı yayımlanmış alıntı**).
- Orijinal 50 ders ID'si, 204 sorunun metin/şık/cevapları, 400 TOEFL kelimesi, 75 phrasal verb, 1.000 bağlamlı genel kelime, 500 genel phrasal ve önceki FSRS öğrenme motoru değişmedi. Bu yedek, geçmiş kullanıcının cihazında sakladığı veriyi içerdiği veya gerçek cihazdaki geçmişi okuduğu iddiasında değildir.
- Gerçek VOA MP3 kaynak URL'leri derslerde mevcut; `human-audio-status.js` akış yüklenme, duraksama ve hata durumlarını bildirir. Tarayıcı `playing` olayı **fiziksel iPhone doğrulaması değildir**. **0 yerel doğal insan sesi MP3**; 42 önceki robotik dosyanın durumu değişmedi.
- Lisans: VOA'nın kendi hazırladığı metin ve sesin kaynak belirtilerek yeniden kullanılabilmesine dair açıklama: <https://learningenglish.voanews.com/p/6861.html>. Üçüncü taraf şarkılar, görseller ve harici kayıtlar otomatik olarak kapsanmaz. Bölümlerin yayıncı kaynak URL'leri `tools/import_voa_reviewed_25_30.py` içindedir.
- Yeniden üretilebilir içerik ithalatı: `python3 tools/import_voa_reviewed_25_30.py`; kaynak satırları `sources/voa-reviewed-publisher/level2-25.txt`–`level2-30.txt`, soruların önceki versiyonları `sources/voa-25-30-original-quiz-ids.json`. İçe aktarma idempotence testi içerir.

## QA doğrulamasının kapsamı

| Kontrol | Sonuç | Ne anlama gelir? |
|---|---|---|
| JS unit tests | 89/89 PASS | Arayüz, ses hata durumu ve öğrenme motoru senaryoları |
| Python unit tests | 178/178 PASS | Veri bütünlüğü, içerik ve koruma kontrolleri |
| Sanal Chromium VOA 25–30 desktop/mobile | PASS/PASS | 6 dersin panel/transkript/MP3 URL görünümü |
| Sanal Chromium VOA 23–24 desktop/mobile | PASS/PASS | Eski derslerde regresyon yok |
| Baseline karşılaştırması | PASS | Eski 50 ders ID'si, 204 soru/cevap, TOEFL kartları ve Speaking işlevi korunuyor |
| Gerçek iPhone Safari uçak modu | **NOT TESTED** | Yalnız fiziksel cihaz ile kanıtlanabilir |
| Gerçek MP3 sesinin duyulması ve doğruluğu | **NOT VERIFIED** | Harici kaynak metni, sesin gerçekten oynadığı veya zaman eşleştiği anlamına gelmez |
| Sesin Safari offline kullanılabilmesi | **NOT AVAILABLE** | Lisanslı sesler yerel paketlenmedi; internet gerekli |
| Bağımsız dil editörü | **NO SIGNOFF** | Otomatik kontrol insan onayı değildir |
| TOEFL 2026 adaptif sınav ve puan | **NOT CALIBRATED** | ETS resmi skor ve deneme eşdeğeri yok |

## 9/10 için kapanması gereken blokajlar

1. **20 Level 1 VOA dersi (33–52):** Resmî yayımlanmış `Conversation` metinlerini tek tek okuyup 80 sorunun repliklerini yeniden eşleştir; uygunsuz üçüncü taraf materyalleri çıkar. Kimlikleri koru. Yaklaşım kaynak URL'lerini içeren `qa/voa-source-coverage.json` dosyasında listeli.
2. **Doğal sesin yerel kurulumu ve QA'sı:** Resmî MP3'leri indir, gerçek byte ve süre/format doğrulaması yap, içeriğin lisans/attribution denetimini sürdür; mobilde erişim ve gerçek ses kaydı için manuel doğrulama yap. Başarısız kaynaklar için güvenli fallback sun.
3. **Fiziksel iPhone Safari/PWA:** HTTPS URL, ana ekran kurulumu, önbellek doğrulaması, uçak modunda yeniden başlatma, yazma/okuma/tekrar ve kayıt kalıcılığı; hem online MP3 hem offline eksik durumları cihazda doğrulansın. Ayrıntı: `docs/IPHONE_SAFARI_PHYSICAL_QA_PROTOCOL_PRIVATE.md`.
4. **Bağımsız ABD İngilizcesi editörü:** 400 TOEFL kelimesi, 75 phrasal verb, genel 1.000/500 kartın anlam, örnek ve seviyesi için imzalı düzeltme; AWL/PHaVE eşleşmesi ETS'de çıkma sıklığı değildir.
5. **TOEFL ölçüm:** Gerçek doğal sesli TOEFL Listening görevleri, Writing için insan/uzman referanslı değerlendirme, resmi 2026 test tasarımına uygun kalibrasyonlu adaptif uygulama; mevcut AEL tanı denemelerini ETS skoru gibi gösterme.
6. **Öğrenme kalıcılığı:** 7 ve 30 günlük geriye dönük hatırlama takip deneyleri; tek seferlik unit-test kalıcılık kanıtı değildir.

**Mühendislik kararı:** Proje iyileştirildi fakat bağımsız doğrulama gerektiren işler bulunduğundan **9/10 onayı veya yayın hazır kararı verilemez**. Yayın kilidi `LOCKED`; GitHub/Google Drive/yayın artefaktı oluşturulmaz. Mevcut Speaking ve öğrenme kimlikleri değişmez.
