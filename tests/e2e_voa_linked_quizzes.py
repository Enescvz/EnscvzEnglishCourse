"""Virtual Chromium UI smoke check; not verified remote audio or iPhone WebKit."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
from e2e_playwright import install_virtual_files
ROOT=Path(__file__).resolve().parents[1]

def run():
    results={}
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
        for label,width,height in [('desktop',1280,850),('mobile',390,844)]:
            page=browser.new_page(viewport={'width':width,'height':height},service_workers='block')
            issues=[]
            page.on('pageerror',lambda e:issues.append(str(e)))
            install_virtual_files(page)
            page.get_by_text('Real progress.').wait_for(timeout=12000)
            page.evaluate("document.querySelector('[data-view=\"authentic\"]').click()")
            page.get_by_role('heading',name='Real Voices · VOA').wait_for(timeout=12000)
            page.locator('[data-act="voaFilter"][data-value="linked"]').click()
            assert page.locator('[data-act="linkedQuizOpen"]').count()>=1
            page.locator('[data-act="linkedQuizOpen"][data-id="voa-linked-2-19"]').click()
            assert page.locator('[data-linked-q]').count()==4
            link=page.locator('a.btn.primary[href^="https://learningenglish.voanews.com/a/"]')
            assert link.count()==1
            for idx in range(4):
                page.locator(f'[data-linked-q="{idx}"] button.choice').first.click()
                assert page.locator(f'[data-linked-q="{idx}"] .auth-feedback').get_by_text('Kaynak kontrolü:').count()==1
                if idx==3:
                    assert 'sesli replik değil' in page.locator('[data-linked-q="3"]').inner_text()
            # Completion must be blocked without an explicit listening self-report.
            page.locator('[data-act="linkedQuizFinish"]').click()
            before=page.evaluate("localStorage.getItem('ael-progress')")
            assert before is None or not json.loads(before).get('authenticLessons',{}), 'Unconfirmed listening was recorded'
            page.locator('#voaListenedConfirm').check()
            page.locator('[data-act="linkedQuizFinish"]').click()
            completed=page.evaluate("Object.values(JSON.parse(localStorage.getItem('ael-progress')).authenticLessons).find(x=>x.assessmentType==='source-linked-comprehension')")
            assert completed['total']==4 and completed['audioPlaybackSelfReported'] is True and completed['audioPlaybackVerified'] is False
            # Newly reviewed Level 1 source evidence appears after the quiz answer,
            # with explicit context for the unreliable narration in Lesson 42.
            page.locator('[data-act="linkedQuizBack"]').click()
            page.locator('[data-act="voaFilter"][data-value="level1"]').click()
            page.locator('[data-act="linkedQuizOpen"][data-id="voa-linked-1-42"]').click()
            page.locator('[data-linked-q="3"] button.choice').first.click()
            context_note=page.locator('[data-linked-q="3"] .auth-feedback').inner_text()
            assert 'Kaynak kontrolü:' in context_note and 'Bağlam notu:' in context_note
            assert 'otomat' in context_note
            assert not issues,issues
            results[label]={'UI':'passed','answerPersistence':True,'externalSourceLink':True,'remoteAudioVerified':False}
            page.close()
        browser.close()
    out=ROOT/'qa/voa-linked-browser-smoke.json'
    out.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(results,ensure_ascii=False))
if __name__=='__main__':run()
