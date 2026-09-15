# Decisions Log

Kept as we go, so anyone (including a future session) can see not just what was
built, but why.

## Static HTML instead of an interactive map
An earlier version of this project was a Leaflet map with markers. It was
dropped. A live map needs a local web server to run (browsers block `fetch()`
on `file://` pages) and a third-party tile provider, and the tile provider had
already changed its terms twice, breaking the page with no change on our end.
A generated static page has neither dependency: it opens by double-clicking and
nothing outside this folder can break it.

A map is still worth having, and SPEC.md keeps it as a nice-to-have. The way
back in is a drawn map with inlined coordinates, not tiles.

## No dependencies
`build_report.py` uses only the Python standard library. No pandas, no Jinja,
no plotting library. The chart is hand-generated SVG, which keeps the output a
single file with no runtime assets and means anyone can run this with whatever
Python they already have.

## Data captured, not fetched
`data/markets.json` is a snapshot of the city's published schedule, committed to
the repo, rather than something the script downloads when it runs. The report
then builds identically offline, on any machine, at any point in the future, and
the numbers in it can be traced to a specific retrieval date. Refreshing the
data is a separate, deliberate step.

## Chart covers the full calendar year
The x-axis runs January through December, so the off-season is visible as empty
space rather than cropped out. This was the default when the chart was built,
not a considered decision about what the reader most needs to see. Most markets
run roughly May through October, so a large share of the chart is empty.

## Link (SNAP) status shown by color
Link acceptance is encoded as the color of each market's marks in the chart
rather than as a separate column or a second chart. It is the dimension most
relevant to the food-access question in SPEC.md, so it belongs on the main
visual rather than beside it.

## Ordering
Markets are ordered by day of week, then alphabetically within each day, in both
the chart and the listing.

## What's open this week
Not started. It is listed as a "must have" in SPEC.md, but no logic or markup
for it exists yet.
