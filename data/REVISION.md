# REVISION.md — arabia.json, revision of 2026-10-19

Two jobs, both done in place at `/home/claude/data/arabia.json`. Same schema plus two new
event fields. `meta.range` is still `[300, 640]`. No existing id changed, no existing id
removed, no existing summary, title, `ar`, `year` or `dispute` reworded except `hijra`
(see §1.4). `meta.note` gained a sentence describing the two new fields, and `meta.revised`
was added.

Counts: **154 → 168 events, 96 → 103 people, 108 → 109 places.** Polities and tribes untouched.

---

## 1. Job 1 — the prophetic and Meccan material

### 1.1 People added (7)

None of these were already in the file; I checked all 96 existing ids first.

| id | name | `lifeCertainty` | birth / death |
|---|---|---|---|
| `muhammad` | Muḥammad ibn ʿAbd Allāh | contested | 570 / 632 |
| `khadija` | Khadīja bint Khuwaylid | contested | null / 619 |
| `abu-talib` | Abū Ṭālib ibn ʿAbd al-Muṭṭalib | contested | null / 619 |
| `abd-al-muttalib` | ʿAbd al-Muṭṭalib ibn Hāshim | legendary | null / 578 |
| `abd-allah-ibn-abd-al-muttalib` | ʿAbd Allāh ibn ʿAbd al-Muṭṭalib | legendary | null / 570 |
| `amina-bint-wahb` | Āmina bint Wahb | legendary | null / 577 |
| `al-najashi` | Al-Najāshī, the Negus of Aksum | legendary | null / null |

`muhammad` carries `tribe: "Quraysh, clan of Hāshim"` and a `lifeNote` that separates the two
halves of his chronology explicitly: the death (8 June 632) and the Hijra (622) are the firm
end, because the Hijrī calendar is counted from the second and everything after from the
first; the birth is not, because it rests on a synchronism with the Year of the Elephant,
which this file already dates **552–572**. So the 570 birth is `estimated: true` with a
twenty-year `dateRange`, and the `lifeNote` says which later events inherit that spread
(anything reckoned by his age) and which do not (anything reckoned in years before the Hijra).
It also records the negative finding from the research: no inscriptional, archaeological or
external documentary evidence for Mecca or Quraysh before 632.

`al-najashi` has `lifeCertainty: "legendary"` because the Islamic sources give him a title and
not a matchable name. The `lifeNote` carries the three candidate identifications (Armah from
1895, Ella Tsaham, Hahn's argument that Armah was Kāleb's son under another name) and notes
that the Aksumite coin sequence gives relative order, not absolute dates.

`abd-al-muttalib` is `legendary` rather than `contested` on purpose: the research explicitly
records "no date located for ʿAbd al-Muṭṭalib's floruit", so his 578 is pure arithmetic off a
contested birth. His `blurb` and `lifeNote` mention the Hubal-arrows story and the
hundred-camel ransom as narrative, and note that the hundred-camel blood-price often credited
to him could not be sourced to him specifically — per `daily_life.md`.

`abd-al-muttalib` is `role: "patron"`, as are Abū Ṭālib, ʿAbd Allāh and Āmina — the same role
the file already uses for Theodora and Hind. `khadija` is `role: "merchant"`, the only other
merchant in the file. `muhammad` is `role: "prophet-figure"`, matching `quss` and `musaylima`.

### 1.2 Place added (1)

`hiraa` — Ghār Ḥirāʾ on Jabal al-Nūr, `coordConfidence: "exact"` (the hill is a known
identified site 3 km NE of the Meccan sanctuary). It is the `placeId` for `revelation-begins`
and a stop on `muhammad`'s `path`. The two ʿAqaba pledges use the existing `mina`, since
al-ʿAqaba is described in the sources only as near Minā; the Aksum migrations use the existing
`aksum`, which is exactly the point of including them.

### 1.3 Events added (14)

All fourteen are `TRAD`. Every one has an `estimated` flag, a `dateNote` naming the dating
device, and a `dateRange` that is a real spread except the death.

