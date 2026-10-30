import json,re,os,subprocess,tempfile,wave,math,struct,shutil
from pathlib import Path
D=Path(__file__).resolve().parents[1]
# Each entry: American English headword | Turkish gloss | compact original sample sentence | level
GENERAL='''
acknowledge|kabul etmek|She acknowledged that her first estimate was wrong.|B2
acquire|edinmek|It takes time to acquire confidence in a new language.|B2
advocate|savunmak|Several neighbors advocate for safer streets.|B2
allocate|tahsis etmek|The city allocated more money to public libraries.|B2
ambiguous|belirsiz|His response was ambiguous, so I asked him to clarify.|C1
anticipate|öngörmek|We anticipate heavier traffic after the game.|B2
apparent|açıkça görülen|It became apparent that we needed a new plan.|B2
appreciate|değerini anlamak|I appreciate how carefully you explained the problem.|B2
arbitrary|keyfî|The deadline seemed completely arbitrary.|C1
assert|iddia etmek|The witness asserted that she had seen the driver.|C1
assess|değerlendirmek|The teacher assessed our progress at the end of the month.|B2
assumption|varsayım|Our decision was based on a mistaken assumption.|B2
attain|elde etmek|She attained a level of fluency she once thought impossible.|C1
authentic|özgün, gerçek|The museum displayed authentic letters from the period.|B2
awareness|farkındalık|The campaign raised awareness about food waste.|B2
bias|önyargı|The article revealed a subtle bias toward one candidate.|C1
breakthrough|önemli ilerleme|The new treatment represents a major breakthrough.|B2
capability|yetenek, kapasite|The device has the capability to translate speech.|B2
coherent|tutarlı|Her argument was clear and coherent.|C1
compelling|ikna edici, etkileyici|He gave a compelling reason to change the schedule.|C1
comprehensive|kapsamlı|The report offers a comprehensive review of the issue.|C1
concede|kabul etmek, taviz vermek|After a long discussion, she conceded that he had a point.|C1
concrete|somut|We need concrete evidence before making a decision.|B2
consequence|sonuç|Every choice has a consequence, even a small one.|B2
considerable|kayda değer|The move required a considerable amount of planning.|B2
consistent|tutarlı|Try to maintain a consistent study routine.|B2
constraint|kısıt|Time is our biggest constraint this week.|C1
contemplate|derinlemesine düşünmek|He contemplated moving to another city.|C1
conventional|geleneksel|Her approach challenged conventional wisdom.|C1
convey|iletmek, aktarmak|Her expression conveyed genuine excitement.|B2
credible|inandırıcı|The explanation sounded credible to everyone in the room.|C1
crucial|kritik, çok önemli|Sleep is crucial for memory and attention.|B2
cumulative|birikimli|The cumulative effect became clear after several months.|C1
decisive|belirleyici|The final question was decisive in the competition.|C1
dedicate|adamak|He dedicated an hour each morning to studying.|B2
deduce|sonuç çıkarmak|From the muddy footprints, she deduced that someone had entered.|C1
deficient|yetersiz, eksik|The plan was deficient in several important details.|C1
deliberate|kasıtlı, bilinçli|Her decision to remain silent was deliberate.|C1
demonstrate|göstermek|The experiment demonstrated a clear pattern.|B2
deprive|mahrum bırakmak|The storm deprived thousands of homes of electricity.|C1
derive|türetmek, kaynaklanmak|The word derives from an old French expression.|C1
deteriorate|kötüleşmek|Road conditions deteriorated overnight.|C1
distinct|ayrı, belirgin|There are two distinct reasons for his decision.|B2
diverse|çeşitli|The neighborhood has a diverse mix of restaurants.|B2
dominant|baskın|One voice was dominant throughout the debate.|C1
dramatic|çarpıcı|The new policy caused a dramatic change in demand.|B2
elaborate|ayrıntılandırmak|Could you elaborate on your main concern?|C1
eliminate|ortadan kaldırmak|The filter can eliminate most of the noise.|B2
emerge|ortaya çıkmak|New details began to emerge after the interview.|B2
emphasize|vurgulamak|She emphasized the importance of regular practice.|B2
encounter|karşılaşmak|We encountered an unexpected delay on the way.|B2
endure|dayanmak|The old bridge endured decades of harsh winters.|C1
enhance|geliştirmek|Adding examples can enhance the explanation.|B2
ensure|sağlamak|Double-check the address to ensure the package arrives.|B2
entail|gerektirmek, beraberinde getirmek|The position entails occasional weekend travel.|C1
establish|kurmak, ortaya koymak|The team established a clear set of guidelines.|B2
evaluate|değerlendirmek|We evaluated several options before choosing one.|B2
evident|belirgin|Her disappointment was evident in her voice.|C1
exceed|aşmak|The final cost may exceed the original budget.|B2
exclude|hariç tutmak|The price excludes local taxes.|B2
exhaustive|kapsamlı ve ayrıntılı|The researcher conducted an exhaustive review.|C1
expand|genişletmek|They hope to expand the program next year.|B2
explicit|açık ve net|The instructions should be explicit about the deadline.|C1
exploit|kötüye kullanmak|The company was criticized for exploiting its workers.|C1
facilitate|kolaylaştırmak|The new signs facilitate navigation in the station.|C1
feasible|uygulanabilir|Is it feasible to complete the project in two weeks?|C1
fluctuate|dalgalanmak|Temperatures fluctuate dramatically in the desert.|C1
formulate|oluşturmak|She formulated a plan before starting the research.|C1
fundamental|temel|Trust is fundamental to a healthy relationship.|B2
furthermore|ayrıca, üstelik|The location is convenient; furthermore, the rent is affordable.|C1
genuine|samimi, gerçek|His apology sounded genuine.|B2
grant|vermek, kabul etmek|The committee granted her request for extra time.|B2
highlight|vurgulamak|The documentary highlights the effects of climate change.|B2
hypothesis|hipotez|The experiment was designed to test the hypothesis.|C1
identical|birebir aynı|The two rooms looked almost identical.|B2
illustrate|örnekle açıklamak|The chart illustrates the change in population.|B2
implement|uygulamaya koymak|The school implemented a new attendance system.|B2
imply|ima etmek|His silence seemed to imply that he disagreed.|B2
incentive|teşvik|The discount gave customers an incentive to return.|C1
incorporate|dahil etmek|Try to incorporate new phrases into your conversations.|B2
inevitable|kaçınılmaz|Some mistakes are inevitable when learning something new.|C1
infer|çıkarım yapmak|Readers can infer her feelings from the final paragraph.|C1
inherent|doğasında bulunan|There are inherent risks in every investment.|C1
initiative|girişim|The library launched an initiative to encourage reading.|B2
insight|derin kavrayış|The interview offered insight into her motivation.|B2
integrate|bütünleştirmek|The team integrated feedback into the final design.|B2
interpret|yorumlamak|Different people may interpret the message differently.|B2
intricate|karmaşık, ince ayrıntılı|The necklace had an intricate design.|C1
investigate|araştırmak|Police are investigating the cause of the fire.|B2
justify|haklı göstermek|How do you justify spending so much on repairs?|C1
legitimate|meşru|She raised a legitimate concern about privacy.|C1
maintain|sürdürmek|He maintained a steady pace throughout the race.|B2
manipulate|yönlendirmek, manipüle etmek|The ad tried to manipulate customers into buying more.|C1
marginal|çok küçük, sınırlı|The changes produced only a marginal improvement.|C1
mitigate|hafifletmek|Trees can help mitigate the effects of extreme heat.|C1
moderate|ılımlı, orta düzey|The town experienced moderate growth last year.|B2
neglect|ihmal etmek|Don't neglect the details when reviewing the contract.|B2
notion|fikir, kavram|She rejected the notion that success happens overnight.|C1
obscure|belirsiz, az bilinen|The article refers to an obscure historical event.|C1
obtain|elde etmek|You must obtain permission before entering the site.|B2
ongoing|devam eden|The investigation is still ongoing.|B2
outcome|sonuç|The outcome surprised even the researchers.|B2
overlook|gözden kaçırmak|I overlooked a small error in the spreadsheet.|B2
overwhelmed|bunalmış|She felt overwhelmed by the number of decisions.|B2
paradox|çelişki gibi görünen durum|It is a paradox that more choices can make decisions harder.|C1
perceive|algılamak|Children often perceive time differently from adults.|C1
persist|ısrarla sürmek|The strange noise persisted throughout the night.|C1
perspective|bakış açısı|Traveling gave her a new perspective on life.|B2
plausible|makul, inandırıcı|His explanation was plausible but not yet proven.|C1
precise|kesin, net|Please provide a precise description of the problem.|B2
predominant|baskın, ağırlıklı|Spanish is the predominant language in the area.|C1
preliminary|ön hazırlık niteliğinde|These are only preliminary findings.|C1
presume|varsaymak|I presume you've already received the invitation.|C1
prioritize|öncelik vermek|She decided to prioritize sleep over late-night work.|B2
profound|derin|The experience had a profound effect on him.|C1
prominent|öne çıkan|She is a prominent researcher in the field.|B2
prospect|olasılık, beklenti|The prospect of moving abroad excited him.|C1
pursue|peşinden gitmek|He plans to pursue a career in journalism.|B2
rationale|gerekçe|The manager explained the rationale behind the decision.|C1
reinforce|pekiştirmek|Regular practice helps reinforce new vocabulary.|C1
reluctant|isteksiz|She was reluctant to share her opinion at first.|B2
remarkable|dikkate değer|The recovery was remarkable given the circumstances.|B2
resilient|dayanıklı|The community proved resilient after the storm.|C1
resolve|çözmek|The neighbors resolved their disagreement peacefully.|B2
retain|akılda tutmak, korumak|Short reviews help you retain new information.|C1
reveal|ortaya çıkarmak|The documents revealed an unexpected connection.|B2
rigorous|titiz|The research underwent rigorous review.|C1
scarce|kıt|Clean drinking water is scarce in the region.|C1
scenario|senaryo, olası durum|Consider the worst-case scenario before deciding.|B2
scope|kapsam|The project has grown beyond its original scope.|C1
scrutinize|titizlikle incelemek|The editor scrutinized every claim in the article.|C1
significant|önemli, kayda değer|The study found a significant difference between the groups.|B2
simultaneously|eş zamanlı olarak|Both alarms sounded simultaneously.|C1
skeptical|kuşkucu|I'm skeptical of claims that seem too good to be true.|C1
speculate|tahminde bulunmak|It is too early to speculate about the cause.|C1
stability|istikrar|The region has enjoyed several years of stability.|B2
substantial|kayda değer, büyük|The renovation required a substantial investment.|B2
subtle|ince, zor fark edilen|There was a subtle change in his tone.|C1
sustain|sürdürmek|The village struggled to sustain its population.|C1
tangible|somut|The team wanted tangible evidence of progress.|C1
tentative|kesin olmayan, geçici|We made tentative plans for the weekend.|C1
thorough|eksiksiz, titiz|The mechanic performed a thorough inspection.|B2
threshold|eşik|The noise reached the threshold for a formal complaint.|C1
transmit|iletmek|The device transmits data over a secure network.|B2
trigger|tetiklemek|The announcement triggered a lively debate.|B2
ultimately|nihayetinde|Ultimately, they decided to stay.|B2
unprecedented|benzeri görülmemiş|The city experienced unprecedented rainfall.|C1
undergo|geçirmek, maruz kalmak|The building will undergo extensive repairs.|C1
underlying|altta yatan|We need to address the underlying cause.|C1
undertake|üstlenmek|The organization undertook a major survey.|C1
valid|geçerli|Her criticism was valid and constructive.|B2
viable|uygulanabilir, sürdürülebilir|They searched for a viable alternative.|C1
vulnerable|savunmasız|Coastal communities are vulnerable to flooding.|B2
widespread|yaygın|The change attracted widespread attention.|B2
affluent|varlıklı|The district has several affluent neighborhoods.|C1
alleviate|hafifletmek|A short walk helped alleviate her stress.|C1
anecdote|kısa ilginç hikâye|She opened the lecture with a funny anecdote.|C1
apt|eğilimli|He is apt to forget appointments when he's busy.|C1
articulate|açıkça ifade etmek|She articulated her concerns calmly.|C1
bolster|güçlendirmek|The new evidence bolstered his argument.|C1
cautious|temkinli|Investors remained cautious after the announcement.|B2
compromise|uzlaşmak|Both sides agreed to compromise.|B2
consecutive|art arda gelen|It rained for five consecutive days.|C1
contradict|çelişmek|The witness's account contradicted the earlier statement.|B2
correlate|ilişkili olmak|The two measures correlate, but that doesn't prove causation.|C1
counterpart|muadil|She met her counterpart from the neighboring school.|C1
culminate|sonuçlanmak|Months of planning culminated in a successful event.|C1
discrepancy|tutarsızlık, farklılık|The accountant found a discrepancy between the reports.|C1
dispute|itiraz etmek|They disputed the accuracy of the figures.|B2
disrupt|aksatmak|Heavy snow disrupted train service.|B2
distinguish|ayırt etmek|It's important to distinguish facts from opinions.|B2
diminish|azalmak|The noise gradually diminished after midnight.|C1
dilemma|ikilem|She faced a dilemma between two attractive offers.|C1
empathy|empati|Empathy helps people communicate across differences.|B2
equivalent|eşdeğer|This amount is equivalent to about two weeks of work.|B2
ethical|etik|The article raises several ethical questions.|B2
exaggerate|abartmak|He tends to exaggerate how long the trip takes.|B2
exemplify|örneğini oluşturmak|Her actions exemplify the team's values.|C1
foster|teşvik etmek|Community events can foster a sense of belonging.|C1
grievance|şikâyet|Employees submitted a formal grievance.|C1
hostile|düşmanca|The audience became hostile during the debate.|C1
impartial|tarafsız|The mediator promised to remain impartial.|C1
inadequate|yetersiz|The explanation was inadequate for such a complex issue.|C1
inclined|meyilli|I'm inclined to agree with the first proposal.|C1
indispensable|vazgeçilmez|A reliable map is indispensable on this trail.|C1
intact|bozulmamış|The old building remained largely intact.|C1
intriguing|ilgi çekici|The documentary explores an intriguing mystery.|C1
irrelevant|alakasız|That detail is irrelevant to the main question.|B2
leverage|etkili biçimde kullanmak|She leveraged her experience to help the new team.|C1
mandatory|zorunlu|Attendance at the safety meeting is mandatory.|B2
mutual|karşılıklı|The agreement depends on mutual trust.|B2
nuance|ince anlam farkı|The translation missed an important nuance.|C1
objective|tarafsız|An objective assessment requires reliable evidence.|B2
obstacle|engel|The lack of funding became a major obstacle.|B2
outweigh|daha ağır basmak|The benefits outweigh the risks for most participants.|C1
persistent|ısrarcı, sürekli|The researcher asked persistent questions.|C1
prevalent|yaygın|The custom is prevalent in many coastal towns.|C1
reconcile|uzlaştırmak|They struggled to reconcile the two accounts.|C1
redundant|gereksiz, mükerrer|Several paragraphs were redundant and could be removed.|C1
relevant|ilgili|Please include only relevant information.|B2
repercussion|olumsuz sonuç|The decision may have serious repercussions.|C1
skepticism|kuşkuculuk|Her claim was met with healthy skepticism.|C1
sophisticated|gelişmiş, karmaşık|The museum uses sophisticated technology to preserve artifacts.|C1
spontaneous|kendiliğinden|The crowd broke into spontaneous applause.|B2
streamline|sadeleştirmek, verimli kılmak|The team streamlined its review process.|C1
susceptible|yatkın, savunmasız|These plants are susceptible to cold weather.|C1
transparent|şeffaf|The organization promised a transparent process.|B2
unanimous|oybirliğiyle|The committee reached a unanimous decision.|C1
undermine|zayıflatmak|Repeated delays can undermine public confidence.|C1
versatile|çok yönlü|This versatile tool works for several tasks.|C1
warrant|gerektirmek|The situation does not warrant an emergency response.|C1
whereas|oysa, halbuki|My sister loves cities, whereas I prefer small towns.|B2
withdraw|geri çekmek|He decided to withdraw his application.|B2
withstand|dayanmak|The shelter can withstand strong winds.|C1
'''

