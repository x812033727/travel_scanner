---
id: 2026-10-05-hold-lost-planner-and-jev-answers
title: Hold lost planner and Jev answers across rounds in drafts, series and Shorts
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5-happy-carson
claimed_at: 2026-10-07T11:22:28Z
created_at: 2026-10-05T23:49:44Z
completed_at:
branch: claude/happy-carson-c1hy91
depends_on:
  - 2026-10-02-stop-repeating-lost-stage-answers-outside
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/series.mjs
  - tools/video/automation/discuss.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/automation/series.test.mjs
  - tools/video/automation/discuss.test.mjs
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
  - tools/video/qa/cli.mjs
  - tools/video/qa/qa.test.mjs
  - tools/video/shorts/lab.mjs
  - tools/video/shorts/lab.test.mjs
  - tools/video/shorts/qa.mjs
---

# Hold lost planner and Jev answers across rounds in drafts, series and Shorts

## Why

When a stage run or a Jev judgement is sent and its answer is lost on the way, the worker's
client (`tools/video/automation/client.mjs`) does not send it again. It throws `RUN_UNCERTAIN`
instead: the web route's 504 `video_ai_run_uncertain`, a gateway 5xx, or a dropped connection.
The model or Jev may already have run, and been charged, on the server. The server keeps no
answer that the worker could fetch again.

A video's own steps (`Automation.move()` → `unanswered()`, flow.mjs:714-726 and :888) already
stop the video until the owner retries. The Shorts planner jobs (`tools/video/automation/shorts.mjs`)
were fixed in 2026-10-02-stop-repeating-lost-stage-answers-outside. The callers below still end
the round with the error, or count the loss as an ordinary failure. The next round, a few
minutes later, then sends the same paid call again. Line numbers are for origin/main d829b18dc.

- `flow.mjs` `draft()` (:1011, planner at :1022) catches `OUTPUT_INVALID` only. On
  `RUN_UNCERTAIN` it throws before `last_draft_at` is written to `GLOBAL_FILE` (:1032), so the
  next round asks the planner again under a new `draft-<minute>` slug.
- `flow.mjs` `draftDrama()` (:1105, planner at :1117), reached from :785. The site's
  `dramaNext()` hands back the same request next round, and it is asked again.
- Jev across rounds. `flow.mjs` `submitOutline()` (:1069, judge at :1073) calls `review/sync.mjs`
  `judgeOutline()` (:208-223). That function returns `{ status: "later" }` for every
  AutomationError that is not the owner's, including `RUN_UNCERTAIN`, so Jev is asked again
  on the next run. `review-push --gate outline` (sync.mjs:395) works the same way. #1237
  (`2026-10-04-prevent-automatic-retries-of-paid-video`) stopped the resend inside one call
  only.
- `qa/cli.mjs` `policyItem()` (:54-71) turns a lost Jev policy answer into a failed `policy`
  item with `who: "service"`, so the next `qa` run asks Jev again. A Short's QA does the same
  (`shorts/qa.mjs:319`).
- `series.mjs` `judgeDocument` (:563, verifier) and `planDocument` (:584, planner) catch
  `OUTPUT_INVALID` only. So do `discuss.mjs` `answerDocument` (:104, planner) and the
  screenplay discussion writers (:179 `anime-discuss-plan`, :185 `discuss`).
- `shorts/lab.mjs` `ask()` (:410) is every writing and checking stage of a lab or highlight
  Short. Its `RUN_UNCERTAIN` (`who: "service"`, status 504 or 0) is caught as `transient` at
  :506-508, "the next round tries again". `subject()` (:562) counts a lost answer from the
  tested model as a technical failure and asks once more on the next round.

These paths need no change: `story.mjs` and `compilation.mjs` make their stage calls only
inside `advance()` (flow.mjs:1427 `advanceCompilation`, :1432 `advanceStory`), which is
inside `move()`. `startStory`, `draftStory`, `startCompilation` and `draftEpisode()` (:1169)
make no stage call.

