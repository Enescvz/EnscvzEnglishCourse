"""Simulated-origin Chromium UI smoke. NOT physical Safari or verified audio playback."""
import json
from pathlib import Path
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]

def prepare(page):
 mime={'.js':'application/javascript','.json':'application/json','.css':'text/css','.svg':'image/svg+xml','.webmanifest':'application/manifest+json'}
 def serve(r):
  if urlparse(r.request.url).hostname!='ael.test':return r.abort()
  path=(ROOT/urlparse(r.request.url).path.lstrip('/')).resolve()
  if ROOT not in path.parents or not path.is_file():return r.fulfill(status=404,body='Not found')
  return r.fulfill(status=200,body=path.read_bytes(),content_type=mime.get(path.suffix,'application/octet-stream'))
 page.route('**/*',serve)
 page.evaluate("Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem:k=>(window.__store||{})[k]||null,setItem:(k,v)=>(window.__store||(window.__store={}))[k]=v}})")
 page.set_content((ROOT/'index.html').read_text().replace('<head>','<head><base href="https://ael.test/">'),wait_until='domcontentloaded')
 page.locator('main h1').wait_for(timeout=25000)

with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 for mobile in (True,):
  ctx=browser.new_context(viewport={'width':390 if mobile else 1366,'height':844 if mobile else 860},is_mobile=mobile,has_touch=mobile)
  page=ctx.new_page();errs=[];page.on('pageerror',lambda e:errs.append(str(e)))
  prepare(page)
  page.evaluate("document.querySelector('.nav-button[data-view=fluencyStudio]').click()")
  assert '8 entegre uygulama' in page.locator('main').inner_text()
  assert page.locator('[data-act="fluencyTab"]').count()==8
  print('RUN','# First human source + comprehension; missing listened gate',flush=True)
  # First human source + comprehension; missing listened gate
  page.locator('[data-act="fluencyChoose"]').first.click();page.locator('[data-act="fluencyCheck"]').click()
  assert page.locator('[data-act="fluencyCommit"]').count()==0
  page.locator('#fluencyListened').check();page.locator('[data-act="fluencyCheck"]').click()
  assert page.locator('[data-act="fluencyCommit"]').count()>=2
  page.locator('[data-act="fluencyCommit"][data-grade="again"]').click()
  assert page.evaluate("Object.keys(JSON.parse(localStorage.getItem('ael-progress')).fluencyCards).length")==1
  print('RUN','# Real-life branching',flush=True)
  # Real-life branching: answer, feedback, save then advance
  page.locator('[data-act="fluencyTab"][data-value="realLife"]').click()
  assert 'Hotel check-in' in page.locator('main').inner_text()
  page.locator('[data-act="fluencyChoose"]').first.click();page.locator('[data-act="fluencyCheck"]').click()
  page.locator('[data-act="fluencyCommit"][data-grade="hard"]').click()
  page.locator('[data-act="fluencyStepNext"]').click()
  assert 'Adım 2/3' in page.locator('main').inner_text()
  print('RUN','# Dictation:',flush=True)
  # Dictation: no audio credit without self report, hidden model, comparison
  page.locator('[data-act="fluencyTab"][data-value="dictation"]').click()
  assert page.locator('audio#media').count()==1
  page.locator('#fluencyAnswer').fill('This is a deliberately partial transcript.')
  page.locator('#fluencyListened').check();page.locator('[data-act="fluencyCheck"]').click()
  assert 'kelime eşleşmesi' in page.locator('main').inner_text()
  page.locator('[data-act="fluencyCommit"][data-grade="again"]').click()
  print('RUN','# Error coach now',flush=True)
  # Error coach now reflects actual mistakes
  page.locator('[data-act="fluencyTab"][data-value="errors"]').click()
  assert 'Hata/tekrar kaydı' in page.locator('main').inner_text()
  assert page.locator('[data-act="fluencyFixError"]').count()>0
  print('RUN','# Writing: preserve',flush=True)
  # Writing: preserve draft on analysis and storage
  page.locator('[data-act="fluencyTab"][data-value="writing"]').click()
  page.locator('#fluencyWriting').fill('I would like to reschedule our meeting because I have a previous commitment. Could we meet tomorrow instead?')
  page.locator('[data-act="fluencyWritingCheck"]').click()
  assert 'gramer' in page.locator('.fluency-audit-live').inner_text().lower() or 'Gramer' in page.locator('.fluency-audit-live').inner_text()
  assert 'reschedule our meeting' in page.locator('#fluencyWriting').input_value()
  page.locator('[data-act="fluencySaveDraft"]').click()
  assert page.evaluate("JSON.parse(localStorage.getItem('ael-progress')).fluencyDrafts['write-email'].text.includes('reschedule')")
  print('RUN','# Thinking requires',flush=True)
  # Thinking requires actual text and labels self assessment.
  page.locator('[data-act="fluencyTab"][data-value="thinking"]').click()
  page.locator('#fluencyAnswer').fill('Thank you for your invitation, but I already have plans that night.')
  page.locator('[data-act="fluencyCheck"]').click()
  assert 'Örnek yanıtla karşılaştır' in page.locator('main').inner_text()
  page.locator('[data-act="fluencyCommit"][data-grade="good"]').click()
  print('RUN','# Bridge uses',flush=True)
  # Bridge uses same original VOAs, no invented file.
  page.locator('[data-act="fluencyTab"][data-value="bridge"]').click()
  assert page.locator('audio#media').count()==1
  assert 'Okuma aşaması' in page.locator('main').inner_text()
  print('RUN','# Adaptive plan',flush=True)
  # Adaptive plan linked actions.
  page.locator('[data-act="fluencyTab"][data-value="adaptive"]').click()
  assert page.locator('[data-act="fluencyPlanGo"]').count()==4
  assert not errs,errs
  page.screenshot(path=str(ROOT/('qa/fluency-mobile-virtual.png' if mobile else 'qa/fluency-desktop-virtual.png')),full_page=True)
  print('PASS simulated', 'mobile' if mobile else 'desktop',flush=True)
  ctx.close()
 browser.close()
