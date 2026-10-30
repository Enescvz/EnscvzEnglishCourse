"""Virtual Chromium import UI regression; NOT a real origin, WebKit or iPhone test."""
import json
from playwright.sync_api import sync_playwright
from e2e_playwright import install_virtual_files


def run(browser,mobile):
    ctx=browser.new_context(viewport={'width':390 if mobile else 1280,'height':844 if mobile else 900},is_mobile=mobile,has_touch=mobile)
    page=ctx.new_page();errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('dialog',lambda d:d.accept())
    install_virtual_files(page)
    page.get_by_text('Real progress.',exact=False).first.wait_for(timeout=15000)
    page.evaluate("document.querySelector('.nav-button[data-view=settings]').click()")
    assert 'İlerleme yedeği' in page.locator('main').inner_text()
    assert 'silmeden' in page.locator('main').inner_text()
    payload={'app':'American English Lab','format':1,'progress':{'version':1,'settings':{'minutes':45},'cards':{'legacy-word':{'attempts':9,'last':100,'due':200}},'phrasals':{},'events':[{'at':7,'type':'recall'}]}}
    page.locator('#importFile').set_input_files({'name':'ael-backup.json','mimeType':'application/json','buffer':json.dumps(payload).encode()})
    page.wait_for_function("() => !!JSON.parse(localStorage.getItem('ael-progress'))?.cards?.['legacy-word']",timeout=5000)
    assert page.evaluate("JSON.parse(localStorage.getItem('ael-progress')).cards['legacy-word'].attempts")==9
    assert page.evaluate("JSON.parse(localStorage.getItem('ael-progress')).settings.minutes")==60 # current settings win
    assert page.evaluate("JSON.parse(localStorage.getItem('ael-progress')).events.length")==1
    # Importing the same backup twice must not double events.
    page.locator('#importFile').set_input_files({'name':'ael-backup.json','mimeType':'application/json','buffer':json.dumps(payload).encode()})
    page.wait_for_timeout(100)
    assert page.evaluate("JSON.parse(localStorage.getItem('ael-progress')).events.length")==1
    assert not errors,errors
    ctx.close()

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
    for mobile in (False,True):
        run(browser,mobile)
        print('PASS import safety virtual', 'mobile' if mobile else 'desktop',flush=True)
    browser.close()