## Definition of done

- [ ] For each path above, a lost answer is recorded where that path keeps its state. The
  same call is not asked again on its own, and the owner can see why (on /admin/videos, the
  series thread, or the video's checklist).
- [ ] A Jev outline or policy judgement whose answer was lost is not asked again on the next
  round or run. It waits for the owner's retry.
- [ ] A later call that is genuinely different still goes out: the next scheduled draft, a new
  drama request, a changed final cut.

## Steps

- [ ] `draft()` and `draftDrama()`: record the loss in `GLOBAL_FILE` (for example
  `lost_draft: { slug, at, why }`) and write `last_draft_at`, so the next interval is a new
  call. For a drama request, tell the site the request is held: check what `dramaNext()`
  offers for that.
- [ ] `submitOutline()`/`judgeOutline()`: tell `RUN_UNCERTAIN` apart from "later". Keep it in
  the video's state (for example `outline_lost`) and block the video for the owner's retry
  instead of "the next run asks again". `review-push --gate outline` should say the same and
  leave the outline to the owner.
- [ ] `series.mjs` and `discuss.mjs`: mark the series job or discussion message as lost
  through the site calls these paths already use (`messageAnswer`, the series job's own
  calls), and do not ask again until the owner retries.
- [ ] `qa/cli.mjs` `policyItem()` and `shorts/qa.mjs`: keep the uncertain judgement per
  final-cut hash in `review/qa.json` and do not ask again for the same hash. The item says
  the outcome is unknown and is for the owner.
- [ ] `shorts/lab.mjs`: block the Short with the reason when `ask()` or `subject()` loses an
  answer. `ShortsWorker.retried()` (automation/shorts.mjs) already resumes a blocked Short
  when the owner asks for a retry.
- [ ] Tests for each path. Use the 504 `video_ai_run_uncertain` fake (`lostAnswer`,
  automation.test.mjs:736), or the `lose` option of `fakeSite` in
  `tools/video/automation/shorts.test.mjs`.

## How to verify

For each path, inject a fetch that runs the stage (or the judge) on the fake site and then
answers 504 `video_ai_run_uncertain`. Across two `auto` rounds or two runs of the command,
the run count for that call must stay at 1.

```bash
node --test tools/video/automation/automation.test.mjs tools/video/automation/series.test.mjs tools/video/automation/discuss.test.mjs tools/video/review/sync.test.mjs tools/video/qa/qa.test.mjs tools/video/shorts/lab.test.mjs
npm run test:tools
node tools/video/long-form/cli.mjs check
```

## Notes

- Split from 2026-10-02-stop-repeating-lost-stage-answers-outside. That ticket did the Shorts
  planner jobs in `tools/video/automation/shorts.mjs`. This one is the rest of its Definition
  of done.
- Receipt: `flow.mjs`, `series.mjs`, `discuss.mjs`, `automation.test.mjs`, `series.test.mjs`,
  `review/sync.mjs`, `review/sync.test.mjs`, `qa/cli.mjs` and `qa/qa.test.mjs` are bound by
  `docs/videos/long-form/review.json`. Changing them turns `cli.mjs check` red until an
  independent reviewer adds a DURATION_ONLY increment. Do not edit review.json yourself.
- The draft PRs that held these files back when this ticket was split have all landed in
  train #1315 (d829b18dc): #1312 and #1301 (`flow.mjs`, `automation.test.mjs`) and #1310
  (`shorts/lab.mjs`). Before claiming, run `who-is-on-it.mjs --scope` for each path again.
- `client.mjs` is out of scope here. Whether the judge routes' 502 settles a judgement is
  ticket 2026-10-05-automation-client-retries-a-judge-s.
- The Shorts pattern to copy (automation/shorts.mjs `unanswered`, `lostBefore`): keep the lost
  slug with `{ kind, variant, at, why }`. Check it before asking. Drop entries after 14 days.
  Give the site something to record, so a job the server keeps naming does not hold up the
  queue.
