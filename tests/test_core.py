import asyncio, os, sys
from playwright.async_api import async_playwright
SKEL='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light}body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style></head><body>@@BODY@@</body></html>'
open('_wrap.html','w',encoding='utf-8').write(SKEL.replace('@@BODY@@',open('atlas.html',encoding='utf-8').read()))
FAILS=[]
def check(name, cond, detail=''):
    print(('PASS  ' if cond else 'FAIL  ')+name+(('  → '+str(detail)) if detail and not cond else ''))
    if not cond: FAILS.append(name)

async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch()
        pg=await b.new_page(viewport={'width':1280,'height':860})
        errs=[]
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append(m.text) if m.type=='error' and 'TUNNEL' not in m.text and 'ERR_' not in m.text else None)
        await pg.goto('file://'+os.path.abspath('_wrap.html')+'?lang=en'); await pg.wait_for_timeout(1500)

        # --- autocomplete ---
        await pg.fill('#search','antar'); await pg.wait_for_timeout(350)
        rows=await pg.locator('#sg .sgrow').count()
        check('autocomplete shows suggestions for "antar"', rows>0, rows)
        txt=await pg.locator('#sg .sgrow').first.inner_text()
        check('suggestion row names its type', 'Figure' in txt or 'Event' in txt or 'Place' in txt, txt)
        icons=await pg.locator('#sg .sgrow svg.ic').count()
        check('every suggestion carries an icon', icons==rows, f'{icons} icons / {rows} rows')

        # arabic query
        await pg.fill('#search','الحيرة'); await pg.wait_for_timeout(350)
        n=await pg.locator('#sg .sgrow').count()
        check('Arabic query matches', n>0, n)

        # tribe appears
        await pg.fill('#search','taghlib'); await pg.wait_for_timeout(350)
        t=await pg.locator('#sg').inner_text()
        check('tribes appear in suggestions', 'Tribe' in t, t[:90])

        # keyboard nav + enter
        await pg.fill('#search','yawm halima'); await pg.wait_for_timeout(300)
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(600)
        year=await pg.inner_text('#yearNum')
        check('Enter on a suggestion jumps the year', year=='554', year)
        panel=await pg.inner_text('#pbody')
        check('selection opens its detail', 'Ḥalīma' in panel or 'Halima' in panel, panel[:80])
        up=panel.upper()
        check('event detail is typed as an event', 'EVENT' in up, panel[:60])
        check('event detail shows connections', ('FIGURES' in up or 'TRIBES' in up or 'POWERS' in up), panel[:300])
        check('event detail keeps the dispute visible', 'DISAGREE' in up, panel[:300])

        # escape closes
        await pg.fill('#search','mecca'); await pg.wait_for_timeout(300)
        await pg.keyboard.press('Escape'); await pg.wait_for_timeout(200)
        check('Escape closes the list', await pg.locator('#sg').is_hidden())

        # --- tooltip types ---
        await pg.click('[data-tab="places"]'); await pg.wait_for_timeout(400)
        await pg.click('#pbody .chip[data-place]'); await pg.wait_for_timeout(700)
        pt=await pg.inner_text('#pbody')
        check('place detail has a type header', 'PLACE' in pt.upper(), pt[:60])

        # tribe detail + cross links
        await pg.fill('#search','bakr'); await pg.wait_for_timeout(300)
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(700)
        tt=await pg.inner_text('#pbody')
        check('tribe detail is typed and lists linked events', 'TRIBE' in tt.upper() and 'event' in tt.lower(), tt[:120])

        # --- wheel: trackpad pan vs mouse zoom ---
        await pg.click('[data-tab="legend"]'); await pg.wait_for_timeout(200)
        before=await pg.evaluate("()=>document.getElementById('root').getAttribute('transform')")
        await pg.mouse.move(400,500)
        await pg.evaluate("""()=>{const m=document.getElementById('map');
          m.dispatchEvent(new WheelEvent('wheel',{deltaX:40,deltaY:12.5,deltaMode:0,bubbles:true,cancelable:true,clientX:400,clientY:500}));}""")
        await pg.wait_for_timeout(250)
        after=await pg.evaluate("()=>document.getElementById('root').getAttribute('transform')")
        import re
        sb=float(re.search(r'scale\(([\d.]+)\)',before).group(1)); sa=float(re.search(r'scale\(([\d.]+)\)',after).group(1))
        tb=re.search(r'translate\(([-\d.]+) ([-\d.]+)\)',before).groups(); ta=re.search(r'translate\(([-\d.]+) ([-\d.]+)\)',after).groups()
        check('trackpad two-finger drag pans, does not zoom', abs(sa-sb)<1e-6 and tb!=ta, f'{sb}->{sa}, {tb}->{ta}')

        await pg.evaluate("""()=>{const m=document.getElementById('map');
          m.dispatchEvent(new WheelEvent('wheel',{deltaX:0,deltaY:-120,deltaMode:0,bubbles:true,cancelable:true,clientX:400,clientY:500}));}""")
        await pg.wait_for_timeout(250)
        after2=await pg.evaluate("()=>document.getElementById('root').getAttribute('transform')")
        s2=float(re.search(r'scale\(([\d.]+)\)',after2).group(1))
        check('mouse wheel zooms in', s2>sa, f'{sa}->{s2}')

        await pg.evaluate("""()=>{const m=document.getElementById('map');
          m.dispatchEvent(new WheelEvent('wheel',{deltaX:0,deltaY:-30,ctrlKey:true,deltaMode:0,bubbles:true,cancelable:true,clientX:400,clientY:500}));}""")
        await pg.wait_for_timeout(250)
        s3=float(re.search(r'scale\(([\d.]+)\)',await pg.evaluate("()=>document.getElementById('root').getAttribute('transform')")).group(1))
        check('trackpad pinch zooms', s3>s2, f'{s2}->{s3}')

        # --- map interaction basics ---
        await pg.click('#zfit'); await pg.wait_for_timeout(300)
        await pg.mouse.move(400,500); await pg.mouse.down(); await pg.mouse.move(520,540,steps=6); await pg.mouse.up()
        await pg.wait_for_timeout(200)
        check('drag pans the map', await pg.evaluate("()=>document.getElementById('root').getAttribute('transform')")!=before)

        # --- map markers exist and have distinct shapes ---
        await pg.click('#zfit'); await pg.wait_for_timeout(400)
        probe="""()=>{const g=document.querySelector('.L-places');
          return {n:g.children.length, circ:g.querySelectorAll('circle').length,
                  rect:g.querySelectorAll('rect').length, path:g.querySelectorAll('path').length,
                  ev:document.querySelectorAll('.L-events path').length,
                  lbl:g.querySelectorAll('text').length};}"""
        far=await pg.evaluate(probe)
        check('zoomed out: plain dots, no symbols', far['rect']==0 and far['path']==0, far)
        check('zoomed out: few places on the map', far['n']<45, far)
        for _ in range(6):
            await pg.click('#zin'); await pg.wait_for_timeout(130)
        await pg.wait_for_timeout(400)
        near=await pg.evaluate(probe)
        check('zoomed in: more places appear', near['n']>far['n'], f"{far['n']} -> {near['n']}")
        check('zoomed in: symbols replace dots', near['rect']>0 or near['path']>0, near)
        check('zoomed in: labels appear', near['lbl']>far['lbl'], f"{far['lbl']} -> {near['lbl']}")
        check('events draw as diamonds', near['ev']>0, near)
        await pg.click('#zfit'); await pg.wait_for_timeout(400)

        # --- theme cycles all three ways ---
        seen=[]
        for _ in range(4):
            await pg.click('#themeBtn'); await pg.wait_for_timeout(180)
            seen.append(await pg.evaluate("()=>document.documentElement.getAttribute('data-theme')"))
        check('theme cycles light -> dark -> auto and back', seen==['light','dark',None,'light'], seen)

        # --- tribes tab ---
        await pg.click('[data-tab="tribes"]'); await pg.wait_for_timeout(400)
        tb=await pg.inner_text('#pbody')
        check('tribes tab lists tribes', 'tribes' in tb.lower() and 'Taghlib' in tb, tb[:80])
        cnt=await pg.locator('#pbody .ev[data-tribe]').count()
        check('tribes tab shows every tribe', cnt==26, cnt)
        await pg.click('#pbody .ev[data-tribe]'); await pg.wait_for_timeout(500)
        check('tribe card opens its detail', 'TRIBE' in (await pg.inner_text('#pbody')).upper())

        # --- play / slider ---
        await pg.click('#play'); await pg.wait_for_timeout(900); await pg.click('#play')
        y2=await pg.inner_text('#yearNum')
        check('play advances the year', y2!='554', y2)

        # --- display settings persist into the DOM ---
        await pg.click('[data-tab="display"]'); await pg.wait_for_timeout(300)
        await pg.click('[data-seg="wheel"] button:nth-child(2)'); await pg.wait_for_timeout(300)
        check('wheel setting applies', await pg.evaluate("()=>JSON.parse(localStorage.getItem('ja-prefs')).wheel")=='pan')
        await pg.click('[data-seg="contrast"] button:nth-child(2)'); await pg.wait_for_timeout(300)
        check('contrast attribute set', await pg.evaluate("()=>document.documentElement.getAttribute('data-contrast')")=='high')
        await pg.click('[data-seg="contrast"] button:nth-child(1)'); await pg.wait_for_timeout(200)

        # --- mobile sheet ---
        await pg.set_viewport_size({'width':390,'height':780}); await pg.wait_for_timeout(700)
        check('sheet renders on mobile', await pg.locator('#grip').is_visible())
        y0=await pg.evaluate("()=>document.getElementById('panel').style.getPropertyValue('--sheet-y')")
        gb=await pg.locator('#grip').bounding_box()
        await pg.mouse.move(gb['x']+195, gb['y']+8); await pg.mouse.down()
        await pg.mouse.move(gb['x']+195, gb['y']+320, steps=10); await pg.mouse.up(); await pg.wait_for_timeout(600)
        y1=await pg.evaluate("()=>document.getElementById('panel').style.getPropertyValue('--sheet-y')")
        check('dragging the sheet down collapses it to peek', y1=='84%', f'{y0} -> {y1}')
        gb=await pg.locator('#grip').bounding_box()   # the grip has moved with the sheet
        await pg.mouse.move(gb['x']+195, gb['y']+8); await pg.mouse.down()
        await pg.mouse.move(gb['x']+195, gb['y']-320, steps=10); await pg.mouse.up(); await pg.wait_for_timeout(600)
        y2=await pg.evaluate("()=>document.getElementById('panel').style.getPropertyValue('--sheet-y')")
        check('dragging it up expands it', y2!=y1, f'{y1} -> {y2}')
        mapvis=await pg.evaluate("()=>{const m=document.getElementById('mapwrap').getBoundingClientRect();return m.height>200;}")
        check('map still has room on mobile', mapvis)

        # --- no horizontal scroll at phone width ---
        await pg.wait_for_timeout(300)
        sw=await pg.evaluate("()=>document.documentElement.scrollWidth"); cw=await pg.evaluate("()=>document.documentElement.clientWidth")
        check('no horizontal scroll at 390px', sw<=cw, f'{sw} vs {cw}')
        await pg.fill('#search','imru'); await pg.wait_for_timeout(350)
        box=await pg.evaluate("()=>{const b=document.getElementById('sg').getBoundingClientRect();return [b.left,b.right];}")
        check('suggestion list stays on screen at 390px', box[1]<=392, box)

        check('no runtime errors', not errs, errs[:4])
        await b.close()
asyncio.run(main())
print()
print('FAILURES:', FAILS if FAILS else 'none')
sys.exit(1 if FAILS else 0)
