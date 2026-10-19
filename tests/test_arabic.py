import asyncio, os, sys
from playwright.async_api import async_playwright
sys.stdout.reconfigure(encoding='utf-8')
SKEL='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light}body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style></head><body>@@BODY@@</body></html>'
open('_wrap.html','w',encoding='utf-8').write(SKEL.replace('@@BODY@@',open('atlas.html',encoding='utf-8').read()))
F=[]
def ck(n,c,d=''):
    print(('PASS  ' if c else 'FAIL  ')+n+(('  → '+str(d)) if d and not c else ''))
    if not c: F.append(n)

# Visible text in Arabic mode that is Latin words with no Arabic in it.
# Allowed on purpose: the transliterated second name (.ar .arbig .arx), the
# evidence codes (.tag), the EN button, and path notes, which have no Arabic in
# the data yet (.where). A transliteration set inside Arabic text is marked
# lang="ar-Latn". A source's own title and address (.src-t, .src-u) are quoted
# as published, in whatever language that is.
LEAKS="""(root)=>{const out=[];const R=document.querySelector(root);if(!R)return out;
const w=document.createTreeWalker(R,NodeFilter.SHOW_TEXT);let n;
while(n=w.nextNode()){const t=n.textContent.trim();
  if(!/[A-Za-z]{2,}/.test(t)||/[\\u0600-\\u06FF]/.test(t))continue;
  const el=n.parentElement;if(!el||el.closest('script,style,.ar,.arbig,.arx,.tag,.where,#langBtn,[lang="ar-Latn"],.src-t,.src-u'))continue;
  const r=el.getBoundingClientRect(),cs=getComputedStyle(el);
  if(!r.width||!r.height||cs.visibility==='hidden'||cs.display==='none'||el.closest('[hidden]'))continue;
  out.push(t.slice(0,60));}
return [...new Set(out)];}"""

async def sweep(pg,label):
    leaks={}
    async def grab(where,root='body'):
        l=await pg.evaluate(LEAKS,root)
        if l: leaks[where]=l
    await grab('all')
    for tab,item in [('events','#pbody .ev[data-ev]'),('people','#pbody .lf[data-person]'),
                     ('places','#pbody [data-place]'),('tribes','#pbody .ev[data-tribe]'),('epics','#pbody .ev[data-epic]'),
                     ('legend',None),('display',None)]:
        await pg.click(f'[data-tab="{tab}"]'); await pg.wait_for_timeout(400)
        await grab(tab)
        if item and await pg.locator(item).count():
            await pg.locator(item).first.click(); await pg.wait_for_timeout(500)
            await grab(tab+' detail','#panel')
            # opening an epic filters to it and moves to its year; undo both so the rest of the sweep starts where it did
            await pg.evaluate("""()=>{const b=document.querySelector('#pbody [data-filter][aria-pressed="true"]');if(b)b.click();
              const r=document.getElementById('range');r.value=554;r.dispatchEvent(new Event('input',{bubbles:true}));}""")
            await pg.wait_for_timeout(200)
    # a power's detail, reached from an event that names one
    await pg.click('[data-tab="events"]'); await pg.wait_for_timeout(300)
    await pg.locator('#pbody .ev[data-ev]').first.click(); await pg.wait_for_timeout(400)
    if await pg.locator('#pbody [data-polity]').count():
        await pg.locator('#pbody [data-polity]').first.click(); await pg.wait_for_timeout(400)
        await grab('power detail','#panel')
    ck(f'{label}: no English-only text in the Arabic interface', not leaks, leaks)

