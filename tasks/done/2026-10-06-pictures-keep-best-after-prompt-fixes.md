---
id: 2026-10-06-pictures-keep-best-after-prompt-fixes
title: Pictures a model takes no style plate for are judged from the look's text, and a slides shot still failing after its prompt fixes keeps its best picture for the owner's final review
status: done
priority: P1
area: tools
owner: claude-fable-5-1-video-unstuck
claimed_at: 2026-10-06T07:04:34Z
created_at: 2026-10-06T07:04:21Z
completed_at: 2026-10-07T01:03:45Z
branch: claude/video-unstuck-plate-accept
depends_on: []
scope:
  - apps/api/app/video_media/catalog.py
  - apps/api/app/video_automation/settings.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/tests/test_video_media_catalog.py
  - apps/api/tests/test_video_automation_settings.py
  - apps/api/tests/test_video_media_api.py
  - tools/video/core/state.mjs
  - tools/video/core/state.test.mjs
  - tools/video/media/prompt-budget.mjs
  - tools/video/media/media.test.mjs
  - tools/video/media/stages.mjs
  - tools/video/media/stages.test.mjs
  - tools/video/media/keyframes.mjs
  - tools/video/media/look-keyframes.test.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/prompts.mjs
  - tools/video/automation/prompts.test.mjs
  - tools/video/automation/story.mjs
  - tools/video/automation/story-prompts.mjs
  - tools/video/automation/story.test.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
  - tools/video/qa/cli.mjs
  - tools/video/qa/qa.test.mjs
  - docs/videos/ILLUSTRATED.md
---

# Pictures a model takes no style plate for are judged from the look's text, and a slides shot still failing after its prompt fixes keeps its best picture for the owner's final review

## Why

On 2026-10-06 nine host-made slides videos were `blocked` on /admin/videos. Three of them
(threads-parental, gemini-gems, sec-ai-trading) read "rendered as a photorealistic image
instead of a 2D risograph illustration; … differ from the style plate": the owner had set the
slides image model to MiniMax `image-01` on 10-04, and

- `media/keyframes.mjs` drew a style plate for every illustrated slides video and sent it with
  every shot as a `role: "style"` reference, and the judge was shown it and asked whether the
  picture was "in the same technique … as the picture labelled style plate";
- the MiniMax adapter (`apps/api/app/video_media/providers/minimax.py`) forwards only a
  `character` reference, so image-01 never saw the plate, drew its own idea of the prompt, and
  the judge failed every take against a plate the model could not follow. A prompt fix cannot
  change that, so `MAX_PROMPT_FIX_ROUNDS` ran out and the video blocked.

The owner decided (2026-10-06) to keep image-01 and make the tools fit it, and that a video
whose keyframes still fail after two prompt fixes must not block any more: keep the judge's
best take, go on to the cut, and have the owner look at the cut with the kept pictures
listed, instead of approving it on the quality check.

Three follow-ups from the review of PR #1339 ride along: the first draft never heard the
per-model prompt budget (the writer prompt said "at most 1000 characters"), `story.mjs`'s
prompt fix dropped `prompt_budget_chars`, and the over-budget branch of `keyframes.mjs`
discarded a shot's earlier takes.

## Definition of done

- [x] An illustrated slides video drawn with an image model the catalog says takes no style
      reference (image-01) gets no style plate: no plate request, no plate paid for, no plate
      sent to the judge, and the style judged from the look's text. A Gemini model keeps its
      plate; a server from before the field is read by its vendor.
- [x] A slides video whose keyframes still fail after `MAX_PROMPT_FIX_ROUNDS` keeps the judge's
      best take of every failing shot (`keyframes --accept-best`), its storyboard approves
      itself with those shots marked accepted, and its final cut goes up for the owner's manual
      review with the kept pictures and their remarks listed. A failing shot with no picture, a
      storyboard the owner sent back, and a drama still wait as before.
- [x] The first draft of a slides video hears `prompt_budget_chars` for the image model the
      settings will draw it with; the story's prompt fix carries it; a shot's earlier takes stay
      on record beside the budget note.

## Steps

- [x] Server: `catalog.MediaModel.style_references` (Gemini image models 1, image-01 0), the
      options view carries it; `storyboard_check_passed` skips the score and problems of a shot
      sent `accepted: true` and takes a null `overall` when every shot was accepted.
- [x] `media/stages.mjs` `takesStyleReference`; `media/keyframes.mjs` draws the plate only then,
      prints `style plate: skipped; …`, takes `--accept-best <ids|all>` (needs_review off,
      `accepted_with_problems`, verdict and takes kept, 保留 on the sheet, exit 1 while any shot
      still waits), and keeps a shot's earlier takes in the over-budget branch.
- [x] `core/state.mjs` `keyframeProblems`: an accepted shot's failed verdict is no review need.
- [x] `automation/flow.mjs`: `acceptBestPictures` after the rounds (slides, no owner note, every
      target with a picture) records `state.accepted_pictures`, a note, and gives the rounds
      back; `media()` prunes the list when a kept shot is drawn again; `gate()` pushes the final
      with `--manual-review`; `draftBudget` gives the first draft `prompt_budget_chars`
      (`slidesImageVendor` reads the settings, `IMAGE_MODEL_VENDORS` maps ids to vendors).
