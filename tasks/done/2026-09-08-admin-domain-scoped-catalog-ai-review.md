---
id: 2026-09-08-admin-domain-scoped-catalog-ai-review
title: Admin domain scoped catalog AI review
status: done
priority: P1
area: api
owner: codex-admin-review
claimed_at: 2026-09-08T10:04:04Z
created_at: 2026-09-08T10:03:38Z
completed_at: 2026-09-08T13:16:24Z
branch: codex/admin-domain-workspaces
depends_on: []
scope:
  - apps/api/app/catalog_review
  - apps/api/tests/test_catalog_review.py
  - apps/api/tests/test_catalog_review_scope.py
  - apps/web/components/admin-catalog-review-panel.tsx
  - apps/web/components/admin-catalog-review-panel.test.tsx
  - apps/web/lib/admin-review-copy.ts
---

# Admin domain scoped catalog AI review

## Why

Moving review UI into domains must isolate server-side candidates and work application, not merely filter a mixed list.

## Definition of done

- [x] Scope hotspots handles only hotspot; foods handles food and merchant.
- [x] Counts, discovery, snapshots, history, apply and resume enforce scope.
- [x] Legacy all runs and idempotency remain compatible; usage and one-active-run limit remain shared.
- [x] Domain UI starts scoped jobs; operations history cannot start a new mixed job.
- [x] PR checks and authorized merge complete.

## Steps

- [x] Add compatible JSON scope contracts without schema migration.
- [x] Add API and five-language UI coverage.

## How to verify

Run uv run pytest tests/test_catalog_review.py tests/test_catalog_review_scope.py.
Run Vitest components/admin-catalog-review-panel.test.tsx; run Ruff and mypy app.

## Notes

Legacy absent scope normalizes to all. Scope mismatch returns 409 rather than silently applying another domain's work.
No AI/provider calls were performed outside isolated fixtures during implementation.
