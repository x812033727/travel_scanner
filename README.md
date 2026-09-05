# Mokaair

Mokaair is a mock-first, API-first travel comparison MVP. It combines
flights, hotels, activities, and transportation into complete trip plans and
explains the trade-off between the cheapest, balanced, and comfortable choices.

## Brand

The public product name is **Mokaair**. The primary wordmark is typography-only:
`Moka` uses mocha brown (`#6B4A3A`) and `air` uses deep teal (`#0D6B68`) on a
cream (`#F7F1E8`) background. Reusable SVG and PNG artwork lives in
`apps/web/public/brand`; Next.js favicon and Apple icon assets live in
`apps/web/app`. Internal database, package, service, and environment identifiers
retain their existing `travel_scanner` / `travel-scanner` names for compatibility.

### Appearance themes

The desktop and mobile headers provide System, Light, and Dark appearance
choices. The preference is applied before the page paints, stored only in the
current browser as `mokaair-theme`, and follows operating-system changes while
System is selected. It does not require an account or sync between devices.
The trip planner's Ocean, Sunset, and Lavender accent themes remain available;
dark mode adapts their surfaces and contrast without replacing the selected
accent.

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

To run the six-hour flight/hotel price monitor and LINE delivery queue locally,
also start `alert-scheduler` and `alert-worker`. LINE account linking requires a
Messaging API channel and the environment values documented in
[`docs/line-price-alerts.md`](docs/line-price-alerts.md).

Run the frontend separately:

```bash
npm install
npm run dev:web
```

Open `http://localhost:3000`; API docs are at `http://localhost:8000/docs`.

## Production deployment

Production starts only with an explicit HTTPS origin, secure cookies, separate
random `APP_SECRET_KEY` and `SETTINGS_ENCRYPTION_KEY` values, and password-protected
PostgreSQL and Redis URLs. Set `POSTGRES_PASSWORD` and `REDIS_PASSWORD`, then use
matching URL-encoded credentials in `DATABASE_URL` and `REDIS_URL`; never reuse the
development `travel` password. The API schema and documentation routes are disabled
in production, while `/health` and `/ready` remain available on the loopback-bound
API port. `TRUST_PROXY_CLIENT_IP=true` assumes the bundled web BFF is the only API caller;
any replacement edge proxy must discard incoming forwarding headers and set the
client IP header itself.

```bash
docker compose -f docker-compose.prod.yml up --build -d
```

The production Compose file runs API processes as non-root users, drops Linux
capabilities, and rejects startup when required secrets are missing or unsafe.

### Deployment center

`/admin/deployments` can deploy only the latest `origin/main` commit whose
push run of the `CI` workflow succeeded. The feature is off by default. Do not
enable it until this version has been deployed manually and the restricted host
agent has passed preflight. Installation and host directory details are in
[`ops/deployer/README.md`](ops/deployer/README.md).

The API container receives only the agent Unix socket directory as a read-only
mount; it never receives a Git checkout or the Docker socket. The host agent
account itself belongs to the `docker` group and is therefore root-equivalent on
the host; the trust boundary is documented in
[`ops/deployer/README.md`](ops/deployer/README.md). Requests are
timestamped, single-use, and HMAC authenticated. The host agent pins the
repository, branch, workflow, Compose project name, release directories, and
health endpoints. It builds SHA-tagged images while the prior services run,
requires a PostgreSQL custom-format backup before migration, then requires
three consecutive API/Web health checks. A failed activation returns to the
previous application images without downgrading the database. Keep migrations
backward compatible.

Only an effective administrator whose email also appears in
`DEPLOY_ADMIN_EMAILS` receives `can_deploy=true`. Starting a deployment requires
the current password and `DEPLOY <7-char-SHA>`. Set the same random 32+ character
`DEPLOY_AGENT_HMAC_KEY` in the API runtime environment and the root-owned agent
environment. The browser cannot select a branch, tag, repository, command, or
historical version. Agent upgrades, database restores, and manual rollback
remain host administrator actions.

