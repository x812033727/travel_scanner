# Travel Scanner

Travel Scanner is a mock-first, API-first travel comparison MVP. It combines
flights, hotels, activities, and transportation into complete trip plans and
explains the trade-off between the cheapest, balanced, and comfortable choices.

Trip search supports an explicit mock development mode, an Amadeus-backed test
or live mode, Skyscanner Flights Live Prices, and Duffel Offer Requests for
approved partners. FlightAware supplies status rather than fares, while Google
Travel Impact Model supplies a consistent per-passenger emissions figure.
Production never falls back to mock or supplier test prices when credentials are
absent. The experimental airline crawler remains a separate, non-bookable
public-fare research surface.

## Architecture and project structure

- `apps/web`: Next.js App Router frontend and same-origin BFF
- `apps/api`: FastAPI modular monolith, RQ worker, models, migrations, tests
- `architecture.md`: boundaries and data flow
- `docker-compose.yml`: API, worker, PostgreSQL, and Redis

## Local development

Copy `.env.example` to `.env`, then run infrastructure and API. Compose runs
`alembic upgrade head` in a one-shot migration service before API and worker
startup, and `/ready` remains unavailable when the database revision is stale:

```bash
docker compose up --build postgres redis migrate api worker
```

Run the frontend separately:

```bash
npm install
npm run dev:web
```

Open `http://localhost:3000`; API docs are at `http://localhost:8000/docs`.

Create an account in the UI to receive three free, non-expiring uses. To grant a
usage pack locally before online checkout is available:

```bash
cd apps/api
uv run python -m app.cli add-usage-package --email you@example.com \
  --package PACK_30 --reference local-test-001
```

## Administration

After applying the database migration, grant an existing account administrator
access and open `http://localhost:3000/admin/users` or
`http://localhost:3000/admin/settings`:

```bash
cd apps/api
uv run python -m app.cli set-admin --email you@example.com
```

Use `--revoke` to remove the database role. `ADMIN_EMAILS` is also accepted as a
comma-separated bootstrap or recovery allowlist; remove the address from that
environment value before revoking its access. The header only exposes the
administration link to administrator accounts, and every administration API
still enforces the role server-side.

The member page searches and paginates accounts, shows available and reserved
uses, activates or suspends accounts, and grants or revokes database-backed
administrator access. Administrators cannot suspend or demote their own active
session, while `ADMIN_EMAILS` roles must be removed from the host environment.
Manual usage changes require a reason and an idempotency key. Every change is a
new `usage_ledger` entry plus an administrator audit event; deductions cannot
reduce the balance below in-flight reservations. Database-backed administrators
cannot adjust their own balance, so a second administrator must authorize that
operation. Administrators whose email is currently listed in `ADMIN_EMAILS` may
increase or deduct their own balance, including accounts that also hold the
database-backed role; these self-adjustments use the same ledger, audit, and
reserved-balance safeguards.

The page manages runtime modes, timeouts and encrypted credentials for Google
Maps, Amadeus, Skyscanner, Duffel, FlightAware, Google Travel Impact, and NAVITIME.
It also shows each provider's last-24-hour request and failure counts. Changes take effect for API and worker
requests without rebuilding the web image. Connection checks and configuration
changes are recorded in `admin_audit_logs`, without secret values. Responses
only include whether a key exists, its source, and a masked suffix.

Set a stable, randomly generated `SETTINGS_ENCRYPTION_KEY` in production before
saving credentials. It is used to derive the Fernet key for database values;
changing it makes existing encrypted settings unreadable. `APP_SECRET_KEY` is
only a backwards-compatible fallback. Restrict the Google server key by API and
server egress IP. Restrict the browser Embed key by API and the production HTTP
referrer. Do not commit either value.

The management APIs are under `/api/v1/admin/users` and
`/api/v1/admin/provider-settings`; the safe runtime browser configuration is served separately from
`/api/v1/runtime/public-config`. Environment variables remain the fallback when
no database override exists, and disabling a provider never silently enables
mock pricing in production.

## Database migration

```bash
cd apps/api
uv sync
uv run alembic upgrade head
```

## Quality checks

```bash
cd apps/api
uv run ruff check .
uv run mypy app
uv run pytest

cd ../..
npm run lint:web
npm run typecheck:web
npm run test:web
npm run build:web
npm run test:e2e --workspace @travel-scanner/web
```

CI also runs an unmocked first-party smoke journey with PostgreSQL, Redis, the
FastAPI service, RQ worker, and Next.js running together. Only the external
travel provider is pinned to deterministic mock mode. The journey runs in
desktop Chromium and a Pixel 7 viewport and covers guest recommendations,
safe sign-in return, progressive search, saving a trip, and full price-alert
management.