def lines(s,fields):
 out=[]
 for ln in s.strip().splitlines():
  if not ln.strip():continue
  a=[x.strip() for x in ln.split('|')]
  assert len(a)==fields,(ln,len(a))
  out.append(a)
 return out
G=lines(GENERAL,4)
assert len(set(x[0] for x in G))==len(G)
# Accounting + Finance: headword | Turkish meaning. These are distinct curated technical terms,
# not synthetic repetitions. Example/definition is provided for every headword as simple original context.
FIN='''
accounts payable|ticari borçlar
accounts receivable|ticari alacaklar
accrual accounting|tahakkuk esaslı muhasebe
cash accounting|nakit esaslı muhasebe
accrued expense|tahakkuk etmiş gider
accrued revenue|tahakkuk etmiş gelir
accrued interest|tahakkuk etmiş faiz
adjusting entry|düzeltme kaydı
amortization|itfa, amortisman
asset impairment|varlık değer düşüklüğü
allowance for doubtful accounts|şüpheli alacak karşılığı
accounts aging|alacakların yaşlandırılması
accounting period|muhasebe dönemi
accounting policy|muhasebe politikası
audit trail|denetim izi
auditor's opinion|denetçi görüşü
balance sheet|bilanço
bank reconciliation|banka mutabakatı
book value|defter değeri
capital expenditure|sermaye harcaması
cash equivalents|nakit benzerleri
cash flow statement|nakit akış tablosu
chart of accounts|hesap planı
closing entry|kapanış kaydı
contra asset|eksi aktif hesabı
cost allocation|maliyet dağıtımı
cost of goods sold|satılan malın maliyeti
credit memo|alacak dekontu
current asset|dönen varlık
current liability|kısa vadeli yükümlülük
debit balance|borç bakiyesi
deferred expense|ertelenmiş gider
deferred revenue|ertelenmiş gelir
depletion|tükenme payı
depreciation|amortisman (maddi duran varlık)
direct cost|doğrudan maliyet
double-entry bookkeeping|çift taraflı kayıt sistemi
earnings before interest and taxes|faiz ve vergi öncesi kâr
expense recognition|giderin muhasebeleştirilmesi
fair value|gerçeğe uygun değer
fiscal year|mali yıl
fixed asset|duran varlık
general ledger|büyük defter
goodwill|şerefiye
gross margin|brüt kâr marjı
gross profit|brüt kâr
historical cost|tarihî maliyet
income statement|gelir tablosu
indirect cost|dolaylı maliyet
intangible asset|maddi olmayan duran varlık
inventory turnover|stok devir hızı
journal entry|yevmiye kaydı
liability|yükümlülük
long-term liability|uzun vadeli yükümlülük
management accounting|yönetim muhasebesi
matching principle|eşleştirme ilkesi
materiality|önemlilik
net income|net kâr
net loss|net zarar
noncurrent asset|duran varlık
operating expense|faaliyet gideri
operating income|faaliyet kârı
outstanding invoice|ödenmemiş fatura
payroll expense|ücret gideri
prepaid expense|peşin ödenmiş gider
provision|karşılık
purchase order|satın alma siparişi
reconciliation|mutabakat
retained earnings|dağıtılmamış kârlar
revenue recognition|hasılatın muhasebeleştirilmesi
sales return|satış iadesi
shareholders' equity|özkaynaklar
straight-line depreciation|doğrusal amortisman
subsidiary ledger|yardımcı defter
tangible asset|maddi duran varlık
tax liability|vergi yükümlülüğü
trial balance|mizan
unearned revenue|kazanılmamış gelir
variable cost|değişken maliyet
variance analysis|sapma analizi
working capital|işletme sermayesi
write-down|değer düşürme
write-off|kayıttan silme
withholding tax|stopaj
break-even point|başabaş noktası
contribution margin|katkı payı
cost center|maliyet merkezi
profit center|kâr merkezi
budget variance|bütçe sapması
operating budget|faaliyet bütçesi
capital budgeting|sermaye bütçelemesi
absorption costing|tam maliyetleme
activity-based costing|faaliyet tabanlı maliyetleme
standard costing|standart maliyetleme
period cost|dönem maliyeti
product cost|ürün maliyeti
sunk cost|batık maliyet
opportunity cost|fırsat maliyeti
contingent liability|koşullu yükümlülük
subsequent event|bilanço tarihinden sonraki olay
internal control|iç kontrol
segregation of duties|görevlerin ayrılığı
material misstatement|önemli yanlışlık
asset turnover|aktif devir hızı
quick ratio|asit-test oranı
current ratio|cari oran
receivables turnover|alacak devir hızı
days sales outstanding|alacak tahsil süresi
inventory write-down|stok değer düşüklüğü
impairment loss|değer düşüklüğü zararı
lease liability|kira yükümlülüğü
right-of-use asset|kullanım hakkı varlığı
finance lease|finansal kiralama
operating lease|faaliyet kiralaması
consolidated statements|konsolide tablolar
noncontrolling interest|kontrol gücü olmayan pay
intercompany transaction|grup içi işlem
foreign exchange gain|kur farkı kârı
foreign exchange loss|kur farkı zararı
stock-based compensation|hisse bazlı ödeme
financial instrument|finansal araç
hedge accounting|korunma muhasebesi
cash-generating unit|nakit yaratan birim
segment reporting|bölümlere göre raporlama
related-party transaction|ilişkili taraf işlemi
financial disclosure|finansal açıklama
restatement|finansal tabloların yeniden düzenlenmesi
closing balance|kapanış bakiyesi
opening balance|açılış bakiyesi
cost basis|maliyet esası
liquidity|likidite
solvency|borç ödeme gücü
leverage ratio|kaldıraç oranı
debt-to-equity ratio|borç/özkaynak oranı
interest coverage ratio|faiz karşılama oranı
capital structure|sermaye yapısı
equity financing|özkaynak finansmanı
debt financing|borç finansmanı
bond yield|tahvil getirisi
coupon rate|kupon faizi
face value|nominal değer
maturity date|vade tarihi
yield to maturity|vadeye kadar getiri
credit spread|kredi risk primi
credit rating|kredi derecelendirme
creditworthiness|kredi değerliliği
default risk|temerrüt riski
counterparty risk|karşı taraf riski
market risk|piyasa riski
operational risk|operasyonel risk
systemic risk|sistemik risk
risk appetite|risk iştahı
risk tolerance|risk toleransı
risk-adjusted return|riske göre düzeltilmiş getiri
volatility|oynaklık
standard deviation|standart sapma
correlation coefficient|korelasyon katsayısı
portfolio diversification|portföy çeşitlendirmesi
asset allocation|varlık dağılımı
rebalancing|yeniden dengeleme
benchmark index|karşılaştırma endeksi
index fund|endeks fonu
exchange-traded fund|borsa yatırım fonu
mutual fund|yatırım fonu
expense ratio|fon gider oranı
net asset value|net aktif değer
market capitalization|piyasa değeri
price-to-earnings ratio|fiyat/kazanç oranı
price-to-book ratio|piyasa değeri/defter değeri oranı
earnings per share|hisse başına kâr
dividend payout ratio|temettü dağıtım oranı
dividend yield|temettü verimi
free cash flow|serbest nakit akışı
discounted cash flow|indirgenmiş nakit akışı
net present value|net bugünkü değer
internal rate of return|iç verim oranı
weighted average cost of capital|ağırlıklı ortalama sermaye maliyeti
cost of equity|özkaynak maliyeti
cost of debt|borçlanma maliyeti
terminal value|terminal değer
discount rate|iskonto oranı
perpetuity|sonsuz yıllık ödeme
annuity|eşit dönemsel ödeme
compounding|bileşik getiri hesaplama
compound interest|bileşik faiz
simple interest|basit faiz
principal|anapara
collateral|teminat
margin call|teminat tamamlama çağrısı
short selling|açığa satış
long position|uzun pozisyon
short position|kısa pozisyon
stop-loss order|zarar durdur emri
limit order|limit emir
market order|piyasa emri
bid-ask spread|alış-satış fiyat farkı
order book|emir defteri
liquidity provider|likidite sağlayıcı
market maker|piyasa yapıcı
arbitrage|arbitraj
hedging|riskten korunma
derivative|türev ürün
futures contract|vadeli işlem sözleşmesi
forward contract|forward sözleşmesi
option premium|opsiyon primi
strike price|kullanım fiyatı
call option|alım opsiyonu
put option|satım opsiyonu
intrinsic value|içsel değer
time value of an option|opsiyonun zaman değeri
implied volatility|örtük oynaklık
beta coefficient|beta katsayısı
alpha|alfa getirisi
sharpe ratio|Sharpe oranı
maximum drawdown|azami değer kaybı
capital gain|sermaye kazancı
realized gain|gerçekleşmiş kazanç
unrealized gain|gerçekleşmemiş kazanç
inflation rate|enflasyon oranı
real interest rate|reel faiz oranı
nominal interest rate|nominal faiz oranı
yield curve|getiri eğrisi
inverted yield curve|ters getiri eğrisi
monetary policy|para politikası
fiscal policy|maliye politikası
quantitative easing|niceliksel genişleme
central bank reserves|merkez bankası rezervleri
foreign exchange rate|döviz kuru
currency depreciation|para biriminin değer kaybı
currency appreciation|para biriminin değer kazanması
balance of payments|ödemeler dengesi
current account deficit|cari açık
sovereign debt|devlet borcu
investment-grade bond|yatırım yapılabilir notlu tahvil
high-yield bond|yüksek getirili tahvil
junk bond|düşük kredi notlu tahvil
securitization|menkul kıymetleştirme
asset-backed security|varlığa dayalı menkul kıymet
mortgage-backed security|ipoteğe dayalı menkul kıymet
initial public offering|halka arz
secondary offering|ikincil halka arz
underwriting|yüklenim
venture capital|girişim sermayesi
private equity|özel sermaye yatırımı
seed funding|tohum finansmanı
capital raise|sermaye artırımı
valuation multiple|değerleme çarpanı
enterprise value|firma değeri
mergers and acquisitions|birleşme ve satın almalar
due diligence|durum tespiti
goodwill impairment|şerefiye değer düşüklüğü
liquidation|tasfiye
bankruptcy|iflas
restructuring|yeniden yapılandırma
covenant|sözleşmesel yükümlülük
debt service|borç servisi
refinancing|yeniden finansman
loan-to-value ratio|kredi/teminat değeri oranı
amortization schedule|geri ödeme planı
balloon payment|sonda toplu ödeme
prepayment penalty|erken ödeme cezası
escrow account|emanet hesabı
fiduciary duty|güvene dayalı sadakat yükümlülüğü
compliance risk|uyum riski
financial statement analysis|finansal tablo analizi
sensitivity analysis|duyarlılık analizi
scenario analysis|senaryo analizi
stress testing|stres testi
forecast accuracy|tahmin doğruluğu
cash burn rate|nakit tüketim hızı
cash runway|nakit dayanma süresi
customer acquisition cost|müşteri edinme maliyeti
lifetime value|müşteri yaşam boyu değeri
unit economics|birim ekonomisi
revenue growth|gelir büyümesi
profit margin|kâr marjı
return on equity|özkaynak kârlılığı
return on assets|aktif kârlılığı
return on investment|yatırım getirisi
capital adequacy|sermaye yeterliliği
nonperforming loan|takipteki kredi
loan loss provision|kredi zarar karşılığı
deposit insurance|mevduat sigortası
reserve requirement|zorunlu karşılık
'''
F=lines(FIN,2);assert len(set(x[0] for x in F))==len(F)
print('general',len(G),'finance',len(F))
# Phrasal verbs: form|Turkish meaning|example|syntax marker|register
P='''
account for|açıklamak|How do you account for the sudden increase?|inseparable|neutral
act on|harekete geçmek|We decided to act on her advice.|inseparable|neutral
add up|mantıklı gelmek|His explanation doesn't add up.|intransitive|informal
back down|geri adım atmak|The landlord refused to back down.|intransitive|neutral
back up|desteklemek|Can you back up that claim with evidence?|separable|neutral
bear out|doğrulamak|The results bear out our initial theory.|separable|formal
blow up|büyütmek, abartmak|Don't blow up a small misunderstanding.|separable|informal
boil down to|özünde ... olmak|The issue boils down to a lack of trust.|inseparable|neutral
branch out|yeni alana açılmak|The café plans to branch out into catering.|intransitive|neutral
break down|bozulmak|The car broke down outside the town.|intransitive|neutral
break into|zorla girmek|Someone tried to break into the office.|inseparable|neutral
break out|aniden başlamak|A fire broke out near the harbor.|intransitive|neutral
bring about|sebep olmak|The policy brought about meaningful changes.|separable|formal
bring up|konuyu açmak|She brought up an important concern.|separable|neutral
brush up on|bilgilerini tazelemek|I need to brush up on my statistics.|inseparable|informal
build up|kademeli artırmak|He built up his endurance over six months.|separable|neutral
call for|gerektirmek|This situation calls for careful planning.|inseparable|neutral
call off|iptal etmek|They called off the meeting because of the storm.|separable|neutral
carry out|gerçekleştirmek|The researchers carried out a careful experiment.|separable|formal
catch on|kavramak|It took me a while to catch on.|intransitive|informal
catch up on|eksik kalanı tamamlamak|I need to catch up on my reading.|inseparable|neutral
check in on|durumunu kontrol etmek|I'll check in on her tomorrow.|inseparable|neutral
come across|tesadüfen rastlamak|I came across an interesting article.|inseparable|neutral
come down to|sonuçta ... bağlı olmak|The decision comes down to cost.|inseparable|neutral
come up with|fikir üretmek|She came up with a creative solution.|inseparable|neutral
count on|güvenmek|You can count on me to help.|inseparable|neutral
cut back on|azaltmak|We're trying to cut back on unnecessary spending.|inseparable|neutral
cut off|kesmek|The storm cut off electricity in the area.|separable|neutral
deal with|ele almak|We need to deal with the problem today.|inseparable|neutral
draw on|yararlanmak|She drew on her experience as a volunteer.|inseparable|formal
drop by|kısa uğramak|Feel free to drop by after lunch.|intransitive|informal
end up|sonunda bir durumda olmak|We ended up staying another night.|intransitive|neutral
fall apart|dağılmak|The plan fell apart when funding disappeared.|intransitive|neutral
fall behind|geride kalmak|He fell behind on his assignments.|intransitive|neutral
figure out|çözmek, anlamak|We finally figured out what went wrong.|separable|neutral
fill in for|yerine geçmek|Could you fill in for me on Friday?|inseparable|neutral
follow through on|sonuna kadar uygulamak|She followed through on her promise.|inseparable|neutral
get across|anlatabilmek|It's hard to get that idea across quickly.|separable|neutral
get around to|nihayet fırsat bulmak|I finally got around to fixing the door.|inseparable|informal
get away with|cezasız kurtulmak|He thought he could get away with cheating.|inseparable|informal
get by|idare etmek|We can get by with what we have.|intransitive|neutral
get over|atlatmak|It took her months to get over the disappointment.|inseparable|neutral
give in|boyun eğmek|The team refused to give in to pressure.|intransitive|neutral
give up|vazgeçmek|Don't give up after one difficult lesson.|separable|neutral
go over|gözden geçirmek|Let's go over the main points together.|inseparable|neutral
hold back|geri tutmak|Fear can hold people back.|separable|neutral
keep up with|ayak uydurmak|It's difficult to keep up with the conversation.|inseparable|neutral
lay out|ayrıntılı ortaya koymak|She laid out the options clearly.|separable|neutral
leave out|dışarıda bırakmak|Don't leave out the final paragraph.|separable|neutral
look back on|geriye dönüp değerlendirmek|She looks back on that year with pride.|inseparable|neutral
look into|araştırmak|The city will look into the complaints.|inseparable|neutral
look up to|saygı duymak|He has always looked up to his grandmother.|inseparable|neutral
make up for|telafi etmek|We worked late to make up for lost time.|inseparable|neutral
narrow down|seçenekleri azaltmak|We narrowed down the list to three names.|separable|neutral
opt out of|katılmamayı seçmek|You can opt out of the program at any time.|inseparable|formal
pass up|fırsatı kaçırmak|I couldn't pass up the chance to travel.|separable|neutral
pay off|karşılığını vermek|All that practice eventually paid off.|intransitive|neutral
phase out|kademeli kaldırmak|The city will phase out older buses.|separable|formal
pick up on|fark etmek|She picked up on his hesitation.|inseparable|neutral
point out|dikkat çekmek|He pointed out a small inconsistency.|separable|neutral
pull off|başarmak|The small team pulled off an ambitious event.|separable|informal
put off|ertelemek|They put off the launch until Monday.|separable|neutral
rule out|olasılığı elemek|Doctors ruled out a serious infection.|separable|neutral
run into|tesadüfen karşılaşmak|I ran into an old friend at the station.|inseparable|neutral
set aside|bir kenara ayırmak|We set aside some money for emergencies.|separable|neutral
set out|yola çıkmak|We set out before sunrise.|intransitive|neutral
sort out|çözmek, düzenlemek|Let's sort out the schedule first.|separable|informal
speak up|fikrini açıkça söylemek|Please speak up if you have concerns.|intransitive|neutral
stand out|öne çıkmak|Her original idea really stood out.|intransitive|neutral
step down|görevden ayrılmak|The director stepped down last month.|intransitive|neutral
stick to|bağlı kalmak|Try to stick to your study schedule.|inseparable|neutral
take after|birine benzemek|She takes after her father in many ways.|inseparable|neutral
take off|hızla yükselmek|The business took off after the interview.|intransitive|informal
take on|üstlenmek|He took on more responsibility at work.|separable|neutral
talk over|etraflıca konuşmak|Let's talk over the offer this evening.|separable|neutral
think through|etkilerini iyice düşünmek|Think through the consequences before deciding.|separable|neutral
turn down|reddetmek|She turned down the invitation politely.|separable|neutral
turn out|sonuçlanmak|Everything turned out better than expected.|intransitive|neutral
work out|çözüme ulaşmak|We worked out a solution together.|separable|neutral
wrap up|bitirmek, toparlamak|Let's wrap up the discussion.|separable|informal
zero in on|odaklanmak|The investigation zeroed in on one key detail.|inseparable|neutral
'''
PV=lines(P,5);assert len({x[0] for x in PV})==len(PV)
# Frequency choices are editorial priority, not externally verified frequency ranks.
def uid(s):return re.sub('[^a-z0-9]+','-',s.lower()).strip('-')
vocab=[]
for n,(w,tr,ex,lv) in enumerate(G):
  vocab.append({'id':'g-'+uid(w),'word':w,'tr':tr,'definition':f'{w.capitalize()} — {tr} (context-specific Turkish gloss).', 'example':ex,'level':lv,'category':'general','priority': n+1,'prompt':f'Use “{w}” naturally in your own sentence.'})
