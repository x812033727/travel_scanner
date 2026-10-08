---
id: 2026-10-08-windows-video-path-assertions
title: Keep Windows path assertions portable in video tools tests
status: in-progress
priority: P2
area: tools
owner: codex-windows-video-validation
claimed_at: 2026-10-08T17:08:23Z
created_at: 2026-10-08T17:08:03Z
completed_at:
branch: codex/windows-video-validation-20261009
depends_on: []
scope:
  - tools/video/review/sync.test.mjs
  - tools/video/shorts/from-drama.test.mjs
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Keep Windows path assertions portable in video tools tests

## Why

The complete Windows tools run exposed a review diagnostic assertion that requires POSIX separators even when the CLI correctly reports native paths, plus a brightness fixture that joins a literal Windows absolute path below a temporary directory and produces an invalid path on Windows. The related stock-fetch assertion uses the existing task `2026-10-07-accept-windows-separators-in-stock-fetch`, adopted from PR #1359.

## Definition of done

- [ ] Both affected files pass on Windows without weakening their semantic assertions.
- [ ] Independent review updates the changed sync-test duration binding.
- [ ] Linux CI preserves the same behavior and measurement coverage.

## Steps

- [x] Preserve the full-run failures and confirm no open PR changes these three files.
- [ ] Use platform-portable expectations and a valid local fixture path.
- [ ] Run affected files, independently review the receipt, then validate full-suite coverage.

## How to verify

Run the complete media, review-sync and from-drama test files with bundled Windows Node and ffmpeg, then required Ubuntu video/tools CI. Keep semantic assertions on stock credits, lost-answer request count, redacted output and real image brightness.

## Notes

The first broader Windows run completed with ten failures, including these three. Logs are retained under `<home>/mokaair-work/windows-video-validation-20261009`. Other failures are separately tracked: project-lease child imports and speech-journal rename failures. No production display or provider behavior needs changing for these assertion/fixture issues.

### 2026-10-09 Windows repair and validation

- `review/sync.test.mjs` now matches the complete lost-answer warning line, including the exact timestamp, reason and `path.join("review", "outline-lost.json")`. The assertion remains tied to the native path; request-count and unchanged-brief no-retry checks remain intact.
- `shorts/from-drama.test.mjs` uses the real absolute temporary path on Windows and retains its literal Windows-like directory on POSIX. Before running the real FFmpeg brightness probe, it asserts that the actual stats filename contains a drive colon and backslash. The six-frame count and measured mid-grey range remain unchanged; the Windows case is not skipped.
- Bundled Node v24.19.0 ran the complete `media/media.test.mjs`, `review/sync.test.mjs` and `shorts/from-drama.test.mjs` files with `--test-concurrency=3`: actual exit 0, 131 passed, 0 failed, 0 skipped, duration 140141 ms. This includes the end-to-end synthetic Short and real brightness measurements. Full log: `<home>/mokaair-work/windows-video-validation-20261009/path-assertions-after.log`.
- `git diff --check` passed for the three changed test files. The author did not alter duration receipts. Independent receipt review, broader suite validation and Linux CI remain separate completion gates.
