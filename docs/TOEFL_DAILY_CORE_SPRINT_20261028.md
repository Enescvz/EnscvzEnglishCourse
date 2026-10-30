# TOEFL + Daily English — ortak çekirdek, 28 Ekim 2026

**Kapsam:** Özel geliştirme; yayımlama kilitli. Speaking değiştirilmedi. Mevcut öğrenme ID'leri ve tarayıcı ilerleme verileri korunur.

## Kısa müfredat

- **200 kelime:** Academic Word List (AWL) sublist 1'deki 60 başlık (US yazımıyla `analyze`, `labor`) ve AEL'deki mevcut 140 günlük/akademik kullanımlı kelime.
- **50 phrasal verb:** Mevcut AEL kartlarından seçildi; yeni ID veya sahte tekrar yok.
- **50 yeni tam bağlamlı akademik kelime:** `data/toefl-academic.json`, `toefl-*` ID, orijinal Türkçe anlam, İngilizce açıklama, 2 farklı İngilizce örnek. Editoryal statü `authored_unreviewed`.
- **150 mevcut kelime + 50 mevcut phrasal:** Önceden kullanılan kart ID'lerine referans verildi. Öğrenme ve FSRS geçmişi aynen kalır.
- Günlük plan: **10 kelime + 3 phrasal** (yaklaşık 20 günlük ilk tur; tekrarlar ayrıca planlanır).

Bunlar **TOEFL'da kesin en sık geçen 200 kelime** değildir. ETS resmî sınav kelime sıklık tablosu sağlamamaktadır. Akademik çekirdeğin frekans gerekçesi AWL sublist 1'e dayanır; 140 kelime ve 50 phrasal seçimi henüz bağımsız dil editörü/US sözlü korpus sıklık incelemesinden geçmemiştir. Bilinmeyen sayıyı kesin istatistik gibi sunmayın. İçerik, güncellenen TOEFL 2026'nın günlük kampüs ve akademik dil karışımı için hazırlanmış bir **başlangıç setidir**, sınav kapsamının tamamı değildir.

## Entegrasyon

`js/app.js` içinde Vocabulary ve Phrasal ekranları `🎓 TOEFL + Daily` filtresini paylaşır. Ana ekranda kısa giriş bağlantıları bulunur. `data/toefl-core.json` yalnızca **mevcut veya yeni kart ID'lerine** bakar; mevcut `data/vocabulary.json`, `data/phrasals.json`, `data/fluency-focus.json`, Speaking fonksiyonu ve kullanıcı ilerlemesi değiştirilmedi. Sadece 50 yeni kelime çalışma sırasında genel kelime havuzuna yüklenir; 1.000 genel odak kartı 1.000 olarak kalır. `sw.js` yeni JSON dosyalarını önbelleğe alır, bu önbelleğe almanın fiziksel cihazda başarılı çalıştığı **doğrulanmamıştır**.

## Kaynak ve lisans

1. AWL 570 akademik kelime ailesini on frekans grubunda sıralar; ilk 60 sublist 1 içindedir: https://www.eapfoundation.com/vocab/academic/awllists/index.php . EAPFoundation eğitim amaçlı *ticari olmayan* kullanımda kaynak göstermeye izin verir. Başlıklar ABD yazımıyla normalize edildi, açıklama/örnek metinler birebir alınmadı.
2. COCA kaynaklı Academic Vocabulary List (AVL) arka plan araştırması: https://www.english-corpora.org/coca/avl.asp . AVL kaynak materyali kopyalanmadı.
3. ETS güncel sınav biçimi: https://www.eu.ets.org/toefl/test-takers/ibt/upcoming-updates-jan-2026.html . Bu uygulama ETS tarafından onaylanmış veya bir ETS ürünü değildir.

## Test / eksikler

Başlangıç: 49 Node + 121 Python = 170/170. Değişiklik sonrası: 50 Node + 125 Python = **175/175**. Sanal Chromium masaüstü/mobil modül kontrolünde iki `PASS` görüldü; çalışma yürütücüsü zaman aşımı / temiz çıkış kanıtı yok; bu **fiziksel iPhone Safari testinin yerine geçmez**. 0 yerel insan sesli MP3, TOEFL kelime frekansının ETS sınav sorularında bağımsız ölçümü yok, doğal telaffuz/US editörü onayı yok. Herhangi bir tamamlanma, resmî TOEFL puanına hazırlık garantisi olarak sunulamaz.

**Sıradaki işler:** 50 yeni kartın insan editörü US anlam/okunuş QA'sı; 200/50'lik setin gerçek okuma ve dinleme metinleriyle korpus doğrulaması; öğrenci başına zayıf kelime tespiti; offline iPhone WebKit testi; devam eden 38 VOA transkripti ve 152 soru kaynak çalışması. Speaking dışarıda kalır, yayın kilidi açık kalır.
