---
id: 2026-09-09-frontend-flow-saved-api
title: Unified saved items and private inbox API
status: review
priority: P1
area: api
owner: codex-saved-flow
claimed_at: 2026-09-09T03:07:29Z
created_at: 2026-09-09T03:06:50Z
completed_at:
branch: codex/frontend-explore-flow
depends_on: []
scope:
  - apps/api/app/saved
  - apps/api/app/i18n.py
  - apps/api/app/community/collections.py
  - apps/api/app/community/models.py
  - apps/api/app/community/discovery.py
  - apps/api/migrations/versions/0067_collection_inbox.py
  - apps/api/tests/test_saved_flow.py
  - apps/api/tests/test_saved_flow_integration.py
  - apps/api/tests/test_community_foundation.py
  - apps/api/tests/fixtures/frontend_flow_seed.py
  - apps/api/tests/test_travel_services_integration.py
---

# Unified saved items and private inbox API

## Why

One-click saving must work without enrolling in community and without requiring a
named collection first. Existing typed favorites, post saves and private lists
must remain visible and removable, even when a source is withdrawn or a rollout
is disabled. Organizing a reference must not accidentally delete its base save.

## Definition of done

- [x] An authenticated account can save, hydrate up to 100 visible states, and
  browse the deduplicated private library with real filtered cursor pagination.
- [x] Existing five favorite types and post reactions remain authoritative; guides
  use a DB-unique private inbox without moving old data or copying public content.
- [x] Collection removal/deletion preserves saved references; global unsave removes
  every owned membership. The hidden inbox cannot be listed, renamed or deleted.
- [x] Withdrawn, expired and disabled-source references become removable private
  placeholders; account-switch guards reject writes intended for another user.
- [ ] Full final-head CI, including real PostgreSQL migration/concurrency cases,
  and unmocked browser acceptance pass before parent merges/deploys.

## Steps

- [x] Add the additive 0067 role/unique migration and preserve 255-character opaque
  restaurant identifiers; test both frozen 0066 and current-metadata shapes.
- [x] Add account-only saved/collection APIs, current-source projections and
  transactional compatibility adapters for the original collection routes.
- [x] Cover pagination beyond 500 references, aliases, unavailable sources,
  capacity rollback, typed favorite/reaction replay and cross-account isolation.
- [x] Add only the three required errors in the five backend languages.
- [x] Supply one deterministic, loopback-only opt-in CI hotspot fixture for the
  unmocked guest-to-save-to-plan browser journey.
- [x] Record focused checks after the publication-gate/race hardening.

## How to verify

From `apps/api`, with `PYTHONPATH=.` and an isolated local test configuration:

```sh
python -m ruff check .
python -m mypy app
python -m pytest --ignore=tests/test_deployment_center.py -q --tb=short
python -m pytest tests/test_saved_flow.py tests/test_saved_flow_integration.py tests/test_community_foundation.py tests/test_discovery_community.py tests/test_travel_discovery.py tests/test_saved_items_integration.py -q --tb=short
python -m alembic heads
```

The Linux CI run must omit the Windows-only ignore and set
`RUN_INTEGRATION_TESTS=1` against its disposable PostgreSQL service. It exercises
actual first-inbox concurrent creation and same-item organization with a bounded
20-second timeout; migration tests roll back only a random scratch schema.

The optional browser fixture command is:
`PYTHONPATH=. DISCOVERY_E2E=1 python tests/fixtures/frontend_flow_seed.py`.
It reads `DATABASE_URL` explicitly, requires PostgreSQL+asyncpg on loopback with
no connection override query, rechecks the bound engine, and performs no provider
calls. Root owns the workflow and browser acceptance spec.

## Notes

- PR #374 is open. Implementation is complete and this task is in review, not
  done. Full PostgreSQL-enabled CI is being revalidated after the fixture fix;
  no final pass, merge, or deployment is claimed yet.
- Full local API verification before the final narrow refinements: Ruff passed,
  mypy 278 source files passed, pytest 2084 passed / 129 skipped in 339.46 seconds.
  One warning is the existing `test_usage_settings` AsyncMock coroutine warning;
  no unrelated admin source was changed. Local `test_deployment_center.py` is
  excluded because its Linux deployment agent imports `fcntl`.
- Final saved/migration focused run: 28 passed / 4 PostgreSQL-specific skipped
  in 84.26 seconds; owned Ruff and mypy passed. The related compatibility run
  had 110 passes and a fixture-only Redis cache mock omission, subsequently fixed
  and passed by the focused run. The final alias-membership fix passed Ruff,
  mypy and 3 targeted regression tests in 15.55 seconds.
- No Docker CLI is available locally. No production DB or local `.env` was used;
  full local checks set unreachable loopback DB/Redis URLs and disable integration
  tests. Real PostgreSQL upgrade/concurrency remains an explicit CI gate.
- `0067_collection_inbox` is the verified Alembic head. Fresh `0001` creates current
  metadata, so additions are existence-guarded. Downgrade intentionally does not
  shrink the target field and is not an automatic deployment rollback step.
- New routes emit `private, no-store`; mutations accept `expected_user_id` as a
  stale-account guard. GET/states never enroll profiles or call paid providers.
- `total` counts deduplicated private references including unavailable tombstones.
  Filters execute before pagination; cursors are bound to user and filter context.
- `hotel` aliases `service`, article/video alias guide, itinerary aliases post;
  ordinary services never become hotels. Restaurant Google IDs retain case and
  are not interpreted as UUIDs. Inbox cap is 10,000 references, separate from
  the existing 500-item named-list limit and existing rate policy.
- The original collection rate-policy seam is preserved. Original post saves use
  Reaction(save), preventing an unnecessary duplicate inbox membership on replay.
  Typed favorites use unique-key inserts defensively against legacy writers.
  Account serialization uses NO KEY UPDATE to avoid blocking legacy FK inserts;
  real PostgreSQL concurrency checks remain bounded by 20 seconds. Logical list
  removal clears all aliases within that list, retaining the base and other lists.
- CI fixture ID is `55000000-0000-4000-8000-000000000001`, title/query is
  `Frontend flow fixture Tokyo river`, destination is Tokyo. Its source and map
  IDs are explicitly synthetic and never represent reviewed production data.
- CI follow-up (77f7ab, run 34309418031): 2365 PostgreSQL-enabled tests passed,
  7 skipped, one service-favorites fixture failed because its new saved limiter
  used a process-global Redis client belonging to an earlier event loop. The
  service integration client now isolates the collection policy limiter just
  like its existing service/affiliate limiters; production rate limits are not
  modified. An always-on regression reuses that exact client and failing scenario
  with an unisolated-Redis trap and verifies all four policy calls. Ruff passed;
  the focused regression passed in 43.43 seconds. Final Linux CI rerun is required.
