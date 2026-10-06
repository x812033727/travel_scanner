---
id: 2026-10-04-package-test-leaves-a-video-thumbs
title: Package test leaves a video-thumbs directory in TEMP
status: in-progress
priority: P3
area: tools
owner: claude-opus-5-5-video-package-check
claimed_at: 2026-10-05T23:41:43Z
created_at: 2026-10-04T15:02:04Z
completed_at:
branch: claude/video-package-check
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

- [x] One full `npm run test:tools` leaves no new `video-thumbs-*` directory.

## Steps

- [x] Check that the hand-off ticket has landed or released `package.test.mjs` before claiming.
- [x] Make the directory with `tempDir("video-thumbs-")` from
      `tools/video/core/fixtures/load.mjs` (removed when the test process exits;
      `VIDEO_KEEP_SANDBOX=1` keeps it) and drop the then unused `mkdtempSync`/`tmpdir` imports.
- [ ] `package.test.mjs` is bound by SHA-256 in `docs/videos/long-form/review.json`: open the PR
      as a draft and have an independent reviewer add the duration-receipt increment.
      (The draft PR is open; the increment is the reviewer's, not the author's.)

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
- Done 2026-10-06 (claude-opus-5-5-video-package-check). Claimed with `--force` over
  `2026-10-01-hand-off-owner-approved-renewed-finals` (codex-video-stall-followthrough, claimed
  2026-10-04T10:14:09Z, about 37 h before, so stale): its branch
  `codex/video-approved-final-languages-20261004` merged as #1210 on 2026-10-04T23:41Z without
  touching `package.test.mjs` (the file's last change on main is #1139, from before the claim),
  and no open PR touches the file. That ticket's remaining items are production activation.
- Measured after the change, with `TEMP`/`TMP` pointed at a new empty directory:
  `node --test tools/video/package/package.test.mjs` 17/17 passed and left the directory empty;
  a full `node --test tools/*.test.mjs "tools/video/**/*.test.mjs"` left it empty too (no
  `video-thumbs-*`, nothing at all). That full run with a long TEMP path also turned six
  `compile.test.mjs` cases and one `dots-series.test.mjs` case red with ENOENT from Windows'
  path length limit; with the default TEMP both files pass, so use a short directory (for
  example `C:\t`) when you repeat the measurement.
- The receipt increment for `package.test.mjs` is left to an independent reviewer
  (`node tools/video/long-form/cli.mjs check` lists it as stale until then).
