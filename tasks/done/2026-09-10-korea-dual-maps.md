---
id: 2026-09-10-korea-dual-maps
title: Korea dual map identities and transport navigation
status: done
priority: P1
area: api
owner: codex-korea-dual-maps
claimed_at: 2026-09-10T03:20:08Z
created_at: 2026-09-10T03:19:53Z
completed_at: 2026-09-10T05:34:25Z
branch: codex/korea-dual-maps
depends_on: []
scope:
  - apps/api/tests/test_trip_share_fork.py
  - apps/api/app/i18n.py
  - apps/api/tests/test_trip_routing.py
  - apps/api/tests/test_trip_share_payload.py
  - README.md
  - apps/web/components/itinerary-timeline.tsx
  - apps/web/components/itinerary-timeline.test.tsx
  - .github/workflows/ci.yml
  - tools/korea-map-preview.mjs
  - apps/web/components/trip-map-identity-editor.tsx
  - apps/web/components/trip-map-identity-editor.test.tsx
  - apps/web/components/travel-services/catalog.tsx
  - apps/web/components/travel-services/catalog.test.tsx
  - apps/api/app/ai/itinerary.py
  - apps/api/app/travel_services/imports.py
  - apps/api/app/travel_services/admin.py
  - apps/web/components/travel-services/admin.tsx
  - apps/web/components/travel-services/admin.test.tsx
  - apps/web/components/travel-services/explorer.tsx
  - apps/web/types/naver-maps.d.ts
  - apps/api/app/saved/router.py
  - apps/api/app/locations/map_identity.py
  - apps/api/app/locations/map_identity_review.py
  - apps/api/app/locations/map_identity_tasks.py
  - apps/api/app/locations/map_identity_router.py
  - apps/api/app/models.py
  - apps/api/migrations/versions/0070_map_identity_metadata.py
  - apps/api/app/main.py
  - apps/api/app/hotspots/maps.py
  - apps/api/app/hotspots/places.py
  - apps/api/app/hotspots/service.py
  - apps/api/app/hotspots/router.py
  - apps/api/app/foods/service.py
  - apps/api/app/foods/router.py
  - apps/api/app/travel_services/schemas.py
  - apps/api/app/travel_services/service.py
  - apps/api/app/travel_services/router.py
  - apps/api/app/trips
  - apps/api/app/places/router.py
  - apps/api/tests/test_map_identities.py
  - apps/api/tests/test_map_identity_review.py
  - apps/api/tests/test_korea_dual_maps.py
  - apps/web/components/route-map.tsx
  - apps/web/components/route-map.test.tsx
  - apps/web/components/route-mode-panel.tsx
  - apps/web/components/route-mode-panel.test.tsx
  - apps/web/components/route-segment-card.tsx
  - apps/web/components/route-segment-card.test.tsx
  - apps/web/components/planner/route-panel.module.css
  - apps/web/messages/en/trips.json
  - apps/web/messages/zh-TW/trips.json
  - apps/web/messages/ja/trips.json
  - apps/web/messages/ko/trips.json
  - apps/web/messages/zh-CN/trips.json
  - apps/web/e2e/korea-dual-maps.spec.ts
  - apps/web/lib/trip-types.ts
  - apps/web/components/place-picker.tsx
  - apps/web/components/place-picker.test.tsx
  - apps/web/components/trip-editor.tsx
  - apps/web/components/trip-editor.test.tsx
  - apps/web/components/admin-food-merchants-panel.tsx
  - apps/web/components/admin-food-merchants-panel.test.tsx
  - apps/web/components/admin-hotspots-panel.tsx
  - apps/web/components/admin-hotspots-panel.test.tsx
  - apps/web/components/admin-map-identities-panel.tsx
  - apps/web/components/admin-map-identities-panel.test.tsx
  - apps/web/components/travel-services/hotel-options-admin.tsx
  - apps/web/components/travel-services/hotel-admin.test.tsx
  - apps/web/lib/map-identities.ts
  - apps/web/lib/map-identity-copy.ts
  - apps/web/components/food-merchant-card.tsx
  - apps/web/components/food-merchant-card.test.tsx
  - apps/web/components/food-dish-card.tsx
  - apps/web/components/food-dish-card.test.tsx
  - apps/web/components/hotspot-explorer.tsx
  - apps/web/components/hotspot-explorer.test.tsx
  - docs/korea-dual-maps.md
---

# Korea dual map identities and transport navigation

## Why

Implement the approved Korean dual-map plan on an isolated main-based worktree.
Basemap choice, actual routing provider, and external navigation are independent.
One canonical catalog/trip place can have independently verified Google and NAVER
identities. Existing Korean publication and coordinate-evidence gates stay intact.

## Definition of done

- [x] KR transit uses Google basemap/ODsay time; walking offers two basemaps and external/manual time; driving uses NAVER.
- [x] Both map identities survive catalog/trip/hotel reads and ordinary edits.
- [x] Human-reviewed Google candidate batches never auto-publish or rewrite canonical coordinates.
- [x] Map/navigation changes never query paid routes or mutate trip version.
- [x] Local checks, production build and desktop/mobile fixture verification completed.
- [x] GitHub PostgreSQL/Redis migration, container and full-stack CI gates pass.
- [x] Deliver reviewed change; merge and deployment separately authorized and verified.

## Steps

- [x] Root: trip/route contracts, supplemental identity editor, integration tests.
- [x] korea_routing_backend: shared identities, catalog metadata/review/RQ and migration.
- [x] korea_routing_frontend: map/panel/navigation, five locales and browser fixtures.
- [x] korea_catalog_frontend: admin review/forms and catalog dual-map links.
- [x] Review combined changes, regression checks and documentation.
- [x] Publish implementation branch and report CI/release boundaries.