Further sections below document providers, usage packs, orchestration, and
optimization as those modules are introduced.

## Usage packs and audit history

Registration grants three uses. The inactive-checkout catalog contains 10 uses
for NT$199, 30 for NT$499, and 100 for NT$1,299. Uses stack, never expire, and
every successful full-trip search, public-airline-fare search, back-to-back fare
comparison, or trip re-optimization costs exactly one use.

One use is reserved while work is in flight and charged only when a usable
result exists. Empty results and failures release it and create a visible
zero-charge record. The append-only PostgreSQL `usage_ledger` records grants,
charges, releases, migrations, and adjustments; the `usage_reservations` unique
key prevents duplicate charges. Members can review these records and their
reference numbers at `GET /api/v1/usage/history` and in the account page.

## Adding a provider

Implement the relevant protocol in `apps/api/app/providers/base.py`, normalize
every response into `providers/schemas.py`, then register the adapter with the
search orchestrator. Keep credentials in environment-backed settings and never
return provider-specific payloads or secrets to the client.

The built-in Mock Provider generates stable TPE/Japan examples from a hash of
the request. Every result includes `is_mock`, retrieval time, expiry time, and a
non-bookable example URL.

For provider-backed search, set `TRAVEL_PROVIDER_MODE=live` together with
`AMADEUS_CLIENT_ID`, `AMADEUS_CLIENT_SECRET`, and `AMADEUS_ENV=test` or
`production`. `GOOGLE_MAPS_API_KEY` is optional and enriches hotels, activities,
photos, opening hours, and route estimates. Secrets belong in the runtime
environment and must never be committed. `GET /api/v1/providers/status` reports
whether live, test, mock, or disabled data is active, plus the selected and
fallback provider for each search module.

Flights can be selected independently with
`FLIGHT_PROVIDER_MODE=auto|skyscanner|duffel|amadeus|mock|disabled`. With
`FLIGHT_SEARCH_STRATEGY=hybrid`, auto mode queries Skyscanner, Duffel, then
Amadeus until at least `FLIGHT_MIN_RESULT_COUNT` unique itinerary groups exist.
The user can explicitly request all remaining configured sources without another
usage charge. Mock is available only outside production; Amadeus test and Duffel
test responses are also rejected in production. Skyscanner exact-date searches use the Live Prices
create/poll flow and emit repeated `module.results` SSE batches; flexible-date
searches use Indicative Prices and never expose booking actions. Provider
session tokens and booking URLs stay server-side. Skyscanner revalidation uses
Itinerary Refresh, Amadeus uses Flight Offers Price with a private cached raw
offer, and Duffel uses Get Offer. The browser posts to
`POST /api/v1/offers/{offer_id}/clickout`, which validates ownership and expiry,
records an audit event, and responds with a secure 303 redirect.

Set `DUFFEL_ACCESS_TOKEN` and `DUFFEL_ENV=test|live` to enable Duffel. Its first
release is recheck-only and does not create orders. Set `FLIGHTAWARE_API_KEY` to
enable `/flights/status`: departures within two days use exact FlightAware status
matching, while later dates are labelled only as schedule-verified. Tracks are
loaded on demand and kept only in short Redis caches. Independent status lookups
charge once only for a new successful external result; cache hits, empty results,
failures and idempotency replays do not charge. Set
`GOOGLE_TRAVEL_IMPACT_API_KEY` for official TIM emissions. Google Flights prices
and unofficial search-result scraping are intentionally unsupported.

Hotels can be selected independently with
`HOTEL_PROVIDER_MODE=auto|booking|amadeus|mock|disabled`. In `auto` mode an
enabled Booking.com Demand API integration wins, Amadeus is the fallback, and
mock is available only outside production. Booking.com requires
`BOOKING_DEMAND_ENABLED=true`, an Affiliate ID, and a Bearer Token. It uses the
official v3.1 sandbox by default, resolves the app's IATA destination through
`/common/locations/cities` to a Booking city ID, caches that mapping in Redis, searches available
accommodations, and returns only validated HTTPS Booking.com redirect URLs.
Affiliate link settings remain separate from Demand API hotel search settings.
Technical timeouts, rate limits, and provider errors trigger one Amadeus
fallback; a valid empty response does not call a second provider.

Amadeus now sends every leg of a `multi_city` request rather than silently using
only the first route. Its offers remain recheck-only because the adapter does
not provide an approved clickout URL. The Skyscanner application checklist and
product narrative are in
[`docs/skyscanner-partnership-application.md`](docs/skyscanner-partnership-application.md).