Create an account in the UI to receive the currently configured number of free,
non-expiring uses. To grant a
usage pack locally before online checkout is available:

```bash
cd apps/api
uv run python -m app.cli add-usage-package --email you@example.com \
  --package PACK_30 --reference local-test-001
```

## Administration

After applying the database migration, grant an existing account administrator
access and open `http://localhost:3000/admin/users` or
`http://localhost:3000/admin/usage-settings` or
`http://localhost:3000/admin/system-settings` or
`http://localhost:3000/admin/layout-settings` or
`http://localhost:3000/admin/settings`; deployment allowlisted administrators
also see `http://localhost:3000/admin/deployments`:

```bash
cd apps/api
uv run python -m app.cli set-admin --email you@example.com
# or create the first administrator without the public registration form
uv run python -m app.cli create-admin --email you@example.com
```

Use `--revoke` to remove the database role. `ADMIN_EMAILS` is also accepted as a
comma-separated bootstrap or recovery allowlist for accounts that already exist;
remove the address from that environment value before revoking its access.
Addresses listed in `ADMIN_EMAILS` or `DEPLOY_ADMIN_EMAILS` cannot self-register
through the public form (`admin_email_reserved`): create those accounts with
`create-admin`, or register them before adding them to the allowlist, so that an
attacker cannot claim an administrator address first. Signing out revokes the
presented access token immediately. The desktop and mobile headers
use the same `/auth/me` result and expose the administration link only to
accounts with an effective database or `ADMIN_EMAILS` role. Every administration
API still enforces the role server-side.

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

The plans and usage page manages the registration trial, public one-time usage
packs, and the cost of all 12 metered operations. Trial grants accept 1–10,000
uses. Public packs require names in Traditional Chinese, Simplified Chinese,
English, Japanese, and Korean; each pack contains 1–100,000 uses, costs
NT$0–10,000,000, has an explicit display order, and can be archived or restored.
Pack codes are generated once and remain immutable. At most one active pack is
featured, and archived packs remain available to historical ledger references.
This catalog intentionally does not process payments or issue purchased packs.

Each operation cost accepts 0–100 uses. A zero-cost operation is still reserved
idempotently and writes a successful zero-amount ledger entry, but leaves the
member balance unchanged. Changes apply immediately to new operations and new
registrations. Existing balances, ledger entries, prior package grants, and
in-flight reservations are not rewritten: every reservation snapshots the cost
that was effective when it began. The public, uncached
`GET /api/v1/usage-catalog?locale=...` endpoint exposes only the effective trial
grant, active localized packs, and operation costs. The existing `/api/v1/plans`
endpoint remains available for compatibility. Administrative changes are stored
in `admin_audit_logs` with before/after values and the actions
`registration_trial_updated`, `usage_operation_costs_updated`,
`usage_package_created`, `usage_package_updated`, or `usage_package_archived`.

The system settings page manages public registration, runtime modes and timeout
or circuit-breaker protection. `REGISTRATION_ENABLED=true` is the environment
default. Saving the public-registration switch stores `registration_enabled` in
the existing `provider_configs.runtime` JSON row; that database value takes
priority and applies immediately to later requests. Turning it off blocks every
new self-registration, including addresses in `ADMIN_EMAILS`, without affecting
existing account login, password changes or administrator features. The public
`GET /api/v1/auth/registration-status` response is never cached, and failed
status checks do not expose a usable registration form.

