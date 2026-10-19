# arabia.json — authoring notes

Companion to `/home/claude/data/arabia.json`. Everything below is about the *data's* reliability, not the period's.

Counts: 108 places, 154 events, 96 people, 13 polities, 26 tribes.

---

## 1. Coordinates I had to guess

`coordConfidence` is set honestly on every place. The split is **33 exact, 30 approximate, 45 guessed**.

**`guessed` — do not draw a confident pin.** Almost all of these are battlefields. The ayyām corpus names a water, a hill or a clan's pasture and nothing more; the research notes repeatedly say "no coordinates found for any site." I placed each one in the right *region* (the tribes' known range, or the landmark the source measures from) and nothing finer.

| id | why guessed |
|---|---|
| `shib-jabala` | Sources give only "an isolated mountain pass ~150 km south of ʿUnayza". I put it 150 km south of real ʿUnayza. |
| `dhi-qar` | Deliberately unlocated by the sources. The modern Iraqi governorate name is the only hook, and the research notes flag that localisation as *their* inference, not a sourced claim. I used it anyway and marked it guessed. |
| `buath` | Near Medina; no position relative to the oasis is given anywhere. |
| `al-kulab`, `khazaz`, `al-sullan` | Placed from al-Khāqānī's one-line glosses only: "a water between Kūfa and Baṣra", "a mountain between Baṣra and Mecca", "a valley in Tihāma beside Mount Khazāz". |
| `rahrahan` | The narrative names no toponym at all — only "the nearest waters of Banū Dārim". |
| All seven Basūs days (`al-nahy`, `al-dhanaib`, `waridat`, `al-qusaybat`, `quda`, `al-fusayl`) and `dhi-najab` | Undated and unlocated. Scattered across plausible Bakr/Taghlib ground in lower Iraq and northern Najd. These are *spacing* choices for map legibility, nothing more. |
| All Dāḥis days (`al-habaa`, `dhu-husa`, `al-muraqqab`, `al-faruq`, `al-raqam`, `araair`) | Same. Placed in ʿAbs/Fazāra country. |
| `ayn-ubagh` | "ʿAyn Ubāgh at Dhāt al-Khiyār" — a spring in the steppe between Syria and Iraq. Nothing narrows it. |
| `al-mushaqqar`, `hajar-yamama`, `fulayj`, `tuwarin`, `qusayba`, `wadi-abqar`, `ruwafa` | Named in the sources with no identified site. `al-mushaqqar` is explicitly absent from every source the researchers reached. `wadi-abqar` may never have been a real place at all — nothing confirms it beyond "a deep valley in Najd". |
| `majanna`, `dhu-al-majaz`, `nakhla`, `shamta`, `al-abla`, `al-hurayra` | The Fijār fairground cluster. Only ʿUkāẓ itself has published coordinates; the rest are "near ʿUkāẓ" or "near Mecca". I ringed them around ʿUkāẓ. |
| `al-mushallal`, `nakhlat-al-shamiyya`, `hudhayl-country`, `tabala`, `jurash` | Shrine sites known only from Ibn al-Kalbī's place-formulas ("between Medina and Mecca", "seven nights from Mecca"). |
| `khawarnaq` | "Near al-Ḥīra" is all Iranica gives. `al-Sadīr`, the other Lakhmid palace, has nothing but a name and is **not in the dataset**. |
| `awara`, `tikhfa`, `al-nisar` | Undated and unlocated days. |

**`approximate`** means the region or the near-neighbour town is certain and the point is within a few tens of km: `hira` (ruins ~7 km ESE of Najaf, measured from Najaf), `namara` and `jabal-says` (both "~100–105 km SE of Damascus"), `al-jabiya` ("between the Ḥawrān plain and the Golan, west of Nawā"), `hima` ("~90 km north of Najrān"), `naiit` ("~50 km north of Ṣanʿāʾ"), `zafar` ("near Ṣanʿāʾ"), and the Gulf/eastern sites.

**`exact`** means a real modern settlement or a securely identified archaeological site. `ukaz` carries published coordinates (21°28′28″N, 40°38′42″E) and is the only fair in the set that does.

---

## 2. Events I could not date at all

Every one of these is in the dataset with a best-guess central `year`, an honest `dateCertainty`, the real spread in `dateRange`, and the problem stated in `dispute`. **Nothing was dropped for lacking a date, and no precision was invented.** But `year` for these is a *placement*, not a claim.

### Completely undated — `dateCertainty: "legendary"`

