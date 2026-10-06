---
id: 2026-10-06-a-pending-discussion-job-and-the
title: A pending discussion job and the bookkeeping's site calls do not hold their video
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-06T13:39:27Z
completed_at:
branch:
depends_on:
  - 2026-10-06-a-failing-video-is-deferred
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/discuss.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/automation/series.test.mjs
---

# A pending discussion job and the bookkeeping's site calls do not hold their video

## Why

Two gaps read in the code while the review of PR #1342 was being answered
(`2026-10-06-a-failing-video-is-deferred`). Neither comes from that pull request, and neither was
changed there; both are the same kind of trouble its review found: a step that acts on a video
while another step has something of that video in flight.

1. **A discussion whose writer job is still running does not hold its video.** A line on a
   screenplay is answered by the writer (`discuss.mjs` `answerScript`, variant `discuss` or
   `anime-discuss-plan`), a durable job. When it is not done within the client's 25 seconds it
   throws RUN_PENDING; outside a video's unit that ends the run (`flow.mjs` `step()`), and nothing
   remembers that this video has a writer job in flight. On the next round the video's own unit
   comes first. If the owner sent the screenplay back in the meantime, `fixScript` sends the
   writer's `episode` request while the discussion job runs: two writer jobs for one video, and
   whichever answer lands second rewrites `video.json` from a script the other no longer matches.
   If the owner approved it, the video moves on and the discussion's rewrite then lands on an
   approved script. Since PR #1342 `answerScript` holds a line while its video is not at rest;
   this is the mirror image, and it is as old as the durable writer.
2. **The first lane's bookkeeping awaits the site for a video it does not hold.**
   `recordVideoId` and `tellCompilationDone` (`flow.mjs` `bookkeeping()`) are called for a video
   that is `active` or `done` and not in `busy`; they await a report or `compilationDone`, and
   `tellCompilationDone` then saves the first lane's copy of `auto.json`. A second lane may have
   taken the video in between (its languages, say) and saved its own progress, which that save
   writes over. The retry acknowledgement had the same shape and was fixed in PR #1342 by holding
   the video in `busy` from before the save to after the report.

## Definition of done

- [ ] While a discussion's writer job for a video is still running on the server, no other writer
      request is sent for that video and its own stages wait; the discussion's answer is taken on
      a later round, and the video moves again after it.
- [ ] No step of the first lane's bookkeeping saves `auto.json` for a video another lane may have
      taken since the step read it.

## Steps

- [ ] `step()`: a RUN_PENDING thrown outside a video's unit that names a video (`error.slug`,
      `tagged` by `client.mjs`) and whose slug is one of this worker's videos sets that video
      aside in the shared `pendingUntil` instead of only ending the run, or `stepUnit` asks the
      receipt store whether the video has an unfinished writer journal before moving it. Decide
      which with a test that owns the sequence: the owner's line, a pending `discuss` job, the
      owner's rejection, the next round.
- [ ] `bookkeeping()`: hold the video in `busy` around `recordVideoId` and `tellCompilationDone`
      (a `try`/`finally`, as the retry acknowledgement does), or have them save before the await
      and nothing after it.
- [ ] Tests in `automation.test.mjs` (two lanes, the site call held in flight) and
      `series.test.mjs` (the discussion sequence above).

## How to verify

```bash
node --test tools/video/automation/automation.test.mjs tools/video/automation/series.test.mjs \
  tools/video/automation/discuss.test.mjs
```

## Notes

- Found by reading, not seen on the host. The first needs the owner to act on the script gate
  within the minutes a discussion job runs; the second needs a second lane to take a finished
  video during one site call.
- `flow.mjs` and `automation.test.mjs` are bound by the duration-review receipt
  (`docs/videos/long-form/review.json`): a change here needs the independent re-bind.
- A line on a screenplay also waits behind a STOP file in its video's own work directory only by
  accident: with durable runs the client does not send while the file is there and the run ends
  on RUN_PENDING every round. Holding such a line in `answerScript` (the video is held, so is its
  line) would be the same kind of guard; decide it with the first item.
