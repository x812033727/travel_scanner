---
id: 2026-10-01-activate-the-cc-intro-default-and
title: Activate the CC intro default and rebuild eligible existing videos
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-01T07:41:48Z
completed_at:
branch: codex/branding-cc-prompt-20261001
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
- [ ] Audit every existing long-video row; rebuild all eligible unapproved cuts,
  verify media/timing and re-submit for manual owner review where applicable.
- [x] Record exact changed/excluded counts and reasons, including any approval
  boundary or uploaded videos that cannot be replaced in place.
- [x] Preserve worker/hold ownership, approved evidence, media outside Git and
  unrelated production state; save and verify the activation receipt.

## Steps

- [x] Confirm owner authorization, package hashes and generic live installer path.
- [x] Read live host/current/worker/locks and inventory all existing videos.
- [x] Install the selected v2 package with guarded current comparison.
- [ ] Rebuild eligible existing cuts and verify the actual persisted result.
- [ ] Save the receipt and deliver an exact coverage statement.

## How to verify

Run the deployed branding CLI in dry-run mode, compare the observed old current,
install the immutable assets, then independently read current and sha256sum from
the running worker. Audit local final/publish approvals, upload manifests and
remote review/YouTube state before each candidate. For changed cuts compare body
hashes, frame counts, captions, chapters, dubs and new pending manual reviews.
Check that only this operation's hold/STOP is removed and original worker is live.

## Notes

- User authorization: "好 幫我將所有的開頭都改成這個" on 2026-10-01.
- Exact package: mokaair-brand-package-v2-cc; selection hash
  a27622022d8d9e2f56221a81a1d7443ab241c40a37a515925784511f0416dcdd.
- The default activation used the already deployed media installer, without a
  code deployment. PR #1077 now also adds explicit owner final renewal because
  ordinary re-import cannot supersede approved publish/language packages safely.
  Default installation is complete; the new renewal code is not merged/deployed.
- Do not reuse the old v1 deploy/activate/finish scripts: they build an image and
  are bound to a different SHA, source package and before-cut verifier.
- Old final/publish approvals and uploaded video IDs are protected by the current
  adopter. Do not delete approvals or bypass protection to make an all-rows claim.
- Production activation: 2026-10-01T08:11:19Z, exit 0, receipt root
  /root/mokaair-channel-branding-cc-20261001-a27622022d8d. Readback at 09:24:17Z
  verified the exact current/assets, original running worker, no STOP and no hold.
- Windows current also selects v2; 55 existing metadata files are unchanged.
- Fresh complete channel audit at 09:26:31Z confirmed 11 public project videos
  plus one unlisted OAuth demonstration, no active upload sessions or VPS jobs.
- Existing-cut coverage: 6 season originals, 6 retained v1 bodies and 5 approved
  legacy full attachments. Source/body approvals and all original bytes are retained.
  The 14 with old approved languages/publish require explicit final renewal after
  the owner authorizes code merge/deployment; do not mark this rollout complete yet.
- All 17 independent candidate full files were rehashed at 09:40:56Z. Three new
  final reviews are present on the site: 04 approved externally, 05 corrected pending
  (68ea82d7-ed07-42f8-9895-17ec30db9856), 06 pending. This operation made no approval,
  upload or publication decisions. The remaining 14 source approvals are still active
  until a real owner renewal supersedes them; no old evidence has been deleted.
- Counts from the 55-row audit: 17 rebuilt long cuts, 11 public long cuts preserved,
  7 first-build longs, 1 without a local source project, 15 Shorts, 4 dropped.
- Read-only refresh at 10:14 UTC confirmed unchanged default/worker, no hold/STOP,
  11 public videos, no upload sessions/VPS jobs and unchanged three new site finals.
  Candidate CLI, owner website control and downstream stale-source guards are now
  implemented in draft PR #1077; live renewal of the remaining 14 is still pending
  explicit code merge/deployment authorization. Canonical worker/manual-package
  handoff after owner review remains the separate unclaimed dependent ticket.
- Leaving this activation task open and released at that deployment boundary;
  do not mark all existing production cuts changed based on local candidates.
