---
id: 2026-10-01-add-a-cc-reminder-to-the
title: Add a CC reminder to the five-second Mokaair channel intro
status: done
priority: P2
area: docs
owner: codex-branding-cc
claimed_at: 2026-10-01T07:22:30Z
created_at: 2026-10-01T07:22:20Z
completed_at: 2026-10-01T07:35:01Z
branch: codex/branding-cc-prompt-20261001
depends_on: []
scope:
  - docs/videos/branding-release/2026-10-01-channel-branding-cc-preview.md
---

# Add a CC reminder to the five-second Mokaair channel intro

## Why

The owner requested a visible CC reminder in the existing cinematic Mokaair intro,
plus the like/share/bell call to action. The selected v1 package already has the
three-action outro, so preserve it and produce a new five-second intro with a
clear functional subtitle prompt.

## Definition of done

- [x] A five-second intro shows the original Mokaair logo and a readable
  "開啟 CC 字幕" reminder, without a slogan or a timing change.
- [x] The three-second outro shows like/share/bell; provide a combined preview
  and a hash-verified package outside the public repository.
- [x] Inspect desktop/mobile-sized frames and validate media specs, audio and
  branding installation in dry-run mode; preserve the previous source package.
- [x] Record the distinction between prepared assets and production activation.

## Steps

- [x] Verify selected source assets, deployment receipt and collision-free scope.
- [x] Render the new intro and package the existing CTA outro.
- [x] Inspect readability and perform actual media/integration validation.
- [x] Deliver previews and save a preparation receipt.

## How to verify

Count exact frames with ffprobe, decode the MP4s without errors, verify 1080p/
30 fps and 48 kHz stereo audio, compare retained source hashes/audio, then run
the branding CLI against the new manifest with --dry-run. Inspect a 390px-wide
preview and the reminder's fade-in/hold frames. Keep generated media outside git.

## Notes

- The 2026-09-30 release receipt documents v1 production activation. It is not
  evidence that this requested v2 is installed.
- New output location: ~/mokaair-work/channel-intro-20260930/brand-package-v2-cc/.
- Existing v1 final approvals, per-video pins and production defaults are not
  modified while preparing this package. No paid generation is needed.
- The pending multilingual producer work in PR #1048 is separate and remains
  preserved on codex/youtube-approved-languages-sync-20260930.
- Completed local package: mokaair-brand-package-v2-cc, selection hash
  a27622022d8d9e2f56221a81a1d7443ab241c40a37a515925784511f0416dcdd.
  Preview opened in the app and linked in the delivery; media remains outside git.
- Validation: 14/14 existing branding tests, installer dry-run (installed=false),
  full decode and exact frame counts; real media smoke passed 540 frames/18 sec,
  exact audio segments and +5 sec caption timing. CC desktop/390px frames checked.
- The intro AAC packets and decoded PCM match v1; the outro is byte-identical.
  No headphone/physical-phone listening acceptance is claimed.
- Production activation and existing-video adoption are outside this asset
  preparation task; this receipt must not be treated as an installation approval.
