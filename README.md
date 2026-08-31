# Travel Scanner

Travel Scanner is a mock-first, API-first travel comparison MVP. It combines
flights, hotels, activities, and transportation into complete trip plans and
explains the trade-off between the cheapest, balanced, and comfortable choices.

Trip search supports an explicit mock development mode, an Amadeus-backed test
or live mode, and a Skyscanner Flights Live Prices integration for approved
partners. Production never falls back to mock prices when credentials are
absent. The experimental airline crawler remains a separate, non-bookable
public-fare research surface.

## Architecture and project structure

- `apps/web`: Next.js App Router frontend and same-origin BFF
- `apps/api`: FastAPI modular monolith, RQ worker, models, migrations, tests
- `architecture.md`: boundaries and data flow
- `docker-compose.yml`: API, worker, PostgreSQL, and Redis

## Local development

Copy `.env.example` to `.env`, then run infrastructure and API:

```bash
docker compose up --build postgres redis api worker
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
```

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
whether live, test, mock, or disabled data is active.

Flights can be selected independently with
`FLIGHT_PROVIDER_MODE=auto|skyscanner|amadeus|mock`. In `auto` mode an approved
`SKYSCANNER_API_KEY` wins, Amadeus is the fallback, and mock is available only
outside production. Skyscanner exact-date searches use the Live Prices
create/poll flow and emit repeated `module.results` SSE batches; flexible-date
searches use Indicative Prices and never expose booking actions. Provider
session tokens and booking URLs stay server-side. The browser posts to
`POST /api/v1/offers/{offer_id}/clickout`, which validates ownership and expiry,
records an audit event, and responds with a secure 303 redirect.

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

Japan transit enhancement is optional. Set `NAVITIME_API_BASE_URL`,
`NAVITIME_CLIENT_ID`, and `NAVITIME_API_KEY` only after obtaining the required
commercial rights. When configured, sourced exit, platform, and recommended-car
fields are displayed. Missing details are explicitly marked unavailable and are
never inferred.

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
The selected exact dates are then passed to the normal provider workflow.
Hotel preferences support nightly price ranges, property type, star rating,
review score/count, areas, and transit distance. Vacation-rental results are
provider-neutral and only appear when an actual provider returns them; the
application does not scrape Airbnb or label mock inventory as live.

## API summary

- Auth: `/api/v1/auth/register`, `/login`, `/logout`, `/me`
- Search: `POST /api/v1/searches`, status, SSE events, and offer refresh
- Product: plans, usage, saved trips, re-optimization, and price alerts
- Intelligence: natural-language parsing and destination discovery
- Experimental airline fares: crawler status and public cached-fare discovery
  plus two-trip back-to-back price comparison

The Next.js browser app calls only its same-origin `/api/travel/*` BFF. The BFF
stores JWTs in HttpOnly/SameSite cookies and attaches them to the internal API;
the browser never receives provider credentials or persists an access token.
