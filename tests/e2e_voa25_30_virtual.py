"""Virtual Chromium content and audio-state UI smoke; NOT a physical Safari/MP3 playback certification."""
from playwright.sync_api import sync_playwright
from e2e_playwright import install_virtual_files
CASES=['Only Human','Look-alikes','Fish out of Water','For the Birds',"Where There's Smoke...",'Dream a Little Dream']

def run(browser,mobile):
 ctx=browser.new_context(viewport={'width':390 if mobile else 1440,'height':844 if mobile else 900},is_mobile=mobile,has_touch=mobile)
 page=ctx.new_page();errors=[]
 page.on('pageerror',lambda exc:errors.append(str(exc)))
 install_virtual_files(page)
 page.get_by_text('Real progress.').wait_for(timeout=15000)
 page.evaluate("document.querySelector('.nav-button[data-view=authentic]').click()")
 assert '30 uygulama içi transkript' in page.locator('main').inner_text()
 for title in CASES:
  page.locator('[data-field=voaSearch]').fill(title)
  page.locator('[data-act=authenticOpen]').first.click()
  assert title in page.locator('main').inner_text()
  assert page.locator('#humanAudioStatus').count()==1
  current=page.locator('#humanAudioStatus').inner_text()
  assert current.strip(), 'Audio status must not be empty'
  assert 'onaylandı' not in current.lower(), current
  assert page.locator('audio#media').count()==1
  if title=='Dream a Little Dream':
   assert 'Telif ayrımı' in page.locator('main').inner_text()
   assert 'you can reach for the stars' not in page.locator('main').inner_text().lower()
  page.locator('[data-act=authenticToggleTranscript]').click()
  assert page.locator('#authenticTranscript .turn').count()>=40
  assert 'Bir sorun oluştu' not in page.locator('main').inner_text()
  page.locator('[data-act=authenticBack]').click()
 assert not errors,errors
 ctx.close()
 return 'mobile virtual Chromium' if mobile else 'desktop virtual Chromium'

if __name__=='__main__':
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
  try:
   for mobile in [False,True]:print('PASS',run(browser,mobile),flush=True)
  finally:browser.close()
