---
id: 2026-10-02-stop-repeating-lost-stage-answers-outside
title: Stop repeating lost stage answers outside a video's own steps
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-02T15:22:48Z
completed_at:
branch:
depends_on:
  - 2026-09-29-prevent-lost-long-running-language-stages
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/series.mjs
  - tools/video/automation/discuss.mjs
  - tools/video/automation/story.mjs
  - tools/video/automation/shorts.mjs
  - tools/video/automation/compilation.mjs
  - tools/video/automation/client.mjs
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
again: a new draft's planner (`draft`, `draftDrama`, `draftEpisode` in flow.mjs),
series documents and recaps (series.mjs), discussion answers (discuss.mjs), brand
stories (story.mjs), Shorts (shorts.mjs) and compilations (compilation.mjs). Jev's
`judgeOutline` / `judgePolicy` POSTs are model calls too and still use the generic
retry policy (4 attempts on any 5xx).

## Definition of done

- [ ] A lost answer in each of those paths is recorded where the path keeps its
  state, and the same call is not asked again on its own; the owner sees why.
- [ ] Jev's judge calls do not repeat a judgement whose answer was lost.

## Steps

- [ ] List each `automation.stage(...)` / `api.run(...)` caller outside `move()` and
  where it records progress (series job, discussion message, Shorts topic, …).
- [ ] Decide per path how the owner resumes it (an existing retry or a new one).

## How to verify

Inject a fetch that runs the stage on the fake site and answers 504
`video_ai_run_uncertain` (see `lostAnswer` in automation.test.mjs) for each path;
the run count for that call stays 1 across two `auto` rounds.

## Notes

- Filed from 2026-09-29-prevent-lost-long-running-language-stages, which covered the
  video steps and the language units only.
