# Jāhiliyya Atlas

An interactive map and timeline of pre-Islamic Arabia, roughly 300–640 CE.

Drag the year slider and the map redraws: spheres of influence rise and fall,
settlements appear and are abandoned, battlefields surface while their events
are in view, and the side panel lists what happened that year. It was built as
research scaffolding for a visual novel set in the period, and it is meant to
be honest about how little of this chronology is actually fixed.

To publish it: push this repo, then in **Settings → Pages** set the source to
the `main` branch, root folder. `index.html` is already built and committed, so
the atlas goes live at `https://<your-username>.github.io/jahiliyya-atlas/`
with nothing else to configure. Put that link here.

---

## What makes it different from a pretty map

Almost every date in the Arabian interior is a back-calculation, not a record.
Shiʿb Jabala is dated across a fifty-year spread by five different scholars.
*Encyclopaedia Iranica* declines to print a Lakhmid king-list at all. The only
one of the great *ayyām* that can be tied to an externally dated battle is Yawm
Ḥalīma in June 554.

So the atlas grades everything it shows.

**Evidence grade** on every event:

| Tag | Meaning | Count |
|---|---|---|
| `EPI` | Fixed by a dated inscription | 25 |
| `EXT` | From a Greek, Syriac, Latin or Persian source | 40 |
| `TRAD` | From the later Arabic-Islamic tradition | 104 |
| `RECON` | A modern scholarly reconstruction | 3 |

**Date certainty**: `fixed` · `approximate` · `contested` · `legendary`.
Contested events carry the full proposed range, and 126 of the 172 events carry
a recorded scholarly dispute, shown on the card rather than smoothed away. An
`estimated` year renders as *c. 570* — a convention or a midpoint, not a
transmitted date — with a note saying what the date actually rests on.

**Coordinate confidence**: a solid dot means the site is identified, a faint
ring means approximate, a dashed ring means a guess. 47 of the 111 places are
guesses — the *ayyām* name a well or a hill and nothing more. Markers nudged
apart so they don't overlap keep a hairline leader back to their true position:
the pin is a label, the line end is the claim.

Spheres of influence are soft blobs on purpose. These powers had reach and
clients, not borders.

## Using it

| Action | How |
|---|---|
| Pan | Drag, or arrow keys with the map focused |
| Zoom | Scroll, pinch, `+` / `−`, double-click (shift to zoom out) |
| Reset view | `0`, or the ⤢ button |
| Move the year | Drag the slider, or ← / → anywhere else (shift for decades) |
| Jump to the next dated event | The ◀ ▶ buttons beside Play |
| Find something | The search box autocompletes people, places, events, tribes and powers, in Latin or Arabic |
| Switch language | The **ع** button — interface, content and map labels |
| Filter the map | Pick a content tab; a pill shows the filter and clears it |

The **Display** tab has interface text size, a separate map-label size, a
high-contrast mode, a scroll-wheel mode (auto / pan / zoom), a toggle for the
pulsing markers, a Latin / العربية / both switch for map labels, and checkboxes
for every layer. Settings persist in `localStorage`.

On a phone the map runs full-bleed under a bottom sheet that drags between
peek, half and full. One finger pans, two fingers pan and zoom together, pinch
zooms. On a trackpad a two-finger drag pans and pinch zooms; a mouse wheel
zooms.

**Arabic.** The ع button switches the whole interface to Arabic: the panel goes
RTL, the map labels switch script, and the event prose, blurbs and dispute
notes come from `data/arabia.ar.json`, written from the Arabic sources rather
than translated. The timeline stays left-to-right in both languages.

## Layout

