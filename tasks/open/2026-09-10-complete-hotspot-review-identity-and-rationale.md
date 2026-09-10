---
id: 2026-09-10-complete-hotspot-review-identity-and-rationale
title: Complete hotspot review identity and rationale editor
status: in-progress
priority: P1
area: web
owner: codex-hotspot-review-editor
claimed_at: 2026-09-10T05:34:25Z
created_at: 2026-09-10T01:47:53Z
completed_at:
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
No production deployment or merge is authorized here. Existing non-empty QIDs are
immutable through this narrow editor; assigning an ID does not verify its source,
map identity or automatically publish it. No paid provider request on page load.

Local validation: complete API pytest 2704 passed / 161 skipped, Ruff and mypy
passed; Web ESLint, TypeScript and i18n passed; complete Vitest 192 files / 1540
tests passed; production build and 4 desktop/Pixel 7 light/dark fixture Playwright
cases passed. Real PostgreSQL integration races remain skipped locally. See
docs/hotspot-review-editor.md for evidence boundaries. Merge/deployment pending
separate authorization; these tests do not complete production catalog moderation.
