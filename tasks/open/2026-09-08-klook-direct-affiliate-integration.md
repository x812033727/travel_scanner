---
id: 2026-09-08-klook-direct-affiliate-integration
title: Klook direct affiliate product integration and reviewed rollout
status: in-progress
priority: P1
area: api
owner: codex-klook-root
claimed_at: 2026-09-08T16:43:31Z
created_at: 2026-09-08T16:29:02Z
completed_at:
branch: codex/klook-product-integration
depends_on: []
scope:
  - docs/klook-integration.md
  - docs/klook-products
  - apps/api/app/travel_services/klook_catalog.py
  - apps/api/tests/test_klook_catalog.py
  - apps/web/e2e/travel-services.spec.ts
---

# Klook direct affiliate product integration and reviewed rollout

## Why

Connect the user's approved Klook affiliate account to useful hotel, day trip,
airport transfer and connectivity discovery without requiring Travelpayouts or
pretending affiliate enrollment grants price API access.

## Definition of done

- [x] Explicit independent Klook enrollment, safe tracked clickouts and truthful UI.
- [x] Source-backed, additive pending product manifest with preview/apply/replay tests.
- [x] Existing hotel facts, other booking platforms and review states preserved.
- [ ] Desktop / Pixel 7 browser checks and proportional API / Web regression validation.
- [ ] PR with evidence and rollout instructions; production activation requires its own review.

## Steps

- [x] Start isolated branch from latest origin/main; leave original dirty checkout untouched.
- [x] Verify account AID and documented link format using the authenticated internal browser.
- [x] Integrate channel-aware backend and five-language catalog/admin UI from bounded agents.
- [x] Record verified source identities and test safe additive pending imports.
- [ ] Run checks, review diff and open PR.

## How to verify

API: Ruff, mypy, focused and full pytest, Alembic upgrade/heads (fresh PostgreSQL in CI).
Web: ESLint, TypeScript, Vitest, i18n, production build, travel-services.spec.ts
desktop Chromium and Pixel 7. No production API calls, bookings, paid queries or bulk publication.

## Notes

Klook's official text-link tool documents https://www.klook.com URLs with aid;
s.klook.com does not track. Account enrollment is independent from product/link review.
API inquiry is submitted but not approved. Use no scraped prices, inventory or images.
The original models.py is dirty and remains untouched; clean-worktree model scope
must be handed over by the merchant task owner before backend editing.

## Development evidence

- Original merchant owner verified its historical claim and released only models.py;
  task-only handoff eef3671 cherry-picked as e7ac316. Original dirty checkout untouched.
- Backend focused channel tests: 47 passed / 2 PostgreSQL-only skipped. Broader
  service/affiliate/provider/hotel tests: 236 passed / 25 skipped before final redirect cases.
- Additive importer: 36 passed. Manifest: 10 unique activity products, one exact
  hotel link, two candidate-only sources; no production writes or new approvals.
- Web owned regression: 84 passed; TypeScript, whole ESLint, i18n and production
  Turbopack build passed. Tools: 27 passed; task validation 190 files.
- New Klook Playwright: 20 passed across five locales, desktop Chromium and Pixel 7.
  Initial filter-history assertion incorrectly expected push per filter; actual
  existing replaceState is intentional. Test now verifies reload and back between
  pages; no assertion timeout or application navigation change.
- Whole Ruff and mypy (262 sources) passed. Alembic head0064; no local Docker/PG.
  Real0063/freshmetadata migration tests remain PostgreSQL-gated for CI.
- Full Web run became very slow and showed a failure in unchanged
  itinerary-place-browser.test.tsx before interruption; isolated rerun and full CI
  still required. Do not describe the incomplete local run as passing.
- Full local API: 1903 passed / 122 skipped / one existing AsyncMock warning;
  Linux-only deployment_center excluded on Windows. This was before the final
  alias/privacy patch; final related bundle 152 passed / 2 PG-only skipped.
- Complete 126-case existing/new travel-service Playwright passed (4.7 minutes).
  Console destination-stream-close errors occurred during navigation, but no
  assertion failed; not claiming those pre-existing transport errors were fixed.
- Isolated unchanged itinerary-place-browser rerun: 7 passed without edits.
  Complete Web retry is still running; latest-SHA Linux CI is authoritative.
- Independent review found a Klook short/detail alias inconsistency across hotel
  health, public option matching and clickout. Fixed only for the same typed
  numeric hotel identity, with bidirectional booking-query context preservation;
  changed IDs/categories/subdomains remain rejected. Generic Klook template
  tracking uses only coarse module/locale, never a member/trip-derived identifier.
