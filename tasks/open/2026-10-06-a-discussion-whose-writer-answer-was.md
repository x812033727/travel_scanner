---
id: 2026-10-06-a-discussion-whose-writer-answer-was
title: A discussion whose writer answer was lost ends every round
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5-discuss-lost
claimed_at: 2026-10-07T12:41:51Z
created_at: 2026-10-06T15:36:43Z
completed_at:
branch:
depends_on:
  - 2026-10-06-a-failing-video-is-deferred
scope:
  - tools/video/automation/discuss.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/series.test.mjs
  - tools/video/automation/discuss.test.mjs
---

# A discussion whose writer answer was lost ends every round

## Why

The owner's line on a screenplay is answered by the writer outside any video's unit
(`tools/video/automation/discuss.mjs` `answerScript`). An error of one video's own stage is sorted
by `flow.mjs` `move()` (`errorScope`: the run ends, the video waits, or the video is blocked with
the reason), but an error of the discussion's request is not: `answerScript` takes only an answer
that is not JSON (a reply says so) and, since the repair of PR #1342, a saved job the server no
longer has (the video is blocked as `job_gone:writer`). Everything else leaves `step()` as an
exception, `auto` exits 3 or 4, and since the discussion comes before the series, the drama
requests and the scheduled draft, none of them runs in that round. The site hands the same line
over again on the next round, so the same thing happens every round:

- **The answer was lost** (`RUN_UNCERTAIN`). With durable runs the journal says `uncertain` and the
  client throws it again on every round, for ever: no video is blocked, so no owner retry can set
  the journal aside. Without durable runs the request is simply sent again, and paid for again, on
  every round the gateway loses the answer.
- **A refusal of this request** (a 4xx such as `video_ai_job_input_changed`, a body the API will
  not take). Asking again is refused the same way, every round.
- **A busy service or a rate limit** after the client's own retries. This one passes, but it ends
  the round each time instead of making the line wait.

Read in the code while the second review of PR #1342 was being answered; not seen on the host.

## Definition of done

- [x] An error of a screenplay discussion's request never ends a round more than once for the
      same cause: a lost answer blocks the video as `uncertain:writer` (as its own writer's does),
      a refusal blocks it with the reason, a service that is busy makes the line wait.
- [x] While the video is blocked that way the owner's line stays unanswered (no "no screenplay
      here" reply), and after the owner's retry the line is sent exactly once more.
- [x] No discussion request is paid for twice without the owner's retry.

## Steps

- [x] `answerScript`'s catch: sort the error as `move()` does (share the code rather than copy
      it): `RUN_UNCERTAIN` goes to `Automation.unanswered`, a "video" scope to `block`, a "wait"
      scope to `defer` (the line is then held by `resting`), a "run" scope is thrown as today.
- [x] Hold the line while its video is blocked as `uncertain:writer` (today only
      `job_gone:writer` holds it, `discuss.mjs`); decide whether every block should hold the line
      instead of answering that there is no screenplay.
- [x] Tests in `series.test.mjs` on the durable route (the helper `durableDiscussion` is there):
      an uncertain journal, the round does not throw, the owner's retry, one new request.

## How to verify

```bash
node --test tools/video/automation/series.test.mjs tools/video/automation/discuss.test.mjs \
  tools/video/automation/automation.test.mjs
```

## Notes

- `flow.mjs` and `automation.test.mjs` are bound by the duration-review receipt
  (`docs/videos/long-form/review.json`): a change there needs the independent re-bind.
- The planner's answer on a document (`answerDocument`) has the same shape and no video to block:
  its errors end the round too. A document thread has no durable job, so nothing is left behind,
  but a refusal repeats every round all the same; decide it here or file it.
- Since the repair of PR #1342 a discussion's journal that no line claims any more (the thread was
  answered for or withdrawn while its job was running) is harmless but stays: the first lane asks
  the site for the next line at the start of every unit while it is there, and the other lanes
  leave that video to the first. If one is ever seen on the host, setting such a journal aside once
  its job is over belongs here.
