---
id: 2026-09-09-clarify-stay22-module-switch
title: Clarify the modular hotel affiliate switch and original-channel fallback
status: done
priority: P1
area: web
owner: codex-stay22-module
claimed_at: 2026-09-09T13:15:13Z
created_at: 2026-09-09T13:15:12Z
completed_at: 2026-09-11T15:54:18Z
branch: codex/stay22-modular-toggle
depends_on: []
scope:
  - apps/web/components/travel-services/stay22-admin.tsx
  - apps/web/components/travel-services/stay22-admin.test.tsx
  - docs/stay22-module-switch.md
  - .github/workflows/ci.yml
---

# Clarify the modular hotel affiliate switch and original-channel fallback

## Why

The user requested a modular on/off switch, supplied an actual Stay22 Hub Script
and explicitly accepted its seven-platform LinkSwap, Spark and Nova scope. Existing
Allez is already a separately validated native clickout module, so distinguish it
from browser Script execution rather than imply the three OTA boxes control LMA.

## Definition of done

- [x] The admin sees saved mode separately from unsaved preview and can disable without losing settings.
- [x] Allez and full Script modes have accurate scope, LMA ID validation and five-language explanations.
- [x] Save failures preserve form and confirmed mode; admin never executes the third-party Script.

## Steps

- [x] Inspect actual Hub details and editing restrictions in Chrome; user approved full scope.
- [x] Add mode, Script ID, preserved settings and explicit document lifecycle explanation.
- [x] Validate UI, document separate native/Script contracts and hand over the feature PR.

## How to verify

Vitest stay22-admin tests, TypeScript, ESLint, i18n, production Next build and
browser fixtures. Root isolation and backend config/options each have their own
claimed task; no real Stay22 traffic or booking is generated in CI.

## Notes

Hub ID supplied by the user: 6aa15a455ff1d17f658d1692, domain mokaair.com.
Hub showed Inactive, seven platforms plus Spark/Nova enabled and no self-service
switch for excluding providers/features (must contact Stay22). The user accepted
that full scope. Reading Hub or showing enabled config is not proof of tracking.
The previous d9ef8fcd first-click fix is live; this new Script work is not merged or
deployed. Canonical dirty checkout remains untouched.

Admin focused tests: 10 passed after final explanatory copy additions. Full
ESLint, i18n, 27 tooling tests, Ruff, mypy (291 files) and final production Next
build (267 routes including regenerated TypeScript route types) passed. CI now
includes the isolated full Script browser suite. Full local Vitest was stopped
under host memory pressure; do not report it as completed.

PR #383: https://github.com/x812033727/travel_scanner/pull/383.
The corrected offline-guarded combined browser regression passed all 50 cases
(28 Script + 22 Allez, desktop and Pixel 7). CI must independently finish the full
suite. The PR is not merge/deployment authorization; leave production settings
unchanged. Earlier fulfilled-redirect fixture risk and its transport correction
are documented in the browser task and rollout document.

## Closed after merge (site owner's instruction, not the holder)

PR #383 merged on 2026-09-09 as squash `73f893a`, whose tree is identical to the PR head
`132e3d7`, so everything on the branch reached main; the branch has since been deleted.
Every check on that head passed: `api`, `web`, `containers`, `full-stack-smoke`,
`discovery-browser` and `planner-browser`. The task stayed in `review` and kept holding its
scope, which blocked later claims, so claude-opus-5 moved it to done on 2026-09-11.

If the holder still has follow-up work that never reached the branch, file a new task rather
than reopening this one.
