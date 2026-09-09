---
id: 2026-09-08-resolve-pending-catalog-evidence-with-browser
title: Resolve pending catalog evidence with browser verification
status: done
priority: P1
area: ops
owner: codex
claimed_at: 2026-09-08T08:35:20Z
created_at: 2026-09-08T08:34:35Z
completed_at: 2026-09-08T08:57:06Z
branch: codex/catalog-review-all-20260908
depends_on: []
scope:
  - docs/catalog-review-followup-2026-09-08.md
  - ops/catalog_review_followup_20260908.py
  - ops/catalog_review_followup_20260908.json
---

# Resolve pending catalog evidence with browser verification

## Why

User asks to continue resolving pending catalog entries with Gemini API or the built-in browser.
Previous full review left 1,780 hotspots, 163 merchants and one style pending. This follow-up
repairs source/identity gaps where evidence is available, without rerunning identical model
assessments, expanding discovery or changing quotas. Existing main checkout remains untouched.

## Definition of done

- [x] Independently inspect a bounded batch of official branch sources and exact map identities.
- [x] Apply justified evidence repairs with real actor attribution, snapshot guards and audit history.
- [x] Publish only if durable coordinates and every existing publication requirement are supported.
- [x] Record unresolved gaps and verify public results, backups and idempotent writes.

## Steps

- [x] Recheck production pending counts and source provenance.
- [x] Research official sources and independent durable coordinates.
- [x] Apply and verify explicit reviewed repairs; preserve all previous assessments.

## How to verify

Read-only SQL inventory, browser exact branch comparisons, normal service validation,
Ruff, script compilation, manifest parsing, task check and public BFF negative/positive checks.

## Notes

Read-only helpers reviewed existing contracts and official JP/HK/TW sources. Current pending
merchants: 163, 94 with Google IDs, 44 marked map verified. All 44 use Google Maps as their
coordinate source, incorrectly labelled admin_verified by an older workflow. Do not refresh
or bless those coordinates. Existing coordinate_queue apply path has this provenance defect;
do not use it. Existing coordinate_fill extraction ignores embedded Google and can provide
read-only page-owned JSON-LD/meta candidates, subject to branch verification.
All 1,780 pending hotspots lack an exact map ID; 1,715 carry Wikidata coordinates.
Existing Gemini assess rereads supplied source URLs rather than discovering missing map IDs;
therefore browser/source repair is the relevant next step. No new model calls yet.

Completed bounded follow-up at 08:54 UTC. Researched 19 HK/JP/TW merchants;
repaired nine previously source-less merchants, with exact built-in-browser map
checks for all nine. Four approved with genuine coordinates: Yung Kee from its
own Restaurant JSON-LD, Chef Hung Jianbei and Liang Pin from Taipei friendly-store
CSV, Sun Way / 三味 from Taipei shop-renovation CSV. All government source titles
retain provider/year/dataset and OGDL-1.0 attribution. Five others got source and
address repairs but remain pending; unsupported coordinate_source_type and map
verification were cleared while historical values and URLs remain private.

Also corrected this task's own four previous approvals (Yamamotoya, Ukishima,
Gecko Hue, Kanomwan) after confirming their coordinates were Google-derived.
Withdrew them to pending, preserving IDs, coordinates, original sources and all
audits. This is not a closure determination. No unrelated admin approvals changed.
Nine source-repair audits and four provenance-correction audits, each with normal
merchant update audit, exact full before snapshots and same-commit after-hash
receipts. Both paths replayed without extra writes. Normal service blocked the
first pending repair with verified map + missing durable source; transaction
rolled back and resumed with unverified complete location status, not a relaxed gate.

Public BFF four new positive IDs and nine negative pending/withdrawn results passed;
DB final merchants 273 approved / 163 pending / 3 rejected. /ready healthy.
Private before/final backups 12,565,997 / 12,582,384 bytes, mode600, restore indices
verified. No Gemini calls, quota changes, application/schema/deployment or account
mutations. Evidence report and explicit manifest are in this task's scoped docs/ops
files. Separate P1 backlog records the production coordinate-queue provenance bug.
