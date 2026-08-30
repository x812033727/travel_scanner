# Travel Scanner

Travel Scanner is a mock-first, API-first travel comparison MVP. It combines
flights, hotels, activities, and transportation into complete trip plans and
explains the trade-off between the cheapest, balanced, and comfortable choices.

> Trip-search offers remain deterministic demonstration data. The experimental
> airline crawler API may read explicitly labelled, non-live public fare pages;
> it never contacts booking, payment, private inventory, or AI services.

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

Create an account in the UI to receive the FREE plan. For local PRO testing:

```bash
cd apps/api
uv run python -m app.cli set-plan --email you@example.com --plan PRO
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

Further sections below document providers, plans, credits, orchestration, and
optimization as those modules are introduced.

## Plans and credits

Registration creates a FREE subscription with 20 monthly credits. PRO has 200
credits; it is intentionally not unlimited. Search cost is calculated on the
server (1 per fixed module, 4 for flexible flights, 5 for flight + hotel, 10 for
a full trip, 15 for multi-city, and 3 for re-optimization).

Credits are reserved and debited in the same PostgreSQL transaction. The
immutable `usage_ledger` records every grant, debit, and refund, while the
`usage_reservations` unique key prevents duplicate charges. Redis adds the fast
rate-limit and in-flight guard, but is never the accounting source of truth.

## Adding a provider

Implement the relevant protocol in `apps/api/app/providers/base.py`, normalize
every response into `providers/schemas.py`, then register the adapter with the
search orchestrator. Keep credentials in environment-backed settings and never
return provider-specific payloads or secrets to the client.

The built-in Mock Provider generates stable TPE/Japan examples from a hash of
the request. Every result includes `is_mock`, retrieval time, expiry time, and a
non-bookable example URL.

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
dates into two conventional round trips, a Taiwan-origin wrapper ticket, and a
foreign-origin reverse ticket. The service reads at most two unique public pages
per enabled airline, then reports both the cheapest mixed-airline combination
and the cheapest same-airline combination per passenger. It never suggests
skipping a coupon: every ticket must be flown in order.

Foreign-origin fares retain their source currency. Frankfurter reference rates
provide a clearly labelled TWD estimate and are cached in Redis for 24 hours;
up to seven-day-old cached rates may be used with a stale warning if the rate
service is unavailable. If no conversion rate exists, raw fares remain visible
but no cross-currency savings claim is produced.

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
  -H "Content-Type: application/json" \
  -d '{"origin":"TPE","destination":"NRT","departure_date":"2026-11-10","return_date":"2026-11-15","flex_days":7,"airlines":["CI","BR","JX"]}'
```

## Search orchestration

`POST /api/v1/searches` validates the JWT, entitlement, rate limit, idempotency
key, and credits before creating an RQ job. The worker calls provider modules in
parallel; one provider failure becomes a warning instead of cancelling useful
results. Normalized offers are persisted and published through a replayable
Redis Stream exposed at `GET /api/v1/searches/{id}/events`.

## Cost and optimization

`TotalCostEngine` keeps provider-confirmed prices separate from estimates such
as local transportation. The optimizer applies hard preferences, candidate
caps, a Pareto frontier, and a bounded beam before a 500 ms OR-Tools CP-SAT
selection. The cheapest result is always the lowest feasible total; balanced
and comfortable results use documented, adjustable scoring weights.

## Natural-language search

`POST /api/v1/ai/parse-trip` uses a deterministic rules-based parser for the
MVP. It extracts constraints and reports confidence/missing fields; it never
creates prices. Destination discovery ranks a small mock historical candidate
set before the normal live mock search, mirroring the future production flow.

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
