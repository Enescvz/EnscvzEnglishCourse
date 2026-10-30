# American English Lab — Genel kelime bağlam yükseltme sprinti

**Tarih:** 28 Ekim 2026 · **Durum:** ÖZEL GELİŞTİRME, YAYINLAMA YASAK

## Tamamlanan gerçek çalışmalar

1. Eski 422 genel kelime dersinin **182 tek örnekli kaydına**, mevcut örnekten farklı, özgün, bağlamlı İngilizce cümle eklendi. Artık genel kategoride ikinci örneği eksik kayıt yok. Eski ID, ilk örnek, Türkçe anlam, tanım ve geçmiş verileri korunuyor.
2. **145 yeni genel kelime** (35 B2 + 110 C1) özgün İngilizce tanım, Türkçe karşılık, birbirinden farklı iki Amerikan İngilizcesi örneği ve konuşma alıştırması promptu ile eklendi. İçerikler tek tek editör onayı almamış taslaklardır.
3. **17 ilave C1 kelime** için aynı iki bağlamlı formatta gerçek taslaklar yazıldı. Bu sayede seçili 1.000 kelimelik müfredatta yalnızca başlık düzeyinde kalan hedef sıfırlandı.
4. Üretim kuyruğunda bulunmayan ama belgeli CEFR-J/Octanove kaynak kataloğunda ve 500+500 odak müfredatında eşleşen 7 kelime, seviyeleri birebir uyuştuğu sürece içe alınabilir. Keyfî veya kaynaksız kelimeler hâlâ reddediliyor.
5. Bağlamlı derse dönüşen **35 hızlı anlam kartı** hızlı kart listesinden çıkarıldı. Gerçek öğrenme kartlarıyla çift sayım yapılmadı.
6. Odak müfredatı, kaynak ekranı ve çevrimdışı ses listesi yeniden üretildi. Genel kelime taslakları `584/1000`, phrasal verb taslakları `500/500`.

## Kanıtlanan sayılar

| İçerik | Önce | Sonra |
|---|---:|---:|
| Genel bağlamlı ders taslağı | 422 | **584** |
| Genel tek örnekli ders | 182 | **0** |
| Müfredattaki gloss-only kelime | 451 | **416** |
| Müfredattaki headword-only kelime | 127 | **0** |
| Müfredattaki bağlamlı phrasal verb | 500 | **500** |
| Müfredat dışı hızlı kart | 852 | **817** |
| Finans/Accounting dersleri | 284 | **284** |
| Finans/Accounting tek örnekli ders | 232 | **232** |

- **Testler:** `npm run test:all` başarılı, **46 Node + 65 Python = 111 test**.
- `tools/audit_examples.py`: **584 genel + 500 phrasal** için en az 2 farklı örnek. Finans/Accounting için 232 eksik ikinci örnek.
- `tools/audio_qa.py`: 42 teknik ses dosyası kontrol edildi. Bunlar sentetik dosyalardır, insan kaydı değildir.
- Chromium sanal origin senaryosu terminale `PASS desktop` ve `PASS mobile` yazdı; **test süreci kapanışta zaman aşımına uğradı**, dolayısıyla tam başarılı E2E süreci olarak sunulamaz. Gerçek iPhone WebKit/Safari kanıtı yok.
- `tools/release_gate.py`: **LOCKED**. Bağımsız editöryal onay, lisanslı gerçek insan kayıtları ve diğer ders türü kotaları eksik. Hiçbir yayın yapılmadı.

## Doğrulanmamış noktalar ve sıradaki öncelik

- Kelime seviyeleri sadece kaynakta aday olarak işaretli; konuşma frekansına göre bilimsel olarak derecelendirilmiş veya bağımsız editörce doğrulanmış değil. 1.000 kelimenin konuşma odaklı kürasyonu iyileştirilmeli.
- Kalan **416 odak hızlı kartın** özgün İngilizce tanım + iki doğal örnek + telaffuz/geri çağırma alıştırmalarıyla bağlamlı derse dönüştürülmesi gerekiyor.
- **232 finans kartında** ikinci örnek eksik; ayrı onarım sprinti açılmalı.
- Bağımsız editöryal doğruluk, Amerikan aksanı ve gerçek iPhone Safari testi tamamlanmadan yayın kilidi kaldırılmamalı.
- GitHub'a veya Google Drive'a bu geliştirme yedeği yüklenmedi.
