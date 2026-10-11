---
id: 2026-10-09-windows-video-test-path-assertions
title: Make Windows video test path assertions portable
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-09T17:23:26Z
completed_at:
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

- [ ] Stock and outline-lost assertions verify the real behavior on both platforms.
- [ ] The brightness drive-path regression exercises its intended filter without an invalid Windows directory.
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
