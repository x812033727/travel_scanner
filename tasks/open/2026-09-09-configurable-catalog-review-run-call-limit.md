---
id: 2026-09-09-configurable-catalog-review-run-call-limit
title: Configurable catalog review run call limit
status: review
priority: P1
area: api
owner: codex-catalog-call-limit
claimed_at: 2026-09-09T12:12:50Z
created_at: 2026-09-09T12:11:48Z
completed_at:
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
- [ ] Five-language admin controls, deep links, and focused API/web checks pass; PR provided without production changes.

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
