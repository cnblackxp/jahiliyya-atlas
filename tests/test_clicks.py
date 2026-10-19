import asyncio,os,sys
from playwright.async_api import async_playwright
SKEL='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light}body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style></head><body>@@BODY@@</body></html>'
open('_wrap.html','w',encoding='utf-8').write(SKEL.replace('@@BODY@@',open('atlas.html',encoding='utf-8').read()))
F=[]
def ck(n,c,d=''):
    print(('PASS  ' if c else 'FAIL  ')+n+(('  → '+str(d)) if d and not c else ''))
    if not c: F.append(n)
# pick the first marker in this layer whose centre is not covered by another marker
CTR = """(sel)=>{const L=document.querySelector(sel);
  for(const g of L.children){
    const c=g.querySelector('circle');
    const p=document.getElementById('map').createSVGPoint();
    p.x=+c.getAttribute('cx'); p.y=+c.getAttribute('cy');
    const q=p.matrixTransform(document.getElementById('root').getScreenCTM());
    const hit=document.elementFromPoint(q.x,q.y);
    if(hit && hit.closest(sel)) return {x:q.x,y:q.y};
  }
  return null;}"""
async def run(pw,w,h,mobile):
    b=await pw.chromium.launch()
    pg=await b.new_page(viewport={'width':w,'height':h},has_touch=mobile,is_mobile=mobile)
    e=[]; pg.on('pageerror',lambda x:e.append(str(x)))
    await pg.goto('file://'+os.path.abspath('_wrap.html')+'?lang=en'); await pg.wait_for_timeout(1700)
    tag=f'[{w}x{h}] '
    await pg.click('[data-tab="tribes"]'); await pg.wait_for_timeout(400)
    for lay,tab in [('.L-places','places'),('.L-events','events'),('.L-people','people'),('.L-tribes','tribes')]:
        await pg.click('[data-tab="all"]'); await pg.wait_for_timeout(400)
        pt=await pg.evaluate(CTR,lay)
        if not pt: ck(tag+tab+': marker present',False); continue
        await pg.mouse.click(pt['x'],pt['y']); await pg.wait_for_timeout(650)
        act=await pg.evaluate("()=>document.querySelector('.ptabs button[aria-selected=\"true\"]').dataset.tab")
        ck(tag+'click a marker → '+tab+' tab', act==tab, act)
        body=(await pg.inner_text('#pbody')).strip()
        ck(tag+tab+': detail opened', body.startswith('←') or body.startswith('→'), body[:40])
        if mobile:
            sy=await pg.evaluate("()=>document.getElementById('panel').style.getPropertyValue('--sheet-y')")
            ck(tag+tab+': sheet rose to show it', sy!='84%', sy)
    # a drag must still pan and must not open anything
    await pg.click('[data-tab="all"]'); await pg.wait_for_timeout(350)
    before=await pg.evaluate("()=>document.getElementById('root').getAttribute('transform')")
    pt=await pg.evaluate(CTR,'.L-places')
    await pg.mouse.move(pt['x'],pt['y']); await pg.mouse.down()
    await pg.mouse.move(pt['x']+120,pt['y']+70,steps=10); await pg.mouse.up()
    await pg.wait_for_timeout(500)
    after=await pg.evaluate("()=>document.getElementById('root').getAttribute('transform')")
    ck(tag+'dragging from a marker pans the map', before!=after)
    act=await pg.evaluate("()=>document.querySelector('.ptabs button[aria-selected=\"true\"]').dataset.tab")
    ck(tag+'dragging does not open the marker', act=='all', act)
    ck(tag+'no errors', not e, e[:2])
    await b.close()
async def main():
    async with async_playwright() as pw:
        await run(pw,1180,840,False)
        await run(pw,412,915,True)
asyncio.run(main())
print(); print('FAILURES:', F or 'none')
sys.exit(1 if F else 0)
