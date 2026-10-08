---
id: 2026-10-08-a-document-line-whose-planner-request
title: A document line whose planner request keeps waiting holds every discussion thread behind it
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-08T02:24:31Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/discuss.mjs
  - tools/video/automation/discuss.test.mjs
  - tools/video/automation/series.test.mjs
  - .agents/skills/youtube-video/references/series.md
  - .claude/skills/youtube-video/references/series.md
  - tools/video/automation/flow.mjs
---

# A document line whose planner request keeps waiting holds every discussion thread behind it

## Why

The worker answers the owner's discussion lines one at a time, and the site always hands over
the oldest unanswered line across every series (`apps/api/app/video_automation/messages.py`
`next_message`). On a **document** line (setting, outline, chapter, bible) whose planner
request fails in a way that may pass (`errorScope` "wait": any 5xx or 429, for example 503
`video_ai_upstream_busy`), `discuss.mjs` `answerDocument` only adds the line to
`automation.waitingLines`, a set that lives for one run. The next run asks the planner again,
with the client's retries, and nothing counts the runs. A line whose request never clears is
never answered, and every other discussion thread in every series waits behind it for good,
with nothing on the page; only a log line says so.

The commonest persistent trigger is a settled refusal of the model service itself: 502
`video_ai_upstream_failed`, which `apps/api` returns for any vendor 4xx (a prompt over the
model's context on a long setting document, a revoked key). `errorScope` makes every status
of 500 or more "wait", so the same request is sent, and refused, every run.

#1361 had handled both on its own version of 2026-10-06-a-discussion-whose-writer-answer-was
(a per-line wait count in `_series/<slug>/threads.json`, `failingReply` after six runs, and
`video_ai_upstream_failed` answered at once with `refusedReply`). #1364 landed that ticket
first with its own design, and #1361 was rebased onto main without them (2026-10-08), so they
are filed here against main's code. Found by the overlap comparison of the two PRs.

## Definition of done

- [ ] A document line whose planner request keeps waiting is answered once, after a bounded
      number of runs, with a reply that says the request kept failing and how to ask again; the
      threads behind it then move on. A line that gets through earlier clears its count.
- [ ] A document line refused by the model service (502 `video_ai_upstream_failed`) is answered
      once with the refusal (shorten the line, or check the AI settings), not asked every run.
- [ ] The youtube-video skill's 討論串 section says what main does when a discussion's request
      fails, for screenplays and documents (lost answer, refusal, waits, held lines, the kept
      reply in `discussion-answer.json`), in main's terms.

## Steps

- [ ] `discuss.mjs` `answerDocument`: a per-line count of "wait" runs kept under
      `_series/<slug>/` (beside `discussion-answer.json`, not in it), a `failingReply` posted
      through `postAnswer` at the limit (the worker's `DEFER_LIMIT` is 6; discuss.mjs cannot
      import flow.mjs, so pass it on the automation), the count dropped once the line is answered.
- [ ] Answer `video_ai_upstream_failed` on a document line with `refusedReply` at once.
- [ ] Also consider, from the same comparison (each low): a screenplay line on a video blocked
      `uncertain:writer` by the video's **own** writer stage is held by `heldBy` until the
      owner's retry, and every thread behind it waits that long, although main answers every
      other block with `blockedReply` for exactly that reason (#1361 held only this line's own
      `blocked_line` and `job_gone:writer`); and `lineFailed` sets `blocked_line` only after
      `requestFailed` has saved the block and awaited `reportBlocked`, so a worker killed in
      that PUT leaves a blocked video without the line it holds.
- [ ] Tests in discuss.test.mjs or series.test.mjs (six runs of waiting, then the reply; a 502
      `video_ai_upstream_failed`); the skill bullet in both copies of series.md.

## How to verify

`node --test tools/video/automation/discuss.test.mjs tools/video/automation/series.test.mjs`,
then `npm run test:tools` (the skill copies are compared there).

## Notes

#1361's versions for reference: commits d283fe24a and df6427a7d on its branch before the
rebase (a70357543: `discuss.mjs` `threadNotes`, `failingReply`; `flow.mjs` `sortFailure`).
Do not copy them: main has `postAnswer`/`takeUnposted`/`keepReply` and `lineFailed` instead.
