import asyncio,os,sys
from playwright.async_api import async_playwright
SKEL='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light}body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style></head><body>@@BODY@@</body></html>'
open('_wrap.html','w',encoding='utf-8').write(SKEL.replace('@@BODY@@',open('atlas.html',encoding='utf-8').read()))
F=[]
def ck(n,c,d=''):
    print(('PASS  ' if c else 'FAIL  ')+n+(('  → '+str(d)) if d and not c else ''))
    if not c: F.append(n)
VIEW="()=>{const m=document.getElementById('root').getAttribute('transform').match(/translate\\(([-\\d.]+) ([-\\d.]+)\\) scale\\(([\\d.]+)\\)/);return {tx:+m[1],ty:+m[2],s:+m[3]};}"
TOUCH = """([type,id,x,y])=>{
  const el = type==='pointerdown' ? document.elementFromPoint(x,y) : window;
  const ev = new PointerEvent(type,{pointerId:id,pointerType:'touch',isPrimary:id===1,
    clientX:x,clientY:y,bubbles:true,cancelable:true,buttons:type==='pointerup'?0:1});
  (el||window).dispatchEvent(ev);}"""
async def seq(pg,steps):
    for st_ in steps:
        await pg.evaluate(TOUCH,st_); await pg.wait_for_timeout(22)