async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch()
        pg=await b.new_page(viewport={'width':1280,'height':860})
        e=[]; pg.on('pageerror',lambda x:e.append(str(x)))
        await pg.goto('file://'+os.path.abspath('_wrap.html')+'?lang=en'); await pg.wait_for_timeout(1500)
        await pg.click('#langBtn'); await pg.wait_for_timeout(500)

        # readouts that were only refreshed on the next pan or zoom
        sc=await pg.inner_text('#scaletxt'); zl=await pg.inner_text('#zoomlvl')
        ck('scale bar switches to Arabic with the language', 'كم' in sc, sc)
        ck('zoom readout switches to Arabic with the language', not any(w in zl for w in ['anchors','cities','towns','shrines','everything']), zl)

        await sweep(pg,'desktop')

        # map names: with Arabic labels, nothing that has an Arabic name stays Latin
        await pg.click('#zfit'); await pg.wait_for_timeout(300)
        for _ in range(3): await pg.click('#zin'); await pg.wait_for_timeout(80)
        await pg.wait_for_timeout(500)
        lat=await pg.evaluate("""()=>[...document.querySelectorAll('#map text.lbl-ridge,#map text.lbl-sea,#map text.lbl-region')]
          .map(t=>t.textContent).filter(s=>!/[\\u0600-\\u06FF]/.test(s))""")
        ck('ridge, sea and region names are Arabic when labels are Arabic', not lat, lat)

        # search rows name their kind in Arabic
        await pg.fill('#search','مكة'); await pg.wait_for_timeout(400)
        sg=await pg.evaluate(LEAKS,'#sg')
        ck('search suggestions carry no English-only labels', not sg, sg)
        sub=await pg.evaluate("()=>[...document.querySelectorAll('#sg .nm span')].map(s=>s.textContent).join(' | ')")
        ck('search suggestion kinds are Arabic', not any(w in sub for w in ['city','capital','shrine',' CE','events']), sub)
        await pg.keyboard.press('Escape')

        # tooltip on a place marker
        at=await pg.evaluate("""()=>{const m=document.getElementById('map').getBoundingClientRect();
          for(const g of document.querySelectorAll('.L-places > g')){const r=g.getBoundingClientRect();
            const x=r.x+r.width/2,y=r.y+r.height/2;
            if(r.width&&x>m.left+40&&x<m.right-40&&y>m.top+40&&y<m.bottom-40)return [x,y];}return null;}""")
        ck('a place marker is on screen to hover', at)
        if at:
            await pg.mouse.move(at[0],at[1]); await pg.wait_for_timeout(300)
            tp=await pg.evaluate(LEAKS,'#tip')
            ck('map tooltip carries no English-only labels', not tp, tp)

        # back to English leaves no Arabic chrome behind
        await pg.click('#langBtn'); await pg.wait_for_timeout(400)
        sc=await pg.inner_text('#scaletxt')
        ck('scale bar switches back to English', 'km' in sc, sc)
        ck('no errors', not e, e)
        await pg.close()

        # the built file on its own, from a plain server that names no charset:
        # the page has to declare UTF-8 itself or Arabic falls back to windows-1252
        import http.server, threading, functools
        srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(
            type('Q',(http.server.SimpleHTTPRequestHandler,),{'log_message':lambda *a:None}),directory=os.getcwd()))
        threading.Thread(target=srv.serve_forever,daemon=True).start()
        raw=await b.new_page()
        await raw.goto(f'http://127.0.0.1:{srv.server_address[1]}/atlas.html'); await raw.wait_for_timeout(800)
        cs=await raw.evaluate("()=>[document.characterSet,document.title]")
        ck('the bare file declares UTF-8 itself', cs[0]=='UTF-8' and cs[1]=='Jāhiliyya Atlas', cs)
        # and its own viewport, or a phone lays it out at 980px and never sees the phone layout
        vw=await raw.evaluate("()=>document.querySelector('meta[name=viewport]')?.content||''")
        ck('the bare file declares a device-width viewport', 'width=device-width' in vw, vw)
        await raw.close(); srv.shutdown()

        ph=await b.new_page(viewport={'width':390,'height':844})
        await ph.goto('file://'+os.path.abspath('_wrap.html')+'?lang=en'); await ph.wait_for_timeout(1500)
        await ph.click('#langBtn'); await ph.wait_for_timeout(500)
        pk=await ph.inner_text('#peekText')
        ck('phone sheet peek is Arabic', not any(w in pk for w in ['event','drag','nothing']), pk)
        await sweep(ph,'phone')
        await b.close()
    print('\nFAILURES:', F or 'none'); sys.exit(1 if F else 0)
asyncio.run(main())