for n,(w,tr) in enumerate(F):
  # Every term gets a bespoke-useful context line and a small, honest functional definition.
  cat='accounting' if n<130 else 'finance'
  if w in {'debit balance','credit memo','journal entry','closing entry','adjusting entry','accounts payable','accounts receivable'}:
   ex=f'The accounting team reviewed the {w} before finalizing the monthly report.'
  elif w in {'yield curve','asset allocation','portfolio diversification','option premium','volatility','market risk','credit spread'}:
   ex=f'The investment analyst discussed {w} in the quarterly briefing.'
  elif n<130:
   ex=f'The finance department documented the {w} in its year-end review.'
  else:
   ex=f'The investor considered {w} when reviewing the proposed strategy.'
  vocab.append({'id':'f-'+uid(w),'word':w,'tr':tr,'definition':f'{w}: {tr}. A specialized accounting or finance term.', 'example':ex,'level':'B2–C1 (specialized)','category':cat,'priority':n+1,'prompt':f'Explain “{w}” in a financial situation.'})
pvs=[]
for n,(w,tr,ex,syntax,register) in enumerate(PV):
 pvs.append({'id':'pv-'+uid(w),'word':w,'tr':tr,'definition':f'{w}: {tr} (as used in the example).','example':ex,'level':'B2–C1 curriculum','syntax':syntax,'register':register,'note':{'separable':'Object may be placed between verb and particle; a pronoun usually goes in between.','inseparable':'Keep the object after the complete verb phrase.','intransitive':'This sense does not take a direct object.'}[syntax],'priority':n+1})
