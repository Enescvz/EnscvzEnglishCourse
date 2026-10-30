"""Virtual-routed Chromium only; not physical iPhone, official scoring, or true network-offline QA."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from e2e_playwright import install_virtual_files
ROOT=Path(__file__).resolve().parents[1]
report={"method":"Virtual Chromium routed assets; not real origin or physical Safari", "desktop":"not_run","mobile_viewport":"not_run","real_iphone_safari":"not_tested","official_ETS_scoring":"not_available","human_listening_audio":"not_verified", "releaseApproved":False}
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
  try:
   for mobile in (False,True):
    ctx=browser.new_context(viewport={'width':390 if mobile else 1440,'height':844 if mobile else 900},is_mobile=mobile,has_touch=mobile)
    page=ctx.new_page(); errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    install_virtual_files(page)
    page.get_by_text('Real progress.').wait_for(timeout=15000)
    page.evaluate("document.querySelector('.nav-button[data-view=toefl]').click()")
    page.locator('[data-act="startWritingExam"]').click(timeout=8000)
    assert page.locator('#toeflTimedWriting').count()==1
    page.locator('#toeflTimedWriting').fill('The instructor extended the deadline because of a campus closure.')
    current=page.evaluate("JSON.parse(localStorage.getItem('ael-progress')).toeflActiveWriting")
    assert current and len(current['answers'])==1,current
    page.locator('[data-act="writingExamNext"]').click()
    page.locator('#toeflTimedWriting').fill('The survey suggests that students prefer shorter workshops.')
    page.evaluate("document.querySelector('.nav-button[data-view=reading]').click()")
    page.evaluate("document.querySelector('.nav-button[data-view=toefl]').click()")
    assert page.locator('[data-act="resumeWritingExam"]').count()==0 or page.locator('#toeflTimedWriting').count()==1
    page.locator('[data-act="finishWritingExam"]').click()
    assert 'puandı' not in page.locator('main').inner_text()
    a=page.evaluate("JSON.parse(localStorage.getItem('ael-progress'))")
    assert not a.get('toeflActiveWriting')
    assert len(a['toeflWritingAttempts'])==1
    assert a['toeflWritingAttempts'][0]['officialScore'] is None
    assert a['toeflWritingAttempts'][0]['grammarGraded'] is False
    assert not a['listenHistory']
    page.locator('[data-act="exitWritingExam"]').click()
    page.locator('[data-act="startToeflDiagnostic"]').click()
    assert '50 soru · 30 dakika' in page.locator('main').inner_text()
    assert page.locator('[data-act="toeflMiniAnswer"]').count()==20
    page.locator('[data-act="finishToeflMini"]').click()
    a=page.evaluate("JSON.parse(localStorage.getItem('ael-progress'))")
    assert a['toeflAttempts'][-1]['total']==50
    assert a['toeflAttempts'][-1]['officialScore'] is None
    assert not errors,errors
    report['mobile_viewport' if mobile else 'desktop']='passed'
    ctx.close()
  finally:browser.close()
except Exception as exc:report['error']=str(exc)[:1200]
finally:
 (ROOT/'qa/toefl-extended-browser-smoke.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(report,ensure_ascii=False,indent=2))
if 'error' in report:raise SystemExit(1)
