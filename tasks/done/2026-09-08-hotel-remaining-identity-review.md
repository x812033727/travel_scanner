---
id: 2026-09-08-hotel-remaining-identity-review
title: Hotel remaining identity review
status: done
priority: P1
area: ops
owner: codex-hotel-remaining-review
claimed_at: 2026-09-08T21:17:53Z
created_at: 2026-09-08T21:17:40Z
completed_at: 2026-09-08T21:52:53Z
branch: codex/hotel-review-remaining-20260909
depends_on: []
scope:
  - docs/hotel-review-remaining-20260909
  - ops/hotel_review_remaining_20260909.py
---

# Hotel remaining identity review

## Why

User renewed hotel review with the built-in browser or Gemini. Previous batches are
immutable; current live inventory has 20 pending hotels and 105 pending options.
Obtain genuinely new exact-identity evidence, not duplicate reviews of unchanged gaps.

## Definition of done

- [x] Record actual new primary/IAB evidence with exact identities and honest gaps.
- [x] Apply only eligible, newly evidenced pending subset through normal admin services.
- [x] Preserve full 420-row membership, original 295 approved rows, settings and receipts;
      verify audit attribution, replay and five-locale public visibility.

## Steps

- [x] Read existing contracts and capture new live baseline.
- [x] Research missing platform URLs and three Kyoto map identities without guessing.
- [x] Guarded operator, tests, backup, dry-run/apply and independent verification.

## How to verify

New snapshot/manifest row hashes, normal version checks, offline operator tests,
Ruff, independent SQL snapshots, receipt replay and public locale/city GETs.

## Notes

Fresh baseline semantic SHA256 c938d83913645ac6a7651eca0e705621b33b40bb235905392c54917492bdb03d.
60 products and 360 options; 40/255 already approved. Preserve previous evidence.
Gemini catalog-review only supports hotspot/food/merchant, so do not disguise hotel
as another type or bypass shared quota. No paid API, quota increase, booking/clickout,
affiliate activation, app code deployment, GitHub push/merge, or canonical dirty edits.

Completed this bounded evidence batch: 27 receipts, 21 approved new option URLs,
3 normal-link-guard rollbacks and 3 unchanged Kyoto map holds. All 60 products,
original 295 approved rows, settings, old 357 receipts and historical audits unchanged.
Actual untouched rows 399; normal edit/review audits 21 each; replay zero additions.
Public options 183 -> 192, all 90 locale/city GET checks passed; 92 offline tests and
scoped Ruff passed. First read-only SQL type mismatch fixed before any mutation;
failed output retained, v2 SQL passes all three phases. Final /ready is healthy.

This does not mean all hotels are publishable: 20 products / 84 options remain
pending (73 URL-null), explicitly listed with evidence age and missing requirements
in docs/hotel-review-remaining-20260909/remaining-items.json. Existing broader hotel
readiness task remains open. See REPORT.md and verification-report.json for proof.