Live Prices calls must be initiated by a user with exact dates. AI destination
discovery and scheduled price alerts do not call Skyscanner Live Prices. Public
airline-page crawlers under `/labs/airlines` remain an isolated research tool
and are never merged into bookable provider results.

`POST /api/v1/flights/back-to-back` performs the production two-trip
comparison. It issues five exact ticket searches through the selected flight
provider: two conventional returns, the initial one-way, the foreign-origin
two-leg multi-city ticket, and the final one-way. The response contains mixed-
airline and same-marketing-airline totals. Missing tickets remain missing and
produce a partial comparison; manual prices and crawler quotes are not inserted
into this live response. The legacy crawler comparison remains available only
under `/api/v1/crawlers/airlines/back-to-back-fares`.

Saved optimized plans include an editable day-by-day itinerary. Owners can
update it with optimistic version checks, rotate or revoke a secret read-only
share link, and keep provider-confirmed amounts separate from estimates.

## Itinerary and transit planning

Blank-trip creation is a four-step, option-driven flow. It stores travelers, rooms, total
budget, pace, interests, lodging types, nightly price range, hotel stars, review thresholds,
preferred area, station walking limit, breakfast/refund requirements, red-eye preference,
routing preference, and notes in the trip's existing JSON data. Optional filters always offer
an explicit "no preference" path and require no database migration.

`POST /api/v1/trips` accepts both saved search plans and `source=blank` trips.
The planner supports structured Places selections, per-day ordering, fixed
appointments, duration and notes, detailed transit steps, and read-only shared
views. Fixed-order route calculation is free. Same-day itinerary optimization
uses the existing auditable reservation flow and charges one use only after a
usable order is applied.

Google Routes is the global fallback. Set `GOOGLE_MAPS_API_KEY` for server-side
Places and Routes calls and an origin-restricted
`NEXT_PUBLIC_GOOGLE_MAPS_BROWSER_KEY` for the optional embedded planner map.
Google provider responses are kept in short-lived Redis caches; durable trip
records retain provider IDs and user-authored fields instead of raw payloads.
The administrator settings page also shows an application-side monthly request
counter for server-side Places, Routes, and photo calls. Its default budget is
10,000 requests (`GOOGLE_MAPS_MONTHLY_REQUEST_LIMIT`); browser Embed loads and
Google Cloud usage from before this counter was deployed are not included. The
bundled Redis service enables append-only persistence for these monthly counters.

Japan transit enhancement is optional. Set `NAVITIME_API_BASE_URL`,
`NAVITIME_CLIENT_ID`, and `NAVITIME_API_KEY` only after obtaining the required
commercial rights. When configured, sourced exit, platform, and recommended-car
fields are displayed. Missing details are explicitly marked unavailable and are
never inferred.

## Travel hotspot intelligence

The public `/hotspots` page searches a time-stamped attraction catalog and shows global or city
rankings for Japan, South Korea and Thailand. The scheduled `hotspot-collector` seeds stable place
identities, collects the latest and preceding 30-day Wikimedia pageview totals, and writes
explainable global and per-city ranking snapshots. Cold-start values remain visibly marked as
estimates rather than live popularity.

The API exposes `/api/v1/hotspots/rankings`, `/api/v1/hotspots/sources`, and the compact
`/api/v1/hotspots/for-planner` feed. The last endpoint is intended for AI itinerary candidate
selection; route feasibility, opening hours and traveler preferences still decide the final plan.
Google Places remains an on-demand lookup because its content cannot be persisted as a general
ranking database. Discussion sources stay disabled until the intended use has an applicable API
and retention agreement. See [`docs/hotspot-intelligence.md`](docs/hotspot-intelligence.md) for the
formula, source policy, settings and manual collection command.

## Experimental public airline fares

`POST /api/v1/crawlers/airlines/fares` reads public cached-fare pages for China
Airlines (`CI`) and STARLUX (`JX`). EVA Air (`BR`) has a complete adapter but is
fail-closed by default because its fare subdomain did not expose a readable
`robots.txt` to the crawler user-agent during implementation. Check current
source availability at `GET /api/v1/crawlers/airlines/status`.

The collector accepts airport codes, optional dates with a configurable flex
window, cabin class, airlines, and per-airline limit. It returns
`PublicFareQuote`, not `FlightOffer`: these public pages contain recently seen
round-trip prices but do not establish live inventory, exact flight numbers, or
bookability. Results therefore set `is_live=false`, `is_bookable=false`, and
`is_mock=false`, retain the official source URL, and include the source's
last-seen text when available.

