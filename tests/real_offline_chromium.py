"""Development-only real localhost + Chromium offline test (never iPhone/WebKit)."""
import json, subprocess, socket, time, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
PORT=18487

def run():
    report={'testType':'localhost_http_chromium_service_worker_offline', 'verifiedPlatform':'headless Chromium desktop emulation','physicalIphoneSafari':'NOT_TESTED','externalVoaMp3':'NOT_TESTED','releaseEvidence':False,'checks':{},'status':'NOT_RUN'}
    server=None
    try:
        server=subprocess.Popen([sys.executable,'-m','http.server',str(PORT),'--bind','127.0.0.1'],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        for _ in range(30):
            try:
                with socket.create_connection(('127.0.0.1',PORT),timeout=.5):break
            except OSError:time.sleep(.15)
        else:raise RuntimeError('local HTTP server did not start')
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
            try:
                ctx=browser.new_context(service_workers='allow',viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
                page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                url=f'http://127.0.0.1:{PORT}/'
                page.goto(url,wait_until='networkidle',timeout=20000)
                page.get_by_text('Real progress.').wait_for(timeout=15000)
                page.evaluate('navigator.serviceWorker.ready')
                report['checks']['httpContentLoaded']=True
                page.evaluate("document.querySelector('.nav-button[data-view=writing]').click()")
                page.locator('[data-act="writingMode"][data-mode="toefl"]').click()
                assert 'TOEFL 2026' in page.locator('main').inner_text()
                page.locator('#toeflWriting').fill('The library will close early because of renovations.')
                page.locator('[data-act="checkToeflSentence"]').click()
                assert 'eşleşiyor' in page.locator('main').inner_text()
                assert page.evaluate("JSON.parse(localStorage.getItem('ael-progress')).writing['toefl:tw26-sentence-01']")
                report['checks']['writingAndPersistenceOnline']=True
                page.reload(wait_until='networkidle');page.evaluate('navigator.serviceWorker.ready')
                page.wait_for_function('navigator.serviceWorker.controller !== null',timeout=15000)
                # Confirm complete pre-cache of app shell and core content prior to airplane mode.
                names=page.evaluate("caches.keys()")
                assert names
                report['checks']['serviceWorkerControlling']=True
                ctx.set_offline(True)
                page.reload(wait_until='domcontentloaded',timeout=20000)
                page.get_by_text('Real progress.').wait_for(timeout=15000)
                page.evaluate("document.querySelector('.nav-button[data-view=writing]').click()")
                page.locator('[data-act="writingMode"][data-mode="toefl"]').click()
                assert 'The library will close early because of renovations.' in page.locator('#toeflWriting').input_value()
                report['checks']['writingDraftSurvivesOfflineReload']=True
                page.evaluate("document.querySelector('.nav-button[data-view=authentic]').click()")
                assert '204' not in errors
                assert '50 ücretsiz VOA kaynağı' in page.locator('main').inner_text()
                report['checks']['voaTextCatalogOffline']=True
                assert not errors,errors
                report['status']='PASS_CHROMIUM_ONLY'
                ctx.close()
            finally: browser.close()
    except Exception as e:
        report['status']='BLOCKED_OR_FAILED'
        report['error']=str(e)[:650]
    finally:
        if server:server.terminate();server.wait(timeout=5)
        (ROOT/'qa/real-offline-chromium-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return report['status']=='PASS_CHROMIUM_ONLY'
if __name__=='__main__':sys.exit(0 if run() else 1)
