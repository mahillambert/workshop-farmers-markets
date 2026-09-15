# Data Sources

## Chicago Farmers Markets 2026 Schedule
- **Publisher:** City of Chicago, Department of Cultural Affairs and Special
  Events (DCASE)
- **URL:** https://www.chicago.gov/city/en/depts/dca/supp_info/farmers_market_schedule.html
- **Retrieved:** 2026-09-15
- **Captured to:** `data/markets.json`

The published schedule lists markets grouped by day of week, each with an
address, a season, and hours. Two markers appear on the page and are carried
into the data:

- `(L)` — the market accepts Link (SNAP) benefits, captured as `accepts_link`
- `*` — independently run Community Partner market supported by DCASE,
  captured as `community_partner`

### Why not the Chicago Data Portal
The data portal has a "Farmers Markets" dataset
(https://data.cityofchicago.org/Environment-Sustainable-Development/Farmers-Markets-Map/atzs-u7pv),
which would be the more natural machine-readable source. It was not used: its
base year is 2011 and it has not been refreshed for recent seasons, so it lists
markets that no longer operate and omits current ones. The DCASE schedule page
is the authoritative current listing.

This is worth knowing before anyone "improves" the project by switching to the
API. The portal dataset is easier to consume and wrong.

### Known wrinkles in the source
- A few markets run on two different days of the week, with different hours and
  season dates on each. These appear as separate entries on the source page and
  as separate records here.
- Some markets publish a continuous season ("May 16 - October 31"); others
  publish a list of specific dates, usually twice a month.
- One market (Farm on Ogden's Summer Market) is listed without an address.
- A small number of the city's listed dates do not fall on the market's stated
  day of week. These were transcribed as published rather than corrected.
