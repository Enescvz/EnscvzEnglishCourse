"""Targeted virtual Chromium smoke for 500 expressions. No real Safari or audio proof."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]
def run(browser,mobile=False):
 ctx=browser.new_context(viewport={'width':390 if mobile else 1440,'height':844 if mobile else 900},is_mobile=mobile,has_touch=mobile)
 page=ctx.new_page();errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 mime={'.js':'application/javascript','.json':'application/json','.css':'text/css','.svg':'image/svg+xml','.webmanifest':'application/manifest+json'}
 def respond(route):
  path=(ROOT/urlparse(route.request.url).path.lstrip('/')).resolve()
  if not path.is_file() or ROOT not in path.parents:route.fulfill(status=404,body='Not found');return
  route.fulfill(status=200,body=path.read_bytes(),content_type=mime.get(path.suffix,'application/octet-stream'))
 page.route('**/*',respond)
 page.set_content((ROOT/'index.html').read_text().replace('<head>','<head><base href="https://ael.test/">'),wait_until='domcontentloaded')
 page.get_by_text('Real progress.').wait_for(timeout=15000)
 page.evaluate("document.querySelector('[data-view=expressions]').click()")
 main=page.locator('main')
 assert '500/500' in main.inner_text()
 for level,count,phrase in [('B1','150','Keep you warm'),('B2','210',"I'm leaning toward"),('C1','140',"I wouldn't go so far as to say")]:
  page.locator(f'[data-act="expressionLevel"][data-value="{level}"]').click()
  text=main.inner_text()
  assert phrase in text,(level,phrase)
  assert count in text
  page.locator('[data-act="expressionPractice"]').click()
  assert 'Hafıza Koçu' in main.inner_text()
  assert level+' Kalıplar' in main.inner_text()
  assert phrase in main.inner_text()
  page.evaluate("document.querySelector('[data-view=expressions]').click()")
 # Cross-context filter: all 500 share one FSRS identity, not duplicate decks.
 page.locator('[data-act="expressionLevel"][data-value="all"]').click()
 page.locator('[data-act="expressionContext"][data-value="toefl"]').click()
 assert 'TOEFL + Daily' in main.inner_text()
 page.locator('[data-act="expressionPractice"]').click()
 assert 'Hafıza Koçu' in main.inner_text()
 assert 'TOEFL + Daily' in main.inner_text()
 page.evaluate("document.querySelector('[data-view=expressions]').click()")
 page.locator('[data-act="expressionContext"][data-value="daily"]').click()
 assert 'Yalnız Daily English' in main.inner_text()
 page.locator('[data-act="expressionContext"][data-value="all"]').click()
 assert '500/500' in main.inner_text()
 assert not errors,errors
 ctx.close()
if __name__=='__main__':
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for mobile in (False,True):
   run(browser,mobile)
   print('PASS', 'mobile' if mobile else 'desktop','virtual Chromium')
  browser.close()
