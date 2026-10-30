# Hafıza bilimi ve yabancı dil öğrenimi: araştırma + kod denetimi

**Tarih:** 2026-10-29 — yalnızca özel geliştirme, yayın yasak.

## Araştırma kapsamı ve kanıt sınırları

- **Aralıklı tekrar:** Mawson & Kang (2025) uygulamalı eğitim meta-analizi, 22 çalışma/31 etki büyüklüğünde dağıtılmış çalışmanın toplu avantajını yaklaşık `d=0.54` buldu. Bu AEL üzerinde ölçülmüş bir sonuç değildir. https://pubmed.ncbi.nlm.nih.gov/40564553/
- **Aktif hatırlama:** McDermott (2021) derlemesi; öğrenilen bilgiyi hafızadan geri getirmek uzun vadeli kalıcılığı artırabilir. https://pubmed.ncbi.nlm.nih.gov/33006925/
- **Yabancı dil ve web uygulamaları:** Belardi ve diğerleri (2021), 79 kişilik kelime uygulaması çalışmasında zaman aralığı, geri bildirim ve geri çağırmanın birlikte kullanımından yarar buldu. Raporlanan %29 fark başka sisteme otomatik genellenmez. https://pubmed.ncbi.nlm.nih.gov/34867656/
- **Bağlamsal kelime öğrenimi:** bağlamda hatırlama ve çıkarım iki bağımsız deneyde kelime hatırlamaya katkı yaptı. https://pubmed.ncbi.nlm.nih.gov/35436027/
- **Üretim:** yalnızca dinleyip taklit etmek yerine kelimeyi bellekte üretme ve sonrasında geri bildirim alma daha iyi sonuç verebiliyor. https://pubmed.ncbi.nlm.nih.gov/23681928/
- **Kişisel çağrışım / anahtar kelime:** Qu ve diğerleri (2024), kısıtlı hatırlama sayısında fayda buldu. Karşıt sonuçlar olduğundan çağrışım ZORUNLU değil; etimoloji gibi sunulamaz. https://pubmed.ncbi.nlm.nih.gov/38317910/ ; https://pubmed.ncbi.nlm.nih.gov/14672102/
- **Anki:** FSRS hedef hatırlama oranı varsayılan %90; Hard, unutma anlamına gelmez; FSRS kişisel optimizasyonu geçmiş verisi ister. https://docs.ankiweb.net/deck-options.html
- **Duolingo:** aralıklı tekrar ve hata odaklı kişiselleştirme kullanıyor; Duolingo'nun kendi öğrenen verisiyle eğitilmiş HLR modeli AEL'deki FSRS ile aynı değildir. https://research.duolingo.com/papers/settles.acl16.pdf ; https://blog.duolingo.com/spaced-repetition-for-learning/
- **Doping Hafıza:** kendi kamusal içeriği çağrışım, zihin haritası ve aktif tekrar vurguluyor. Pazarlama kaynaklı `2–4 kat` gibi genel nicel iddialar AEL etkinliği kanıtı olarak kullanılmadı. https://www.dopinghafiza.com/ogrenci-ve-veli-sorulari/yks-ogrenci-sorulari/ayt-kimya-periyodik-tablo-hizli-ezberleme-yontemi

## Başlangıç kod denetimi ve yapılan revizyonlar

| Kontrol | Başlangıç | Revizyon |
|---|---|---|
| FSRS-5 %90 hedef | Mevcut, yalnızca varsayılan parametre | Değişmedi; gerçek kullanıcı geçmişi olmadan kişisel optimizasyon iddiası yok |
| Hafıza Koçu sıra | Erken, henüz zamanı gelmemiş FSRS kartları boş slotlara giriyordu | Yalnızca zamanı gelen ve yeni kartlar; geçmişi bozuk eski kayıtlar kaybolmuyor |
| Aktif hatırlama | Türkçeden İngilizce açık yanıt vardı ama kişisel ipucu aynı aşamada açılabiliyordu | Hatırlama öncesinde ipucu çıkarıldı; ipucu öğrenme aşamasında kalır |
| Ses yokken değerlendirme | TTS yokluğu Hard'a zorlayabiliyordu | Metin hatırlama + bağlam doğruysa TTS yokluğu notu düşürmez |
| Gerçek ses başarısı | Sentetik TTS tanıma `modeSuccess.listening` hanesine yazılıyordu | Yalnız `ttsRecognitionSuccess` olarak ayrı tutulur; insan sesi kanıtı değildir |
| Kendi cümlesi | Öz değerlendirme önce FSRS notunu değiştiriyordu | Not yalnız ölçülen aktif hatırlama ve bağlam üzerinden; üretim ayrı öz değerlendirme |
| TOEFL entegrasyonu | 400/75 seçkisi vardı ama Hafıza Koçu'nun 50 yeni akademik kartı kapsam dışında | Eski ID ve aynı progress bankasıyla 475/475 TOEFL karta ortak hafıza filtresi |
| Bağlamlı ezber | İki orijinal cümle ve çoktan seçmeli anlam | Mevcut; seçeneklerin anlamsal zorluğu bağımsız editör kontrolü bekliyor |

## Kanıtlanmayanlar

- FSRS parametreleri geçmiş kullanıcı verileriyle optimize edilmedi; yüzde 90 gerçek kullanıcı başarısı olarak ölçülmedi.
- TOEFL kelimeleri arasında belirli kelimelerin sınavda kesin çıkacağı kanıtlanamaz.
- Otomatik üretim cümlesi kontrolü semantik/doğruluk onayı değildir. Öğrenci öz değerlendirmesi resmi dil seviyesi değildir.
- Cihaz TTS'si gerçek insan sesli Listening değildir; iPhone WebKit/gerçek offline test yapılmadı.
- Bu sistemin A/B deneyi, 30/60 günlük kullanıcı hatırlama oranı ve harici editör onayı henüz yoktur.

## Önerilen kontrollü öğrenme protokolü

1. Günde yaklaşık 10 yeni kelime + 3 phrasal hedefle; önce zamanı gelenleri çalış. Gerçek kullanıcı yüküne göre limiti küçült.
2. İlk karşılaşmada anlam/iki bağlam ve İSTEĞE BAĞLI kişisel çağrışım oluştur; sahte etimoloji anlatma.
3. İngilizce yanıtı görmeden Türkçeden üret (typed recall), sonra düzeltici geri bildirim al.
4. İkinci doğal cümlede anlamı ayırt et, mümkünse yeni bağlamlarda Reading/Listening üzerinden karşılaş.
5. Cümleyi kendin yaz; otomatik doğrulanmamışsa sadece öz değerlendirme olarak sakla.
6. FSRS takvimi geldiğinde yeniden test et; tekrar zamanı gelmeyen kartları sırf boş kontenjan var diye zorla açma.
7. 1/7/30 gün sonra cevapların ve ses modu sonuçlarının tutulduğu gönüllü kullanıcı pilotunda hatırlama ve süre metriklerini test et; yayın kilidini koru.

**Yayın:** `LOCKED`. Speaking koduna dokunulmadı; eski kart ID'leri, kayıtlar ve veriler silinmedi.
