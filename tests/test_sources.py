import asyncio, json, os, sys
from playwright.async_api import async_playwright
sys.stdout.reconfigure(encoding='utf-8')
SKEL='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light}body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style></head><body>@@BODY@@</body></html>'
open('_wrap.html','w',encoding='utf-8').write(SKEL.replace('@@BODY@@',open('atlas.html',encoding='utf-8').read()))
F=[]
def ck(n,c,d=''):
    print(('PASS  ' if c else 'FAIL  ')+n+(('  → '+str(d)) if d and not c else ''))
    if not c: F.append(n)

# --- the data: every record carries a sources list, and every source can be found again ---
D=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','data','arabia.json'),encoding='utf-8'))
KINDS=('events','people','places','tribes','polities')
missing=[f'{k}/{r["id"]}' for k in KINDS for r in D[k] if not isinstance(r.get('sources'),list)]
ck('every record in every collection has a sources list', not missing, missing[:6])
ck('no record still uses the old single source field', not [r['id'] for k in KINDS for r in D[k] if 'source' in r])
ck('every event has at least one source', not [e['id'] for e in D['events'] if not e['sources']],
   [e['id'] for e in D['events'] if not e['sources']][:6])
FIELDS={'url','title','lang','work','author','volume','page','year','accessed','archive','supports','note','noteAr'}
bad=[]
for k in KINDS:
    for r in D[k]:
        for s in r['sources']:
            if not s.get('title'): bad.append((r['id'],'no title'))
            if not s.get('url') and not s.get('work'): bad.append((r['id'],'neither url nor work'))
            if set(s)-FIELDS: bad.append((r['id'],sorted(set(s)-FIELDS)))
            if s.get('url') and not s['url'].startswith('https://') and not s['url'].startswith('http://'): bad.append((r['id'],'url'))
            if not set(s.get('supports',[]))<={'date','place','people','narrative'}: bad.append((r['id'],s['supports']))
ck('every source has a title and either a link or a printed work, in known fields', not bad, bad[:6])

async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch()
        pg=await b.new_page(viewport={'width':1280,'height':860})
        e=[]; pg.on('pageerror',lambda x:e.append(str(x)))
        await pg.goto('file://'+os.path.abspath('_wrap.html')); await pg.wait_for_timeout(1500)

        # open an event by id through the panel's own click handler, as an event card would
        async def open_event(eid):
            await pg.evaluate("""(id)=>{const o=document.createElement('div');o.className='ev';o.dataset.ev=id;
              document.getElementById('pbody').appendChild(o);o.click();}""",eid)
            await pg.wait_for_timeout(500)

        # an event with one source: its own section, the address readable on the card
        await open_event('dam-breach-449')
        sect=await pg.evaluate("()=>[...document.querySelectorAll('#pbody .sect')].map(s=>s.textContent)")
        ck('an event has a Sources section', any(s.startswith('Sources') for s in sect), sect)
        u=await pg.evaluate("()=>{const a=document.querySelector('#pbody .src .src-u');return a&&[a.textContent,a.href]}")
        ck('the source address is shown as text, not hidden behind a word', u and 'wikipedia.org/wiki/Marib_Dam' in u[0], u)
        t=await pg.evaluate("()=>{const a=document.querySelector('#pbody .src .src-t');return a&&[a.tagName,a.textContent,a.target]}")
        ck('the source title is a link that opens in a new tab', t and t[0]=='A' and t[1]=='Marib Dam' and t[2]=='_blank', t)

        # several sources, a printed work without a link, and a note
        await open_event('barqi-robin-naiit')
        n=await pg.evaluate("()=>document.querySelectorAll('#pbody .src').length")
        ck('an event with two sources shows both', n==2, n)
        sect=await pg.evaluate("()=>[...document.querySelectorAll('#pbody .sect')].map(s=>s.textContent)")
        ck('the section heading carries the count', 'Sources · 2' in sect, sect)
        pr=await pg.evaluate("()=>{const c=[...document.querySelectorAll('#pbody .src')][1];return c&&[c.querySelector('.src-t').tagName,c.textContent]}")
        ck('a printed work with no link is not drawn as a link', pr and pr[0]=='SPAN' and 'Printed work' in pr[1] and 'Semitica et Classica' in pr[1], pr)
        note=await pg.evaluate("()=>document.querySelector('#pbody .src .src-n')?.textContent||''")
        ck('a source note is shown', 'deleted from Wikipedia' in note, note)

        # Arabic Shamela page: volume and page, Arabic title kept as published
        await open_event('dahis-qatan')
        m=await pg.evaluate("()=>document.querySelector('#pbody .src .src-m')?.textContent||''")
        ck('a book source shows work, volume and page', 'al-ʿIqd al-farīd' in m and 'vol. 6' in m and 'p. 25' in m, m)

        # a figure with none says so
        await pg.click('[data-tab="people"]'); await pg.wait_for_timeout(300)
        await pg.locator('#pbody .lf[data-person]').first.click(); await pg.wait_for_timeout(500)
        none=await pg.evaluate("()=>{const s=[...document.querySelectorAll('#pbody .sect')].find(x=>x.textContent.startsWith('Sources'));return s&&s.nextElementSibling&&s.nextElementSibling.textContent}")
        ck('a figure with no source says so instead of showing nothing', none and 'No source recorded for this figure yet' in none, none)

        # in Arabic the section heading and the empty state follow the language
        await pg.click('#langBtn'); await pg.wait_for_timeout(400)
        none=await pg.evaluate("()=>{const s=[...document.querySelectorAll('#pbody .sect')].find(x=>x.textContent.startsWith('المصادر'));return s&&s.nextElementSibling&&s.nextElementSibling.textContent}")
        ck('the Sources section is Arabic in the Arabic interface', none and 'لم يُسجَّل مصدرٌ' in none, none)

        ck('no errors', not e, e)
        await b.close()
    print('\nFAILURES:', F or 'none'); sys.exit(1 if F else 0)
asyncio.run(main())
