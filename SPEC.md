# Chicago Farmers Markets 2026 — Spec

## Goal
Answer a practical question about food access in Chicago: **when and where can
someone get to a farmers market, and which markets accept Link (SNAP)?**

A plain list doesn't answer this, because Chicago's markets are seasonal and
most run only part of the year. The report has to show the shape of the season,
not just the roster.

## Must have
- A single self-contained `report.html` that opens directly in a browser, with
  no web server, no internet connection, and no separate CSS or JS files
- A chart showing, for each market, **the days it is actually open** across the
  season, so gaps and short seasons are visible
- Link (SNAP) acceptance distinguished in the chart
- Headline figures: number of markets, total market days in the season, and
  how many markets accept Link
- A count of markets by day of week
- A full listing of every market with name, address, hours, season, and Link
  and community-partner status
- A **"what's open this week" section** listing the markets running in the next
  seven days — **not yet built**
- Every market in `data/markets.json` appears in the report
- All market details come from `data/markets.json`, so the report can be
  regenerated after a data update without touching the script

## Nice to have (not required for v1)
- A simple static map of market locations, drawn without map tiles or any
  network request. The data has addresses but no coordinates, so this needs
  geocoding first.
- Filtering the listing by day or by Link acceptance
- Walking distance or transit access to each market

## Out of scope for this version
- A tile-based interactive map (see DECISIONS.md)
- Live data: the schedule is captured once per season, not fetched at runtime
- Vendor-level detail (what each market sells)

## Data
`data/markets.json` is the City of Chicago's published 2026 farmers market
schedule, captured on the date recorded in the file's `retrieved` field.

**One record per market-day.** A market that runs on two different days of the
week has two records, because the season, hours, and Link status can differ
between them.

Schedules come in two shapes, and both appear in the data:
- `"type": "range"` — the market runs every week between `start` and `end`,
  minus any dates in `exceptions`
- `"type": "dates"` — the market runs **only** on the specific dates listed,
  typically twice a month
