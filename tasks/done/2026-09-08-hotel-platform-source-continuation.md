---
id: 2026-09-08-hotel-platform-source-continuation
title: Hotel platform source continuation
status: done
priority: P1
area: ops
owner: codex-hotel-platform-review
claimed_at: 2026-09-08T23:36:46Z
created_at: 2026-09-08T23:36:46Z
completed_at: 2026-09-09T00:19:26Z
branch: codex/hotel-platform-sources-20260909
depends_on: []
scope:
  - docs/hotel-review-platforms-20260909
  - ops/hotel_review_platforms_20260909.py
---

# Hotel platform source continuation

## Why

Continue the user's hotel review with new browser-verified platform identities.
Research the remaining empty Osaka/Taipei Expedia/Agoda slots and one existing
Kyoto Agoda URL whose actual localized landing page can resolve an earlier guard hold.
No product publication, map overrides, quote activation, paid API or deployment.

## Definition of done

- [x] Review only newly evidenced exact identities with ordinary versioned admin routes.
- [x] Preserve all 60 hotel products, 319 previously approved rows, out-of-scope
  options, quotes/settings, original receipts and historical audits.
- [x] Verify actual results, full-row rollback of guard failures, replay, normal
  audit pairing and public additions only under already-approved parents.

## Steps

- [x] Capture fresh baseline and research bounded Osaka/Taipei candidates.
- [x] Confirm each selected hotel name/full address in IAB; record actual landing URLs.
- [x] Compile exact manifest, dry-run, protect a new backup and apply normal review.
- [x] Complete independent SQL, public matrices, offline tests and remaining-item report.

## How to verify

Use the existing API Python runtime with PYTHONPATH=apps/api, scoped Ruff with
apps/api/pyproject.toml, full-row/receipt verifier, RR READ ONLY SQL in three phases,
and anonymous six-city/five-locale public GETs before/after/replay. New evidence lives
only in docs/hotel-review-platforms-20260909. Use a new tag; never rewrite prior receipts.

## Notes

Baseline 2026-09-08 23:37:42.330750+00:00; semantic SHA256
7b86b02a40dfe00946f1df45d8e201e3dc59bf49066469c30dbfcc60f5628e49.
60 products (40 approved/20 pending), 360 options (279 approved/81 pending).
Source-research helpers are not browser verification; actual IAB observations are
recorded separately. One Kyoto existing pending slot may receive an exact URL and
evidence URL correction; it cannot change parent/provider/property ID or maps.

Completed bounded batch: 21 normal option edits + 21 reviews + 21 new receipts;
all approved, zero holds. Independent SQL confirmed 13 protected groups unchanged,
including all 60 products, 319 original approved rows, 387 old receipts and 9,663
historical audits. Replay retained all 420 full rows and created no extra audits.
Public matrices: 90 anonymous GETs, 40 hotels, 192 -> 212 -> 212 options; the one
Kyoto option remains hidden under its pending parent. 178 offline tests passed.
The full pinned local verifier passed at 2026-09-09T00:15:27Z.

This task completes only the 21-item new-evidence batch, not all hotel moderation.
Remaining: 20 pending products and 60 pending options (50 without stored URL,
10 with stored URL), with original evidence ages/reasons in remaining-items.json.
No Gemini, paid API/quota change, quote, booking, affiliate, deployment, migration
or restart. Both deployment locks released after replay; the separate planner owner
was notified before its authorized deployment window. Evidence stays local-only.
