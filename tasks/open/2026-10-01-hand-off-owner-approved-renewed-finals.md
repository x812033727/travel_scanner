---
id: 2026-10-01-hand-off-owner-approved-renewed-finals
title: Hand off owner-approved renewed finals to canonical and imported upload packages
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-01T09:53:00Z
completed_at:
branch:
depends_on:
  - 2026-10-01-long-video-renewal-tools-and-ui
scope:
  - tools/video/review/renewal-handoff.mjs
  - tools/video/review/renewal-handoff.test.mjs
  - tools/video/review/renewal.mjs
  - tools/video/review/renewal.test.mjs
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
  - tools/video/package/cli.mjs
  - tools/video/package/package.test.mjs
  - docs/videos/BRANDING.md
---

# Hand off owner-approved renewed finals to canonical and imported upload packages

## Why

The owner can stage a replacement final and create a new human-pending review, but
approval alone does not replace the canonical worker's old final, branding pin,
checks, timeline, captions or upload package. The renewal submission guard deliberately
refuses those old bytes. An explicit source-bound handoff is still required before
automatic production can continue, including manual imported cuts with no normal TTS
or scene timeline. This ticket is not authorization to deploy or operate live media.

## Definition of done

- [ ] For the six isolated v1 revisions with a verified canonical body, the owner can
      adopt only the exact newly approved review/hash/branding into a fresh, verified
      work snapshot; canonical originals, approval decisions and body proof are archived.
- [ ] The transfer rechecks owner approval and upload inactivity immediately before an
      atomic activation. Failure, stale approval or ambiguous result keeps the old worker
      held and preserves both snapshots; changing an approval id alone is impossible.
- [ ] Imported season and legacy candidates have a separate explicit manual-package
      handoff binding original/final/body proofs, translated metadata and every caption
      offset. Missing timeline/TTS/scene evidence is reported rather than fabricated.
- [ ] Newly approved final identity and all applicable source reviews are reflected in
      publish/language manifests, canonical approval artifacts and actual uploaded bytes.
- [ ] Renewed compilations either gain verified episode/body/caption source transfer or
      retain a precise documented hold with their own follow-up; no old merged SRT reuse.
- [ ] No paid regeneration occurs unless a separately authorized body change needs it;
      unchanged narration and source caches are retained.

## Steps

- [ ] Freshly collision-check and claim the exact files before implementation.
- [ ] Define a receipt with old and new final identities, body/pin/check/timeline hashes,
      owner approval identity, archived original paths and activation result/readback.
- [ ] Build the normal-workdir transfer from the six v1 candidate proofs without
      overwriting the existing workdir during preparation or rewriting checks to pass.
- [ ] Define the separate imported manual-package contract; fail closed when the
      available source evidence cannot prove chapter/subtitle offsets and retained body.
- [ ] Add stale approval, concurrent worker, interrupted activation and old-language
      regressions; exercise actual emitted bytes through the API package consumer.
- [ ] Document owner initiation, stage/approve/adopt/package separation and recovery.

## How to verify

Run focused Node tests for renewal/handoff/sync/package, the real Python YouTube package
consumer against emitted fixtures, tools checks and task validation. Compare retained
original media hashes and every caption's first/last cue against the new presentation
timeline. A successful HTTP response is not approval, canonical activation or upload.

## Notes

- Read-only implementation audit on 2026-10-04: live final reviews for the 18
  affected slides are approved renewal candidates, while publish approval is false
  and chosen languages still await the canonical source-bound handoff. This is not
  a request for another owner final approval or an upload authorization.
- The old `<home>/mokaair-work/channel-intro-20260930` candidate evidence
  directory referenced by the prior handoff is currently absent. Locate retained
  canonical/server/archive sources before preparing those 17 candidates; do not
  regenerate paid media merely because local evidence is missing.
- DevDay retains canonical source files under
  `<home>/mokaair-work/videos/openai-devday-2026-recap` and the candidate
  under `branding-audit-20261004`: 153 audio segments, timeline/narration hashes,
  source checks and preservation proof. Its old local pending receipt is a stale
  snapshot; use the fresh approved backend identity. Preserve the original
  publish thumbnail, not an arbitrary newer final-review thumbnail.
- Implementation remains needed: a prepare/verify snapshot receipt, guarded
  activation with worker STOP/idle and fresh upload/owner activity checks, and the
  separate imported manual-package consumer. Existing source-hash guards remain
  intact. The 2026-10-04 recovery branch fixes writer, image completeness and
  status-report code; it does not activate these renewal candidates.

- Filed unclaimed; the predecessor implements a concrete staged-candidate and manual
  pending-review entry point only. No live deployment, import, upload or publication.
- Six v1 candidates have canonical retained body copies/hashes and original
  checks/timeline/video.json available outside the repository. Six season imports have
  final/meta/zh-TW SRT/thumbnail plus normalization/source/body proof but lack a normal
  pipeline timeline. Five legacy candidates originate from approved publish attachments
  and contain translated captions/metadata; do not invent source scene/TTS evidence.
- Candidate media remains outside Git. Read the latest rollout receipts and owner review
  state at execution time; an earlier pending review may already have been decided.
- The existing guard intentionally rejects renewed compilation producer output and any
  normal worker still holding old final/branding/caption bytes. Keep that protection
  until this source-bound transfer exists. Never delete an old approval or use force.
