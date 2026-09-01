# Travel Scanner architecture

Travel Scanner is an API-first modular monolith. The browser talks only to the
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

The API is organized by product modules (`auth`, `usage`, `search`, `providers`,
`pricing`, `optimization`, `trips`, `alerts`, `hotspots`, `weather`, and `ai`). PostgreSQL is
the source of truth. Redis is used for queues, short-lived caching, streams, rate limiting,
and circuit-breaker state. Provider-specific payloads never escape the adapter
layer.

The `hotspots` module is a separate, public planning-intelligence surface. A
scheduled collector stores a stable attraction catalog, aggregate source
observations, and explainable global and per-city ranking snapshots. It exposes
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