The layout management page controls the public Hotspots, Trips, Price Alerts,
Flight Status, Airline Fares, and Pricing surfaces. Their environment defaults
are `HOTSPOTS_ENABLED`, `TRIPS_ENABLED`, `ALERTS_ENABLED`,
`FLIGHT_STATUS_ENABLED`, `AIRLINE_FARES_ENABLED`, and `PRICING_ENABLED`; all
default to `true`. Saving creates or updates the existing
`provider_configs.layout` JSON row, whose values take priority over the
environment immediately. A disabled feature is removed from desktop and mobile
navigation and related Web actions, and direct visits show a localized paused
page. APIs and stored data remain available, and read-only `/share/[token]`
links are unaffected. The public `GET /api/v1/runtime/site-visibility` endpoint
returns only the six effective booleans with `Cache-Control: no-store`; failed
checks hide controlled entries and show an unavailable state. Layout changes
use the `layout_settings_updated` audit action with the operator, fields that
actually changed, and resulting visibility values.

Food merchants are browsed by city, sub-city area (商圈) and site-wide cuisine
category. Areas (`food_areas`, seeded 1:1 from each destination profile's
`areas`) and categories (`food_categories`, 18 seeded) are managed under
`/admin/foods`; merchants carry an optional area plus one or more categories, and
publishing a merchant requires at least one category. Seeds only fill gaps:
anything an administrator sets or clears stays that way. After deploying a
release that adds taxonomy data, run `python -m app.cli seed-foods` inside the
API container so the tables are populated without waiting for the hotspot
collector, which only runs under the `hotspots` compose profile.

The API and keys page separately manages encrypted credentials for Google Maps,
NAVER Maps, Ekispert, ODsay, Amadeus, Skyscanner, Duffel, FlightAware, Google Travel Impact, NAVITIME and
affiliate providers. Desktop uses keyboard-accessible, horizontally scrollable
provider tabs, mobile uses a provider selector, and only the active provider is
rendered. Unsaved input remains intact while switching providers, and recent
administration activity has its own tab. The page also shows each provider's
last-24-hour request and failure counts. Changes take effect for API and worker
requests without rebuilding the web image. Provider connection checks and
configuration changes are recorded in `admin_audit_logs`, without secret values.
System setting changes use the `system_settings_updated` action and record only
the changed field names and effective registration result. Responses only
include whether a key exists, its source, and a masked suffix.

Google, LINE, and Apple member login are configured on the same API and keys
page. Each provider remains hidden until it is both enabled and fully
configured. Exact callback URLs, provider-console setup, linking rules, and
security behavior are documented in [`docs/social-login.md`](docs/social-login.md).

Set a stable, randomly generated `SETTINGS_ENCRYPTION_KEY` in production before
saving credentials. It is used to derive the Fernet key for database values;
changing it makes existing encrypted settings unreadable. `APP_SECRET_KEY` is
only a backwards-compatible fallback. Restrict the Google server key by API and
server egress IP. Restrict the browser Embed key by API and the production HTTP
referrer. Do not commit either value.

The management APIs are under `/api/v1/admin/users`,
`/api/v1/admin/usage-settings`, `/api/v1/admin/provider-settings`, and
`/api/v1/admin/deployments`; the safe runtime browser configuration is served separately from
`/api/v1/runtime/public-config` and `/api/v1/runtime/site-visibility`.
Environment variables remain the fallback when no database override exists,
and disabling a provider never silently enables mock pricing in production.

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

Registration trial uses, the public inactive-checkout catalog, and the cost of
each metered operation are configured on the plans and usage administration
page. The initial catalog contains packs of 10 uses for NT$199, 30 for NT$499,
and 100 for NT$1,299, and every operation initially costs one use. Uses stack
and never expire.

The configured cost is reserved while work is in flight and charged only when
a usable result exists. Empty results and failures release the reservation and
create a visible zero-charge record. The append-only PostgreSQL `usage_ledger` records grants,
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
photos, opening hours, route estimates, and saved-trip weather. Secrets belong in the runtime
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
Blank trips immediately receive a complete editable draft for every travel day.
The AI planner can use OpenAI Responses, Anthropic Messages, or MiniMax
Responses with strict structured output. `AI_PLANNER_MODE=auto` follows
`AI_PLANNER_PRIORITY`; timeout, rate-limit, invalid schema, refusal, and provider
errors move to the next configured provider. If none succeeds, the server fills
every day from the built-in destination catalog and labels the result as a
fallback instead of returning an empty itinerary.