```
index.html              the built atlas, self-contained, open it directly
AGENTS.md               context for anyone (human or AI) picking the project up
KNOWN_ISSUES.md         open bugs with reproduction steps
src/
  template.html         the page: CSS, markup, and all the map logic
  build.py              inlines the JSON into the template → index.html
  geo/
    make_basemap.py     clips Natural Earth land/rivers/lakes to the region
    make_terrain.py     hand-authored deserts, ranges, region and sea names
    land.json rivers.json lakes.json terrain.json
data/
  arabia.json           the chronology: events, places, people, polities, tribes
  arabia.ar.json        Arabic content, keyed by the same ids
  ui.ar.json            Arabic interface strings
  NOTES.md              guessed coordinates, undated events, adjudicated conflicts
  REVISION.md           log of the dates and prophetic-material revision
  REVISION.ar.md        log of the corrections from the Arabic sources
research/
  report.md             the English research report
  report.ar.md          the Arabic report, written from the Arabic sources
  notes/                the eight source-by-source research files behind it
tests/                  Playwright browser tests — see tests/README.md
```

## Building

```bash
python3 src/build.py
```

That is the whole build. No bundler, no dependencies, no package.json — it
reads the geography and the data and writes one HTML file. The two Arabic files
are optional; without them the page still builds and the language button has
nothing to switch to.

To run the tests:

```bash
pip install playwright && python3 -m playwright install chromium
python3 src/build.py build/atlas.html
cd build && for t in ../tests/test_*.py; do python3 -I "$t"; done
```

Regenerating the basemap is optional and needs `shapely`:

```bash
pip install shapely
python3 src/geo/make_basemap.py   # downloads Natural Earth, clips, simplifies
python3 src/geo/make_terrain.py   # rewrites the hand-authored layers
python3 src/build.py
```

## Editing the chronology

`data/arabia.json` is the only file you need to touch to change what the atlas
shows. Five collections:

```jsonc
{
  "places":   [{ "id", "name", "ar", "lat", "lon", "kind", "from", "to",
                 "blurb", "coordConfidence" }],
  "events":   [{ "id", "year", "title", "ar", "evidence", "dateCertainty",
                 "dateRange", "placeId", "category", "summary", "dispute",
                 "peopleIds", "politiesIds", "source" }],
  "people":   [{ "id", "name", "ar", "role", "birth", "death", "lifeCertainty",
                 "lifeNote", "tribe", "blurb",
                 "path": [{ "year", "placeId", "what" }] }],
  "polities": [{ "id", "name", "ar", "from", "to", "kind", "capitalId", "blurb",
                 "zones": [{ "from", "to",
                             "centers": [{ "lat", "lon", "r" }] }] }],
  "tribes":   [{ "id", "name", "ar", "lat", "lon", "r", "blurb" }]
}
```

`r` is a radius in kilometres of soft influence, not a boundary. `path` entries
move a figure across the map as the year advances; leave the array empty rather
than inventing a journey. Events also carry `estimated`, `dateNote` and an
optional `endYear`. Ids are referenced from `arabia.ar.json`, so never rename
one. Run `python3 src/build.py` after editing.

Before changing anything, read `AGENTS.md` — it explains the evidence grading
and why several apparently odd choices in the code exist.

## Known limits

- **Coastlines are modern.** The head of the Gulf and the Tihāma shore both sat
  differently in late antiquity.
- **Region names are placed, not surveyed.** نجد، تهامة، الحجاز، اليمامة، الدهناء
  and the rest sit where they read well on a modern outline.
- **Desert and mountain shapes are hand-drawn** approximations, not data.
- The projection is equirectangular with a standard parallel at 25°N, which is
  fine for this latitude band and wrong further out.
- Three events sit outside 300–640 on purpose (the Nabataean annexation of 106,
  the Ruwāfa Thamūd temple of 167, Zenobia in 269). They are reachable through
  search and the "All" window, not the slider.

## Sources and licence

Code and the hand-authored layers: **MIT**, see `LICENSE`.

The chronology in `data/arabia.json` and the text in `research/` are compiled
from published scholarship and from the Arabic sources; each event carries a
`source` URL where one exists. `data/NOTES.md` and `research/notes/` record what
could not be verified. Treat the dataset as a research aid with its uncertainty
flags attached, not as an authority.

Coastlines, rivers and lakes derive from
[Natural Earth](https://www.naturalearthdata.com/) 1:50m, which is in the public
domain. See `ATTRIBUTION.md`.

Fonts are loaded from Google Fonts: Amiri (Arabic and Latin), IBM Plex Sans,
IBM Plex Mono — all under the SIL Open Font License.
