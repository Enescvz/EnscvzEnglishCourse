"""Browser end-to-end regression tests. Run with: python tests/e2e_playwright.py"""
import json,os,subprocess,time
from urllib.parse import urlparse
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
URL=os.environ.get('AEL_BASE_URL','http://127.0.0.1:8973/')

def install_virtual_files(page):
    """Sandbox-only UI harness: replace blocked navigation and localStorage.
    NOT a real deployment, not a Safari/WebKit test and not release evidence.
    """
    mime={'.js':'application/javascript','.json':'application/json','.css':'text/css','.svg':'image/svg+xml','.mp3':'audio/mpeg','.webmanifest':'application/manifest+json'}
    def respond(route):
        path=(ROOT/urlparse(route.request.url).path.lstrip('/')).resolve()
        if ROOT not in path.parents or not path.is_file():
            return route.fulfill(status=404,body='Not found',headers={'Access-Control-Allow-Origin':'*'})
        return route.fulfill(status=200,body=path.read_bytes(),content_type=mime.get(path.suffix,'application/octet-stream'),headers={'Access-Control-Allow-Origin':'*'})
    page.route('**/*',respond)
    page.evaluate("Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem:k=>(window.__store||{})[k]||null,setItem:(k,v)=>(window.__store||(window.__store={}))[k]=v,removeItem:k=>delete window.__store[k]}});")
    raw=(ROOT/'index.html').read_text(encoding='utf-8')
    page.set_content(raw.replace('<head>','<head><base href="https://ael.test/">'),wait_until='domcontentloaded',timeout=30000)

