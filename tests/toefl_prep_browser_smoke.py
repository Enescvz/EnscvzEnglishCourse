"""Virtual Chromium view checks, intentionally NOT real Safari/offline/audio/release evidence."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from e2e_playwright import install_virtual_files
ROOT=Path(__file__).resolve().parents[1]
report={'method':'virtual asset routed Chromium only','releaseEvidence':False,
'desktop':'not_run','mobile_viewport':'not_run','physical_iPhone_Safari':'not_tested','audio_playback':'not_tested','offline_origin':'not_tested'}
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
  try:
   for mobile in (False,True):
    ctx=browser.new_context(viewport={'width':390 if mobile else 1440,'height':844 if mobile else 900},is_mobile=mobile,has_touch=mobile)
    page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    install_virtual_files(page)
    page.get_by_text('Real progress.').wait_for(timeout=15000)
    page.evaluate("document.querySelector('.nav-button[data-view=toefl]').click()")
    page.locator('main h1').get_by_text('TOEFL + Daily · 2026').wait_for(timeout=12000)
    assert page.locator('main').get_by_text('Reading alıştırması').count()>0
    assert 'doğrulanmış ses' in page.locator('main').inner_text()
    page.locator('[data-act="startToeflMini"]').click()
    assert page.locator('[data-act="toeflMiniAnswer"]').count()==36
    assert '12 dakika' in page.locator('main').inner_text()
    page.locator('[data-act="toeflMiniAnswer"]').first.click()
    assert page.locator('#toeflMiniClock').count()==1
    page.locator('[data-act="finishToeflMini"]').click()
    assert '1–6 ya da 0–120' in page.locator('main').inner_text()
    saved=page.evaluate("JSON.parse(localStorage.getItem('ael-progress')).toeflAttempts")
    assert len(saved)==1 and saved[0]['officialScore'] is None and saved[0]['total']==9
    page.locator('[data-act="exitToeflMini"]').click()
    page.locator('[data-act="startToeflDiagnostic"]').click()
    assert page.locator('[data-act="toeflMiniAnswer"]').count()==20
    assert '50 soru · 30 dakika' in page.locator('main').inner_text()
    page.locator('[data-act="toeflReadingNext"]').click()
    assert 'Sayfa 2/10' in page.locator('main').inner_text()
    page.locator('[data-act="toeflMiniAnswer"]').first.click()
    page.locator('[data-act="exitToeflMini"]').click()
    assert page.locator('[data-act="resumeToeflReading"]').count()==1
    page.locator('[data-act="resumeToeflReading"]').click()
    assert page.locator('[data-act="toeflMiniAnswer"]').count()==20
    page.locator('[data-act="finishToeflMini"]').click()
    assert '1–6 ya da 0–120' in page.locator('main').inner_text()
    page.locator('[data-act="exitToeflMini"]').click()
    assert page.evaluate("JSON.parse(localStorage.getItem('ael-progress')).toeflAttempts.length")==2
    page.locator('[data-act="toeflScriptOpen"]').first.click()
    assert 'Metin provası (ses kaydı değildir)' in page.locator('main').inner_text()
    assert not page.evaluate("JSON.parse(localStorage.getItem('ael-progress')).listenHistory").__len__()
    page.evaluate("document.querySelector('.nav-button[data-view=writing]').click()")
    page.locator('[data-act="writingMode"][data-mode="toefl"]').click()
    page.locator('[data-act="nextToeflWriting"]').click()
    page.locator('[data-act="nextToeflWriting"]').click()
    page.locator('[data-act="nextToeflWriting"]').click()
    assert page.locator('[data-act="toeflWritingHints"]').count()==1
    page.locator('#toeflWriting').fill('Hello Professor Martin, I missed the meeting yesterday. Could we meet on Thursday at three? Thank you for your time. Kind regards, Student')
    page.locator('[data-act="toeflWritingHints"]').click()
    assert 'resmî TOEFL' in page.locator('main').inner_text()
    assert not errors,errors
    report['mobile_viewport' if mobile else 'desktop']='passed'
    ctx.close()
  finally:browser.close()
except Exception as exc:
 report['error']=str(exc)[:1000]
finally:
 (ROOT/'qa/toefl-prep-browser-smoke.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(report,ensure_ascii=False,indent=2))
if 'error' in report or report['desktop']!='passed' or report['mobile_viewport']!='passed':raise SystemExit(1)
