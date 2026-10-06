---
id: 2026-10-06-a-failing-video-is-deferred
title: A failing video is deferred on its own instead of halting the lane
status: in-progress
priority: P1
area: tools
owner: claude-fable-5-1-video-unstuck
claimed_at: 2026-10-06T08:03:45Z
created_at: 2026-10-06T08:03:10Z
completed_at:
branch: claude/video-unstuck-loop-fairness
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/cli.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/automation/series.test.mjs
  - tools/video/automation/story.test.mjs
---

# A failing video is deferred on its own instead of halting the lane

## Why

On 2026-10-06 the owner reported that the video automation on /admin/videos "keeps getting
stuck". Besides the nine blocked videos (PRs #1337–#1341), the worker loop itself let one
video's trouble stop all of them:

- `later()` set the whole lane `halted`, and the videos go oldest first, so the oldest video's
  passing failure (a vendor's exit 4, a STOP file during tts, Jev away, a push or report the site
  did not take) ended the lane's run every round, and the second lane ran into the same video
  next.
- `move()` caught only POLICY_HOLD, RUN_UNCERTAIN and OUTPUT_INVALID; any other AutomationError
  (a 409 of one video's job, a 503 the client had already retried) ended the whole worker run
  (`cli.mjs`), every round.
- After a gate was approved on the site, `this.pull()` was trusted: a review-pull that recorded
  nothing (the file changed since, the storyboard's checks) was reported as the approval, and the
  next unit found the gate open and did it again, up to the run's 40 units.
- Two lanes took turns polling the same running writer job (the busy set is released between
  units); the API log showed a 429 on `GET run/jobs/…` at 04:49:37.

The owner decided (2026-10-06) to fix the loop too, in its smallest form, on its own ticket, last.

## Definition of done

- [x] A video whose stage meets a passing failure waits on its own (`deferred_until`, five
      minutes doubled per deferral in a row up to two hours, or the server's `retry_after`), and
      the lane moves the next video in the same run; a unit that moves it clears the wait.
- [x] An error from one video is sorted: the token, the owner's settings or budget, every
      subscription account and the site out of reach still end the run; a 4xx of this video's
      request blocks it with the reason; a busy service, a 429 or a 5xx defers it.
- [x] An approval the site gave that review-pull did not record defers the video instead of being
      reported as approved, at every gate the worker pulls.
- [x] Two lanes do not poll the same running writer job in one run.

## Steps

- [x] `flow.mjs`: `defer()`, `moved()`, `waiting()`, `errorScope()` with `DEFER_BASE_MS`,
      `DEFER_MAX_MS`, `PENDING_RECHECK_MS`; `stepUnit` skips a waiting video; `move()` sorts its
      errors; `step()` sets a pending writer's video aside in the shared `pendingUntil`.
- [x] Every per-video `later()` is a `defer()`: media exit 4, tts / retake / narration check /
      dub check stopped by a STOP file (`backoffMs: 0`, this run only), narration and dub exit 4,
      pushes (`submissionFailure`, languages, tidied languages), the retry acknowledgement, Jev
      not judging an outline. `later()` stays for a draft, a series, a discussion and a report the
      token or the site refused.
- [x] `pulled(state, gate, file)` after every review-pull at an approved gate (outline, script,
      look, storyboard, audio, final, publish, languages, the narration push).
- [x] `cli.mjs`: the lanes share `skipped` and `pendingUntil` as they share `busy`.
- [x] Tests: five new tests in `automation.test.mjs` (a busy writer defers only its video and
      doubles; a 409 blocks only its video; the error and deferral table; an unrecorded approval
      defers and is pulled once a run; two lanes look a pending writer up once); the tests that
      drove "the next run" on one worker call `nextRun()`; `series.test.mjs`'s fake worker gets
      `pulled`, `story.test.mjs` clears the run's `skipped` for its next run.

## How to verify

```bash
node --test tools/video/automation/automation.test.mjs tools/video/automation/cli.test.mjs
node --test tools/video/automation/*.test.mjs
npm run check:tasks
```

On the host after deploy: the worker log shows `deferred until` lines for a video whose vendor is
busy while later videos keep moving in the same run; `auto.json` of such a video has
`deferred_until` and `defer_count`, both gone once it moves. No more runs of 40 units on one
video's `chose outline`/`approved` line.

## Notes

- `retryLater` (OUTPUT_INVALID) still ends the run, as a cost guard against a model that answers
  garbage for every video; it now also puts the video in the shared `skipped`, so the second lane
  does not ask the writer for it again in the same run. `unanswered` (RUN_UNCERTAIN) still ends
  the run too: an answer lost on the way says more about the gateway than about the video.
- A pending writer is set aside in memory for `PENDING_RECHECK_MS` (the worker's 300 s round), not
  the client's `durablePollMs` (25 s) the plan named: one lookup already polls for up to 25 s, and
  looking again 25 s later is the pattern that met the 429. Nothing is saved, so the next round
  looks it up at once. A RUN_PENDING outside a video's unit (a discussion, a series document)
  still ends the run, since nothing else would skip it.
- `errorScope` treats a who:"owner" code that is not about the token, the settings or the budget
  as the video's (`video_production_voice_mismatch`, `video_ai_subject_not_chosen`): it blocks that
  video instead of ending every run.
- A review-push that exits 3 (who: owner) defers the video instead of ending the run: the exit
  code cannot tell a 401 from a file the push wants, and a token the site refuses is refused at
  the next unit's video list, which ends the run.
- A deferral is not reported to the site; the video keeps its last stage on /admin/videos.
- Left as it was (outside this scope): `compilation.mjs` still calls `automation.later()` for a
  compile that exits 4; `series.mjs` and `story.mjs` call it for series-level conditions only.
- Stacked on PR #1341 (`claude/video-unstuck-plate-accept`); claimed with `--force` because the
  same owner's open tasks hold `flow.mjs` and `automation.test.mjs`. The scope grew by
  `series.test.mjs` and `story.test.mjs` (one line each) once their tests met `pulled()` and the
  shared `skipped`; `story.test.mjs` is also in PR #1341's task, by the same owner.
- The duration-review receipt (`docs/videos/long-form/review.json`) binds `flow.mjs` and
  `automation.test.mjs`: `node tools/video/long-form/cli.mjs check` is red until a reviewer
  re-binds it.
