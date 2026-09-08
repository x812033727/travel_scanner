---
id: 2026-09-08-hotel-held-evidence-followup
title: Hotel held-evidence follow-up review
status: done
priority: P1
area: ops
owner: codex-hotel-review-followup
claimed_at: 2026-09-08T16:20:12Z
created_at: 2026-09-08T16:19:51Z
completed_at: 2026-09-08T16:55:12Z
branch: codex/hotel-review-followup-20260909
depends_on: []
scope:
  - docs/hotel-review-followup-20260909
  - ops/hotel_review_followup_20260909.py
---

# Hotel held-evidence follow-up review

## Why

User renewed the request to review hotels with the built-in browser or Gemini.
The previous batch is complete and immutable; fresh production baseline still has
20 pending products and 154 pending booking options. Work only on newly evidenced
pending entries, never replay the old import/review manifests over current versions.

## Definition of done

- [x] Newly obtained identity/location evidence is recorded without guessing IDs or copying restricted coordinates.
- [x] Eligible existing pending entries use normal versioned admin review and attributable atomic receipts.
- [x] Verify preserved rows/settings, replay, and public five-locale visibility; document remaining blockers honestly.

## Steps

- [x] Capture fresh live baseline and recover IAB with a fresh kernel.
- [x] Recheck 54 provider URLs; verify three Kyoto CC0 candidates; record failed exact-map UI attempts without approving products.
- [x] Check a bounded new official Busan administrative-coordinate route; original file returned 403, so all 10 products stay pending.
- [x] Backup, guarded dry-run/apply, independent verification and report.

## How to verify

Offline operator regression tests/Ruff and task checks. New immutable live baseline,
per-row version/hash locks, normal admin services, independent READ ONLY/REPEATABLE READ
SQL snapshots, complete changed-row diff, idempotent replay and 30 public locale/city GETs.

## Notes

before.json captured 2026-09-08 16:20:20 UTC; semantic SHA256
d9823e0996ad09ba14fe05b2e9a674544544d4dacb7b87d6fac288be5e51453c.
60 hotel products/360 options; 40 products and 206 options already approved.
No quota changes, paid quote calls, booking/clickout, affiliate activation or deployment.
Preserve old docs/hotel-review-all-20260908 and its operator. Original dirty checkout untouched.

Completed scoped evidence batch: 67 receipts = 49 option approvals + 5 option holds +
13 product holds. All 60 products and 371/420 full rows unchanged; original 246
approved rows preserved. Replay reuses all 67 receipts; independent SQL confirms
normal option audits +49, no other settings/related tables/old receipts changed.
Public 40 hotels/183 options (was 165), all 30 locale/city cases pass.
Current remaining 20 products/105 options require more evidence; this task's
bounded follow-up is complete, not a claim that the entire catalog is publishable.
See docs/hotel-review-followup-20260909/REPORT.md for exact gaps and next evidence.
No application deployment or GitHub writes. Backup index readable, not full restore tested.
