---
id: 2026-09-08-travel-discovery-api
title: Travel discovery search feed and explicit preferences API
status: done
priority: P1
area: api
owner: codex-discovery-api
claimed_at: 2026-09-09T00:11:48Z
created_at: 2026-09-08T23:24:09Z
completed_at: 2026-09-09T01:19:47Z
branch: codex/travel-discovery-community
depends_on: []
scope:
  - apps/api/app/discovery
  - apps/api/app/main.py
  - apps/api/app/config.py
  - apps/api/migrations/versions/0065_travel_discovery.py
  - apps/api/tests/test_travel_discovery.py
  - apps/api/tests/test_discovery_migration.py
  - apps/api/app/hotspots/guides.py
  - apps/api/app/hotspots/admin_router.py
  - apps/api/tests/test_hotspot_guides.py
  - apps/api/tests/test_hotspot_admin_guides.py
  - apps/api/app/hotspots/ai_search.py
  - apps/api/tests/test_hotspot_ai_search.py
---

# Travel discovery search feed and explicit preferences API

## Why

Offer one public discovery surface across existing reviewed travel catalogs and
published community snapshots, without paid provider calls, private itinerary
inference, automatic publication or production activation.

## Definition of done

- [x] Default-off status and unavailable gate; catalog discovery remains independent of community rollout.
- [x] Alias-aware search, explicit-interest/latest/following feeds, safe details and real suggestions.
- [x] Live source publication, visibility, freshness, block and follow reauthorization on every page.
- [x] Private versioned preferences, reset/dismissal, account-erasure helper and existing private collections.
- [x] Separate guarded migration 0065 and metadata registration; no browsing-history or metrics tables.
- [x] Scoped Ruff, mypy and SQLite/ASGI regression checks pass.
- [x] PostgreSQL migration cases run in database-enabled CI (not available locally).

## Steps

- [x] Agree typed DiscoveryItem and shared community/collection resolver contracts.
- [x] Implement SQL-filtered bounded source adapters, locale separation and stable pagination.
- [x] Cover missing configuration, unsafe/stale content, source gates, concurrency and ownership.

## How to verify

From apps/api with its directory on PYTHONPATH, using the sibling installed runtime
`C:/Users/x8120/.codex/worktrees/mokaair-admin-domains/apps/api/.venv/Scripts/python.exe`:

- `-m ruff check app/discovery app/main.py app/config.py migrations/versions/0065_travel_discovery.py tests/test_travel_discovery.py tests/test_discovery_migration.py`
- `-m mypy app/discovery`: 9 files passed.
- `-m pytest tests/test_travel_discovery.py tests/test_discovery_migration.py -q`: 17 passed, 2 PostgreSQL-only cases skipped locally.
- With `RUN_INTEGRATION_TESTS=1`, migration tests create isolated transactional PostgreSQL schemas for frozen 0064 and fresh current-metadata cases, verify idempotent upgrade and account-deletion cascade.

## Notes

- GET `/discovery/status` is always available and no-store. `DISCOVERY_ENABLED` is false by default; no setting was activated.
- Search/feed snapshots retain only IDs and a hashed reader/filter/preference-version binding for 300 seconds, at most 500 IDs. Source queries cap 100 candidates each, with explicit interests fetched before recency caps. This is a bounded discovery window, not an exhaustive catalog export.
- `X-Travel-Locale` controls display labels/hrefs; optional query `locale` filters authored guide/post language. Original source text is not represented as translated.
- Existing Osaka/Kyoto source catalog IDs expand from the unified destination ID; manual preference IDs are canonicalized consistently.
- No prices, Google cached fields, private trip data or arbitrary media thumbnails are projected. YouTube metadata must be fresh before SQL LIMIT; embedding additionally requires explicit public/embeddable status.
- Preference writes lock and refresh the User row before feature rows, preventing a cached authenticated identity from recreating preferences after erasure. Reset preserves monotonic version and clears dismissals; erasure deletes both tables without committing the caller transaction.
- Shared `resolve_discovery_items(session, identifiers, viewer, locale)` accepts at most 100 stable keys and returns reauthorized typed items. `guide:UUID` covers article/video, `post:UUID` covers post/itinerary.
- Collection wrappers use the community agent's owner-checked storage helpers without requiring a social Profile or community activation. Older unsupported references remain removable unavailable stubs in that shared helper.
- Search metrics use existing consent-aware `record_event`, only first-page kind/result_count facts, never raw query or private preference payloads. Admin metrics router is parent-owned.
- Parent owns integration, CI, PR and deployment; no commits or external mutations performed by this task.
- Follow-up evidence pipeline: existing YouTube requests already include `status`; the client discarded it. Search/import now persist only strict provider privacy/embeddable fields, manual import and AI candidate scoring retain this provider-only evidence, and upsert clears missing/malformed proof (including non-provider edits of a video URL). No new requests, flags, migrations or bulk backfill were added. Existing locale/review/manual tags remain unchanged.
- Discovery community details now include the shared `public_media_refs` ID/alt/dimension projection after publication authorization. Storage keys/signed URLs remain excluded and media reads still reauthorize through the existing endpoint.
- Follow-up verification: scoped Ruff passed; mypy discovery plus the three touched hotspot modules passed (12 files); combined hotspot-guides, hotspot-admin-guides, hotspot-AI-search, discovery-community, travel-discovery and discovery-migration pytest suites passed 117 tests with 3 PostgreSQL-only skips. `git diff --check` and `npm run check:tasks` passed (194 tasks). No live provider calls were made.
- Review delivery: draft PR [#372](https://github.com/x812033727/travel_scanner/pull/372), source head `fa280c3a`. Parent integration evidence: full local API 2018 passed / 125 skipped (Unix deployment-script tests excluded on Windows), full Ruff/mypy passed (275 files), Linux discovery full-stack passed. PostgreSQL migration-suite completion remains tracked by the parent in PR CI. This task only updates its review record; parent owns the board generation and commits.
- Final delivery: PR [#372](https://github.com/x812033727/travel_scanner/pull/372) was squash-merged as `6eacb8210c2b456b65e870902f9a6f5ed5022629`. Independently verified the exact merge-SHA main [CI run](https://github.com/x812033727/travel_scanner/actions/runs/34297744944): Ruff passed; mypy passed for 275 source files; schema checks 4 passed; Linux API 2259 passed / 4 skipped / 3 warnings with 74% coverage. `RUN_INTEGRATION_TESTS=1` was present and `tests/test_discovery_migration.py` reported all five cases passed, including both PostgreSQL migration paths.
- Merge-SHA browser verification: Vitest 1069 passed across 155 files; isolated browser UI 282 passed; full-stack smoke 8 travel + 6 private-media/mail/community + 2 admin-domain cases passed. [Planner UX](https://github.com/x812033727/travel_scanner/actions/runs/34297744926) passed 22 cases; [discovery acceptance](https://github.com/x812033727/travel_scanner/actions/runs/34297744914) passed 18 desktop/Pixel 7 fixture and 2 unmocked cases. Containers passed; all three push workflows completed successfully.
- Production deployment evidence supplied by the parent (the sole production operator): exact merged release deployed successfully across all eight services, schema at `0066`, and readiness passed three consecutive checks. Discovery and community remain OFF; environment and volumes were preserved. Pre-deployment backup was verified at 13,672,114 bytes with mode `600`. This task made no production or provider calls and does not represent deployment as feature activation.
