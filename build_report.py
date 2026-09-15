"""Chicago Farmers Markets 2026 - season coverage report.

Reads data/markets.json and writes report.html, a single self-contained page
that can be opened directly in a browser.

See SPEC.md for what the report is meant to contain, and DECISIONS.md for why
it is built this way.
"""

import html
import json
from datetime import date, timedelta
from pathlib import Path

DATA_FILE = Path("data/markets.json")
OUTPUT_FILE = Path("report.html")

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Chart geometry
CHART_W = 840
LABEL_W = 258
ROW_H = 16
PLOT_X0 = LABEL_W
PLOT_W = CHART_W - LABEL_W - 12
HEADER_H = 34

LINK_COLOR = "#2f6f4e"
PLAIN_COLOR = "#a8a89c"

STYLES = """
  :root { color-scheme: light; }
  body {
    margin: 0 auto; padding: 32px 24px 64px; max-width: 900px;
    font-family: Georgia, 'Times New Roman', serif; line-height: 1.5;
    color: #1d1d1b; background: #fdfdfb;
  }
  header { border-bottom: 3px solid #1d1d1b; padding-bottom: 14px; }
  h1 { font-size: 1.9rem; margin: 0 0 6px; letter-spacing: -0.01em; }
  .meta { font-family: system-ui, sans-serif; font-size: 0.82rem; color: #6b6b64; margin: 0; }
  .meta a { color: #4a6f8a; }
  h2 { font-size: 1.2rem; margin: 40px 0 10px; padding-bottom: 6px;
       border-bottom: 1px solid #d8d8d0; }
  h3 { font-size: 1rem; margin: 28px 0 6px; font-variant: small-caps;
       letter-spacing: 0.04em; color: #3f3f3a; }
  .stats { display: flex; flex-wrap: wrap; gap: 28px; margin: 22px 0 4px;
           font-family: system-ui, sans-serif; }
  .stat .n { display: block; font-size: 1.7rem; font-weight: 600; line-height: 1.1; }
  .stat .l { font-size: 0.78rem; color: #6b6b64; text-transform: uppercase;
             letter-spacing: 0.06em; }
  table.daycount { border-collapse: collapse; font-family: system-ui, sans-serif;
                   font-size: 0.88rem; margin-top: 6px; }
  table.daycount th, table.daycount td { text-align: left; padding: 4px 22px 4px 0;
                                         border-bottom: 1px solid #e8e8e0; }
  .chartwrap { overflow-x: auto; margin-top: 8px; }
  .legend { font-family: system-ui, sans-serif; font-size: 0.8rem; color: #55554e;
            margin-top: 8px; }
  .legend i { display: inline-block; width: 22px; height: 9px; vertical-align: -1px;
              margin-right: 5px; border-radius: 1px; }
  .market { padding: 10px 0; border-bottom: 1px solid #ededE5; }
  .market:last-child { border-bottom: none; }
  .name { font-weight: 700; font-size: 1rem; }
  .badge { font-family: system-ui, sans-serif; font-size: 0.68rem; font-weight: 600;
           letter-spacing: 0.05em; padding: 1px 6px; border-radius: 3px;
           background: #e3efe7; color: #2f6f4e; margin-left: 7px; vertical-align: 2px; }
  .badge.partner { background: #f0ebe0; color: #7a6433; }
  .detail { font-family: system-ui, sans-serif; font-size: 0.86rem; color: #55554e;
            margin-top: 3px; }
  .season { font-family: system-ui, sans-serif; font-size: 0.82rem; color: #6b6b64;
            margin-top: 2px; }
  footer { margin-top: 48px; padding-top: 16px; border-top: 1px solid #d8d8d0;
           font-family: system-ui, sans-serif; font-size: 0.78rem; color: #85857c; }
  @media (max-width: 560px) { body { padding: 20px 16px 48px; } }
"""


def load_data():
    with DATA_FILE.open() as f:
        return json.load(f)


def market_dates(market):
    """Every date in 2026 this market is open."""
    schedule = market["schedule"]
    start = date.fromisoformat(schedule.get("start") or schedule["dates"][0])
    end = date.fromisoformat(schedule.get("end") or schedule["dates"][-1])
    skip = {date.fromisoformat(d) for d in schedule.get("exceptions", [])}

    weekday = DAYS.index(market["day"])
    current = start
    while current.weekday() != weekday:
        current += timedelta(days=1)

    dates = []
    while current <= end:
        if current not in skip:
            dates.append(current)
        current += timedelta(days=7)
    return dates


def season_text(market):
    schedule = market["schedule"]
    if schedule["type"] == "dates":
        listed = [date.fromisoformat(d) for d in schedule["dates"]]
        shown = ", ".join(f"{MONTHS[d.month - 1]} {d.day}" for d in listed)
        return f"Selected {market['day']}s: {shown}"
    start = date.fromisoformat(schedule["start"])
    end = date.fromisoformat(schedule["end"])
    text = (f"{MONTHS[start.month - 1]} {start.day} to "
            f"{MONTHS[end.month - 1]} {end.day}")
    if schedule.get("exceptions"):
        skipped = [date.fromisoformat(d) for d in schedule["exceptions"]]
        text += " (no market " + ", ".join(
            f"{MONTHS[d.month - 1]} {d.day}" for d in skipped) + ")"
    return text