The browser test surface is available at `http://localhost:3000/labs/airlines`.
It shows each adapter's current policy state before submitting an authenticated
fare query through the same-origin BFF, and keeps public cached fares clearly
separate from live, bookable inventory.

The same page also provides a complete two-trip back-to-back comparison through
`POST /api/v1/crawlers/airlines/back-to-back-fares`. It expands four ordered
dates and accepts an independent `first_destination` and `second_destination`.
When both destinations match, the request can choose two explicitly separated
strategies. `nested_round_trips` compares two conventional round trips with a
Taiwan-origin wrapper ticket and a foreign-origin reverse ticket.
`reverse_two_segment` follows the external-station two-segment pattern: one
foreign-origin round trip covers the first return and second departure, while
separate one-way tickets cover the first departure and final return. The
official China Airlines and STARLUX cached-fare pages currently publish only
round-trip rows, so the two one-way per-passenger prices are accepted as
clearly marked manual inputs (`head_one_way_fare` and `tail_one_way_fare`). A
manual `middle_two_segment_fare` can also replace a missing reverse fare.
Missing values produce an unavailable comparison instead of a fabricated half
round-trip estimate. The service still reads at most two unique public pages
per enabled airline, then reports both the cheapest mixed-airline combination
and the cheapest same-airline combination per passenger. It never suggests
skipping a coupon: every ticket must be flown in order.

Different destinations are supported for `reverse_two_segment`: the middle
manual fare represents the ordered multi-city ticket `destination A -> Taiwan
-> destination B`, while the head and tail inputs complete the first outbound
and final inbound. If either conventional public round trip is missing,
`conventional_first_fare` and `conventional_second_fare` provide clearly marked
manual fallbacks as well. `nested_round_trips` still requires a true open-jaw
provider when the destinations differ and returns
`pricing_capability=open_jaw_provider_required` rather than fabricating that
price. Legacy requests with one `destination` remain accepted and apply it to
both trips.

Foreign-origin fares retain their source currency. Frankfurter reference rates
provide a clearly labelled TWD estimate and are cached in Redis for 24 hours;
up to seven-day-old cached rates may be used with a stale warning if the rate
service is unavailable. If no conversion rate exists, raw fares remain visible
but no cross-currency savings claim is produced.

Some official public-fare pages select a different locale for foreign-origin
routes. The fetcher follows at most three redirects only when every target
remains on the same allowlisted HTTPS host and passes the runtime robots check;
cross-host redirects fail closed. When a requested date range has no cached
fare, the response uses user-facing ticket-role names and reports the nearest
date pair found in the already-fetched public page. A missing comparison is
reported as unavailable, never as `0%` savings. STARLUX public dates can be
sparse enough that a STARLUX-only four-ticket comparison is unavailable even
though both official pages were read successfully.

For pages that need a real browser runtime, the Chrome bridge asks the API for
allowlisted, robots-approved targets, opens only those targets in an isolated
Google Chrome process, parses the page's `__NEXT_DATA__` in Chrome, retains only
the allowlisted public-fare fields, and posts those rows back to the existing
Python normalizer. The API repeats the source and robots checks, rejects
captures older than 15 minutes, limits row count and payload size, and records
a SHA-256 digest. The bridge never accepts an arbitrary target URL and does not
reuse a personal Chrome profile, log in to an airline, or bypass a challenge.

Set either a short-lived API token or local Travel Scanner credentials, then
run the tool from the repository root. Credentials remain in memory; prefer
environment variables over command-line arguments.

```bash
export TRAVEL_SCANNER_TOKEN="your-short-lived-token"
npm run crawl:airlines:chrome -- \
  --origin TPE --destination NRT \
  --departure-date 2026-11-10 --return-date 2026-11-15 \
  --airlines CI,BR,JX --headed --strict \
  --output chrome-fares.json
```

On PowerShell, use `$env:TRAVEL_SCANNER_TOKEN = "..."`. Alternatively set
`TRAVEL_SCANNER_EMAIL` and `TRAVEL_SCANNER_PASSWORD`; the tool signs in through
the normal API and does not persist the returned token. Use `--channel chromium`
only when Google Chrome is unavailable. `BR` is reported as policy-disabled
until its robots policy can be verified; the Chrome path does not override it.

The bridge endpoints are `POST /api/v1/crawlers/airlines/browser-targets` and
`POST /api/v1/crawlers/airlines/browser-captures`. Both require Travel Scanner
authentication and use the normal per-user rate limit.