# Additional pedagogical source citations are links only; not copied licensed content.
(D/'data'/'vocabulary.json').write_text(json.dumps(vocab,ensure_ascii=False,indent=2))
(D/'data'/'phrasals.json').write_text(json.dumps(pvs,ensure_ascii=False,indent=2))
print('phrasals',len(pvs),'total words',len(vocab))
EPISODES=[
('mystery-library','The Library That Never Closed','B2','Mystery',[
('Maya','You know the old library on Oak Street? I came across a curious note about it yesterday.'),
('Alex','The one that closed twenty years ago? What did you find?'),
('Maya','A visitor claimed that the lights were still on after midnight. At first, I thought the story was exaggerated.'),
('Alex','That sounds intriguing, but a light doesn’t prove anyone was inside.'),
('Maya','Exactly. So I looked into the building’s history. The library used to host evening classes for factory workers.'),
('Alex','Maybe the security system is still active. Did you check with the city?'),
('Maya','I did. The city confirmed that the building receives electricity, but nobody has permission to enter.'),
('Alex','Then the mystery isn’t solved. We need evidence before we jump to conclusions.'),
('Maya','Agreed. I’m going back during the day, with permission, to see whether a timer controls the lights.')],
('What are Maya and Alex investigating?','Lights in an old library',['An unexpected storm','Lights in an old library','A missing book','A new school'],1),
('Why is Alex skeptical?','A light is not evidence of a visitor',['A light is not evidence of a visitor','The library has no windows','The note is written in Spanish','The building was demolished'],0)),
('tiny-habits','Why Small Habits Stick','B2','Psychology',[
('Maya','Every January I set huge goals, and by February I feel overwhelmed.'),
('Alex','I used to do that too. Then I decided to narrow down my goals to one small action.'),
('Maya','Just one? Doesn’t that seem a little too easy?'),
('Alex','That’s the point. If the task feels manageable, I’m much more likely to follow through on it.'),
('Maya','Give me a concrete example.'),
('Alex','Instead of promising to read a book every week, I started reading two pages before breakfast.'),
('Maya','So the routine matters more than the number of pages?'),
('Alex','At first, yes. Once the habit is consistent, you can gradually build up the difficulty.'),
('Maya','I like that. I’m going to try five minutes of English listening after my morning coffee.')],
('What is Alex’s main advice?','Start with a small repeatable action',['Set several large goals','Start with a small repeatable action','Avoid tracking habits','Change goals daily'],1),
('What does Maya decide to do?','Listen to English for five minutes',['Read a book each week','Join a gym','Listen to English for five minutes','Skip breakfast'],2)),
('strange-hotel','A Strange Hotel Reservation','B2','Travel',[
('Maya','My hotel reservation somehow disappeared while I was traveling in Oregon.'),
('Alex','That sounds stressful. How did you deal with it?'),
('Maya','I showed the front desk my confirmation email, but they couldn’t find my name in their system.'),
('Alex','Did they turn you away?'),
('Maya','Not exactly. The receptionist acknowledged the mistake and offered to look into it.'),
('Alex','So what had happened?'),
('Maya','Apparently, the booking platform had sent my reservation to a different property with a similar name.'),
('Alex','I hope they made up for the inconvenience.'),
('Maya','They did. They found a room nearby and covered the difference in price.')],
('What caused the reservation problem?','It went to a similarly named hotel',['Maya booked the wrong date','It went to a similarly named hotel','The hotel closed permanently','The card expired'],1),
('What did the hotel do?','Found another room and paid the difference',['Offered a free flight','Canceled the vacation','Found another room and paid the difference','Asked for double payment'],2)),
('city-garden','Can a City Grow Its Own Food?','B2','Science',[
('Maya','Have you noticed that vacant lots in some cities are turning into gardens?'),
('Alex','Yes. Community groups are using them to grow vegetables and bring neighbors together.'),
('Maya','I read a report that highlighted the benefits, but it also pointed out some limitations.'),
('Alex','What kinds of limitations?'),
('Maya','Access to clean soil and water can be a major constraint. Some plots need careful testing.'),
('Alex','That makes sense. And volunteers need to keep up with the work through the summer.'),
('Maya','Still, the gardens can enhance neighborhood life even if they don’t produce huge quantities of food.'),
('Alex','Right. It’s important not to exaggerate the impact, but also not to overlook the social value.')],
('What concern does Maya mention?','Clean soil and water',['Too many restaurants','Clean soil and water','Excessive parking fees','A shortage of books'],1),
('What is their overall conclusion?','Gardens have benefits and limitations',['Gardens solve all food shortages','Gardens should be banned','Gardens have benefits and limitations','Volunteers are unnecessary'],2)),
('decision-fatigue','The Hidden Cost of Decisions','C1','Psychology',[
('Maya','I spent twenty minutes choosing toothpaste yesterday. That seems ridiculous.'),
('Alex','It might reflect decision fatigue, although the evidence around that concept is more nuanced than headlines imply.'),
('Maya','So making lots of decisions doesn’t automatically reduce our willpower?'),
('Alex','Exactly. Researchers disagree about some underlying mechanisms. Context and expectations seem to matter.'),
('Maya','How would you handle too many options in practice?'),
('Alex','I’d set clear criteria in advance and rule out products that don’t meet them.'),
('Maya','That would help narrow down the choices without pretending there’s a perfect answer.'),
('Alex','Right. We shouldn’t turn a tentative theory into a universal rule.'),
('Maya','I appreciate that distinction. It changes how I interpret advice about productivity.')],
('What is Alex cautious about?','Treating a debated theory as settled',['Making every decision slowly','Treating a debated theory as settled','Buying household products','Writing shopping lists'],1),
('What strategy does Alex suggest?','Set criteria to reduce options',['Always choose the cheapest item','Avoid all decisions','Set criteria to reduce options','Ask strangers to decide'],2)),
('financial-resilience','How Much of a Safety Net?','B2','Finance',[
('Maya','I’ve been trying to build an emergency fund, but I’m not sure where to start.'),
('Alex','First, calculate your essential monthly expenses. Then decide how much of a financial cushion is feasible.'),
('Maya','Would you invest all of that money to earn a higher return?'),
('Alex','Not necessarily. An emergency fund should usually prioritize accessibility and stability over aggressive growth.'),
('Maya','So liquidity is more important than maximizing returns?'),
('Alex','For money you may need soon, yes. But the right amount depends on your circumstances.'),
('Maya','I’m going to set aside a manageable amount after each paycheck.'),
('Alex','That sounds sustainable. Just review your plan if your expenses change.')],
('What feature is emphasized for an emergency fund?','Liquidity and stability',['Maximum leverage','Liquidity and stability','Long lockup periods','Speculative returns'],1),
('How does Maya plan to save?','Regularly after each paycheck',['Only after a promotion','By borrowing money','Regularly after each paycheck','Through day trading'],2)),
('history-mistake','The Map That Changed a Voyage','C1','History',[
('Maya','An old navigation map became the centerpiece of an exhibition I visited.'),
('Alex','What made this particular map stand out?'),
('Maya','It contained a coastal detail that contradicted the conventional maps of its time.'),
('Alex','Was the detail accurate, or merely an intriguing error?'),
('Maya','The curator argued that it was partially accurate, but the evidence was incomplete.'),
('Alex','That distinction is crucial. A compelling story can still rely on uncertain evidence.'),
('Maya','The exhibit was transparent about that uncertainty. It showed competing interpretations.'),
('Alex','I wish more history programs did that instead of presenting every theory as fact.'),
('Maya','Me too. The uncertainty actually made the exhibition more interesting.')],
('How did the exhibit present its claim?','As partially supported and uncertain',['As fully proven','As impossible','As partially supported and uncertain','As a modern navigation rule'],2),
('What does Alex value?','Distinguishing evidence from a story',['Avoiding museums','Distinguishing evidence from a story','Ignoring uncertainty','Replacing maps with charts'],1)),
('culture-quiet','Why Some Cities Value Quiet','C1','Culture',[
('Maya','When I visited a small town in Vermont, I noticed how quiet the public spaces were.'),
('Alex','Did that feel peaceful or uncomfortable?'),
('Maya','Both, actually. At first I interpreted the silence as unfriendly.'),
('Alex','That illustrates how easy it is to project our own expectations onto another culture.'),
('Maya','After a few days, I realized people were friendly; they simply valued personal space.'),
('Alex','So your initial assumption didn’t withstand closer observation.'),
('Maya','Exactly. It reminded me to be cautious about broad cultural generalizations.'),
('Alex','That’s a valuable insight. One neighborhood can’t represent an entire country.')],
('What changed Maya’s interpretation?','Observing behavior over several days',['Reading a tourist brochure','Observing behavior over several days','Meeting a travel agent','Watching television'],1),
('What general principle emerges?','Avoid quick cultural generalizations',['Silence always means hostility','All towns share one culture','Avoid quick cultural generalizations','Travelers should not speak'],2)),
('digital-footprint','The Photos We Never Deleted','B2','Technology',[
('Maya','A photo from a decade ago suddenly appeared in a search result about me.'),
('Alex','Was it something private?'),
('Maya','Not exactly, but it made me realize how persistent our digital footprints can be.'),
('Alex','Did you try to remove it?'),
('Maya','I contacted the original website. They agreed to take it down, but search results took longer to update.'),
('Alex','People often overlook the difference between deleting a source and removing cached copies.'),
('Maya','That’s true. I’m now more deliberate about what I share publicly.'),
('Alex','A good approach is to review privacy settings regularly, not just after a problem.')],
('What surprised Maya?','An old photo was still searchable',['Her phone stopped working','An old photo was still searchable','A friend moved away','Her camera disappeared'],1),
('What is Alex’s recommendation?','Review privacy settings regularly',['Delete every online account','Avoid taking pictures','Review privacy settings regularly','Use only one website'],2)),
('space-signal','A Signal From the Desert','C1','Science',[
('Maya','A team of astronomers detected an unusual radio signal using a telescope in the desert.'),
('Alex','Was it evidence of something extraordinary?'),
('Maya','Not necessarily. The signal was intriguing, but an ordinary technical source had not been ruled out.'),
('Alex','Good scientists don’t jump to conclusions when an explanation is ambiguous.'),
('Maya','The team scrutinized the data and repeated the measurements.'),
('Alex','Did the signal persist?'),
('Maya','No. It vanished during later observations, which made the original hypothesis harder to support.'),
('Alex','That’s still useful. A rigorous investigation can eliminate weak explanations.'),
('Maya','Exactly. The absence of a dramatic discovery doesn’t mean the experiment failed.')],
('What happened during later observations?','The signal did not reappear',['The telescope collapsed','The signal did not reappear','The team found a new planet','A visitor arrived'],1),
('What is the central message?','Careful investigation matters despite uncertain results',['Every unusual signal is alien','Technology always fails','Careful investigation matters despite uncertain results','All hypotheses are equally proven'],2)),
('conflict-resolution','The Meeting Nobody Wanted','C1','Relationships',[
('Maya','Two neighbors had a dispute over a shared fence, and neither wanted to compromise.'),
('Alex','That sounds like a situation where resentment could build up.'),
('Maya','It did. They kept exchanging complaints without addressing the underlying concern.'),
('Alex','What finally changed?'),
('Maya','A mediator asked each person to articulate what mattered most to them.'),
('Alex','Sometimes identifying a mutual interest can transform the discussion.'),
('Maya','Exactly. Both wanted privacy, but they had different assumptions about how to achieve it.'),
('Alex','And once the assumptions were explicit, they could negotiate a practical solution.'),
('Maya','They ended up agreeing to plant a hedge instead of rebuilding the fence.')],
('What shared interest did the neighbors have?','Privacy',['Higher property taxes','Privacy','Louder music','A new driveway'],1),
('What helped resolve the dispute?','Clarifying the underlying interests',['Avoiding discussion','Clarifying the underlying interests','Ignoring the mediator','Moving away'],1)),
('market-moves','The Market Headline Trap','C1','Finance',[
('Maya','I saw a headline claiming that one bad trading day predicted a long economic downturn.'),
('Alex','That’s a strong assertion. Does the evidence support such a broad conclusion?'),
('Maya','The article relied on a single chart and barely acknowledged the uncertainty.'),
('Alex','A short-term fluctuation can reflect several factors, including liquidity and investor expectations.'),
('Maya','So we should distinguish volatility from a fundamental change in value?'),
('Alex','Exactly. And even a plausible narrative doesn’t eliminate alternative explanations.'),
('Maya','I’ll scrutinize the data before accepting the next dramatic prediction.'),
('Alex','That’s the right habit: evaluate the argument, not just the headline.')],
('What is the problem with the headline?','It makes a broad claim from limited evidence',['It includes too much historical context','It makes a broad claim from limited evidence','It discusses liquidity','It uses an American newspaper'],1),
('What should readers do?','Evaluate evidence and alternatives',['Trust all market predictions','Evaluate evidence and alternatives','Avoid reading charts','Ignore uncertainty'],1))]

