---
id: 2026-10-08-validate-windows-stock-path-and-brightness
title: Validate Windows stock path and brightness fixture regressions
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-08T15:27:42Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/media/media.test.mjs
  - tools/video/shorts/from-drama.test.mjs
---

# Validate Windows stock path and brightness fixture regressions

## Why

The 2026-10-08 full tools run on Windows/Node 24.19.0 still fails two test-only portability checks: media.test.mjs:540 expects POSIX slashes in CLI output; from-drama.test.mjs:383 constructs a temp child path containing a second C: drive segment and mkdir fails ENOENT. The earlier brightness production helper fix remains intact; the new regression fixture itself is not portable.

## Definition of done

- [ ] Both tests preserve their assertions and pass on Windows and Linux.

## Steps

- [ ] Recheck current main and active owners, then normalize the stock output assertion and make the brightness fixture valid on Windows.
- [ ] Run targeted cases and affected files on the supported runtime without weakening media measurement.

## How to verify

Run `node --test tools/video/media/media.test.mjs tools/video/shorts/from-drama.test.mjs`; use installed ffmpeg. Record Windows results and Linux CI on the same head.

## Notes

Found in TEMP/ou-external-look-all-tools.log while checking PR #1388 (2162 tests, 8 original failures). Separate reference-analysis, automation ESM and project-lease failures are already tracked by 2026-10-07-windows-reference-comparison-ffmpeg, 2026-10-07-windows-video-test-imports and 2026-10-07-make-project-lease-test-children-use. This ticket does not authorize changes to production media or services.
