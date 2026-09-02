# Travel hotspot intelligence

Mokaair maintains a searchable, time-stamped popularity signal for attractions in its
supported destinations. The ranking is a planning hint, not a live crowd or safety forecast.

## Source policy

| Source | Role | Stored data | Status |
| --- | --- | --- | --- |
| Mokaair curated catalog | Stable attraction identity, aliases, city, category, coordinates and cold-start relevance | Catalog fields and an explicitly estimated seed signal | Enabled |
| [Wikimedia Analytics API](https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/) | Recent public interest | 30-day aggregate pageviews, previous 30-day aggregate, observation date and source URL | Enabled by default |
| [Google Places API](https://developers.google.com/maps/documentation/places/web-service) | Place identity, map entry, address, opening hours and official-site candidate | Place ID is retained; normalized Places content is cached for no more than 30 days with attribution | Enabled only when a server-side key is configured |
| [Reddit Data API](https://redditinc.com/policies/data-api-terms) | Possible future discussion-volume aggregate | Nothing until the intended commercial use has an applicable agreement | Disabled |

Wikimedia aggregate data is CC0. Requests identify Mokaair through a configurable User-Agent
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

## Nearby dining coverage

Every approved hotspot can expose restaurant candidates within 5 or 10 km. Public results enforce
both thresholds: Google rating at least 3.8 and at least 1,000 user ratings. The default Bayesian
recommendation sort balances rating and review volume; explicit rating, review-count and distance
sorts remain available. Only the versioned formula and constants are durable: each restaurant's
score is derived from the live response and is neither cached nor used as a historical rating.

The first request uses Places Nearby Search for a fast result. The `restaurant-scans` RQ queue builds
broader 10 km coverage with Places Aggregate API cells: a cell with more than 100 results is split
into seven overlapping half-radius circles until every returned Place ID set is complete or the
configured depth/budget is reached. Each discovered ID is then checked against live Place Details;
only IDs simultaneously meeting the 3.8 rating and 1,000-review thresholds become public hotspot
relationships. The six-hour hotspot collector queues at most one missing or stale hotspot per cycle,
and administrators can also start scans from the hotspot review page.

Google display content is not treated as application-owned data. The database retains durable Place
IDs, hotspot relationships, Place-ID-only scan progress and a free standard Maps URL generated by
Mokaair from each Place ID. Rating, review count, name, hours, official website,
Google-returned Maps URI and derived recommendation score are fetched or calculated live and are not
persisted. Coordinates are the only display values cached: they live in Redis with an enforced
configurable TTL of at most 30 days and are never written to the database. Each response includes
Google attribution, provider observation time and this persistence policy. Google Maps short links
are not stored; if no live Maps URI is available, the UI uses the generated standard Maps URL.

Monthly fail-closed request budgets are independently configurable for Aggregate, Nearby and live
Place Details requests. The defaults stop at 80% of the published free usage caps; the Details
guard counts the shared Place Details SKU, including non-restaurant calls, so another feature cannot
silently consume the reserved buffer. Sorting an already loaded result is client-side and sends no
new provider request. The admin coverage panel shows feature calls, whole-SKU usage, safety-budget
remaining and the app-observed Google SKU free tiers. Google Cloud Billing remains the billing
authority, particularly when the same credential is used outside this deployment.

Relevant API surfaces:

- `POST /api/v1/hotspots/{hotspot_id}/restaurant-searches` with radius, sort and cursor.
- `POST /api/v1/admin/hotspots/restaurants/scans` to queue selected or missing coverage.
- `GET /api/v1/admin/hotspots/restaurants/coverage` for progress and quota disclosure.
- `PATCH /api/v1/admin/hotspots/restaurants/places/{place_id}` for policy/admin suppression.
