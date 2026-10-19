# Tests

Browser tests against the built `index.html`, using Playwright and headless
Chromium. They test behaviour, not appearance — most of the bugs this project
hit were things that looked fine in a screenshot.

## Running them

```bash
pip install playwright
python3 -m playwright install chromium

python3 src/build.py build/atlas.html   # the tests read ./atlas.html
cd build && for t in ../tests/test_*.py; do python3 -I "$t"; done
```

Each file wraps `atlas.html` in the same minimal page skeleton the artifact
host provides, writes it to `_wrap.html`, and drives that. They expect to be
run from a directory containing `atlas.html`. Every file prints PASS/FAIL per
assertion and a final `FAILURES:` line, and exits non-zero if anything failed.

Google Fonts won't load in a sandbox; the resulting console error is ignored.

## What each file covers

**test_core.py** — search autocomplete (ranking, Arabic queries, keyboard
navigation), the detail panels and their cross-links, the evidence and date
flags, the zoom detail tiers, theme cycling, the Tribes tab, and the phone
layout's lack of horizontal scroll.

**test_mobile.py** — overlay geometry across three phone sizes, in both colour
schemes and both languages. For each filter tab it asserts the focus pill is fully on screen,
above the sheet, clear of the zoom buttons and clear of the scale bar. Written
after a pill rendered off-screen behind the bottom sheet: `is_visible()` passes
for an element that is visible in the wrong place, so these assert positions.

**test_clicks.py** — clicking a marker opens its own tab and detail, on desktop
and phone, and dragging from a marker pans the map *without* opening it.
Written after pointer capture on `pointerdown` silently retargeted every marker
click to the `<svg>`.

**test_zoom.py** — selection and camera. The tribe-card path end to end, the
filter surviving a selection, a hidden layer being forced visible, both zoom
limits relative to the home framing, the point under the cursor staying put
through a wheel zoom, pinch stepping, and the redraw debounce.

**test_touch.py** — synthetic touch pointers. Two-finger drag pans *and* does
not zoom, pinch in and out, one finger pans, lifting one of two fingers doesn't
jump the map, a tap still opens a marker, and a touch drag starting on a marker
pans without opening it. Written after two-finger pan turned out to compute
only a distance ratio, which is 1 when fingers move together — so it jittered
the zoom and never panned.

**test_sources.py** — the `sources` schema and its panel section. Every record
in every collection has a list, no record keeps the old `source` field, every
source has a title and a link or a printed work. In the panel: the section has
its own heading with a count, the address is visible as text, a printed work
is not drawn as a link, notes show, and a record with none says so.

**test_epics.py** — the `epics` data (every member, figure and tribe exists;
Arabic present; sources in both languages, folk layer included) and the
feature: the Epics tab, opening an epic (lands on its first event, ticks on the
timeline for every member with its range, the folk layer shown apart), the
filter narrowing and announcing itself on the lists, an event's "part of" and
its filter toggle, a figure's filter, the pill and Clear, URL restore with
`filter=none` and `filter=person:…`, and the phone in both languages.

**test_url.py** — the view in the address bar, and the reading settings.
Arabic by default; `?lang`, `?year`, and each record kind open what they name,
on the right year and tab; bad parameters fall back; the URL follows the
slider, tabs, records and language, and reloading it reproduces the view; a
language saved by an older version does not override the default, a chosen
one is remembered and a link does not overwrite it; other parameters survive.
Every reading setting applies, survives a reload and resets. On a phone, in
both languages, the largest text has no sideways scroll, the pill overlaps
nothing and the map keeps its room.

**test_arabic.py** — the Arabic interface, desktop and phone. Walks every tab
and a detail card of each kind and fails on any visible text that is Latin with
no Arabic in it, apart from the transliterated second name, the evidence codes
and anything marked `lang="ar-Latn"`. Also checks the scale bar, zoom readout
and sheet peek switch language at once, map names follow the Arabic label
setting, and search rows name their kind in Arabic. Written after a pass in
Arabic found the Legend, Display and every detail card still in English.

On Windows, run each file as `python -X utf8 -I` — `-I` ignores
`PYTHONIOENCODING`, and the default console codepage can't print the results.

## Known gaps

No test covers the timeline density bars or the Legend tab's contents. Path
notes on a figure's "where they were" list (`people[].path[].what`) have no
Arabic in the data yet and still show in English. The three selection bugs
recorded at the end of `../data/NOTES.md` have reproduction steps but no test
yet.
