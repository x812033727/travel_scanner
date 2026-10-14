---
id: 2026-10-14-support-10-minute-minimax-cute-brand
title: Support 10-minute MiniMax cute brand-story series
status: review
priority: P1
area: tools
owner: codex-8a78-story-route
claimed_at: 2026-10-14T16:11:01Z
created_at: 2026-10-14T16:10:55Z
completed_at:
branch: codex/brand-stories-five-20261014
depends_on: []
scope:
  - tools/video/automation/story.mjs
  - tools/video/automation/story.test.mjs
  - tools/video/story-plans/plan.mjs
  - tools/video/story-plans/plan.test.mjs
  - apps/api/app/video_automation/stories.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/series.py
  - apps/api/tests/test_video_story_import.py
  - apps/api/tests/test_video_story_series.py
  - tools/video/core/drama.mjs
  - tools/video/core/explainer-family.test.mjs
  - tools/video/core/story.test.mjs
---

# Support 10-minute MiniMax cute brand-story series

## Why

The owner selected MiniMax `image-01`, the exact `{"preset":"cute-mystery"}` look and about 10 minutes for five brand stories after the A01/B18 pilot. The existing story-series importer and compiler require 12–15 minutes with nonempty custom style/negative; the worker forces `video.json.look.preset=custom`. Merely changing the five treatments would still produce the old visuals and length. Preserve the original 100-story Gemini/13-minute route while allowing a separate five-story series to use the new settings.

## Definition of done

- [x] A new story series with 10 minutes, `image-01` and exact `{"preset":"cute-mystery"}` look validates through local compiler and API importer checks.
- [x] The six-chapter story worker emits a `video.json` with that exact look, while original custom story series still emits its old look unchanged.
- [x] Focused JS/Python regression tests pass, including rejection of malformed mixed custom/preset looks.

## Steps

- [x] Extend the narrow story-series validators/schema without changing the original 100-story source files.
- [x] Carry the preset through series state to `video.json`; keep the story writer and fact-checker route.
- [x] Run focused tests and record any remaining server or import gate.

## How to verify

Run `node --test tools/video/story-plans/plan.test.mjs tools/video/automation/story.test.mjs` plus the targeted API tests under `apps/api`, and check a 10-minute preset payload and original 13-minute custom payload. This task does not import, render or purchase media.

## Notes

- The main branch's `curio-*` visual lint is slug-scoped; it does not automatically validate `story-*` episodes. The five-film task records its separate visual acceptance checks.
- The importer starts new `kind=story` series as active. The five-series payload stays local/dry-run until the A01/B18 pilot and owner gate; this task only makes the specified format possible.
- Local receipt (2026-10-15): `seriesProblems` accepts the five-series `series.json`; Python `check_story_file` accepts all five selected episode rows with zero problems/refusals. An in-memory SQLite import of one selected episode persisted 10 minutes, `image-01`, `style_preset=custom` and exact `look={"preset":"cute-mystery"}`. No live import was run.
- Worker receipt: the new route has a 9:00–11:00 narration band, `video.json.target_minutes=[9,11]`, and 80 budgeted illustrations at about 7.5 seconds each. The original 13-minute route retains its 11:30–15:30 band, `[12,15]` video target and 90 budgeted shots. The cute route's internal `brief.md` adds the two sections required by the preset lint; custom briefs keep their earlier sections.
- A29 cast smoke test: compose a video with its actual two-person cast, one shot referencing a cast ID, its real series look, and fixture scenes; `validateVideo` and `lintVideo` each reported zero errors. Its 21 warnings reflect short synthetic fixture scenes, not an approved production script.
- Checks: `node --test tools/video/automation/story.test.mjs` 21/21 passed using an ASCII `subst` drive because Windows Node 24 crashes in the existing fixture `cpSync` when the checkout's Unicode path is used directly; `node --test tools/video/story-plans/plan.test.mjs tools/video/core/explainer-family.test.mjs tools/video/core/duration.test.mjs` 47/47 passed; targeted Python pytest 9/9 passed; Ruff and mypy on changed Python files passed. The temporary drive mapping was removed.
- `npm run check:tasks` is currently red for an unrelated duplicate A21 correction ticket in both `tasks/open/` and `tasks/done/`; this task's new `review` status is not the failure.
- API PATCH follow-up (2026-10-15): added `series.py` to this ticket's scope after `who-is-on-it --scope apps/api/app/video_automation/series.py` found no active task or open PR touching it. The service checks the merged story series state before saving a change to look, duration, image model or style preset. A cute look must retain exactly 10 minutes, `image-01` and story `custom`; moving back to the original custom look requires its 12–15 minute story length and `custom` writer preset in one PATCH. Focused service/schema tests cover each partial break and both complete transitions. Checks: `uv run pytest tests/test_video_story_series.py tests/test_video_series.py -q` 58 passed, 3 skipped; Ruff and mypy on the two changed Python files passed. `npm run check:tasks` is still red only for the duplicate A21 open/done ticket noted above.
- Still gated: this is a local code and fixture check. The five-series live import, generated audio/images, render, upload, publication and owner acceptance remain separate decisions and receipts.
