import asyncio, os, sys
from urllib.parse import urlparse, parse_qs
from playwright.async_api import async_playwright
sys.stdout.reconfigure(encoding='utf-8')
SKEL='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light}body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style></head><body>@@BODY@@</body></html>'
open('_wrap.html','w',encoding='utf-8').write(SKEL.replace('@@BODY@@',open('atlas.html',encoding='utf-8').read()))
BASE='file://'+os.path.abspath('_wrap.html')
F=[]
def ck(n,c,d=''):
    print(('PASS  ' if c else 'FAIL  ')+n+(('  → '+str(d)) if d and not c else ''))
    if not c: F.append(n)
def q(url): return {k:v[0] for k,v in parse_qs(urlparse(url).query).items()}
STATE="""()=>({lang:document.documentElement.lang, year:+document.getElementById('yearNum').textContent,
  h3:document.querySelector('#pbody h3')?.textContent||null,
  tab:document.querySelector('.ptabs button[aria-selected="true"]')?.dataset.tab})"""

async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch()
        ctx=await b.new_context(viewport={'width':1280,'height':860}); pg=await ctx.new_page()
        e=[]; pg.on('pageerror',lambda x:e.append(str(x)))
        async def load(params=''):
            await pg.goto(BASE+params); await pg.wait_for_timeout(1300)
            return await pg.evaluate(STATE)
        async def settle(): await pg.wait_for_timeout(450)   # the URL write is debounced

        # --- first visit: Arabic by default, and the URL says so ---
        s=await load()
        ck('Arabic is the default language on a first visit', s['lang']=='ar', s)
        await settle(); u=q(pg.url)
        ck('the URL records language and year on load', u.get('lang')=='ar' and u.get('year')=='554', pg.url)

        # --- a link restores language and year ---
        s=await load('?lang=en&year=600')
        ck('?lang=en opens in English', s['lang']=='en', s)
        ck('?year=600 opens on 600', s['year']==600, s)

        # --- a link to an event opens it, on its own year and tab ---
        s=await load('?lang=en&event=imru-death')
        ck('?event= opens that event', s['h3']=='Imruʾ al-Qays dies near Ankara', s)
        ck('an event link lands on the event\'s year and tab', s['year']==565 and s['tab']=='events', s)
        await settle(); u=q(pg.url)
        ck('the URL keeps the open event and its year', u.get('event')=='imru-death' and u.get('year')=='565', pg.url)

        # --- a figure keeps the year the link gives ---
        s=await load('?lang=en&person=imru-al-qays-poet&year=560')
        ck('?person= opens that figure', s['h3']=='Imruʾ al-Qays', s)
        ck('a figure link keeps its own year', s['year']==560 and s['tab']=='people', s)

        for kind,rid,name in [('place','hira','al-Ḥīra'),('tribe','taghlib','Taghlib'),('power','lakhmids',None)]:
            s=await load(f'?lang=en&{kind}={rid}')
            ok = s['h3'] is not None and (name is None or name in s['h3'])
            ck(f'?{kind}= opens that record', ok, s)

        # --- nonsense is ignored, not fatal ---
        await pg.evaluate('()=>localStorage.clear()')   # no saved language, so the default shows
        s=await load('?lang=xx&year=abc&event=no-such-event&tab=nope')
        ck('bad parameters fall back to the defaults', s['lang']=='ar' and s['year']==554 and s['h3'] is None and s['tab']=='all', s)
        s=await load('?lang=en&year=9999')
        ck('an out-of-range year is clamped', s['year']==640, s)

        # --- whose language is it ---
        await pg.evaluate("()=>localStorage.setItem('ja-prefs',JSON.stringify({lang:'en',us:1}))")   # what older versions saved for everyone
        s=await load()
        ck('a language saved automatically by an older version does not override the Arabic default', s['lang']=='ar', s)
        await pg.click('#langBtn'); await pg.wait_for_timeout(300)
        s=await load()
        ck('a language chosen with the button is remembered', s['lang']=='en', s)
        s=await load('?lang=ar')
        ck('a ?lang= link shows its language', s['lang']=='ar', s)
        s=await load()
        ck('opening a ?lang= link does not overwrite the reader\'s own choice', s['lang']=='en', s)
        await pg.evaluate('()=>localStorage.clear()')

        # --- parameters that are not the atlas's own are left alone ---
        await load('?v=7&lang=en&year=600'); await settle(); u=q(pg.url)
        ck('other query parameters survive the URL rewrite', u.get('v')=='7' and u.get('year')=='600', pg.url)

        # --- the URL follows the app ---
        await load('?lang=en&event=imru-death')
        await pg.evaluate("()=>{const r=document.getElementById('range');r.value=500;r.dispatchEvent(new Event('input',{bubbles:true}));}")
        await settle(); u=q(pg.url)
        ck('moving the slider updates the year and drops the selection', u.get('year')=='500' and 'event' not in u, pg.url)
        await pg.click('[data-tab="tribes"]'); await settle(); u=q(pg.url)
        ck('a tab change is in the URL', u.get('tab')=='tribes', pg.url)
        await pg.locator('#pbody .ev[data-tribe]').first.click(); await settle(); u=q(pg.url)
        ck('opening a record puts it in the URL', 'tribe' in u and 'tab' not in u, pg.url)
        await pg.click('#langBtn'); await settle(); u=q(pg.url)
        ck('switching language updates the URL', u.get('lang')=='ar', pg.url)
        # and a copied URL reproduces what was on screen
        before=await pg.evaluate(STATE); s=await load('?'+urlparse(pg.url).query)
        ck('reloading the URL reproduces the same view', s==before, (before,s))

        # --- accessibility settings: applied, saved, survive a reload, reset ---
        await load('?lang=en&tab=display')
        for seg,v,attr,want in [('us','1.75',None,None),('lh','loose','data-lh','loose'),('spacing','wide','data-spacing','wide'),
                                ('reduce','on','data-reduce','on'),('links','underline','data-links','underline'),
                                ('focus','strong','data-focus','strong')]:
            btn=pg.locator(f'[data-seg="{seg}"] button[data-v="{v}"]')
            ck(f'Display has a "{seg}" option {v}', await btn.count()==1)
            if await btn.count():
                await btn.click(); await pg.wait_for_timeout(150)
                if attr: ck(f'{seg}={v} is applied to the page', await pg.evaluate(f"()=>document.documentElement.getAttribute('{attr}')")==want)
        us=await pg.evaluate("()=>getComputedStyle(document.documentElement).getPropertyValue('--us').trim()")
        ck('the largest text size is applied', us=='1.75', us)
        await pg.reload(); await pg.wait_for_timeout(1200)
        kept=await pg.evaluate("()=>['data-lh','data-spacing','data-reduce','data-links','data-focus'].map(a=>document.documentElement.getAttribute(a))")
        ck('accessibility settings survive a reload', kept==['loose','wide','on','underline','strong'], kept)
        tr=await pg.evaluate("()=>getComputedStyle(document.getElementById('tip')).transitionDuration")
        ck('reduced motion removes transitions', tr in ('1e-05s','0s') or tr.startswith('1e-'), tr)
        await load('?lang=en&event=dam-breach-449')          # an event with source links to look at
        lnk=await pg.evaluate("()=>[...document.querySelectorAll('#pbody a')].map(a=>getComputedStyle(a).textDecorationLine)")
        ck('links are underlined when asked, source cards included', lnk and all('underline' in x for x in lnk), lnk)
        await pg.click('[data-tab="display"]'); await pg.wait_for_timeout(300)
        await pg.click('[data-reset-prefs]'); await pg.wait_for_timeout(300)
        back=await pg.evaluate("()=>[getComputedStyle(document.documentElement).getPropertyValue('--us').trim(),document.documentElement.getAttribute('data-lh'),document.documentElement.getAttribute('data-reduce')]")
        ck('reset restores the default reading settings', back==['1','normal','auto'], back)
        ck('reset keeps the chosen language', (await pg.evaluate("()=>document.documentElement.lang"))=='en')

        # --- on a phone, in both languages: links restore, and the largest text fits ---
        OVERLAP="""()=>{const r=s=>{const b=document.querySelector(s)?.getBoundingClientRect();return b&&b.width?b:null};
          const hit=(a,b)=>a&&b&&!(a.right<=b.left||b.right<=a.left||a.bottom<=b.top||b.bottom<=a.top);
          const p=r('#focuspill'); return ['#scalebar .bar','#scaletxt','#zoomlvl','#zin','#zout','#zfit'].filter(s=>hit(p,r(s)));}"""
        for lang,title in [('ar','وفاةُ امرئ القيس'),('en','Imruʾ al-Qays dies near Ankara')]:
            ph=await b.new_page(viewport={'width':390,'height':844})   # fresh storage: nothing left from the desktop run
            await ph.goto(BASE+f'?lang={lang}&event=imru-death'); await ph.wait_for_timeout(1300)
            s=await ph.evaluate(STATE)
            ck(f'phone/{lang}: an event link opens that event on its year', s['h3']==title and s['year']==565 and s['lang']==lang, s)
            await ph.evaluate("()=>document.querySelector('[data-tab=\"display\"]').click()"); await ph.wait_for_timeout(400)
            await ph.evaluate("()=>document.querySelector('[data-seg=\"us\"] button[data-v=\"1.75\"]').click()"); await ph.wait_for_timeout(500)
            sw=await ph.evaluate("()=>[document.documentElement.scrollWidth,document.documentElement.clientWidth]")
            ck(f'phone/{lang}: largest text has no horizontal scroll', sw[0]<=sw[1], sw)
            await ph.evaluate("()=>document.querySelector('[data-tab=\"events\"]').click()"); await ph.wait_for_timeout(500)
            ov=await ph.evaluate(OVERLAP)
            ck(f'phone/{lang}: at the largest text the filter pill overlaps nothing', not ov, ov)
            mh=await ph.evaluate("()=>document.getElementById('map').getBoundingClientRect().height")
            ck(f'phone/{lang}: at the largest text the map keeps most of the screen', mh>=520, mh)
            await ph.close()
        ck('no errors', not e, e)
        await b.close()
    print('\nFAILURES:', F or 'none'); sys.exit(1 if F else 0)
asyncio.run(main())
