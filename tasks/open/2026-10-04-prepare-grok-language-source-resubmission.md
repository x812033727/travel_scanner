---
id: 2026-10-04-prepare-grok-language-source-resubmission
title: Prepare source-bound Grok language resubmission
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-10-04T16:59:49Z
completed_at:
branch: codex/video-native-followups-20261004-1525
depends_on: []
scope:
  - docs/ops/video-grok-language-source-resubmission.md
---

# Prepare source-bound Grok language resubmission

## Why

The Grok language batch 178a957d-19f9-451d-b1cc-fe516f4d2b2e was approved by
the owner at 2026-10-04 16:03:04Z. The deployed normal producer still omits
schema-1 source-manifest and metadata roles. Verify the actual consumer result
and prepare a source-bound successor from existing artifacts, preserving this
approval and the real Japanese skip. The concrete owner request to resubmit
Cloudflare was completed separately; it is not permission to replace this
approved Grok version with a new pending review.

## Definition of done

- [x] Freeze exact current source/final/publish/owner choices, old review,
      complete attachments and original metadata; confirm the real missing-role
      error without changing production.
- [x] Prepare and independently validate a complete schema-1 packet and a
      durable single-submit candidate with zero real network or paid calls.
- [ ] Obtain a specific owner decision before changing the current approved
      Grok language batch to a new pending successor.
- [ ] If authorized, submit once and verify the actual new review, all files,
      source binding, preserved approvals, settings and paid accounting.

## Steps

- [x] Reconcile existing reviews/files and native branded metadata read-only.
- [x] Bind a successor to the actual source identities and original choice.
- [x] Review transport, wire shape, unknown-response latch and restart refusal.
- [x] Preserve EN/KO ready and the exact JA skip; do not regenerate speech or
      mark old failed audio as ready.
- [ ] Leave this handoff open until the owner decision and real action resolve.

## How to verify

Use the actual deployed consumer with true ReviewStore bytes. Test hypothetical
approval only on transient copies; production approval and upload remain real
owner actions. Inject counting fetch for the candidate; cover source/choice/
decision drift, missing JSON/files, pending rejection, lost response and replay.

## Notes

Normal producer implementation is already tracked by
2026-09-30-youtube-approved-languages-sync and has overlapping held scopes.
Do not duplicate that code task or modify its owner's claims. This task has only
an operational-document scope; all proposed runtime work stays in TEMP until
specific review and owner authorization. No PR1210 merge/deploy, source change,
paid generation or YouTube action follows from this task.

2026-10-04 17:15Z: Preparation is complete. Real deployed consumer reproduced
the legacy missing-role 409; original ten store/canonical files and source choices
match. Complete twelve-file successor manifest 00e8260712b3eac0f7b65f45162665049e5b158373144ea40f93fd6fe2668afb
and request db802a72ca8d8ce6c696d26e9e699aaf64a5d4818033d3fa226cf144a9ce35e0
are frozen under `<temp>/mokaair-grok-resubmit-20261004`. Root 13/11, independent
packet 17 and real-adapter/normal-flow 24 cases passed with zero real network/paid.
Deployed verify_files=True used original ten real files and two new JSON bytes
only in memory; hypothetical transient approvals did not change real approval,
store or DB. Proof ed7cb5b8291eaf6512485b6c053ce6e5f90b6899f8e1ec064d49f44f22da3447.
Fixed receipt namespace was absent; no live PUT/POST has occurred. See scoped
operational document for complete hashes, preserved JA skip and execution guards.
Remaining work requires a new Grok-specific owner decision, fresh preflight,
single submission and actual twelve-file readback. Do not repeat the WAF action
or infer PR1210/deployment/paid authorization from this preparation.
