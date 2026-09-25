/**
 * CityPulse backend — civic data fusion API (hackathon reference implementation)
 * ---------------------------------------------------------------------------
 * What this file demonstrates (mapped to the problem statement):
 *   1. Ingest 3+ distinct feed types (weather, traffic, transit, AQI, power, citizen reports)
 *   2. Normalize them into ONE common schema (see normalize() below)
 *   3. Run a basic anomaly + correlation pass over the normalized window
 *   4. Serve a live JSON feed + a plain-language summary for the frontend
 *   5. Store and corroborate citizen reports (no personal identifiers kept)
 *   6. Show where real APIs plug in for production (see "REAL DATA SOURCES")
 *
 * Run:
 *   cd backend && npm install && npm start
 *   -> http://localhost:4000/api/feed/Chennai
 *   -> http://localhost:4000/api/reports/Chennai
 *   -> http://localhost:4000/api/news/Chennai
 */
const express = require("express");
const cors = require("cors");
const app = express();
app.use(cors());
app.use(express.json());

/* ---------------------------------------------------------------------- */
/* 1. RAW FEED SIMULATORS — swap each of these for a real fetch() call.   */
/*    They deliberately return DIFFERENT shapes/units, exactly like real  */
/*    civic feeds would, to demonstrate the normalization step below.     */
/* ---------------------------------------------------------------------- */

// REAL DATA SOURCES (production wiring points):
//  - Weather / cyclone: IMD Mausam API (mausam.imd.gov.in), OpenWeatherMap "onecall" + alerts
//  - Flood / disaster bulletins: NDMA SACHET Common Alerting Protocol (CAP) feed, sachet.ndma.gov.in
//  - Air quality: CPCB / data.gov.in AQI Bhuvan API
//  - News: NewsAPI.org (`/v2/everything?q=<city> flood OR cyclone OR gas leak&language=en`), or GDELT
//  - Traffic/transit: city transit GTFS-realtime feeds, or Google/HERE traffic APIs
// Each requires an API key — set as an environment variable, never hard-coded:
//   process.env.OPENWEATHER_API_KEY, process.env.NEWS_API_KEY, process.env.AQI_API_KEY

function rawWeatherFeed(city) {
  // shape: {rain_mm, wind_kmph, alert}
  return { rain_mm: Math.round(Math.random() * 90), wind_kmph: Math.round(Math.random() * 60), alert: Math.random() > 0.85 ? "heavy_rain_warning" : null };
}
function rawTrafficFeed(city) {
  // shape: {congestion_pct, incidents:[{type, lat, lng}]}
  const incidents = [];
  if (Math.random() > 0.8) incidents.push({ type: "accident" });
  if (Math.random() > 0.9) incidents.push({ type: "signal_fault" });
  return { congestion_pct: Math.round(Math.random() * 100), incidents };
}
function rawTransitFeed(city) {
  // shape: {avg_delay_min, cancellations}
  return { avg_delay_min: Math.round(Math.random() * 25), cancellations: Math.random() > 0.9 ? 1 : 0 };
}
function rawAqiFeed(city) {
  // shape: {aqi}
  return { aqi: Math.round(40 + Math.random() * 260) };
}
function rawPowerFeed(city) {
  // shape: {grid_load_pct, fault_reported}
  return { grid_load_pct: Math.round(Math.random() * 100), fault_reported: Math.random() > 0.9 };
}

