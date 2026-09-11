---
id: 2026-09-11-food-reservation-platforms
title: Independent food reservation save and multi-platform support
status: review
priority: P1
area: web
owner: codex-food-reservation-platforms
claimed_at: 2026-09-11T06:29:33Z
created_at: 2026-09-11T06:29:13Z
completed_at:
branch: codex/food-reservation-platforms
depends_on: []
scope:
  - apps/api/app/foods/platform_links.py
  - apps/api/app/foods/admin_router.py
  - apps/api/app/foods/service.py
  - apps/api/app/i18n.py
  - apps/api/tests/test_reservation_platform_auth.py
  - apps/api/tests/test_food_integration.py
  - apps/api/tests/test_food_platform_links.py
  - apps/api/tests/test_discovery_flow.py
  - apps/web/components/admin-food-merchants-panel.tsx
  - apps/web/components/admin-food-merchants-panel.test.tsx
  - apps/web/components/admin-merchant-platform-editor.tsx
  - apps/web/components/admin-merchant-platform-editor.test.tsx
  - apps/web/components/merchant-external-links.tsx
  - apps/web/components/merchant-external-links.test.tsx
  - apps/web/lib/reservation-platforms.ts
  - apps/web/lib/reservation-platforms.test.ts
  - apps/web/lib/foods.ts
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/e2e/food-reservation-platforms.spec.ts
  - .github/workflows/food-map-reservations.yml
  - docs/food-reservation-platforms.md
---

# Independent food reservation save and multi-platform support

## Why

Reservation research found valid owner-linked services outside the old country-to-one-provider mapping. Saving a platform currently also patches unrelated merchant facts. Administrators need an isolated, auditable platform save and independently reviewed multiple platforms per merchant.

## Definition of done

- [x] Platform-only save never modifies merchant facts, coordinates, food relations, or merchant approval.
- [x] Twelve known platforms can be independently reviewed across countries; only verified precise venue links are public.
- [x] Concurrent reviews are rejected with a recoverable conflict; drafts survive provider switching and failures.
- [ ] Five-language UI, authenticated API, URL security, mobile layout, and compatibility checks pass.

## Steps

- [x] Backend registry, multi-row reads, isolated writes, version checks and tests.
- [x] Independent admin editor, shared public URL validation, localization and tests.
- [ ] Browser regression, documentation and final validation.

## How to verify

Run focused pytest, Vitest, translation validation, typecheck, lint, production build, and dedicated Food map and reservations Playwright CI. Open an existing merchant, modify its name without saving, add a verified second reservation platform using only the platform button, and confirm the name draft remains unsaved while both platform rows remain available.

## Notes

- Isolated worktree from origin/main 52e3ecfec0e88505f4d8fbdf6962b41857bcbc0d; original dirty workspace untouched.
- Claim overlap was the prior food-map-reservation-entry task already merged in PR #391 at 28ca9d70548db61d3e63a218ef965f6ec267f99f, verified as an ancestor of this base. Force-claim applies only to this isolated successor; other owner task files remain untouched.
- Existing database uniqueness already supports one row per merchant/provider, so no migration or destructive data change is required.
- This task does not merge, deploy, apply catalog research, make reservations, or enable paid APIs. Actual catalog follow-up remains separate.
- Local checks: 176 focused API tests passed; final public/shared 167 and final admin 19 tests passed. Ruff app/tests, Mypy three API source files, five-language/25-namespace integrity and typecheck passed. Production build passed before the final modal safeguard refinement; CI rebuild is required for the final tree.
- Independent parser review compared 318 Node/Python URL and identity cases. Fixed Unicode ASCII-slug confusion and encoded-locale inference. Modal review found background keyboard access and mismatched merchant-response risks; reused the shared modal hook, inert background, guarded open handlers, submitted-ID comparison, and added keyboard/inflight regression.
- Four new PostgreSQL integration cases cover same-merchant concurrent creation, cross-merchant URL aliases, stale versions and preservation of unrelated rows; eight integration cases collect locally but require CI PostgreSQL. New Playwright suite collects 32 cases; actual browser execution uses the ordinary dedicated CI workflow, not a workaround for the previously denied local service launch.
