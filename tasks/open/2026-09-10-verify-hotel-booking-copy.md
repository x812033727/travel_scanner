---
id: 2026-09-10-verify-hotel-booking-copy
title: Verify simplified hotel booking copy without changing affiliate flow
status: review
priority: P2
area: web
owner: codex-hotel-copy-tests
claimed_at: 2026-09-10T00:47:25Z
created_at: 2026-09-10T00:46:05Z
completed_at:
branch: codex/hotel-booking-copy
depends_on: []
scope:
  - apps/web/components/travel-services/booking-panel.test.tsx
  - apps/web/e2e/stay22-allez.spec.ts
---

# Verify simplified hotel booking copy without changing affiliate flow

## Why

The requested copy cleanup must hide the per-platform Stay22 badge and long
editorial source notes without removing the general commission disclosure,
source/license attribution, stored metadata or the native booking submission.

## Definition of done

- [x] Booking panels omit the Stay22 badge and retain the general commission disclosure.
- [x] Source disclosure says "資料來源", retains source/publisher/license links and does not render changes notes.
- [x] Native first-party POST, booking context, retry, security and responsive browser assertions remain intact.
- [x] Focused unit tests pass; root coordinates the production build and desktop/mobile browser validation.

## Steps

- [x] Inspect existing assertions and preserve all non-copy affiliate behavior coverage.
- [x] Add source-credit fixtures and strengthen existing desktop/mobile booking flows.
- [x] Run focused Vitest and hand off browser checks without starting a competing build/server.

## How to verify

From apps/web: npx vitest run components/travel-services/booking-panel.test.tsx
components/travel-services/catalog.test.tsx
components/travel-services/stay22-admin.test.tsx lib/stay22-allez-copy.test.ts
--pool=threads --maxWorkers=1. After the root's coordinated production build:
PLAYWRIGHT_SERVE_BUILD=true npm run test:e2e --workspace @travel-scanner/web --
stay22-allez.spec.ts --workers=1. The existing 22 browser cases retain loopback
fixtures, block external traffic and never issue real affiliate clicks.

## Notes

This task edits only the two test files and this record. Product JSX/translations
belong to the parent. The fixtures keep affiliate_channel=stay22 and nonempty
source changes data: absence must be a rendering change, not deletion of inputs.
Browser source/license anchors are inspected but never followed. Existing source
and license security attributes, optional dates/party, first-click/retry behavior,
no-prefetch, no-opener, 44px targets, focus restoration and overflow checks remain.

Validation on 2026-09-10: all four focused Vitest files passed, 41 tests in 15.38s
(booking panel/source credits, catalog, Stay22 admin and five-language Allez copy).
The first new-source test run exposed unavailable jest-dom matchers in this file;
the assertions now use native DOM attributes like the existing tests, and the full
focused rerun passed. A prior startup run was deliberately stopped while the
parent replaced temporary dependency junctions with an independent npm install.

No product code, settings, booking targets or backend data were changed by this
test task. Production build and the updated 22 desktop/Pixel 7 browser cases are
handed to the parent; this local unit result does not claim those browser checks
have run or any real affiliate request has occurred.

Parent verification afterward: production build, standalone TypeScript, full Web
ESLint and five-language checks passed. All 22 updated browser cases passed on
Desktop Chromium and Pixel 7 in 47.8s using the production build, including the
real local BFF header/retry cases. Parent inspected desktop/mobile screenshots.
No real affiliate click, source navigation or production mutation was performed.
