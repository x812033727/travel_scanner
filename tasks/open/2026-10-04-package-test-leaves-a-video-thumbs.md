---
id: 2026-10-04-package-test-leaves-a-video-thumbs
title: Package test leaves a video-thumbs directory in TEMP
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-04T15:02:04Z
completed_at:
branch:
depends_on:
  - 2026-10-03-other-tool-tests-still-leave-temporary
scope:
  - tools/video/package/package.test.mjs
---

# Package test leaves a video-thumbs directory in TEMP

## Why

`tools/video/package/package.test.mjs:332` makes its work directory with
`mkdtempSync(path.join(tmpdir(), "video-thumbs-"))` and never removes it, so every
`npm run test:tools` leaves one `video-thumbs-*` directory in the system's temporary
directory (47 of them on the owner's machine on 2026-10-03). It is the last prefix of
`2026-10-03-other-tool-tests-still-leave-temporary`; that ticket fixed the other eight but left
this file alone, because `2026-10-01-hand-off-owner-approved-renewed-finals`
(codex-video-stall-followthrough) claimed `package.test.mjs` on 2026-10-04T10:14Z and its
package work has not landed.

## Definition of done

- [ ] One full `npm run test:tools` leaves no new `video-thumbs-*` directory.

## Steps

- [ ] Check that the hand-off ticket has landed or released `package.test.mjs` before claiming.
- [ ] Make the directory with `tempDir("video-thumbs-")` from
      `tools/video/core/fixtures/load.mjs` (removed when the test process exits;
      `VIDEO_KEEP_SANDBOX=1` keeps it) and drop the then unused `mkdtempSync`/`tmpdir` imports.
- [ ] `package.test.mjs` is bound by SHA-256 in `docs/videos/long-form/review.json`: open the PR
      as a draft and have an independent reviewer add the duration-receipt increment.

## How to verify

```bash
mkdir -p /tmp/empty-temp && W=$(cygpath -w /tmp/empty-temp)
TEMP="$W" TMP="$W" node --test tools/video/package/package.test.mjs
ls /tmp/empty-temp   # nothing left
```

## Notes

- Measured on 2026-10-04 by the parent ticket: with `TEMP`/`TMP` pointed at an empty
  directory, the test files that call `mkdtemp` left exactly one `video-thumbs-*` directory,
  from this file.
