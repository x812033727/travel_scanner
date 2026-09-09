---
id: 2026-09-08-review-all-pending-travel-catalog-with
title: Review all pending travel catalog with evidence
status: done
priority: P1
area: ops
owner: codex
claimed_at: 2026-09-08T06:48:25Z
created_at: 2026-09-08T06:48:03Z
completed_at: 2026-09-08T08:31:15Z
branch: codex/catalog-review-all-20260908
depends_on: []
scope:
  - docs/catalog-review-2026-09-08.md
  - ops/catalog_review_20260908.py
  - ops/catalog_review_20260908_styles.json
  - ops/catalog_review_20260908_decisions.json
---

# Review all pending travel catalog with evidence

## Why

User requested evidence-based review of every pending hotspot, merchant and merchant style.
Starting inventory: 2,215 hotspots, 167 merchants, 44 styles; no pending foods.

## Definition of done

- [x] Every initial pending candidate has an explicit evidence-based outcome or a documented unresolved requirement.
- [x] Apply only justified decisions, with real administrator attribution and existing publication gates.
- [x] Verify resulting counts, audit records and preserved private/account data.

## Steps

- [x] Inspect production and back up the database before review writes.
- [x] Start the existing review UI under the authenticated administrator.
- [x] Review all 44 style sources, including browser fallback.
- [x] Complete bounded Gemini batches without re-evaluating completed snapshots or changing quotas.
- [x] Inspect and apply individual outcomes, recording unresolved evidence.

## How to verify

Read-only SQL counts, existing service optimistic-version checks and audit logs;
`npm run check:tasks`; operational script dry runs and compilation before execution.

## Notes

Production image at start: `3bc315a29b2795e242116ecadb2a3541f3d05a50`.
Verified private backup: `/root/mokaair-catalog-review-20260908-RHlybdu8/before.dump`,
7,575,880 bytes, mode 600; `pg_restore --list` succeeded.
Authenticated UI created run `5d18ecd2-bec0-45ac-84b3-02a13a5cbd6a` with 2,382 snapshots.
Its actor and matching request audit establish the administrator for this operation;
never synthesize a user or change authentication configuration.
Current API snapshots all pending records but a run is capped at 80 calls. Follow-up
operational batches must select only initial-scope entities not yet assessed in this
review family, retain every old snapshot, and keep all per-run/daily ceilings intact.
Style review does not authorize map identities, coordinates or publication.
CAFE ACME TFAM's source is generic positioning: retain pending unless concrete
in-store cultural activity is verified. Walden and Soiree evidence is on linked
greeting/about pages, not homepage prose; update source links accordingly.

Applied 43 approved styles and 1 keep-pending style with 44 normal style audits.
Root run: 632 assessed (596 hotspots, 36 merchants). Applied 131 hotspot rejections
and 501 keep-pending decisions; 632 normal application audits plus 632 separate
editorial-decision audits. All eight manifest groups succeeded; root version is 11.
Do not alter the original Gemini reasons when recording editorial overrides.

Follow-up run `feab40cb-27b9-4f91-aedd-4e7ecb55b0ed` contains 640 initial-scope
unassessed hotspots. Another deployment replaced containers with image `bdd01b64`
at 07:06 UTC; the worker was interrupted after 80 assessments / 11 calls. After its
lease expired, normal prepare_resume + enqueue restored it, preserving usage and
snapshots. Confirmed progress afterward (208 assessed, 31 calls). Do not redeploy
or merge unrelated work as part of this editorial task.

Batch 2 finished at 07:27:59 UTC with 576 assessed / 48 truncated-response errors /
16 untouched, 80 calls. Its 194 model rejections were individually inspected:
114 reject + 80 keep-pending; with 382 model-needs-review records, 576 applications
and 576 editorial audits succeeded. Batch 2 version is 12. Root + batch 2 total:
245 rejected hotspots, 963 kept pending (including 36 merchants), 1,208 unique
completed applications. Original assessments remain immutable; do not replay new
versions with old idempotency keys. The manifest pins each original expected version.

Third batch `e4cf0849-3877-4065-8571-61c1a6f837d0` started 07:30:04 UTC after another
deployment released both locks. It contains 640 initial-scope unassessed hotspots.
1,174 initial entities were still unassessed before this batch. Last confirmed running:
56 assessed, 9 calls. Need finish this and remaining batches, inspect all new reject
suggestions, apply explicit decisions, then verify all 2,382 unique initial entities.
Public API + BFF and browser confirmed FAbULOUS / Walden styles only; pending
merchants never leaked. Ruff check/format, compilation, task check and root
idempotency replay passed. No PR/push/merge/deployment requested for these ops files.

