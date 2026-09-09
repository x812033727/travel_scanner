---
id: 2026-09-08-content-review-evidence-followup
title: Resolve remaining merchant and guide review evidence
status: done
priority: P1
area: ops
owner: codex-content-review
claimed_at: 2026-09-08T16:04:47Z
created_at: 2026-09-08T16:03:47Z
completed_at: 2026-09-08T16:44:34Z
branch: codex/content-review-evidence-followup
depends_on: []
scope:
  - docs/catalog-content-reviews/2026-09-09-followup.json
  - docs/catalog-content-reviews/2026-09-09-followup-result.md
  - apps/api/tests/test_catalog_content_review_followup.py
---

# Resolve remaining merchant and guide review evidence

## Why

The user requested complete merchant and hotspot-guide review using the in-app browser or Gemini. The fresh production snapshot contains 443 previously held records (163 merchants, 172 articles, 108 videos), with no new IDs or content drift from the preceding review. Resolve actual evidence gaps without rerunning unchanged whole-catalog AI or weakening publication requirements.

## Definition of done

- [x] Reconcile every one of the 443 IDs and preserve source-specific evidence and remaining gaps.
- [x] Independently adjudicate useful article bodies, actual video language and target content; approve only supported results and reject proven ineligible entries with accurate reasons.
- [x] Preserve merchant data where precise identity or durable location evidence remains incomplete.
- [x] Apply only the sealed decisions through normal review handlers after a new verified backup and fresh full-record guards.
- [x] Verify exact receipts, allowed field changes, five-locale public visibility and unchanged historical data.

## Steps

- [x] Capture fresh inventory, runtime/schema and usage; compare prior evidence without new provider calls.
- [x] Review all remaining articles/videos and bounded high-potential merchant evidence in parallel.
- [x] Run only targeted, budgeted video clips where language or explanation remains unresolved.
- [x] Seal evidence, validate and apply; independently verify and record actual outcomes.

## How to verify

Run the private pure-contract suite and repository evidence tests. Record protected backup attributes, preflight fingerprints, apply result and independent postflight proof in the result document. Check representative public details with the in-app browser; no clickout counting is needed.

## Notes

Worktree starts at b675f5d34a353eddfb789a953968c3c6d45eac4a. Original dirty checkout is untouched. This is an operational editorial task, not permission to deploy code, enlarge paid quotas, or publish unverified merchant coordinates. A completed review can leave explicitly explained pending items; uncertainty is not evidence for rejection.

The reviewed manifest contains 40 approvals (10 articles / 30 videos), 148 rejections (103 / 45), and 255 pending (163 merchants / 59 articles / 33 videos). Four article locale corrections are explicit. Root IAB disproved stable Simplified Chinese at the CLAPPER_STUDIO redirect, so that proposed approval was held. Twelve bounded native-video calls total 860 seconds and 59,816 provider-reported tokens, no retry; one out-of-range timestamp response is invalid and not used to approve. API/evidence tests: 50 passed; private scope guards: 13 passed; clip contracts: 6 passed. Fresh backup, scope/full-record preflight and independent artifact/secret checks passed; apply/postflight status will be recorded in the result document.

Applied once, exit 0. Independent postflight at 2026-09-08T16:40:45Z passed: 443 receipts, 188 normal guide audits, zero merchant mutations, all 709 historical target audits unchanged. Five-locale public visibility en7/ja1/zh-TW32, held/rejected zero. Final pending exact sets 92 guides+163 merchants have no new/missing IDs. Runtime remains b675f5d, schema0063 and readiness200. Root IAB confirmed the newly approved Lotus Pond video appears with the preserved creator title. See docs/catalog-content-reviews/2026-09-09-followup-result.md. This finite editorial batch is complete; 255 evidence-repair items remain explicitly pending, not approved or falsely rejected.