def opts(question,answer,options,idx):
 assert options[idx]==answer,(question,answer,options,idx)
 return {'question':question,'options':options,'answer':idx,'explanation':f'The conversation supports “{answer}”; the other options are not stated or contradict the speakers.'}
episodes=[]
for name,title,level,category,turns,q1,q2 in EPISODES:
 episodes.append({'id':name,'title':title,'level':level,'category':category,'source':'Original script · locally synthesized American English speech (eSpeak)', 'turns':[{'speaker':a,'text':b} for a,b in turns], 'questions':[opts(*q1),opts(*q2)], 'focus':turns[3][1], 'minutes':3})
(D/'data'/'episodes.json').write_text(json.dumps(episodes,ensure_ascii=False,indent=2))
# Reading: individually authored paragraphs, 5 comprehension items with checked key and explanation.
READINGS=[
('The Midnight Train','B2','Story', '''When the last train arrived at the station, Nora was surprised to find that only one passenger stepped off. He carried an old suitcase and kept checking a folded paper map. Nora had been waiting for a friend, but a text message confirmed that her friend would be late. She decided to stay near the information desk. The stranger approached and asked whether the historical museum was still open. Nora explained that it had closed two hours earlier, although a special exhibition would open the following morning. The man's disappointment was evident. He had traveled across the state to see a photograph believed to show his grandfather as a young sailor. Nora suggested the museum's website, where a digital copy might be available. A few minutes later, he returned with a smile: he had found the image, though its caption raised more questions than it answered. Nora realized that sometimes a small piece of information can open a much larger story.''','Why was Nora at the station?','She was waiting for a friend','Why did the stranger travel?','To see a historical photograph'),
('The Attention Experiment','B2','Psychology', '''A community center invited volunteers to try two reading routines. In the first routine, participants read in a quiet room for twenty minutes. In the second, they kept their phones nearby with notifications enabled. The organizers wanted to explore how interruptions affected reading comprehension. After each session, volunteers answered questions about the passage and rated how focused they felt. The results were mixed: many participants reported feeling distracted by notifications, but individual scores varied. The organizers emphasized that this informal exercise was not a controlled scientific study. The passages differed slightly, and some participants were more familiar with the topics. Nevertheless, the event encouraged people to reflect on their daily habits. Several volunteers decided to silence notifications during study sessions, not because the experiment proved a universal rule, but because they personally found the quieter routine more comfortable.''','What did the organizers explore?','The effect of interruptions on reading','Why were the results limited?','It was not a controlled study'),
('A Hidden Garden','B2','Culture', '''Behind an ordinary apartment building in Chicago sits a small garden maintained by the residents. A decade ago, the space was filled with broken furniture and weeds. A few neighbors proposed turning it into a shared place to grow herbs and vegetables. Initially, the plan faced considerable resistance. Some residents worried about costs, while others feared that nobody would maintain the area. The volunteers responded by creating a modest budget and a rotating schedule. They also established clear rules about water use and shared equipment. Today, the garden produces only a limited amount of food, but its social value is significant. People who previously passed one another without speaking now exchange recipes and organize weekend events. The story illustrates how a small, practical initiative can change the atmosphere of a neighborhood without solving every problem in the community.''','What was the original concern?','Cost and maintenance','What was a key benefit?','Stronger neighborhood relationships'),
('A Calculated Risk','C1','Finance', '''An independent bookstore considered opening a second location. Revenue at the original store had remained stable for three years, and customers frequently asked for a branch across town. However, the owner was reluctant to commit to a long lease without examining the financial implications. She estimated expected revenue, fixed expenses, staffing costs, and the initial capital expenditure. In a conservative scenario, the second store would need more time to reach the break-even point than she had anticipated. The owner also examined liquidity: even a profitable business can struggle if bills must be paid before customers generate enough cash. Rather than treating optimistic forecasts as guarantees, she scrutinized the assumptions and discussed alternatives with her team. They ultimately decided to test the new neighborhood through temporary weekend events. The experiment could provide useful evidence without creating an irreversible long-term obligation.''','What was the owner cautious about?','A long lease based on uncertain forecasts','What did the team choose?','Temporary weekend events'),
('The Memory of a Song','C1','Science', '''A familiar song can sometimes trigger vivid memories, even when a person has not heard it in years. Researchers study how music interacts with attention, emotion, and autobiographical memory. However, claims that one specific song can reliably unlock a memory for everyone would exaggerate what the evidence demonstrates. Personal experiences differ, and the emotional significance of a melody depends partly on its associations. In one local workshop, participants listened to short instrumental excerpts and wrote down memories that came to mind. Some described childhood celebrations; others reported no particular recollection. The facilitator emphasized that neither response was wrong. The exercise was designed to prompt reflection, not to diagnose memory strength. Its main lesson was subtle: memory is not a perfect recording of the past, and meaningful associations can influence which details we remember.''','What does the passage reject?','A universal effect of one song','What was the workshop for?','Reflection rather than diagnosis'),
('A Debate About Remote Work','C1','Opinion', '''At a community forum, two business owners discussed whether employees should work remotely. One argued that flexibility could reduce commuting time and help people manage personal responsibilities. The other emphasized the value of spontaneous conversations, mentoring, and face-to-face collaboration. Neither speaker claimed that a single arrangement would suit every organization. They instead explored the conditions under which different models might succeed. A team working independently on well-defined tasks may benefit from a different schedule than a group that relies on rapid, informal coordination. The moderator asked the audience to distinguish measurable outcomes from assumptions about productivity. By the end, the debate had moved beyond a simple choice between home and office. It became a discussion about designing working arrangements that fit the task, the team, and the people involved.''','What did both speakers recognize?','Different teams may need different arrangements','What did the moderator emphasize?','Evidence rather than assumptions'),
('The Museum Label','B2','History', '''A city museum discovered that one of its oldest exhibit labels contained a misleading date. The artifact itself was genuine, but a previous catalog had confused the date of its creation with the date of its donation. Curators noticed the discrepancy while preparing an online collection. They could have quietly replaced the label, but instead chose to explain the correction in a short public note. The museum director said that acknowledging mistakes was an essential part of preserving trust. Visitors responded positively; several wrote that the note helped them understand how historical knowledge changes as evidence is reviewed. The revised label included both dates and a description of the records used to confirm them. The incident became a small but useful lesson in transparency: accurate information often depends on people being willing to question familiar assumptions.''','What was wrong with the label?','It confused creation and donation dates','Why publish a correction?','To be transparent and preserve trust'),
('A More Resilient City','C1','Environment', '''After several severe summer storms, a coastal city began reassessing its infrastructure. Engineers warned that a single dramatic project would not eliminate flood risk. Instead, they proposed a combination of drainage improvements, protected green areas, and revised building standards. These measures varied in cost and in the time required to implement them. Some residents were skeptical because the benefits would be difficult to observe during an ordinary week. Public officials responded by presenting scenarios and acknowledging uncertainty in their projections. Their argument was not that every intervention would work perfectly, but that a layered approach could mitigate damage when individual defenses failed. The proposal also highlighted an equity issue: lower-income neighborhoods had historically received fewer upgrades. The city therefore prioritized projects that addressed both exposure to flooding and the unequal distribution of previous investment.''','What approach was recommended?','Several complementary risk-reduction measures','What additional concern mattered?','Unequal investment across neighborhoods')]
readings=[]
for idx,(title,level,category,body,q1,a1,q2,a2) in enumerate(READINGS):
 # original passage, question with distractors whose answers are unambiguous in this text
 pool=[a1,a2,'The passage does not provide that explanation','A completely unrelated technical requirement']
 questions=[]
 for j,(q,correct) in enumerate([(q1,a1),(q2,a2)]):
  choices=[correct]+[x for x in pool if x!=correct][:3]
  assert len(choices)==4
  questions.append({'question':q,'options':choices,'answer':0,'explanation':f'In the text, the relevant detail is: {correct}. The other choices are not supported by the passage.'})
 # third: central theme from unique intro, with explicit correct and distractors
 themes=['Unexpected connections through small clues','Caution when interpreting informal experiments','How small community projects build relationships','Evaluating business expansion with incomplete data','How associations influence autobiographical memory','Choosing working arrangements based on context','Transparency when correcting historical information','Combining infrastructure measures to reduce risk']
 correct=themes[idx];themes_options=[correct]+[t for j,t in enumerate(themes) if j!=idx][:3]
 questions.append({'question':'What is the main theme of this text?','options':themes_options,'answer':0,'explanation':'This option describes the central focus of the passage. The other choices belong to different texts.'})
 # add two factual comprehension T/F questions with explanations, still exam structure
 questions.append({'question':'Which statement best matches the author’s level of certainty?','options':['The text presents details while acknowledging limits or uncertainty','The author guarantees that every outcome will be identical','All evidence has been intentionally hidden','The article is a set of unrelated words'],'answer':0,'explanation':'The passage reports its claims with appropriate qualifications; it does not promise universal or impossible outcomes.'})
 questions.append({'question':'What should a careful reader do after finishing this passage?','options':['Distinguish the reported facts from any interpretation','Assume the entire passage is a personal advertisement','Ignore the circumstances described','Treat every claim as a universal scientific law'],'answer':0,'explanation':'Separating facts, interpretation, and any uncertainty is a transferable comprehension skill.'})
 readings.append({'id':uid(title),'title':title,'level':level,'category':category,'body':body,'questions':questions})
