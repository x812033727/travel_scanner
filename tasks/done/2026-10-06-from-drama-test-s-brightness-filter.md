---
id: 2026-10-06-from-drama-test-s-brightness-filter
title: from-drama test's brightness filter breaks on a Windows temp path
status: done
priority: P3
area: tools
owner: claude-opus-5-5-from-drama
claimed_at: 2026-10-07T03:34:22Z
created_at: 2026-10-06T00:31:53Z
completed_at: 2026-10-07T03:40:59Z
branch: claude/happy-carson-c1hy91
depends_on: []
scope:
  - tools/video/shorts/from-drama.test.mjs
---

# from-drama test's brightness filter breaks on a Windows temp path

## Why

`tools/video/shorts/from-drama.test.mjs` arrived with the in-house video tooling train (#1315).
Its test "a stand-in episode is cut to a Short whose window follows the located subjects and
whose captions are the Shorts layer" (line ~365) fails on Windows after about 200 s of work. The
`brightness` helper (line ~349) passes the stats file to ffmpeg inside a filter graph as
`metadata=print:...:file=${stats}`. On Windows, `stats` is a temp path with a drive colon and
backslashes. The filter parser reads the colon as an option separator and the backslashes as
escapes, and ffmpeg answers "No option name near 'Users…brightness.txt'". On Linux the path has
neither character, so CI passes. On a Windows dev machine, `npm run test:tools` is red for a
reason that has nothing to do with the change being tested.

## Definition of done

- [x] The test passes on Windows as well as Linux, still measuring the same frames above the
  caption bar.

## Steps

- [x] Escape the path for the filter graph, the way the tools already do for ffmpeg filter
  arguments if they have a helper, or run ffmpeg with the stats directory as its working
  directory and pass a bare file name.
- [ ] Run the test on Windows and on Linux (CI). Linux done here; Windows not available in this session (see Notes).

## How to verify

`node --test --test-name-pattern="stand-in episode is cut" tools/video/shorts/from-drama.test.mjs`
on Windows, then CI's tools job.

## Notes

- Found by claude-opus-5-5-check-journal on 2026-10-06 while re-running the Shorts tests after
  rebasing onto cff4a6ac6. The test does not touch check-audio or the speech journal.
- Two other `npm run test:tools` reds on the same Windows machine are also environment-only:
  - `tools/reference-analysis.test.mjs` "--compare matches the measured cuts…": this machine's
    ffmpeg exits with "Invalid argument" on a null output.
  - `tools/video/review/renewal-handoff.test.mjs` "same source path with a replacement
    directory is not renamed": a Windows EPERM on rename.
  Neither is in this ticket's scope.
- 2026-10-07 (claude-opus-5-5-from-drama): took the second option. `brightness()` runs ffmpeg with
  `cwd` set to the stats file's directory and the filter graph names `path.basename(stats)` only,
  so no drive colon or backslash ever reaches the graph; the input goes in as `-i <absolute path>`,
  outside the graph. Same crop, same frames above the caption bar.
- New test "the brightness probe reads a stats file whose path has a drive colon and backslashes"
  needs only ffmpeg: it writes the stats file under a directory literally named
  `C:\Users\runner\AppData` (legal on Linux) and checks six mid-grey levels. It fails with the old
  helper and passes with the new one, which reproduces the Windows failure on Linux.
- The stand-in episode test itself passes on Linux (67 s). It needs Playwright's Chromium; this
  container ships build 1194 while the pinned Playwright wants 1243, so the run used a scratch
  `PLAYWRIGHT_BROWSERS_PATH` pointing at the installed headless shell (nothing in the repo changed).
- Not run on Windows: no Windows machine here. The last step stays open for whoever next runs
  `npm run test:tools` on the Windows dev machine; the regression test above is the proof meanwhile.
