# American English Lab — VOA Level 2 Listening QA: 10 transkript (28 Ekim 2026)

**Geliştirme ve kalite raporu; yayıma izin vermez. Speaking kapsam dışıdır.**

## Gerçek veri durumu

| Ölçüm | Doğrulanmış değer |
|---|---:|
| VOA'nın resmi, insan sesiyle seslendirilmiş kaynak sayfaları | 50 |
| Özgün soruların bulunduğu dersler | 50 |
| Toplam özgün soru | 204 |
| Uygulamada yayımlanmış konuşma transkripti olan ders | **10** |
| Uygulamada metni olmayan, VOA sayfasına yönlendirilen ders | **40** |
| Transkriptli derslerde repliğe bağlanmış sorular | **44/44** |
| Dış kaynakta cevap metni bulunan, repliği uygulamaya alınmamış sorular | **160** |
| Uygulamaya paketlenmiş gerçek insan MP3 | **0** |
| Gerçek iPhone Safari MP3 oynatma testi | **0** |
| Ses ile transkriptin saniye bazında eşleşmesi | **0** |

## Bu tur eklenen yayıncı transkriptleri

- [Level 2 · Lesson 7 — Tip Your Tour Guide](https://learningenglish.voanews.com/a/lesson-7-tip-your-tour-guide/4064769.html): 39 konuşmacı repliği, 4 soru + replik/speaker kanıtı. Doğrudan MP3 bağlantısı yayımlanmış; **oynatımı doğrulanmadı**. Sayfanın sonundaki şarkıya ait 21 kelimelik edat tablosu, konuşma repliklerinden ayrı `publisherAppendix` olarak tutuluyor. Şarkıyla eşleşme doğrulanmadı.
- [Level 2 · Lesson 8 — The Best Barbecue](https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-8-best-barbecue/4073994.html): 30 konuşmacı repliği, 4 soru + replik/speaker kanıtı. İncelenen sayfada doğrudan **128 kbps MP3 bağlantısı görünmediğinden** `audioUrl: null` olarak saklandı. Uygulamada bozuk bir `<audio>` oynatıcı yerine yayımcı sayfasına güvenli bağlantı var.
- [Level 2 · Lesson 9 — Pets Are Family, Too!](https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-9-pets-are-family-too/4074883.html): 38 konuşmacı repliği, 4 soru + replik/speaker kanıtı. Kaynağın gerçek adı “One-of-Kind Pet” olarak soru seçeneğinde düzeltildi. MP3 bağlantısı kaynakta var; **cihaz oynatımı doğrulanmadı**.

Önceden uygulamada bulunan **Level 2 Lessons 1, 2, 3 ve 10** için 20 sorunun da konuşma repliğiyle kanıtı tamamlandı. Lesson 3'te iki farklı replikle desteklenen bir cevap için `sourceEvidenceAdditional` alanı ve arayüz görünümü eklendi. Soru sırası, ID'ler ve öğrenme kayıtları değiştirilmedi.

## Eğitim içeriği kalite sınırları

1. Transkriptler VOA **Conversation** bölümündeki yayımlanmış metne dayanır; **MP3 ile insan tarafından kelime kelime karşılaştırılmış değillerdir**. Dolayısıyla “ses-transkript senkronu doğrulandı” etiketi kullanılmaz.
2. VOA, kurgulanmış insan sesli derslerdir; kendiliğinden gelişen/sokak röportajı gibi konuşmalar değildir. C1 düzeyinde gerçek hayattaki hızlı doğal konuşma ihtiyacını tek başına karşılamaz.
3. İlgili sayfalar VOA özgün materyalidir; yine de üçüncü taraf müzik, katkı ve yerel MP3 yeniden dağıtımı ayrı değerlendirilmelidir. Hiçbir insan sesi MP3 yerel olarak paketlenmedi.
4. Dinlemeyi tamamladım butonu **kullanıcının kendi beyanına** dayanır; harici oynatma API ile takip edilmez.
5. 42 eski eSpeak MP3 teknik olarak erişilebilir, fakat robotik ve doğal dinleme hedefi için **onaysız** durumdadır.
6. Kelime listesinde 1.000 genel + 500 phrasal verb iki örnekli **editoryal taslak** bulunur; Amerikan konuşma sıklığı, sözcük anlamı ve seviye için bağımsız uzman onayı yoktur.

## Test ve yayın kararı

- `npm test` — 49/49 başarılı.
- `python3 -m unittest discover -s tests -p 'test_*.py'` — 118/118 başarılı.
- Sanal Chromium masaüstü (1280×850) ve mobil viewport (390×844): VOA liste/filtresi, 7–9. derslerde metin, self-report gate, Lesson 8 MP3 yoksa yönlendirme, Reading ve Grammar akışı başarılı. **Gerçek iPhone Safari/WebKit testi değildir.**
- Importer yeniden çalışınca tekrar kayıt üretmiyor.
- `python3 tools/release_gate.py` **exit 1 / LOCKED**. Henüz yayın ZIP'i veya GitHub yüklemesi izni yok.

## Kalan işlerin önceliği

1. Kalan **40** VOA dersinin konuşma transkriptini yayımlanmış metinden, tek tek kaynak kontrolüyle entegre et; **160** sorunun doğru cevaplarını replik bazında doğrula.
2. Kullanılabilir doğal insan seslerini doğru lisansla yerel paketleme ve doğrudan MP3 linklerini iPhone Safari'de gerçek oynatım testinden geçir.
3. ABD günlük konuşma sıklığı / B2-C1 anlam kontrolüyle müfredatın editoryal seçimini doğrula; gerektiğinde eski kayıtları ID değiştirmeden arşivle.
4. Dinleme için segment alıştırmaları, gerçek zamanlamalar, erişilebilirlik ve çevrimdışı hata davranışını geliştir.
5. Reading, Grammar ve genel iOS/Windows QA'yı gerçek cihazda tamamla; Speaking'e dokunma.
