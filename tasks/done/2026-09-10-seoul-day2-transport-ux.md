---
id: 2026-09-10-seoul-day2-transport-ux
title: Seoul Day 2 transport settings and readable route details
status: done
priority: P1
area: web
owner: codex-seoul-day2-release
claimed_at: 2026-09-10T06:16:47Z
created_at: 2026-09-10T05:38:15Z
completed_at: 2026-09-11T15:54:23Z
branch: codex/seoul-day2-transport-ux
depends_on: []
scope:
  - apps/web/components/trip-editor.tsx
  - apps/web/components/trip-editor.test.tsx
  - apps/api/app/trips/routing.py
  - apps/api/tests/test_korea_transit_google_fallback.py
  - apps/api/tests/test_trip_routing.py
  - apps/web/components/route-mode-panel.tsx
  - apps/web/components/route-mode-panel.test.tsx
  - apps/web/components/route-segment-card.tsx
  - apps/web/components/route-segment-card.test.tsx
  - apps/web/components/planner/route-panel.module.css
  - apps/web/components/route-timeline-link.tsx
  - apps/web/components/route-timeline-link.test.tsx
  - apps/web/components/planner/day-timeline-copy.ts
  - apps/web/lib/trip-types.ts
  - apps/web/lib/trip-types.test.ts
  - apps/web/messages/zh-TW/trips.json
  - apps/web/messages/zh-CN/trips.json
  - apps/web/messages/en/trips.json
  - apps/web/messages/ja/trips.json
  - apps/web/messages/ko/trips.json
  - apps/api/app/trips/router.py
  - apps/api/tests/test_korea_dual_maps.py
  - apps/api/tests/test_naver_maps.py
  - apps/web/e2e/korea-dual-maps.spec.ts
  - apps/web/e2e/planner-route-tones.spec.ts
  - apps/web/e2e/navigation.spec.ts
  - docs/seoul-day2-transport-ux.md
---

# Seoul Day 2 transport settings and readable route details

## Why

Real Chrome operation of the user's Seoul Day 2 exposed transport estimates
presented as queried routes, missing structured step lists, disabled dead-end
actions and an ODsay-only country policy while no ODsay key was configured.
An authorized, single metered Google Routes probe for the same public endpoints
returned HTTP 200 with a route. Use existing Google as a configuration fallback
and make actual route details the primary UI, without inventing schedules.

## Definition of done

- [x] KR transit can use configured Google when ODsay is not configured.
- [x] Queried transit shows readable boarding, transfer and walking steps before the map.
- [x] Unavailable modes disclose their state before requesting, with useful fallback actions.
- [x] Manual and unqueried timings are never labelled as verified routes.
- [x] Browser and backend regressions pass; distinguish production from local validation.

## Steps

- [x] Root: real Chrome Day 2 + Google consumer details + one metered Routes probe.
- [x] Routing backend: configuration fallback, preserved quota/mode matrix, fixtures.
- [x] Routing frontend: usable panel, detailed steps, honest fallback and manual input.
- [x] Catalog frontend: timeline status and no fabricated KR walking duration.
- [x] Root: integration, regression and Chrome verification.
- [ ] Separately authorized PR, merge and deployment; then re-query the live Day 2.

## How to verify

Ruff/mypy/pytest for routing/navigation; web ESLint/TypeScript/i18n/Vitest;
desktop/mobile Korea route E2E and actual Chrome transport settings/details.

## Notes

No catalog, credentials, publication, AI rewrite, reservations or provider
activation changes. User clarified that this task targets transport settings
and information, not rearranging sights. Any trip test mutation stays in Day 2.
PR385 is being integrated by a different task; admin-hotspots files are not
owned here. The user authorized PR merge and production deployment on 2026-09-10
after accepting the local fix. Coordinate with the preceding PR385 deployment.

Implementation and targeted validation are complete; see
docs/seoul-day2-transport-ux.md for exact evidence and live-versus-fixture boundaries.
The release task is active again; do not mark done until merge and production
verification are recorded.
Real production trip items and saved routing remained unchanged. Google probe
and detailed check used the existing usage meter (two bounded requests total).
Unrelated force-refresh propagation and locale-prefixed login return bugs were
recorded in separate open tasks, not silently folded into this change.

## Closed after merge (site owner's instruction, not the holder)

PR #387 merged on 2026-09-10 with merge commit `a044e4c`, whose second parent is the branch
head `3876b73`, so every commit on the branch is on main; the branch has since been deleted.
Every check on that head passed: `api`, `web`, `containers`, `full-stack-smoke`,
`discovery-browser` and `planner-browser`. The task stayed in `review` and kept holding its
scope, which blocked later claims, so claude-opus-5 moved it to done on 2026-09-11.

The one unticked step, deploying and then re-querying the live Seoul Day 2, is not recorded
here or in `docs/seoul-day2-transport-ux.md`, which still ends by asking for it. That check
needs only one of the 27 paths this task held, that document, so it moved to
`2026-09-11-seoul-day2-live-requery` instead of keeping all 27 locked. This overrides the note
above about staying open until production verification is recorded: on this board a merged
pull request closes its task (`tasks/README.md`), and the verification now has a task of its
own.

If the holder still has follow-up work that never reached the branch, file a new task rather
than reopening this one.
