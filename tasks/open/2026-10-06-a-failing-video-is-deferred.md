---
id: 2026-10-06-a-failing-video-is-deferred
title: A failing video is deferred on its own instead of halting the lane
status: review
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
  - tools/video/automation/discuss.mjs
  - tools/video/automation/client.mjs
  - tools/video/automation/run-receipts.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/automation/cli.test.mjs
  - tools/video/automation/client.test.mjs
  - tools/video/automation/run-receipts.test.mjs
  - tools/video/automation/discuss.test.mjs
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
      minutes doubled per deferral in a row up to two hours, and no sooner than the server's
      `retry_after`), and the lane moves the next video in the same run; the next visit that ends
      without trouble clears the wait.
- [x] An error from one video is sorted: the token, the owner's settings or budget, every
      subscription account and the site out of reach still end the run; a 4xx of this video's
      request blocks it with the reason; a busy service, a 429 or a 5xx defers it.
- [x] An approval the site gave that review-pull did not record defers the video instead of being
      reported as approved, at every gate the worker pulls.
- [x] Two lanes do not poll the same running writer job in one run.
- [x] (Review of PR #1342.) A video is never passed over for ever: six deferrals in a row (three
      for an approval that cannot be recorded) end in a block with the last reason, the page shows
      a waiting video from its second deferral, and `auto` names the deferred videos.
- [x] (Review.) No paid request is sent twice or at the same time for one video because of this
      change: a line on a screenplay waits while its video is not at rest, the retry
      acknowledgement holds its video, and a saved job the server no longer has is sent again
      only under the owner's retry.

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

The review of PR #1342 (twelve findings, every one confirmed by a second reader; eight changes):

- [x] 1. `discuss.mjs` `answerScript` leaves the owner's line unanswered while its video is not
      at rest (`Automation.resting`: in `busy`, in the run's `skipped`, `pendingUntil` in the
      future, or `deferred_until` in the future), before any reply and any model request.
      `series.mjs`, `story.mjs`, `compilation.mjs` and `shorts.mjs` were read for the same shape
      and have none (see Notes).
- [x] 2. `defer()` counts toward `DEFER_LIMIT` (6) and then blocks as `deferred:<what>` with
      "still could not move after N tries: …"; `pulled()` uses `UNRECORDED_LIMIT` (3) and blocks
      as `unrecorded:<gate>`. From the second deferral in a row the report carries a checklist row
      with key `deferred` (why, until when, which try), best effort, under the stage the unit
      last reported or the page shows; `auto.json` `deferred_reported` remembers it, and the next
      report without it takes it off. `cli.mjs` `idleLine` names the videos that wait on their
      own (`Automation.deferredVideos`: a saved deferral, a writer still running, one only this
      run left).
- [x] 3. `move()` calls `moved()` after every visit that ends without trouble, with or without a
      line; not after one that ended the run with `later()`.
- [x] 4. `media()` exit 4 with a STOP file in reach, or a last line starting "stopped ", is a
      `backoffMs: 0` deferral.
- [x] 5. The four no-dispatch 409s wait; `errorScope`'s table test lists every code of the
      worker's routes with its scope (`ERROR_SCOPES` in `automation.test.mjs`, 108 rows).
- [x] 6. `client.mjs` `durableRun` marks a settled 4xx of a known receipt's lookup `gone`;
      `move()` blocks it as `job_gone:<stage>`; `bookkeeping` hands the kind to `retryRuns`, and
      `run-receipts.mjs` `retryCandidates` lists that stage's queued or running journal for it.
- [x] 7. `bookkeeping()` holds the retried video in `busy` from before the save to after the
      acknowledgement.
- [x] 8. `client.mjs` `request()` keeps `Retry-After` on the error as `retry_after`.
- [x] Tests for each: twelve new in `automation.test.mjs`, its error table rewritten as
      `ERROR_SCOPES` and three more rows in the retry table; three new in `client.test.mjs`, one
      each in `run-receipts.test.mjs`, `discuss.test.mjs`, `series.test.mjs` and `cli.test.mjs`.
      Every one of the twenty fails on the code before the change: the seven test files were run
      against a `git archive` of the branch head with only the test files replaced and the new
      constants the tests import appended to `flow.mjs` and `run-receipts.mjs`, so they link.

## How to verify

