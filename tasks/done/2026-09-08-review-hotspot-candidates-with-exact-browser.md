---
id: 2026-09-08-review-hotspot-candidates-with-exact-browser
title: Review hotspot candidates with exact browser identities
status: done
priority: P1
area: ops
owner: codex
claimed_at: 2026-09-08T09:08:14Z
created_at: 2026-09-08T09:06:33Z
completed_at: 2026-09-08T09:34:34Z
branch: codex/catalog-review-all-20260908
depends_on: []
scope:
  - docs/hotspot-review-2026-09-08.md
  - ops/hotspot_review_20260908.py
  - ops/hotspot_review_20260908.json
---

# Review hotspot candidates with exact browser identities

## Why

The user requests evidence-based hotspot candidate review using the built-in browser or Gemini. The remaining 1,780 candidates lack exact map identities; this follow-up verifies an explicit 12-candidate Taipei/Kaohsiung batch against current official sources, permitted map IDs and independent durable coordinates. It does not blanket-approve the backlog.

## Definition of done

- [x] Each of the 12 candidates has a documented current-source decision; unresolved or closed places remain pending.
- [x] Publication uses exact verified map identity, independent source inspection, durable coordinates and existing publication gates.
- [x] Any production changes have a fresh verified backup, real administrator attribution, full-snapshot guard and replay-safe audit receipt.
- [x] Actual applied outcomes and remaining backlog are reported without claiming completion of all candidates.

## Steps

- [x] Verify official venue/tourism sources and map identities in the built-in browser.
- [x] Dry-run and apply only the explicit reviewed manifest through existing review services.
- [x] Verify publication eligibility, audit receipts and idempotent replay; record evidence.

## How to verify

Run the scoped one-off script snapshot, dry-run, apply and replay in the existing API container under deployment locks. Verify PostgreSQL backup index, publication gaps and SQL audit/count results. Run Python compilation/lint and repository task checks locally.

## Notes

No new discovery, quota increase, code deployment or remote Git mutation. Google data is used only for exact permitted place IDs and editorial identity matching; coordinates must come from independent durable sources. Current announcements supersede stale tourism pages. Partial venue closure must not be represented as unrestricted access.

Operationally completed 2026-09-08: 11 approved, Sun Yat-sen Memorial Hall kept pending. Backlog 1,780 -> 1,769. 12 normal audits + 12 atomic source receipts, replay produced no duplicates. Current derived rankings refreshed from existing signals only (one audited refresh); 60 public BFF locale searches verified. Full evidence and source/coordinate caveats in docs/hotspot-review-2026-09-08.md. The finite batch is done, not the whole backlog. Local artifacts only, no PR/push/deployment performed by this task.