- 2026-10-07 (claude-opus-5-5-discuss-lost), `flow.mjs` and `discuss.mjs`:
  - `move()`'s sorting is now `Automation.requestFailed(state, error, { sends, request })`, which
    `move()` and the discussion's catch both call: a policy hold parks the project, RUN_UNCERTAIN
    goes to `unanswered` (`uncertain:writer`), RUN_PENDING and a "run" scope are thrown, a job
    gone goes to `jobGone`, a "video" scope blocks with the reason, a "wait" scope defers.
    `move()` behaves as before (PROJECT_HELD and OUTPUT_INVALID stay its own).
  - `answerHeld`'s catch: OUTPUT_INVALID is told to the owner as before, PROJECT_HELD is thrown
    for `step()` as before, everything else goes to `requestFailed`, named as "the writer request
    for the owner's line on script:N" (and `error.unit` for the lost-answer reason). When that
    blocks the video, auto.json keeps the line's id as `blocked_line`; the owner's retry deletes
    it with the other block fields.
  - Holding: a line on the screenplay of a blocked video waits for the retry when the block is
    `job_gone:writer`, `uncertain:writer` or this line's own (`blocked_line`), since the retry
    resends what blocked it. Decided: every other block is answered with `blockedReply` (the
    video is stopped, its reason, and to ask again after dealing with it), not held, and no
    longer with "no screenplay here". The site hands over one line at a time, so holding a line
    behind a block the owner may never retry would hold every line behind it.
  - A paid answer the site did not take: before this, a `messageAnswer` that failed after the
    writer answered ended the round, and the next round asked the writer again (paid twice, and a
    rewrite already saved was rewritten again). The answer, or the unusable or lost reply that
    followed a paid call, is now kept in `discussion-answer.json` (the video's work directory, or
    `_series/<slug>` for a document) before it is posted, and the next visit for that line posts
    it with no model request (`postAnswer`, `takeUnposted`). A kept answer of another line is set
    aside.
  - `answerDocument` (the Notes' question, decided here): the planner is not durable, so a lost
    answer was asked, and paid for, again every round. Now a lost answer (`lostReply`) and a
    refusal (`refusedReply`) are told to the owner and the thread waits for them; a busy service
    or a rate limit leaves the line for the rest of the run (`Automation.waitingLines`), which
    goes on with the series work, and the next run asks again; everyone's trouble still ends the
    run. discuss.mjs reads the scope through `Automation.errorScope`, since it cannot import
    flow.mjs back.
  - Not done: an orphaned discussion journal no line claims (the last Note) was not seen; it is
    left as the Note says.
- Tests:
  - `series.test.mjs`, durable route: a lost answer blocks as `uncertain:writer` once, the next
    round throws, sends and answers nothing, the retry archives the journal and sends the line
    exactly once; a refusal blocks with the reason and holds the line until the retry; a busy
    service defers the video, the round goes on, the line waits, and it is asked once more after
    the wait; an answer the site did not take is posted on the next round with no second request.
  - `discuss.test.mjs`: the planner's lost answer, refusal, busy service, everyone's trouble and
    an unusable answer; a blocked video's line held for the three kinds and answered with the
    block otherwise.
- Review (2026-10-07, three lenses, each finding verified), all fixed in `discuss.mjs` (and one
  line of `flow.mjs`):
  - should-fix, a regression: on a long anime, a deferral or block after the paid
    `anime-discuss-plan` let `step()` settle that answer, so the next visit paid for the plan
    again. `lineFailed` takes the slug out of the step's settle set, as `fence()` does; the plan
    is taken from its journal on the next visit.
  - should-fix: a line's deferrals never reached `DEFER_LIMIT` or the card, because the video's own
    clean visit before each new attempt ended the row (`moved`). The line keeps its own row
    (`line_defers`, restored before each new failure, deleted with the block, on the owner's retry
    and when the line is answered), so a request that never gets through is reported from the
    second deferral and blocks the video as `deferred:writer` after the limit, with the line held.
  - should-fix: the rewrite's lint repairs (`saveAndLint`) were outside the catch. A repair still
    running after the client's wait (the usual case on the durable route) or failing lost the paid
    reply, left the rewrite marked checked, and the line was asked, and paid for, again. Now the
    script is marked unchecked and the reply kept before the repairs; a repair still running is the
    video's own to take up, a failed one is sorted as the line's request, and the kept reply is
    posted on the next unit. A STOP or lost lease restores the script and drops the kept reply,
    as before.
  - should-fix: a kept reply was posted only while the video was at rest, so a block in between
    answered the line with "劇本先不動" though the rewrite was saved. A kept reply for the line is
    now posted first, whatever the video is doing (posting asks no model and touches nothing of
    the video).
  - should-fix: posting a kept reply left the discussion's succeeded durable run untaken
    (`discussionOpen` true, the secondary lanes skipping the video). Keeping a reply now binds the
    finished runs to the kept file (`adoptRuns`), as a rewrite's are bound to video.json.
  - should-fix (tests): the "goes on" check of the deferral now looks at `halted`; the planner's
    kept answer, a kept reply of another line set aside, the kept lost and unusable replies, and
    a video blocked as `uncertain:verifier` are tested; the durable fake's failures use what the
    API sends (`video_ai_job_uncertain`, `video_ai_project_dropped`, a job failed before dispatch,
    a 502 from the answer route). On the durable route a vendor busy after dispatch ends as
    `uncertain:writer`, like the video's own writer; "busy" in the tests is a job the server failed
    before it reached the model.
  - Not defects: the Notes' "throws ... nothing" wording.
- Mutations of each review fix (the answers settled on failure, no line row restored or saved, the
  kept reply only when at rest, runs not bound to the kept reply, the reply not kept before the
  repairs, the flags not cleared before them, repair errors rethrown) each fail a test.
