import asyncio, json, os, sys
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

# --- the data: an epic only points at things that exist, has its Arabic, and is sourced on both sides ---
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','data')
D=json.load(open(os.path.join(ROOT,'arabia.json'),encoding='utf-8'))
AR=json.load(open(os.path.join(ROOT,'arabia.ar.json'),encoding='utf-8'))
EV={e['id']:e for e in D['events']}; PP={p['id'] for p in D['people']}; TR={t['id'] for t in D['tribes']}
for x in D.get('epics',[]):
    bad=[m['eventId'] for m in x['members'] if m['eventId'] not in EV]+[i for i in x.get('peopleIds',[]) if i not in PP]+[i for i in x.get('tribeIds',[]) if i not in TR]
    ck(f'{x["id"]}: every member, figure and tribe exists', not bad, bad)
    ck(f'{x["id"]}: roles are prelude, core or aftermath', all(m.get('role','core') in ('prelude','core','aftermath') for m in x['members']))
    a=AR.get('epics',{}).get(x['id'],{})
    ck(f'{x["id"]}: Arabic name, summary, date note and dispute', all(a.get(k) for k in ('name','summary','dateNote','dispute')), sorted(a))
    langs={s['lang'] for s in x.get('sources',[])}
    ck(f'{x["id"]}: sourced in both English and Arabic', {'en','ar'}<=langs, langs)
    if x.get('folk'):
        fl={s['lang'] for s in x['folk'].get('sources',[])}
        ck(f'{x["id"]}: the popular-epic layer has its own sources in both languages', {'en','ar'}<=fl, fl)
        ck(f'{x["id"]}: and its Arabic', bool(a.get('folk')))
basus=next((x for x in D.get('epics',[]) if x['id']=='basus-war'),None)
ck('the War of al-Basūs is an epic', basus is not None)
CORE=[m['eventId'] for m in basus['members'] if m.get('role','core')=='core'] if basus else []

STATE="""()=>({year:+document.getElementById('yearNum').textContent, h3:document.querySelector('#pbody h3')?.textContent||null,
  tab:document.querySelector('.ptabs button[aria-selected="true"]')?.dataset.tab, ticks:document.querySelectorAll('#density .ft').length,
  pill:document.getElementById('focuspill').hidden?null:document.getElementById('focuspill').textContent})"""