- **All seven named days of the Basūs war.** The only date anywhere in the corpus is the war's overall 494–534 span, from one modern Arabic compilation. The individual days have no year in any source. I spread them 496–530 to preserve the sequence the sources *do* give (ʿUnayza → al-Nahy → al-Dhanāʾib → Wāridāt → al-Quṣaybāt → Quḍa → al-Fuṣayl), which is far more trustworthy than the years.
- **All the days of Dāḥis wa-l-Ghabrāʾ.** Same situation, worse: the war's conventional bracket of "c. 568–609" is **Sir William Muir's Victorian reconstruction, not a source date**, and that is stated in the `dispute` field of `dahis-race`. I spread the days 568–589 along al-ʿIqd al-Farīd's ordered index, which is the only source giving a sequence *with* winner and loser per day.
- **Yawm ʿAyn Ubāgh** (`ayn-ubagh`). No date in any source reached. I placed it c. 556, between the two Lakhmid generations, and the `dispute` field explains that it is a distinct battle from Ḥalīma, not a conflation.
- **Yawm Khazāz**, **al-Sullān I and II**, **al-Kulāb I and II**, **al-Ṣafqa**, **Ṭikhfa**, **al-Nisār**, **Awāra I and II**, **al-Bardān**, **al-Waqīṭ**, **al-Shaqīqa**.
- **Yawm al-Nisār** is the weakest entry in the file: an index entry in three medieval lists, no narrative, no place, no date. Its `year` of 500 is a bare midpoint of the period and the `dispute` field says so.
- **Ḥilf al-Fuḍūl.** Undated in every source, and the research explicitly warns that the Fijār→Ḥilf al-Fuḍūl causal chain is unverified.
- **Qusayy taking the Kaʿba.** See §4 — the contradiction is a century wide.
- **The Fijār days** are dated only by Muḥammad's reported age at them (given as 14 to 20), which itself depends on the Year of the Elephant. The one CE figure in the whole cycle is al-Khāqānī's "Fijār II ends 589", which I used for `fijar-hurayra`.

### Where `dateRange` carries a genuine published spread

These are the ones a map-builder should render as a bar, not a tick:

| event | range | nature of the spread |
|---|---|---|
| `shib-jabala` | 551–600 | 551, 553, 570, c. 580 (Caskel), and "under al-Nuʿmān III, 582–602" (Bosworth). ~50 years for one famous battle. I adopted **c. 580** internally per the report's recommendation, because it is the only option compatible with al-Mundhir IV (r. 575–580) appearing among the leaders. The report suggests letting **570 stand as the folk date characters cite**. |
| `year-of-elephant` | 552–572 | Five directions: traditional c. 570–571; 568/9 from South Arabian finds; **552** on Ry 506, which Gajda accepts and which does not name Mecca; "one or two decades earlier than 570"; and 14 Feb 572 (Zein and el-Wakil). Plus al-Zuhrī's tradition putting it before Muḥammad's father was born — the tradition contradicting itself. |
| `aksumite-invasion` | 525–543 | 525 (Munro-Hay, on an 518 accession for Dhū Nuwās), c. 530 (on a 523 accession), as late as **543** (Jacques Ryckmans). |
| `dhi-qar` | 602–624 | Muslim tradition spreads it 602–624; modern scholarship narrows to 604–611. The 602 deposition is a hard lower bound because every account chains the battle to al-Nuʿmān's fall. |
| `dhu-nuwas-accession` | 517–523 | Three incompatible dates in two reference articles: 517, 522, "518 or 522". |
| `dam-final-breach` | 570–575 | Given as either, with no source for either figure. |
| `imru-constantinople` / `imru-death` | 561–565 | And see `imru-al-qays-poet`'s `lifeNote` for the two irreconcilable birth schemes. |
| `faw-abandoned` | 400–500 | "Abruptly abandoned around the 5th century" is the whole of it. |
| `abraha` (person) | — | His `lifeNote` records that the *firm epigraphic window is 547–559*, not the 535–570 tenure the infoboxes give. |

### Two events deliberately outside the 300–640 window

`nabataea-annexed` (106) and `thamud-temple-ruwafa` (167). Both are in because the period inherits them directly — the Bostran era dates four of the eight key inscriptions, and the Ruwāfa temple is the hard counter-evidence to a belief that was live in the 6th century. `zenobia-marid` (269) is just before the window. Each says so in its `dispute` field. A time slider starting at 300 will hide them; that is probably correct, but they are there if you want a "ruins layer" toggle.

---

