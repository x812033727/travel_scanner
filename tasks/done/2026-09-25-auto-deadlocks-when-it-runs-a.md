---
id: 2026-09-25-auto-deadlocks-when-it-runs-a
title: auto deadlocks when it runs a sub-command through the CLI entry it was started from
status: done
priority: P1
area: tools
owner: claude-opus-5-5
claimed_at: 2026-09-25T14:22:12Z
created_at: 2026-09-25T14:22:06Z
completed_at: 2026-09-25T14:23:32Z
branch: claude/video-auto-entry
depends_on: []
scope:
  - tools/video/cli.mjs
  - tools/video/automation
  - docs/videos/AUTOMATION.md
---

# auto deadlocks when it runs a sub-command through the CLI entry it was started from

## Why

Beginning at 14:12Z on 2026-09-25, every run of the production video worker ended within a
tenth of a second: "Warning: Detected unsettled top-level await at tools/video/cli.mjs:198",
exit 13. That was the first run with an approved gate: the outline of
`google-ai-student-plan-taiwan` had been approved at 13:12Z. To record an approval, `auto` runs
`review-pull` through `main`. It gets `main` by importing `../cli.mjs` (`run()` in
`tools/video/automation/flow.mjs`). The worker starts `node tools/video/cli.mjs auto`, so
`cli.mjs` is the process entry, and it was still at `process.exitCode = await main(...)`. A
module that is awaiting at its top level cannot finish loading, so the import waited for `main`
and `main` waited for the import. Node saw nothing left to run and exited with 13.

The tests never showed it, because they import `cli.mjs` as an ordinary module. Every gate
approval, `tts`, `render`, `assemble` and `package` goes through the same path, so the worker
could not get past the first thing the owner approved.

## Definition of done

- [x] `node tools/video/cli.mjs auto` can run sub-commands through `main`: the entry starts
      `main` without a top-level await and still sets the exit code.
- [x] A test fails if the entry block awaits again.

## Steps

- [x] `tools/video/cli.mjs`: `main(argv).then((code) => { process.exitCode = code; })`.
- [x] `tools/video/automation/automation.test.mjs`: assert the entry block has no `await`.

## How to verify

`node --test tools/video/automation/automation.test.mjs`. After the deploy the worker log shows
units of work, such as "the owner chose outline A" or "script drafted", not "exited with 13".
Diagnosis on the host: running the same unit by importing `flow.mjs` from a module on stdin
finished with "google-ai-student-plan-taiwan: the owner chose outline A", while running it as
the worker does gave exit 13.

## The second fault: an unusable answer is retried at once, forty times

Once the deadlock was bypassed, the writer stage for the same video answered six times in a row
with about 1,500 to 2,100 output tokens and no `video` object. After each one, `auto` said "the
next run tries again", but it went straight on to the next unit, which was the same writer call.
A run allows up to 40 units. Six calls, about 106,000 Opus subscription tokens, went by in two
minutes before the worker was stopped with its STOP file at 14:24:45Z. What the model actually
answered was not kept.

- [x] An unusable answer from any stage is saved to `<workdir>/<slug>/answers/`. The run ends
      there (`Automation.halted`).
- [x] A second unusable answer in a row from the same stage blocks the video. The first item on
      its /admin/videos checklist says why: 「卡住，需要人處理：…」.
- [x] A service that is down (the narration check, sending a review) also ends the run instead
      of looping, and it does not count towards blocking.
- [x] A planner answer that is not JSON no longer ends the run with an error, which made the
      next round draft again. It counts as an unusable plan and waits for the next interval.

## Notes

- An error in `main` still ends the process with an unhandled rejection and exit 1, the same as
  a rejected top-level await did.
- The writer's six answers were not kept, so why they had no script is still unknown. The
  brief's official pages were not in `source_urls`, since the planner listed only the site
  article, so the writer saw one source. Check the first answer kept in `answers/` before
  changing the prompt.
- A behavioural test would need `cli.mjs` as a child process's entry, with a repository root in
  a temporary directory: `ROOT` comes from where `paths.mjs` sits, and `auto` writes into
  `ROOT/docs/videos`. The source check is the cheap guard until someone builds that.
