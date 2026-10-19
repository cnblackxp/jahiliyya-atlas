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

**test_mobile.py** — overlay geometry across three phone sizes in both colour
schemes. For each filter tab it asserts the focus pill is fully on screen,
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

## Known gaps

No test covers the Arabic content rendering beyond the interface strings, the
timeline density bars, or the Legend tab's contents. The three selection bugs
recorded at the end of `../data/NOTES.md` have reproduction steps but no test
yet.