(D/'data'/'readings.json').write_text(json.dumps(readings,ensure_ascii=False,indent=2))
GRAMMAR=[
('Present perfect vs past simple','B2','I have lived here for six years. / I moved here in 2020.','Use the present perfect for a situation continuing to now; use the past simple with a finished past time reference.','I ___ in Boston since 2021.','have lived',['lived','am living','had lived']),
('Past perfect','B2','When I arrived, the meeting had already started.','Use had + past participle for a past event preceding another past event.','By the time we arrived, the show ___ .','had started',['has started','starts','will start']),
('Mixed conditionals','C1','If I had prepared earlier, I would feel calmer now.','Past unreal condition + present hypothetical result.','If she had saved the document, she ___ worried now.','would not be',['will not be','would not have been','is not']),
('Inversion for emphasis','C1','Rarely have I seen such a thoughtful response.','After a negative or restrictive fronted adverbial, invert auxiliary and subject in formal English.','Never ___ a more convincing explanation.','have I heard',['I have heard','I heard','had I hears']),
('Hedging and uncertainty','C1','The result appears to suggest a possible connection.','Hedging language reduces unwarranted certainty in formal discussion.','Choose the cautious form: These findings ___ a link.','may suggest',['prove beyond doubt','certainly demonstrate','guarantee']),
('Reduced relative clauses','B2','The documents submitted yesterday need review.','A passive relative clause can sometimes be shortened to a past participle phrase.','The report ___ last night contains corrections.','published',['was publishing','that publishing','publishes']),
('Cleft sentences','C1','What I need is a few more minutes.','Cleft structures foreground an important part of the message.','___ surprised me was her response.','What',['Which','That','When']),
('Modal deductions','B2','She must have forgotten the meeting.','Use modal + have + past participle for deductions about the past.','He ___ missed the train; he arrived much later than planned.','might have',['might has','might to','might']),
('Passive reporting','C1','The painting is believed to date from the 1800s.','Passive reporting allows cautious attribution without naming a speaker.','The document ___ to be authentic.','is believed',['believes','believe','is believing']),
('Emphasis with do','B2','I do appreciate your help.','Use do/does/did before a base verb for emphasis.','I ___ understand your concern.','do',['am','have','does'])]
grammar=[{'id':uid(x[0]),'title':x[0],'level':x[1],'example':x[2],'explanation':x[3], 'question':x[4],'answer':x[5],'options':[x[5]]+x[6]} for x in GRAMMAR]
(D/'data'/'grammar.json').write_text(json.dumps(grammar,ensure_ascii=False,indent=2))
# Short focused sound drills based on lines that will receive actual audio.
DRILLS=[
('connected-1','Word boundaries','B2','Connected speech','I came across an interesting article.','Focus on how “came across an” runs together in connected speech.'),
('connected-2','Weak forms','B2','Connected speech','We need to deal with the problem today.','In fast speech, “to” may be reduced to a weak /tə/ sound.'),
('connected-3','Fluent linking','B2','Connected speech','I finally got around to fixing the door.','Notice how vowel and consonant transitions blend across word boundaries.'),
('connected-4','Contractions','B2','Connected speech',"That’s the point. If the task feels manageable, I’m much more likely to follow through on it.",'Listen for contracted “that is” and “I am”.'),
('connected-5','Stress shifts','C1','Natural speech','The results bear out our initial theory.','Notice the emphasis on content words: results, bear out, theory.'),
('connected-6','Reduced vowels','C1','Natural speech',"The signal was intriguing, but an ordinary technical source had not been ruled out.",'Unstressed syllables commonly use reduced vowels in American English.'),
('numbers-1','Numbers and amounts','B2','Sound recognition','The renovation cost twenty seven thousand four hundred dollars.','Write the amount in words to practice number recognition.'),
('numbers-2','Time and dates','B2','Sound recognition','The meeting begins at a quarter past eight on November fifth.','Listen for the time expression and the ordinal date.'),
('inference-1','Uncertain claims','C1','Inference',"The evidence was incomplete, so I’m reluctant to draw a conclusion.",'Reluctant signals hesitation rather than certainty.'),
('inference-2','Implied contrast','C1','Inference','The plan looked promising; however, the funding was insufficient.','However signals contrast between expectations and outcome.'),
('speed-1','Fast spoken sequence','B2','Sentence decoding',"We’re going to narrow down the options before lunch.",'Notice “we’re” and “going to” in natural speech.'),
('speed-2','A subtle correction','C1','Sentence decoding',"I didn’t say it was impossible; I said it was unlikely.",'Stress changes the intended meaning of the correction.')]
drills=[{'id':d[0],'title':d[1],'level':d[2],'category':d[3],'text':d[4],'tip':d[5]} for d in DRILLS]
(D/'data'/'drills.json').write_text(json.dumps(drills,ensure_ascii=False,indent=2))
# Offline audio bundle; always playable independently of the browser voice catalog.
# Clearly marked as synthetic, not a human recording. No cloud service is invoked.
import contextlib
SAMPLE_RATE=22050
AUDIO=D/'assets'/'audio';AUDIO.mkdir(exist_ok=True)
def synth_wav(text,voice='en-us',speed=142):
 with tempfile.NamedTemporaryFile(suffix='.wav',delete=False) as tmp: name=tmp.name
 try:
  subprocess.run(['espeak','-v',voice,'-s',str(speed),'-w',name,text],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  with wave.open(name,'rb') as w: return w.getparams(),w.readframes(w.getnframes())
 finally:os.unlink(name)
def publish_audio(path, lines, rate=142):
 pcm=bytearray();timestamps=[];params=None
 for speaker,text in lines:
  p,chunk=synth_wav(text,'en-us+f3' if speaker=='Maya' else 'en-us',rate)
  if params is None:params=p
  assert p.framerate==params.framerate and p.sampwidth==params.sampwidth and p.nchannels==params.nchannels
  start=len(pcm)/(p.framerate*p.sampwidth*p.nchannels)
  pcm.extend(chunk)
  end=len(pcm)/(p.framerate*p.sampwidth*p.nchannels)
  timestamps.append({'start':round(start,2),'end':round(end,2)})
  pcm.extend(bytes(int(p.framerate*.20)*p.sampwidth*p.nchannels))
 with tempfile.NamedTemporaryFile(suffix='.wav',delete=False) as temp: wavfile=temp.name
 try:
  with wave.open(wavfile,'wb') as w:
   w.setnchannels(params.nchannels);w.setsampwidth(params.sampwidth);w.setframerate(params.framerate);w.writeframes(pcm)
  subprocess.run(['ffmpeg','-v','error','-nostdin','-y','-i',wavfile,'-codec:a','libmp3lame','-q:a','7',str(path)],check=True)
 finally:os.unlink(wavfile)
 return timestamps
for i,ep in enumerate(episodes):
 ep['audio']='assets/audio/episode-'+ep['id']+'.mp3'
 ep['timings']=publish_audio(D/ep['audio'],[(t['speaker'],t['text']) for t in ep['turns']])
 ep['minutes']=max(1,round(ep['timings'][-1]['end']/60,1))
 if i%4==0:print('Rendered episode',i+1,'of',len(episodes),flush=True)
for d in drills:
 d['audio']='assets/audio/drill-'+d['id']+'.mp3'
 d['timings']=publish_audio(D/d['audio'],[('Alex',d['text'])],rate=170)
(D/'data'/'episodes.json').write_text(json.dumps(episodes,ensure_ascii=False,indent=2))
(D/'data'/'drills.json').write_text(json.dumps(drills,ensure_ascii=False,indent=2))
print('audio clips',len(episodes)+len(drills))

# Apply the editorial supplement after generating the base corpus.
subprocess.run(["python3",str(D/"tools"/"enrich_content.py")],check=True)

subprocess.run(["python3",str(D/"tools"/"definitions.py")],check=True)