/* ---------------------------------------------------------------------- */
/* 2. NORMALIZATION — every feed becomes {type, value, unit, severity,    */
/*    zone, city, timestamp, source} so anomaly detection never needs to  */
/*    know each feed's original shape.                                   */
/* ---------------------------------------------------------------------- */
function severityFromValue(value, watch, critical) {
  if (value >= critical) return "critical";
  if (value >= watch) return "watch";
  return "normal";
}
function normalize(city) {
  const w = rawWeatherFeed(city), tr = rawTrafficFeed(city), tn = rawTransitFeed(city), aq = rawAqiFeed(city), pw = rawPowerFeed(city);
  const now = new Date().toISOString();
  const readings = [
    { type: "weather", value: w.rain_mm, unit: "mm", severity: severityFromValue(w.rain_mm, 40, 70), city, timestamp: now, source: "weather-feed" },
    { type: "traffic", value: tr.congestion_pct, unit: "%", severity: severityFromValue(tr.congestion_pct, 55, 80), city, timestamp: now, source: "traffic-feed" },
    { type: "transit", value: tn.avg_delay_min, unit: "min", severity: severityFromValue(tn.avg_delay_min, 10, 18), city, timestamp: now, source: "transit-feed" },
    { type: "aqi", value: aq.aqi, unit: "AQI", severity: severityFromValue(aq.aqi, 150, 250), city, timestamp: now, source: "aqi-feed" },
    { type: "power", value: pw.grid_load_pct, unit: "%", severity: severityFromValue(pw.grid_load_pct, 65, 85), city, timestamp: now, source: "power-feed" },
  ];
  if (w.alert) readings.push({ type: "weather_alert", value: 1, unit: "flag", severity: "critical", city, timestamp: now, source: "weather-feed" });
  if (pw.fault_reported) readings.push({ type: "power_fault", value: 1, unit: "flag", severity: "critical", city, timestamp: now, source: "power-feed" });
  tr.incidents.forEach(i => readings.push({ type: i.type, value: 1, unit: "flag", severity: "watch", city, timestamp: now, source: "traffic-feed" }));
  return readings;
}

/* ---------------------------------------------------------------------- */
/* 3. ANOMALY + CORRELATION — rolling window per city, flags when 2+      */
/*    independent signal types are "watch" or worse at the same time.     */
/* ---------------------------------------------------------------------- */
const WINDOW = {}; // { city: [ {readings, timestamp} ] }, capped rolling window
function pushWindow(city, readings) {
  WINDOW[city] = WINDOW[city] || [];
  WINDOW[city].push({ readings, timestamp: Date.now() });
  if (WINDOW[city].length > 12) WINDOW[city].shift(); // keep last 12 snapshots
}
function correlate(city, readings) {
  const elevated = readings.filter(r => r.severity !== "normal");
  const distinctTypes = new Set(elevated.map(r => r.type));
  const correlated = distinctTypes.size >= 2;
  return {
    elevatedCount: elevated.length,
    distinctSignalTypes: [...distinctTypes],
    correlated,
    confidence: Math.min(100, Math.round((distinctTypes.size / 5) * 100)),
  };
}
function plainLanguageSummary(city, readings, correlation) {
  if (!correlation.correlated) return `${city} is reading normal across monitored civic signals right now.`;
  const list = correlation.distinctSignalTypes.join(", ");
  return `${city} shows correlated movement across ${correlation.distinctSignalTypes.length} signal types (${list}) — confidence ${correlation.confidence}%. This is a possible link based on the current window, not a confirmed cause.`;
}

/* ---------------------------------------------------------------------- */
/* 4. ROUTES                                                              */
/* ---------------------------------------------------------------------- */
app.get("/api/feed/:city", (req, res) => {
  const city = req.params.city;
  const readings = normalize(city);
  pushWindow(city, readings);
  const correlation = correlate(city, readings);
  res.json({
    city,
    generatedAt: new Date().toISOString(),
    readings,
    correlation,
    summary: plainLanguageSummary(city, readings, correlation),
  });
});

app.get("/api/history/:city", (req, res) => {
  res.json({ city: req.params.city, window: WINDOW[req.params.city] || [] });
});

