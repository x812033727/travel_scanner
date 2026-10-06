---
id: 2026-10-06-a-discussion-whose-writer-answer-was
title: A discussion whose writer answer was lost ends every round
status: open
priority: P2
area: tools
owner:
claimed_at:
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

- [ ] An error of a screenplay discussion's request never ends a round more than once for the
      same cause: a lost answer blocks the video as `uncertain:writer` (as its own writer's does),
      a refusal blocks it with the reason, a service that is busy makes the line wait.
- [ ] While the video is blocked that way the owner's line stays unanswered (no "no screenplay
      here" reply), and after the owner's retry the line is sent exactly once more.
- [ ] No discussion request is paid for twice without the owner's retry.

## Steps

- [ ] `answerScript`'s catch: sort the error as `move()` does (share the code rather than copy
      it): `RUN_UNCERTAIN` goes to `Automation.unanswered`, a "video" scope to `block`, a "wait"
      scope to `defer` (the line is then held by `resting`), a "run" scope is thrown as today.
- [ ] Hold the line while its video is blocked as `uncertain:writer` (today only
      `job_gone:writer` holds it, `discuss.mjs`); decide whether every block should hold the line
      instead of answering that there is no screenplay.
- [ ] Tests in `series.test.mjs` on the durable route (the helper `durableDiscussion` is there):
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