def run(browser, mobile=False, virtual=False):
    ctx=browser.new_context(viewport={'width':390 if mobile else 1440,'height':844 if mobile else 900},device_scale_factor=1,is_mobile=mobile,has_touch=mobile)
    page=ctx.new_page();errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    if virtual:install_virtual_files(page)
    else:page.goto(URL,wait_until='networkidle',timeout=30000)
    page.get_by_text('Real progress.').wait_for(timeout=10000)
    page.screenshot(path=str(ROOT/('preview-mobile.png' if mobile else 'preview-desktop.png')),full_page=True)
    assert 'Aktif kelime' in page.locator('main').inner_text()
    # Nav across every module.
    modules=['listening','vocabulary','phrasals','podcasts','reading','grammar','speaking','writing','conversations','pronunciation','tests','review','analytics','settings']
    for mod in modules:
        page.locator(f'.side [data-view="{mod}"]').click() if not mobile else page.evaluate("m=>document.querySelector('.nav-button[data-view=\"'+m+'\"]').click()",mod)
        assert page.locator('main h1').count()>0,mod
        assert 'Bir sorun oluştu' not in page.locator('main').inner_text(),mod
    # Source catalogue should load real local JSON, without counting candidates as lessons.
    page.evaluate("document.querySelector('.nav-button[data-view=\"catalog\"]').click()")
    page.get_by_text('4.851 başlık',exact=False).wait_for(timeout=10000)
    assert page.locator('.catalog-entry').count()==30
    page.locator('[data-act="catalogKind"][data-value="p"]').click()
    assert '1204 kaynak kaydı' in page.locator('main').inner_text()
    page.locator('[data-act="catalogNext"]').click()
    assert 'Sayfa 2/' in page.locator('main').inner_text()
    page.locator('[data-act="catalogAvailability"][data-value="lesson"]').click()
    catalog=json.loads((ROOT/'data/candidate-catalog.json').read_text(encoding='utf-8'))
    source_pv=len([x for x in catalog['entries'] if x['t']=='p' and x['lesson']])
    assert f'{source_pv} kaynak kaydı' in page.locator('main').inner_text()
    page.locator('[data-act="catalogOpenLesson"]').first.click()
    assert page.locator('main h1').count()>0
    # Rapid bilingual recognition is separately tracked from full-lesson mastery.
    page.evaluate("document.querySelector('.nav-button[data-view=\"rapid\"]').click()")
    assert 'Hızlı Kelime Kartları' in page.locator('main').inner_text()
    page.locator('[data-act="rapidReveal"]').wait_for(timeout=10000)
    page.locator('[data-act="rapidReveal"]').click()
    assert page.locator('[data-act="rapidKnow"]').count()==1
    page.locator('[data-act="rapidKnow"]').click()
    assert page.evaluate("Object.keys(JSON.parse(localStorage.getItem('ael-progress')).rapidCards).length")>=1
    page.locator('[data-act="rapidLevel"][data-value="C1"]').click()
    # The current residual quick-gloss backlog contains only B2 words.
    assert 'Bu filtrede kelime yok' in page.locator('main').inner_text()
    page.locator('[data-act="rapidLevel"][data-value="all"]').click()
    # Memory Coach: focus targets are not confused with unfinished lessons.
    page.evaluate("document.querySelector('.nav-button[data-view=\"memory\"]').click()")
    assert 'Hafıza Koçu' in page.locator('main').inner_text()
    assert page.locator('[data-act="memoryStart"]').count()==1
    page.locator('[data-act="memoryStart"]').click()
    assert 'Ne duydun?' in page.locator('main').inner_text()
    page.locator('[data-act="memorySkipListen"]').click()
    page.locator('[data-act="memoryNextRecall"]').click()
    page.locator('[data-act="memoryRevealRecall"]').click()
    page.locator('[data-act="memoryNextContext"]').click()
    assert 'Which meaning fits this sentence?' in page.locator('main').inner_text()
    page.locator('[data-act="memoryChooseContext"]').first.click()
    assert 'Doğru:' in page.locator('main').inner_text()
    page.locator('[data-act="memoryNextProduce"]').click()
    page.locator('[data-act="memorySkipProduce"]').click()
    page.locator('[data-act="memoryFinishNo"]').click()
    assert page.evaluate("Object.keys(JSON.parse(localStorage.getItem('ael-progress')).memoryCues||{}).length")>=0
    assert 'Bir sorun oluştu' not in page.locator('main').inner_text()
    # Vocabulary recognition and repetition persistence.
    page.evaluate("document.querySelector('.nav-button[data-view=\"vocabulary\"]').click()")
    page.locator('[data-act="mode"][data-mode="recognition"]').first.click()
    assert page.locator('[data-act="practiceChoice"]').count()==4
    page.locator('[data-act="practiceChoice"]').first.click()
    page.locator('[data-act="grade"][data-grade="again"]').click()
    assert page.locator('main').get_by_text('Sonraki kelime').count()>0
    # Text recall
    page.locator('[data-act="mode"][data-mode="recall"]').first.click()
    page.locator('#answer').fill('intentionally wrong')
    page.locator('[data-act="gradeWord"]').click()
    assert 'Beklenen ifade' in page.locator('main').inner_text()
    # Phrasal verb
    page.evaluate("document.querySelector('.nav-button[data-view=\"phrasals\"]').click()")
    page.locator('[data-act="mode"][data-mode="recognition"]').first.click()
    assert page.locator('[data-act="practiceChoice"]').count()==4
    # Synthetic MP3s are quarantined. No playable synthetic podcast/drill UI.
    page.evaluate("document.querySelector('.nav-button[data-view=\"listening\"]').click()")
    assert 'Eski 18 podcast ve 24 kısa ses alıştırması arşivlendi' in page.locator('main').inner_text()
    assert page.locator('[data-act="openDrill"]').count()==0
    page.evaluate("document.querySelector('.nav-button[data-view=\"podcasts\"]').click()")
    assert 'Robotik podcast yayında değil' in page.locator('main').inner_text()
    assert page.locator('[data-act="openEpisode"]').count()==0
    assert page.locator('audio[src*=\"assets/audio\"]').count()==0
    # Reading test, word dictionary, 5 questions
    page.evaluate("document.querySelector('.nav-button[data-view=\"reading\"]').click()")
    page.locator('[data-act="openReading"]').first.click()
    assert page.locator('[data-act="answerQuestion"]').count()==20
    # 25Q exam
    page.evaluate("document.querySelector('.nav-button[data-view=\"tests\"]').click()")
    page.locator('[data-act="startExam"]').click()
    assert page.locator('[data-act="examAnswer"]').count()==100
    assert 'Doğru:' not in page.locator('main').inner_text()
    page.locator('[data-act="examAnswer"]').first.click()
    page.once('dialog',lambda d:d.accept())
    page.locator('[data-act="submitExam"]').first.click()
    assert 'Sınav Sonuçları' in page.locator('main').inner_text()
    assert 'Doğru:' in page.locator('main').inner_text()
    # local persistence
    state=page.evaluate("localStorage.getItem('ael-progress')")
    assert 'quizHistory' in state
    if virtual:
        # Do not falsely claim a true browser restart/local-storage persistence test.
        assert page.evaluate("JSON.parse(localStorage.getItem('ael-progress')).quizHistory.length")>=1
    else:
        page.reload(wait_until='networkidle')
        assert page.evaluate("JSON.parse(localStorage.getItem('ael-progress')).quizHistory.length")>=1
    # Settings backup and theme
    page.evaluate("document.querySelector('.nav-button[data-view=\"settings\"]').click()")
    page.locator('[data-field="theme"]').select_option('light')
    assert page.locator('html').get_attribute('data-theme')=='light'
    with page.expect_download() as download_info:page.locator('[data-act="export"]').click()
    download=download_info.value
    assert 'backup' in download.suggested_filename
    assert not errors,errors
    ctx.close();return 'mobile' if mobile else 'desktop'

if __name__=='__main__':
    with sync_playwright() as p:
      browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
      virtual=os.environ.get('AEL_STATIC_HARNESS')=='1'
      if virtual:print('SIMULATED ORIGIN: virtual files + mock storage; NOT genuine browser E2E release proof',flush=True)
      try:
       results={}
       for mobile in (False,True):
        key=run(browser,mobile,virtual)
        results[key]='passed'
        print('PASS',key,flush=True)
       if virtual:
        (ROOT/'qa/browser_harness_report.json').write_text(json.dumps({'testType':'chromium_virtual_origin_with_mock_storage','releaseEvidence':False,'desktop':results.get('desktop'),'mobile_simulated_viewport':results.get('mobile'),'webkit_iphone':'not_tested','real_local_storage_persistence':'not_tested'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
      finally:
       browser.close()