- [x] `review/sync.mjs`: storyboard shots `accepted: true`, `judge.overall` from the other shots,
      `payload.accepted`; the final reads `accepted_with_problems` from the manifest, goes up as
      a manual review with the reason, `accepted_pictures` and the summary line.
- [x] `qa/cli.mjs`: kept shots as warnings on the `assemble` item.
- [x] `automation/prompts.mjs` writer text, `SLIDES_CAMERA_WORDS`; `story.mjs` and
      `story-prompts.mjs` carry and explain `prompt_budget_chars`.
- [x] Tests: `test_video_media_catalog.py`, `test_video_automation_settings.py`,
      `test_video_media_api.py`; `look-keyframes.test.mjs` (three tests, one adjusted),
      `stages.test.mjs`, `media.test.mjs` (the vendor table pinned to catalog.py),
      `state.test.mjs`, `prompts.test.mjs`, `story.test.mjs`, `sync.test.mjs` (two),
      `qa.test.mjs`, `automation.test.mjs` (the slides walk extended, two new tests).
- [x] `docs/videos/ILLUSTRATED.md`: a dated section with the table and what to check after deploy.

## How to verify

```bash
node --test tools/video/media/look-keyframes.test.mjs tools/video/media/stages.test.mjs tools/video/media/media.test.mjs tools/video/core/state.test.mjs tools/video/automation/prompts.test.mjs tools/video/automation/story.test.mjs tools/video/review/sync.test.mjs tools/video/qa/qa.test.mjs tools/video/automation/automation.test.mjs
cd apps/api && uv run ruff check . && uv run mypy app && PYTHONUTF8=1 uv run pytest tests/test_video_media_catalog.py tests/test_video_automation_settings.py tests/test_video_media_api.py tests/test_video_media_providers.py
npm run check:tasks
```

On the host after deploy: retry one of the three videos blocked on the plate and watch the
worker log for `style plate: skipped; minimax/image-01 takes no style reference`; on a video
whose keyframes still fail twice, `N pictures kept with the judge's remarks after 2 prompt
fixes`, `auto.json.accepted_pictures`, the storyboard approved on arrival, and the final card
pending with "N 張插圖未通過 judge（…），需站主審看" in its summary.

## Notes

- `--accept-best` is taken by the worker only when the judge, not the owner, failed the
  pictures (`fixPrompts` with no `ownerNote`): a storyboard the owner sent back twice still
  blocks, since the owner is already looking. A drama's pictures block as before (the owner's
  decision was about the slides route; a drama's storyboard is the owner's gate anyway).
- The final gate's manual review does not depend on the worker's flag: `review-push --gate
  final` reads `accepted_with_problems` from keyframes/manifest.json itself, so a person
  pushing by hand gets the same card. The worker still passes `--manual-review`, which the
  walk test asserts.
- The worker's settings (`ToolSettingsView`) name the slides image model by id alone, without
  its vendor, and carry no `media_options`; `IMAGE_MODEL_VENDORS` in `prompt-budget.mjs` maps
  the catalog's ids and `media.test.mjs` holds it to `catalog.py`. An id the table does not
  know falls back to the drama's vendor when it is the drama's own model, else to the
  server's field limit (4000), which caps at the writer's 1000 anyway.
- `draftBudget` counts the heaviest look the video may get (the five print presets plus
  tech-story, which the writer may name itself; riso-teal on 2026-10-06), not the slug's own
  print run, and every whole-script rewrite (lint fix, screenplay fix, prompt fix) carries it
  beside the first draft (review of PR #1341). The replan path rewrites the brief with the
  planner, not the script; the `write()` after it carries the budget.
- When every shot of a board was accepted, `judge.overall` goes up as null and the server
  passes the board on its coverage alone; an `overall` of null beside a scored shot fails.
- Stacked on PR #1340 (`claude/video-unstuck-retry`), which is stacked on #1339 and #1337; the
  task was claimed with `--force` because those tasks, by the same owner, share `flow.mjs`,
  `keyframes.mjs` and the automation tests.
- The duration-review receipt (`docs/videos/long-form/review.json`) binds `flow.mjs`,
  `prompts.mjs`, `state.mjs`, `automation.test.mjs` and others touched here: `node
  tools/video/long-form/cli.mjs check` is red on them until a reviewer re-binds.

### 2026-10-07 標記完成（由站主授權，非原持有者）

- 證據：程式隨 PR #1341 於 2026-10-06 進 main（commit `a435f067`，標題同本票）；
  後續 #1344（`e5f9c058`）疊在它上面合併。分支已刪。
- 票停在 review、持有者 claude-fable-5-1-video-unstuck，佔住 `flow.mjs`、`keyframes.mjs`、
  `stages.mjs` 與 automation 測試等，擋住約 21 張票。站主 2026-10-07 同意由 claude-opus-5-5 代為結案。
- 清單全部已勾，沒有未完成項目要交代去向。上面 Notes 記的 long-form 審查收據重綁仍待審查者處理。
