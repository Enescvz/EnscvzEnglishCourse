"""Real local Chromium service-worker/offline smoke (NOT iOS Safari, not audio QA)."""
import json
import threading
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(ROOT),**kwargs)
    def log_message(self,*args):pass

def run():
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    result={'testType':'local_http_chromium_service_worker_offline_smoke',
            'realIphoneSafari':False,'voaExternalMp3Offline':False,'humanAudioPlaybackVerified':False,
            'verified':False}
    try:
      with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
        try:
          context=browser.new_context(service_workers='allow')
          page=context.new_page()
          page.goto(f'http://127.0.0.1:{server.server_port}/',wait_until='domcontentloaded',timeout=25000)
          page.get_by_text('Real progress.').wait_for(timeout=20000)
          page.wait_for_function("() => !!navigator.serviceWorker.controller",timeout=20000)
          cache=page.evaluate("""async () => {
             const names=await caches.keys();
             const active=names.find(x=>x.startsWith('ael-dev-20261028-voa14-'));
             const c=active?await caches.open(active):null;
             return {active,reading:!!(c&&await c.match('./data/readings.json')),
                     toefl:!!(c&&await c.match('./data/toefl-core.json')),
                     voa:!!(c&&await c.match('./data/authentic-listening.json'))};
          }""")
          assert all([cache['active'],cache['reading'],cache['toefl'],cache['voa']]),cache
          context.set_offline(True)
          page.reload(wait_until='domcontentloaded',timeout=15000)
          page.get_by_text('Real progress.').wait_for(timeout=15000)
          page.evaluate("document.querySelector('.nav-button[data-view=\"reading\"]').click()")
          page.locator('[data-act="openReading"]').first.wait_for(timeout=10000)
          page.locator('[data-act="openReading"]').first.click()
          assert page.locator('[data-act="answerQuestion"]').count()==20
          page.evaluate("document.querySelector('.nav-button[data-view=\"vocabulary\"]').click()")
          assert 'TOEFL + Daily' in page.locator('main').inner_text()
          result.update({'verified':True,'offlineCoreReload':'passed',
                         'offlineReadingQuiz':'passed','offlineVocabularyNavigation':'passed',
                         'cachedContent':cache})
          context.close()
        finally:browser.close()
    finally:server.shutdown();server.server_close()
    (ROOT/'qa/offline-chromium-smoke.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    return result

if __name__=='__main__': print(json.dumps(run(),ensure_ascii=False,indent=2))
