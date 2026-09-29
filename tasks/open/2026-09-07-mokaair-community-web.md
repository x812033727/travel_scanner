---
id: 2026-09-07-mokaair-community-web
title: Mokaair community responsive web and five-language experience
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-07T10:14:21Z
completed_at:
branch: codex/p1-task-audit
depends_on: []
scope:
  - apps/web/e2e/community.spec.ts
  - apps/web/e2e/community-ui.spec.ts
  - apps/web/components/community
  - docs/community-local-acceptance-2026-09-29.md
  - .github/workflows/ci.yml
---

# Mokaair community responsive web and five-language experience

## Why

Deliver the approved international travel community and reviewed pet-friendly
experience within the existing five-locale Web/PWA, without exposing private trips.

## Definition of done

- [x] Base responsive discovery, publishing, profiles, collections, messaging and
      moderation are implemented; merged #340 historical browser evidence is below.
- [x] Pet filters and trip companion requirements expose uncertainty instead of guessing;
      merged real-service evidence and fresh local contracts are recorded below.
- [x] New copy exists in all five catalogs; closed/unavailable states fail safely.
- [ ] Expanded five-locale/light-dark browser acceptance, including translation
      failure and revised originals, passes at the current change's exact CI head.

## Steps

- [x] Shared state, accessible UI and conservative server-side feature gates.
- [x] Wire the base content, social, pet and administration flows to the real BFF.
- [ ] Complete the expanded real-service permissions/responsive/keyboard/failure matrix.

## How to verify

Run npm run test:web, check:i18n, typecheck:web, lint:web and build:web. Run the
community Playwright suite on desktop and Pixel 7 against isolated services.

## Notes

Checkpoint: rebased onto main 54009ba. CI 34130887751 passed Web components,
TypeScript, lint, five-locale checks, the default production build and isolated
desktop/Pixel 7 UI tests. Existing real-stack travel journeys also pass after
fixing a community Provider remount which reset core forms during auth hydration.
New regressions preserve core state and prevent cross-account community caches.
The real SMTP/MinIO community journey reached blocking on both devices; update
assertions to distinguish an unfollowed read-only thread from a hidden blocked
thread, and verify rejected writes never enter delivered history.
Pet/account lifecycle browser acceptance remains open. Local Webpack build passes;
default Turbopack cannot use this workspace's shared node_modules junction.
Draft PR #340 must not enable production or claim complete plan acceptance.

Follow-up: CI 34133067407 passed 130 component files, 172 isolated browser tests,
and four real-service community journeys (publication/messages and SMTP
reset/deletion on desktop and Pixel 7). Both pet-review journeys still time out;
retain secondary admin traces and preserve the original failing action on teardown.
Scoped image retry and shared-session reset/verification regressions pass locally.
Pet AI candidate failures now use the five-language catalog in ordinary trip tools.
General hotspot/merchant associations now use a shared search picker and typed
reference contract. The editor retains selections on error and saves only IDs;
previews, moderation and public posts display server-resolved place names/links.
Focused component tests cover edits, retries, duplicates, limits and layout gates.
Exact-head real-service acceptance is still required.

CI 34135827036 confirms desktop/Pixel 7 pet species filters after the auth-hydration
fix. The next pet test step must open the current planner's tools drawer first.
A test-only TypeScript role-option error also needs the next full CI verification.

Integrated main f2c3b2a. BFF timeout resolution retains community streams/media,
hotel clickouts, booking-option review and hotel quote-search deadlines together.
The next CI run must validate the actual merge with main, not only the feature head.

CI 34137517824 / 43d0481 passed 132 Web component files, 208 isolated browser
tests, typecheck, lint, five-locale catalogs and default production builds.
Real pet tests exposed initial preference loading overwriting early edits.
e096aeb disables those controls until loaded, preserves dirty drafts and their
CAS version, and binds conflict confirmation to its original version. New focused
regressions pass; the expanded real reconnect and pet flows await full CI.

Full CI 34138592625 / e096aeb passed 779 component tests, 208 isolated browser
tests and all six real community journeys, including offline catch-up and pet
place publication. A repeat exposed a backend comment/fork deadlock; fork E2E
now records the POST result directly so server errors are not hidden by a URL timeout.

Built on isolated main 516713d. The existing forgot-password task owns the login
entry; this task owns the new confirmation/recovery UI and public community pages.

### 2026-09-29 local P1 reconciliation (codex-p1-product)

Claimed for the owner-authorized P1 review. The matching implementation PRs are
merged and no matching open PR or active same-feature implementation was found.
The former broad scopes have been narrowed to this local acceptance work. Forced
claims only bypass historical/shared scope metadata; no other agent application
changes are taken over. No production or cloud-account access is included.

Added `e2e/community-ui.spec.ts` and included it in the required Web CI job.
Its 20 synthetic Chromium cases cover five locales, light/dark and desktop/Pixel 7:
feed/post rendering, translation 503 preserving the original, successful retry,
a normal reaction refresh receiving a newer original, stale translation removal,
new-revision translation, show-original, report Escape/focus return and overflow.
Unexpected browser writes and external requests are blocked and asserted absent.

Local ESLint and 20-case discovery passed; existing community component tests
passed **10 files / 52 tests**. Next production build and TypeScript passed with
348 pages. API community/discovery contracts passed **52 / 8 skipped** separately.
These results are not browser execution. Automatic approval review rejected
starting the loopback Next preview with `blocked by policy`; CUA had no browser
surfaces (IAB unavailable, Chrome creation timed out). No equivalent launcher was
used. The new matrix remains **authored, pending exact-head CI execution**.

See `docs/community-local-acceptance-2026-09-29.md`. Real PostgreSQL/Redis/MinIO/
Mailpit/worker outage/capacity and the full real-service locale matrix remain open.