def unique_markets(records):
    """One entry per market."""
    return list({market["name"]: market for market in records}.values())


def day_counts(records):
    counts = {day: 0 for day in DAYS}
    for market in records:
        counts[market["day"]] += 1
    return counts


def x_for(day, year_start, year_days):
    return PLOT_X0 + PLOT_W * ((day - year_start).days / year_days)


def render_chart(markets, year):
    year_start = date(year, 1, 1)
    year_end = date(year, 12, 31)
    year_days = (year_end - year_start).days

    rows = sorted(markets, key=lambda m: (DAYS.index(m["day"]), m["name"]))
    height = HEADER_H + len(rows) * ROW_H + 8
    parts = [
        f'<svg viewBox="0 0 {CHART_W} {height}" width="{CHART_W}" height="{height}" '
        f'role="img" aria-label="Season coverage by market" '
        f'font-family="system-ui, sans-serif">'
    ]

    for index, name in enumerate(MONTHS):
        gx = x_for(date(year, index + 1, 1), year_start, year_days)
        parts.append(f'<line x1="{gx:.1f}" y1="{HEADER_H - 12}" x2="{gx:.1f}" '
                     f'y2="{height - 8}" stroke="#e6e6dd" stroke-width="1"/>')
        parts.append(f'<text x="{gx + 3:.1f}" y="{HEADER_H - 18}" font-size="9" '
                     f'fill="#8a8a80">{name}</text>')

    for index, market in enumerate(rows):
        y = HEADER_H + index * ROW_H
        color = LINK_COLOR if market["accepts_link"] else PLAIN_COLOR
        label = market["name"]
        if len(label) > 34:
            label = label[:33] + "…"
        parts.append(f'<text x="{LABEL_W - 10}" y="{y + 11}" font-size="10.5" '
                     f'text-anchor="end" fill="#33332e">{html.escape(label)}</text>')
        parts.append(f'<rect x="{PLOT_X0}" y="{y + 3}" width="{PLOT_W}" height="10" '
                     f'fill="#f4f4ec"/>')
        for open_day in market_dates(market):
            mx = x_for(open_day, year_start, year_days)
            parts.append(f'<rect x="{mx:.1f}" y="{y + 3}" width="2.6" height="10" '
                         f'fill="{color}"/>')

    parts.append("</svg>")
    return "\n".join(parts)


def render_market(market):
    name = html.escape(market["name"])
    badges = ""
    if market["accepts_link"]:
        badges += '<span class="badge">Accepts Link</span>'
    if market["community_partner"]:
        badges += '<span class="badge partner">Community partner</span>'
    address = html.escape(market["address"]) or "Address not listed"
    hours = html.escape(market["hours"])
    season = html.escape(season_text(market))
    return f"""      <div class="market">
        <div class="name">{name}{badges}</div>
        <div class="detail">{address} &middot; {hours}</div>
        <div class="season">{season}</div>
      </div>"""


def render_report(data):
    records = data["markets"]
    markets = unique_markets(records)
    counts = day_counts(records)
    year = data["season"]

    total_days = sum(len(market_dates(m)) for m in markets)
    link_markets = sum(1 for m in markets if m["accepts_link"])

    count_rows = "\n".join(
        f"      <tr><td>{day}</td><td>{counts[day]}</td></tr>"
        for day in DAYS if counts[day]
    )

    by_day = []
    for day in DAYS:
        entries = [m for m in markets if m["day"] == day]
        if not entries:
            continue
        listed = "\n".join(render_market(m) for m in sorted(entries, key=lambda m: m["name"]))
        label = "market" if counts[day] == 1 else "markets"
        by_day.append(
            f'    <h3>{day} &mdash; {counts[day]} {label}</h3>\n{listed}'
        )

    chart = render_chart(markets, year)
    source = html.escape(data["source"])
    source_url = html.escape(data["source_url"])

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Chicago Farmers Markets {year}</title>
<style>{STYLES}</style>
</head>
<body>
  <header>
    <h1>Chicago Farmers Markets {year}</h1>
    <p class="meta">Source: {source}<br>
      <a href="{source_url}">{source_url}</a> &middot; retrieved {data["retrieved"]}</p>
  </header>

  <div class="stats">
    <div class="stat"><span class="n">{len(markets)}</span><span class="l">Markets</span></div>
    <div class="stat"><span class="n">{total_days}</span><span class="l">Market days in {year}</span></div>
    <div class="stat"><span class="n">{link_markets}</span><span class="l">Accept Link (SNAP)</span></div>
  </div>

  <h2>Markets by day of week</h2>
  <table class="daycount">
    <tr><th>Day</th><th>Markets</th></tr>
{count_rows}
  </table>

  <h2>When each market is open</h2>
  <div class="chartwrap">
{chart}
  </div>
  <p class="legend">
    <i style="background:{LINK_COLOR}"></i>Accepts Link (SNAP)
    <i style="background:{PLAIN_COLOR}"></i>Does not accept Link
  </p>

  <h2>All markets</h2>
{chr(10).join(by_day)}

  <footer>Generated from data/markets.json by build_report.py.</footer>
</body>
</html>
"""


def main():
    data = load_data()
    OUTPUT_FILE.write_text(render_report(data), encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE} ({len(data['markets'])} market schedules)")


if __name__ == "__main__":
    main()
