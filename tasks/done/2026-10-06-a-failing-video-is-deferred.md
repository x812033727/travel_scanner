---
id: 2026-10-06-a-failing-video-is-deferred
title: A failing video is deferred on its own instead of halting the lane
status: done
priority: P1
area: tools
owner: claude-fable-5-1-video-unstuck
claimed_at: 2026-10-06T08:03:45Z
created_at: 2026-10-06T08:03:10Z
completed_at: 2026-10-06T22:51:49Z
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
- [x] (Second review.) A lane moves a video only from the `auto.json` it reads once it holds the
      video, so a unit another lane finished meanwhile is not run and paid for again, and that
      lane's block is not written over.
- [x] (Second review.) A discussion of a screenplay holds its video like the video's own unit:
      while its writer request is in flight, while its job is still running on the server, and in
      the next round until its answer is taken; a job the server no longer has blocks the video
      as `job_gone:writer` instead of ending every round.
- [x] (Second review.) Trouble that is everyone's and passes on its own (Jev's daily calls or the
      month's speech characters spent, the review store full, a rate limit, a stopped worker)
      never blocks one video, however long it lasts: the video keeps its row on the card and goes
      on by itself.

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

The second review of PR #1342 (six findings from four lenses, two of them the same; five changes):

- [x] 9. `stepUnit` reads a video's `auto.json` again once it holds it in `busy`, and moves that
      state: gone, no longer active or done, or waiting by the fresh copy, the video is left.
- [x] 10. `discuss.mjs` `answerScript` holds its video in `busy` from the resting check to the
      answer. `step()` sets a video aside in `pendingUntil` for a RUN_PENDING that names it,
      whether its own unit or its discussion threw it, and the lane goes on. `run-receipts.mjs`
      `untaken` and `client.mjs` `untakenRuns` list a video's saved runs whose answer is still to
      take; `Automation.discussionOpen` reads them by the writer's discussion variants: the first
      lane takes such a discussion up at the start of its unit, before the video's own stages,
      and the other lanes leave the video to it.
- [x] 11. `stepUnit` records the videos its loop left alone (`passedOver`: busy, waiting, or held
      by a STOP file), and `resting()` is false for them and for a STOP-held video, whatever the
      clock reads when the discussion step asks.
- [x] 12. `answerScript` blocks its video as `job_gone:writer` when the lookup of the
      discussion's saved job is `gone` (`Automation.jobGone`, shared with `move()`), and leaves
      the line unanswered while the video is blocked that way.
- [x] 13. `defer()` takes `everyone`: the deferral waits, doubles and shows on the card and never
      blocks; `auto.json` `defer_shared` counts them, and only the row's other deferrals count
      toward the limit. `everyones()` names the trouble from an error's code (`move()`, the retry
      acknowledgement, the tidied languages' push, the outline judge, whose error `submitOutline`
      keeps) or from what a command that exited 4 printed (the narration and dub checks, dub,
      the pushes, the media stages).
- [x] Tests for each: five new in `automation.test.mjs`, three in `discuss.test.mjs`, two in
      `series.test.mjs`, one each in `client.test.mjs` and `run-receipts.test.mjs`. Every one of
      the twelve fails on the branch head before the change, and nothing else does: the five test
      files were run against a `git archive` of ba1927a32 with only the test files replaced and a
      stub `everyones` appended to `flow.mjs` so they link (264 tests: 12 fail, 251 pass, the
      POSIX-modes skip).

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

Since the second review: on a day Jev's calls run out, the outlines and narrations that reach
Jev keep the row 「暫時過不去 …（連續第 N 次）：… JEV_DAILY_CALL_BUDGET …」 past the seventh try
(`auto.json` has `defer_shared` beside `defer_count`), none of them is blocked, and each goes on
after 00:00 UTC with no retry. A line the owner writes on a screenplay whose answer takes longer
than a unit logs `<slug>: writer is still running; its saved receipt will be checked next round`
without ending the run, and no other writer or verifier line for that slug appears until
`<slug>: the writer answered the owner on script:N`.

