#!/usr/bin/env python3
"""Fast local structural browser QA for VOA pilot; does NOT assert remote audio playback."""
import contextlib
import functools
import http.server
import json
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args):pass

def run():
    handler=functools.partial(QuietHandler,directory=str(ROOT))
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler)
    port=server.server_address[1]
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    results={}
    try:
        with sync_playwright() as p:
            for name,viewport in [('desktop',{'width':1280,'height':850}),('mobile',{'width':390,'height':844})]:
                browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
                context=browser.new_context(viewport=viewport,service_workers='block')
                page=context.new_page()
                errors=[]
                page.on('pageerror',lambda err:errors.append(str(err)))
                page.goto(f'http://127.0.0.1:{port}/#/authentic',wait_until='domcontentloaded')
                page.get_by_role('heading',name='Real Voices · VOA').wait_for(timeout=10000)
                assert page.locator('[data-act="authenticOpen"]').count()==3
                page.locator('[data-act="authenticOpen"]').nth(1).click()
                assert page.get_by_role('heading',name='The Interview — Team Up and Find Out').count()==1
                assert page.locator('#media').get_attribute('src').startswith('https://voa-audio.voanews.eu/')
                assert page.locator('#authenticTranscript').is_hidden()
                page.locator('[data-act="authenticToggleTranscript"]').click()
                assert page.locator('#authenticTranscript').is_visible()
                page.locator('[data-act="authenticToggleTranscript"]').click()
                assert page.locator('#authenticTranscript').is_hidden()
                assert page.locator('[data-auth-q]').count()==6
                for i in range(6):
                    page.locator(f'[data-auth-q="{i}"] button.choice').first.click()
                page.locator('[data-act="authenticFinish"]').click()
                stored=page.evaluate("JSON.parse(localStorage.getItem('ael-progress')).authenticLessons['voa-level2-02-interview']")
                assert stored['total']==6
                assert len(errors)==0,errors
                results[name]={'state':'passed','quizSaved':True,'transcriptToggle':True,'sourceAudioLinked':True,'remoteAudioPlaybackVerified':False}
                browser.close()
    finally:server.shutdown()
    outfile=ROOT/'qa/voa-browser-pilot.json'
    outfile.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(results,ensure_ascii=False))

if __name__=='__main__':run()
