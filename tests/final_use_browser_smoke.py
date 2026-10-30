"""Private virtual-browser smoke, not physical iPhone / HTTPS / offline proof."""
import json,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tests'))
from e2e_playwright import install_virtual_files
results={}
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 try:
  for mobile in (False,True):
   ctx=browser.new_context(viewport={'width':390 if mobile else 1440,'height':844 if mobile else 900},is_mobile=mobile,has_touch=mobile)
   page=ctx.new_page(); errors=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.set_default_timeout(6000)
   install_virtual_files(page)
   page.get_by_text('Real progress.').wait_for(timeout=12000)
   page.evaluate("document.querySelector('.nav-button[data-view=\"toefl\"]').click()")
   assert 'TOEFL' in page.locator('main').inner_text()
   page.locator('[data-act="startToeflDiagnostic"]').click()
   v=page.evaluate("JSON.parse(localStorage.getItem('ael-progress')).toeflActiveReading.version")
   assert v==2,v
   assert page.locator('[data-act="toeflMiniAnswer"]').count()==20
   page.locator('[data-act="toeflMiniAnswer"]').first.click()
   a=page.evaluate("JSON.parse(localStorage.getItem('ael-progress')).toeflActiveReading.answers")
   assert len(a)==1,a
   page.locator('[data-act="exitToeflMini"]').click()
   page.locator('[data-act="resumeToeflReading"]').click()
   assert page.locator('[data-act="toeflMiniAnswer"]').count()==20
   page.locator('[data-act="finishToeflMini"]').click()
   assert 'özgün Reading alıştırması' in page.locator('main').inner_text()
   page.locator('[data-act="startWritingExam"]').click()
   assert page.evaluate("JSON.parse(localStorage.getItem('ael-progress')).toeflActiveWriting.version")==2
   page.locator('#toeflTimedWriting').fill('The campus library is open today.')
   page.locator('[data-act="pauseWritingExam"]').click()
   page.locator('[data-act="resumeWritingExam"]').click()
   assert page.locator('#toeflTimedWriting').input_value()=='The campus library is open today.'
   page.locator('[data-act="finishWritingExam"]').click()
   assert '/10 referans metinle' in page.locator('main').inner_text()
   assert not errors, errors
   results['mobile_virtual' if mobile else 'desktop_virtual']='passed'
   ctx.close()
 finally:browser.close()
print(json.dumps({'type':'static_file_routed_chromium_mocked_storage','not_proof_of_physical_safari':True,'not_real_http_offline':True,'results':results},ensure_ascii=False))
