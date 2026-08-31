# Travel hotspot intelligence

Travel Scanner maintains a searchable, time-stamped popularity signal for attractions in its
supported destinations. The ranking is a planning hint, not a live crowd or safety forecast.

## Source policy

| Source | Role | Stored data | Status |
| --- | --- | --- | --- |
| Travel Scanner curated catalog | Stable attraction identity, aliases, city, category, coordinates and cold-start relevance | Catalog fields and an explicitly estimated seed signal | Enabled |
| [Wikimedia Analytics API](https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/) | Recent public interest | 30-day aggregate pageviews, previous 30-day aggregate, observation date and source URL | Enabled by default |
| [Google Places API](https://developers.google.com/maps/documentation/places/web-service) | On-demand place lookup and display | Only the Place ID may be retained indefinitely; Places content is not persisted into rankings | Existing on-demand integration |
| [Reddit Data API](https://redditinc.com/policies/data-api-terms) | Possible future discussion-volume aggregate | Nothing until the intended commercial use has an applicable agreement | Disabled |

Wikimedia aggregate data is CC0. Requests identify Travel Scanner through a configurable User-Agent
and run sequentially. The collector stores no article text or reader identity.

Do not add scraped TripAdvisor, Dcard, PTT, Instagram, TikTok or Reddit content as a production
source without a documented API contract, retention policy and commercial-use review. Prefer
aggregate counters over post or review bodies.

## Ranking formula

Every collection creates both a global snapshot and one snapshot for each city. Scores are scoped:
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

## API surfaces

- `GET /api/v1/hotspots/rankings`: searchable ranking; filters are `q`, `city_code`, `category`
  and `limit`.
- `GET /api/v1/hotspots/sources`: public source purpose, persistence and readiness status.
- `GET /api/v1/hotspots/for-planner`: compact, source-labelled candidates for the itinerary
  planner. It accepts `city_code`, comma-separated `interests` and `limit`.

The planner endpoint supplies candidates only. Opening hours, route feasibility, trip dates,
traveler interests and explicit preferences must still be applied before an itinerary is saved.
