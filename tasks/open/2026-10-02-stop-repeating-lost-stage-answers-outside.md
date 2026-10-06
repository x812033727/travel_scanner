---
id: 2026-10-02-stop-repeating-lost-stage-answers-outside
title: Stop repeating lost stage answers outside a video's own steps
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5-shorts-planner-lost-answers
claimed_at: 2026-10-05T23:49:11Z
created_at: 2026-10-02T15:22:48Z
completed_at:
branch: claude/shorts-planner-lost-answers
depends_on:
  - 2026-09-29-prevent-lost-long-running-language-stages
scope:
  - tools/video/automation/shorts.mjs
  - tools/video/automation/shorts.test.mjs
---

# Stop repeating lost stage answers outside a video's own steps

## Why

Since 2026-09-29-prevent-lost-long-running-language-stages, the worker's client no
longer sends a stage run again when the request went out and its answer was lost
(`RUN_UNCERTAIN` in `tools/video/automation/client.mjs`: the web route's 504
`video_ai_run_uncertain`, a gateway 5xx, a dropped connection). The model may have
run and been paid for on the server. A video's own steps (`Automation.move`:
production stages and languages) stop that video for the owner's retry.

The stage calls that are not one of a video's own steps still end the `auto` run
with the error, and the next round (a few minutes later) asks the same model call
again. The paths, corrected on 2026-10-06 against origin/main a9e4c3851:

- flow.mjs `draft()` and `draftDrama()`. `draftEpisode()` makes no stage call.
- Jev's judgements across rounds: `submitOutline()` through review/sync.mjs
  `judgeOutline()`, and qa/cli.mjs `policyItem()` and shorts/qa.mjs `judgePolicy`.
  Inside one call they are already sent once (#1237).
- series.mjs `judgeDocument`/`planDocument` and discuss.mjs `answerDocument` and the
  screenplay discussion writers.
- The Shorts planner jobs in automation/shorts.mjs (the day's plan, the day's brief, the
  week's report), and a lab or highlight Short's stages in shorts/lab.mjs.

story.mjs and compilation.mjs are not on the list. Their stage calls run only inside
`advance()` (flow.mjs:1414, :1419), so `move()` already covers them.

## Definition of done

- [x] The Shorts planner jobs (`tools/video/automation/shorts.mjs`): a lost answer is
  recorded under the job's slug in `_shorts/shorts-state.json` (`lost`). The same call is
  not asked again on its own, and the owner sees why (the worker log; for the report, the
  report on the site).
- [ ] A lost answer in each of the other paths is recorded where the path keeps its
  state, and the same call is not asked again on its own; the owner sees why. Moved to
  2026-10-05-hold-lost-planner-and-jev-answers.
- [ ] Jev's judge calls do not repeat a judgement whose answer was lost. Moved to
  2026-10-05-hold-lost-planner-and-jev-answers.

## Steps

- [x] List each `automation.stage(...)` / `api.run(...)` caller outside `move()` and
  where it records progress. The list, with line numbers, is in the follow-up ticket's Why.
- [x] Decide how the owner resumes each Shorts planner job (Notes). For the other
  paths, the follow-up ticket's Steps carry a proposal.

## How to verify

Inject a fetch that runs the stage on the fake site and answers 504
`video_ai_run_uncertain` (see `lostAnswer` in automation.test.mjs) for each path;
the run count for that call stays 1 across two `auto` rounds.

For the Shorts planner jobs: `node --test tools/video/automation/shorts.test.mjs`. Its
three "lost" tests use `fakeSite({ lose })` and fail on the old shorts.mjs.

## Notes

- Filed from 2026-09-29-prevent-lost-long-running-language-stages, which covered the
  video steps and the language units only.
- 2026-10-06, claude-opus-5-5-shorts-planner-lost-answers: partly done. The rest is split
  into 2026-10-05-hold-lost-planner-and-jev-answers. Every remaining file is either bound
  by the long-form duration receipt (flow.mjs, series.mjs, discuss.mjs, automation.test.mjs,
  series.test.mjs, review/sync.mjs, qa/cli.mjs), so it needs an independent DURATION_ONLY
  increment, or is edited by other sessions' open draft PRs: #1312 and #1301 for flow.mjs
  and automation.test.mjs, #1310 for shorts/lab.mjs. client.mjs belongs to
  2026-10-05-automation-client-retries-a-judge-s.
- The ticket's scope was cut down to the two files changed here. The other paths moved
  to the follow-up ticket's scope.
- What the Shorts worker does now. `ShortsWorker.attempt()` catches `RUN_UNCERTAIN` and
  `unanswered()` records `{ kind, variant, at, why }` under the slug: `shorts-plan-<day>`,
  `shorts-brief-<day>` or `shorts-report-<week_start>`. Entries older than 14 days are
  dropped when a new one is recorded. Before `plan()`, `brief()` or `report()` asks,
  `lostBefore(slug)` returns the earlier entry, and if there is one nothing is sent.
  Only that exact slug is held, so the next day's plan or brief, or the next week's
  report, is a new call.
- How each job carries on without holding up the server's queue. The server names a job
  again until it has a result, and the other Shorts jobs wait behind it:
  - Plan: an empty plan is recorded (`shortsPlan([])`, as after two failures). The server
    then names no plan for 12 hours (`PLAN_EVERY`). If it names the same day's plan again,
    the worker records another empty plan.
  - Brief: the server takes no empty topic list (`TopicsIn` needs one topic or more), so
    the worker sets its own 12-hour `holds.brief`. When that runs out on the same day, the
    hold is set again.
  - Report: a report that says the planner's answer was lost (in Chinese, followed by the
    raw-value table) is saved with `shortsReport`. The owner reads it on the site, and the
    server stops naming that week. The loss is recorded before the save. If the save fails,
    the next round saves the same report without asking the model.
- An owner who wants the same call asked again sooner can remove its slug from
  `lost` in `<VIDEO_WORKDIR>/_shorts/shorts-state.json`. No site retry exists for the
  planner jobs, and none was added.
- A lost answer does not count in `failures`, and the unusable answer from an earlier try
  in the same unit is not kept. This follows flow.mjs `unanswered()`.