```bash
node --test tools/video/automation/automation.test.mjs tools/video/automation/cli.test.mjs \
  tools/video/automation/client.test.mjs tools/video/automation/run-receipts.test.mjs \
  tools/video/automation/discuss.test.mjs tools/video/automation/series.test.mjs \
  tools/video/automation/story.test.mjs
node --test tools/video/automation/*.test.mjs
npm run check:tasks
```

On the host after deploy: the worker log shows `deferred until` lines for a video whose vendor is
busy while later videos keep moving in the same run; `auto.json` of such a video has
`deferred_until` and `defer_count`, both gone once a visit ends without trouble. No more runs of
40 units on one video's `chose outline`/`approved` line. A video that keeps failing shows
「暫時過不去，… UTC 後再試（連續第 N 次）：…」 as its current step on /admin/videos from its
second deferral, and after six in a row a blocked card with `blocked_kind` `deferred:<what>`
(or `unrecorded:<gate>`, `job_gone:<stage>`). A round that only waits prints
`nothing to do now: N deferred and tried again later (<slug> until <time>, …)`.

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
  as the video's (`video_production_voice_mismatch`): it blocks that video instead of ending
  every run. Since the review, `video_ai_subject_not_chosen` is no longer one of them: it is
  about the Shorts settings of the whole site, so it ends the run like the other settings codes.
- A review-push that exits 3 (who: owner) defers the video instead of ending the run: the exit
  code cannot tell a 401 from a file the push wants, and a token the site refuses is refused at
  the next unit's video list, which ends the run.
- A first deferral is not reported to the site; the video keeps its last stage on /admin/videos.
  From the second in a row it is (review, change 2).
- Left as it was (outside this scope): `compilation.mjs` still calls `automation.later()` for a
  compile that exits 4; `series.mjs` and `story.mjs` call it for series-level conditions only.
- Draft PR #1342. Before the review: `node --test tools/video/automation/*.test.mjs` green (374);
  `npm run test:tools` 1,891 of 1,902 with five reds: the duration-review binding (below) and
  four this Windows machine already fails outside the automation (reference-analysis and
  from-drama ffmpeg paths, media.test stock path separators, tts/check.test's `process.execPath`
  with a space).
- Stacked on PR #1341 (`claude/video-unstuck-plate-accept`); claimed with `--force` because the
  same owner's open tasks hold `flow.mjs` and `automation.test.mjs`. The scope grew by
  `series.test.mjs` and `story.test.mjs` (one line each) once their tests met `pulled()` and the
  shared `skipped`; `story.test.mjs` is also in PR #1341's task, by the same owner.
- The duration-review receipt (`docs/videos/long-form/review.json`) binds `flow.mjs` and
  `automation.test.mjs`: `node tools/video/long-form/cli.mjs check` is red until a reviewer
  re-binds it.

### The review of PR #1342 (2026-10-06)

Three readers reviewed the draft, and a second reader tried to refute each finding; all twelve
stood (one high, eight medium, three low). By the change that answers them:

- Change 1. A writer still running no longer ends the lane, so the same lane's next unit ran
  the discussion step for that same video: a second writer request while the first was in
  flight, and a rewrite that left the first job's paid answer matching no request (medium).
- Change 2. `defer()` had no ceiling, no path to a block and no report, four findings from
  three sides (high, three medium): a condition waiting cannot cure was tried every two hours
  for ever (an approval review-pull will never record, a push the site always refuses, a
  revoked vendor key answered as a 502 for every video), with nothing on /admin/videos and a log
  line that said every video waits on the owner.
- Change 3. `defer_count` was cleared only by a unit that returned a line, so a video waiting
  on the owner kept its count and unrelated blips days apart compounded to two hours (medium
  and low).
- Change 4. A STOP file that ended the music stage (exit 4, no handler of its own) was a saved,
  counted failure (low).
- Change 5. `errorScope` sent the 409s of a durable job the server failed before its dispatch
  to "video": a STOP file or the switch blocked every video that had a job queued (medium).
- Change 6. A block from the lookup of a job the server no longer has could not be released:
  the retry archived nothing, looked the same job up and blocked again (medium).
- Change 7. The retry acknowledgement's deferral saved the first lane's copy of `auto.json`
  for a video not in `busy`, over what the second lane had saved meanwhile (medium).
- Change 8. `retry_after` reached `defer()` only from a durable writer's failed receipt (low).