## 3. Inconsistencies between the report and the notes

Where the two disagreed I followed the notes, because the notes carry the URLs.

1. **Dāḥis day-names.** The report's prose lists the sequence as "al-Murayqib, Dhū Ḥusā, al-Habāʾa, al-Farūq, al-Raqam, ʿArāʿir" and separately gives the full al-ʿIqd al-Farīd order including **al-Yaʿmariyya, Qaṭan and Ghadīr Qalhā**. The notes are explicit that al-Yaʿmariyya sits between Dhū Ḥusā and al-Habāʾa and is omitted from most popular lists. I included all of them, and flagged in each `dispute` field that al-Raqam is actually Ghaṭafān over Banū ʿĀmir — **not an ʿAbs-vs-Dhubyān day at all** — and that al-Farūq is tagged to a different tribal pairing in a different list. The notes' conclusion is that these are day-*names* reused for more than one engagement.
2. **Basūs day order.** The report gives ʿUnayza → al-Nahy → al-Dhanāʾib → Wāridāt → al-Quṣaybāt → Quḍa → al-Fuṣayl. The notes record that **al-Maʿrifa makes al-Nahy the first engagement**, not ʿUnayza, and reverses the outcome at al-Quṣaybāt. Both are in the `dispute` fields. Also: al-ʿIqd al-Farīd's index lists only five Basūs days, dropping al-Fuṣayl and al-Quṣaybāt entirely.
3. **Spelling of the Dāḥis first day.** Report prose has "al-Muraqqab" in one place and the user's brief has "al-Murayqib"; the Arabic index reads المريقب. I used `al-muraqqab` / al-Muraqqab, matching the report's transliteration of the index entry.
4. **Dam repair date.** The report has "One source dates an Abraha repair to **543**, which clashes with CIH 541's **548**". Unresolved in the sources; I entered both as separate events (`abraha-dam-repair` with `dateCertainty: "contested"`, and `dam-breach-548` + `cih541`) and said so in the dispute field.
5. **Last dam repairs: 557 vs 558.** The user's original brief said 558; the notes say the source reads **557**. I used 557.
6. **Ḥarrān builder's patronym.** Often reported as "Sharāḥīl ibn Ẓālim". The notes are explicit that the publication **reads Ṭalimu, not Ẓālim**. I used Ṭalimu and flagged it.
7. **Qaryat al-Fāw as the Kindite capital.** The report calls this identification "almost certainly a conflation", and the notes are blunter: the site article has the Kinda leaving around **300 CE** and the city abandoned shortly after, which directly contradicts using Fāw as the capital of a 450–550 Kindite kingdom. So **`kinda` has `capitalId: null`** — the 5th–6th-century Kinda were a Najdī over-tribal power with no confirmed urban capital. Fāw is in `places` as a `site` with its abandonment as an event.
8. **Lakhmid king-list.** The conventional table (ʿAmr I 268–295, Imruʾ al-Qays I 295–328, and so on) is in neither the dataset's events nor its people before al-Mundhir III, because *Encyclopaedia Iranica* declines to print a king-list at all and the report treats that refusal as a scholarly signal. Only rulers with EXT or EPI anchors are in `people`. The report's own instruction — "treat anything before al-Mundhir III as free narrative space" — is why.
9. **ʿAmr ibn Hind's accession.** The conventional table says 554, but Ry 506 has "ʿAmr ibn al-Mundhir" acting in **552**. Both are in the data, with the tension noted on the person record and on `murayghan-1`.
10. **Al-Mundhir III's tribute.** One source says Rome was paying him tribute "by 561", seven years after his own death in the same source's table. Visibly broken; omitted.
11. **Al-Nuʿmān III's reign.** Given as 580–602 in an infobox and 582–c. 602 in the lead of the same article, and as 580–595 elsewhere. The event is `dateCertainty: "contested"` with `dateRange: [580, 582]`.
12. **Buʿāth's outcome.** The Buʿāth article says the Aws won; the Banū Qurayẓa article calls the day inconclusive. Flagged.
13. **Raḥraḥān's victor.** Ibn al-Athīr has Banū ʿĀmir and the Lakhmids routed; al-ʿIqd al-Farīd's index tags the day for ʿĀmir *over* Tamīm — the opposite. Al-Qalqashandī's list suggests the name covers two engagements. All in the dispute field.
14. **ʿArāʿir.** `almerja.com` and its own mirror `mail.almerja.net` return **different text** for the same page id, and disagree about which tribe lost. Flagged.
15. **ʿAntara's death.** Three mutually exclusive versions (killed in the Dāḥis fighting / slain by Wasr ibn Jābir or against Ṭayyiʾ / died of old age). The dataset uses the traditional 608 with the alternatives in `dispute`; note that the "died in the Dāḥis war" version is incompatible with the 608 date in the same corpus.
16. **Zarqāʾ al-Yamāma's sight-range.** A week, not three days. And the Ṭasm/Jadīs page does not mention her while her page makes her a Jadīsī, so the traditional join between the two stories is unverified.

