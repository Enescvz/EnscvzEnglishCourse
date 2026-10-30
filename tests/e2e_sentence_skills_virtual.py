"""Targeted simulated-origin UI test. Not a real iPhone Safari/offline release test."""
import json
from pathlib import Path
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
def setup(page):
 mime={'.js':'application/javascript','.json':'application/json','.css':'text/css','.svg':'image/svg+xml','.webmanifest':'application/manifest+json'}
 def route(r):
  path=(ROOT/urlparse(r.request.url).path.lstrip('/')).resolve()
  if ROOT not in path.parents or not path.is_file():return r.fulfill(status=404,body='Not found')
  return r.fulfill(status=200,body=path.read_bytes(),content_type=mime.get(path.suffix,'application/octet-stream'))
 page.route('**/*',route)
 page.evaluate("Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem:k=>(window.__store||{})[k]||null,setItem:(k,v)=>(window.__store||(window.__store={}))[k]=v}})")
 page.set_content((ROOT/'index.html').read_text().replace('<head>','<head><base href="https://ael.test/">'),wait_until='domcontentloaded')
 page.locator('main h1').wait_for(timeout=25000)
def click_nav(page,key):page.evaluate("k=>document.querySelector('.nav-button[data-view=\"'+k+'\"]').click()",key)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 for mobile in (False,True):
  ctx=browser.new_context(viewport={'width':390 if mobile else 1366,'height':844 if mobile else 860},is_mobile=mobile,has_touch=mobile)
  page=ctx.new_page();errs=[];page.on('pageerror',lambda e:errs.append(str(e)))
  setup(page);click_nav(page,'sentenceSkills')
  assert page.get_by_text('340 özgün alıştırma').count()>0
  assert page.locator('[data-act="skillOpen"]').count()==12
  page.locator('[data-act="skillOpen"]').first.click()
  assert page.locator('[data-act="skillToken"]').count()>4
  # Answer model order through original token values (unique index mapping)
  dataset=json.loads((ROOT/'data/sentence-skills.json').read_text())
  ex=dataset['lessons'][0]['exercises'][0];tokens=ex['tokens'];import re
  gold=re.findall(r"[\w]+(?:[’'-][\w]+)*|[^\w\s]",ex['modelAnswer'],flags=re.UNICODE)
  used=set()
  for tok in gold:
   ix=next(i for i,t in enumerate(tokens) if i not in used and t==tok);used.add(ix)
   page.locator(f'[data-act="skillToken"][data-index="{ix}"]').click()
  page.locator('[data-act="skillCheck"]').click()
  assert 'Referans yanıtla eşleşti' in page.locator('main').inner_text()
  page.locator('[data-act="skillGrade"][data-grade="good"]').click()
  assert page.evaluate("Object.keys(JSON.parse(localStorage.getItem('ael-progress')).skillCards).length")==1
  # Jump to cloze, fill expected, advance
  for _ in range(2):page.locator('[data-act="skillNext"]').click()
  assert page.locator('#skillAnswer').count()==1
  cloze=page.locator('.skill-prompt').inner_text()
  assert '_____' in cloze
  page.locator('#skillAnswer').fill('does') # choose content via data rather than assumption below
  # Free answer independent of reference, not falsely auto-graded
  for _ in range(4):page.locator('[data-act="skillNext"]').click()
  assert page.locator('#skillAnswer').count()==1
  page.locator('#skillAnswer').fill('Could you tell me more about this?')
  page.locator('[data-act="skillCheck"]').click()
  assert 'Serbest cevap · öz değerlendirme' in page.locator('main').inner_text()
  page.locator('[data-act="skillGrade"][data-grade="hard"]').click()
  assert page.evaluate("Object.keys(JSON.parse(localStorage.getItem('ael-progress')).skillCards).length")==2
  # old cards must not be erased
  assert page.evaluate("JSON.parse(localStorage.getItem('ael-progress')).version")==1
  page.screenshot(path=str(ROOT/('qa/sentence-skill-mobile-virtual.png' if mobile else 'qa/sentence-skill-desktop-virtual.png')),full_page=True)
  assert not errs,errs
  print('PASS simulated', 'mobile' if mobile else 'desktop',flush=True)
  ctx.close()
 browser.close()
