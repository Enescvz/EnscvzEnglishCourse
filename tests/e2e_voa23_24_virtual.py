"""Targeted virtual-origin Chromium smoke for VOA 23/24. Not a real Safari/audio test."""
from playwright.sync_api import sync_playwright
from e2e_playwright import install_virtual_files

def check(browser,mobile):
 ctx=browser.new_context(viewport={'width':390 if mobile else 1440,'height':844 if mobile else 900},is_mobile=mobile,has_touch=mobile)
 page=ctx.new_page()
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 install_virtual_files(page)
 page.get_by_text('Real progress.').wait_for(timeout=10000)
 page.evaluate("document.querySelector('.nav-button[data-view=\"listening\"]').click()")
 page.locator('[data-view="authentic"]').last.click()
 assert '30 uygulama içi transkript' in page.locator('main').inner_text()
 for title,with_exclusion in [('Rock Star',True),('I Feel Super!',False)]:
  field=page.locator('[data-field="voaSearch"]')
  field.fill(title)
  page.locator('[data-act="authenticOpen"]').first.click()
  body=page.locator('main').inner_text()
  assert title in body
  assert 'ONLINE MP3 · HUMAN' in body
  assert page.locator('audio#media').count()==1
  if with_exclusion: assert 'Telif ayrımı' in body
  else: assert 'Telif ayrımı' not in body
  page.locator('[data-act="authenticToggleTranscript"]').click()
  assert page.locator('#authenticTranscript .turn').count()>35
  assert 'Bir sorun oluştu' not in page.locator('main').inner_text()
  page.locator('[data-act="authenticBack"]').click()
 assert not errors,errors
 ctx.close()
 return 'mobile' if mobile else 'desktop'

if __name__=='__main__':
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
  try:
   for mobile in [False,True]: print('PASS',check(browser,mobile),flush=True)
  finally:browser.close()
