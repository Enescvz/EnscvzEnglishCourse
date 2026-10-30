"""Original authored private-development question/connector/preposition/sentence practice.
No third-party content reproduced. NOT independently editor-approved.
Deterministic generation: stable IDs, never changes legacy expression IDs.
"""
import json
from pathlib import Path

# Each row: stable slug, Turkish title, micro-rule, frequent error, level,
# 10 original model utterances. Models are reference answers, NOT exhaustive answer keys.
LESSONS = [
('yes-no','Yes/No Questions','Present simple: do/does + subject + base verb. Be ve modaller doğrudan öne gelir.','Does she works? → Does she work?','B1',[
'Do you live near here?','Does your sister work on Fridays?','Do they usually eat breakfast at home?','Does he speak English at work?','Do you have enough time?','Are you ready for the meeting?','Is the coffee still hot?','Can you come a little earlier?','Have you finished your homework?','Will you be there tomorrow?']),
('wh-questions','WH Questions','Wh-word + yardımcı fiil + özne + ana fiil (özne soruları hariç).','Where you live? → Where do you live?','B1',[
'Where do you usually have lunch?','What time does the store close?','Why did you change your mind?','How often do you practice English?','Which train should we take?','When are you leaving for Boston?','How much does this ticket cost?','Who are you waiting for?','What did you do after work?','How long have you lived here?']),
('tense-questions','Tense Questions','Zaman referansına göre yardımcı fiil: do/did/have/has/be/will.','Did you went? → Did you go?','B1',[
'Did you watch the game yesterday?','Have you ever visited Chicago?','Are you studying right now?','Were you working at eight last night?','Will you call me when you arrive?','How long have you known her?','What were you doing when I called?','Had you eaten before the movie started?','Are you going to apply next week?','Have you been waiting long?']),
('modal-questions','Modal Questions','Modal + subject + base verb; polite requests often use could/would.','Could you to help? → Could you help?','B1',[
'Could you speak a little more slowly?','Would you mind opening the window?','May I ask you a question?','Should we book a table in advance?','Can I pay by card?','Would you like some coffee?','Could I borrow your charger?','Must we submit the form today?','Might this cause a delay?','Would you be able to join us later?']),
('subject-questions','Subject Questions','Who/what özne olduğunda present simple sorularında do/does gerekmez.','Who did call you? → Who called you?','B2',[
'Who called you this morning?','What happened at the station?','Who knows the answer?','Which team won the final?','What makes this place special?','Who lives in that apartment?','What caused the power outage?','Who sent this email?','Which bus goes downtown?','What changed after the update?']),
('object-questions','Object Questions','Nesneyi sorarken yardımcı fiil kullanılır; who/what nesne, özne başka kişidir.','Who you called? → Who did you call?','B2',[
'Who did you call after the meeting?','What did she buy at the store?','Which book are you reading?','Who does your brother work with?','What are they discussing?','Which option did you choose?','Who have you invited to dinner?','What will you bring tomorrow?','Which movie did you recommend?','What have you learned this week?']),
('negative-questions','Negative Questions','Olumsuz soru şaşkınlık, beklenti veya nazik öneri ifade edebilir.','Why you did not tell me? → Why didn’t you tell me?','B2',[
'Why didn’t you tell me earlier?','Don’t you want to come with us?','Isn’t this your jacket?','Haven’t we met before?','Couldn’t we take a shorter route?','Didn’t you receive my message?','Wouldn’t it be easier to call?','Aren’t they supposed to arrive today?','Why hasn’t she replied yet?','Shouldn’t we check the address first?']),
('indirect-questions','Indirect Questions','Do you know + wh-clause: iç cümlede statement word order (where she lives).','Do you know where does she live? → Do you know where she lives?','B2',[
'Could you tell me where the station is?','Do you know what time the office opens?','I wonder why she left so early.','Could you explain how this works?','Do you happen to know whether he is available?','Can you tell me how much it costs?','Do you remember where we parked?','I was wondering if you could help me.','Do you know when the next train leaves?','Could you tell me who I should contact?']),
('question-tags','Question Tags','Positive statement + negative tag, negative statement + positive tag; yardımcı fiil ve özne eşleşir.','She works here, does she? → She works here, doesn’t she?','B2',[
'You live nearby, don’t you?','She isn’t coming, is she?','They have finished, haven’t they?','It was cold yesterday, wasn’t it?','He can drive, can’t he?','We should leave now, shouldn’t we?','You didn’t forget, did you?','This is your seat, isn’t it?','Let’s take a break, shall we?','I’m late, aren’t I?']),
('preposition-questions','Preposition Questions','Doğal günlük sorularda edat genellikle en sonda bulunabilir.','What are you looking? → What are you looking for?','B2',[
'What are you looking for?','Who are you talking to?','What are you worried about?','Which company do you work for?','What is this tool used for?','Who did you go with?','What are you interested in?','Which city did you move to?','What does this depend on?','What did you spend the money on?']),
('hypothetical-questions','Hypothetical Questions','Second conditional: What would + subject + base verb + if + past simple?','What will you do if you had...? → What would you do if you had...?','B2',[
'What would you do if you won a scholarship?','Where would you live if money weren’t an issue?','Would you change jobs if you had the chance?','How would you react if your flight were canceled?','What would happen if we missed the deadline?','Who would you call if you lost your phone?','Would you move abroad if you found a good job?','How would you explain this to a beginner?','What would you have done if you had known?','Would you have stayed if the offer had been better?']),
('follow-up-questions','Follow-up Questions','Belirsiz ayrıntıyı açmak için how/why/what/which ile doğal takip soruları üret.','And? → Could you tell me a little more about that?','B2',[
'What makes you say that?','Could you tell me a little more about it?','How did you come to that conclusion?','What happened after that?','Can you give me an example?','How long did that take?','What was the hardest part?','Why did you decide to do that?','How did the other person respond?','What would you do differently next time?']),
('prepositions-time','Time Prepositions','At saat/nokta, on gün/tarih, in ay/yıl/dönem; özel kalıpları ayrı öğren.','in Monday → on Monday','B1',[
'Let’s meet at nine thirty.','My birthday is in October.','The appointment is on Tuesday.','The class starts at noon.','We moved here in 2022.','I usually relax on the weekend.','The deadline is on November fifth.','We should leave in the morning.','The store closes at midnight.','I’ll see you on Friday afternoon.']),
('prepositions-place','Place Prepositions','At nokta/etkinlik, in kapalı alan veya şehir, on yüzey/ulaşım bağlamı.','at the room → in the room','B1',[
'She is waiting at the entrance.','The keys are on the kitchen table.','We live in Seattle.','He is in the conference room.','The picture is on the wall.','Let’s meet at the bus stop.','There is a bakery on this street.','The documents are in my bag.','She is on the bus right now.','I left my laptop at home.']),
('movement-prepositions','Movement Prepositions','Into içeri, onto yüzeye, through içinden, across bir taraftan diğerine.','walk across the tunnel → walk through the tunnel','B1',[
'Please walk through the tunnel.','The cat jumped onto the sofa.','We drove across the bridge.','He stepped into the elevator.','She ran out of the building.','The plane flew over the mountains.','Go past the library and turn left.','The children walked along the river.','We climbed up the stairs.','He came down the hill carefully.']),
('verb-preposition','Verb + Preposition','Edatı kelimeyle birlikte öğren: depend on, listen to, wait for.','listen music → listen to music','B2',[
'It depends on the weather.','Please listen to the instructions.','I’m waiting for my friend.','She applied for a new position.','We agreed on a date.','He apologized for the mistake.','They belong to the same club.','I’m thinking about moving abroad.','She insisted on paying the bill.','Can you explain this problem to me?']),
('adjective-preposition','Adjective + Preposition','Sıfatın aldığı edatı kalıp halinde çalış: interested in, good at, afraid of.','interested on → interested in','B2',[
'I’m interested in local history.','She’s very good at solving problems.','He’s afraid of flying.','We are proud of our progress.','I’m responsible for the report.','She is familiar with this software.','They are excited about the trip.','He was surprised by the result.','I’m grateful for your help.','This area is famous for its restaurants.']),
('noun-preposition','Noun + Preposition','İsimden sonra doğal edatları ayırt et: reason for, effect on, access to.','effect to → effect on','B2',[
'What is the reason for the delay?','There has been an increase in demand.','We need access to the building.','The decision had an effect on sales.','She has experience in customer service.','There is a solution to this problem.','The answer to your question is simple.','He made a contribution to the project.','The demand for housing is growing.','I have a strong interest in photography.']),
('because-during','Because / During / While','Because + clause, because of + noun; during + noun, while + clause.','during I was working → while I was working','B2',[
'We stayed inside because it was raining.','The game was canceled because of the storm.','I fell asleep during the movie.','Please don’t call while I’m driving.','We left early because we felt tired.','Because of the traffic, we arrived late.','She took notes during the lecture.','He listened to music while he studied.','The roads were closed because of the snow.','I met her during my first week at college.']),
('for-since-until','For / Since / Until','For süre, since başlangıç, until bitiş sınırı; by son teslim noktası.','since three years → for three years','B2',[
'I have worked here for three years.','She has lived here since 2020.','We waited until the rain stopped.','Please finish the report by Friday.','He has been asleep for two hours.','I haven’t seen her since Monday.','The shop stays open until ten.','You need to register by midnight.','We have known each other for years.','She has been studying since breakfast.']),
('to-for-with','To / For / With','To alıcı/yön, for amaç/yarar, with birliktelik veya araç.','explain me → explain to me','B2',[
'I sent the invitation to my colleague.','This gift is for your sister.','She opened the box with a knife.','Could you explain it to me?','We bought flowers for our neighbor.','He traveled to Denver with his family.','I used my phone to check the map.','The message was written for new students.','She shared the document with me.','I gave the receipt to the cashier.']),
('fixed-preposition-chunks','Fixed Preposition Chunks','Bağlamdaki sabit grupları bütün olarak öğren: on time, in time, at risk.','in time = on time (her zaman aynı değil)','B2',[
'The train arrived on time.','We got there just in time to board.','She is in charge of the team.','The project is at risk of delay.','Please keep in touch with us.','He is on his way to work.','The new rule is in effect now.','I’ll get back to you as soon as possible.','We are in favor of the proposal.','The hotel is within walking distance.']),
('cause-connectors','Cause Connectors','Because/since/as + clause; because of/due to + noun phrase.','because of it was late → because it was late','B1',[
'I took a taxi because I was late.','Since it was getting dark, we headed home.','The flight was delayed because of heavy fog.','As I had no cash, I paid by card.','The match was canceled due to bad weather.','She stayed home because she felt sick.','Since you’re already here, let’s begin.','The meeting ended early because of a power cut.','As traffic was light, we arrived ahead of schedule.','We changed our plans due to unexpected repairs.']),
('result-connectors','Result Connectors','So iki cümleyi bağlayabilir; therefore/as a result daha resmî geçiştir.','Because it rained, so we stayed. → Because it rained, we stayed.','B1',[
'It was raining, so we stayed inside.','He studied hard; therefore, he passed the exam.','The road was closed. As a result, we took a detour.','I forgot my charger, so my phone died.','The price increased; consequently, demand fell.','She missed the bus, so she walked.','They saved money; therefore, they could travel.','The files were lost. As a result, work was delayed.','The weather improved, so we went outside.','We practiced regularly; consequently, we improved.']),
('contrast-connectors','Contrast Connectors','Although/even though + clause; despite/in spite of + noun/-ing; however yeni cümleye geçer.','despite I was tired → despite being tired','B2',[
'Although it was late, we kept talking.','Despite the rain, the match continued.','I wanted to join; however, I had to work.','Even though she was nervous, she spoke clearly.','In spite of being tired, he kept studying.','Although the room was small, it felt comfortable.','The task was difficult; nevertheless, we finished it.','Despite having little time, she helped us.','I liked the hotel, but the service was slow.','Even though we disagreed, we stayed respectful.']),
('condition-connectors','Condition Connectors','If, unless (= if not), as long as, provided that koşul bildirir.','unless you don’t hurry → unless you hurry','B2',[
'If it rains, we’ll stay home.','Unless you hurry, you’ll miss the train.','You can borrow my laptop as long as you return it tonight.','We’ll start provided that everyone is ready.','If I finish early, I’ll call you.','You won’t improve unless you practice.','You may leave early as long as the work is done.','We can go hiking if the weather improves.','Provided that the payment arrives, we’ll ship it tomorrow.','Unless something changes, the meeting starts at ten.']),
('addition-connectors','Addition Connectors','Also günlük dilde; in addition/furthermore resmî ek bilgi verir.','Besides, additionally ... (bağlam olmadan biriktirmek)','B2',[
'The course is practical and also affordable.','In addition, you’ll receive weekly feedback.','The hotel is clean; furthermore, it is close to the station.','She speaks Spanish as well as English.','We need to check the cost. We also need to check the timing.','Besides being reliable, the service is fast.','The plan saves time; moreover, it reduces waste.','He enjoys reading and also likes hiking.','The report is clear. In addition, it includes useful examples.','The software is simple; furthermore, it works offline.']),
('comparison-connectors','Comparison Connectors','Whereas/while zıt özellikleri, on the other hand alternatif bakış açısını kurar.','while = always “-iken” değil; zıtlık da kurabilir','B2',[
'She prefers tea, whereas I prefer coffee.','While the first option is cheaper, the second is faster.','This phone is lighter than my old one.','The north is cooler, while the south is warmer.','On the one hand, the job pays well; on the other hand, it requires travel.','Unlike the previous version, this one works offline.','Both options are useful, but they serve different needs.','Whereas he likes crowds, I enjoy quiet places.','Compared with last year, sales have improved.','The train is faster; however, the bus is cheaper.']),
('examples-connectors','Giving Examples','For example/for instance cümleye; such as isim örneğine uygundur.','such as followed by full clause without adjustment','B1',[
'You can practice daily activities, such as ordering food.','For example, try asking for directions in English.','Some cities, such as Boston and Seattle, have excellent libraries.','I enjoy outdoor sports; for instance, I often go cycling.','There are several ways to save money, including cooking at home.','For example, you could ask a follow-up question.','She likes creative hobbies, such as drawing and photography.','Some tools are free; for instance, this dictionary costs nothing.','Many people learn through practice, including role-play.','We need specific examples, such as a recent customer request.']),
('sequence-connectors','Sequence & Time','First, then, meanwhile, eventually ve afterward olay sırası bildirir; meanwhile paralel süreçtir.','meanwhile = finally değil','B1',[
'First, open the app and choose a lesson.','Then, read the instructions carefully.','Meanwhile, I’ll prepare the materials.','Afterward, we can compare our answers.','Eventually, we found the correct address.','Before you leave, check the door.','As soon as she arrived, we started dinner.','While the food was cooking, I set the table.','Finally, save your progress before closing the app.','In the meantime, you can review the previous lesson.']),
('articles-quantifiers','Articles & Quantifiers','A/an tekil sayılabilir isim, the belirli referans; much/many/few/little miktar bildirir.','many information → much information','B1',[
'I need an umbrella because it’s raining.','The book you lent me was excellent.','There isn’t much time left.','How many people are coming?','We have a few questions about the plan.','There is a little milk in the fridge.','She works at a university.','I don’t have any cash with me.','Could you give me some advice?','The information you sent was useful.']),
('relative-pronouns','Pronouns & Relative Clauses','Who people, which things, that both restrictive; whose possession.','The person which called → The person who called','B2',[
'The woman who called yesterday is my neighbor.','This is the book that I mentioned.','I met someone whose brother lives in Denver.','The laptop, which I bought last year, still works well.','The restaurant where we met has closed.','That’s the reason why I stayed.','The colleague who helped me has left the company.','The movie that we watched was surprising.','She gave me a map, which was very helpful.','This is the place where I grew up.']),
('modals-conditionals','Modals & Conditionals','Could/should/might olasılık, tavsiye, izin; if cümleleri gerçek/varsayımsal sonuçları gösterir.','If I would have time → If I had time','B2',[
'You should check the schedule before leaving.','We might need more time to finish.','If I had a car, I would drive to work.','If you heat ice, it melts.','I could help you after lunch.','You mustn’t park in front of the entrance.','If she had studied, she would have passed.','We don’t have to leave yet.','You should have told me sooner.','If it stops raining, we can go for a walk.']),
('natural-sentence-flow','Natural Sentence Flow','Bağımsız cümleleri anlam ilişkisine göre birleştir; paralellik ve tutarlı zaman kullan.','Although ... but ... birlikte gereksiz olabilir','B2',[
'I wanted to go out, but I was too tired.','Although the task was challenging, we finished on time.','I was cooking when the phone rang.','She was nervous at first, but she gradually relaxed.','Because the train was delayed, we arrived late.','I prefer working in the morning because I can concentrate better.','The idea sounds promising; however, we need more evidence.','If we plan ahead, we can avoid unnecessary delays.','He asked a question, and I gave him a clear example.','We reviewed our mistakes before moving on to the next topic.']),
]

