# Günlük Amerikan İngilizcesi — 300/300 kalıp | 29 Ekim 2026

## Amaç ve kapsam

- Önceki 100 B1 kartı **hiç değiştirilmeden** korunmuştur.
- **120 B2 + 80 C1** özgün (uygulamaya özel yazılmış) yeni ifade eklenmiştir. İfade sayısı: **300**.
- Her kartta Türkçe anlam, İngilizce kullanım notu, **iki ayrı özgün örnek** ve **iki replikli kısa diyalog** vardır: toplam **600 örnek ve 300 diyalog**.
- İfadeler B1/B2/C1 öğretim gruplarıdır. Resmî CEFR seviyesi, korpus sıklığı veya bağımsız insan editörlüğü doğrulanmış **değildir**.
- Yeniden üretilebilir yazım girdisi: `sources/daily-expressions-b2-authored-20261029.tsv` ve `sources/daily-expressions-c1-authored-20261029.tsv`.

## Entegrasyon

- `data/daily-expressions.json`: 100+120+80 ve her kartta kalıcı `ex-{level}-###` kimliği.
- `js/app.js`: B1/B2/C1 filtresi; seçilen düzeyde **FSRS Hafıza Koçu** oturumu başlatılır.
- `js/memory.js` ve `js/engine.js`: mevcut `expression:<id>` FSRS kayıt sistemi aynen kullanılır. Diğer kelime ve phrasal-verb ID'leri etkilenmez.
- `sw.js`: JSON önbelleği ve sürüm güncellemesi; gerçek iPhone Safari offline onayı sayılmaz.

## Kalan kalite engelleri

- **Bağımsız, insan eliyle kapsamlı editoryal inceleme yoktur.** İngilizce kullanımlar ve Türkçe anlamlar ikinci göz tarafından doğrulanmalı.
- **Lisanslı insan ses kaydı yoktur.** İsteğe bağlı cihaz TTS'si insan sesli Listening değildir.
- **Fiziksel iPhone Safari ve offline uçtan uca test yapılmamıştır.**
- Speaking, Listening ve TOEFL alt sistemleri değişmedi; GitHub'a yüklenmedi, yayına hazırlanmadı. Yayın kontrolü `LOCKED` kalmalıdır.

## QA ve devir

Otomatik testler: `npm test` ve `python3 -m unittest discover -s tests -p 'test_*.py'`; sonuç ve kontrol listesi `qa/daily-expressions-300-20261029.json` içindedir. Yeni kullanıcılar seviyelerini filtreleyebilir; eski kart öğrenme geçmişi korunur. İçerik kişisel beta kullanımına taslak olarak uygundur, resmî kalite onayı değildir.