async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch()
        pg=await b.new_page(viewport={'width':412,'height':915},has_touch=True,is_mobile=True)
        e=[];pg.on('pageerror',lambda x:e.append(str(x)))
        await pg.goto('file://'+os.path.abspath('_wrap.html')); await pg.wait_for_timeout(1800)

        # ---- two-finger pan: fingers move together, distance constant ----
        await pg.click('#zfit'); await pg.wait_for_timeout(500)
        v0=await pg.evaluate(VIEW)
        steps=[['pointerdown',1,150,300],['pointerdown',2,250,300]]
        for i in range(1,11):
            steps.append(['pointermove',1,150+i*8,300+i*5])
            steps.append(['pointermove',2,250+i*8,300+i*5])
        steps += [['pointerup',1,230,350],['pointerup',2,330,350]]
        await seq(pg,steps); await pg.wait_for_timeout(400)
        v1=await pg.evaluate(VIEW)
        ck('two-finger drag pans', abs(v1['tx']-v0['tx'])>50 and abs(v1['ty']-v0['ty'])>30,
           f"d=({v1['tx']-v0['tx']:.0f},{v1['ty']-v0['ty']:.0f})")
        ck('two-finger drag does NOT zoom', abs(v1['s']-v0['s'])/v0['s']<0.03,
           f"{v0['s']:.3f} → {v1['s']:.3f}")

        # ---- pinch out: fingers separate ----
        await pg.click('#zfit'); await pg.wait_for_timeout(500)
        v0=await pg.evaluate(VIEW)
        steps=[['pointerdown',1,180,400],['pointerdown',2,230,400]]
        for i in range(1,13):
            steps.append(['pointermove',1,180-i*7,400])
            steps.append(['pointermove',2,230+i*7,400])
        steps += [['pointerup',1,96,400],['pointerup',2,314,400]]
        await seq(pg,steps); await pg.wait_for_timeout(400)
        v1=await pg.evaluate(VIEW)
        ck('pinch out zooms in', v1['s']>v0['s']*1.8, f"{v0['s']:.2f} → {v1['s']:.2f}")

        # ---- pinch in ----
        v0=await pg.evaluate(VIEW)
        steps=[['pointerdown',1,100,400],['pointerdown',2,312,400]]
        for i in range(1,13):
            steps.append(['pointermove',1,100+i*7,400])
            steps.append(['pointermove',2,312-i*7,400])
        steps += [['pointerup',1,184,400],['pointerup',2,228,400]]
        await seq(pg,steps); await pg.wait_for_timeout(400)
        v1=await pg.evaluate(VIEW)
        ck('pinch in zooms out', v1['s']<v0['s']*0.7, f"{v0['s']:.2f} → {v1['s']:.2f}")

        # ---- one finger pans ----
        await pg.click('#zfit'); await pg.wait_for_timeout(500)
        v0=await pg.evaluate(VIEW)
        steps=[['pointerdown',1,200,420]]
        for i in range(1,11): steps.append(['pointermove',1,200-i*9,420-i*4])
        steps.append(['pointerup',1,110,380])
        await seq(pg,steps); await pg.wait_for_timeout(400)
        v1=await pg.evaluate(VIEW)
        ck('one finger pans', abs(v1['tx']-v0['tx'])>40, f"dx={v1['tx']-v0['tx']:.0f}")
        ck('one finger does not zoom', abs(v1['s']-v0['s'])<1e-6, f"{v0['s']:.3f} → {v1['s']:.3f}")

        # ---- lifting one finger of two keeps panning, no jump ----
        await pg.click('#zfit'); await pg.wait_for_timeout(500)
        steps=[['pointerdown',1,150,400],['pointerdown',2,260,400],
               ['pointermove',1,160,410],['pointermove',2,270,410],['pointerup',2,270,410]]
        await seq(pg,steps)
        before=await pg.evaluate(VIEW)
        await seq(pg,[['pointermove',1,180,430],['pointerup',1,180,430]])
        await pg.wait_for_timeout(350)
        after=await pg.evaluate(VIEW)
        jump=abs((after['tx']-before['tx'])-20)+abs((after['ty']-before['ty'])-20)
        ck('lifting a finger does not jump the map', jump<14, f'jump {jump:.1f}px')

        # ---- a tap still opens a marker ----
        await pg.click('#zfit'); await pg.wait_for_timeout(500)
        await pg.click('[data-tab="all"]'); await pg.wait_for_timeout(400)
        pt=await pg.evaluate("""()=>{const L=document.querySelector('.L-places');
          for(const g of L.children){const c=g.querySelector('circle');
            const p=document.getElementById('map').createSVGPoint();
            p.x=+c.getAttribute('cx'); p.y=+c.getAttribute('cy');
            const q=p.matrixTransform(document.getElementById('root').getScreenCTM());
            const h=document.elementFromPoint(q.x,q.y);
            if(h&&h.closest('.L-places')) return {x:q.x,y:q.y};}
          return null;}""")
        await seq(pg,[['pointerdown',1,pt['x'],pt['y']],['pointerup',1,pt['x'],pt['y']]])
        await pg.mouse.click(pt['x'],pt['y']); await pg.wait_for_timeout(700)
        ck('a tap still opens a marker',
           await pg.evaluate("()=>document.querySelector('.ptabs button[aria-selected=\"true\"]').dataset.tab")=='places')

        # ---- a touch drag that starts on a marker pans and does not open it ----
        await pg.click('[data-tab="all"]'); await pg.wait_for_timeout(400)
        v0=await pg.evaluate(VIEW)
        steps=[['pointerdown',1,pt['x'],pt['y']]]
        for i in range(1,11): steps.append(['pointermove',1,pt['x']+i*10,pt['y']+i*6])
        steps.append(['pointerup',1,pt['x']+100,pt['y']+60])
        await seq(pg,steps); await pg.wait_for_timeout(400)
        v1=await pg.evaluate(VIEW)
        ck('dragging from a marker by touch pans', abs(v1['tx']-v0['tx'])>40, f"dx={v1['tx']-v0['tx']:.0f}")
        ck('...and does not open it',
           await pg.evaluate("()=>document.querySelector('.ptabs button[aria-selected=\"true\"]').dataset.tab")=='all')
        ck('no errors', not e, e[:3])
        await b.close()
asyncio.run(main())
print(); print('FAILURES:', F or 'none')
sys.exit(1 if F else 0)