# Four authored scenario cues per lesson for production + transfer tasks (indices 6–9).
# They are situation prompts rather than translations or disguised full answers.
SCENARIOS={
'yes-no':['Kahvenin hâlâ sıcak olup olmadığını sor.','Arkadaşının daha erken gelip gelemeyeceğini sor.','Bir ödevin tamamlanıp tamamlanmadığını sor.','Yarın orada olup olmayacağını öğren.'],
'wh-questions':['Bir biletin fiyatını öğren.','Karşındakinin kimi beklediğini sor.','İşten sonra ne yaptığını sor.','Bir şehirde ne kadar süredir yaşadığını öğren.'],
'tense-questions':['Dün telefonda konuştuğunda onun ne yaptığını öğren.','Film başlamadan önce yemek yiyip yemediğini sor.','Gelecek hafta başvuru yapıp yapmayacağını sor.','Uzun süredir bekleyip beklemediğini sor.'],
'modal-questions':['Birinden şarj cihazını ödünç istemek için nazik bir soru sor.','Bugün formu vermek zorunda olup olmadığını öğren.','Bir işin gecikme ihtimalini sorgula.','Arkadaşının daha sonra katılmaya müsait olup olmadığını nazikçe sor.'],
'subject-questions':['Elektrik kesintisine neyin yol açtığını sor.','E-postayı kimin gönderdiğini sor.','Hangi otobüsün merkeze gittiğini öğren.','Güncellemeden sonra neyin değiştiğini sor.'],
'object-questions':['Akşam yemeğine kimleri davet ettiğini sor.','Yarın ne getireceğini sor.','Hangi filmi tavsiye ettiğini sor.','Bu hafta ne öğrendiğini sor.'],
'negative-questions':['Bir mesajın ulaşıp ulaşmadığını beklentiyle sor.','Telefon etmenin daha kolay olmayacağını öner.','Onların bugün gelmesi gerekmiyor muydu diye sor.','Neden henüz cevap gelmediğini sor.'],
'indirect-questions':['Birinden park ettiğiniz yeri hatırlayıp hatırlamadığını nazikçe sor.','Nazik bir yardım talebi oluştur.','Trenin ne zaman kalktığını dolaylı sor.','Kiminle iletişim kurman gerektiğini nazikçe öğren.'],
'question-tags':['Birinin bir şeyi unutmadığına dair teyit al.','Buranın onun koltuğu olduğunu doğrula.','Beraber mola verme teklifini tag question ile yap.','Geç kalmış olduğun bilgisini teyit et.'],
'preposition-questions':['İlgi duyduğu konuyu uygun edatla sor.','Taşındığı şehri sor.','Bir sonucun neye bağlı olduğunu sor.','Harcanan paranın nereye gittiğini sor.'],
'hypothetical-questions':['Yurt dışında iyi bir iş bulsa taşınıp taşınmayacağını sor.','Bir acemiye konuyu nasıl anlatacağını varsayımsal sor.','Geçmişte önceden bilse ne yapmış olacağını sor.','Teklif daha iyi olsa kalıp kalmayacağını sor.'],
'follow-up-questions':['Birinin yaşadığı olayın en zor kısmını öğren.','Bir kararın nedenini takip sorusuyla açıklaştır.','Bir başkasının verdiği tepkiyi sor.','Aynı deneyimi yaşasa bir dahaki sefere neyi farklı yapacağını sor.'],
'prepositions-time':['Bir teslim tarihinin ayın beşinde olduğunu söyle.','Sabah yola çıkmanız gerektiğini belirt.','Dükkânın gece yarısında kapandığını söyle.','Cuma öğleden sonra görüşmeyi öner.'],
'prepositions-place':['Aynı sokakta bir fırın olduğunu söyle.','Belgelerin çantanın içinde olduğunu söyle.','Birinin şu anda otobüste olduğunu söyle.','Dizüstü bilgisayarını evde bıraktığını açıkla.'],
'movement-prepositions':['Kütüphaneyi geçip sola dönmesini söyle.','Nehir boyunca yürüyen çocukları betimle.','Merdivenlerden yukarı çıktığınızı anlat.','Birinin tepeden dikkatle indiğini anlat.'],
'verb-preposition':['Bir gruba ait olduklarını anlat.','Yurt dışına taşınmayı düşündüğünü anlat.','Hesabı ödemekte ısrar eden birini anlat.','Bir problemi birine açıklamak için doğru edatı kullan.'],
'adjective-preposition':['Bir gezi için heyecanlı olduklarını söyle.','Bir sonuç karşısında şaşırmayı anlat.','Yardım için minnet duyduğunu söyle.','Bir bölgenin restoranlarıyla ünlü olduğunu anlat.'],
'noun-preposition':['Bir sorunun cevabını açıkla.','Bir projeye katkıda bulunmayı anlat.','Konut talebindeki değişimi ifade et.','Fotoğrafçılığa ilgini belirt.'],
'because-during':['Ders sırasında not almayı anlat.','Müzik dinlerken ders çalışmayı anlat.','Kar nedeniyle kapanan yolları açıkla.','Üniversitenin ilk haftasında biriyle tanışmayı anlat.'],
'for-since-until':['Dükkânın saat ona kadar açık olduğunu söyle.','Gece yarısına kadar kayıt olma zorunluluğunu açıkla.','Yıllardır tanışan iki kişiyi betimle.','Kahvaltıdan beri ders çalışan birini anlat.'],
'to-for-with':['Telefonla harita kontrol etmeyi anlat.','Yeni öğrenciler için yazılan mesajı belirt.','Bir belgeyi seninle paylaştığını söyle.','Makbuzun kasiyere verildiğini anlat.'],
'fixed-preposition-chunks':['Yeni kuralın şu anda yürürlükte olduğunu söyle.','Mümkün olduğunca çabuk geri dönüş vaat et.','Bir öneriyi desteklediğinizi söyle.','Otelin yürüyüş mesafesinde olduğunu anlat.'],
'cause-connectors':['Madem herkes burada, derse başlamayı öner.','Elektrik kesintisi nedeniyle toplantının erken bittiğini açıkla.','Trafik sakin olduğu için erken vardığınızı anlat.','Beklenmedik tamirat nedeniyle plan değişikliğini açıkla.'],
'result-connectors':['Birikimleri sayesinde seyahat edebilmelerini açıkla.','Dosyalar kaybolduğu için işlerin gecikmesini anlat.','Hava düzeldiği için dışarı çıkmayı anlat.','Düzenli çalışmanın gelişmeye etkisini açıkla.'],
'contrast-connectors':['İş zor olmasına rağmen bitirmeyi anlat.','Vakti az olmasına rağmen yardım etmeyi anlat.','Otelden memnun olup hizmetten memnun olmamayı anlat.','Farklı düşünseniz de saygıyı korumayı ifade et.'],
'condition-connectors':['İş tamamlanırsa erken çıkma iznini açıkla.','Hava düzelirse doğa yürüyüşüne gitmeyi öner.','Ödeme ulaşırsa ertesi gün kargoya vermeyi koşula bağla.','Bir şey değişmezse toplantının saati değişmeyecek de.'],
'addition-connectors':['Bir planın hem zaman hem atık tasarrufu sağladığını anlat.','Okuma ve yürüyüşten hoşlanan birini anlat.','Raporun net ve örnekli olduğunu ek bilgiyle belirt.','Yazılımın hem kolay hem çevrimdışı çalıştığını anlat.'],
'comparison-connectors':['İki seçeneğin farklı ihtiyaçları karşıladığını söyle.','Birinin kalabalık, senin sakin yerleri sevdiğini karşılaştır.','Geçen yılla kıyasla satış artışını anlat.','Tren ve otobüsün hız/fiyat farkını anlat.'],
'examples-connectors':['Hobiler arasında çizim ve fotoğrafçılığı örnekle.','Ücretsiz araçlara sözlük örneği ver.','Rol yapma üzerinden pratik öğrenmeyi örnekle.','Müşteri isteği gibi somut örneklerle açıklama iste.'],
'sequence-connectors':['Biri gelince yemeğe başlamayı anlat.','Yemek pişerken masa hazırlığını anlat.','Son adımda ilerlemenin kaydedilmesini söyle.','Bu arada önceki dersi tekrar etmeyi öner.'],
'articles-quantifiers':['Tekil bir üniversitede çalıştığını belirt.','Yanında hiç nakit olmadığını söyle.','Birinden sayılamayan tavsiye istediğini anlat.','Gönderilen belirli bilginin yararlı olduğunu söyle.'],
'relative-pronouns':['Sana yardımcı olup sonra işten ayrılan meslektaşı tanıt.','Birlikte izlediğiniz filmi niteleme yan cümlesiyle anlat.','Sana yararlı bir harita verilmesini ek bilgiyle anlat.','Büyüdüğün yeri niteleme yan cümlesiyle tanıt.'],
'modals-conditionals':['Geçmişte ders çalışsaydı kazanacak olacağı varsayımını kur.','Henüz ayrılmak zorunda olmadığınızı söyle.','Birine bunu daha önce söylemesi gerektiğini belirt.','Yağmur durursa yürüyüşü öner.'],
'natural-sentence-flow':['Bir fikir iyi görünse de daha fazla kanıt gerektiğini anlat.','Önceden planlamanın gecikmeyi nasıl önleyeceğini ifade et.','Birinin soru sormasına açık bir örnekle yanıt verdiğini anlat.','Yeni konuya geçmeden önce hataları tekrar ettiğinizi söyle.']
}
assert len(SCENARIOS)==len(LESSONS)
for slug,_,_,_,_,models in LESSONS:
 assert len(SCENARIOS[slug])==4,slug

