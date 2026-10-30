"""Focused virtual Chromium check. Does not verify physical Safari or ETS scoring."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from e2e_playwright import install_virtual_files
ROOT=Path(__file__).resolve().parents[1]
report={'mode':'virtual-routed Chromium','desktop':'not_run','mobile':'not_run','officialETSScore':False,'physicalSafari':'not_tested','real_origin_resume':'not_tested','releaseApproved':False}
try:
 with sync_playwright() as p:
  b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
  try:
   for mobile in (False,True):
    ctx=b.new_context(viewport={'width':390 if mobile else 1440,'height':844 if mobile else 900},is_mobile=mobile,has_touch=mobile)
    page=ctx.new_page();errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    install_virtual_files(page)
    page.get_by_text('Real progress.').wait_for(timeout=15000)
    page.evaluate("document.querySelector('.nav-button[data-view=toefl]').click()")
    page.locator('[data-act="startToeflCloze"]').click(timeout=8000)
    assert page.locator('#toeflClozeAnswer').count()==1
    assert 'Eksik harfi' in page.locator('main').inner_text()
    page.locator('#toeflClozeAnswer').fill('volunteer')
    page.locator('[data-act="submitToeflCloze"]').click()
    assert page.locator('[data-act="nextToeflCloze"]').count()==1
    progress=page.evaluate("JSON.parse(localStorage.getItem('ael-progress'))")
    assert progress['toeflAttempts'][-1]['kind']=='original_typed_word_completion'
    assert progress['toeflAttempts'][-1]['correct'] is True
    assert progress['toeflAttempts'][-1]['officialScore'] is None
    assert progress['listenHistory']==[]
    page.locator('[data-act="closeToeflCloze"]').click()
    page.locator('[data-act="startWritingExam"]').click()
    state=page.evaluate("JSON.parse(localStorage.getItem('ael-progress')).toeflActiveWriting")
    assert state['version']==2
    tasks={t['id']:t for t in json.loads((ROOT/'data/toefl-writing-practice.json').read_text())}
    kinds=[tasks[id]['kind'] for id in state['ids']]
    assert kinds.count('build_sentence')==10 and kinds.count('write_email')==1 and kinds.count('academic_discussion')==1
    page.locator('#toeflTimedWriting').fill('Test draft, preserve me.')
    # The virtual harness does not model a persistent browser origin; inspect serialized draft instead.
    saved=page.evaluate("JSON.parse(localStorage.getItem('ael-progress'))")
    assert saved['toeflActiveWriting']['version']==2
    assert saved['toeflActiveWriting']['answers'][state['ids'][0]]=='Test draft, preserve me.'
    assert not errors,errors
    report['mobile' if mobile else 'desktop']='passed'
    ctx.close()
  finally:b.close()
except Exception as exc:report['error']=str(exc)[:1500]
(ROOT/'qa/toefl-2026-alignment-browser.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
if 'error' in report:raise SystemExit(1)
