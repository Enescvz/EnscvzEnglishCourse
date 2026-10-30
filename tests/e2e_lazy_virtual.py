"""End-to-end simulated Chromium lazy-loading and navigation tests. NOT iPhone Safari."""
import sys
from pathlib import Path
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 ctx=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
 page=ctx.new_page();req=[];errors=[]
 page.on('pageerror',lambda exc:errors.append(str(exc)))
 def serve(route):
  u=urlparse(route.request.url)
  path=(ROOT/u.path.lstrip('/')).resolve()
  req.append(u.path.lstrip('/'))
  if not path.is_file() or ROOT not in path.parents:return route.fulfill(status=404,body='missing')
  return route.fulfill(status=200,body=path.read_bytes(),content_type={'.json':'application/json','.js':'application/javascript','.css':'text/css','.svg':'image/svg+xml'}.get(path.suffix,'application/octet-stream'))
 page.route('**/*',serve)
 page.evaluate("Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem:k=>(window.__store||{})[k]||null,setItem:(k,v)=>(window.__store||(window.__store={}))[k]=v,removeItem:k=>delete window.__store[k]}})")
 page.set_content((ROOT/'index.html').read_text().replace('<head>','<head><base href="https://ael.test/">'),wait_until='domcontentloaded')
 page.get_by_text('Real progress.',exact=False).wait_for(timeout=25000)
 first=set(req)
 assert 'data/vocabulary.json' in first
 assert 'data/phrasals.json' in first
 assert 'data/authentic-listening.json' not in first
 assert 'data/voa-source-catalog.json' not in first
 assert 'data/fluency-focus.json' not in first
 assert 'data/daily-expressions.json' not in first
 page.evaluate("document.querySelector('.nav-button[data-view=reading]').click()")
 page.locator('main h1').get_by_text('Reading Library').wait_for(timeout=15000)
 assert 'data/readings.json' in req
 page.evaluate("document.querySelector('.nav-button[data-view=listening]').click(); document.querySelector('.nav-button[data-view=fluencyStudio]').click(); document.querySelector('.nav-button[data-view=authentic]').click()")
 page.locator('main h1').get_by_text('Real Voices').wait_for(timeout=25000)
 assert 'data/authentic-listening.json' in req
 assert req.count('data/authentic-listening.json')==1,req.count('data/authentic-listening.json')
 assert 'data/fluency-studio.json' in req
 assert 'data/voa-source-catalog.json' in req
 # Full source library must not become a falsely reported offline human voice count.
 assert '50 ücretsiz VOA kaynağı' in page.locator('main').inner_text()
 # Navigate every available module with actual asynchronous data loading.
 for view in ('home','listening','vocabulary','phrasals','expressions','fluencyStudio','sentenceSkills','podcasts','authentic','reading','grammar','speaking','writing','toefl','conversations','pronunciation','tests','review','analytics','settings','catalog','rapid','memory'):
  page.evaluate("view => document.querySelector('.nav-button[data-view='+view+']').click()",view)
  page.wait_for_function("() => document.querySelector('main .section h1') !== null",timeout=25000)
  assert 'İçerik yüklenemedi' not in page.locator('main').inner_text(),view
  assert 'Bir sorun oluştu' not in page.locator('main').inner_text(),view
 # Daily Writing autosave must flush before navigating away, with its exact text and ID.
 page.evaluate("document.querySelector('.nav-button[data-view=writing]').click()")
 page.locator('#writing').wait_for(timeout=15000)
 sample='I am writing a detailed email because I would like to improve my English and clarify my plans.'
 page.locator('#writing').fill(sample)
 page.evaluate("document.querySelector('.nav-button[data-view=home]').click()")
 page.get_by_text('Real progress.',exact=False).wait_for(timeout=15000)
 assert page.evaluate("JSON.parse(localStorage.getItem('ael-progress')).writing['0']") == sample
 page.evaluate("document.querySelector('.nav-button[data-view=writing]').click()")
 page.locator('#writing').wait_for(timeout=15000)
 assert page.locator('#writing').input_value()==sample
 # A quota error must not throw away the unsaved text or navigate away.
 page.evaluate("() => { localStorage.setItem=(key,value)=>{throw Error('QuotaExceededError: storage full')}; return true; }")
 second=sample+' One more important sentence.'
 page.locator('#writing').fill(second)
 page.evaluate("document.querySelector('.nav-button[data-view=home]').click()")
 assert page.locator('#writing').input_value()==second
 assert 'kaydedilemedi' in page.locator('main').inner_text().lower()
 assert not errors,errors
 print('PASS virtual mobile initial-load and concurrent lazy routes:',len(first),'boot requests;',len(req),'total requests')
 browser.close()
