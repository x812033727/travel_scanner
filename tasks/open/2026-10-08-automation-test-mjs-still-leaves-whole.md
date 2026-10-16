---
id: 2026-10-08-automation-test-mjs-still-leaves-whole
title: automation.test.mjs still leaves whole video-core sandboxes in TEMP
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-08T07:24:40Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/automation.test.mjs
  - tools/video/core/fixtures/load.mjs
  - tools/video/core/fixtures/load.test.mjs
---

# automation.test.mjs still leaves whole video-core sandboxes in TEMP

## Why

Since `2026-10-03-video-tool-tests-leave-a-sandbox` (#1200), `tempDir()` in
`tools/video/core/fixtures/load.mjs` removes every sandbox from a `process.once("exit")`
handler. The owner's `%TEMP%` still fills up. On 2026-10-08 it held 1,428 `video-core-*`
directories, 6.6 GB, and the largest was 241 MB. The disk ran low again.

- **The cleanup never ran.** 1,379 of the 1,428 are whole sandboxes: `repo/docs/videos/<slug>/`
  and `lexicon.json` are both still there. If removal had started and then failed on an open
  file, these would be half-deleted.
- **They come in bursts.** By hour of creation (UTC): 10-06 02Z 210, 10-07 05Z 132,
  10-07 10Z 300, 10-07 11Z 56, 10-08 01Z 89. That looks like whole test runs leaking, not a
  steady trickle.
- **Most come from `tools/video/automation/automation.test.mjs`.** The most common `work/`
  entries are `auto-state.json` (745), `chatgpt-ads-off` (682), `repair-fixture` (88),
  `guarded-policy-retry` (44), `answers` (42) and `middle-video` / `newest-video` /
  `oldest-video` (40 each). Those names come from that file's tests.
- **The cause is not known yet.** These are guesses to check, not findings:
  - The automation test process is killed rather than exiting: a test-runner timeout, a hang
    that is killed from outside, or an agent stopping `npm run test:tools`. `exit` handlers do
    not run on a kill.
  - Something calls `process.exit` in a way that skips the handler. Line ~5542 spawns a
    helper process that exits, but that is a child, not the test process.
  - The runs come from worktrees whose base is older than #1200. Many agent worktrees run
    `npm run test:tools`. 102 of the leftovers hold a `LEASE` file, which fits tests that hold
    a lease when they are cut off.

## Definition of done

- [ ] One full `npm run test:tools` on current main leaves no new `video-core-*` directory in
      the system's temporary directory. This includes a run where
      `tools/video/automation/automation.test.mjs` is interrupted.
- [ ] If leaks still happen, a later run removes the earlier run's leftovers, so they cannot
      pile up across runs. Only `video-core-*` older than a few hours is removed, so a test
      running at the same time is never touched.
- [ ] `VIDEO_KEEP_SANDBOX=1` still keeps sandboxes.

## Steps

- [ ] Reproduce with `TEMP`/`TMP` pointed at an empty scratch directory (do not touch the
      owner's `%TEMP%`). Run `node --test tools/video/automation/automation.test.mjs` once
      normally and once killed partway, and count what stays.
- [ ] Find which of the guesses above is real. Add a `process.on("SIGINT"/"SIGTERM")` path,
      or move cleanup to `after()` hooks, as the evidence shows.
- [ ] Add a stale sweep to `tempDir()` (first call per process): remove `video-core-*`
      directories older than N hours (for example 6), each in its own try/catch, never
      following links.
- [ ] Extend `tools/video/core/fixtures/load.test.mjs`: a child that is killed leaves its
      sandbox, and the next child's sweep removes it once it is old enough.

## How to verify

```bash
mkdir -p "$PWD/.tmp-sandbox-check" && TEMP="$PWD/.tmp-sandbox-check" TMP="$PWD/.tmp-sandbox-check" \
  node --test tools/video/automation/automation.test.mjs; ls "$PWD/.tmp-sandbox-check" | wc -l
node --test tools/video/core/fixtures/load.test.mjs
```

## Notes

- Measured on the owner's machine on 2026-10-08 during a disk cleanup. The owner chose to open
  this ticket instead of only deleting the leftovers again.
- The leftovers older than a day were not deleted this time, because the owner did not tick
  that option. Do not use them as a clean baseline.
