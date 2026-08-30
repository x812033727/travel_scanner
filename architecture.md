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
`pricing`, `optimization`, `trips`, `alerts`, and `ai`). PostgreSQL is the source
of truth. Redis is used for queues, short-lived caching, streams, rate limiting,
and circuit-breaker state. Provider-specific payloads never escape the adapter
layer.

For the MVP every provider is deterministic and clearly marked as mock. Adding a
live provider means implementing the relevant provider protocol and registering
it with the provider registry; callers and frontend contracts remain unchanged.

