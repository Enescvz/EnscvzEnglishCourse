"""Small virtual-origin Chromium UI smoke only. NOT a Safari offline proof."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]

def run():
    errors=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
        results={}
        try:
            for mobile in (False, True):
                ctx=browser.new_context(viewport={'width':390 if mobile else 1280,'height':844 if mobile else 800},device_scale_factor=1,is_mobile=mobile,has_touch=mobile)
                page=ctx.new_page()
                page.on('pageerror',lambda error:errors.append(str(error)))
                def respond(route):
                    path=(ROOT/route.request.url.split('ael.test/',1)[-1].split('?',1)[0]).resolve()
                    if not path.is_relative_to(ROOT) or not path.is_file():
                        route.fulfill(status=404,body='not found')
                    else:
                        import mimetypes
                        route.fulfill(status=200,body=path.read_bytes(),content_type=mimetypes.guess_type(path.name)[0] or 'application/octet-stream')
                page.route('https://ael.test/**',respond)
                page.evaluate("Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem:k=>(window.__store||{})[k]||null,setItem:(k,v)=>(window.__store||(window.__store={}))[k]=v,removeItem:k=>delete window.__store[k]}})")
                html=(ROOT/'index.html').read_text(encoding='utf-8').replace('<head>','<head><base href="https://ael.test/">')
                page.set_content(html,wait_until='domcontentloaded',timeout=20000)
                page.get_by_text('Real progress.').wait_for(timeout=12000)
                page.evaluate("document.querySelector('.nav-button[data-view=settings]').click()")
                text=page.locator('main').inner_text()
                assert 'Safari · Çevrimdışı kullanım' in text
                assert 'İçerikleri indir / doğrula' in text
                page.locator('[data-act="offlineCheck"]').click()
                page.locator('#offlineReadiness').get_by_text('Henüz hazır değil',exact=False).wait_for(timeout=10000)
                assert not errors,errors
                results['mobile_viewport' if mobile else 'desktop_viewport']='passed'
                ctx.close()
        finally:browser.close()
    (ROOT/'qa/safari-offline-settings-ui-smoke.json').write_text(json.dumps({'type':'virtual_origin_chromium_ui','results':results,'physicalSafari':'NOT_TESTED','realServiceWorkerOffline':'NOT_TESTED','releaseEvidence':False},ensure_ascii=False,indent=2)+'\n')
    return results
if __name__=='__main__':print(run())
