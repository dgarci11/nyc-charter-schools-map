# NYC Charter Schools Map

An interactive map of **462 charter school sites across New York City's five boroughs**.

**Live map:** https://USERNAME.github.io/nyc-charter-schools-map/


| Borough | Schools |
|---|---|
| Brooklyn | 157 |
| Bronx | 154 |
| Manhattan | 92 |
| Queens | 47 |
| Staten Island | 12 |

## Features
- Every charter school site as a point, colored by borough, clustered at low zoom
- Click a point for the name, address, school type, district, and data source
- Filter by borough and search by name, address, or ZIP

## Data
- **Source:** NYC Department of City Planning [Facilities Database (FacDB)](https://data.cityofnewyork.us/d/ji82-xba5) on NYC Open Data, subgroup `CHARTER K-12 SCHOOLS` (last refreshed July 2026). FacDB already geocodes each site and combines two inputs:
  - NYC DOE's Location Code Generation and Management System (LCGMS): 286 sites
  - NYSED's active-institutions list: 180 records
- **Cleaning** (`scripts/fetch_data.py`):
  - Merges rows that have the same normalized name at the same location, which removes 3 duplicates across the two sources
  - Drops 1 record whose address is outside NYC (a Westchester ZIP)
- **Note:** this counts *sites*. Many charter networks run several campuses under one charter, and co-located schools can share a building, so the total is higher than the number of charters NYSED reports for NYC.

## Run locally
```bash
python3 scripts/fetch_data.py      # refresh data/charter_schools.geojson
python3 -m http.server 8000        # open http://localhost:8000
```

## Stack
Static HTML + [Leaflet](https://leafletjs.com/) + Leaflet.markercluster, CARTO Positron basemap. No build step; hosted on GitHub Pages.
