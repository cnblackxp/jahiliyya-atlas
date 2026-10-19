# Known issues

Open bugs with reproduction steps, newest first. Write a failing test before
fixing anything here — all three below share one root cause and a single rule
fixes them, so a test for each is what proves it.

## 1. A selected record can be invisible on the map

**One rule covers all three cases: whatever is selected is always drawn — past
the layer toggles, past the evidence and category filters, past the year
window — and selecting something always lands on a year where it exists.**

Selection already overrides the *layer* toggles (`layerOn()` in
`src/template.html` lets the selected id through). It does not override the
filters in `visibleEvents()`, nor the year window, nor the absence of a path
step. So the panel opens a full record while the map shows nothing.

### 1a. A filter excludes it

1. Display tab → untick **EPI** under "Show events by evidence".
2. Search `namara`, press Enter.
3. Panel shows the Namāra inscription in full. Map draws **zero** event markers.

Same for any unticked category. Confirmed in a browser.

### 1b. The event is before 300 CE

Five events sit outside `meta.range`, reachable by search but not by the
slider: `nabataea-annexed` (106), `hira-palmyrene-garrison` (132),
`thamud-temple-ruwafa` (167), `zenobia-marid` (269), `himyar-conquers-saba`
(285). Selecting one clamps the year to 300, the ±window excludes it, and no
marker can ever appear.

Search `palmyrene` → year clamps to 300, zero markers.

### 1c. A figure has no attested position at the landing year

`reveal()` jumps to a person's **birth** year. For most figures the first
`path` step is decades later, so nothing is drawn and `moveTo()` finds nothing
to fly to, leaving the camera where it was.

Search `imru`, pick Imruʾ al-Qays. Year lands on 496; his first attested
position is Najd in 525. The People tab filters the map to figures, and nobody
in the dataset is placed in 496 — so the whole map goes blank beside a full
biography.

Birth is the right landing year for a *birth event*, not for a biography. Land
on the first year the figure is locatable; fall back to birth only when they
are never placed; and when a selected person has no position at the current
year, say so in the panel rather than leaving an empty map to be interpreted.

## 2. Figure movement is thin, and interpolating it would lie

Pins already jump between `path` steps as the year changes, but only 41 of 106
people have a path and only **27 have two or more steps**, so the motion is
rarely visible.

Densifying it is cheap and well-sourced: a figure named in an event that has a
place was, by that event's own claim, there that year. 23 more people have two
or more placed events but no real path. Mark such points as derived rather than
stated.

Do **not** interpolate smoothly between steps. For Imruʾ al-Qays the research
says plainly that no itinerary is transmitted and the six-step path is the
report's own reconstruction; sliding a pin along it would present a modern
guess as a record. Snap between attested positions, draw the trail for the
selected figure only, show the connecting segments as inferred, and fade a pin
whose last known position is long behind the current year — "we lost track of
him" should not look like "he stayed".

## 3. Sourcing is thin — schema ready, data still to come

**Done (2026-10-19):** every record in every collection now has a `sources`
list (schema in `data/REVISION.md` §6.1), the panel shows it as its own
section, all 82 links were audited, and the eleven events whose link was dead,
off-topic or only a contents page were re-sourced (§6.2).

**To do — the data:**

- [ ] **Extend the Imruʾ al-Qays pattern to every event** (`REVISION.md` §6.4):
  three or more sources per event, at least one English and one Arabic, each
  read, with a note wherever a source dates or places it differently. Arabic
  classical works on Shamela or Wikisource (al-Kāmil, al-ʿIqd, Ibn Kathīr)
  beside a modern reference on each side.
- [ ] **Kitāb al-Aghānī** for the Imruʾ al-Qays events — the main classical
  source for all five, not yet found online in a citable form.
- [ ] **Sources for people, places, tribes and powers.** All 256 have an empty
  list; the panel says "No source recorded … yet". Start with the figures whose
  dates carry a `lifeNote`, and places with `coordConfidence: exact`.
- [ ] **More than one source per event.** 156 of 172 still have one. Split by
  what each backs (`supports`): the date, the place and the account often come
  from different works.
- [ ] **Fill `supports`** on the 160 migrated sources, which have none yet.
- [ ] **Deep-link the inscriptions** (priority 3 in AGENTS.md): CIH 540/541,
  Ry 506, Murayghān, ẒM 1, the Ḥimà texts → DASI; Namāra, Jabal Usays,
  Ḥarrān → OCIANA or the published edition, alongside the current links.
- [ ] **Read the three unread links** by hand: Iranica *Ḥīra*
  (`hira-bishop-410`, `hira-surrenders`) and academia.edu (`satih-prophecy`).
- [ ] **Settle al-Ḥīra in 132** (`REVISION.md` §6.3): no source found carries
  the year or the garrison; both Wikipedias say 32 CE.
- [ ] **Replace container pages** where a direct one exists: 33 URLs serve 123
  events, *Muhammad* alone 11.
- [ ] **Archive copies** (`archive`) for anything that could vanish — one
  Wikipedia page already did.

**Why it mattered:** before this, 116 of 172 sources were Wikipedia, every
event had exactly one source, and many pointed at a container rather than a
claim — the 449 dam breach cites the "Marib
Dam" article rather than the inscription that dates it. The strongest evidence
in the atlas (CIH 541, Ry 506, Ja 1028) links to Wikipedia instead of to the
DASI or OCIANA record with its photograph and facsimile.

The date, the location and the narrative of a single event often come from
different places, which is what the `supports` field is for.

This is what let bug #4 happen.

## 4. FIXED — compound events share one source field

`hijra` carried both the Hijra and Heraclius leaving Constantinople, with a
single `source` pointing at the Byzantine–Sasanian war article. The link was
right for the half you weren't reading. Split into `hijra` (TRAD) and
`heraclius-counteroffensive` (EXT) on 2026-10-19, each with its own source.

Worth auditing for other compound entries.
