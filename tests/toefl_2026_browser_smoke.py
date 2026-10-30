"""Targeted virtual-asset Chromium QA, not true origin/offline or physical iPhone QA."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from e2e_playwright import install_virtual_files
ROOT=Path(__file__).resolve().parents[1]
report={'method':'mocked_asset_routing_in_Chromium_not_real_offline','releaseEvidence':False,'desktop':'not_run','mobile_viewport':'not_run','physicalIphone':'not_tested','audioPlayback':'not_tested'}
try:
 with sync_playwright() as p:
  b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
  try:
   for mobile in (False,True):
    ctx=b.new_context(viewport={'width':390 if mobile else 1440,'height':844 if mobile else 900},is_mobile=mobile,has_touch=mobile)
    page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    install_virtual_files(page)
    page.get_by_text('Real progress.').wait_for(timeout=10000)
    page.evaluate("document.querySelector('.nav-button[data-view=writing]').click()")
    page.locator('[data-act="writingMode"][data-mode="toefl"]').click()
    assert page.locator('#toeflWriting').count()==1
    page.locator('#toeflWriting').fill('The library will close early because of renovations.')
    page.locator('[data-act="checkToeflSentence"]').click()
    assert 'eşleşiyor' in page.locator('main').inner_text()
    # Leave this page and return: stored progress ID is stable.
    page.evaluate("document.querySelector('.nav-button[data-view=reading]').click()")
    assert page.locator('[data-act="openToeflReading"]').count()==18
    page.locator('[data-act="openToeflReading"]').first.click()
    assert page.locator('[data-act="answerQuestion"]').count()==8
    for idx in [0,1]:
     page.locator(f'[data-key="tr-tr26-words-01-{idx}"]').first.click()
    page.locator('[data-act="completeToeflReading"]').click()
    assert page.evaluate("JSON.parse(localStorage.getItem('ael-progress')).lessons['tr26-words-01']")
    page.evaluate("document.querySelector('.nav-button[data-view=authentic]').click()")
    page.locator('[data-field="voaSearch"]').fill('Movie Night')
    page.get_by_text('Movie Night').first.wait_for(timeout=10000)
    page.locator('[data-act="authenticOpen"][data-id="voa-linked-2-19"]').click()
    assert 'Bir sorun oluştu' not in page.locator('main').inner_text()
    page.locator('[data-act="authenticToggleTranscript"]').click(timeout=5000)
    assert 'sahne yönergesi' in page.locator('main').inner_text()
    assert not errors,errors
    report['mobile_viewport' if mobile else 'desktop']='passed'
    ctx.close()
  finally: b.close()
except Exception as e:
 report['error']=str(e)[:800]
finally:
 (ROOT/'qa/toefl-2026-browser-smoke.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(report,ensure_ascii=False,indent=2))

if 'error' in report or report['desktop']!='passed' or report['mobile_viewport']!='passed':raise SystemExit(1)
