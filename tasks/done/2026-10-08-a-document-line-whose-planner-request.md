---
id: 2026-10-08-a-document-line-whose-planner-request
title: A document line whose planner request keeps waiting holds every discussion thread behind it
status: done
priority: P2
area: tools
owner: claude-opus-5-5-pr-tidy
claimed_at: 2026-10-16T17:40:25Z
created_at: 2026-10-08T02:24:31Z
completed_at: 2026-10-16T17:42:07Z
branch: claude/youthful-brahmagupta-1giys7
depends_on: []
scope:
  - tools/video/automation/discuss.mjs
  - tools/video/automation/discuss.test.mjs
  - .agents/skills/youtube-video/references/series.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
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

- [x] A document line whose planner request keeps waiting is answered once, after a bounded
      number of runs, with a reply that says the request kept failing and how to ask again; the
      threads behind it then move on. A line that gets through earlier clears its count.
- [x] A document line refused by the model service (502 `video_ai_upstream_failed`) is answered
      once with the refusal (shorten the line, or check the AI settings), not asked every run.
- [x] The youtube-video skill's 討論串 section says what main does when a discussion's request
      fails, for screenplays and documents (lost answer, refusal, waits, held lines, the kept
      reply in `discussion-answer.json`), in main's terms.

## Steps

- [x] `discuss.mjs` `answerDocument`: a per-line count of "wait" runs kept under
      `_series/<slug>/` (beside `discussion-answer.json`, not in it), a `failingReply` posted
      through `postAnswer` at the limit (the worker's `DEFER_LIMIT` is 6; discuss.mjs cannot
      import flow.mjs, so pass it on the automation), the count dropped once the line is answered.
- [x] Answer `video_ai_upstream_failed` on a document line with `refusedReply` at once.
- [x] Also consider, from the same comparison (each low): a screenplay line on a video blocked
      `uncertain:writer` by the video's **own** writer stage is held by `heldBy` until the
      owner's retry, and every thread behind it waits that long, although main answers every
      other block with `blockedReply` for exactly that reason (#1361 held only this line's own
      `blocked_line` and `job_gone:writer`); and `lineFailed` sets `blocked_line` only after
      `requestFailed` has saved the block and awaited `reportBlocked`, so a worker killed in
      that PUT leaves a blocked video without the line it holds.
- [x] Tests in discuss.test.mjs or series.test.mjs (six runs of waiting, then the reply; a 502
      `video_ai_upstream_failed`); the skill bullet in
      `.agents/skills/youtube-video/references/series.md`, the only copy (only SKILL.md is copied
      under `.claude/skills`).

## How to verify

`node --test tools/video/automation/discuss.test.mjs tools/video/automation/series.test.mjs`,
then `npm run test:tools`.

## Notes

#1361's versions for reference: commits d283fe24a and df6427a7d on its branch before the
rebase (a70357543: `discuss.mjs` `threadNotes`, `failingReply`; `flow.mjs` `sortFailure`).
Do not copy them: main has `postAnswer`/`takeUnposted`/`keepReply` and `lineFailed` instead.

### 2026-10-16 fix (claude-opus-5-5-pr-tidy)

`tools/video/automation/discuss.mjs` `answerDocument`:
- A document line whose planner request fails with errorScope "wait" now counts its runs in
  `_series/<slug>/discussion-waits.json`.
  - From the `MAX_DOCUMENT_WAITS`th run (6), the owner is told once with `failingReply(runs, why)`
    and the count goes, so the threads behind it move on.
  - Every answered path clears the line's count: a reply, an unusable answer, a lost answer or a
    refusal. A later wait counts from one again.
- A 502 `video_ai_upstream_failed` (the model service's own refusal) is answered at once with
  `refusedReply`, like a 4xx, instead of being sent and refused every run.
- Within a run, `automation.waitingLines` still keeps the line from being asked twice, so the count
  goes up once a run.

The design follows what #1361 had: a per-line wait count, an answer after six runs, and an
immediate refusal. The count lives in its own file beside the series' planner answers, not in
`threads.json`.

`.agents/skills/youtube-video/references/series.md` 討論串 gains a bullet on what main does when a
document or screenplay discussion request fails: the lost answer, refusal, waits and failingReply
for documents; uncertain or job_gone blocks, `blocked_line`, deferral and blockedReply for
screenplays; and the kept reply in `discussion-answer.json`.

Scope:
- `flow.mjs` and `series.test.mjs` were not needed and left the scope.
- The duration receipt files joined it, because `discuss.mjs` is in `REVIEW_FILES`. They overlap
  only as the shared append-only receipt ledger, with no open PR on them, so the claim used
  `--force`.
- The receipt increment was written by an independent reviewer (`claude-pr-review-discuss-waits`).

Ran:
- `node --test tools/video/automation/discuss.test.mjs`: 13/13, two of them new.
  - A line kept busy for six runs, each a fresh Automation, is answered on the sixth. A line that
    got through on run six clears its count, and its next wait counts from one.
  - A 502 `video_ai_upstream_failed` is answered at once, asked once.
- `npm run test:tools`: 2389 passed. The one failure was the stale receipt before it was rebound.
- `tools/video/long-form/cli.mjs check`: PASS after the receipt.
