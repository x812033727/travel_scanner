---
id: 2026-09-30-activate-channel-branding-and-rebuild-unapproved
title: Activate channel branding and rebuild unapproved long videos
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-09-30T01:40:50Z
completed_at:
branch:
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

- [ ] The reviewed release is deployed using the guarded production workflow.
- [ ] The selected package is hash-verified in the production video-work volume
      and is the default for new long-video builds.
- [ ] Freshly verified unapproved existing long cuts are rebuilt, with captions,
      chapters and all chosen dubs synchronized to the 5-second intro.
- [ ] Rebuilt final reviews are submitted with --manual-review and read back as
      pending; no approval, publication or already-approved cut is changed.
- [ ] Save activation, before/after SHA and playback evidence; record any real
      owner playback/listening still outstanding.

## Steps

- [ ] Confirm exact tested PR/SHA deployment authorization and active-worker state.
- [ ] Re-read live inventory/reviews immediately before selecting each cut;
      skip anything now approved, published, dropped or Shorts.
- [ ] Preserve old media and checks for rollback; install the fixed asset package.
- [ ] Rebuild chosen cuts with --adopt-branding, then chosen dubs and captions.
- [ ] Run QA and review-push --gate final --manual-review; verify pending readback.

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
