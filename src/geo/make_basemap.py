#!/usr/bin/env python3
"""Clip Natural Earth land, rivers and lakes to the Arabian region.

Downloads three Natural Earth 1:50m layers, clips them to the bounding box
below, simplifies them, drops features that did not exist in late antiquity
(the Suez Canal, Lake Nasser and so on), and writes the compact JSON the
atlas ships with.

Only needed if you want to regenerate the basemap. The committed
land.json / rivers.json / lakes.json are the output of this script.

    pip install shapely
    python3 make_basemap.py
"""
import json
import os
import urllib.request

from shapely.geometry import box, shape
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
BBOX = (20.0, 0.0, 72.0, 50.0)  # lon_min, lat_min, lon_max, lat_max

BASE = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/"
SOURCES = {
    "land": "ne_50m_land.geojson",
    "rivers": "ne_50m_rivers_lake_centerlines.geojson",
    "lakes": "ne_50m_lakes.geojson",
}

# Features that are modern engineering, not late-antique geography.
MODERN_RIVERS = {"Suez Canal", "Ismailiya Canal", "Gharraf Canal"}
MODERN_LAKES = {"Lake Nasser", "Lake Tharthar", "Razzaza Lake",
                "South Aral Sea", "Sarygamysh Köli"}


def download(name, filename):
    path = os.path.join(HERE, "_" + filename)
    if not os.path.exists(path):
        print("downloading", filename)
        urllib.request.urlretrieve(BASE + filename, path)
    return json.load(open(path))


def rounded(coords):
    return [[round(x, 3), round(y, 3)] for x, y in coords]


def main():
    clip = box(*BBOX)

    # --- land -------------------------------------------------------------
    geoms = []
    for f in download("land", SOURCES["land"])["features"]:
        g = shape(f["geometry"])
        if not g.is_valid:
            g = g.buffer(0)
        if g.intersects(clip):
            geoms.append(g.intersection(clip))
    land = unary_union(geoms).simplify(0.035, preserve_topology=True)

    polys = list(land.geoms) if land.geom_type.startswith("Multi") else [land]
    out_land = [{"o": rounded(p.exterior.coords), "i": []}
                for p in polys if p.geom_type == "Polygon" and p.area >= 0.02]

    # --- rivers -----------------------------------------------------------
    out_rivers = []
    for f in download("rivers", SOURCES["rivers"])["features"]:
        name = f["properties"].get("name") or ""
        if name in MODERN_RIVERS:
            continue
        g = shape(f["geometry"])
        if not g.intersects(clip):
            continue
        g = g.intersection(clip)
        parts = list(g.geoms) if g.geom_type.startswith("Multi") else [g]
        for ls in parts:
            if ls.geom_type != "LineString":
                continue
            simple = ls.simplify(0.03)
            if simple.length < 0.5:
                continue
            out_rivers.append({"n": name, "p": rounded(simple.coords)})

    # --- lakes ------------------------------------------------------------
    out_lakes = []
    for f in download("lakes", SOURCES["lakes"])["features"]:
        name = f["properties"].get("name") or ""
        if name in MODERN_LAKES:
            continue
        g = shape(f["geometry"])
        if not g.intersects(clip):
            continue
        g = g.intersection(clip).buffer(0)
        if g.area < 0.05:
            continue
        parts = list(g.geoms) if g.geom_type.startswith("Multi") else [g]
        for p in parts:
            if p.geom_type == "Polygon":
                out_lakes.append({"n": name,
                                  "o": rounded(p.simplify(0.02).exterior.coords)})

    for name, payload in (("land", out_land), ("rivers", out_rivers), ("lakes", out_lakes)):
        path = os.path.join(HERE, name + ".json")
        json.dump(payload, open(path, "w"), separators=(",", ":"))
        print(f"{name}.json  {len(payload)} features  {os.path.getsize(path)} bytes")


if __name__ == "__main__":
    main()