Third run was interrupted again by image `200e46ea` deployment at ~07:39 UTC after
256 assessments / 37 calls. Resumed through normal service after lease expiry;
usage retained. Later confirmed 392 assessments / 57 calls, version 4.

Two root-scope merchants whose only missing assessment requirement was readable
source evidence were independently checked against their existing official branch
pages: Yamamotoya Honten (Sakae Honmachidori) and Mak's Noodle Central. The bounded
`browser-merchants` command requires unchanged full initial snapshot, no publication
gaps, previous keep-pending application, and current real administrator permission.
Applied ordinary `approve` only (never verify/verify_activate): 2 merchants approved,
normal `food_merchants_batch_updated` + `catalog_review_browser_override` audits.
Map/coordinate verification stamps are unchanged from September 7. Original model
assessments remain keep-pending history. Final current totals must account for these
two later overrides: 271 approved / 165 pending / 3 rejected merchants.

Batch 3 finished 07:53 UTC: 576 assessed, 16 truncated errors, 80 calls. Reviewed
all 203 reject suggestions: 113 reject / 90 keep-pending; with 373 model-needs-review,
all 576 explicit decisions applied. Run version 12; manifest now has 22 groups.
First 3 batches: 1,784 unique applications, 358 rejected / 1,426 historically pending,
including the 2 separately approved merchants described above.
Batch 4 `4930c6ea-6e4d-4526-91be-f58fb14e706f` started 07:54 UTC with all remaining
598 initial entities (467 hotspots, 131 merchants). Continue evidence checks and
normal run limits; never confuse published state with completed assessments.

Initial pass completed 2026-09-08 08:16 UTC. Batch 4 finished after normal resume of 24 truncated
responses: all 598 assessed, no failures, 78 calls. Its 117 reject suggestions became
77 reject / 40 pending; with 481 model-pending, all 598 decisions applied. Version 13.
Four runs total 318 calls, 2,382 distinct assessed/applied initial entities, no missing
or new out-of-scope pending entities. 708 reject suggestions individually reviewed;
435 accepted, 273 kept pending. Catalog audits: 2,382 applied + 2,382 editorial.

Three more independent official-source checks approved Ukishima Brewing Tap Room,
Gecko Hue and Kanomwan Chang Moi. The bounded command now requires a keep-pending
assessment from any member of the same review family plus unchanged root snapshot;
all previous map/coordinate verification dates remain September 7. Five overrides
total, each with normal merchant approval audit and separate browser-source audit.
At 08:16, initial outcomes: hotspots 435 rejected / 1,780 pending; merchants 5 approved /
162 pending; styles 43 approved / 1 pending. Pending means documented unresolved
publication requirements, not unassessed or an automatic approval.

All 29 manifest groups replayed identically (cmp), merchant replays added no audits.
Public BFF confirmed five positive merchants, three pending negatives, and style
filters unchanged at one public merchant each. /ready passes database/Redis, schema
0063_destination_offers. After-backup 11,450,502 bytes mode 600 with verified index
alongside before-backup; all server artifacts retained. No member/account/ledger,
quota, deployment, application code or schema mutations were made by this task.
Ruff check/format, remote py_compile, JSON parsing, task validation and diff check pass.
Full findings and explicit unresolved requirements are in docs/catalog-review-2026-09-08.md.
This is a completed operational review, not a PR/deployment task. No remote Git writes.

Final public UI verification exposed this task's mistaken Mak's Noodle Central
approval: the canonical name and official source identify 77 Wellington Street,
but the existing Chinese name and exact Google Place ID identify Mak An Kee at
37 Wing Kut Street. Official Hong Kong Tourism Board and Cathay sources distinguish
the shops; live browser inspection confirmed the existing ID points to the latter.
Using the existing update service, withdrew only this task's approval to pending /
inactive / map ambiguous, cleared the map verification stamp, and preserved IDs,
coordinates, coordinate verification, and all prior history. Exact original snapshot
plus the known approval updated_at guarded the correction. Added one identity
correction audit with before/after and sources, plus one normal merchant update audit.
Idempotent replay succeeded without an additional write. Removed this merchant
from the browser approval helper to prevent accidental reapproval.

Final verified outcomes at 08:28 UTC: hotspots 435 rejected / 1,780 pending;
merchants 4 approved / 163 pending; styles 43 approved / 1 pending. Total 2,426
assessed records: 47 approved, 435 rejected, 1,944 documented pending requirements.
Full database merchants: 273 approved / 163 pending / 3 rejected. Public BFF returns
zero for the withdrawn merchant and one exact result for each of the four retained
approvals. Readiness still passes. The original after.dump is retained; final backup
final-after-correction.dump is 12,415,953 bytes, mode 600, with verified restore index.
