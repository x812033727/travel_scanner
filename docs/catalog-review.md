# Gemini catalog review and bounded expansion

The administrator page is `/{locale}/admin/catalog-review`. It reuses the encrypted
Gemini configuration from Settings; the browser never receives the key. This is a
catalog workflow, not an itinerary operation, and it never debits member credits.

## Operator workflow

1. Start **Review pending**. The API snapshots every pending hotspot, dish and merchant,
   including inactive rows. Source excerpts and Gemini's responses are untrusted data.
   A background worker fetches public evidence and assesses batches of at most 20.
2. Read the stored reason, exact short citations, missing requirements and proposed
   action. The counts labelled “recommended approval/rejection” are not published changes.
   Once the job stops, select eligible rows, preview, and explicitly confirm an action.
3. Once all snapshot rows have been assessed, **Discover 100** becomes available:
   40 hotspots/popular places, 20 dishes, and 40 real merchant branches in the existing
   destination catalog. This is a target, not a promise that missing evidence will be
   invented to fill a quota. Discovery requests at most five drafts per call, deduplicates
   against all statuses (including rejected/disabled tombstones), and commits small batches.
4. New entries are saved as **pending, inactive and unverified**, then assessed with
   independently fetched evidence. Complete missing source/map/coordinate work in the
   existing catalog editor and start a fresh review. Only an eligible confirmed approval
   activates the entry. A candidate in the database is not necessarily a public entry.

“Review complete” means every snapshot was assessed, including those needing manual
work; it does not mean the production pending count reached zero. Partial discovery
reports the actual created count and does not manufacture results after three consecutive
unproductive batches. Existing approved entries are not included in a pending snapshot.

## Evidence and publication requirements

- HTTPS sources pass syntax, public-DNS, IP-pinned TLS, timeout and response-size checks.
  Fetch concurrency is three. Redirects from publishers are not followed. Only the server's
  tourism/Wikimedia registry and independently verified, published merchant websites grant
  source authority. A model URL, domain name or confidence score does not grant authority.
- Search discovery accepts URLs present in Gemini grounding metadata and the trusted
  registry. Google/Naver Maps content and unlicensed Michelin content are not ingested.
  Full page text is transient; persisted evidence contains source URL, digest, outcome and
  short exact citations, not copied pages, descriptions, photos or reviews.
  Canonical Wikidata QID pages use the official `wbgetentities` endpoint to read bounded
  structured identity facts, retaining the canonical QID citation. This avoids ingesting
  oversized HTML. Outbound model context excludes administrator IDs and arbitrary metadata.
- Approval suggestions require confidence at least 0.9 and exact fetched trusted citations.
  All server publication gates still apply. Rejection requires evidence; an alias, incomplete
  name, uncertain type or absent map is a reason to keep pending, not automatic rejection.
- Hotspots and merchants need an already independently verified exact map identity,
  durable coordinates, coordinate source and verification timestamps. Korean places require
  Naver; other places require a Google Place ID. Hotspots additionally require Wikidata identity.
  Merchant sources must identify the actual branch, not merely its city or chain.
- Dishes require five localized names/summaries, supported destinations, meal types and
  verified source evidence. Merchant relationships resolve existing catalog identifiers;
  generated identifiers and geographic coordinates are never trusted or installed.
- Gemini corrections are suggestions only. This workflow cannot set Place IDs, Naver URLs,
  coordinates, verified timestamps, deep-travel approval or other identity authority.

## API and concurrency

All endpoints require the existing administrator capability:

| Endpoint | Purpose |
| --- | --- |
| `GET /api/v1/admin/catalog-review` | Configuration availability, pending counts, recent jobs |
| `POST /api/v1/admin/catalog-review/runs` | Snapshot review or bounded discovery; Idempotency-Key required |
| `GET /api/v1/admin/catalog-review/runs/{id}` | Persisted counts, status, budget and resumability |
| `GET /api/v1/admin/catalog-review/runs/{id}/items` | Paginated assessment previews, default 30, maximum 100 |
| `POST /api/v1/admin/catalog-review/runs/{id}/resume` | Explicit retry of unfinished work |
| `POST /api/v1/admin/catalog-review/runs/{id}/apply` | Confirm selected eligible actions with version and Idempotency-Key |

Only one catalog job runs globally. PostgreSQL serializes job starts, worker leases and
apply operations. Workers renew a five-minute lease; stale workers cannot reserve calls
or commit. An orphaned queue entry becomes resumable after five minutes. Resume reuses
persisted created entries and skips assessments already completed. It never resets usage.

Apply checks the current row and relationship fingerprint, pending status, a seven-day
assessment lifetime, action eligibility and current publication requirements. Concurrent
admin edits therefore invalidate the old assessment. Each changed entity gets an audit
record; repeated apply keys return the saved receipt rather than writing again.
Seed reruns preserve manual moderation and corrected evidence, including reviewed food
translations and rejected hotspot identities.

## Usage and limits

The shared configured `HOTSPOT_GUIDE_GEMINI_DAILY_SEARCH_BUDGET` is reserved **before**
each Gemini HTTP request, including structured-output repairs. Each run additionally has
an immutable maximum of 80 requests. Source fetches themselves do not call Gemini.
Usage records contain attempted calls and returned token totals; network failures may
consume a reservation without token usage being returned.

These are request safety limits, **not a dollar cap**. Grounding may issue multiple
search queries and Gemini billing depends on the selected model and token/search usage.
See [Google Search grounding](https://ai.google.dev/gemini-api/docs/google-search) and
[Gemini rate limits](https://ai.google.dev/gemini-api/docs/rate-limits). Keep provider-side
quota/billing controls in place. Daily-budget exhaustion is resumable after reset; a run
at its own call limit requires a new, explicitly started job and is not silently extended.

## Deployment and verification

Deploy API, Web and worker together, run Alembic to the current head, and restart workers
so the `catalog-review` RQ queue is consumed. No scheduler starts a paid catalog run on
deployment. The administrator must explicitly start both stages.

Run API Ruff, mypy and pytest; web lint, locale parity, typecheck, single-worker Vitest and
production build; task/tool checks; PostgreSQL fresh migration and integration tests;
container build and full-stack smoke. Integration tests use rolled-back PostgreSQL
transactions and mocked Gemini/evidence/queue calls. Local Windows cannot collect the
existing Unix-socket deployment-center test; Linux CI is required for the complete suite.

After deployment, separately record live run IDs, exact assessed/created/applied totals,
unresolved gaps and provider usage. Code tests or seed fixtures are not proof of a live
100-item expansion. Do not declare the user's data task complete until the production
results and remaining verification work have been checked.
