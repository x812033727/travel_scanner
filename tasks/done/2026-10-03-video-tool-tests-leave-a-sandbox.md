---
id: 2026-10-03-video-tool-tests-leave-a-sandbox
title: Video tool tests leave a sandbox in TEMP on every call
status: done
priority: P2
area: tools
owner: claude-opus-5-5-sandbox-cleanup
claimed_at: 2026-10-03T12:22:42Z
created_at: 2026-10-03T12:18:34Z
completed_at: 2026-10-04T05:34:11Z
branch: claude/video-test-sandbox-cleanup
depends_on: []
scope:
  - tools/video/core/fixtures/load.mjs
  - tools/video/core/fixtures/load.test.mjs
  - tools/video/media/media.test.mjs
  - tools/video/automation/tidy.test.mjs
---

# Video tool tests leave a sandbox in TEMP on every call

## Why

`sandbox()` in `tools/video/core/fixtures/load.mjs` builds a throwaway repository and work
base with `mkdtempSync(tmpdir(), "video-core-")` and nothing ever removed it. About 220 calls
in `tools/video/**/*.test.mjs` (and `compilationSandbox()` in `tools/video/compile/fixture.mjs`,
which builds on it) each left one behind on every run, and only a handful of tests cleaned up
after themselves with `t.after`. On the owner's Windows machine `%TEMP%` held 21,437
`video-core-*` directories, 44.6 GB, after about a day of agents running `npm run test:tools`,
and the disk ran out. Two smaller piles had the same shape: 1,577 `video-tidy-*` directories
from `place()` in `tools/video/automation/tidy.test.mjs`, and 192 `video-media-*` directories
from inline `mkdtempSync` calls in `tools/video/media/media.test.mjs` (which also leaves
`video-media-none-*` and `video-home-*`).

## Definition of done

- [x] One full `npm run test:tools` leaves no new `video-core-*`, `video-tidy-*` or
      `video-media-*` directory in the system's temporary directory.
- [x] `VIDEO_KEEP_SANDBOX=1` keeps them, for a look after a failing test.
- [x] A directory that cannot be removed (a file still open on Windows) never throws from
      the exit handler and never changes the test process's exit code.

## Steps

- [x] `load.mjs`: `tempDir(prefix)` makes the directory and remembers it; the first call adds
      one synchronous `process.once("exit")` handler that removes every remembered directory
      with `rmSync(dir, { recursive: true, force: true })`, each in its own try/catch, unless
      `VIDEO_KEEP_SANDBOX=1`. `sandbox()` uses it.
- [x] `media.test.mjs` and `tidy.test.mjs` make their directories with `tempDir()` too.
- [x] `tools/video/core/fixtures/load.test.mjs`: a child node process makes sandboxes and
      exits, and they are gone; with `VIDEO_KEEP_SANDBOX=1` the sandbox stays; with `rmSync`
      made to throw for one sandbox the child still exits 0 with nothing on stderr and the
      next sandbox still goes.
- [x] Count `%TEMP%\video-core-*` before and after one full `npm run test:tools`.

## How to verify

```bash
node --test tools/video/core/fixtures/load.test.mjs
node --test tools/video/media/media.test.mjs tools/video/automation/tidy.test.mjs
# Before and after one full run; the new names should be none of this run's.
ls -d "$TEMP"/video-core-* | wc -l; npm run test:tools; ls -d "$TEMP"/video-core-* | wc -l
```

## Notes

- Removal is at process exit, not per test: node --test runs every test file in a process of
  its own, so exit is the end of that file's tests, and many sandboxes are made inside helpers
  with no test context at hand (`compilationSandbox()`, `context(sandbox(), ...)`), so a
  `t.after` at each of the ~220 call sites would be a far bigger change. Nothing outlives the
  process:
  no test that uses a sandbox spawns a detached or unref'd child, nothing in `tools/` hands a
  sandbox path to another test file, and the only modules importing `load.mjs` are test files
  and `tools/video/compile/fixture.mjs` (itself only imported by tests).
- `rmSync` does not follow links. The only links the affected tests make are junctions in
  `tidy.test.mjs`, and they all point inside the same `video-tidy-*` directory anyway; no
  `sandbox()` user makes a link, and no production code under `tools/video` makes one.
- Tests that already clean up with `t.after(() => rmSync(box.base, ...))` keep working:
  `force: true` makes the second removal a no-op.
- A process killed before it exits (a test timeout that kills the child, Ctrl+C) still leaves
  its directories; the exit event does not fire then.
- Verified on 2026-10-04 on the owner's Windows machine, on top of origin/main 97c0dd615. That
  morning `%TEMP%` held 23,090 `video-core-*` directories (69.6 GB), two days after the last
  manual clean-up; they are the owner's to remove and this task deleted none of them.
  - One full `npm run test:tools` (1,507 tests): the names in `%TEMP%` before and after are the
    same sets for `video-core-*` (23,090), `video-tidy-*` (2,031) and `video-media-*` (237).
    The one new name is a `video-home-*` from `tools/video/tts/tts.test.mjs`, which the
    follow-up task covers.
  - `node --test "tools/video/**/*.test.mjs"` with `TEMP`/`TMP` pointed at an empty directory
    (1,278 tests) leaves 31 directories, 422 KB, none of them with the three prefixes: every
    one is a prefix listed in `2026-10-03-other-tool-tests-still-leave-temporary`.
  - `tools/video/tts/check.test.mjs` alone, same empty-directory method: origin/main leaves 7
    `video-core-*` (13 MB), this branch leaves none.
  - The only failing test in both runs, "a second transcript clears a line only Gemini
    misheard" in `tools/video/tts/check.test.mjs`, fails the same way on a pristine origin/main
    on this machine and passes on CI's Linux.
- None of the four files is bound by `docs/videos/long-form/review.json`
  (`node tools/video/long-form/cli.mjs check` passes unchanged), so no duration-receipt
  increment goes with this change.