## How to verify

Ruff, mypy, pytest, lint:web, typecheck:web, check:i18n, Vitest, build:web,
check:tasks and test:tools. Browser fixtures: e2e/korea-dual-maps.spec.ts (Seoul
390px/Busan1280px). CI must run real PostgreSQL fresh Alembic upgrade/Compose and
the existing first-party full-stack suite. Fixture screenshots are not evidence
that production credentials or real Korean routes are available.

## Notes

Base daa71684167aafcaea9d1f44505132a0b3ace749. Worktree:
C:/Users/x8120/.codex/worktrees/korea-dual-maps. Original dirty checkout untouched.
Before claiming, freshly verified PR375,374,383 merged and CIgreen and closed
their completed code claims only. Blocked site-experience manual acceptance and
NAVER/business catalog backlogs remain blocked; no production data approved.
No provider keys, settings, booking or paid API calls changed.

Final root validation: Ruff passed; mypy passed (301 files); ESLint, TypeScript,
five-locale i18n, 27 tooling tests and task-board checks passed. Alembic has one
head, 0070_map_identity_metadata. Full pytest passed 2730 tests with 160
environment-gated skips; subsequent hotel/coordinate/localization regressions
passed all 67 dual-map tests. Full Vitest passed 1562 tests with one map-heading
failure captured while that component was being updated; the final source then
passed all 84 editor/map/identity tests. Production Next build generated 272
pages, and its two Seoul/Busan fixture E2E cases passed. PostgreSQL/Redis/RQ and
container checks remain CI-only on this Windows host without Docker.

Frontend final check (2026-09-10): 82/82 tests passed across trip-editor (67)
and route-map (15), plus scoped ESLint. Stale map identities, derived links and
legacy data identities/URLs now clear when a location is replaced by typing,
PlacePicker selection or meal catalog selection; ordinary label/duration edits
preserve them, and new catalog identities are adopted instead of old ones.

Installed Chrome 152.0.7977.83, isolated Playwright chrome-channel profile:
2/2 real login + Next BFF/synthetic backend scenarios passed (Busan 412x915,
Seoul 1464x807). Transit preview -> walk NAVER/Google selector -> drive
preview/apply -> reload; two previews and one apply per scenario, version 1->2
only on apply, map heights 240/240/240px, no horizontal overflow, no external
requests or page errors. Existing-profile CUA timeouts were not reproduced.
This does not establish live Google/NAVER/ODsay credentials or coverage.
The installed-Chrome 2/2 result and root's visual inspection remain valid,
but all six manual-browser screenshot files were cleared by the later
Playwright run and are not retained. Regeneration stopped at a tool-policy
denial of local Next production-server startup; no startup variants were
attempted, and the new fixture API process was stopped.
Two latest production-build E2E screenshots are preserved instead:
C:/Users/x8120/.codex/visualizations/2026/09/10/korea-dual-maps/
playwright-fixture-seoul-390.png and playwright-fixture-busan-1280.png.
These are labelled API/SDK fixture images, not the installed-Chrome evidence
or proof of live provider operation.
Full-suite/final production-build E2E and CI remain root-owned release gates.

Release follow-up (2026-09-10): PR #386 merged with the head-commit guard after
all 12 branch/PR checks passed. Exact reviewed head d9b1700d129ff2f37ba4352772de56946dc656d8;
merge commit fe26ff8c9fa7ee8fccdd6f317e389d4260adc4f5. The authoritative PR CI
run 34436632965 passed API 3073 tests (15 skips), web 1568 tests, 418 browser
tests, containers and the real PostgreSQL/Redis/RQ full-stack smoke. This
supersedes the earlier local partial-suite evidence above. The user separately
authorized merge and deployment; production activation waits for post-merge
main CI run 34438101893. No provider or catalog activation is authorized by
the deployment request. The original dirty checkout remains untouched.

Deployment completed at 2026-09-10T04:54:51Z after main CI 34438101893 and the
Planner UX/discovery workflows passed. All eight pre-existing application
services use fe26ff8c9fa7ee8fccdd6f317e389d4260adc4f5 images. The manual
deployment held both host locks, preserved the existing project/runtime and
PostgreSQL/Redis containers/volumes, and verified a private 15,901,774-byte
custom-format dump with pg_restore --list before migration. Runtime checksum
is unchanged. Schema is 0070_map_identity_metadata; the added JSON column is
NOT NULL with empty-object default and zero NULL rows. API readiness and local
plus public planner checks passed three consecutive times. Seoul/Busan food,
Seoul hotspot/hotel APIs and public home/planner/food/hotspot pages returned
200; the new admin identity route rejects unauthenticated access with 401.
The first page probe used the nonexistent /zh-TW/hotels URL and got the
expected 404; the actual hotel entry is /zh-TW/destinations/{city}/services.
No real provider lookup, credential change, catalog approval or data import
was performed. Old-image fallback alone would fail the strict schema readiness
check after 0070; no rollback or automatic database restore was performed.

Closure reconciled during PR385 integration with explicit confirmation from the
owning task on 2026-09-10. PR386 is merged at fe26ff8c with all 12 branch/PR checks
passing; the owner confirmed production deployment completed 04:54:51 UTC with
schema0070, unchanged provider settings, health/readiness checks and a verified
private backup. This supersedes the earlier pending CI/release notes above.
The owner's detailed local closure is commit ffd78f2a in korea-dual-maps.
No outstanding edits to admin-hotspots-panel.tsx or its test remain under this
claim; the owner explicitly handed those files to PR385 integration. The separate
Seoul transport-UI investigation does not use those files. This bookkeeping does
not itself deploy or complete any remaining catalog/provider work.
