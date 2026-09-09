---
id: 2026-09-09-fix-first-hotel-clickout-and-affiliate
title: Fix first hotel clickout and affiliate availability feedback
status: done
priority: P1
area: web
owner: codex-hotel-clickout
claimed_at: 2026-09-09T12:30:33Z
created_at: 2026-09-09T12:30:33Z
completed_at: 2026-09-09T13:04:18Z
branch: codex/hotel-first-click-fix
depends_on: []
scope:
  - apps/web/components/travel-services/booking-panel.tsx
  - apps/web/components/travel-services/booking-panel.test.tsx
  - apps/web/app/api/travel
  - apps/web/lib/hotel-clickout-error.ts
  - apps/web/lib/hotel-clickout-error.test.ts
  - apps/web/lib/hotel-booking-placement.ts
  - apps/web/e2e/stay22-allez.spec.ts
  - apps/api/app/travel_services
  - apps/api/tests/test_stay22_routes.py
  - docs/hotel-first-click-fix.md
---

# Fix first hotel clickout and affiliate availability feedback

## Why

Production API logs show three first-click POSTs with placement=discovery returning 422, followed by retry POSTs without that parameter returning 303. Discovery uses the shared BookingPanel but the backend placement Literal and recovery-page allowlist omitted this actual caller.

## Definition of done

- [x] Discovery hotel official and affiliate options succeed on the first valid POST.
- [x] Retry preserves all valid placement/context values; unknown placements remain rejected.
- [x] Desktop/mobile browser fixtures and real API contract tests cover this previously missed entry.

## Steps

- [x] Unify frontend placement type/retry allowlist and backend annotation/campaign allowlist.
- [x] Test, document verified root cause and open a PR; no unrequested activation or deployment.

## How to verify

Focused pytest contract tests; ESLint, TypeScript, Vitest, i18n, production build, desktop/Pixel Playwright. Browser fixtures block external hosts and do not represent real OTA tracking verification.

## Notes

Canonical checkout is dirty and untouched. Base is a8be96cd; prior merged Stay22 task closure is carried as metadata. User Chrome connection disappeared during tool initialization, so browser acceptance uses isolated Chromium tests; production request logs provide direct reproduction evidence. No live clickout, provider activation or account setting change performed by this fix.

PR #382: backend 259 tests, focused frontend/BFF 46 tests, Chromium desktop/Pixel 20 tests, task tooling 15 tests, Ruff, targeted mypy, ESLint, TypeScript, i18n and production build passed. Linux CI remains authoritative for the full suite. Wait for explicit merge/deployment authorization; no production setting or hotel review change belongs to this patch.

Follow-up: the user explicitly approved merge/deployment. All 12 PR checks passed;
PR #382 merged as d9ef8fcd3565ae3ddd02751d334e662e20412a99, merged-main CI passed
and the exact commit deployed successfully with backup and preserved runtime/data.
Official and Booking discovery first POSTs returned 303 without following external
redirects. The user separately authorized Booking via Stay22; this was saved through
their authenticated admin UI (version7, mokaair, Bookingonly), not bundled into the
code patch. Missing hotel Booking URLs and a pre-existing global Referrer-Policy
override have separate open follow-ups. See the scoped rollout document for evidence.