AI keys, models, priority, official Base URLs, and timeouts can be managed from
the encrypted admin provider-settings page. Only destination, dates, travelers,
preferences, routing preference, notes, and preserved itinerary summaries are
sent to a selected AI provider; account identity and email are excluded. Google
Places optionally resolves up to 24 suggested locations after generation.

`POST /api/v1/trips/{id}/itinerary/generate` requires `Idempotency-Key` and the
current trip version. The request accepts `scope=day` with `day_date`, or the
backward-compatible default `scope=trip`. Day scope leaves every other date
untouched. Both scopes replace only unlocked AI suggestions, preserving manual,
provider-generated, locked, and fixed-time items. Initial generation is
free. A successfully applied live-AI regeneration charges the configured
`ai_itinerary_generation` cost; catalog
fallback and failed application release the reservation. Fixed-order route
calculation remains free, while same-day itinerary optimization charges its
configured `itinerary_optimization` cost
only after a usable order is applied.

The planner also supports structured Places selections, per-day ordering,
fixed appointments, duration and notes, detailed transit steps, and read-only
shared views.

Attractions and food copied into a plan keep their name in all five site
locales plus the original script (`trip_plan_items.names_json`, one map for
`title` and one for `location_name`). Every catalog path writes it: hotspot and
merchant trip selections, the AI planner's candidates, the deterministic search
builder and the AI meal placeholders. Trip responses resolve `title` and
`location_name` for the `X-Travel-Locale` of the request (the header the BFF
derives from the `travel_locale` cookie) and return the full map as `names`, so
switching language re-labels a saved plan and the UI can show the original text
under the title. Saving the itinerary with the label the client was shown
keeps the map; a real rename drops it for that field only, and Google Places
resolution drops the `location_name` map because the provider label replaces
the catalog one. Free-text stops never carry a map.

Saved trips automatically enqueue a `trip-routes` RQ job after AI place
resolution. Routes are calculated in itinerary order, one day at a time, so
each next start is based on the previous stop's end, the provider duration, and
the day's buffer (transit and 10 minutes by default). Flexible and locked stops
may move in time; `fixed_time` appointments keep their scheduled time and expose
the predicted arrival plus a lateness warning instead of being silently moved.
Normalized day settings and applied segments are durable PostgreSQL records;
third-party raw responses and 15-minute route previews stay in Redis.

The planner route API supports lightweight status polling and deliberate
preview-before-apply interactions:

- `GET /api/v1/trips/{id}/routes/status`
- `POST /api/v1/trips/{id}/routes/compute-day`
- `POST /api/v1/trips/{id}/routes/preview`
- `POST /api/v1/trips/{id}/routes/apply`

Each day can default to transit, walking, or driving with a 0, 5, 10, 15, or
30 minute buffer. Individual adjacent segments may override the day default.
Changing tabs loads up to three real provider alternatives and their downstream
schedule impacts; switching cards or map lines remains a preview. The trip
version and saved times change only after the user applies the selected route. If no
provider route is available, an explicitly labelled manual duration can be
saved without inventing distance, fare, or navigation steps. Existing
`/routes/compute` and `/routes/refresh` callers remain supported.