---

## 4. Things deliberately left *out*, and why

- **`al-Sadīr`** (the second Lakhmid palace): attested as a bare name with no description, date or location. Nothing to put on a map.
- **`Jalliq`**: mentioned in none of the Ghassanid sources reached; its location (Damascus Ghūṭa? al-Jābiya itself?) could not be confirmed. A poetically attested site of uncertain identification.
- **Yawm al-Firāḍ, Yawm al-Bishr, Yawm Aḥad al-Jaww**: the notes say **nothing found** for these in any of five medieval indexes. Aḥad al-Jaww is probably Awāra, which *is* in the data. I did not invent entries.
- **`Harim ibn Sinān`** as the Dāḥis peacemaker and the dedicatee of Zuhayr's Muʿallaqa: **unverified**, and his father Sinān appears only as a failed *war* coalition-builder, on the opposite side of the matter. Every peace account credits al-Ḥārith ibn ʿAwf al-Murrī alone, so that is what `dahis-peace` says, with the problem in its `dispute` field.
- **ʿAbla**, and the whole `Sīrat ʿAntara` layer: later accretion, no attestation in the earliest sources.
- **The 50,000 Maʾrib migrants** figure: marked citation-needed in the source. Omitted and flagged in `dam-final-breach`.
- **Routine female infanticide**: the notes argue it is a 9th-century anti-Tamīm polemic with no pre-Islamic evidence in any language. Not an event.

---

## 5. Field conventions a map-builder needs

- **`zones[].centers[].r` is kilometres of soft influence, not a border.** Polities with patchy reach get several centers. Zones change where the extent genuinely shifted: `himyar` at 380, `aksumite-yemen` 525–570, `sasanian-yemen` from 570, `kinda` rising and collapsing (450 / 528 / 550), `ghassanids` at 528, 569 and 584 (the breakup), `lakhmids` ending **602** not 640, `quraysh` expanding after 580. `aksumite-yemen` and `sasanian-yemen` are separate polities from `aksum` and `sasanians` so that the occupation can be rendered as its own blob with its own lifespan.
- **`year` is always the single best central estimate** and is always inside `dateRange`. For `dateCertainty: "legendary"` entries, treat `year` as a map-placement, not a claim. Two events (`nabataea-annexed`, `thamud-temple-ruwafa`) and one person (`abu-amr`, an 8th-century philologist) sit outside the 300–640 window on purpose.
- **107 of the 154 events carry a non-null `dispute`.** That is not noise — it is the honest proportion for this period, and the single most useful thing in the file. If the UI hides `dispute` by default, the data is being laundered.
- **`people` is 96 entries, above the 35–60 the brief asked for.** The notes had enough substantive material on the minor Basūs and Dāḥis cast — Bujayr, al-Ḥārith ibn ʿUbād, Ḍirār, Wabra, Qarāwash, Shaddād — that cutting them would have thrown away exactly the scene-level detail the sources preserve best. Filter on `role` or `lifeCertainty` if the cast is too large for a UI.
- **37 of 96 people have a non-empty `path`.** The rest are empty by design rather than invention — the notes are explicit that, for example, there is **no documented itinerary** for Imruʾ al-Qays's wanderings, so his six-step path is reconstructed from scattered episodes (Najd → Taymāʾ → Ghassanid territory → Constantinople → Ankara) exactly as the report recommends, and no further.
- **`evidence` uses the report's scheme exactly**: EPI, EXT, TRAD, RECON. The hard EPI spine of the whole file is eight points: **Namāra 328, Zabad 512, Jabal Usays 528, CIH 541 = 548, Dūmat al-Jandal 548/9, Ry 506 = 552, Ḥarrān 568, and the last dated Ḥimyarite text 559/560.** Everything else hangs off those plus the Greek and Syriac sources. If you want a "what do we actually know" filter, that is it.
- Three places (`awwam`) end before 640 on purpose: the Awām temple was abandoned in the 4th century, so it should drop off a time slider before the story starts.
