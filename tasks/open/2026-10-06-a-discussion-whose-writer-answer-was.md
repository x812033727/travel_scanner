---
id: 2026-10-06-a-discussion-whose-writer-answer-was
title: A discussion whose writer answer was lost ends every round
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5-happy-carson
claimed_at: 2026-10-07T09:58:30Z
created_at: 2026-10-06T15:36:43Z
completed_at:
branch: claude/happy-carson-c1hy91
depends_on:
  - 2026-10-06-a-failing-video-is-deferred
scope:
  - tools/video/automation/discuss.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/series.test.mjs
  - tools/video/automation/discuss.test.mjs
  - tools/video/automation/automation.test.mjs
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
  - .agents/skills/youtube-video/references/series.md
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

### 2026-10-07 done (claude-opus-5-5-happy-carson, PR #1361)

- `flow.mjs`: `move()`'s catch is now `Automation.sortFailure(state, error, { sends })`, unchanged
  for a unit (a pure extraction: the automation and series suites passed before the discussion
  used it). `discuss.mjs` `answerHeld` sorts every failure of the discussion's request there but
  an answer of nothing usable (still answered for the owner): a lost answer blocks the video as
  `uncertain:writer` and ends the run once (`unanswered`), a gone job as `job_gone:writer` as
  before, a refusal blocks it with the reason, a busy service defers it; the run's trouble, a
  STOP or lease and a job still running are thrown as before.
- Decided: only the line whose own request blocked the video holds (`blocked_line`, saved with
  the block and cleared by the retry), as a gone writer job's always did; it is sent once after
  the owner's retry. Holding every blocked video's line was tried and dropped: the site hands over
  the oldest unanswered line of every series (`messages.py` `next_message`), so one video blocked
  for days would hold every thread behind it. A video blocked for anything else now has the owner
  told it is blocked and to send the line again after the retry (`blockedReply`), instead of the
  untrue "這台工人沒有 … 的劇本"; the threads behind it move on.
- Decided here, not filed: a line on a document (`answerDocument`, no video to block, no durable
  job). A lost answer and a refusal are answered for the owner once (`lostReply`: it may have run
  and been paid, send the line again to ask again; `refusedReply`); a busy service holds the line
  for the rest of the run (`heldLines`) and it is asked next round; the run's trouble is thrown as
  before. `Automation.threadScope` sorts it without an import cycle.
- Tests (`series.test.mjs`): a durable discussion whose job turns `uncertain` (one round ends,
  the video blocked, a round later nothing sent or answered, the retry archives the journal and
  sends exactly one new request, its answer reaches the owner); a refused job (blocked with the
  reason, nothing sent until the retry); a busy job (deferred, the lane goes on, the line waits,
  sent once after the wait); the non-durable route losing the answer (one request over three
  rounds); a video blocked for its own reasons (the owner told, no writer request, the next thread
  comes up); and a document's lost, refused and busy planner request. Each new rule was removed in
  turn and a test failed.
- Not done: the stray journal of a discussion whose line was answered meanwhile (Notes, last
  point) has not been seen on the host. Answering the owner is still outside the try:
  a failed `messageAnswer` after a paid answer ends the run as before, and its answer stays
  saved for the next unit (durable) or is lost (not durable).
- Scope overlap: `2026-10-07-a-discussion-s-refused-script-revision` (the lexicon restore in
  `answerHeld`) shares discuss.mjs and flow.mjs; it waits until this lands.

### 2026-10-07 independent review (3 reviewers, each finding checked by a skeptic)

- Blocking, fixed: a long anime's discussion whose act request failed after its plan was paid
  for returned a line, so the unit settled the plan's saved run and the next attempt bought the
  plan again (4 plans in 8 rounds while the act stayed busy). A failure line now takes the video
  out of the unit's runs to settle (`answerHeld`, `runSlugs`); `discuss.test.mjs` pins it.
- Should-fix, fixed: a discussion's wait never reached the limit or the card, because the video's
  own trouble-free visit (`moved`) cleared `defer_count` between attempts; it now counts on its own
  (`discussion_waits`, cleared by an answer and by the retry), backs off, reports from the second
  wait and blocks as `deferred:writer` after DEFER_LIMIT. `blocked_line` is now saved with the
  block itself (no window). A block's reason names the line and what the retry sends within the
  card's 120 characters (`unanswered` and the refusal take `sends`).
- Should-fix, fixed (documents): a settled refusal of the model service's own
  (`video_ai_upstream_failed`, a vendor 400 such as a prompt too long or a revoked key) is answered
  once like the site's 4xx; any other wait is counted per line in `_series/<slug>/threads.json` and
  answered after DEFER_LIMIT rounds (`failingReply`), so no line holds the threads after it for
  good; a lost answer is saved there before its reply goes up, so a reply the site did not take is
  posted next round instead of the planner being asked, and paid, again.
- Noted, not changed: on the durable route the API records every failure after dispatch as
  uncertain (ai.py), so in production a busy vendor blocks the video as `uncertain:writer` (as its
  own writer's would) and holds the line for the owner's retry; the busy-wait path covers failures
  before dispatch and the non-durable route. The tests use what the API really records for each.
  A gone writer job of the video's own also holds a line on its screenplay, as before this ticket.
- Nits fixed: the replies speak to the owner and name the button 「重試這支影片」; `refusedReply`
  no longer contradicts itself; the skill's 討論串 section describes all of it
  (`.agents/skills/youtube-video/references/series.md`).
- Rejected by the skeptics: an endless refuse-retry loop (the owner's retry is the only resend, and
  dropping the video ends it) and a reply wrong after a blocked-from-done retry.

