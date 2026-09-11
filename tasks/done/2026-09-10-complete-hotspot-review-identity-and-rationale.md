---
id: 2026-09-10-complete-hotspot-review-identity-and-rationale
title: Complete hotspot review identity and rationale editor
status: done
priority: P1
area: web
owner: codex-hotspot-review-editor
claimed_at: 2026-09-10T05:34:25Z
created_at: 2026-09-10T01:47:53Z
completed_at: 2026-09-11T15:54:22Z
branch: codex/hotspot-review-editor
depends_on: []
scope:
  - apps/api/app/hotspots/admin_router.py
  - apps/api/tests/test_hotspot_review_identity_editor.py
  - apps/web/components/admin-hotspots-panel.tsx
  - apps/web/components/admin-hotspots-panel.test.tsx
  - apps/web/lib/hotspot-review-copy.ts
  - apps/web/e2e/hotspot-review-editor.spec.ts
  - docs/hotspot-review-editor.md
---

# Complete hotspot review identity and rationale editor

## Why

Continued evidence-based moderation is blocked by missing category/QID inputs and
missing persisted decision rationale. Correct these in the canonical location
editor without changing publication rules or silently approving candidates.

## Definition of done

- [x] Administrators can correct a category, fill a missing QID and preserve reasons.
- [x] Existing identities and concurrent changes are protected; status is unchanged by edits.
- [x] Focused API/UI tests and desktop/Pixel 7 fixture journeys pass.

## Steps

- [x] Backward-compatible API, row locks, audit and regression tests.
- [x] Five-language canonical editor, minimal patches and recoverable conflicts.

## How to verify

Run Ruff, mypy, hotspot API tests, ESLint, i18n, TypeScript, Vitest, production build
and `playwright test hotspot-review-editor.spec.ts` for desktop and Pixel 7.

## Notes

Isolated branch from origin/main daa71684. Original dirty checkout is untouched.
Initial implementation did not authorize deployment or merge. Existing non-empty QIDs are
immutable through this narrow editor; assigning an ID does not verify its source,
map identity or automatically publish it. No paid provider request on page load.

Local validation: complete API pytest 2704 passed / 161 skipped, Ruff and mypy
passed; Web ESLint, TypeScript and i18n passed; complete Vitest 192 files / 1540
tests passed; production build and 4 desktop/Pixel 7 light/dark fixture Playwright
cases passed. Real PostgreSQL integration races remain skipped locally. See
docs/hotspot-review-editor.md for evidence boundaries. Merge/deployment pending
separate authorization; these tests do not complete production catalog moderation.

2026-09-10 continuation: user explicitly authorized resolving PR385 conflicts,
retesting, merging and deployment, then resuming moderation. Merged origin/main
fe26ff8c, preserving PR386 dual maps. Its task owner explicitly handed over the
two admin files and confirmed code/CI/deployment complete; closed only that
completed claim via task CLI. Another active transport-UI task does not overlap.

Additional integration fixes preserve omitted decision reasons, protect dirty
workspace/link navigation, and keep pending editor requests locked across list
refreshes. API final local pytest2822/161skips, Ruff/mypy301 and single0070 head
pass; focusedWeb31, scopedESLint/fullTypeScript pass. FullWeb/build/browser and
fresh final-head CI still pending here; never use previous-head green checks.
Deployment must use immutable source/images with both host locks, verified fresh
backup, preserved existing runtime/data containers and repeated readiness checks.
Actual live source is /root/mokaair-release-fe26ff8c-UaykAgja/source, not the
historical /root/travel_scanner checkout. No provider settings/flags/spending or
new catalog batch is authorized by the deployment operation itself.

## Closed after merge (site owner's instruction, not the holder)

PR #385 merged on 2026-09-10 as squash `1aefd59`, whose tree is identical to the PR head
`45716cb`, so everything on the branch reached main; the branch has since been deleted.
Every check on that head passed: `api`, `web`, `containers`, `full-stack-smoke`,
`discovery-browser` and `planner-browser`. The task stayed in `review` and kept holding its
scope, which blocked later claims, so claude-opus-5 moved it to done on 2026-09-11.

If the holder still has follow-up work that never reached the branch, file a new task rather
than reopening this one.
