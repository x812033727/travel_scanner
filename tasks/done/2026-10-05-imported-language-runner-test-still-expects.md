---
id: 2026-10-05-imported-language-runner-test-still-expects
title: Imported-language runner test still expects the native dub to have no speech journal of its own
status: done
priority: P3
area: tools
owner: claude-runner-test
claimed_at: 2026-10-07T03:42:24Z
created_at: 2026-10-05T23:50:56Z
completed_at: 2026-10-07T03:52:37Z
branch: claude/happy-carson-c1hy91
depends_on: []
scope:
  - docs/videos/imported-long-languages/runner.test.mjs
  - docs/videos/imported-long-languages/runner.mjs
---

# Imported-language runner test still expects the native dub to have no speech journal of its own

## Why

`docs/videos/imported-long-languages/runner.test.mjs` test "actual runner and native dub replay
saved raw WAV after consumer interruption without a second POST" (line 707) fails on origin/main
a9e4c3851. Its second `run` ends with `video_speech_result_held` instead of the expected `EEXIST:`
error (assertion at line 756). No CI job runs this file (`test:tools` only globs `tools/**`), so
nothing caught it.

Train #1302 (a9e4c3851) gave `tools/video/dubs/cli.mjs` its own speech journal
(`tools/video/tts/speech-journal.mjs`, under `<workdir>/audio/speech-journal`). The test was
written when the imported-language journal was the only one. A temporary log of the POST bodies
showed that in the second run, the first chunk (segments `n000`...) no longer reaches the
imported journal's replay. The dub goes on to the next chunk (segments `n014`...) and sends its
first POST. The test's `fetch` then trips `assert.equal(posts, 1, "consumer restart cannot buy
the saved response again")` inside the journal's try, and the journal answers its 409 hold. That
second POST is for a different body, so nothing was bought twice. The test's assumptions are out
of date: it expects a single POST overall, and it times the interruption to the fourth status
GET. Most likely the dub's own journal now serves the first chunk from disk, so the imported
journal's identity probe no longer comes where the test expects it. This is not yet proven
line by line.

## Definition of done

- [x] The test passes again with the native dub's own speech journal in place.
- [x] It still proves that a body whose answer the imported journal saved is not POSTed a second
  time after the consumer is interrupted. A POST for a later chunk is either allowed and counted
  separately or prevented by the fixture.

## Steps

- [x] Trace the second run of the test: which journal (the dub's `audio/speech-journal` or the
  imported `speech-journal/journal.json`) answers the first chunk, and when each status GET happens.
- [x] Adjust the fixture's interruption point, the POST count and the error expectation to match.
  Keep the "no second POST for the same body" guarantee.
- [x] Run the three files below and record the result in the PR body.

## How to verify

From the repository root, with node_modules linked: `node --test
docs/videos/imported-long-languages/runner.test.mjs
docs/videos/imported-long-languages/speech-journal.test.mjs tools/video/tts/client.test.mjs`.
These use fake transports only, so nothing is paid for. Nothing in CI runs the first two files,
so attach the output to the PR.

## Notes

- Found by claude-speech-journal-502 while verifying
  2026-10-05-speech-journal-releases-never-reached-502. It was red the same way before that
  change. The baseline run of the three files above on unchanged a9e4c3851 code (Windows 11,
  Node with node_modules linked) passed 110 of 111, and this test was the only failure. It is
  still the only failure after a rebase onto d829b18dc (#1315): 122 of 123 passed.
- The directory is also the whole scope of the stale claim
  2026-09-29-resume-imported-long-video-languages (codex-video-stall-followthrough). Its branch
  was merged as PR #1210. Check it before claiming.

## 2026-10-07 (claude-runner-test)

- On origin/main 666afb04 two tests were red, not one: "keep an unknown speech POST held across
  invocations" as well, both ending "Dub did not produce a checked track or an explicit skip
  reason". Cause, besides the test's timing: since #1342 (f99c8032) `makeDub` answers a dub exit 4
  with `defer()` (the slug goes into `automation.skipped` with `deferred_until`) instead of halting,
  and the runner only stopped on `automation.halted` or `blocked`, so it went on to read a track
  that was never made. Scope widened to `runner.mjs` for that reason: the runner now clears the
  slug from `automation.skipped` before each unit and treats a deferred unit as a stop with the
  automation's own line (`automation.skipped?.…`, since test automations have no such set). The
  held test passes again unchanged.
- The replay test: traced every status GET and POST. In the second invocation the first chunk
  (n000…) is replayed from the imported journal with no request (the native dub's own journal,
  `audio/speech-journal`, now sits in front of it), the 40 line clips are written, and only then
  does the fresh probe before the next chunk (n014…) run; that next chunk's POST is a different
  body. The test now plants the owner's video STOP in that probe once line clips exist, and asserts
  one POST in all (the fetch still fails any second POST), the saved WAV cut into line clips, the
  imported journal byte-identical, and no checked or skipped dub. The first invocation's
  assertions (EEXIST, one succeeded record, the saved bytes) are unchanged.
- Verified: `node --test docs/videos/imported-long-languages/*.test.mjs` (126 pass, 44 in
  runner.test.mjs); `npm run test:tools`. Still true: no CI job runs this directory (test:tools
  globs tools/**), so it can drift again unnoticed.
