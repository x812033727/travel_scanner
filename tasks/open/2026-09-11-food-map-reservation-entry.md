---
id: 2026-09-11-food-map-reservation-entry
title: Fix food map and reservation entry points
status: blocked
priority: P1
area: web
owner: codex-food-map-reservation-entry
claimed_at: 2026-09-11T03:51:31Z
created_at: 2026-09-11T03:49:54Z
completed_at:
branch: codex/food-map-reservation-entry
depends_on: []
scope:
  - apps/web/components/merchant-external-links.tsx
  - apps/web/components/merchant-external-links.test.tsx
  - apps/web/components/food-dish-card.tsx
  - apps/web/components/food-dish-card.test.tsx
  - apps/web/components/food-merchant-card.tsx
  - apps/web/components/food-merchant-card.test.tsx
  - apps/web/components/discovery/card.tsx
  - apps/web/components/discovery/card-details.test.tsx
  - apps/web/components/discovery/detail-drawer.tsx
  - apps/web/components/discovery/detail-drawer.test.tsx
  - apps/web/messages/en/foods.json
  - apps/web/messages/ja/foods.json
  - apps/web/messages/ko/foods.json
  - apps/web/messages/zh-TW/foods.json
  - apps/web/messages/zh-CN/foods.json
  - apps/web/e2e/food-map-reservations.spec.ts
  - apps/api/tests/test_discovery_flow.py
  - docs/catalog-content-reviews/2026-09-11-reservation-links.md
  - docs/catalog-content-reviews/2026-09-11-reservation-links.json
---

# Fix food map and reservation entry points

## Why

Discovery food details omit supplied maps/reservation links; merchant details link back to themselves. Provide explicit safe external actions without changing publication gates, then research public merchants' reservation pages separately.

## Definition of done

- [ ] Shared map/reservation/official-site actions work in discovery, dish and merchant cards, five locales and small screens.
- [ ] Nested merchant detail returns to food then results with filters, scroll and focus preserved; no self-link loop.
- [ ] Relevant API/component, translation, types, lint, production build and browser fixtures pass.
- [x] Record fresh public inventory and per-merchant reservation research separately from UI completion; only independently verified links may be applied.

## Steps

- [x] Fetch latest main and create isolated worktree; retain unrelated work and prior moderation data.
- [x] Implement shared external actions and detail navigation.
- [ ] Validate and conduct finite original-platform checks using the in-app browser.

## How to verify

Run relevant Vitest suites, API discovery/platform tests, npm check:i18n/typecheck:web/lint:web/build:web/check:tasks and Playwright food-map-reservations fixtures. Distinguish fixture E2E from live third-party evidence. No provider requests in application tests.

## Notes

Base d0ec33ee6d39a4bd8e2a39275b55cc675ddf5095. Fresh GitHub checks confirm old overlapping tasks' PR374 merged a899437a and PR378 merged95122362; both are ancestors of main, source files clean in prior worktree and prior release-record task marked done there. Main retains old review task metadata. Used explicit task-tool --force for the new isolated follow-up only, leaving other owners' task files unchanged; no overlap with current security/hotel work.

Parallel ownership: root discovery/card/detail-drawer and their tests; merchant_external_ui shared component, legacy cards and five foods catalogs; food_links_acceptance E2E and API test; reservation_inventory public inventory, drawer unit tests, and research reports. No PR/merge/deploy. The hotel coordinator's initial production-write pause for PR389 was respected; release is recorded below. No production mutation was attempted.

## Implementation and validation handoff

- Shared `MerchantExternalLinks` renders the original approved primary/secondary map URLs, all valid reservation links, and a distinct official website action. HTTPS/host/branch-page checks, no invented fallback URLs, new-tab accessibility labels, minimum 44px targets, narrow-screen stacking, five-language platform-language and empty-state copy.
- Discovery food rows keep internal merchant titles; merchant details show address/actions without a self-referential where-to-eat section. Boundary-owned navigation restores the parent detail's actual scroll body and remounted merchant focus, then returns to the originating list. Modified clicks are not added to local history ownership.
- Relevant Vitest run: **12 files / 135 tests passed**. API `tests/test_discovery_flow.py`: **56 passed**, including all seven providers/five locales, publication and URL gates; new cases block provider client construction. Scoped API Ruff passed.
- `check:i18n` (5 locales / 25 namespaces), `typecheck:web`, full `lint:web`, and final `build:web` all exit 0. Final rebuild compiled in 6.9s, TypeScript in 4.1s, 278 pages generated. `git diff --check` clean. `check:tasks` passes with pre-existing stale/overlap warnings recorded above.
- E2E file defines 16 distinct cases covering five locales, explicit 320/390/1280 viewports and light/dark loops. Playwright `--list` and ESLint pass, but **the actual browser suite has not run**. Do not treat its assertions as verified visual evidence.
- Local Next start was explicitly rejected by execution policy (no process created); no alternate launch was attempted. User was asked to start port 3316 manually. A read-only probe confirms port 3316 is not yet listening. The task is waiting for that external action, not a code/build failure.
- An isolated API visibility fixture is running at 127.0.0.1:8316 (owned PID 12536, exec session 63927) for the requested manual test startup. It is synthetic, with no DB or paid providers. Keep it for the imminent user handoff; terminate it after E2E is complete. All Playwright external URLs are intercepted and never reach providers.

Manual test startup, in this worktree's `apps/web`:

```powershell
$env:API_INTERNAL_URL='http://127.0.0.1:8316'
npm run start -- --hostname 127.0.0.1 --port 3316
```

Then run the existing test server only (do not change the rejected launch into another automated launch):

```powershell
$env:PLAYWRIGHT_BASE_URL='http://127.0.0.1:3316'
$env:PLAYWRIGHT_REUSE_EXISTING='true'
npx playwright test e2e/food-map-reservations.spec.ts --project=desktop-chromium --workers=2
```

## Separate reservation research

Fresh inventory: 331 public / 331 map links / 3 existing platform links; all 96 previously returned IDs still excluded. In-app original-page checks covered the first 10 merchant identities; seven new same-branch platform candidates and the existing Yat Lok photo-to-overview correction remain **unapplied**. Three of these ten platform pages display a booking interface, six Chope pages explicitly do not accept Chope bookings, and one OpenRice page does not establish booking capability. No dates, seats or actual reservations were checked. The other 321 merchants remain not started, not "not found".

See `docs/catalog-content-reviews/2026-09-11-reservation-links.{md,json}` for exact per-ID evidence and application boundaries. General admin Save PATCHes the entire merchant before PUTting its platform, so no production saves were made solely to record platform notes. A later platform-only application must re-read current rows and use the existing dedicated authorized PUT with ordinary audit records.

The hotel coordinator released the deployment write pause after 04:04:42 UTC, with merchant/platform fingerprints unchanged on main 5e3168e18174427c9ce4ed5b7219517ad3d1f4aa. This food task itself has not merged, deployed, or changed production data. Reconcile current main and rerun checks before any later PR/merge request.
