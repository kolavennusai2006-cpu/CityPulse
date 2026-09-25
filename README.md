# CityPulse — Civic Intelligence OS

A citizen-first live city companion for the "CityPulse: The Live Civic Health Dashboard" hackathon track. One glance tells a resident what's happening around them, what to do about it, and why — grounded in fused, normalized civic signals rather than a single raw number.

## Run it

**Frontend (no build step needed):**
```
cd citypulse
python3 -m http.server 8080     # or any static server
# open http://localhost:8080
```
You can also just double-click `index.html` — everything runs client-side with simulated-but-realistic data across 24 Indian cities.

**Backend (optional, for judges who want to see the data-fusion API separately):**
```
cd citypulse/backend
npm install
npm start
# GET  http://localhost:4000/api/feed/Chennai
# GET  http://localhost:4000/api/reports/Chennai
# POST http://localhost:4000/api/reports
```
The frontend currently runs fully standalone (it generates its own deterministic simulated feed so the demo never breaks mid-pitch). Point `script.js`'s data functions at the backend's `/api/feed/:city` route when you're ready to demo the two connected — the response shapes already match.

## How this maps to the problem statement

| Requirement | Where it lives |
|---|---|
| Ingest 3+ distinct data types | `backend/server.js` normalizes weather, traffic, transit, AQI and power feeds (5 types); frontend adds citizen reports and hazard bulletins as two more |
| Normalize into a common schema | `normalize()` in `server.js`; `buildCityData()` / `buildIncidents()` in `script.js` |
| Detect anomalies/correlations | `correlate()` in `server.js`; `anomaly` flag + convergence/confidence scoring in `script.js` |
| Live, glanceable dashboard | Hero status, priority alert, zone grid, live incident map |
| Plain-language summary | "Civic brief" section + `plainLanguageSummary()` / `answerQuestion()` |
| Optional: alerting | Browser notifications + the flashing critical-incident banner |
| Optional: historical replay | "Historical risk profile" section with a year-by-year chart and a step-through replay of past events |
| Degrade gracefully | "Data source status" strip simulates a feed going degraded and falling back to last-known data |
| Epistemic honesty | Every correlation is labeled "possible link, not confirmed cause" in the UI copy |

## Feature tour

- **Hero + Priority Alert** — the single highest-risk zone right now, with its dominant signals and a 15-minute forecast.
- **Avoid right now** — a fast-scan list of zones and roads to steer clear of, with the reason (waterlogging, signal down, closure…).
- **Today's advisory / "What should I carry"-style tips** — plain-language, generated only from currently elevated signals.
- **India hazard watch** — news-style cards for cyclone watches, flood warnings, gas leaks and power-cut risk. Renders instantly from the local signal-derived feed, then tries the backend for **real** live headlines (NewsAPI.org, filtered by city + hazard keywords) and swaps them in — with a 🟢 LIVE / ⚪ Simulated tag so it's always clear which you're looking at. If the backend isn't running or no key is set, it falls back to the simulated bulletin automatically (see "Live news setup" below).
- **Plan your route** — Dijkstra over a per-city road graph, avoiding segments closed by rain-related risk or a critical zone.
- **Choose your view** — the same underlying data, reframed for a resident, a business owner, a city official, emergency response, or a journalist.
- **Is it safe right now?** — one-tap plain verdict per zone, with text-to-speech.
- **Report something** — citizen reporting (waterlogging, road damage, accident, power outage, gas leak, transit, signal down, fallen tree, gathering, garbage, streetlight, other), optional photo, and neighbour confirmations that upgrade a report from Unverified → Corroborated → Verified. No names or personal identifiers are collected.
- **Live incident map** — an interactive, zoomable SVG map per city: click a zone or an incident marker for full detail. No external map tiles or API key required, so it always renders in a locked-down demo environment.
- **Historical risk profile** — a 5-year reference dataset per zone (floods, cyclones, accidents, power cuts) plus a step-through "replay" of past significant events, so judges can see the pattern-detection story even without a live multi-day dataset.
- **Ask CityPulse** — answers are computed live from the current in-memory feed state (not an LLM hallucinating numbers) — every figure it cites is one you can also see elsewhere on the page.
- **What-if simulation** — drag signal sliders and recompute risk instantly, to demonstrate the scoring formula transparently.

## Live news setup (already wired, just needs a key)

The news panel is **not just a stub** — `backend/server.js`'s `/api/news/:city` route makes a real call to NewsAPI.org, filters for hazard keywords (flood, cyclone, waterlogging, gas leak, power outage, landslide, heatwave) plus the city name, tags each headline's severity, and caches results for 5 minutes so you don't burn your API quota on every poll.

To go live:
1. Get a free key at **https://newsapi.org/register** (the free "Developer" tier works from `localhost`, which is exactly what you want for a hackathon demo — a deployed public domain needs a paid plan or a swap to **GNews.io**, which has a friendlier free tier for small live sites).
2. Run the backend with the key set:
   ```
   cd backend
   NEWS_API_KEY=your_key_here npm start
   ```
3. In `script.js`, `NEWS_BACKEND_URL` is already set to `http://localhost:4000` — as soon as the backend is running with a key, refresh the page and the news cards will switch from "⚪ Simulated demo feed" to "🟢 LIVE" automatically. No key or backend not running → it silently falls back to the simulated feed, so the frontend never breaks or blocks on the network (this is the "degrade gracefully" requirement in action, not just a placeholder).
4. Deploying the backend somewhere other than `localhost:4000`? Update `NEWS_BACKEND_URL` at the top of the "India hazard watch" section in `script.js` to match.

## Wiring in the rest of the real data (post-hackathon)

The remaining simulated pieces are isolated so they're a clean swap too:

1. **Weather / cyclone** — IMD Mausam API or OpenWeatherMap "onecall" + alerts.
2. **Flood / disaster bulletins** — NDMA's SACHET Common Alerting Protocol feed (sachet.ndma.gov.in).
3. **Air quality** — CPCB / data.gov.in AQI API.
4. **Traffic/transit** — city GTFS-realtime feeds, or a commercial traffic API.

Every one of these needs an API key — keep them as environment variables (`OPENWEATHER_API_KEY`, `AQI_API_KEY`, etc.), never hard-coded, and never commit them.

## Files

```
citypulse/
├── index.html          # markup + section layout
├── style.css            # dark civic-ops visual theme
├── script.js            # simulation engine, rendering, map, reporting, historical replay
├── backend/
│   ├── server.js         # Express API: normalization, anomaly/correlation, reports, news stub
│   └── package.json
└── README.md
```
