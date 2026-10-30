"""Targeted virtual Chromium memory-coach regression; NOT Safari, HTTP or offline QA."""
from playwright.sync_api import sync_playwright
from e2e_playwright import install_virtual_files


def run(browser, mobile):
    context=browser.new_context(viewport={'width':390 if mobile else 1350,'height':844 if mobile else 900},is_mobile=mobile,has_touch=mobile)
    page=context.new_page()
    errors=[]
    page.on('pageerror',lambda e: errors.append(str(e)))
    install_virtual_files(page)
    page.get_by_text('Real progress.',exact=False).first.wait_for(timeout=15000)
    page.evaluate("document.querySelector('.nav-button[data-view=memory]').click()")
    assert 'Hafıza Koçu' in page.locator('main h1').inner_text()
    page.locator('[data-act="memoryScope"][data-value="toefl"]').click()
    assert '🎓 TOEFL + Daily' in page.locator('main').inner_text()
    assert page.locator('[data-act="memoryStart"]').count()==1
    page.locator('[data-act="memoryStart"]').click()
    assert 'sentetik en-US TTS' in page.locator('main').inner_text()
    page.locator('[data-act="memorySkipListen"]').click()
    page.locator('[data-act="memoryNextRecall"]').click()
    assert 'bağımsız hatırlama testi' in page.locator('main').inner_text()
    assert page.locator('main details').count()==0
    page.locator('[data-act="memoryRevealRecall"]').click()
    page.locator('[data-act="memoryNextContext"]').click()
    assert page.locator('[data-act="memoryChooseContext"]').count()==4
    page.locator('[data-act="memoryChooseContext"]').first.click()
    page.locator('[data-act="memoryNextProduce"]').click()
    page.locator('[data-act="memorySkipProduce"]').click()
    page.locator('[data-act="memoryFinishNo"]').click()
    assert 'Bir sorun oluştu' not in page.locator('main').inner_text()
    assert not errors,errors
    context.close()

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
    for mobile in (False,True):
        run(browser,mobile)
        print('PASS virtual', 'mobile' if mobile else 'desktop',flush=True)
    browser.close()
