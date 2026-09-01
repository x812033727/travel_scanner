# Travel hotspot intelligence

Travel Scanner maintains a searchable, time-stamped popularity signal for attractions in its
supported destinations. The ranking is a planning hint, not a live crowd or safety forecast.

## Source policy

| Source | Role | Stored data | Status |
| --- | --- | --- | --- |
| Travel Scanner curated catalog | Stable attraction identity, aliases, city, category, coordinates and cold-start relevance | Catalog fields and an explicitly estimated seed signal | Enabled |
| [Wikimedia Analytics API](https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/) | Recent public interest | 30-day aggregate pageviews, previous 30-day aggregate, observation date and source URL | Enabled by default |
| [Google Places API](https://developers.google.com/maps/documentation/places/web-service) | Place identity, map entry, address, opening hours, Plus Code and official-site candidate | Place ID is retained; normalized Places content is cached for no more than 30 days with attribution | Enabled only when a server-side key is configured |
| [Reddit Data API](https://redditinc.com/policies/data-api-terms) | Possible future discussion-volume aggregate | Nothing until the intended commercial use has an applicable agreement | Disabled |

Wikimedia aggregate data is CC0. Requests identify Travel Scanner through a configurable User-Agent
and run sequentially. The collector stores no article text or reader identity.

Do not add scraped TripAdvisor, Dcard, PTT, Instagram, TikTok or Reddit content as a production
source without a documented API contract, retention policy and commercial-use review. Prefer
aggregate counters over post or review bodies.

## Ranking formula

Every collection creates global, legacy city-code, and stable `destination_id` snapshots. Scores are scoped:
a score of 80 in Tokyo is comparable within that Tokyo snapshot, not an absolute measure of global
visitor volume.

The 0-100 score uses:

- 45% recent interest: log-normalized pageviews over the latest complete 30-day window.
- 25% growth: change from the preceding 30-day window; no change is 50 points.
- 20% quality: the maintained editorial relevance used for cold-start stability.
- 10% confidence: 80 with a current Wikimedia signal, 35 for curated-only cold start.

Items without a collected trend remain visible but are returned with `is_estimate=true`. API
responses expose the component scores, sources, signal date and whether the result is estimated.

## Collection and operations

`hotspot-collector` runs once on startup and then at
`HOTSPOT_COLLECTION_INTERVAL_SECONDS` (six hours by default). Daily Wikimedia observations are
idempotent, so multiple runs refresh the same dated signal and ranking snapshot.

The checked-in cold-start catalog contains 450 reviewed attractions across 31 destinations. The
12 secondary destinations contribute exactly 180 entries (10 general and five deep-travel places
each). Weekly Wikipedia/Wikidata discovery can fill each new destination to 18 public places, for
a complete target of 529. Discovered candidates never receive a deep-travel designation without
an administrator review.

In `docker-compose.prod.yml` the collector sits behind the `hotspots` compose profile, so it is
opt-in — it reaches out to the Wikimedia API on a schedule, which not every deployment wants. Start
it alongside the rest of the stack with:

```bash
docker compose -f docker-compose.prod.yml --profile hotspots up -d
```

Without the profile the other services start as usual and the hotspot API surfaces keep serving the
curated catalog and whatever signals were collected previously.

Run a collection manually:

```bash
cd apps/api
uv run python -m app.cli collect-hotspots
```

Relevant settings:

- `HOTSPOT_COLLECTION_ENABLED`
- `HOTSPOT_COLLECTION_INTERVAL_SECONDS`
- `HOTSPOT_WIKIMEDIA_ENABLED`
- `HOTSPOT_WIKIMEDIA_USER_AGENT`
- `HOTSPOT_WIKIMEDIA_TIMEOUT_SECONDS`
- `HOTSPOT_PLACE_ENRICHMENT_ENABLED`
- `HOTSPOT_PLACE_REFRESH_AFTER_DAYS` (21 by default)
- `HOTSPOT_PLACE_CACHE_DAYS` (30 by default)
- `HOTSPOT_PLACE_REFRESH_BATCH_SIZE` (20 per collector run by default)

### Google place enrichment

Google place enrichment runs on the dedicated `hotspot-places` RQ queue in chunks of 25. An
administrator must confirm the estimated request count before starting an all-country, single-country,
or selected-hotspot run. Missing Place IDs first use a locate-only text search and retain at most three
candidates; Place Details then fetches the normalized display fields. Existing Place IDs are treated as
legacy locked identities and seed reconciliation never clears them.

Exact alias/country matches within 5 km and fuzzy matches of at least 0.90 with matching city/country
within 1.5 km may be approved automatically. Everything else remains pending for an administrator.
Google website candidates are only published automatically when they are public HTTPS URLs and are not
social, booking, ticketing, or review-aggregation sites. A manually approved official URL always wins.

Provider fields become eligible for refresh after 21 days and expire after 30 days. A failed refresh
keeps the previous cache visible only until its original expiry; expired provider fields are not returned
by the public endpoint. Automatic refresh pauses when either the Place Details Enterprise or Text Search
Pro usage reaches 90% of its configured monthly free threshold. If `GOOGLE_MAPS_API_KEY` is absent, no
queue work is started and the UI reports the integration as unavailable—there is no fixture or browser
scraping fallback in production.

## API surfaces

- `GET /api/v1/destinations`: the canonical destination directory, including role, parent,
  gateways, lodging areas and recommended days.
- `GET /api/v1/hotspots/rankings`: searchable ranking with stable `destination_id`, legacy
  `city_code`, role, country, category, style and cursor filters.
- `GET /api/v1/hotspots/facets`: dynamic country, destination, category and travel-style counts.
- `GET /api/v1/hotspots/sources`: public source purpose, persistence and readiness status.
- `GET /api/v1/hotspots/{id}/place`: policy-aware current place details, field sources,
  freshness and Google attribution.
- `GET /api/v1/hotspots/for-planner`: compact, source-labelled candidates for the itinerary
  planner. It accepts `destination_id` or legacy `city_code`, comma-separated `interests`, trip
  days and explicitly selected extension destinations.

Eight secondary destinations are searchable for flights and lodging: Taichung, Kaohsiung,
Sendai, Kanazawa, Hiroshima, Daegu, Chiang Rai and Da Lat. Tainan, Gyeongju, Jeonju and Hue are
extension destinations only; they keep independent attraction rankings but are added through
Kaohsiung, Busan, Seoul and Da Nang respectively. Trips of 1–3 days do not include extension
cities, 4–6 day trips allow one, and trips of at least seven days allow two.

The ranking response includes a lightweight `place_summary`; full place data stays on the detail endpoint.
The planner endpoint supplies candidates only. Opening hours, route feasibility, trip dates,
traveler interests and explicit preferences must still be applied before an itinerary is saved.
