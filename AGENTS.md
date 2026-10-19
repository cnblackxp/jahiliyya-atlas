# Working on the Jāhiliyya Atlas

Context for an AI agent picking this project up. Read this before touching
anything. If you only read one section, read **The one rule that matters**.

---

## What this is

An interactive map and timeline of pre-Islamic Arabia, roughly 300–640 CE. A
year slider drives a map of the peninsula and its neighbours: spheres of
influence rise and fall, settlements appear and are abandoned, battlefields
surface while their events are in view, and a side panel shows what happened.
It is bilingual, English and Arabic, with the Arabic written from the Arabic
sources rather than translated.

It is one self-contained HTML file, `index.html`, built by a Python script from
four geography files and two or three data files. No bundler, no npm, no
runtime dependencies beyond a Google Fonts stylesheet.

## Why it exists

It began as research scaffolding for a visual novel set in the period — a man
and his wife travelling the Arabian deserts, meeting the real and legendary
figures of the Jāhiliyya. The research that produced it established something
that reframed the project: **no interactive map-plus-timeline for pre-Islamic
Arabia exists, and no machine-readable chronology of the period exists in any
repository.** That absence is why this is worth maintaining.

The owner reads Arabic natively and English fluently. The richest sources for
this period are Arabic and untranslated — al-Aghānī in 24 volumes, Jawād ʿAlī's
al-Mufaṣṣal in 20 — while the polished digital tools are English and mostly
cover other centuries. The Arabic side of this project is the underserved one.

## The one rule that matters

**This atlas is an argument about how much we actually know, and every feature
must preserve that.**

Almost every date in the interior of Arabia is a back-calculation, not a
record. Shiʿb Jabala is dated across sixty years by different scholars. The
*Encyclopaedia Iranica* declines to print a Lakhmid king-list at all. Of 172
events, 25 are fixed by a dated inscription and 126 carry a recorded scholarly
dispute.

So the data carries its own uncertainty, and the interface shows it:

- **`evidence`** — `EPI` (inscription-fixed), `EXT` (Greek, Syriac, Latin or
  Persian source), `TRAD` (later Arabic-Islamic tradition), `RECON` (modern
  reconstruction).
- **`dateCertainty`** — `fixed`, `approximate`, `contested`, `legendary`.
- **`estimated`** — true when the year is a convention or a midpoint rather
  than a transmitted date. The interface renders those as *c. 570* / *نحو ٥٧٠*.
- **`dateRange`** — the full spread the sources allow. Must not be collapsed to
  `[year, year]` for anything not genuinely fixed.
- **`dateNote`** — what the date actually rests on, in one sentence.
- **`dispute`** — where scholars disagree, with names and competing figures.
- **`coordConfidence`** — `exact`, `approximate`, `guessed`. 47 of 111 places
  are guesses; the *ayyām* name a well or a hill and nothing more. The map
  draws a dashed ring for a guess and a faint ring for an approximation.

**Never launder uncertainty into confidence.** Do not collapse a range, drop a
dispute, interpolate a position between two attested points, or present a
reconstruction as a record. If a feature would require inventing precision,
that is a reason not to build the feature in that form. Several decisions in
the codebase exist only for this reason — markers nudged apart for legibility
keep a hairline leader back to their true position, because the pin is a label
and the line end is the claim.

The inverse also holds: do not invent doubt to look humble. An
inscription-dated event keeps its single year and `estimated: false`.

## Handling sensitive material

The atlas covers the life of the Prophet Muhammad and the religions of the
period. The discipline that keeps this accurate is the same one that keeps it
respectful: **report, don't assert.** Say which tradition carries a report —
Ibn Isḥāq via Ibn Hishām, al-Ṭabarī, al-Wāqidī — and keep sīra, ḥadīth and
modern reconstruction visibly distinct. Prophetic material is graded `TRAD`
like everything else from the later Arabic tradition, and only the death in 632
is graded `fixed`. Write in the same plain register as every other entry, with
no devotional or polemical language in either direction.

Note the chain this creates: the traditional birth is pegged to the Year of the
Elephant, which this atlas itself dates across 552–572, so the birth inherits
that whole spread. Age-reckoned events inherit it too; Hijra-reckoned ones do
not, because the Hijra is an epoch rather than a derived number.

## Layout

