---
id: 2026-10-09-windows-video-test-path-assertions
title: Make Windows video test path assertions portable
status: done
priority: P2
area: tools
owner: claude-opus-5-5-board
claimed_at: 2026-10-17T10:44:15Z
created_at: 2026-10-09T17:23:26Z
completed_at: 2026-10-17T10:44:30Z
branch:
depends_on: []
scope:
  - tools/video/media/media.test.mjs
  - tools/video/review/sync.test.mjs
  - tools/video/shorts/from-drama.test.mjs
---

# Make Windows video test path assertions portable

## Why

The complete tools run with Node 24.19.0 on Windows failed three unrelated video
fixtures: stock stdout and outline-lost stdout use platform path separators while
their regex assertions demand forward slashes, and a brightness fixture builds
an embedded Windows drive path as a child directory that Windows cannot create.
Linux CI and the article-localization payload are separate from these local failures.

## Definition of done

- [x] Stock and outline-lost assertions verify the real behavior on both platforms.
- [x] The brightness drive-path regression exercises its intended filter without an invalid Windows directory.
- [ ] Targeted Windows and Linux tests pass with no reduced behavioral assertions.

## Steps

- [ ] Claim these exact test paths and inspect current upstream changes.
- [ ] Reproduce each observed failure with a targeted test before fixing the fixture.
- [ ] Verify portable assertions and record actual subprocess exits.

## How to verify

Run the stock-fetch test in media.test.mjs, the lost-outline test in sync.test.mjs
and the drive-colon brightness test in from-drama.test.mjs individually and in
their normal suites on Windows and Linux. Do not change media/paid behavior just
to satisfy a platform-specific fixture expectation.

## Notes

Observed in the article-localization review's full tools run, actual exit1:
media.test.mjs:501 (assertion at540), sync.test.mjs:242 (assertion at264), and
from-drama.test.mjs:370 (mkdir at383). The latter is a new fixture limitation in
an already completed brightness-filter repair, rather than evidence that its
original filter fix is wrong. No fix, complete-suite PASS or POSIX rerun is claimed.
Existing automation-import, project-lease-import and reference-ffmpeg tickets
already cover their distinct Windows failures; do not duplicate those tickets.
- 2026-10-17 (claude-opus-5-5-board): landed in #1391 (`99f0651ee`, "keep video fixtures and
  diagnostics portable on Windows"), which changed exactly these three files and left this ticket
  open. On main: the outline-lost assertion builds its path with `path.join("review",
  "outline-lost.json")`, the stock line prints `stock/<sha>.png` on every platform (stock.mjs
  `stockFile` joins with `/`) and the `assets[]` line is compared with `path.join`, and the
  brightness test makes a Windows-looking drive-letter child directory only on POSIX (`stats` on win32) while
  still asserting a drive colon in the stats path. All three pass on Linux here. Not run on
  Windows in this session; #1391's Windows run is the evidence for that side. The two speech
  journal Windows tickets are separate and still open.
