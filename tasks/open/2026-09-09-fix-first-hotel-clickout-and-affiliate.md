---
id: 2026-09-09-fix-first-hotel-clickout-and-affiliate
title: Fix first hotel clickout and affiliate availability feedback
status: in-progress
priority: P1
area: web
owner: codex-hotel-clickout
claimed_at: 2026-09-09T12:30:33Z
created_at: 2026-09-09T12:30:33Z
completed_at:
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

- [ ] Discovery hotel official and affiliate options succeed on the first valid POST.
- [ ] Retry preserves all valid placement/context values; unknown placements remain rejected.
- [ ] Desktop/mobile browser fixtures and real API contract tests cover this previously missed entry.

## Steps

- [ ] Unify frontend placement type/retry allowlist and backend annotation/campaign allowlist.
- [ ] Test, document verified root cause and open a PR; no unrequested activation or deployment.

## How to verify

Focused pytest contract tests; ESLint, TypeScript, Vitest, i18n, production build, desktop/Pixel Playwright. Browser fixtures block external hosts and do not represent real OTA tracking verification.

## Notes

Canonical checkout is dirty and untouched. Base is a8be96cd; prior merged Stay22 task closure is carried as metadata. User Chrome connection disappeared during tool initialization, so browser acceptance uses isolated Chromium tests; production request logs provide direct reproduction evidence. No live clickout, provider activation or account setting change performed by this fix.
