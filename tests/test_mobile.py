import asyncio,os,sys
from playwright.async_api import async_playwright
SKEL='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light}body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style></head><body>@@BODY@@</body></html>'
open('_wrap.html','w',encoding='utf-8').write(SKEL.replace('@@BODY@@',open('atlas.html',encoding='utf-8').read()))
F=[]
def ck(n,c,d=''):
    print(('PASS  ' if c else 'FAIL  ')+n+(('  → '+str(d)) if d and not c else ''))
    if not c: F.append(n)

DEVICES=[('Android 412x915',412,915),('iPhone 390x844',390,844),('small 360x740',360,740)]

async def run(pw,name,w,h,scheme,lang):
    b=await pw.chromium.launch()
    pg=await b.new_page(viewport={'width':w,'height':h},has_touch=True,is_mobile=True,color_scheme=scheme)
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto('file://'+os.path.abspath('_wrap.html')+'?lang='+lang); await pg.wait_for_timeout(1700)
    tag=f'[{name} {scheme} {lang}] '
    for tab in ['events','people','places','tribes']:
        await pg.click(f'[data-tab="{tab}"]'); await pg.wait_for_timeout(500)
        box=await pg.evaluate("""()=>{const p=document.getElementById('focuspill');
          if(p.hidden) return null; const b=p.getBoundingClientRect();
          const sh=document.getElementById('panel').getBoundingClientRect();
          const mc=document.querySelector('.mapctl').getBoundingClientRect();
          const sb=document.getElementById('scalebar').getBoundingClientRect();
          return {l:b.left,r:b.right,t:b.top,bo:b.bottom,w:b.width,sheetTop:sh.top,
                  ctlLeft:mc.left,sbTop:sb.top,sbBottom:sb.bottom,vw:innerWidth};}""")
        ck(tag+tab+': pill exists', box is not None)
        if not box: continue
        ck(tag+tab+': pill fully on screen', box['l']>=0 and box['r']<=box['vw']+0.5, box)
        ck(tag+tab+': pill clear of the sheet', box['bo']<=box['sheetTop']+0.5, box)
        ck(tag+tab+': pill clear of zoom buttons', box['r']<=box['ctlLeft']+0.5, box)
        ck(tag+tab+': pill clear of scale bar', box['bo']<=box['sbTop']+0.5, box)
        n=await pg.evaluate("()=>document.querySelectorAll('.L-places > g, .L-events > g, .L-people > g, .L-tribes > g').length")
        ck(tag+tab+': something is drawn', n>0, n)
    sw=await pg.evaluate("()=>document.documentElement.scrollWidth")
    ck(tag+'no horizontal scroll', sw<=w, f'{sw} vs {w}')
    ck(tag+'no errors', not errs, errs[:2])
    if name.startswith('Android') and scheme=='dark' and lang=='en':
        await pg.screenshot(path='m_fixed.png')
    await b.close()

async def main():
    async with async_playwright() as pw:
        for n,w,h in DEVICES:
            for sc in ['dark','light']:
                for lang in ['ar','en']:   # the panel flips to RTL in Arabic; the overlays must still clear each other
                    await run(pw,n,w,h,sc,lang)
asyncio.run(main())
print(); print('FAILURES:', F if F else 'none')
sys.exit(1 if F else 0)
