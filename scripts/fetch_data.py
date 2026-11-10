"""Download NYC charter school locations and write data/charter_schools.geojson.

Source: NYC Department of City Planning, Facilities Database (FacDB), via NYC Open Data
https://data.cityofnewyork.us/d/ji82-xba5  (subgroup "CHARTER K-12 SCHOOLS").
FacDB combines NYC DOE (LCGMS) and NYSED active-institution records; rows with the
same normalized name at (nearly) the same location are collapsed.
"""
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

URL = "https://data.cityofnewyork.us/resource/ji82-xba5.json?" + urllib.parse.urlencode(
    {"$where": "facsubgrp='CHARTER K-12 SCHOOLS'", "$limit": 5000}
)
OUT = Path(__file__).resolve().parent.parent / "data" / "charter_schools.geojson"
SOURCES = {"doe_lcgms": "NYC DOE (LCGMS)", "nysed_activeinstitutions": "NYSED"}


def norm(name):
    name = re.sub(r"\bCHARTER( SCHOOL)?\b|\bCS\b|\bCHS\b", "", name.upper())
    return re.sub(r"[^A-Z0-9]", "", name)


def main():
    with urllib.request.urlopen(URL) as resp:
        rows = json.load(resp)

    # Prefer DOE rows (richer school-level detail) when collapsing duplicates.
    rows.sort(key=lambda r: r["datasource"] != "doe_lcgms")
    seen, features = set(), []
    for r in rows:
        if not r.get("boro"):  # outside the five boroughs (e.g. a Westchester ZIP)
            continue
        lat, lon = float(r["latitude"]), float(r["longitude"])
        key = (norm(r["facname"]), round(lat, 3), round(lon, 3))
        if key in seen:
            continue
        seen.add(key)
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [round(lon, 6), round(lat, 6)]},
            "properties": {
                "name": r.get("opname") or r["facname"].title(),
                "type": r["factype"].replace(" - CHARTER", "").title(),
                "address": r.get("address", "").title(),
                "borough": r["boro"].title(),
                "zip": r.get("zipcode", ""),
                "district": r.get("schooldist", ""),
                "source": SOURCES.get(r["datasource"], r["datasource"]),
            },
        })

    features.sort(key=lambda f: f["properties"]["name"])
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps({"type": "FeatureCollection", "features": features}, indent=1))
    print(f"{len(rows)} rows -> {len(features)} schools written to {OUT}")


if __name__ == "__main__":
    main()
