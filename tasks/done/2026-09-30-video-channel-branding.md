---
id: 2026-09-30-video-channel-branding
title: Apply channel intro and outro with synchronized video artifacts
status: done
priority: P1
area: tools
owner: codex-channel-branding
claimed_at: 2026-09-30T01:38:08Z
created_at: 2026-09-30T01:14:00Z
completed_at: 2026-09-30T01:47:32Z
branch: codex/video-channel-branding
depends_on: []
scope:
  - tools/video/core/branding.mjs
  - tools/video/core/branding.test.mjs
  - tools/video/core/state.mjs
  - tools/video/core/state.test.mjs
  - tools/video/core/stages.mjs
  - tools/video/core/stages.test.mjs
  - tools/video/core/compilation.mjs
  - tools/video/core/compilation.test.mjs
  - tools/video/assemble
  - tools/video/compile
  - tools/video/dubs
  - tools/video/package
  - tools/video/qa
  - tools/video/review/pages.mjs
  - tools/video/review/pages.test.mjs
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
  - tools/video/branding
  - tools/video/cli.mjs
  - docs/videos/README.md
  - docs/videos/BRANDING.md
---

# Apply channel intro and outro with synchronized video artifacts

## Why

The owner selected a 5-second Mokaair intro without a tagline and a separate
3-second like/share/bell outro. Future long videos should use this package, and
currently unapproved long cuts should be rebuilt for review. The present pipeline
has no external branding layer; simply joining MP4s would desynchronize captions,
chapters, dubbed tracks and compilation episodes.

## Definition of done

- [x] New long cuts adopt a pinned external branding package; Shorts and existing
      approved/published cuts remain unchanged unless explicitly selected.
- [x] Final duration, captions, chapters and dubs use the same branding offset;
      compilations contain branding once, with body media retained and verified.
- [x] Meaningful tooling tests and a real media smoke check pass.
- [x] Record the exact pending-cut inventory and activation/rebuild status.

## Steps

- [x] Prepare and hash the selected assets outside the public repository.
- [x] Add branding selection, media wrapping and artifact bindings.
- [x] Integrate caption, dub, compilation, package and QA timing.
- [x] Resolve the review-module scope collision before editing that module.
- [x] Validate locally and prepare a reviewable draft PR.

## How to verify

Run targeted video tests, `npm run test:tools`, and `npm run check:tasks`.
Use the selected media with a fixture body to verify 150 intro frames, 90 outro
frames, synchronized audio/captions, one wrapper in compilations, and SHA-bound
approval invalidation. Deployment and live rebuild require separately recorded
activation evidence; local success is not a deployment claim.

## Notes

- User explicitly included currently pending long videos in the rebuild scope.
- Initial claim was rejected because `tools/video/review` overlaps
  `2026-09-28-drama-listener-stale-check`, held by codex-ten-drama in review.
  Initially excluded the conflicting scope while checking the active branch.
  Resolved by live evidence: PR #978 merged at 2026-09-29T15:06:37Z, its
  head 7f1fafec contains the old worktree head 572bb9c9 (merge-base exit 0),
  sync.mjs/sync.test.mjs have no local changes in worktree 31ce, and no open
  PR remains on that branch. The claim is a stale merged-work record, not an
  active file change. Added only the two required sync paths with --force;
  the other task and checkout remain untouched. Earlier confirmation is no
  longer needed because the suspected active collision was disproved.
- Assets and read-only inventory: `~/mokaair-work/channel-intro-20260930/`.
- Live review records confirm the six imported `ai-real-world-*` cuts have approved
  final reviews and are excluded from the pending-only rebuild.
- Bundled Node 24.19.0 full tooling suite: 885 tests, 883 passed, 2 skipped,
  0 failed. Task validation passed (existing unrelated stale-claim warnings).
- Real media: 540 frames / 18.000 seconds; unchanged 300-frame body SHA;
  150-frame intro and 90-frame outro; WAV has 864000 samples per channel and
  0 mismatches against each decoded source segment; subtitle +5 seconds.
- Added rollback regressions for failed QA and filesystem promotion, plus
  same-script re-timed TTS, dub wrapper failure, per-video pins and manual review.
- Final incremental compilation check: 28/28 passed after requiring source
  caption manifests to match branded episodes; stale/missing manifests skip the
  locale and remove obsolete output captions instead of subtracting five seconds
  from an old body-timed SRT.
- The local default is installed and re-read with verified asset hashes.
  Production is unchanged. Deployment, live installation, fresh queue selection
  and manual pending-review submission remain in
  `2026-09-30-activate-channel-branding-and-rebuild-unapproved`.
