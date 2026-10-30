# Toplu B2–C1 Vocabulary / Phrasal Verb üretim hattı

**Durum: geliştirme / yayın kapalı.** Üretim veri dosyaları (`data/vocabulary.json`, `data/phrasals.json`) otomatik olarak değiştirilmez. `qa/candidate-*.json` dosyaları yalnızca **inceleme kuyruğudur**, canlı ders değildir.

## Neden kaynakları böyle birleştiriyoruz?

- CEFR-J B2 ve Octanove C1 derlenmiş listeler: B2/C1 kelime **adayları** ve Türkçe anlam ön-çalışması.
- Vocab Bloom Hub 0.2.0: kelime için kaynak tanım ve örnek **adayları**; phrasal verb, ayrı anlamlar, nesne konumu ve register **adayları**.
- Mevcut editoryal üretim kartları: tekrar etmeyecek şekilde eleme.
- Uygulama ana veri kümesine aktarım **yalnızca insan dil editörünün anlam, gerçek Amerikan kullanımı, CEFR, cümle, telaffuz ve Türkçe gloss doğrulamasından sonra** yapılabilir.

Bu kaynaklar resmî, tamamı doğrulanmış CEFR 3.500 + 600 listesi değildir; B2/C1 etiketleri çelişebilir. `sourceLevelConflict`, `levelDisagreement`, `senseCandidates`, `missingRequiredFields` gibi alanlar bunun için bulunmaktadır.

## İşlem

Python 3.10+ yeterli, ücretli API veya paket gerektirmez. İnternet erişimi olan geliştirme bilgisayarında:

```bash
python3 tools/bulk_curriculum.py --download --allow-network
npm run test:corpus
npm test
npm run release:check
```

İlk komut büyük (~100–250 MB) açık lisanslı veri kaynaklarını `sources/` altına indirir ve **üretim veri dosyalarını değiştirmeden** şu dosyaları oluşturur:

- `qa/candidate-vocabulary.json`: mevcut kartlardan farklı B2/C1 kelime adayları.
- `qa/candidate-phrasals.json`: çok anlamlı phrasal verb adayları; Türkçe karşılık gerekli olduğunda boş bırakılır.
- `qa/bulk-import-report.json`: aday sayıları, red sebepleri, girdilerin SHA-256 kontrol toplamı, kaynak ve bilinen riskler.

Kaynak dosyalar elindeyse `--cefr-b2`, `--cefr-c1`, `--bloom-words`, `--bloom-meanings`, `--bloom-phrasals` bayraklarına yerel dosya yollarını verebilirsin. `sources/` GitHub'a commit edilmemelidir.

## Yayına alınmadan önce editoryal kontrol

1. Kaynaktaki her anlamın Türkçe karşılık ve özgün ABD kullanımına uygun olduğunu doğrula; çok anlamlı kelimelerde ilk anlamı körlemesine seçme.
2. Kelimenin/öğretilen **anlamının** B2 veya C1 olduğuna dair kaynak kanıtını sakla; A1–B1 anlamlarıyla müfredat sayısını doldurma.
3. Word spelling/IPA/recording en-US uygunluğu; kişi adları, arkaik ifadeler ve Britanya'ya özgü kullanımları ayıkla.
4. Phrasal verbs için 600 **farklı headword**, anlamlar için ayrı sense kimliği, nesne konumu ve örnek uyumu sağlayacak gerçek cümleler hazırla.
5. QA yalnızca kartlara insan tarafından gerçekten bakıldığında `editorialStatus='approved'` yazabilir; sırf doldurmak için otomatik onaylanamaz.
6. İçeriğe kullanılan üçüncü taraf veri kaynaklarının CC lisans atıflarını ekle; özellikle Vocab Bloom Hub'ın AI-generated uyarısı zorunludur.
7. Chromium + iPhone WebKit E2E, ses hakları, bağlantılar ve tüm cevaplar denetlenmeden yayın yok.

> Bu ortamda ağ erişimi kısıtlıysa import aracı sadece test edilebilir; gerçek kaynakların indirilip çalıştırıldığı iddia edilmemelidir.

### Sıralama algoritması

Genel kelimelerde sıralama kaynağı ilk olarak NGSL 1.2 ilk 3.000 geniş derlem frekansıdır. Ardından önceden belirlenmiş sınırlı editoryal kullanım öncelikleri ve B2→C1 devreye girer. NGSL'de bulunmayan kelimelerin düşük kullanımlı olduğu iddia edilmez. Phrasal verb sıralamasında henüz kalıba özel doğrulanmış Amerikan konuşma frekansı olmadığından manuel pratik fayda öncelikleri kullanılır; bu değerler istatistiksel frekans diye sunulmaz.


## Hızlandırılmış resmi kaynak içe aktarımı (2026-10-27)

Tek komut: `npm run curriculum:bulk-fast`. Bu komut CEFR-J Wordlist 1.5 (B2),
Octanove C1/C2 Profile 1.0 (yalnızca C1) ve English Vocabulary'nin
CC BY-NC 4.0 lisanslı İngilizce/Türkçe phrasal verb listelerini **toplu** indirir.

- `qa/fast-vocabulary-candidates.json`: B2/C1 düzeyli farklı kelime başlıkları.
- `qa/fast-phrasal-candidates.json`: anlam adayları bulunan fakat B2/C1 etiketi henüz olmayan phrasal verb başlıkları.
- `qa/fast-import-report.json`: kesin aktarım sayıları ve kaynak SHA256 değerleri.

İndirilen kaynakların tam metni `sources/` altında tutulur; `sources/` Git tarafından
izlenmez. Liste başlıkları ile *aktif öğretilen kartlar* farklı sayılır.
Etimoloji/çoklu anlam, en-US IPA/ses, Türkçe karşılık, doğal örnek ve soru
içerikleri eksikse kayıt canlı ders olarak kullanılamaz. Bu komut yayın kilidini
açmaz.

Kaynaklar / yeniden kullanım: CEFR-J (Tono Lab, atıf zorunlu); Octanove C1
(CC BY-SA 4.0); tema4p/english-vocabulary (CC BY-NC 4.0, ticari kullanım yasak).
İlk iki kaynak CEFR-J ve Octanove'nin özgün profil CSV'leridir; Oxford
ve Cambridge ücretli/telifli sözlük kayıtları topluca alınmaz.

Not: Çalışma ortamımızın ağ erişimi kapalı olduğundan burada `--download`
başarılı oldu diye raporlanmıyor. Kaynak sayıları harici GitHub okumalarıyla
önceden doğrulanmıştır; indirildi/işlendi demek için lokal rapor gerekir.
