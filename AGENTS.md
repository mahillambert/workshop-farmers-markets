# AGENTS.md

## What this is
A single Python script, `build_report.py`, that reads `data/markets.json` and
writes a self-contained `report.html` summarizing Chicago's 2026 farmers market
season. No framework, no build step, no package manager, no web server.

## Before making changes
Read `SPEC.md` (what the report is supposed to contain) and `DECISIONS.md`
(choices already made, and why) first. Update `DECISIONS.md` when you make or
change a decision, not only when you finish a feature.

## Running it
```
python3 build_report.py
```
Writes `report.html`. Open that file directly in a browser.

## Conventions
- Python standard library only. Don't add pandas, Jinja, matplotlib, or a build
  step without a real reason, and record it in `DECISIONS.md` if you do.
- `report.html` must stay a single self-contained file: styles inline, charts as
  inline SVG, no external CSS or JS, no network requests at view time. It has to
  work offline and when opened from `file://`.
- `report.html` is a generated artifact. Change `build_report.py`, never
  `report.html` by hand.
- Market details live in `data/markets.json`. Don't hardcode any market's name,
  address, day, hours, or season into the script.
- `data/markets.json` is a captured snapshot with a recorded source and
  retrieval date (see `SOURCES.md`). Don't edit market records to make the code
  work. If the data looks wrong, say so rather than changing it.

## Verifying changes
There is no test suite. To check a change: re-run the script, open
`report.html` in a browser, and read the rendered page against `SPEC.md`.

The script exiting cleanly is not evidence that the report is correct. A
dropped record, a miscounted total, or a schedule drawn the wrong way produces
a page that renders perfectly and says something false. Check the actual
content against the spec and against `data/markets.json`, and when you report
back, say which parts you verified by looking at the output and which parts you
are assuming.
