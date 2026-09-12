# Gemini catalog review and bounded expansion

The administrator page is `/{locale}/admin/catalog-review`. It reuses the encrypted
Gemini configuration from Settings; the browser never receives the key. This is a
catalog workflow, not an itinerary operation, and it never debits member credits.

## Operator workflow

1. Start **Review pending**. The API snapshots every pending hotspot, dish and merchant,
   including inactive rows. Source excerpts and Gemini's responses are untrusted data.
   A background worker fetches public evidence and assesses batches of at most eight.
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
| `POST /api/v1/admin/catalog-review/runs` | Snapshot review, bounded discovery or merchant enrichment; Idempotency-Key required |
| `GET /api/v1/admin/catalog-review/runs/{id}` | Persisted counts, status, budget and resumability |
| `GET /api/v1/admin/catalog-review/runs/{id}/items` | Paginated assessment previews, default 30, maximum 100 |
| `POST /api/v1/admin/catalog-review/runs/{id}/resume` | Explicit retry of unfinished work |
| `POST /api/v1/admin/catalog-review/runs/{id}/apply` | Confirm selected eligible actions (including `apply_corrections`) with version and Idempotency-Key |

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
a snapshotted cumulative request limit. Configure **Catalog review cumulative call
limit** (default **80**, integer **1–1000**) in **Admin → Providers & keys →
Gemini multilingual guide search**:
`/{locale}/admin/settings?provider=gemini_guides&field=catalog_review_max_calls`.
The equivalent environment default is `CATALOG_REVIEW_MAX_CALLS`. The AI review
panel links directly to this single editor and distinguishes the current default,
the selected run's approved cap, and its cumulative usage. Source fetches themselves
do not call Gemini.

Saving the provider setting never starts/resumes a job, changes a run's approved
cap, resets usage, or changes the independent shared daily budget. The new default
is used for new requests that omit `max_calls`; explicit values must not exceed
the current setting. Old clients sending `80` remain supported when the setting
allows it. Job-start idempotency hashes retain whether a cap was explicit or a
configured default, so the two distinct spending requests cannot share a key.
Identical retries after a settings change return the original snapshot, not
another paid run; previously stored legacy hashes remain replayable.

For an existing stopped run, first raise the setting, then select **Resume with
new limit** and confirm the old/new cap, already consumed calls, remaining per-run
allowance and daily limit. The optional resume body is
`{"expected_version": 4, "max_calls": 200}`. The API requires an unchanged run
version, a stopped partial/failed run (or a worker with an expired lease / orphaned
queue under the existing recovery rules), a new cap above both its prior cap and usage,
and a value no greater than the current setting. The same transaction records the
old/new cap and usage in the audit log and queues the existing run. Assessments,
snapshot IDs, idempotency hash and cumulative usage are retained; an ordinary
bodyless resume does not extend the cap. Saving a lower setting likewise does not
retroactively revoke an already approved run budget. No active run is silently
granted a larger budget. Concurrent starts/resumes remain globally serialized.
Usage records contain attempted calls and returned token totals; network failures may
consume a reservation without token usage being returned.

Assessment batches use bounded excerpts in the model request; citation verification
still checks the independently fetched source. Failed batches retain a safe machine
error code (truncation, blocked/empty output, validation/identity mismatch, rate limit,
timeout or provider failure), not a raw provider response or credential-bearing error.
Legacy failures recorded only an exception class, so their exact cause is unknown.
After three consecutive failed batches, the worker pauses with a resumable partial
result instead of spending the remaining budget. Explicit resume processes only
unfinished/error rows, preserving prior assessments and the original call limit.
Input, visible output and thinking-token usage are reported separately; visible
output alone does not represent all generated tokens.

A missing candidate in Gemini's response is not a completed assessment. Response
IDs must exactly match the requested batch; missing, duplicate or unknown IDs fail
closed without an additional automatic paid repair. Older synthetic "Gemini did not
return this candidate" placeholders are identified by their complete legacy shape,
excluded from completion and publication, and can be explicitly resumed in their
original run. Resume preserves real assessments, applied/stale rows, snapshot IDs
and cumulative call usage. It does not start another all-pending review.
Legacy entries whose current entity was edited, approved or deleted are marked
stale before retry, so obsolete snapshots do not consume another model call.

