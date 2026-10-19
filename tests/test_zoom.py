import asyncio,os,sys
from playwright.async_api import async_playwright
SKEL='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light}body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style></head><body>@@BODY@@</body></html>'
open('_wrap.html','w',encoding='utf-8').write(SKEL.replace('@@BODY@@',open('atlas.html',encoding='utf-8').read()))
F=[]
def ck(n,c,d=''):
    print(('PASS  ' if c else 'FAIL  ')+n+(('  → '+str(d)) if d and not c else ''))
    if not c: F.append(n)
VIEW="()=>{const t=document.getElementById('root').getAttribute('transform');const m=t.match(/translate\\(([-\\d.]+) ([-\\d.]+)\\) scale\\(([\\d.]+)\\)/);return {tx:+m[1],ty:+m[2],s:+m[3]};}"
async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch(); pg=await b.new_page(viewport={'width':1180,'height':840})
        e=[];pg.on('pageerror',lambda x:e.append(str(x)))
        await pg.goto('file://'+os.path.abspath('_wrap.html')+'?lang=en'); await pg.wait_for_timeout(1700)
        home=(await pg.evaluate(VIEW))['s']

        # --- the reported bug: tribe card ---
        await pg.click('[data-tab="tribes"]'); await pg.wait_for_timeout(500)
        await pg.click('#pbody .ev[data-tribe]'); await pg.wait_for_timeout(900)
        v=await pg.evaluate(VIEW)
        ck('tribe card zooms the map in', v['s']>home*1.1, f"home {home:.2f} → {v['s']:.2f}")
        shown=await pg.evaluate("()=>document.querySelectorAll('.L-tribes > g').length")
        ck('tribe card draws tribes on the map', shown>0, shown)
        ck('tribe stays on the Tribes tab',
           await pg.evaluate("()=>document.querySelector('.ptabs button[aria-selected=\"true\"]').dataset.tab")=='tribes')
        other=await pg.evaluate("()=>document.querySelectorAll('.L-places > g, .L-events > g').length")
        ck('the filter still holds — no places or events leak back', other<=1, other)
        ck('the selected tribe is ringed',
           await pg.evaluate("()=>[...document.querySelectorAll('.L-tribes circle')].some(c=>(c.getAttribute('stroke')||'').includes('--accent'))"))

        # --- layer forced on even when unticked ---
        await pg.click('[data-tab="display"]'); await pg.wait_for_timeout(400)
        await pg.uncheck('#layer-people'); await pg.wait_for_timeout(300)
        await pg.click('[data-tab="people"]'); await pg.wait_for_timeout(400)
        await pg.click('#pbody .lf'); await pg.wait_for_timeout(800)
        ck('selecting a hidden figure still shows it',
           await pg.evaluate("()=>document.querySelectorAll('.L-people > g').length")>0)
        await pg.click('[data-tab="display"]'); await pg.wait_for_timeout(300)
        await pg.check('#layer-people'); await pg.wait_for_timeout(300)

        # --- zoom limits are relative to the home framing ---
        await pg.click('#zfit'); await pg.wait_for_timeout(400)
        # re-read: a web font arriving after load can resize the map pane and so the home framing
        home=(await pg.evaluate(VIEW))['s']
        for _ in range(14): await pg.click('#zout'); await pg.wait_for_timeout(60)
        await pg.wait_for_timeout(300); lo=(await pg.evaluate(VIEW))['s']
        ck('cannot zoom out past the whole region', lo>=home*0.69, f'{lo:.2f} vs home {home:.2f}')
        for _ in range(26): await pg.click('#zin'); await pg.wait_for_timeout(45)
        await pg.wait_for_timeout(300); hi=(await pg.evaluate(VIEW))['s']
        ck('zoom in stops at a sane limit', hi<=home*22.1, f'{hi:.2f}')
        ck('zoom in actually went deep', hi>home*8, f'{hi:.2f}')

        # --- wheel zoom keeps the point under the cursor ---
        await pg.click('#zfit'); await pg.wait_for_timeout(400)
        under=await pg.evaluate("""()=>{const r=document.getElementById('map').getBoundingClientRect();
          const p=document.getElementById('map').createSVGPoint(); p.x=400; p.y=400;
          const q=p.matrixTransform(document.getElementById('root').getScreenCTM().inverse());
          return {lx:q.x,ly:q.y};}""")
        for _ in range(6):
            await pg.mouse.move(400,400)
            await pg.evaluate("()=>document.getElementById('map').dispatchEvent(new WheelEvent('wheel',{deltaY:-120,deltaMode:0,bubbles:true,cancelable:true,clientX:400,clientY:400}))")
            await pg.wait_for_timeout(60)
        await pg.wait_for_timeout(350)
        after=await pg.evaluate("""()=>{const p=document.getElementById('map').createSVGPoint(); p.x=400; p.y=400;
          const q=p.matrixTransform(document.getElementById('root').getScreenCTM().inverse());
          return {lx:q.x,ly:q.y};}""")
        drift=((under['lx']-after['lx'])**2+(under['ly']-after['ly'])**2)**0.5
        ck('wheel zoom holds the point under the cursor', drift<1.0, f'drift {drift:.3f} world units')

        # --- trackpad pinch anchors too ---
        await pg.click('#zfit'); await pg.wait_for_timeout(400)
        s0=(await pg.evaluate(VIEW))['s']
        for _ in range(8):
            await pg.evaluate("()=>document.getElementById('map').dispatchEvent(new WheelEvent('wheel',{deltaY:-18,ctrlKey:true,deltaMode:0,bubbles:true,cancelable:true,clientX:500,clientY:420}))")
            await pg.wait_for_timeout(40)
        await pg.wait_for_timeout(350)
        s1=(await pg.evaluate(VIEW))['s']
        ck('pinch zooms smoothly in steps', s1>s0*1.5 and s1<s0*6, f'{s0:.2f} → {s1:.2f}')

        # --- redraw is debounced, not per-tick ---
        calls=await pg.evaluate("""async ()=>{let n=0; const L=document.querySelector('.L-places');
          const ob=new MutationObserver(()=>n++); ob.observe(L,{childList:true});
          for(let i=0;i<10;i++){document.getElementById('map').dispatchEvent(
            new WheelEvent('wheel',{deltaY:-100,deltaMode:0,bubbles:true,cancelable:true,clientX:400,clientY:400}));
            await new Promise(r=>setTimeout(r,25));}
          await new Promise(r=>setTimeout(r,400)); ob.disconnect(); return n;}""")
        ck('ten wheel ticks do not trigger ten relayouts', calls<=6, f'{calls} mutation bursts')

        # --- opening a record centres it, and never zooms out from where the reader is ---
        async def open_card():
            await pg.click('[data-tab="events"]'); await pg.wait_for_timeout(300)
            eid=await pg.locator('#pbody .ev[data-ev]').first.get_attribute('data-ev')
            await pg.locator('#pbody .ev[data-ev]').first.click(); await pg.wait_for_timeout(700)
            return eid
        await pg.click('#zfit'); await pg.wait_for_timeout(400)
        for _ in range(7): await pg.click('#zin'); await pg.wait_for_timeout(60)
        await pg.wait_for_timeout(300); deep=(await pg.evaluate(VIEW))['s']
        await open_card(); s=(await pg.evaluate(VIEW))['s']
        ck('opening an event while zoomed in does not zoom out', s>=deep-1e-6, f'{deep:.2f} → {s:.2f}')
        await pg.click('#zfit'); await pg.wait_for_timeout(400)
        await open_card(); s=(await pg.evaluate(VIEW))['s']
        ck('opening an event from the whole map still zooms in to it', s>home*2.5, f'home {home:.2f} → {s:.2f}')
        # the event's place lands in the middle of the visible map
        off=await pg.evaluate("""()=>{const sel=document.querySelector('.L-events circle[stroke="var(--accent)"]');
          if(!sel) return null; const b=sel.getBoundingClientRect(), m=document.getElementById('map').getBoundingClientRect();
          return [Math.abs(b.x+b.width/2-(m.left+m.width/2)), Math.abs(b.y+b.height/2-(m.top+m.height/2))];}""")
        ck('the opened event is centred on the map', off and off[0]<40 and off[1]<40, off)
        ck('no errors', not e, e[:3])
        await b.close()
asyncio.run(main())
print(); print('FAILURES:', F or 'none')
sys.exit(1 if F else 0)