## Notes

- `retryLater` (OUTPUT_INVALID) still ends the run, as a cost guard against a model that answers
  garbage for every video; it now also puts the video in the shared `skipped`, so the second lane
  does not ask the writer for it again in the same run. `unanswered` (RUN_UNCERTAIN) still ends
  the run too: an answer lost on the way says more about the gateway than about the video.
- A pending writer is set aside in memory for `PENDING_RECHECK_MS` (the worker's 300 s round), not
  the client's `durablePollMs` (25 s) the plan named: one lookup already polls for up to 25 s, and
  looking again 25 s later is the pattern that met the 429. Nothing is saved, so the next round
  looks it up at once. A RUN_PENDING outside a video's unit (a discussion, a series document)
  still ends the run, since nothing else would skip it. (Since the second review a discussion's
  sets its video aside the same way and the lane goes on; a series document's still ends it.)
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
  hold in `busy`. Both are older than this pull request. (The first was done here after all, in
  the second review; the second is what that ticket still holds.)
- After the review: the seven files of "How to verify" are green on this Windows machine (141,
  6, 33, 20 with one skip for POSIX modes, 3, 55, 17), and so is the whole directory (393 tests,
  two skipped: POSIX modes, file symlinks). `npm run test:tools`: 1,910 of 1,921 pass, six
  skipped, and the same five reds as before the review (the duration-review binding and the
  four of this Windows machine).

### The second review of PR #1342 (2026-10-06)

Four readers went over the head after the first review's changes (ba1927a32), each through the
real `step()` with only the stages stubbed; six findings, two of them the same one from two
sides (one high, the rest medium). By the change that answers them:

- Change 9 (high; on main too, and older than this pull request). A lane's loop listed every
  `auto.json` once per unit and moved each video with that copy. While it visited an older video
  (a status read and a reviews call), another lane could finish a unit on a later one, save it
  and let it go: the first lane then ran the same stage again from the copy (two verifier
  requests for one video) and saved over the other lane's state, an `uncertain:verifier` block
  included. The first review's change 7 had closed one instance of it.
- Change 10 (medium). A discussion's writer request did not hold its video: while it was in
  flight, `busy` was empty and another lane sent the video's own request beside it; when its
  durable job outlasted the unit, the lane's run ended and nothing remembered the job, so
  another lane of the same run, or the next round's first unit, took a screenplay the owner had
  sent back meanwhile and sent `writer/episode` beside it. The discussion's saved request then no
  longer matched the script, and its paid answer was set aside and bought again.
- Change 11 (medium; introduced by change 1). `resting()` read the clock again after the unit's
  loop had: a writer's recheck time, or a saved wait, that ran out between the two readings left
  the video unvisited by the loop and at rest for the guard, and `writer/discuss` went out
  beside the pending job.
- Change 12 (medium). The `gone` of change 6 was handled only in `move()`. From a discussion's
  lookup it left `step()` as an exception every round: `auto` ended at the discussion step,
  ahead of the series, the drama requests and the scheduled draft, the journal stayed, and no
  retry could reach it because no video was blocked for it.
- Change 13 (medium, found twice). The limit of change 2 blocked a video for trouble that is
  everyone's and passes on its own. With Jev's daily calls spent at 10:00 UTC, an outline at its
  judgement or a narration at its check was deferred at 1, 8, 19, 40, 81 and 163 minutes and
  blocked at 284 as `deferred:judge`, and stayed blocked after the budget came back at midnight,
  one owner retry for each video. Before the first review it resumed by itself.

What was decided, and what the code then asked for:

- A video is moved from the copy read once it is held. The check the loop made on the listed
  copy stays (it is what decides whether to hold the video at all); what the fresh copy says
  then decides whether to move it.
- A RUN_PENDING that names one of this worker's videos sets that video aside like its own
  pending writer, and the lane goes on, where a discussion's used to end the lane's run. With
  the video in `pendingUntil` the reason for ending it ("nothing else would skip it") is gone:
  the line is held by `resting()`, so the next unit does not ask again. A series document's
  still ends the run.
- The next round takes the discussion up first, on the first lane, at the start of the unit,
  and only when some active video that the loop could take has a saved run of a discussion
  still to take (`untakenRuns`: prepared, queued, running, or succeeded and not adopted; the
  writer's `discuss` and `anime-discuss-plan` variants). It is the site that hands the line, so
  the step is the ordinary discussion step run earlier, not a lookup of its own: a job still
  running sets the video aside again, a finished one is answered with no new request, and the
  video's own stage follows on the next unit. Looking the job up from the video's own unit was
  the other way; it would have told "still running" from "over" but could not take the answer,
  and the answer has to be taken before a rewrite makes its request stale.
- The other lanes leave a video with such a saved run to the first lane. They cannot answer a
  line, and without this the second lane, which starts its unit at the same moment, reaches the
  video before the first lane holds it.
- A saved run no line claims any more (the site answered the thread for another reason, or
  withdrew it, while the job ran) holds nothing on the first lane: the discussion step finds no
  line, and the video moves in the same unit. The other lanes keep leaving that video to the
  first, and the first asks the site for the next line at the start of each unit while the
  journal is there. A line cannot be withdrawn on the site today, and a video whose discussion
  is pending is not moved, so it cannot be blocked and answered for meanwhile; setting such a
  journal aside is noted in `2026-10-06-a-discussion-whose-writer-answer-was`.
- A video its own STOP file holds is not at rest either: its line waits with it. With durable
  runs the client would not send while the file is there in any case.
- `job_gone:writer` from a discussion reads "… a retry sets the saved request aside and the
  owner's line on script:N is answered once more". While a video is blocked as
  `job_gone:writer`, for its own writer's job or a discussion's, a line on its screenplay is held
  instead of being answered with "no screenplay here"; other blocks answer as before.
- Which trouble is everyone's (`EVERYONE_CODES`): `jev_budget_exhausted`,
  `video_speech_budget_exhausted`, `video_review_store_full`, `rate_limit_exceeded`,
  `rate_limit_unavailable`, `video_ai_job_queue_unavailable`, `video_ai_worker_stopped`,
  `video_ai_automation_disabled`. Left out on purpose, so they still reach the limit and a
  card: a vendor's own answers (the first review: a revoked key reads as a 502 for every
  video); `video_ai_job_interrupted_before_dispatch` and `video_ai_job_dispatch_closed` (the
  first review: a queue that loses every job before its dispatch must reach a card); and the
  forwarders' 502 `upstream_unavailable`, which one reader asked for. It is also what a request
  the API does not answer within the forwarder's 60 seconds gets
  (`apps/web/app/api/video/reviews/[...path]/forward.ts`: the abort at line 61 lands in the
  same catch as an API that is down, line 83), so it can be one video's own report or push
  that never goes through, which is what the limit is for; and with the API down altogether the
  unit's own list read ends the run before any video is deferred, so an outage does not count
  deferrals. `video_speech_not_configured` never reaches a deferral: the speech client makes it
  the owner's (exit 3).
- `tts`, `dub`, `check-audio`, `qa` and `review-push` print the server's detail, not its code,
  and `review/sync.mjs` and `dubs/cli.mjs` belong to another task in progress
  (`2026-10-01-hand-off-owner-approved-renewed-finals`), so the worker reads the wording
  (`EVERYONE_WORDING`: the setting's name `JEV_DAILY_CALL_BUDGET`, "the review store is full",
  the two sentences of the month's speech characters and the tools' own pre-check, the two
  sentences of the rate limit). The whole output of the command is read, not its last line: the
  final cut's quality check prints Jev's spent budget on its policy row, above the push's own
  last lines. A wording the server changes is counted again, as every deferral was. The
  outline judge's error is kept by `submitOutline` for its code, since `judgeOutline` answers a
  wait with the reason alone.
- An everyone's deferral still raises `defer_count`, so the wait doubles to two hours and the
  row reads 連續第 N 次 past seven; `defer_shared` says how many of the row were such, and the
  limit counts the rest. A video with ten of them and then a vendor's trouble is blocked at that
  trouble's seventh, not its first.
- Noticed and not changed, each filed: a discussion's other errors (a lost answer, a refusal, a
  busy service) still end the round, every round, `2026-10-06-a-discussion-whose-writer-answer-was`;
  `tts` and a narration retake that exit 4 block the video at once instead of waiting,
  `2026-10-06-tts-and-a-narration-retake-that`; the bookkeeping's `recordVideoId` and
  `tellCompilationDone` still await the site for a video they do not hold, which is what is left
  of `2026-10-06-a-pending-discussion-job-and-the` (its first item is done here).
- After the second review: the seven files of "How to verify" are green on this Windows machine
  (146, 6, 34, 21 with the POSIX-modes skip, 6, 57, 17), and so is the whole directory (405
  tests, the same two skipped). `npm run test:tools`: the same five reds as before and no other
  (the duration-review binding, now for `flow.mjs`, `discuss.mjs`, `automation.test.mjs` and
  `series.test.mjs`, and the four of this Windows machine); the run counted 1,932 tests, 1,921
  passed and six were skipped, and the third `discuss.test.mjs` test, added after it started,
  is green in the directory run.
- **Verified at `e0a752ad` (2026-10-07, two independent read-only readers).**
  - *Money and concurrency.* The five fixes of `e0a752ad` hold. One paid duplicate was left,
    older than this PR: `draft()` and `draftDrama()` saved the video as active and then awaited
    Jev's outline judgement without holding it. A second lane could then submit the outline
    again, and when Jev failed it, pay the planner twice. A scratch test showed two judgements,
    two submits and two planner runs. Fixed: `firstOutline()` holds the video from the save
    until the outline is in, with a test that fails without it.
  - *Deferral semantics.* The backoff, the limits, the reset, STOP, `errorScope` (each code
    checked against the API's status), `job_gone` and the whole-worker wait all match the
    decisions above. No regression was found.
  - *Regressions and tests.* No regression against main. Every gate's `pulled()` can reach
    "approved", and a single lane works as before. Ten of the thirty behavioural hunks of
    `e0a752ad` had no test that went red when the hunk was reverted. Two of them now have one:
    `move()`'s `everyone` (a rate-limited stage request deferred past the limit, never blocked)
    and the STOP file in `movable()`. The other eight are the `everyone` flag at the retry
    acknowledgement, the media exit 4, the language pushes and the dub steps; each passes
    `everyones(...)` the same way the tested sites do.
  - *Known low items.* `job_gone`'s block put the server's words before the instruction, and
    the card's label is cut at 120 characters (`schemas.py` `max_length=120`), so the owner
    lost what a retry does. The instruction now comes first, and the longest form is 103
    characters. Other blocked reasons are still cut at 120; that cut is the server's limit.
    A writer job that stays queued has no ceiling: filed as
    `2026-10-06-a-writer-job-that-stays-queued`. `tellCompilationDone` still saves without
    holding its video (filed above). `pulled()` counts the row's earlier deferrals of other
    kinds toward its limit of three, so a report deferral followed by two unrecorded pulls
    blocks as `unrecorded:`; this is low, and is left as is.
  - *Open question, not confirmed.* On the first lane the discussion-first path calls
    `discussStep` once. If the site hands over a line for another, non-resting video first, it
    returns null, and the loop could move the video whose discussion is still open with its own
    stages. The site hands lines over oldest first (`messages.py` `order_by(created_at)`), which
    one reader found keeps the open discussion's line first. No test was written.
- **A third reader verified `4a7e644a` and `134d3f7e`.** The hold is complete. Nothing that
  `submitOutline` reaches checks `busy` for its own slug. Every `job_gone` instruction fits
  within 120 characters (the longest is 104). Both new tests fail when the code they cover is
  reverted. The reader also found the same unheld shape in `draftEpisode`: it saves the
  episode as active and then awaits `approve()` and `report()`. A lane that listed the episode
  in that window would find no outline approval and submit the outline. It now holds the
  episode until the report is sent, and a test fails without the hold.
