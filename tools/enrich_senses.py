from pathlib import Path
import json
p=Path(__file__).resolve().parents[1]/'data/phrasals.json';d=json.loads(p.read_text())
meaning={
('take off','uçak havalanmak'):'For an airplane or other aircraft to leave the ground and begin flying.',
('take off','kıyafeti çıkarmak'):'To remove clothing from your body.',
('break down','duygusal olarak çökmek'):'To lose emotional control and start crying or become unable to cope.',
('break down','parçalara ayırarak açıklamak'):'To explain a complicated total or process by dividing it into simpler parts.',
('work out','egzersiz yapmak'):'To exercise regularly to become fitter or stronger.',
('work out','iyi sonuçlanmak'):'To develop successfully or end in a good result.',
('bring up','çocuk yetiştirmek'):'To care for and raise a child until adulthood.',
('back up','verileri yedeklemek'):'To make a separate copy of digital information for protection.',
('cut off','birinin sözünü kesmek'):'To interrupt someone before they have finished speaking.',
('get over','engeli aşmak'):'To cross a physical obstacle by climbing or jumping.',
('pay off','borcu tamamen ödemek'):'To pay all the money owed on a loan or debt.',
('put off','birinden soğutmak'):'To make someone dislike or lose interest in something.',
('take on','yeni çalışan almak'):'To employ additional people for work.',
('turn down','sesi kısmak'):'To lower the volume or intensity of a device.',
('set aside','bir kenara koymak'):'To put something to one side for later use.',
('look into','yakından incelemek'):'To examine a matter carefully to discover relevant facts.',
('come across','izlenim vermek'):'To create a particular impression through behavior or speech.',
('give up','bir şeyi bırakmak'):'To stop a habit or activity deliberately.',
}
for v in d:
 for s in v.get('senses',[]):
  key=(v['word'],s['tr'])
  if key in meaning:s['definition']=meaning[key]
  else:s.setdefault('definition',v['definition'])
 if len(v.get('senses',[]))>1:v['senseCount']=len(v['senses'])
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('Total phrasal senses',sum(len(x['senses']) for x in d))
