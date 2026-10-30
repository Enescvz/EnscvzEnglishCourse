"""Chromium virtual-origin smoke check. NOT remote-audio or WebKit release evidence."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from e2e_playwright import install_virtual_files
ROOT=Path(__file__).resolve().parents[1]

def run():
 results={}
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
  for name,w,h in [('desktop',1280,850),('mobile',390,844)]:
   page=browser.new_page(viewport={'width':w,'height':h},service_workers='block')
   errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   install_virtual_files(page)
   page.get_by_text('Real progress.').wait_for(timeout=12000)
   page.evaluate("document.querySelector('.nav-button[data-view=authentic]').click()")
   page.get_by_text('50 sorulu ders',exact=False).wait_for(timeout=12000)
   assert '50 kaynak' in page.locator('main').inner_text()
   page.locator('[data-act=voaFilter][data-value=source]').click()
   assert '0 kaynak' in page.locator('main').inner_text()
   page.locator('[data-act=voaFilter][data-value=linked]').click()
   assert '32 kaynak' in page.locator('main').inner_text()
   # An external source quiz must not be saved as a completed listening session
   # until the learner explicitly self-reports listening. The browser cannot verify audio.
   page.locator('[data-act=linkedQuizOpen]').first.click()
   assert page.locator('#voaListenedConfirm').count()==1
   for i in range(4):
    page.locator(f'[data-linked-q="{i}"] button.choice').first.click()
   page.locator('[data-act=linkedQuizFinish]').click()
   assert page.get_by_text('Dinlemeyi tamamladıysan',exact=False).count()>=1
   page.locator('#voaListenedConfirm').check()
   page.locator('[data-act=linkedQuizFinish]').click()
   assert page.get_by_text('Kaynak bağlantılı dinleme soruları:',exact=False).count()>=1
   # Full-transcript lessons must use the same honest self-report gate.
   page.evaluate("document.querySelector('.nav-button[data-view=authentic]').click()")
   page.locator('[data-act=voaFilter][data-value=imported]').click()
   assert '18 kaynak' in page.locator('main').inner_text()
   page.locator('[data-act=authenticOpen][data-id=voa-linked-2-08]').click()
   # Lesson 8 has no verified direct audio URL; never render a broken player.
   assert page.locator('#media').count()==0
   assert 'doğrulanmış doğrudan MP3' in page.locator('main').inner_text()
   # New publisher-transcript lessons keep original quiz IDs, show answer evidence,
   # and expose source-linked MP3 URLs without claiming verified audio playback.
   page.evaluate("document.querySelector('.nav-button[data-view=authentic]').click()")
   page.locator('[data-act=voaFilter][data-value=imported]').click()
   for lesson_id, phrase in [('voa-linked-2-11','Food, a blanket, and warm clothing'),('voa-linked-2-12','About thirty thousand')]:
    page.locator(f'[data-act=authenticOpen][data-id={lesson_id}]').click()
    assert page.locator('#media').get_attribute('src').startswith('https://voa-audio.voanews.eu/')
    assert page.locator('#authenticTranscript').is_hidden()
    page.locator('[data-act=authenticToggleTranscript]').click()
    assert page.locator('#authenticTranscript').is_visible()
    assert page.locator('[data-auth-q]').count()==4
    assert phrase in page.locator('main').inner_text()
    assert page.locator('#authenticListenedConfirm').count()==1
    page.evaluate("document.querySelector('.nav-button[data-view=authentic]').click()")
    page.locator('[data-act=voaFilter][data-value=imported]').click()
   page.evaluate("document.querySelector('.nav-button[data-view=authentic]').click()")
   page.locator('[data-act=voaFilter][data-value=imported]').click()
   page.locator('[data-act=authenticOpen][data-id=voa-linked-2-07]').click()
   assert page.locator('#authenticListenedConfirm').count()==1
   assert page.locator('#authenticTranscript').is_hidden()
   for i in range(page.locator('[data-auth-q]').count()):
    page.locator(f'[data-auth-q="{i}"] button.choice').first.click()
   assert 'Kaynak:' in page.locator('[data-auth-q="0"]').inner_text()
   page.locator('[data-act=authenticFinish]').click()
   assert page.get_by_text('yalnızca soruları cevaplamak dinleme tamamlandı sayılmaz',exact=False).count()>=1
   page.locator('#authenticListenedConfirm').check()
   page.locator('[data-act=authenticFinish]').click()
   assert page.get_by_text('Dinlediğini beyan ettiğin kaydın soruları:',exact=False).count()>=1
   # New Lessons 15-18 are integrated; transcript and online player are not device proof.
   page.evaluate("document.querySelector('.nav-button[data-view=authentic]').click()")
   page.locator('[data-act=voaFilter][data-value=imported]').click()
   for n in (15,16,17,18):
    page.locator(f'[data-act=authenticOpen][data-id=voa-linked-2-{n:02d}]').click()
    assert page.locator('#media').get_attribute('src').startswith('https://voa-audio.voanews.eu/')
    assert page.locator('#authenticTranscript').is_hidden()
    page.locator('[data-act=authenticToggleTranscript]').click()
    assert page.locator('#authenticTranscript .turn').count()>=20
    assert page.locator('[data-auth-q]').count()==4
    assert page.locator('#authenticListenedConfirm').count()==1
    page.evaluate("document.querySelector('.nav-button[data-view=authentic]').click()")
    page.locator('[data-act=voaFilter][data-value=imported]').click()
   page.evaluate("document.querySelector('.nav-button[data-view=reading]').click()")
   assert page.locator('[data-act=openReading]').count()==30
   page.locator('[data-act=openReading][data-id=the-last-minute-change]').click()
   assert page.locator('[data-act=answerQuestion]').count()==20
   assert 'A Last-Minute Change of Plans' in page.locator('main').inner_text()
   page.evaluate("document.querySelector('.nav-button[data-view=grammar]').click()")
   assert page.locator('.test-question').count()==20
   assert page.get_by_text('Grammar Workshop').count()>=1
   assert not errors,errors
   results[name]={'50Voa':True,'32Linked':True,'18Imported':True,'selfReportGate':True,'30Readings':True,'20Grammar':True,'browser':'virtual origin Chromium','realAudioVerified':False}
   page.close()
  browser.close()
 print(results)
if __name__=='__main__':run()
