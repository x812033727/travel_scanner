---
id: 2026-09-08-travelpayouts-live-destination-activation
title: Complete live Travelpayouts brand and destination offer verification
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-09-08T06:54:47Z
completed_at:
branch:
depends_on: []
scope:
  - docs/travel-services.md
---

# Complete live Travelpayouts brand and destination offer verification

## Why

PR #358 supplies the destination-offer catalog for 33 destinations; the operational
brand review and offer matrix still require live verification before publication.
Deploying the code does not create or approve these entries.

The observations below are the 2026-09-08 deployment handoff, not a statement
of the current deployed SHA, live account approvals, catalog counts or release
settings. This 2026-09-09 documentation integration only reconciles source at
main a899437aaf2f60c7affe2e944d49d62216537c90; it performs no live verification,
approval, publication, clickout or deployment.

## Definition of done

- [ ] Reconcile current Project 570089 Available brands using a working signed-in browser.
- [ ] Create and verify applicable brand/destination/module landing pages for all 33 destinations.
- [ ] Publish only entries passing brand, tracking, destination and final-page checks.
- [ ] Verify real clickout 303 redirects and recorded brand/destination analytics.

## Steps

- [ ] Restore browser attachment or perform human review of brand project status.
- [ ] Resolve Klook/KKday HTTP 403 landing verification without bypassing protection.
- [ ] Establish authorized evidence for KKday's invl.me intermediary before allowlisting.
- [ ] Reconcile channels separately: the later direct Klook integration does not establish Travelpayouts project approval or destination-offer acceptance.

## How to verify

Use /admin/travel-services destination offers and release controls. Test each
brand through the existing shared Partner Links client; conversion success alone
does not establish a verified destination. Read the public destination API and
sample a real clickout per approved brand. Preserve existing content gates.

## Historical observations: 2026-09-08

At that observation, server account Project 570089 was enabled with token and marker configured.
Klook/KKday had same-day approved/enabled database brand records; Booking/Trip.com
were pending/disabled. Before this deployment there were no affiliate product
offers and only six destinations enabled in catalog release settings.

Native Partner Links with shorten=true returned aviasales.tpx.gr, klook.tpx.gr,
kkday.tpx.gr, rejected by existing allowlists. PR #363 switches to documented full
links and a fresh cache namespace; Kiwi.com is static-only per official API docs.
Full-link probe: Aviasales -> HTTP 200; Klook -> affiliate.klook.com -> exact Klook
path HTTP 403; KKday -> invl.me -> exact KKday path HTTP 403. These are not approved
landing checks, and no offer was published based on them.

Browser attachment timed out twice. Native computer-use then stopped because it
could not reliably identify the current browser URL. No subsequent GUI actions
were attempted and no old screenshot was treated as current account approval.

## Historical deployment evidence: 2026-09-08 07:06 UTC

- PR #358 merged as 737cdbb20c80e7bc4aa651590bfd63800d1b692d.
- PR #363 merged as bdd01b64ed371deec53160c754c21390968dc3f9, the SHA deployed during this operation.
- Exact main CI 34197059294 passed all four jobs: API 1872 passed / 3 skipped,
  Web 790 unit tests and 230 browser tests, 12 full-stack journeys, and containers.
- Verified head and merge trees match c4c82f072bb9cfc671b89be7ed436f26e9165973.
- Deployment at 2026-09-08 07:06 UTC used the existing Compose project/runtime
  settings, a mode-0600 8,916,158-byte PostgreSQL backup with readable archive index,
  and migration 0063_destination_offers. At that verification, all eight app services ran the deployed
  SHA with zero restarts; PostgreSQL/Redis were not recreated. Readiness passed
  repeatedly and community/registration state plus environment checksum matched.
- Post-deploy HTTP verification: 215 requests, no unexpected status or contract
  errors. All 33 destination pages, 165 destination/module queries and five
  localized disclosure responses passed. This validates empty-state behavior,
  NOT completed brand activation: destination_offer_count was zero in that snapshot.
- Native (unmodified) deployed Partner Links client produced tp.media URLs for
  Aviasales/Klook/KKday with matching configured marker and Project 570089; repeat
  lookups matched cache. Aviasales final page returned 200. Klook returned 403;
  KKday has an unallowlisted invl.me hop and final page 403. Neither is approved by
  these checks. Existing catalog gates and brand review states were not changed.
- No signed-in live browser acceptance was completed because browser control
  stopped as noted above. No test booking, public offer, or brand approval was made.

## Later source integration, not live approval

Fixed main includes the separate Klook direct-affiliate implementation from
PR #370 / 29c36b258789d3750d3620cceb3a8d1da7fc59df. See
[its integration guide](../../docs/klook-integration.md) for the independent
enrollment, product/link review and pending-import boundaries. Its merged code
and recorded account evidence do not complete the Travelpayouts 33-destination
matrix above, transfer approvals between channels, or establish price API rights.
All live verification items in this task remain open. Check actual current state
under a separately authorized operational review before changing any gate.
