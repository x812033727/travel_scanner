# Travel Scanner

Travel Scanner is a mock-first, API-first travel comparison MVP. It combines
flights, hotels, activities, and transportation into complete trip plans and
explains the trade-off between the cheapest, balanced, and comfortable choices.

> All offers in this repository are deterministic demonstration data. No live
> provider, booking, payment, or AI service is contacted.

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

## Search orchestration

`POST /api/v1/searches` validates the JWT, entitlement, rate limit, idempotency
key, and credits before creating an RQ job. The worker calls provider modules in
parallel; one provider failure becomes a warning instead of cancelling useful
results. Normalized offers are persisted and published through a replayable
Redis Stream exposed at `GET /api/v1/searches/{id}/events`.
