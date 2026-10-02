---
id: 2026-10-01-activate-the-cc-intro-default-and
title: Activate the CC intro default and rebuild eligible existing videos
status: done
priority: P2
area: docs
owner: codex-branding-cc-rollout
claimed_at: 2026-10-01T11:11:58Z
created_at: 2026-10-01T07:41:48Z
completed_at: 2026-10-01T14:13:38Z
branch: codex/cc-intro-rollout-receipt-20261001
depends_on: []
scope:
  - docs/videos/branding-release/2026-10-01-channel-branding-cc-activation.md
---

# Activate the CC intro default and rebuild eligible existing videos

## Why

The owner approved the prepared CC-reminder intro and asked to apply it to all
openings. Activate this exact media package on the production video work volume,
audit existing videos against live approvals and local pins, and rebuild every
eligible existing long cut. Uploaded cuts require a separate replacement upload;
do not describe a new default as proof that existing bytes were replaced.

## Definition of done

- [x] Production current selects v2 CC with verified asset hashes and old current
  retained for rollback; the existing worker reads the same selection.
- [x] Audit every existing long-video row; rebuild all eligible completed unuploaded cuts,
  verify media/timing and re-submit for manual owner review where applicable.
- [x] Record exact changed/excluded counts and reasons, including any approval
  boundary or uploaded videos that cannot be replaced in place.
- [x] Preserve worker/hold ownership, approved evidence, media outside Git and
  unrelated production state; save and verify the activation receipt.

## Steps

- [x] Confirm owner authorization, package hashes and generic live installer path.
- [x] Read live host/current/worker/locks and inventory all existing videos.
- [x] Install the selected v2 package with guarded current comparison.
- [x] Rebuild eligible existing cuts and verify the actual persisted result.
- [x] Save the receipt and deliver an exact coverage statement.

## How to verify

Run the deployed branding CLI in dry-run mode, compare the observed old current,
install the immutable assets, then independently read current and sha256sum from
the running worker. Audit local final/publish approvals, upload manifests and
remote review/YouTube state before each candidate. For changed cuts compare body
hashes, frame counts, captions, chapters, dubs and new pending manual reviews.
Check that only this operation's hold/STOP is removed, the expected worker is running
and persistent service identities/mounts are preserved.

## Notes

- Owner scope: “先改尚未上架與之後影片”; later authorization explicitly permitted
  green-CI merge/deployment and the remaining 14 renewals. Final approval and
  YouTube upload/publication remain owner decisions.
- Selected package `mokaair-brand-package-v2-cc`, selection
  `a27622022d8d9e2f56221a81a1d7443ab241c40a37a515925784511f0416dcdd`.
  The 5-second CC reminder is the production/Windows first-build default; the
  original 3-second like/share/bell outro is unchanged.
- Historical asset-only activation completed 08:11:19 UTC, exit 0. Its exact old
  worker/image, source-hash preservation and installer receipt remain in the
  activation document; that operation did not deploy application code.
- PR #1077 passed all 11 checks at head
  `a2b40dc5108f786a79d1ba009e4a1bb7802492d2`, tree
  `478b1b06d8b212f626cfd0a5d9bf5a63ab9e215b`, and merged as
  `16272d006ddc72bea0ef57eaaf2570cc3faf132c`. Exact code deployment completed
  13:31:01 UTC, exit 0: fresh PGDMP/restore-list verification, 13 healthy running
  services, preserved persistent identities/mounts and cleared own hold/STOP.
- All 17 rebuilt eligible finals are present on the site. The 14 remaining cuts
  were each renewed through the authenticated owner website with fresh-version,
  single-POST and immediate persisted pending identity/hash readback. They remain
  human-pending; episodes 04/05/06 retain their separate external owner approvals.
- Final independent receipt verified 13:59:48 UTC:
  `rollout/final-coverage-renewed-2026-10-01T13-59-04-107Z.json`, SHA
  `106f1d6e7c0d17af9fc650e24f00a26454815efdfa3403861fdfa5e468f15bec`.
  It binds all 17 source/candidate hashes, 14 submissions, unchanged defaults,
  56 verified attachments, retained source history and complete channel readback.
  Raw media/account/host receipts remain outside Git.
- Historical 55-row coverage: 17 rebuilt long cuts, 11 public long cuts preserved,
  seven first-build longs, one missing local source project, 15 Shorts and four
  dropped projects. Fresh inventory adds `gemini-4-argon-who-can-use-it` as an
  unassembled first-build long with no pin; total 56, separate from the 17 revisions.
- All 17 old source IDs/hashes/decisions/files remain in history: 14 source finals
  intentionally superseded, three original import sources still approved. The
  complete 12-entry channel ID/privacy inventory, including 11 public URLs, is
  unchanged; all 17 targets have no YouTube ID/schedule/session/VPS/sync activity.
- Source/media QA and 177 API / 1049 tools / 136 producer-consumer probes are
  preserved in the activation document. The previously stalled local full-web run
  is historical incomplete evidence; final exact-head CI completed successfully.
- The live pending-review interface was verified. This operation made zero final
  approvals, YouTube uploads or publications and did not claim full owner playback
  or listening. Canonical worker/manual-package handoff after owner review remains
  `2026-10-01-hand-off-owner-approved-renewed-finals`; non-zh-TW transport remains
  `2026-10-01-youtube-narration-request-transport`. Neither is silently completed.
- Implementation and live rollout evidence are complete. This task closes with
  the verified rollout receipt; owner review and the dependent canonical handoff
  remain separate.
