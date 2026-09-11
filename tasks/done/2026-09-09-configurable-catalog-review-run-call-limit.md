---
id: 2026-09-09-configurable-catalog-review-run-call-limit
title: Configurable catalog review run call limit
status: done
priority: P1
area: api
owner: codex-catalog-call-limit
claimed_at: 2026-09-09T15:54:14Z
created_at: 2026-09-09T12:11:48Z
completed_at: 2026-09-11T15:54:29Z
branch: codex/catalog-review-call-limit
depends_on: []
scope:
  - apps/api/app/catalog_review
  - apps/api/app/config.py
  - apps/api/app/admin/service.py
  - apps/api/tests/test_catalog_review.py
  - apps/api/tests/test_catalog_review_jobs.py
  - apps/api/tests/test_catalog_review_integration.py
  - apps/api/tests/test_catalog_review_scope.py
  - apps/api/tests/test_admin_provider_settings.py
  - apps/web/components/admin-catalog-review-panel.tsx
  - apps/web/components/admin-catalog-review-panel.test.tsx
  - apps/web/components/admin-settings-panel.tsx
  - apps/web/components/admin-settings-panel.test.tsx
  - apps/web/lib/admin-catalog-budget-copy.ts
  - apps/web/lib/admin-catalog-budget-copy.test.ts
  - apps/web/e2e/admin-domains.spec.ts
  - docs/catalog-review.md
  - .env.example
---

# Configurable catalog review run call limit

## Why

The catalog review cumulative 80-call ceiling is hardcoded in the API and UI. Administrators need a separate configurable per-run ceiling without bypassing the shared daily budget or resetting previously consumed calls.

## Definition of done

- [x] A single shared provider setting controls the default and ceiling for catalog review runs (default 80, range 1–1000).
- [x] Existing runs preserve their approved cap until an explicit, version-checked resume confirms a higher cap; counters, review snapshots, and publication gates remain intact. Expired-lease/orphaned work remains recoverable without allowing duplicate live workers.
- [x] Five-language admin controls, deep links, and focused API/web checks pass; PR provided without production changes.

## Steps

- [x] Register and test the runtime provider setting and server-side enforcement.
- [x] Replace hardcoded UI limits, expose settings and explicit resume confirmation, and validate.

## How to verify

Run focused catalog review/provider pytest, Ruff, mypy; web lint, i18n, TypeScript, focused Vitest, build and browser coverage; task checks.

## Notes

Isolated from origin/main a8be96cd. Existing untranslated-message files are claimed by another task; new five-language copy uses the established typed-copy module pattern instead. No production settings changes or provider requests.

- New requests record explicit/default budget provenance in their idempotency hash; identical requests remain replayable after settings changes or extensions, while omitted vs explicit 80 cannot share a new key. Legacy hashes remain compatible.
- Existing runtime override, single provider editor, dirty-field-only saving, version conflict handling, secrets masking, shared daily budget, and admin audit paths are reused; no migration required.
- Ruff, mypy (291 source files), web ESLint, i18n, TypeScript, production build, tools (27), focused API (170 passed / 18 PostgreSQL-only skipped), provider settings (90), and focused Vitest (124) passed. New budget browser workflow passed desktop/Pixel 7 in both light/dark (4 tests); full-suite/CI results are recorded below when complete.
- Local Docker CLI is unavailable; real PostgreSQL and container validation must run in CI. No live Gemini/evidence calls or production writes are used by tests. Screenshots are isolated UI fixtures, not production data.
- PR: https://github.com/x812033727/travel_scanner/pull/381 (not merged or deployed).
- Final focused API/provider/localization regression: 263 passed, 18 PostgreSQL-only skipped. Reused existing localized validation/resume errors instead of changing another task's backend language registry.
- Latest production-build admin-domain Playwright: 24 passed (desktop/Pixel 7, five locales, light/dark including new budget workflow). An earlier busy-host Back navigation observation timed out while displaying loading placeholders; condition-based actual-value assertions now wait up to 15 seconds, without fixed sleeps. Viewport screenshots confirm readable, 44px controls and focus containment.
- CI for implementation SHA a14b79d8 passed Planner UX, Travel discovery acceptance and containers; final-head CI remains required before merge. Alembic head remains 0068_admin_operations_center (no schema change).

## Closed after merge (site owner's instruction, not the holder)

This task was still `in-progress`, and its notes still say PR #381 is not merged. It merged
on 2026-09-09 as squash `584dd43`, whose tree is identical to the PR head `1ca3a1d`, so
everything on the branch reached main; the branch has since been deleted. Every check on
that head passed: `api`, `web`, `containers`, `full-stack-smoke`, `discovery-browser` and
`planner-browser`. An `in-progress` task holds its scope exactly as a `review` one does, so
claude-opus-5 moved it to done on 2026-09-11.

If the holder still has follow-up work that never reached the branch, file a new task rather
than reopening this one.