Safety controls include a fixed HTTPS host allowlist, runtime `robots.txt`
checks that fail closed, Redis-backed page caching and per-host throttling (with
a process-local development fallback), bounded response size, timeout, and one
transient retry. The collector never logs in, solves CAPTCHAs, or calls private
booking endpoints.

Run a fresh live contract check from the command line. `--strict` returns a
non-zero exit code when an enabled adapter cannot fetch and parse at least one
fare. Expected policy-disabled adapters are reported but do not fail the run.

```bash
cd apps/api
uv run python -m app.cli verify-airline-crawlers \
  --origin TPE --destination NRT --strict
```

The same check is available as the manually dispatched GitHub workflow
`Airline crawler live validation`. It deliberately does not run on every push:
external fare pages are volatile, while normal CI always runs deterministic
parser, robots-policy, cache, and verification-report tests.

Example authenticated request:

```bash
curl -X POST http://localhost:8000/api/v1/crawlers/airlines/fares \
  -H "Authorization: Bearer $TOKEN" \
  -H "Idempotency-Key: fare-example-001" \
  -H "Content-Type: application/json" \
  -d '{"origin":"TPE","destination":"NRT","departure_date":"2026-11-10","return_date":"2026-11-15","flex_days":7,"airlines":["CI","BR","JX"]}'
```

## Search orchestration

`POST /api/v1/searches` validates the JWT, shared feature limits, rate limit,
idempotency key, and available uses before creating an RQ job. The worker calls provider modules in
parallel; one provider failure becomes a warning instead of cancelling useful
results. Normalized offers are persisted and published through a replayable
Redis Stream exposed at `GET /api/v1/searches/{id}/events`.

## Cost and optimization

`TotalCostEngine` keeps provider-confirmed prices separate from estimates such
as local transportation. The optimizer applies hard preferences, candidate
caps, a Pareto frontier, and a bounded beam before a 500 ms OR-Tools CP-SAT
selection. The cheapest result is always the lowest feasible total; balanced
and comfortable results use documented, adjustable scoring weights.

## Guided AI search

`POST /api/v1/ai/parse-trip` uses a deterministic rules-based parser for the
MVP. It extracts constraints and reports confidence/missing fields; it never
creates prices. The home page also provides a five-step option flow for a
travel window, trip-length range, multiple countries, travelers, lodging, and
interests. Every optional preference has an explicit no-preference state;
structured choices override supplementary free text.

`POST /api/v1/destinations/discover` returns up to three deterministic,
curated-estimate city/date recommendations before a credit-bearing search.
This estimate-only endpoint is available to guests and does not reserve or
charge a use. The selected criteria remain in the URL; exact provider search,
trip saving, and alerts require login and safely return to that local URL after
authentication. External or protocol-relative `next` values are rejected.
The selected exact dates are then passed to the normal provider workflow.
Hotel preferences support nightly price ranges, property type, star rating,
review score/count, areas, and transit distance. Vacation-rental results are
provider-neutral and only appear when an actual provider returns them; the
application does not scrape Airbnb or label mock inventory as live.

## Price alerts and account UX

Flight, hotel, and saved-trip cards can create an alert using the currently
displayed source currency and price, or leave the target blank to follow any
drop. The API verifies the resource belongs to the authenticated user. A
database uniqueness constraint prevents duplicate or concurrent alerts for
the same resource; another user's resource is deliberately indistinguishable
from a missing resource.

`GET /api/v1/alerts` includes a display title, route/property/destination
summary, current price, source currency, and quote time. Alerts can be updated
with `PATCH /api/v1/alerts/{id}`, paused, resumed, and deleted only after UI
confirmation. Failed deletion leaves the row visible. Account pages distinguish
loading, empty, signed-out, forbidden, and service-failure states, while the
mobile keyboard-accessible navigation exposes trips, alerts, airline fares,
plans, and account routes.

## API summary

- Auth: `/api/v1/auth/register`, `/login`, `/logout`, `/me`
- Search: `POST /api/v1/searches`, status, SSE events, official offer refresh,
  `POST /searches/{id}/flight-sources/expand`, and FlightAware enrichment
- Flight status: `POST/GET /api/v1/flights/status-lookups` and an owned,
  on-demand `/items/{item_id}/track` endpoint
- Product: plans, usage, saved trips, re-optimization, and price alerts
- Intelligence: natural-language parsing and destination discovery
- Experimental airline fares: crawler status and public cached-fare discovery
  plus two-trip back-to-back price comparison

The Next.js browser app calls only its same-origin `/api/travel/*` BFF. The BFF
stores JWTs in HttpOnly/SameSite cookies and attaches them to the internal API;
the browser never receives provider credentials or persists an access token.