All five food localizations retain a bounded representation in the request. If
review context is omitted or truncated, the server downgrades approval/rejection
to `needs_review`; a shorter prompt is not proof that unseen content was reviewed.

These are request safety limits, **not a dollar cap**. Grounding may issue multiple
search queries and Gemini billing depends on the selected model and token/search usage.
See [Google Search grounding](https://ai.google.dev/gemini-api/docs/google-search) and
[Gemini rate limits](https://ai.google.dev/gemini-api/docs/rate-limits). Keep provider-side
quota/billing controls in place. Daily-budget exhaustion is resumable after reset; a run
at its own call limit needs an explicitly confirmed budget increase before it can
resume. Do not start another all-pending run just to bypass the old cap.

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

### Verified production deployment: 2026-09-07

PR #315 / commit `a817003829235a54f12f68b4bcc99c652548fdee` was deployed over the
existing SSH connection after main CI `34076706328` passed. PostgreSQL backup
`/root/travel_scanner_catalog_20260907T024258Z_ba50331.dump` was nonempty and its
custom-format archive index was verified before migration. Migration 0054, three
consecutive readiness checks, all nine existing services, authenticated admin-page
loading and the `catalog-review` queue passed. Anonymous API/BFF requests return 401.

The initial build inherited restrictive checkout permissions and failed before
migration; the original services remained live. A requested broad host chmod was
rejected and was not performed. Successful images were built instead from a clean
Git archive of the verified SHA in a private staging directory, using the protected
original runtime env only through Compose. Existing checkout permissions remain
restricted: **do not use that checkout as a direct build context on the next deploy**.
Use another canonical archive/private staging build and verify non-root image
imports, or separately obtain approval for a reviewed permission normalization.
Keep the existing Compose project name and runtime configuration; never include
secrets in the archive. No previous images, backups or volumes were removed.

The first live review run `1eb2d91f-9d7c-49a4-86fd-6c8aa8a97456` captured 307 rows:
101 hotspots and 206 merchants. It completed partially with 187 assessed as needing
review and 120 batch errors, after 17 calls (692011 input / 61779 visible output /
50321 thinking tokens). No entries were approved or published. Legacy `ValueError`
records cannot establish whether the provider truncated, blocked, or returned invalid
identities; the configured output limit was 8000 tokens and timeout 45 seconds.
Do not blindly resume those errors until the diagnostics/batch fix is deployed.
The snapshot also confirms existing publication gaps: all 307 have unverified map
matches, 215 lack durable verified coordinates, 179 lack exact map identity, and
32 lack a direct merchant source. These counts overlap. A successful model assessment
does not resolve these independent requirements or authorize bulk publication.

## Merchant enrichment (`enrich_merchants`)

A third run mode fills the descriptive gaps of **pending food merchants** — address,
the merchant's own website, a tourism-board listing, 商圈 and categories — so that the
ordinary review and the coordinate work have something to stand on. It is available
only in the Food workspace (`scope=foods`) and never publishes: `map_match_status`,
coordinates, `review_status` and `is_active` are never written by it.

Owner decision (2026-09-12): platforms are used only for **identity and discovery**.
Google supplies a Place ID through the existing matcher; Google Search grounding finds
candidate pages; Tabelog, Gurunavi, HotPepper, Retty, OpenRice, CatchTable, reservation
platforms and social networks are never stored as sources (`PLATFORM_HOSTS` in
`app/foods/enrichment.py`). Durable facts still come from the merchant's own site
(`merchant_official` / `merchant_website`), a tourism-board or government page about
that one merchant (`official_tourism` / `merchant_listing`) or Wikimedia.

### What the worker does

1. **identify** — for snapshot rows without a Place ID outside Korea, the existing
   `match-food-merchant-places` logic runs (Google Text Search Pro, 90% SKU brake,
   ownership check). It writes only `google_place_id` with the run id in its audit row.
   `identify_places: false` skips it.
2. **enrich** — five merchants per batch, two Gemini calls:
   - a grounded prose search for each merchant's official page and tourism listing
     (`_ENRICH_SEARCH_INSTRUCTIONS`); every non-platform host in the grounding metadata
     is kept and flagged `trusted` or not;
   - the server fetches every candidate page and the merchant's already cited pages
     (`fetch_sources`, same SSRF and size limits) and classifies them
     (`verify_candidates`): a trusted-registry page that names the merchant is a
     **listing**; any other non-platform page that names the merchant *and* places it
     (address fragment or the city's name in any script) is an **official** candidate;
   - one structured call (`_ENRICH_INSTRUCTIONS`) extracts `address`,
     `official_website_url`, `listing_source_url`, `area_slug` and `category_slug`
     corrections with a quote each; `verified_corrections` keeps only those whose cited
     page was fetched, still contains the quote, and whose value passes the field's
     rule (an official site must be a verified official candidate, a listing a verified
     listing, an address must appear on the page and be empty in the snapshot, areas and
     categories must be active catalog slugs).
   Each item's snapshot is refreshed right before its batch is assessed, so the
   fingerprint the apply step checks is the state Gemini saw. Items are always
   `needs_review`; `allowed_actions` is `apply_corrections` (when something was
   verified) or `keep_pending`.
3. **apply_corrections** — writes the item's corrections through
   `app.foods.enrichment.apply_merchant_enrichment`, the same function the researched
   JSON importer uses: only empty scalars are filled, sources are upserted by URL with
   `last_verified_at` refreshed, categories are only added (`source='gemini'`), the
   listing host must be trusted, and one `food_merchant_enriched` audit row records
   before/after, origin and evidence. Snapshot, seven-day and pending checks apply as
   for the other actions.

### Requests, budgets and the CLI

`POST /runs` with `{"mode": "enrich_merchants", "scope": "foods"}` plus optional
`destination_ids`, `limit` (≤ 500) and `identify_places`; those three fields are
rejected for the other modes and do not enter their request hashes. The overview
reports `can_start_enrichment`; items expose `corrections` and `identify`; runs expose
`enrichment` counts.

163 pending merchants cost about 33 batches × 2 = 66 Gemini calls (99 with every
repair). The per-run cap (`catalog_review_max_calls`, default 80) must be raised to at
least 120 before a full run, or the run must be chunked with `destination_ids` (≤ 40
merchants ≈ 16 calls). The Google phase spends at most one Text Search Pro call per
merchant without a Place ID.

```bash
python -m app.cli enrich-food-merchants --actor-email <admin> --dry-run
python -m app.cli enrich-food-merchants --actor-email <admin> --destination tokyo --limit 5 --max-calls 6
```

The command creates the run through the normal service (idempotency key derived from
actor, arguments and UTC date, so a retry resumes rather than re-searches) and executes
the worker inline in the api container; corrections are still applied from the admin
page.

### Researched batches (browser lane)

`python -m app.cli export-food-merchant-worklist [--status pending] [--destination …]
[--include-researched] [--out <path>]` prints each merchant with its current data, the
destination's areas (slug, names, match terms) and the active categories. Research
results go into `app/foods/data/enrichment/<date>-<name>.json` (schema in
`app/foods/enrichment_import.py`: per record an outcome of `found`, `partial`,
`not_found` or `blocked_retry_later`, the official page and listing with exact quotes,
the address taken from one of them, the Google Maps branch URL or Place ID with an
identity observation, area and category slugs, the Naver outcome for Korean rows, and
the evidence list). `python -m app.cli apply-food-merchant-enrichment [--file …]
[--check] [--limit N] [--slug …] [--apply]` validates the whole file first, then writes
through the same shared function; a dry run makes the same calls and rolls back.
`not_found` and `blocked_retry_later` records only leave a
`food_merchant.cli_enrichment_researched` audit row, which the worklist export uses to
skip settled merchants and list blocked ones again.

### Known limits

- Official sites behind bot walls or rendered only by JavaScript return `http_403` or
  `empty_content` and produce no candidate; publisher redirects are not followed.
- Korean rows skip the Google phase and still need a Naver place URL by hand.
- A chain's brand site that names the branch and the city passes the official check;
  the human applying the corrections is the last check on branch identity.
- Coordinates are out of scope: `fill-food-merchant-coordinates` can read JSON-LD from
  the newly added pages, and the coordinate queue reviewer must not treat a Google
  candidate's coordinates as durable.
