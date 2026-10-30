"""Simulated Chromium tests, NOT physical iPhone or externally verified human audio."""
from pathlib import Path
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
import argparse, json
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--desktop',action='store_true');args=p.parse_args()

def prepare(page, stored=None):
 mime={'.js':'application/javascript','.json':'application/json','.css':'text/css','.svg':'image/svg+xml','.webmanifest':'application/manifest+json'}
 def serve(route):
  if urlparse(route.request.url).hostname!='ael.test':return route.abort()
  path=(ROOT/urlparse(route.request.url).path.lstrip('/')).resolve()
  if ROOT not in path.parents or not path.is_file():return route.fulfill(status=404,body='Not found')
  return route.fulfill(status=200,body=path.read_bytes(),content_type=mime.get(path.suffix,'application/octet-stream'))
 page.route('**/*',serve)
 page.evaluate("""(stored)=>{window.__store=stored;Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem:k=>window.__store[k]??null,setItem:(k,v)=>window.__store[k]=v}})}""",stored or {})
 page.set_content((ROOT/'index.html').read_text().replace('<head>','<head><base href="https://ael.test/">'),wait_until='domcontentloaded')
 page.locator('main h1').wait_for(timeout=25000)

with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 ctx=browser.new_context(viewport={'width':1366 if args.desktop else 390,'height':860 if args.desktop else 844},is_mobile=not args.desktop,has_touch=not args.desktop,accept_downloads=True)
 page=ctx.new_page();err=[];page.on('pageerror',lambda e:err.append(str(e)));prepare(page)
 page.evaluate("document.querySelector('.nav-button[data-view=fluencyStudio]').click()")
 page.locator('[data-act="fluencyTab"][data-value="writing"]').click()
 draft='I am writing to ask whether you could recommend another suitable time for our meeting because I am unavailable tomorrow.'
 page.locator('#fluencyWriting').fill(draft)
 page.locator('#fluencyDraftStatus').get_by_text('otomatik kaydedildi').wait_for(timeout=12000)
 assert page.evaluate("JSON.parse(localStorage.getItem('ael-progress')).fluencyDrafts['write-email'].text")==draft
 page.locator('[data-act="fluencyMove"][data-value="1"]').click()
 page.locator('[data-act="fluencyMove"][data-value="-1"]').click()
 assert page.locator('#fluencyWriting').input_value()==draft,'Draft lost after navigation'
 # Simulate quota error; a failed save must block switching to another writing prompt.
 page.evaluate("(() => {localStorage.setItem=()=>{throw Error('QuotaExceededError')};return true;})()")
 page.locator('#fluencyWriting').fill(draft+' Please respond soon.')
 page.locator('#fluencyDraftStatus').get_by_text('başarısız').wait_for(timeout=12000)
 page.locator('[data-act="fluencyMove"][data-value="1"]').click()
 assert page.locator('#fluencyWriting').input_value().endswith('Please respond soon.')
 assert page.evaluate("JSON.parse(localStorage.getItem('ael-progress')).fluencyDrafts['write-email'].text")==draft
 print('PASS: autosave, persistence, quota-failure blocks navigation',flush=True)
 page2=ctx.new_page();bad='{"version":1,"cards":{'
 prepare(page2,{'ael-progress':bad})
 assert page2.get_by_text('Öğrenme kaydı koruma modunda').count()==1
 page2.evaluate("document.querySelector('.nav-button[data-view=fluencyStudio]').click()")
 page2.locator('[data-act="fluencyTab"][data-value="realLife"]').click()
 page2.locator('[data-act="fluencyChoose"]').first.click()
 page2.locator('[data-act="fluencyCheck"]').click()
 page2.locator('[data-act="fluencyCommit"][data-grade="again"]').click()
 assert page2.evaluate("localStorage.getItem('ael-progress')")==bad, 'Direct fluency write overwrote corrupt data'
 page2.evaluate("document.querySelector('.nav-button[data-view=settings]').click()")
 page2.locator('[data-field="minutes"]').select_option('30')
 assert page2.evaluate("localStorage.getItem('ael-progress')")==bad, 'Corrupt data overwritten'
 with page2.expect_download() as d:page2.locator('[data-act="exportCorrupt"]').click()
 download=d.value
 assert download.suggested_filename.startswith('ael-ham-kurtarma-')
 assert Path(download.path()).read_text()==bad
 # Recovery is deliberate and retains the valid imported card IDs.
 backup={'app':'American English Lab','format':1,'progress':{'version':1,'cards':{'recovered-card':{'last':42,'attempts':3}},'phrasals':{},'settings':{'minutes':30}}}
 page2.on('dialog',lambda dialog:dialog.accept())
 page2.locator('#importFile').set_input_files({'name':'recovery.json','mimeType':'application/json','buffer':json.dumps(backup).encode()})
 page2.wait_for_function("() => {const p=JSON.parse(localStorage.getItem('ael-progress'));return p?.cards?.['recovered-card']?.attempts===3;}")
 assert page2.get_by_text('Öğrenme kaydı koruma modunda').count()==0
 print('PASS: corrupted progress protected, raw download and deliberate recovery',flush=True)
 assert not err,err
 ctx.close();browser.close()
 print('PASS simulated', 'desktop' if args.desktop else 'mobile',flush=True)
