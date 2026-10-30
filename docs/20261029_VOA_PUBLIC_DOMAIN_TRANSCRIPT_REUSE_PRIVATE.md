# 29 Ekim 2026 — VOA açık kaynaklı gerçek insan sesi ve transkript entegrasyonu

**Yalnızca özel geliştirme; DO NOT DEPLOY.** Kullanıcının özgün hedefi, VOA gibi ücretsiz ve yasal yeniden kullanımlı yayıncıların gerçek insan seslerini ve transkriptlerini tek ders ekranında sunmaktır. Yayıncıya dış bağlantı geçici aşamadır.

## Lisans kararı
- VOA Learning English kendi ürettiği metin/MP3/medyayı kaynak gösterilerek eğitim ve ticari amaçla yeniden kullanmaya izin verir: https://learningenglish.voanews.com/p/6861.html
- Bu hak, üçüncü taraf şarkı sözleri ve haber ajansı materyallerini kapsamaz: https://learningenglish.voanews.com/p/6021.html
- Ücretsiz erişilebilen diğer kaynakların hepsi serbestçe kopyalanamaz; her kaynak için lisans denetlenir.

## Bu geliştirmede gerçekten yapılanlar
- Level 2 Lesson 23 (Rock Star): resmî VOA Conversation kaynak metni, kullanıcıya ait dersin mevcut ID'siyle entegre edildi; dört soru konuşmacı ve replik indeksine bağlandı; üçüncü taraf şarkı sözleri çıkarıldı ve eksiklik arayüzde açıkça belirtiliyor. Orijinal ses harici VOA MP3 bağlantısıdır, yerel MP3 değildir.
- Level 2 Lesson 24 (I Feel Super!): resmî VOA Conversation metni tüm konuşma replikleriyle eklendi; dört soru mevcut ID'leri korunarak replik kanıtına bağlandı. Ses yine yayıncının MP3 adresine bağlıdır.
- `js/app.js`: varsa telif hakkı nedeniyle çıkarılmış bölümler açıkça gösteriliyor. Eksik `focus` alanına sahip derslerde UI hatası engellendi.
- 50 ders / 204 özgün soru sabit. Uygulama içi transkript **24**, yayıncı bağlantılı **26**. Toplam **100** soru uygulama içi replik kanıtlı ve **104** soru yayıncı alıntı kanıtlı.
- Açık kalemleri içeren `qa/voa-remaining-transcript-backlog-20261029.json` üretildi.

## QA kısıtları
- Resmî HTML metni web üzerinden incelendi. Konuşma metninin birebir **sesle zaman eşleşmesi** test edilmedi.
- Ortam dış ağa DNS erişimi sağlayamadığı için MP3 baytları indirilemedi; **yerel insan sesi MP3 sayısı 0**. iPhone Safari'nin gerçek ses oynatımı ve çevrimdışı ses oynatımı doğrulanmadı.
- Lesson 23 şarkı sözleri telif nedeniyle metinde yer almadığından **kaydın bütünüyle birebir transkripti değildir**; öğrenciye açıkça bildirilir.
- Sanal Chromium masaüstü/mobil hedefli testler gerçek fiziksel iPhone testinin yerine geçmez.
- Speaking modülü ve FSRS öğrenme motoru değişmedi. GitHub veya dağıtım yapılmadı, yayın kilidi açık.

## Toplu içerik tamamlama yöntemi
1. Resmî VOA sayfasındaki Conversation bölümünü ve doğrudan insan sesli MP3 bağlantısını seç.
2. Aynı dersteki telifli şarkı/haber ajansı görselleri ve konuşmaları ayır; gerekirse şarkı bölümünü açıkça belirtip atla.
3. Transkripti konuşmacı-replik formatında yerel dosyaya aktar; otomatik çekilen metni insan kontrolü olmadan tam diye etiketleme.
4. Mevcut dört sorunun kanıtını metindeki tek bir repliğe eşle; cevapları yeniden üretmeden doğrula.
5. İçerik kimliklerini ve ilerleme verisini aynen koru; ardından JS, Python ve hedefli UI testlerini çalıştır.
6. Resmî gerçek insan MP3 sesini ancak lisans ve bayt bütünlüğü denetlenerek özel geliştirme paketine al; gerçek iPhone'da oynatma doğrulanana kadar bayrağı kapalı tut.