Google Routes is the global fallback. Set `GOOGLE_MAPS_API_KEY` after enabling
Places API (New), Routes API, and Weather API for server-side calls, and use an origin-restricted
`NEXT_PUBLIC_GOOGLE_MAPS_BROWSER_KEY` for the route drawer after enabling Maps
JavaScript API. Restrict the browser key by HTTP referrer to
`https://mokaair.com/*` and `https://www.mokaair.com/*`, and keep it separate
from the server Routes key. The browser SDK is fail-closed: setting a key alone
does not load it. Set `GOOGLE_MAPS_JAVASCRIPT_ENABLED=true` (or enable the same
switch in the admin provider settings) only after the API and both production
referrers are verified. While the switch is off, route options and exact
external navigation remain available without loading the browser map SDK.
Google provider responses are kept in short-lived Redis caches; durable trip
records retain provider IDs and user-authored fields instead of raw payloads.
The administrator settings page also shows the current and five previous Google
billing months for server-side Places, Routes, Weather, and photo calls. Usage is
grouped by billable SKU because Google applies the global monthly no-cost thresholds
independently: Essentials 10,000, Pro 5,000, and Enterprise 1,000 billable events per
SKU. These defaults can be adjusted with `GOOGLE_MAPS_ESSENTIALS_FREE_LIMIT`,
`GOOGLE_MAPS_PRO_FREE_LIMIT`, and `GOOGLE_MAPS_ENTERPRISE_FREE_LIMIT` when a contract
differs. See the official [pricing categories](https://developers.google.com/maps/billing-and-pricing/pricing-categories)
and [global SKU price list](https://developers.google.com/maps/billing-and-pricing/pricing).
Months reset on Pacific Time. The application meter conservatively counts outbound
requests, including failed requests; browser Maps JavaScript loads, pre-deployment history, and
the provider's final billable-event decisions are not included. Google Cloud Console
remains the billing source of truth. The bundled Redis service enables append-only
persistence, and new counters are retained for monthly history.

The YouTube guide provider uses the same administrator usage disclosure for its
Pacific-Time daily quota day. It tracks outbound `search.list` calls against the
default 100-call Search Queries allocation and `videos.list` calls against the
default 10,000-unit core allocation. Override these display thresholds with
`HOTSPOT_GUIDE_YOUTUBE_SEARCH_DAILY_FREE_LIMIT` and
`HOTSPOT_GUIDE_YOUTUBE_CORE_DAILY_FREE_LIMIT` if Google approves different project
quotas. `HOTSPOT_GUIDE_YOUTUBE_DAILY_SEARCH_BUDGET=80` keeps 20 default search calls
available for manual administrator actions. Counters include failed requests but
exclude pre-deployment history and calls made by other clients, so Google Cloud
Console remains the quota source of truth. See YouTube's official
[quota costs](https://developers.google.com/youtube/v3/determine_quota_cost) and
[`search.list` reference](https://developers.google.com/youtube/v3/docs/search/list).

The saved-trip planner requests `GET /api/v1/trips/{trip_id}/weather` through
the authenticated BFF. It displays current conditions plus Google's daily
forecast (up to 10 days) for a confirmed trip coordinate. Results default to a
15-minute cache (`WEATHER_CACHE_TTL_SECONDS=900`). Trips outside the forecast
window remain usable and show that weather is not yet available instead of
inventing a long-range forecast. Enable the service by following the official
[Google Weather API setup guide](https://developers.google.com/maps/documentation/weather/cloud-setup).

Japanese transit prefers the official [Ekispert API](https://docs.ekispert.com/v1/api/).
Set `EKISPERT_API_KEY`; the API origin is pinned to `api.ekispert.jp`. The default
`EKISPERT_SEARCH_TYPE=plain` uses average waiting times and is explicitly shown as
a preview rather than a dated timetable. Set it to `departure` only when the
Ekispert contract includes timetable search. `EKISPERT_MONTHLY_REQUEST_LIMIT`
is an atomic server-side hard cap (450 by default). One route search returns up
to three alternatives, and the map line uses the returned station sequence so
the UI labels it as a schematic rather than exact track geometry. Existing
NAVITIME support remains a deployment fallback when Ekispert is not configured;
the app never calls both paid providers for the same preview. Without either
provider, the planner offers an exact Google Maps deep link and manual duration
instead of inventing a route.

Korean transit uses the official ODsay `searchPubTransPathT` endpoint. Set
`ODSAY_API_KEY` to a **Server Key** restricted to the production server's fixed
egress IP, not a browser Web Key. `ODSAY_DAILY_REQUEST_LIMIT=25` reserves five of
the Basic plan's 30 daily calls for connection checks; commercial contracts can
raise this value. `ODSAY_LANGUAGE=0` requests the Korean response supported by
Standard contracts; select another documented language only when the contract
includes multilingual output. A single request supplies up to three alternatives. The app
does not call ODsay's additional route-geometry endpoint for every candidate;
it draws a clearly labelled stop-sequence line and keeps NAVER Maps as the exact
external navigation destination. ODsay's general route data is a preview, not a
promise of the future departure timetable.

Korean place lookup, browser maps, and driving routes use NAVER Maps where its
official APIs provide structured data; public transit uses ODsay as described
above. Set `NAVER_MAPS_CLIENT_ID` and `NAVER_MAPS_CLIENT_SECRET` after
enabling Web Dynamic Map, Directions 5, Geocoding, and NAVER API HUB Local
Search for the same NCP application. Restrict the browser Client ID to the
production HTTP referrer. Korean place lookup tries NAVER Local Search and
Geocoding before Google, the planner renders NAVER Dynamic Map before Google
Embed, and driving uses NAVER Directions before Google. NAVER place IDs are
never passed to Google; only WGS84 coordinates cross the provider boundary.

NAVER Directions does not return structured transit or walking routes. ODsay
provides the structured Korean public-transit preview, while walking remains an
exact external NAVER handoff. If either mode has no structured result, the API
returns `kind=external_only` with server-generated official NAVER app/web links.
That result cannot be applied to itinerary times, and the user may enter a
clearly labelled manual duration instead. The administrator usage card counts
server-side `local_search`, `geocode`, and `directions` requests only. It excludes
browser Dynamic Map loads and is not NAVER billing data; NAVER Cloud Console is
the source of truth. After adding the two repository secrets, run the manual
`NAVER Maps credential smoke` workflow (or
`uv run python -m app.cli verify-naver-maps --strict`) to verify Seoul Local
Search, Geocoding fallback, and a real Directions 5 response without making
external availability part of normal CI.

## Travel hotspot intelligence

The public `/hotspots` page searches a time-stamped attraction catalog and shows global,
destination, main-city, secondary-city and deep-travel rankings across 33 destinations in seven
Asian markets. The offline catalog contains 563 reviewed places; weekly discovery can expand it
to 649. The scheduled `hotspot-collector` seeds stable place identities, collects the latest and
preceding 30-day Wikimedia pageview totals, and writes explainable ranking snapshots. Cold-start
values remain visibly marked as estimates rather than live popularity.

The collector is opt-in in production: it sits behind the `hotspots` compose profile, so start it
with `docker compose -f docker-compose.prod.yml --profile hotspots up -d`. See
`docs/hotspot-intelligence.md`.

Every attraction, dish and merchant is stored with a label per site locale (`en`, `ja`, `ko`,
`zh-TW`, `zh-CN`) plus the text in the country's own script. Hotspots keep them in
`hotspot_localizations` with the original in `metadata_json.local_name`; dishes in
`food_localizations` with `local_name`; merchants derive English from `name`, the original from
`local_name`, and administrators may override any locale in `food_merchants.names_json`. The
shared rules live in `app/localized_names.py`: a locale that is the original language reads the
original, and any other gap falls back through a fixed chain so a label always exists. Public
responses return the resolved `name` for the request locale and the full map as `names`.

The canonical `/api/v1/destinations` catalog separates searchable destinations from cross-city
extensions. The API also exposes `/api/v1/hotspots/rankings`, `/api/v1/hotspots/facets`,
`/api/v1/hotspots/sources`, and the compact
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

Set either a short-lived API token or local Mokaair credentials, then
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
`POST /api/v1/crawlers/airlines/browser-captures`. Both require Mokaair
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