| id | year | range | certainty | est. | what fixes it |
|---|---|---|---|---|---|
| `muhammad-born` | 570 | 552–572 | contested | yes | inherits the Year of the Elephant's whole spread |
| `abd-allah-dies` | 570 | 552–572 | legendary | yes | "about six months before the birth" |
| `amina-dies` | 577 | 558–578 | legendary | yes | his sixth year |
| `abd-al-muttalib-guardianship` | 577 (endYear 579) | 558–580 | legendary | yes | his sixth to eighth years |
| `muhammad-marries-khadija` | 595 | 577–597 | contested | yes | his twenty-fifth year |
| `kaba-rebuilt-black-stone` | 605 | 595–610 | contested | yes | five years before the revelation, or his 35th year |
| `revelation-begins` | 610 | 608–612 | approximate | yes | twelve years before the Hijra |
| `public-preaching-begins` | 613 | 611–615 | approximate | yes | nine years before the Hijra |
| `aksum-migrations` | 615 (endYear 616) | 613–616 | contested | yes | 7 BH or 9 BH for the first group, 6 BH or 7 BH for the second |
| `hashim-boycott` | 616 (endYear 619) | 615–620 | approximate | yes | roughly 7 BH to 3 BH |
| `year-of-sorrow` | 619 | 619–620 | approximate | yes | three years before the Hijra |
| `aqaba-pledge-first` | 621 | 620–621 | approximate | yes | one year before the Hijra, at a pilgrimage season |
| `aqaba-pledge-second` | 622 | 621–622 | approximate | yes | June 622, months before the move |
| `muhammad-dies` | 632 | 632–632 | **fixed** | **no** | 8 June 632, 11 AH — the one date in his life not reckoned off something else |

Dating decisions worth stating:

- **The birth is not given 570–571.** It gets the Elephant's full 552–572, and its `dispute`
  carries al-Zuhrī's tradition putting the Elephant before ʿAbd Allāh was born — the tradition
  contradicting its own synchronism.
- **Age-reckoned events are widened, Hijra-reckoned events are not.** The marriage (his 25th
  year) gets a twenty-year span, 577–597. The revelation (twelve years before the Hijra) gets
  608–612, because the Hijra is an epoch and not a derived number. This distinction is the main
  structural decision in Job 1 and it is stated in every affected `dateNote` and in
  `muhammad`'s `lifeNote`.
- **The Kaʿba rebuilding** has two competing dating devices (five years before the revelation
  vs. his 35th year). I used the first for `year` and said in the `dateNote` that the second
  would widen it by two decades. The `dispute` carries Marinus of Tyre on quadrangular-stone
  veneration in the 2nd century, against Robin on the Kaʿba's late-6th-century rise and Webb on
  its regional rather than pan-Arabian reach — all from `religion_and_gods.md`.
- **The Aksum migrations are one event with `endYear`**, not two, because Caetani and Watt
  doubted there were two distinct migrations and Watt traced the two canonical lists to later
  disputes over precedence in ʿUmar's registers. Splitting them into two dated events would
  have asserted what the scholarship denies. The `dispute` says so.
- **The boycott is `dateCertainty: "approximate"` with `endYear: 619`**, so it draws as a band,
  per the brief.
- **Only the death is `fixed`.** Its `dispute` notes that the year is as firm as the Arabic
  tradition gets while still being externally unattested.

### 1.4 The existing `hijra` entry

