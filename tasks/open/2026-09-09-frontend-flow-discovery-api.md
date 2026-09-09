---
id: 2026-09-09-frontend-flow-discovery-api
title: Public discovery categories and safe detail projections
status: in-progress
priority: P1
area: api
owner: codex-discovery-flow-api
claimed_at: 2026-09-09T04:14:00Z
created_at: 2026-09-09T03:06:51Z
completed_at:
branch: codex/frontend-explore-flow
depends_on: []
scope:
  - apps/api/app/discovery
  - apps/api/tests/test_discovery_flow.py
  - apps/api/app/trips/router.py
  - apps/web/components/frontend-plan-action.test.tsx
  - apps/web/components/trip-editor.test.tsx
---

# Public discovery categories and safe detail projections

## Why

Unify public discovery navigation around five category groups and let a lazy
detail panel show existing reviewed content and truthful planning actions,
without weakening publication, cache, account or provider-request boundaries.

## Definition of done

- [x] Public search/feed/suggestions accept backward-compatible category groups; existing type is an intersection before candidate caps and pagination.
- [x] Lazy details expose approved introductions, related article/video sources, current place data and existing reviewed hotel/merchant projections.
- [x] Planning capabilities identify actual selectable places/restaurants/hotel products and are absent when identity evidence is insufficient.
- [x] No new provider requests, prices, private itinerary reads, raw booking targets or feature activations.
- [x] Focused Ruff, mypy and API regression tests pass; integration evidence is recorded.
- [x] Trip options resolve legacy localized names to canonical destination IDs without exposing private snapshots; shared planning-action tests cover confirmation, account isolation and safe unknown-result recovery.

## Steps

- [x] Agree category/detail/planning contracts with parent and discovery frontend owner.
- [x] Reuse public cache, intro, merchant, hotel and source-policy helpers in a details-only projection.
- [x] Cover category intersections/cursors, source expiry, hidden drafts, real restaurant options and hotel action gates.

## How to verify

From apps/api with its directory on PYTHONPATH, use the installed sibling
`C:/Users/x8120/.codex/worktrees/mokaair-admin-domains/apps/api/.venv/Scripts/python.exe`:

- `-m ruff check app/discovery tests/test_discovery_flow.py`
- `-m mypy app/discovery`
- `-m pytest tests/test_discovery_flow.py tests/test_travel_discovery.py tests/test_discovery_migration.py -q`

## Notes

- Categories are `all|hotspots|foods|hotels|guides`; foods contains food/merchant and guides contains article/video. Legacy kinds and IDs remain unchanged, including posts/itineraries under all subject to community visibility. Category participates in the reader-bound cursor fingerprint; disjoint category/type returns an empty page, not all content.
- `GET /discovery/content/{kind}/{UUID}` returns the original DiscoveryItem plus `detail` (intro/place/guides/merchants/hotel/planning). Feed/search keep detail null and do not invoke detail serializers. Existing authenticated write APIs are unchanged.
- Planning includes kind/id/destination_id/selection_path/product_id/merchants as applicable. Hotel selection uses existing POST `/trips/{trip_id}/travel-services` with `{product_id,version}` and Idempotency-Key; only fully reviewed product identity yields that capability. Food requires a real chosen merchant; no eligible merchants means no action. Guides use the related hotspot identity, never the guide UUID as a place.
- Place data reuses `place_detail_payload`, preserving manual official URLs, durable coordinates, expiry and attribution. Pending/expired provider fields stay hidden. Related sources use the stricter existing discovery freshness rule before SQL LIMIT. No persisted permitted catalog image source was found, so thumbnails remain null rather than inventing image rights.
- Merchant options reuse the existing publication SQL and card serializer (up to 30 current public merchants). Hotels reuse public_product/ready_offer/public_options/ready_hotel_links; prices remain absent and booking target/review URLs stay server-side.
- Initial verification: scoped Ruff and mypy (10 files) passed; 8 new API tests passed. Combined discovery suite initially had 24 passed / 2 PostgreSQL-only skips / 1 preexisting collection-fixture failure after the simultaneous canonical saved refactor; parent and saved owner were notified to update the old rate-limit mock. PostgreSQL is not available locally; no schema changes belong to this task.
- Final scoped verification: Ruff passed; mypy passed all 10 discovery source files; the 9 new flow cases passed. Combined `test_discovery_flow.py`, `test_travel_discovery.py`, `test_discovery_migration.py`, `test_hotspot_places.py` and `test_hotel_platforms.py` passed 64 tests with only the 2 PostgreSQL migration cases skipped locally. The saved owner fixed shared rate-policy delegation, so the earlier compatibility test now passes without removing production rate limits. `git diff --check` passed. No commit, push, production change, provider request or feature activation was performed.
- Follow-up parent-approved scope adds only `/trips/options` canonical `destination_id` projection in the trip router plus a new frontend regression file. Existing catalog resolvers support stored IDs, localized destination names, airport aliases and legacy snapshot city names. Unknown or malformed values stay null; authenticated ownership, undated counts and saved-trip caps are unchanged. An actual-route SQLite regression checks those boundaries and private-data omission. The new flow API suite passed 10 tests; Ruff passed discovery/trip router/test; mypy passed 11 source files.
- `frontend-plan-action.test.tsx` passed all 13 Vitest cases: one canonical destination match vs ambiguity, explicit dish restaurant/day/meal choice, every-day main-hotel replacement confirmation, guest login return with no reads/writes, account-bound create-trip marker and return-only confirmation, version-conflict refresh without automatic resubmit, network/504 unknown hotspot outcomes with no resend after reopening, exact original hotel body/path/key replay, and stale account read/write response isolation. Only Dialog is simplified for these transport tests; real buttons and effects remain mounted. The first run used unavailable jest-dom matchers; replacing those assertions with native DOM checks yielded a clean run without app changes.
- CI follow-up, coordinated by parent with the parallel planner owner: `trip-editor.test.tsx` is claimed only for its top-level `next/navigation` mock. The single-line change adds `useSearchParams: () => new URLSearchParams()` required by the reused saved action in the hotel picker. The previously failing stay-area/main-hotel test passed (1 passed, 53 unselected), and scoped ESLint plus `git diff --check` passed. No production editor code or other assertions changed; no commit or push was made.
