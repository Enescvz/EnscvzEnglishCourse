# American English Lab — VOA 12 Transkriptli Özel Geliştirme QA (28.10.2026)

**YAYIN KİLİTLİ — sadece özel geliştirme yedeği. Speaking kapsam dışı.**

## Bu geliştirme adımı

Kaynak: [VOA Level 2 Lesson 11 — The Big Snow](https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-11-the-big-snow/4102755.html) ve [VOA Level 2 Lesson 12 — Run! Bees!](https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-12-run-bees/4139015.html). Yayıncının **Conversation** konuşmacı replikleri ve doğrudan 128 kbps MP3 bağlantıları incelendi. Metin, **ses kaydıyla kelime kelime karşılaştırılmış değildir**. Sayfadaki görsel/stil işaretleri veya bağımsız sahne efekti notları zorunlu konuşma olarak gösterilmedi. Kaynaktaki dil bilgisi anlatımına ait replikler metin kapsamında tutuldu.

- Lesson 11: 51 konuşmacı repliği, 4 soru replik kanıtı; yiyecek/battaniye/giyim doğru seçeneği kaynağa göre düzeltildi.
- Lesson 12: 34 konuşmacı repliği, 4 soru replik kanıtı; 30.000 arı cevabı replikte doğrulandı.
- Her ikisi mevcut `voa-linked-2-11` / `voa-linked-2-12` kart kimliğini ve önceki quiz sırasını koruyarak içeri alındı. JSON güncellemeleri `tools/import_reviewed_voa_11_12.py` ile tekrarlanabilir ve idempotenttir.
- Tam transkriptli derslerin yeni toplamı **12**, yayıncı sayfasında kalan ders **38**; 204 özgün soru korunmuştur, bunların **52** tanesinde konuşmacı/replik kanıtı vardır. Kalan **152** soru bu düzeyde kaynak kontrolü bekliyor.

## Sınırlar ve telif

VOA [içerik kullanım politikası](https://learningenglish.voanews.com/p/6861.html), kendi eğitim metinlerinin ve MP3'lerinin kaynak gösterilerek yeniden kullanılmasına izin verir; AP/Reuters/AFP veya başka üçüncü taraf eserleri kapsamaz. Uygulamada içerikler VOA Learning English kaynaklı ve bağlantılıdır. **İnsan MP3'leri uygulama içine indirilmedi/paketlenmedi.**

Kaynak sayfalarındaki MP3 bağlantıları mevcut olabilir ama **gerçek sesin oynadığı, içeriğin birebir kaynağa denk geldiği veya iPhone Safari'de çaldığı doğrulanmadı**. Çevrimdışı dinleme yoktur. Kullanıcı dinlediğini kendisi onaylamadan iki quiz akışında Listening tamamlandı sayılmaz. 42 mevcut eSpeak MP3 robotiktir ve doğal ses QA onaysızdır. Hiçbir kelime/phrasal dersine bağımsız dil editörü onayı verilmemiştir.

## Test ve devam

49 Node ve 121 Python testi başarılı (170/170). Sanal Chromium masaüstü ve mobil akış kontrolleri geçti ancak runner kapanışı zaman aşımına uğradı; bunu gerçek cihaz veya tamamıyla temiz uçtan uca QA geçişi sayma. `python tools/release_gate.py` LOCKED olmak zorundadır.

Öncelik: kalan 38 yayıncı Conversation transkripti + 152 soruda replik kanıtı, gerçek MP3 ve iPhone Safari cihaz doğrulaması, 1.000 genel + 500 phrasal taslağında anlam / günlük konuşma sıklığı / offline QA. Speaking'e dokunma, eski kayıtları silme, GitHub veya yayın ZIP'i üretme.
