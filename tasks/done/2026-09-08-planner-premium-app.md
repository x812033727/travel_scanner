---
id: 2026-09-08-planner-premium-app
title: Premium app-style itinerary planning flow
status: done
priority: P1
area: web
owner: codex-planner-premium
claimed_at: 2026-09-08T23:14:10Z
created_at: 2026-09-08T21:19:04Z
completed_at: 2026-09-09T00:23:12Z
branch: codex/planner-premium-app
depends_on: []
scope:
  - .github/workflows/planner-premium.yml
  - apps/web/e2e/full-stack.spec.ts
  - apps/web/e2e/trip-stay-areas.spec.ts
  - apps/web/e2e/stay22-maps.spec.ts
  - apps/web/e2e/readability.spec.ts
  - apps/web/e2e/community.spec.ts
  - apps/web/e2e/travel-services.spec.ts
  - apps/web/components/itinerary-diff.tsx
  - apps/web/components/itinerary-diff.test.tsx
  - apps/web/components/itinerary-place-browser.tsx
  - apps/web/components/itinerary-place-browser.test.tsx
  - apps/web/e2e/navigation.spec.ts
  - apps/api/app/trips/search_criteria.py
  - apps/api/app/trips/stay_areas.py
  - apps/api/app/trips/stay_router.py
  - apps/web/components/new-trip-form.tsx
  - apps/web/components/new-trip-form.test.tsx
  - apps/web/components/trip-editor.tsx
  - apps/web/components/trip-editor.test.tsx
  - apps/web/components/planner-overlay.tsx
  - apps/web/components/planner-overlay.test.tsx
  - apps/web/components/planner
  - apps/web/components/route-mode-panel.tsx
  - apps/web/components/route-mode-panel.test.tsx
  - apps/web/app/globals.css
  - apps/web/lib/planner-copy.ts
  - apps/web/lib/planner-copy.test.ts
  - apps/api/app/trips/router.py
  - apps/api/tests/test_trip_preferences.py
  - apps/web/e2e/planner-premium.spec.ts
  - docs/planner-premium-app.md
---

# Premium app-style itinerary planning flow

## Why

The itinerary was below a tall hero, AI status, service shortcuts and weather. New trips required a wizard; mobile controls and contextual panels competed with the actual timeline. Travelers need a calm, itinerary-first workspace with manual and AI planning equally accessible.

## Definition of done

- [x] City and dates create a manual blank trip in one page without paid provider requests.
- [x] Timeline and day navigation precede supporting services; tools mount on demand.
- [x] Add, move, edit, undo, AI preview/apply and route selection retain existing data contracts.
- [x] Traveler/preference patches preserve omitted fields and invalidate only affected quotes.
- [x] Desktop/mobile browser regressions, full tests and CI are verified; PR is ready for review.

## Steps

- [x] Claim an isolated branch from current origin/main and preserve the shared checkout.
- [x] Implement single-page creation, premium timeline and contextual sheets.
- [x] Add safe preference updates, pending-operation guards and regression tests.
- [x] Finish visual checks and all automated validation, then create PR. Merge/deployment completed only after the user's separate authorization.

## How to verify

Run API pytest/ruff/mypy; npm run lint:web, typecheck:web, check:i18n, check:tasks; Web Vitest with --pool=threads --maxWorkers=1; production build; Playwright navigation.spec.ts and planner-premium.spec.ts with one worker. CI adds Linux/PostgreSQL/Redis, container and full-stack smoke coverage.

Browser scenarios use isolated fixture trips, not production accounts or paid provider data. Verify 390px timeline visibility, continuous additions, More actions, cross-day movement, Tools categories, explicit AI preview/apply and single-page creation.

## Notes

Base: b675f5d34a353eddfb789a953968c3c6d45eac4a. Worktree: C:/Users/x8120/.codex/worktrees/mokaair-planner-premium.

Rebased onto 29c36b258789d3750d3620cceb3a8d1da7fc59df before final CI. Completed Klook task archive and community E2E scope handoff are owner-provided task-only commits; no foreign checkout was modified. Updated existing browser journeys to enter their new tools categories without dropping their underlying assertions. Nested legacy service sheets retain keyboard ownership until dismissed.

Feature-local five-language copy avoids overlapping the active merchant-style task's messages scope. Existing completed #366 and #368 task records were archived only after remote merge/release evidence was checked.

First browser run exposed an oversized configured hotel card; lodging details now expand on demand. Pending metadata/intent requests prevent panel switching and stale-response overwrites. API full Windows run excludes test_deployment_center.py because socketserver.UnixStreamServer is Linux-only; CI must cover it.

Draft PR #371 is open. At 84d8b5a, CI Web passed 1,024 unit tests and 282 browser scenarios; dedicated planner CI passed 22 desktop/mobile scenarios, and containers/full-stack smoke passed. API CI exposed a new test fixture's missing owner-before-trip flush on PostgreSQL; the fixture now explicitly orders inserts and enables SQLite foreign-key enforcement. The updated head must pass the complete CI before marking the PR ready.

## Authorized release completed (2026-09-09)

- User explicitly requested merge and redeployment. PR #371 was squash-merged with head guard `36f246e2a0a6bdc0c16069a4b67e42e60fe7a26a` as `f752ce43ac8e0ae77346d1fce809b223fedd17b6` at 00:07:42 UTC.
- Final head: API 2,169 passed / 3 skipped; Web 1,024 unit tests, 282 isolated browser scenarios, and 22 planner/Stay22/stay-area browser scenarios passed. The unchanged header-session test's initial timing race passed a same-head rerun; no assertions were weakened. Main CI `34293662794` and Planner UX `34293662707` passed before activation.
- Deployed a checksum-verified clean archive through the configured local PuTTY session. Preserved the `travel_scanner` Compose project, existing protected runtime environment, PostgreSQL/Redis container identities and volumes, and all previous release images/backups. An initial deployment-lock contention stopped safely; the owner completed its bounded catalog work before the retry acquired the existing lock.
- Verified a 13,232,310-byte custom-format PostgreSQL backup and archive index (mode 600). Main also contained the already-merged Klook change, so migration advanced 0063 to `0064_klook_affiliate_channels`; no provider/publication switches or catalog records were changed by this deployment. Old-image rollback must not automatically downgrade this schema.
- All eight application services run the exact target image tags and prepared image IDs with zero restarts. Three consecutive API readiness, local Web and HTTPS checks passed. Homepage, trips, new trip, hotspots and foods returned HTTP 200.
- Authenticated Chrome verified the live single-page create form, existing Tokyo timeline at 390px and desktop width, tool-sheet opening, Escape/focus return, and no horizontal overflow. Temporary viewport override was reset. No trip was created, AI generation invoked, or route queried during production smoke; the existing smoke trip remained version 6 with all 36 item rows and persisted trip content byte-identical.
- Protected release directory: `/root/mokaair-release-f752ce43-DRGh4XQF`. The shared dirty checkout remains untouched. This task-only release record is local follow-up metadata; no additional product release is needed.