// India-wide hazard / news bulletins.
// LIVE when NEWS_API_KEY is set (uses NewsAPI.org's /v2/everything, filtered
// by city + hazard keywords). Falls back to a clearly-labeled simulated
// bulletin when no key is set or the live call fails — this is the
// "degrade gracefully" requirement from the problem statement in action,
// not just a placeholder.
//
// Get a free key at https://newsapi.org/register (dev-tier keys work from
// localhost; for a deployed domain you'd need a paid plan, or swap in
// GNews.io — https://gnews.io — which has a more generous free tier for
// small live domains). Set it before starting the server:
//   NEWS_API_KEY=your_key_here npm start
const NEWS_CACHE = {}; // { city: {items, fetchedAt} } — avoid hammering the API on every poll
const NEWS_CACHE_MS = 5 * 60 * 1000; // 5 minutes
const HAZARD_KEYWORDS = "flood OR cyclone OR waterlogging OR \"gas leak\" OR \"power outage\" OR landslide OR heatwave";
const SEVERITY_KEYWORDS = {
  critical: ["cyclone", "flood", "gas leak", "landslide", "evacuat", "casualt", "death"],
  watch: ["outage", "waterlogg", "closure", "advisory", "heatwave", "disruption"],
};
function guessSeverity(text) {
  const lower = text.toLowerCase();
  if (SEVERITY_KEYWORDS.critical.some(k => lower.includes(k))) return "critical";
  if (SEVERITY_KEYWORDS.watch.some(k => lower.includes(k))) return "watch";
  return "normal";
}
async function fetchLiveNews(city) {
  const key = process.env.NEWS_API_KEY;
  if (!key) return null; // no key configured -> caller falls back to simulated
  const cached = NEWS_CACHE[city];
  if (cached && Date.now() - cached.fetchedAt < NEWS_CACHE_MS) return cached.items;
  const url = `https://newsapi.org/v2/everything?q=${encodeURIComponent(`"${city}" AND (${HAZARD_KEYWORDS})`)}&language=en&sortBy=publishedAt&pageSize=8&apiKey=${key}`;
  const r = await fetch(url); // Node 18+ has a global fetch; no extra dependency needed
  if (!r.ok) throw new Error(`NewsAPI responded ${r.status}`);
  const data = await r.json();
  const items = (data.articles || []).map(a => ({
    title: a.title,
    source: a.source?.name || "News",
    body: a.description || "",
    url: a.url,
    time: new Date(a.publishedAt).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    badge: guessSeverity(`${a.title} ${a.description || ""}`),
  }));
  NEWS_CACHE[city] = { items, fetchedAt: Date.now() };
  return items;
}
app.get("/api/news/:city", async (req, res) => {
  const city = req.params.city;
  try {
    const liveItems = await fetchLiveNews(city);
    if (liveItems) return res.json({ city, simulated: false, source: "NewsAPI.org", items: liveItems });
  } catch (err) {
    console.error(`live news fetch failed for ${city}:`, err.message);
    // fall through to simulated response below
  }
  res.json({
    city,
    simulated: true,
    note: process.env.NEWS_API_KEY
      ? "Live fetch failed this cycle (rate limit, network, or bad response) — showing a fallback bulletin."
      : "No NEWS_API_KEY set — showing a fallback bulletin. See the comment above this route for how to go live.",
    items: [
      { title: `No live bulletins fetched for ${city} this cycle`, source: "CityPulse backend", body: "The dashboard is still showing its own signal-derived hazard cards — this endpoint only adds real news headlines on top.", badge: "normal", time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }) },
    ],
  });
});

/* ---------------------------------------------------------------------- */
/* 5. CITIZEN REPORTS — in-memory store (swap for a real DB in production)*/
/*    No names, phone numbers or precise personal identifiers are stored. */
/* ---------------------------------------------------------------------- */
let REPORTS = []; // {id, city, zone, type, desc, time, confirmations}

app.get("/api/reports/:city", (req, res) => {
  res.json(REPORTS.filter(r => r.city === req.params.city));
});

app.post("/api/reports", (req, res) => {
  const { city, zone, type, desc } = req.body || {};
  if (!city || !zone || !type) return res.status(400).json({ error: "city, zone and type are required" });
  const report = {
    id: `r${Date.now()}${Math.floor(Math.random() * 999)}`,
    city, zone, type,
    desc: (desc || "").slice(0, 240),
    time: Date.now(),
    confirmations: 0,
    status: "unverified",
  };
  REPORTS.push(report);
  res.status(201).json(report);
});

app.post("/api/reports/:id/confirm", (req, res) => {
  const report = REPORTS.find(r => r.id === req.params.id);
  if (!report) return res.status(404).json({ error: "not found" });
  report.confirmations += 1;
  report.status = report.confirmations >= 5 ? "verified" : report.confirmations >= 2 ? "corroborated" : "unverified";
  res.json(report);
});

app.get("/api/health", (req, res) => res.json({ ok: true, time: new Date().toISOString() }));
// Python AI Intelligence Bridge
app.get("/api/intelligence/:city", async (req, res) => {
  try {
    const response = await fetch("http://localhost:5000/api/citypulse");

    if (!response.ok) {
      throw new Error(`Python API returned ${response.status}`);
    }

    const intelligence = await response.json();

    res.json({
      success: true,
      city: req.params.city,
      intelligence
    });

  } catch (error) {
    console.error("Python Intelligence API unavailable:", error.message);

    res.status(503).json({
      success: false,
      error: "Python intelligence engine unavailable"
    });
  }
});

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => console.log(`CityPulse backend listening on http://localhost:${PORT}`));