```
index.html              built output, committed so GitHub Pages serves it
src/
  template.html         the whole page — CSS, markup, map logic. ~1,800 lines
  build.py              inlines JSON into the template → index.html
  geo/
    make_basemap.py     clips Natural Earth land/rivers/lakes to the region
    make_terrain.py     hand-authored deserts, ranges, region and sea names
    land.json rivers.json lakes.json terrain.json
data/
  arabia.json           the chronology — the file to edit
  arabia.ar.json        Arabic content, keyed by the same ids
  ui.ar.json            Arabic interface strings
  NOTES.md              guessed coordinates, undated events, adjudicated conflicts
  REVISION.md           the dates/Muhammad revision log
  REVISION.ar.md        the Arabic-sources correction log
research/
  report.md             the English research report
  report.ar.md          the Arabic report, written from Arabic sources
  notes/                eight source-by-source research files
tests/                  Playwright browser tests — see tests/README.md
KNOWN_ISSUES.md         open bugs with reproduction steps
```

## Build and test

```bash
python3 src/build.py                    # → index.html
python3 src/build.py build/atlas.html   # for the tests
cd build && for t in ../tests/test_*.py; do python3 -I "$t"; done
```

Regenerating the basemap is optional and needs `shapely`. The committed geo
JSON is the output of those two scripts.

**Always run all six test files before publishing.** They exist because this
project kept shipping bugs that looked fine in a screenshot: a focus pill
rendered off-screen behind the bottom sheet, pointer capture silently killing
every marker click, two-finger pan computing a distance ratio that is 1 when
fingers move together. Each of those produced a test file. Add to them.

## Data model

Five collections in `arabia.json`: `places`, `events`, `people`, `polities`,
`tribes`. Ids are stable and referenced across files — **never rename or delete
one.** `arabia.ar.json` is a parallel map from the same ids to Arabic fields
only; if you add a record, add its Arabic too.

Things that are easy to get wrong:

- `dateRange` is the uncertainty about the event. `endYear` is when a span
  ended. For a reign, `endYear` can legitimately exceed `dateRange[1]`.
- `zones[].centers[].r` is a radius in **kilometres of soft influence**, not a
  border. These powers had reach and clients, not boundaries, and the map draws
  them as soft blobs on purpose.
- Tribe-to-event links are **derived at runtime** by matching names in event
  text and each figure's stated tribe. There is no tribe field on events. The
  interface labels these as a reading aid rather than a claim in the sources;
  keep that label.
- Region names, desert outlines and mountain ranges in `terrain.json` are hand
  placed on a modern outline, not surveyed.
- Coastlines are modern. The head of the Gulf and the Tihāma shore both sat
  differently in late antiquity.

## Interface conventions

- The map draws filled pictographic glyphs at constant screen size, following
  Maki's conventions — 15px grid, solid paths, no outlines, because outlines
  mush at marker size. The same glyph set is used on the map, in search results
  and in the panel.
- Detail is tiered by zoom: anchors only when far out, then cities, then
  shape-coded symbols, then every label. A small map pane raises every
  threshold.
- Content tabs filter the map to their own kind; All, Legend and Display leave
  it alone. A pill on the map names the active filter and clears it.
- Touch and mouse have **separate** handlers. One finger pans; two fingers pan
  and zoom together about their midpoint. Mouse drag pans, with pointer capture
  deferred until movement so a click stays a click. Do not merge these paths.
- The timeline runs left to right in both languages. Arabic flips the panel to
  RTL but never the time axis.
- Every colour is a token with light and dark values. There is a high-contrast
  mode, four interface text sizes, and a separate map-label size.

## Priorities if you are picking up work

1. The three selection bugs in `KNOWN_ISSUES.md`. One rule fixes all three.
   Write the failing tests first.
2. The citation schema change, also in `KNOWN_ISSUES.md` — one URL per event is
   the weakest part of the project, and nearly every credibility improvement
   depends on fixing it first.
3. Deep-link the inscriptions to DASI and OCIANA records. Biggest credibility
   win per hour: the strongest evidence currently cites Wikipedia.
4. Depth over reach. 172 events across 340 years is thin. Resist extending the
   date range.

## How to behave here

Propose, don't silently rewrite. This dataset encodes a lot of careful
adjudication between conflicting sources, recorded in `REVISION.md` and
`REVISION.ar.md`. If you change a date, a grade or a dispute note, log what you
changed and why in the same style.

When the sources conflict, record the conflict. Do not pick a winner quietly.
Several of the most valuable entries in this atlas exist because the Arabic and
English scholarship disagree and both readings are preserved.