What was decided, and what the code then asked for:

- The limits count deferrals, not tries: six of them (5, 10, 20, 40, 80 and 120 minutes), and
  the seventh failure in a row blocks; three for `pulled()` (35 minutes), and the fourth blocks.
  The block's reason is the last line; `block()` clears the wait, so the owner's retry starts
  the video at once, and `resetForRetry` leaves `deferred:`, `unrecorded:` and `job_gone:` alone.
- The server's `retry_after` is a floor under the doubling wait, not the wait itself as it was
  before the review. It had to change once such a deferral counts toward the limit: the API
  answers a busy vendor with 30 seconds, and a wait that short would try the video every round
  and block it within the half hour. A 429 with `Retry-After: 900` still defers fifteen minutes;
  the cap stays two hours.
- A writer still running (RUN_PENDING) neither counts as a deferral nor ends a row of them: a
  queue that loses every job before its dispatch (queued, failed, queued again) must still reach
  the limit. The price is that the page keeps the deferral's row while such a job runs.
- A line on a screenplay is also held while its video carries a `deferred_until` in the future,
  one more condition than the three decided (`busy`, the run's `skipped`, `pendingUntil`). A
  video deferred in an earlier round is passed over before its unit, so `pendingUntil` is never
  set for it in this run; when the deferral came from a read that failed ahead of the writer's
  lookup (the reviews, the acknowledgement), the job sent before it may still be running. The
  line waits until the deferral ends, in a visit without trouble or in a block. The site hands
  over one line at a time, so the lines behind it wait too; before the pull request a failing
  video ended the run ahead of the discussion step every round, so nothing waits longer than it
  did.
- `moved()` does not end the row after a unit that ended the run with `later()` (the site or
  the token failed for this video's push): nothing was read without trouble.
- The deferral's row is reported under the stage the unit itself last reported (a stage that
  reported and then met trouble: "video assembled", then the recap failed), else under the one
  the page shows; a clean visit of a video whose row is on the page sends one report to take it
  off, since a video waiting on the owner would otherwise keep it.
- `auto`'s idle line names every video that sits the round out on its own: a saved deferral
  with its time, a writer still running with its recheck, and one only this run left ("until
  the next round").
- The journal of a job the server no longer has is archived only under the owner's retry of a
  `job_gone:<stage>` block, after one more lookup: found running after all, the retry waits;
  found finished, the normal run takes its answer; still gone, it is archived and the stage is
  sent once. After a re-pair the old job may still be running under the old token, which is why
  the worker never does this on its own.
- The four no-dispatch codes are counted deferrals like any other. They can only come from a
  failed receipt whose `dispatched_at` is null (`run_jobs.py`), and the client has removed that
  journal before it throws, so the next attempt is one new job.
- `ERROR_SCOPES` was read from the server on 2026-10-06 (the file's comment names the sources).
  Codes answered only outside a video's unit (a request, an episode or a compilation being
  started, a series document, a thread's answer) are listed for the default too, though `move()`
  never sees them. `video_ai_subject_not_chosen`, `video_judge_not_enabled`,
  `video_list_filter_invalid` and `video_shorts_state_needs_only` moved from the default
  ("video") to "run": they are about the site's settings or the worker's own list request.
- `series.mjs`, `story.mjs`, `compilation.mjs` and `shorts.mjs` have no step outside a video's
  unit that sends a paid request for a video's slug: their stage calls for `state.slug` are all
  reached from `advance()`; the series step plans documents under `series-<slug>`, and starting
  an episode, a story or a compilation writes files and asks no model; the Shorts run before or
  after the lanes, on their own slugs.
- Noticed and not changed, filed as `2026-10-06-a-pending-discussion-job-and-the`: a
  discussion's own writer job still running does not hold its video on the next round, and the
  first lane's `recordVideoId` and `tellCompilationDone` await the site for a video they do not
  hold in `busy`. Both are older than this pull request.
- After the review: the seven files of "How to verify" are green on this Windows machine (141,
  6, 33, 20 with one skip for POSIX modes, 3, 55, 17), and so is the whole directory (393 tests,
  two skipped: POSIX modes, file symlinks). `npm run test:tools`: 1,910 of 1,921 pass, six
  skipped, and the same five reds as before the review (the duration-review binding and the
  four of this Windows machine).
