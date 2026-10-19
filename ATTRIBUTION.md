# Attribution

## Basemap geometry

Coastlines, rivers and lakes in `src/geo/land.json`, `rivers.json` and
`lakes.json` are derived from **Natural Earth** 1:50m physical vectors
(`ne_50m_land`, `ne_50m_rivers_lake_centerlines`, `ne_50m_lakes`), clipped to
20–72°E / 0–50°N and simplified by `src/geo/make_basemap.py`.

Natural Earth is in the public domain. From their terms:

> No permission is needed to use Natural Earth. Crediting the authors is
> unnecessary.

Credited anyway. <https://www.naturalearthdata.com/>

Modern features were removed by hand so the map does not show engineering that
post-dates the period: the Suez and Ismailiya canals, the Gharraf Canal, Lake
Nasser, Lake Tharthar, Razzaza Lake, and the modern shrunken Aral.

## Hand-authored layers

Everything in `src/geo/terrain.json` — the sand seas, mountain ranges, region
names and sea names — was drawn and placed by hand against modern maps. It is
approximate by nature and is covered by this repository's MIT licence.

## Typefaces

Loaded at runtime from Google Fonts, all under the SIL Open Font License 1.1:

- **Amiri** — Khaled Hosny. Naskh for Arabic, with a companion Latin.
- **IBM Plex Sans** and **IBM Plex Mono** — Mike Abbink and Bold Monday for IBM.

## Chronology

`data/arabia.json` is compiled from published scholarship and from the Arabic
primary sources. Individual events carry a `source` URL where one exists.
`data/NOTES.md` lists the coordinates that were guessed, the events that could
not be dated, and the conflicts between sources that had to be adjudicated.
`research/` holds the report and the research notes behind it.

Where this dataset is used, the evidence and certainty flags should travel with
it. Stripping them turns a graded reconstruction into false precision.
