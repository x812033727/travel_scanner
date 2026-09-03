# Mokaair architecture

Mokaair is an API-first modular monolith. The browser talks only to the
Next.js BFF. The BFF forwards authenticated requests to FastAPI, which owns all
business rules and all provider access.

```text
Browser -> Next.js BFF -> FastAPI -> Search Orchestrator -> Provider adapters
                                    |                       |
                                    v                       v
                               PostgreSQL              Normalized offers
                                    ^                       |
                                    |                       v
                               RQ / Redis <- events <- Cost + optimizer
```

Production deployment is a separate privilege boundary:

```text
Deploy admin -> Next.js BFF -> FastAPI -> read-only Unix socket -> host deploy agent
                                                        agent -> pinned Git mirror
                                                              -> GitHub CI metadata
                                                              -> Docker Compose
                                                              -> pg_dump / releases
```

FastAPI owns authorization, current-password verification, idempotency, the
public deployment history, and sanitized audit events. It does not receive a
Docker socket, Git checkout, GitHub token, runtime environment, or arbitrary
host command. The systemd agent authenticates fixed requests with HMAC,
timestamp, and a persisted one-time nonce; SQLite and a host file lock preserve
job state and global exclusivity while application containers restart. Only
the newest green `origin/main` is deployable. Automatic rollback changes
application images only, so every migration must remain compatible with the
previous release.

The API is organized by product modules (`auth`, `usage`, `search`, `providers`,
`pricing`, `optimization`, `trips`, `alerts`, `hotspots`, `weather`, and `ai`). PostgreSQL is
the source of truth. Redis is used for queues, short-lived caching, streams, rate limiting,
and circuit-breaker state. Provider-specific payloads never escape the adapter
layer.

The `hotspots` module is a separate, public planning-intelligence surface. A
scheduled collector stores a stable attraction catalog, aggregate source
observations, and explainable global, city-code, and stable destination ranking snapshots. The
canonical destination directory distinguishes primary, secondary, and parent-linked extension
destinations; only searchable destinations are passed to flight and lodging providers. It exposes
compact, source-labelled candidates to itinerary planning; popularity never
bypasses opening-hour, route, date, or traveler-preference checks. Restricted
provider content is not copied into this durable ranking store.

Blank-trip planning is separate from price search. `trips` builds a privacy-
filtered `AIItineraryRequest` and invokes the provider-neutral planner in `ai`.
OpenAI and MiniMax use Responses JSON Schema output; Anthropic uses Messages
structured output. The planner normalizes dates, counts, safe time slots, and
durations server-side, then fills missing or invalid coverage from the
destination catalog. Optional Google Places enrichment happens after this
validation, so a Places outage cannot erase the itinerary.

Trip weather is an authenticated, ownership-checked child resource of a saved
trip. The `weather` adapter sends only a representative trip coordinate to
Google Weather, normalizes current conditions and the 10-day daily forecast,
and stores the result in a short-lived Redis cache. Weather never becomes
durable trip state, and dates beyond the provider forecast window are reported
as unavailable rather than estimated.

Initial planning is free and persisted with the trip in one transaction. AI
regeneration uses the usage reservation ledger and optimistic trip version.
Only unlocked `generated_by=ai_planner` rows are replaceable; manual, provider,
locked, and fixed-time rows are copied into the AI context without database IDs
and preserved in storage. Live AI commits one use after the replacement is
saved, while catalog fallback or failure releases the reservation.

Trip routing is a child workflow of the saved itinerary. AI creation returns
the itinerary immediately and enqueues a `trip-routes` job; the worker computes
adjacent pairs sequentially within each day because later start times depend on
earlier travel and buffer durations. `trip_route_day_settings` stores the daily
mode, preference, and buffer. `trip_route_segments` stores only normalized,
applied provider or manual results. Alternate-mode previews are user-triggered,
cached in Redis for 15 minutes, and carry a projected schedule impact without
mutating the trip.

Route writes use optimistic trip versions. Editing a stop invalidates only its
incoming and outgoing pairs. Flexible and locked-but-not-fixed stops propagate
forward; fixed-time appointments preserve their scheduled start and record a
lateness conflict. Stale background jobs discard their result instead of
overwriting newer edits. Google Routes covers transit, walking, and driving,
except that Japanese transit is served only by NAVITIME (the RapidAPI listing or
a direct contract) because Google does not license Japanese transit data to the
Routes API. Korean place lookup,
Dynamic Map rendering, and driving prefer NAVER before Google. Korean transit
and walking remain Google-backed because NAVER Directions is drive-only; when
Google has no result, the response is an external-only NAVER navigation link
that cannot mutate the itinerary schedule. Provider-specific place IDs never
cross adapter boundaries, so a NAVER place reaches Google only as coordinates.

Provider selection is module-specific. Flights choose Skyscanner, Amadeus or
mock through `FLIGHT_PROVIDER_MODE`, while lodging, activities and transport
retain their existing travel provider. Skyscanner uses create/poll batches that
map to repeated SSE `module.results`; Amadeus and mock return a single batch.
Production never falls back to mock data.

Live provider sessions, offer refresh locators and clickout URLs are short-lived
Redis data. PostgreSQL stores normalized offers and ownership. A clickout is a
user-authenticated POST through the BFF; FastAPI validates ownership, freshness
and HTTPS before recording a provider audit row and issuing a 303 redirect.

The experimental `crawlers` module is intentionally outside Search Orchestrator.
Its public airline pages expose cached fare discoveries without the schedule,
inventory, tax guarantees, or booking contract required by `FlightOffer`.
Consequently it returns a separate `PublicFareQuote` contract. Promotion into a
flight provider is allowed only after an authorized source supplies all required
normalized fields and production usage rights.