Range and `year` left alone (622 is an epoch, not an estimate). `summary` extended to mention
the ʿAqaba oaths and the September arrival; `dispute` added, saying the year is the epoch the
rest of the Arabic chronology is counted from but is not externally fixed, that the earliest
Greek and Syriac notices of the Arabs begin later, and that the `EXT` grade on the entry
belongs to its Byzantine half (Heraclius's 4 April departure). `peopleIds` now leads with
`muhammad`. **This is the only existing summary or dispute that was changed at all.**

### 1.5 `muhammad` added to existing events

Added to `peopleIds` on seven entries where he is an actor and was silently absent:
`year-of-elephant`, `hijra`, `khansa-converts`, `allat-shrine-demolished`, `durayd-dies`,
`wadd-demolished`, `dhu-al-khalasa-demolished`. Nothing else in those entries touched.

---

## 2. Job 2 — honest ranges

### 2.1 What was already right

The brief expected many legendary and contested events to carry collapsed `[year, year]`
ranges. **They do not.** All 52 `legendary` and all 27 `contested` events already had genuine
spreads; the 45 collapsed ranges in the original file were all `fixed` entries, which is
correct, plus two `approximate` ones. So Job 2 turned into a narrower audit: find the ranges
that were too tight *given the file's own dispute fields*, rather than a bulk uncollapse.

### 2.2 Ranges widened (27)

Every widening is justified by material already in the dataset's own `dispute` field or in the
research notes. No range was widened to look humble, and no inscription-dated event was touched.

| id | was | now | why |
|---|---|---|---|
| `urwa-dies` | 590–610 | **520–600** | Its own dispute says the published figures are 520 and 600. The old range **contained neither.** This was a bug, not a judgement call. |
| `antara-dies` | 595–615 | 568–615 | One tradition kills him in the Dāḥis fighting, which this file spreads from 568; 595 excluded that version while the dispute field asserted it. |
| `satih-prophecy` | 560–580 | 552–628 | Al-Masʿūdī and Ibn Durayd put the Persian omens under Khusraw II (590–628), not Khusraw I, and the eve-of-the-birth placement inherits the Elephant's 552–572. |
| `shib-jabala` | 551–600 | 551–602 | Bosworth places it under al-Nuʿmān III, whose reign runs to 602. The old upper bound clipped one of the five published options the dispute field lists. |
| `rahrahan` | 550–600 | 550–601 | Dated about a year before Shiʿb Jabala, whose upper bound moved. |
| `dhi-najab` | 552–601 | 552–603 | Dated one year after Shiʿb Jabala, whose upper bound moved. |
| `hatim-dies` | 570–580 | 552–580 | A second tradition puts his death in the year of Muḥammad's birth, itself 552–572. |
| `sayf-vassal-king` | 571–575 | 571–578 | His killing is given as 575 **or 578**; the range stopped at 575 while the dispute field said 578. |
| `amr-ibn-hind-accession` | 554–554 | 552–554 | Ry 506 has him acting in 552. One of only two collapsed non-`fixed` ranges in the file. |
| 12 × Dāḥis days | …–595 or …–600 | …–**609** | The only bracket for the war is Muir's c. 568–609; the day-ranges stopped short of their own war. (`dahis-ghadaq`, `malik-ibn-zuhayr-killed`, `dahis-muraqqab`, `dahis-dhu-husa`, `dahis-yamariyya`, `dahis-habaa`, `dahis-faruq`, `dahis-qatan`, `dahis-ghadir-qalha`, `dahis-raqam`, `dahis-araair`, `dahis-dhat-al-jarajir`) |
| 5 × Fijār days | 584–590 | **566–592** | The cycle's only dating device is Muḥammad's reported age of 14 to 20. That age applies to a birth year this file dates 552–572, so the honest span is 552+14 to 572+20. The old 584–590 quietly assumed the 570 birth as fact. (`fijar-trigger`, `fijar-nakhla`, `fijar-shamta`, `fijar-abla`, `fijar-ukaz`) |
| `fijar-hurayra` | 584–591 | 584–592 | Al-Khāqānī's 589 anchors the low end; the age-based reckoning allows the close as late as 592. |

The Fijār widening is the one with real consequences for the interface: it takes the cycle from
a tidy six-year window to a twenty-six-year one, which is what the evidence actually supports
now that the birth year it hangs off is itself a range.

### 2.3 `estimated` (new boolean, on all 168 events)

**96 true, 72 false.** Rule applied: `estimated: false` for every `dateCertainty: "fixed"`
entry, and for seventeen `approximate`/`contested` entries whose `year` is a **transmitted
figure the sources actually give** rather than a convention or midpoint — `aksumite-invasion`
(525 is Procopius's), `najran-massacre` (523 is transmitted; 524 is the separate destruction
date), `ukaz-founded` (542 is one of the article's own two figures), `abraha-dam-repair` (543 is
a source figure clashing with CIH 541's 548), `amr-ibn-hind-accession`, `amr-ibn-hind-killed`,
`imru-death`, `letter-archimandrites`, `sayf-vassal-king`, `hatim-dies` (578 is from *Kitāb
al-Aghānī*), `mundhir-ghassanid-exiled`, `fijar-hurayra` (589 is al-Khāqānī's), `urwa-dies`,
`antara-dies` (608 is the traditional figure), `khansa-muawiya`, `alexandria-falls`,
`allat-shrine-demolished`, `quraysh-split-605`.

Everything else is `estimated: true`, including every `legendary` event and `muhammad-born`.
An interface rendering `estimated: true` as "c. 570" and `false` as "570" will read correctly
throughout. **Note that this makes `estimated` orthogonal to `dateCertainty`, deliberately:
`antara-dies` is contested *and* a transmitted figure; `quraysh-split-605` is a bare
transmitted 605 with nothing to check it against.**

### 2.4 `dateNote` (new field, on all 168 events)

One sentence per event on what the date rests on. **148 non-null, 20 null.** The nulls are
the straightforwardly fixed entries that need no gloss: `hira-bishop-410`, `kinda-federates-502`,
`mundhir-iii-raids-503`, `himyar-expels-lakhmids-najd`, `simeon-letter`, `thannuris`,
`callinicum`, `perpetual-peace`, `theodora-jacob`, `fifty-year-peace`,
`harith-ibn-jabala-dies`, `justin-assassination-plot`, `ghassanids-sack-hira`,
`ghassanid-phylarchate-broken`, `peace-591`, `numan-deposed`, `jerusalem-falls`,
`ganzaka-624`, `nineveh`, `badhan-ends`.

The notes are typed. Recurring forms:
- inscription-dated: "Fixed by the Bostran era date cut on the stone: 7 Kaslūl, year 223."
- Hijra-counted: "Counted back from the Hijra, which is the one fixed point the Arabic
  tradition really has." (`buath`)
- sequence-placement: "Undated; the year holds the day's place in the sequence, nothing more."
  (all the Basūs and Dāḥis days)
- reign-window: "Undated; the window is simply al-Mundhir III's reign." (`awara-i`)
- bare midpoint: "No source gives a date, a place or a narrative; 500 is a bare midpoint of the
  period." (`al-nisar-day`)
- age-reckoned: the Fijār and the Meccan events, which say so explicitly.

### 2.5 `endYear` added (10, bringing the file to 13 with a span)

Where the span is the event:

| id | year → endYear | what the band is |
|---|---|---|
| `basus-war-begins` | 494 → 534 | the whole forty-year Basūs war, the corpus's only date for it |
| `dahis-race` | 568 → 609 | the whole Dāḥis war, i.e. Muir's bracket |
| `hashim-boycott` | 616 → 619 | *(new event)* the three-year boycott |
| `aksum-migrations` | 615 → 616 | *(new event)* the two reported waves |
| `abd-al-muttalib-guardianship` | 577 → 579 | *(new event)* the two-year guardianship |
| `dam-breach-449` | 449 → 450 | the two consecutive breaches the entry describes |
| `najran-massacre` | 523 → 524 | killings in 523, destruction of the town in 524 |
| `aksumite-invasion` | 525 → 530 | the conquest as a campaign, not a day |
| `sayf-vassal-king` | 571 → 575 | his rule |
| `numan-shelters-khusraw` | 590 → 591 | the flight and the fighting at al-Nahrawān |
| `harith-made-king` | 529 → 569 | his reign, to his externally dated death |
| `amr-ibn-hind-accession` | 554 → 569 | his reign, to his killing |
| `numan-iii-accession` | 581 → 602 | his reign, to the fixed 602 deposition |

The three reigns carry `endYear` so a UI can draw the reign band while `dateRange` still
expresses the uncertainty in the *accession*. These two fields now mean different things and
a consumer should not conflate them: **`dateRange` is how unsure we are about when it started;
`endYear` is when it stopped.** For `numan-iii-accession` the `endYear` of 602 also silently
resolves the 595-vs-602 reign-end contradiction that NOTES.md §3.11 flags, in favour of the
externally fixed deposition; the `dateNote` says so.

---

## 3. Things in the existing data that looked wrong

1. **`urwa-dies` had a range containing neither of its own published figures.** The dispute
   field reads "Dates given as 520–600 with no apparatus behind either figure", and the
   `dateRange` was `[590, 610]`. Fixed to `[520, 600]`. This is the one straightforward error
   found.
2. **Five Fijār days and `fijar-trigger` were dated as if 570 were a fact.** They are dated
   only by Muḥammad's reported age, and the file's own `year-of-elephant` entry spreads his
   birth across 552–572. The tight 584–590 window silently laundered a contested birth year
   into a firm one — exactly the failure mode Job 2 is about, and it was already in the data
   before any prophetic material was added.
3. **Twelve Dāḥis day-ranges ended before their own war's bracket did.** The war is c. 568–609
   per Muir; the days stopped at 595 or 600.
4. **`sayf-vassal-king` and `shib-jabala` each clipped an option their own dispute field
   asserts** (578 for the first, Bosworth's 582–602 for the second).
5. **`hijra` was graded `EXT` with no `dispute`.** The Hijra itself is not externally attested;
   what is `EXT` is the Heraclius half of the entry. Grade left as-is (it is defensible for a
   compound entry) but a `dispute` added saying which half the grade belongs to.
6. **`musaylima-claims` had `dateCertainty: "approximate"` and a null `dispute`** while its
   range is 615–622 and the only dating device is "before the Hijra". Range left alone, which is
   honest; `dateNote` now says what it rests on.
7. **No entry for Muḥammad in a chronology running to 632**, with `khansa-converts`,
   `wadd-demolished`, `dhu-al-khalasa-demolished`, `durayd-dies` and `allat-shrine-demolished`
   all describing his actions without naming him in `peopleIds`. Fixed.
8. **`adi-embassy` is `evidence: "TRAD"` with `dateCertainty: "fixed"` and a collapsed
   `[579, 579]`** — a court record transmitted by the Arabic tradition with nothing external
   behind it. I left the grading alone (it is not mine to re-grade, and the report does call it
   "a court record") but the `dateNote` now says the year is transmitted and unchecked. Three
   other `TRAD`+`fixed` entries are in the same position: `khansa-converts`, `durayd-dies`,
   `wadd-demolished`, `dhu-al-khalasa-demolished`. Their notes name the Hijrī reckoning behind
   them, which is the honest account.

### Not changed, though arguably wrong

- `quraysh-split-605` keeps its collapsed `[605, 605]`. It is the only non-`fixed` collapsed
  range left in the file. The tradition gives a bare 605 and nothing to widen it *toward*;
  inventing a spread would be the opposite of the brief. It is `estimated: false` with a
  `dateNote` saying the year is transmitted and that Mecca has no dated record before 632 to
  check it against.
- `sasanian-conquest-yemen` keeps `fixed` / `[570, 570]`, though `religion_and_gods.md` has
  "annexed by the Sasanians in 575 or 578". The 570 siege of Ṣanʿāʾ is externally dated and the
  575/578 figures belong to the annexation, which is a different event; the `dateNote` records
  the tension rather than widening the range.
- `abu-amr` (an 8th-century philologist) and the two pre-window events stay outside 300–640 on
  purpose, as NOTES.md §2 and §5 explain.

---

## 4. Verification

```
python3 -c "import json;json.load(open('/home/claude/data/arabia.json'))"   # parses
```

Checked programmatically on the written file:
- every event has `estimated` (bool) and `dateNote` (string or null);
- `dateRange[0] <= year <= dateRange[1]` for all 168;
- `endYear >= year` wherever `endYear` is not null;
- every `placeId`, every id in `peopleIds`, every id in `politiesIds` and every `path[].placeId`
  resolves;
- no duplicate event ids; no original id lost;
- `meta.range == [300, 640]`;
- events sorted by `year` with the original relative order preserved among equal years (stable
  sort), so the fourteen new events slot in chronologically without disturbing the existing
  sequence.

## 5. One note for NOTES.md

NOTES.md §5 says "**`year` is always the single best central estimate** and is always inside
`dateRange`" — still true. It should now also say that `estimated` tells you whether `year` is
a transmitted figure or a convention, that `dateNote` says what it rests on, and that
`dateRange` and `endYear` answer different questions (uncertainty about the start vs. the end
of a span). The §2 statement that 52 events are `legendary` and 27 `contested` is now 55 and
31, and 107 of 154 events carrying a non-null `dispute` is now 122 of 168.

---

## 6. Sources — audit, schema change and eleven re-sourced events (later on 2026-10-19)

No date, grade, range, dispute, title or summary changed in this pass. Only where each record
points for its evidence changed.

### 6.1 Schema

`events[].source` (one URL string) is gone. **Every record in all five collections now has a
`sources` list**: events carry what they had, and people, places, tribes and powers carry an
empty list until they are sourced. Each entry is an object:

| field | meaning |
|---|---|
| `url` | the link, or `null` for a printed work with no online copy |
| `title` | the page or chapter title as published, in its own language |
| `lang` | `en` / `ar` — the language of the source, not of the record |
| `work`, `author`, `volume`, `page`, `year` | for books and articles; Shamela pages carry volume and page |
| `accessed` | the date the page was fetched and read for this audit; absent if it could not be read |
| `supports` | what the source backs: any of `date`, `place`, `people`, `narrative`; absent where not yet assessed |
| `note`, `noteAr` | what the source actually says, where that differs from or qualifies the entry |
| `archive` | reserved for an archived copy; unused so far |

Only fields with a value are written. The panel shows the list as its own **Sources** section
with each title, its full address, what it backs and its note.

### 6.2 The audit

All 82 distinct URLs behind the 172 events were fetched and checked against the claim of each
event that cites them: the place, the people, the title and, for EPI/EXT events on
English-language pages, the year. 78 were read; Iranica (`hira`, cited by `hira-bishop-410` and
`hira-surrenders`) and academia.edu (`satih-prophecy`) refuse automated access and remain
unread; the UNESCO page for al-Faw was confirmed by search to be the right site. One link was
dead, six pointed at a page that does not carry the event, and four pointed at a contents list
rather than the account:

| event | was | problem | now |
|---|---|---|---|
| `barqi-robin-naiit` | Wikipedia *Bāriqī-Robin-Nāʿiṭ 1* | page deleted 2026-03-21 (G8); no archived copy | Wikipedia *Abraha*; al-Bāriqī & Robin 2025, *Semitica et Classica* 18: 295–300 (no link; cited from a bibliography, not consulted) |
| `basus-hanw` | marefa *حرب البسوس* | page does not name al-Ḥanw | al-Kāmil i 484 (Shamela 21712/480); almerja Basūs page |
| `basus-naqiyya` | marefa *حرب البسوس* | page does not name al-Naqiyya | al-Kāmil i 484; almerja Basūs page |
| `hira-palmyrene-garrison` | marefa *الحيرة* | page has neither 132 nor Palmyrene troops | ar + en Wikipedia *al-Ḥīra*, **with a note: both give 32 CE, not 132, and no garrison** — see 6.3 |
| `dahis-peace` | en Wikipedia *Dahis and al-Ghabra* | page does not mention the peace | ar Wikipedia *الحارث بن عوف المري*, *هرم بن سنان* |
| `asha-dies` | en Wikipedia *Muʿallaqāt* | mentions al-Aʿshā, not his death | en Wikipedia *Al-A'sha* (gives c. 625 — inside this entry's 625–630, at its low end; noted); ar Wikipedia *أعشى قيس* |
| `himyar-conquers-saba` | en Wikipedia *Himyar* | does not name Shammar Yuharʿish; dates Ḥaḍramawt c. 300, against this entry's "already taken" | en Wikipedia *Shammar Yahri'sh* (first attested 275, Yemen united by c. 280); ar *شمر يهرعش* |
| `dahis-yamariyya` | al-ʿIqd vi 18 (Shamela 23789/1829) | the chapter page; the day's name was only in the contents sidebar | al-ʿIqd vi 21 (23789/1832), the day's own account |
| `dahis-qatan` | al-ʿIqd vi 18 | as above | al-ʿIqd vi 25 (23789/1836) |
| `dahis-ghadir-qalha` | al-ʿIqd vi 18 | as above | al-ʿIqd vi 25, after Yawm Quṭn |
| `shaqiqa-bistam` | al-Kāmil i 453 (21712/449) | the contents page of the ayyām | ar Wikipedia *يوم الشقيقة*; al-Kāmil i 548 (21712/544) |

Two more found on the way: `awara-i` cited a fajernet list that names the day and nothing more
— replaced with ar Wikipedia *يوم أوارة الأول* and al-Kāmil i 497; `basus-quda` keeps its
marefa page and gains al-Kāmil i 483, which tells Yawm Quḍḍa / Taḥlāq al-Limam directly.

Not changed, but worth knowing: 33 URLs serve 123 events between them. *Muhammad* (en
Wikipedia) backs 11 events, *Marib Dam* 7, al-ʿIqd vi 18 still backs `malik-ibn-zuhayr-killed`
correctly. These are container pages — they do carry the claim, usually in one sentence.

### 6.3 Open question: al-Ḥīra in 132

`hira-palmyrene-garrison` (REVISION.ar.md §11) puts the oldest mention of al-Ḥīra in 132 CE,
from Palmyrene troops stationed there, graded EXT / fixed. No source found in this audit carries
either the year or the garrison. Both Wikipedias say instead that the oldest mention is a
Palmyrene-era text dated **32 CE**, and say nothing of troops. The entry is left exactly as it
was — year, grade and dispute untouched — with the two Wikipedia pages attached and the
discrepancy stated in their notes, until the Arabic source behind §11 is found. If it turns
out to be 32, the event falls a century earlier and its `dispute` needs rewriting; if no
source carries the garrison, the summary does too.

### 6.4 Imruʾ al-Qays — a pilot of multi-source, two-language citation

Every event that names an Imruʾ al-Qays now has three to five sources, at least one English
and one Arabic, each read and checked against the event. Nothing in the entries changed.

| event | added |
|---|---|
| `hujr-killed` | Nicholson, *Literary History of the Arabs* (1907) p. 104; ar Wikipedia *حجر بن الحارث*; Ibn Kathīr, *al-Bidāya wa-l-nihāya* ii (Wikisource), via Ibn al-Kalbī |
| `imru-vengeance-war` | Nicholson p. 105; ar Wikipedia *امرؤ القيس*; Ibn Kathīr; *Ashʿār al-shuʿarāʾ al-sitta* (editor's introduction, Shamela 5449 p. 1) |
| `samawal-dies` | ar Wikipedia *السموأل*; *Jewish Encyclopedia* (1906) "Samuel ibn ʿAdiya"; Nicholson pp. 84–85 |
| `imru-constantinople` | Nicholson p. 104; *Jewish Encyclopedia*; ar Wikipedia *امرؤ القيس*; Ibn Kathīr |
| `imru-death` | Nicholson p. 104; ar Wikipedia *امرؤ القيس*; *Ashʿār* introduction p. 2; Ibn Kathīr |
| `namara-inscription` | en Wikipedia *Namara inscription*; ar Wikipedia *نقش النمارة* (the other Imruʾ al-Qays, ibn ʿAmr) |

The new sources do not agree on his dates, and the notes say so rather than choosing:
Nicholson puts the death "about 540", Arabic Wikipedia gives his life as 500–540, the
*Ashʿār* introduction gives 560, and English Wikipedia keeps the 561–565 this atlas uses.
Ibn Kathīr has Caesar poison him but places the death at Jabal ʿAsīb rather than Ankara. The
*Jewish Encyclopedia* says it is not known whether al-Samawʾal's siege came before or after the
poet's death, which matches the existing `dateNote` of `samawal-dies`.

Two of these need care. The *Ashʿār* pages are the modern editor's introduction, not
al-Aʿlam al-Shantamarī, and Shamela's page numbers there do not match the printed book; both
facts are in the notes. Britannica was wanted and could not be read (it refuses automated
access), so it is not cited. *Kitāb al-Aghānī*, the main classical source for every one of
these episodes, was not reachable online in a citable form and is the obvious next addition.
