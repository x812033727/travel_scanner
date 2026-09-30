---
id: 2026-09-30-activate-channel-branding-and-rebuild-unapproved
title: Activate channel branding and rebuild unapproved long videos
status: done
priority: P1
area: ops
owner: codex-branding-rollout
claimed_at: 2026-09-30T02:04:36Z
created_at: 2026-09-30T01:40:50Z
completed_at: 2026-09-30T03:34:03Z
branch: codex/video-branding-release-20260930
depends_on:
  - 2026-09-30-video-channel-branding
scope:
  - docs/videos/branding-release
---

# Activate channel branding and rebuild unapproved long videos

## Why

The owner chose the 5-second no-tagline Mokaair intro and 3-second like/share/bell
outro, and explicitly included existing unapproved long videos in the requested
rollout. The implementation is separate from production deployment and media
installation. Finish the live application after approval of the exact release;
never equate local tests or a draft PR with applied production branding.

## Definition of done

- [x] The reviewed release is deployed using the guarded production workflow.
- [x] The selected package is hash-verified in the production video-work volume
      and is the default for new long-video builds.
- [x] Freshly verified unapproved existing long cuts are rebuilt, with captions,
      chapters and all chosen dubs synchronized to the 5-second intro. No eligible
      assembled cuts remained at activation; no rebuild was performed.
- [x] Rebuilt final reviews are submitted with --manual-review and read back as
      pending; no approval, publication or already-approved cut is changed.
      Not applicable for this execution: zero rebuilt cuts, no review submission.
- [x] Save activation, before/after SHA and playback evidence; record any real
      owner playback/listening still outstanding.

## Steps

- [x] Confirm exact tested PR/SHA deployment authorization and active-worker state.
- [x] Re-read live inventory/reviews immediately before selecting each cut;
      skip anything now approved, published, dropped or Shorts.
- [x] Preserve old media and checks for rollback; install the fixed asset package.
      No existing cut was changed, so per-cut backup/rebuild was unnecessary.
- [x] Rebuild chosen cuts with --adopt-branding, then chosen dubs and captions.
      Not applicable: fresh candidate count was zero.
- [x] Run QA and review-push --gate final --manual-review; verify pending readback.
      Not applicable: no rebuilt final was submitted.

## How to verify

Follow docs/videos/BRANDING.md and the deploy/prod-host-ops/youtube-video skills.
Verify the deployed source revision, current package hash, final frame count
(body + 240), cue offsets (+150 frames), first chapter at 0, and dubbed track
duration. Verify actual final-review status and preview playback, not just an
HTTP success response or a local artifact.

## Notes

- Selected package hash: 0e1274bf0277762abb210e9e4c30848df88cd849c7af2d2630ee1c084e5b4e40.
- Intro SHA-256: 96ad5f64030248403692d2f65cee4492abcd6ac3a4b7e71c5df8a1adea203b11.
- Outro SHA-256: 8d9546a6042bdc30e0ac597d4eb1452d9e84edc588424027df8f7378ccecf6b1.
- Media, local test logs, read-only inventory and pending-adoption-plan.json live
  outside git in ~/mokaair-work/channel-intro-20260930/.
- Snapshot: one already-assembled, unapproved candidate,
  gemini-connected-apps-permissions; it has no submitted final review yet.
  Thirteen other non-protected long projects have no finished cut and adopt on
  first build. Nineteen long projects are approved/published/finished and excluded.
  These are a planning snapshot, not live eligibility at execution time.
- Actual final review records prove all six imported ai-real-world-* cuts were
  approved; do not infer pending status from their inconsistent checklist rows.
- Installation completed only in the local video workbase. No production
  deployment, asset installation, rebuild, review write or publication occurred.
- Final reviews can auto-approve from ordinary QA under existing site settings.
  Use --manual-review to preserve mechanical QA evidence without auto-approving
  these rebuilt cuts; do not alter the global auto-approval policy.

## Completed rollout — 2026-09-30

- The owner approved the concrete CI-green merge/deploy/install/pending-only
  rebuild proposal. PR #1003 passed all 10 checks on
  eb9541cbfc57ed36cf7a7521068fe3b7cd492885 and merged as
  64f132e1c1d19deca9c8ea52c8ad8b76ebd3a8b8 with the same tree.
- Guarded deployment, asset activation and worker resume completed at
  2026-09-30T03:31:00Z. A Docker process-list format error stopped the first attempt
  before database backup/deployment; the reviewed continuation preserved the own
  hold/baseline and completed with exit 0. Activation and finish also exited 0.
- The activation inventory at 03:29:38Z contained 21 protected projects,
  zero eligible assembled pending cuts, and 13 first-build projects. The former
  Gemini candidate became publish-approved/on YouTube while CI was running and
  was excluded. No existing media, review or publication was manually changed.
- The fixed package is now the production default for first long-video builds.
  All 13 services run; PostgreSQL/Redis identities and restart counts were
  preserved; the owned hold and STOP were cleared after verification.
- Authenticated admin reload and video-list rendering were verified. There was
  no new branded production cut to play. Real phone/headphone/owner listening
  remains unverified and is not implied by technical deployment completion.
- Release record: docs/videos/branding-release/2026-09-30-channel-branding-v1.md.
  Non-public receipts: ~/mokaair-work/channel-intro-20260930/production-receipts/.