async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch()
        pg=await b.new_page(viewport={'width':1280,'height':860})
        e=[]; pg.on('pageerror',lambda x:e.append(str(x)))
        async def load(params):
            await pg.goto(BASE+params); await pg.wait_for_timeout(1300); return await pg.evaluate(STATE)
        async def settle(): await pg.wait_for_timeout(450)

        # --- the Epics tab lists it, and opening it filters everything to it ---
        await load('?lang=en&year=600')
        await pg.click('[data-tab="epics"]'); await pg.wait_for_timeout(300)
        n=await pg.locator('#pbody .ev[data-epic]').count()
        ck('the Epics tab lists the epics', n==len(D['epics']), n)
        await pg.locator('#pbody .ev[data-epic="basus-war"]').click(); await pg.wait_for_timeout(700)
        s=await pg.evaluate(STATE)
        ck('opening an epic shows it', s['h3']=='The War of al-Basūs', s)
        ck('opening it from a year with none of its events lands on its first core event', s['year']==min(EV[i]['year'] for i in CORE), s)
        ck('the timeline marks every one of its events', s['ticks']==len(basus['members']), s)
        ck('the map pill names the filter', s['pill'] and 'al-Basūs' in s['pill'], s)
        r=await pg.evaluate("()=>{const t=[...document.querySelectorAll('#density .ft')];const f=[...document.querySelectorAll('#density .fr')];return [t.length,f.length]}")
        ck('each event is drawn as its full range as well as a tick', r[0]==r[1], r)
        order=await pg.evaluate("()=>[...document.querySelectorAll('#pbody .ev[data-ev]')].map(x=>x.dataset.ev)")
        ck('the epic lists its events, prelude first, then in order', order and order[0]=='khazaz-day' and set(order)=={m['eventId'] for m in basus['members']}, order)
        folk=await pg.evaluate("()=>document.querySelector('#pbody .disp.folk')?.textContent||''")
        ck('the popular-epic layer is shown apart, and says so', 'not the akhbār' in folk and 'Tubbaʿ' in folk, folk[:80])
        await settle(); u=q(pg.url)
        ck('the URL holds the epic, with no filter parameter while it is the default', u.get('epic')=='basus-war' and 'filter' not in u, pg.url)

        # --- the filter narrows the lists, and says so there too ---
        await pg.click('[data-tab="events"]'); await pg.wait_for_timeout(400)
        ids=await pg.evaluate("()=>[...document.querySelectorAll('#pbody .ev[data-ev]')].map(x=>x.dataset.ev)")
        ck('the Events list keeps only the epic\'s events', ids and all(i in {m['eventId'] for m in basus['members']} for i in ids), ids)
        bar=await pg.evaluate("()=>document.querySelector('#pbody .fbar')?.textContent||''")
        ck('the list announces the filter', 'al-Basūs' in bar, bar)
        await settle(); u=q(pg.url)
        ck('the URL keeps the filter once the epic is closed', u.get('filter')=='epic:basus-war', pg.url)
        await pg.click('#pbody .fbar [data-filter="off"]'); await pg.wait_for_timeout(400)
        s=await pg.evaluate(STATE)
        ck('the list\'s Clear button removes the filter', s['ticks']==0, s)

        # --- an event says what it is part of ---
        await load('?lang=en&event=basus-waridat')
        part=await pg.evaluate("()=>[...document.querySelectorAll('#pbody .chip[data-epic]')].map(c=>c.textContent)")
        ck('an event in an epic says it is part of it', part==['The War of al-Basūs'], part)
        await pg.click('#pbody [data-filter="epic:basus-war"]'); await pg.wait_for_timeout(400)
        s=await pg.evaluate(STATE)
        ck('and can filter to it without leaving the event', s['ticks']==len(basus['members']) and s['h3']=='Yawm Wāridāt', s)
        await pg.click('#pbody [data-filter="epic:basus-war"]'); await pg.wait_for_timeout(400)
        ck('pressing it again turns the filter off', (await pg.evaluate(STATE))['ticks']==0)
        other=await load('?lang=en&event=imru-death')
        ck('an event in no epic shows no "part of"', await pg.locator('#pbody .chip[data-epic]').count()==0)

        # --- a figure can filter the same way ---
        await load('?lang=en&person=al-muhalhil')
        mine=[x['id'] for x in D['events'] if 'al-muhalhil' in (x.get('peopleIds') or [])]
        await pg.click('#pbody [data-filter="person:al-muhalhil"]'); await pg.wait_for_timeout(400)
        s=await pg.evaluate(STATE)
        ck('a figure filters the timeline to their own events', s['ticks']==len(mine), (s,len(mine)))
        ck('a figure in an epic links to it', await pg.locator('#pbody .chip[data-epic="basus-war"]').count()==1)
        await settle(); u=q(pg.url)
        ck('the figure filter is in the URL', u.get('filter')=='person:al-muhalhil', pg.url)
        await pg.click('#focuspill'); await pg.wait_for_timeout(300)
        ck('the map pill clears the filter', (await pg.evaluate(STATE))['ticks']==0)

        # --- links restore it ---
        s=await load('?lang=en&epic=basus-war&filter=none')
        ck('?epic=…&filter=none opens the epic unfiltered', s['h3']=='The War of al-Basūs' and s['ticks']==0, s)
        s=await load('?lang=en&tab=events&filter=person:kulayb')
        ck('?filter=person:… restores a figure filter', s['ticks']==len([x for x in D['events'] if 'kulayb' in (x.get('peopleIds') or [])]) and s['pill'], s)
        s=await load('?lang=en&filter=epic:nothing')
        ck('an unknown filter is ignored', s['ticks']==0 and s['pill'] is None, s)
        ck('no errors', not e, e)
        await pg.close()

        # --- on a phone, both languages ---
        OVER="""()=>{const r=s=>{const b=document.querySelector(s)?.getBoundingClientRect();return b&&b.width?b:null};
          const hit=(a,b)=>a&&b&&!(a.right<=b.left||b.right<=a.left||a.bottom<=b.top||b.bottom<=a.top);
          const p=r('#focuspill'); return ['#scalebar .bar','#scaletxt','#zoomlvl','#zin','#zout','#zfit'].filter(s=>hit(p,r(s)));}"""
        for lang,name in [('ar','حرب البسوس'),('en','The War of al-Basūs')]:
            ph=await b.new_page(viewport={'width':390,'height':844},has_touch=True,is_mobile=True)
            pe=[]; ph.on('pageerror',lambda x:pe.append(str(x)))
            await ph.goto(BASE+f'?lang={lang}&epic=basus-war'); await ph.wait_for_timeout(1400)
            s=await ph.evaluate(STATE)
            ck(f'phone/{lang}: the epic opens with its ticks on the timeline', s['h3']==name and s['ticks']==len(basus['members']), s)
            ck(f'phone/{lang}: the filter pill overlaps nothing', not await ph.evaluate(OVER), await ph.evaluate(OVER))
            sw=await ph.evaluate("()=>[document.documentElement.scrollWidth,document.documentElement.clientWidth]")
            ck(f'phone/{lang}: no horizontal scroll', sw[0]<=sw[1], sw)
            peek=await ph.evaluate("()=>document.getElementById('peekText').textContent")
            ck(f'phone/{lang}: the sheet peek counts only the epic\'s events', peek and ('1' in peek), peek)
            ck(f'phone/{lang}: no errors', not pe, pe)
            await ph.close()
        await b.close()
    print('\nFAILURES:', F or 'none'); sys.exit(1 if F else 0)
asyncio.run(main())