# Avoid claiming artificial grammatical certainty: the model sentences are curated
# for an example-based exercise; unlimited English alternatives are self-assessed.
MODES=['order','order','guided','guided','guided','guided','production','production','followup','followup']
AREA=lambda i:'question' if i<12 else 'preposition' if i<22 else 'connector' if i<30 else 'sentence'
LESSON_HINTS={
 'question':'Duruma uygun bir soru yaz. Doğal bir alternatif cevabın varsa örnekle karşılaştır.',
 'preposition':'Edatı tek başına değil, doğal bir tam cümle içinde kullan.',
 'connector':'İki düşünce arasındaki anlam ilişkisini gösteren doğal bir cümle yaz.',
 'sentence':'Belirtilen yapıyı doğal bir Amerikan İngilizcesi cümlesinde kullan.'
}
OUT=[]
for n,(slug,title,rule,common,level,models) in enumerate(LESSONS):
 assert len(models)==10,(slug,len(models))
 area=AREA(n); exercises=[]
 for i,answer in enumerate(models):
  mode=MODES[i]; task=('Kelimeleri doğru sıraya yerleştir.' if mode=='order' else
      'Cümledeki boşluğu doğru İngilizce kelime veya ifadeyle tamamla.' if mode=='guided' else
      'Bu konuyu kendi hayatından bir örnekle ifade et.' if mode=='production' else
      'Aynı yapıyı farklı bir günlük durumda kendi sözlerinle kullan.')
  # A transparent, high-level cue: exact answers are not smuggled into a free response.
  task+=' Odak: '+title+'.'
  if i>=6:task=SCENARIOS[slug][i-6]+' İngilizce tek cümle yaz. Farklı ama doğru ifadeler kabul edilebilir.'
  item={'id':f'sk-{slug}-{i+1:02d}','mode':mode,'task':task,'modelAnswer':answer,
        'focus':title,'explanation':rule,'commonError':common,'independentEditorApproved':False}
  if mode=='order':
   import re
   tokens=re.findall(r"[\w]+(?:[’'-][\w]+)*|[^\w\s]",answer,flags=re.UNICODE)
   # Deterministic shuffle: nontrivial even when 5+ words; no spelling distortions.
   item['tokens']=tokens[2::2]+tokens[1::2]+tokens[:1] if len(tokens)>3 else list(reversed(tokens))
   # Avoid ambiguous punctuation token challenges; punctuation ignored in matching.
  exercises.append(item)
 OUT.append({'id':'sl-'+slug,'title':title,'area':area,'level':level,'rule':rule,'commonError':common,
             'description':LESSON_HINTS[area],'editorApproval':'pending-independent-review','exercises':exercises})
assert len(OUT)==34
assert sum(len(x['exercises']) for x in OUT)==340
all_answers=[ex['modelAnswer'] for l in OUT for ex in l['exercises']]
assert len(set(x.casefold() for x in all_answers))==340,'duplicate example sentence'
path=Path(__file__).resolve().parents[1]/'data'/'sentence-skills.json'
path.write_text(json.dumps({'meta':{
 'title':'Sentence Skills: Question Builder, Preposition Lab, Connector Lab, Sentence Builder',
 'version':1,'language':'en-US','totalLessons':34,'totalExercises':340,
 'lessonDistribution':{'question':12,'preposition':10,'connector':8,'sentence':4},
 'independentEditorApproved':False,'authoringStage':'original-authored-private-pilot-pending-independent-review',
 'audio':None,'cefrDisclaimer':'Practice difficulty labels are author estimates, not certified CEFR assessments.',
 'evaluationDisclaimer':'Model answers are not exhaustive; non-matches must not be marked grammatically wrong automatically.'
 },'lessons':OUT},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'{len(OUT)} lessons and {len(all_answers)} unique original examples -> {path}')
