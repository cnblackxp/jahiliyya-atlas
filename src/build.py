#!/usr/bin/env python3
"""Build index.html by inlining the geography and the chronology into the template.

    python3 src/build.py [output.html]

The atlas is a single self-contained HTML file with no runtime dependencies and
no network calls except the Google Fonts stylesheet, so the output can be opened
straight from disk or served by GitHub Pages.

The two Arabic files are optional. Without them the page still builds and the
language button simply has nothing to switch to.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEO = os.path.join(ROOT, "src", "geo")
DATA = os.path.join(ROOT, "data")


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_optional(path):
    try:
        return load(path)
    except FileNotFoundError:
        return None


def main():
    geo = {
        "land":    load(os.path.join(GEO, "land.json")),
        "rivers":  load(os.path.join(GEO, "rivers.json")),
        "lakes":   load(os.path.join(GEO, "lakes.json")),
        "terrain": load(os.path.join(GEO, "terrain.json")),
    }
    data = load(os.path.join(DATA, "arabia.json"))
    ui_ar = load_optional(os.path.join(DATA, "ui.ar.json"))
    data_ar = load_optional(os.path.join(DATA, "arabia.ar.json"))

    def dump(obj):
        return json.dumps(obj, ensure_ascii=False, separators=(",", ":")) if obj else "null"

    page = open(os.path.join(ROOT, "src", "template.html"), encoding="utf-8").read()
    page = page.replace("__GEO__", dump(geo))
    page = page.replace("__DATA__", dump(data))
    page = page.replace("__UIAR__", dump(ui_ar))
    page = page.replace("__DATAAR__", dump(data_ar))

    dest = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "index.html")
    with open(dest, "w", encoding="utf-8", newline="\n") as f:
        f.write(page)

    print(f"wrote {dest}  {os.path.getsize(dest) / 1024:.1f} KB")
    for key in ("events", "places", "people", "polities", "tribes"):
        print(f"  {key}: {len(data.get(key, []))}")
    print(f"  arabic interface: {'yes' if ui_ar else 'no'}")
    print(f"  arabic content:   {len(data_ar.get('events', {})) if data_ar else 0} events")


if __name__ == "__main__":
    main()
