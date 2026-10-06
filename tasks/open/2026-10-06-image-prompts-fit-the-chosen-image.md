---
id: 2026-10-06-image-prompts-fit-the-chosen-image
title: Image prompts fit the chosen image model's limit (MiniMax 1500) instead of being refused
status: in-progress
priority: P1
area: tools
owner: claude-fable-5-1-video-unstuck
claimed_at: 2026-10-06T05:58:01Z
created_at: 2026-10-06T05:57:42Z
completed_at:
branch: claude/video-unstuck-prompt-budget
depends_on: []
scope:
  - tools/video/media/prompt-budget.mjs
  - tools/video/media/keyframes.mjs
  - tools/video/media/stages.mjs
  - tools/video/media/media.test.mjs
  - tools/video/media/look-keyframes.test.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/prompts.mjs
  - tools/video/automation/automation.test.mjs
  - apps/api/app/video_media/admin_api.py
  - apps/api/tests/test_video_media_api.py
---

# Image prompts fit the chosen image model's limit (MiniMax 1500) instead of being refused

## Why

The host worker draws slides pictures with MiniMax `image-01` (`slides_image_model`). The
server sends the vendor `<prompt>. Avoid: <negative>` and refuses the whole request when that
is 1500 characters or longer (`apps/api/app/video_media/providers/minimax.py`,
`video_media_upstream_invalid`). The tool composed a shot's request as the scene prompt (lint
allows 1000) + `. Style: <look.style>` (a riso preset is 576 characters) + `. Camera: …`, and a
retake appended `. Corrections: <judge fixes>`, sliced at the server's field limit of 4000 and
never at the vendor's. With a riso look only about 500 characters were left for the scene, so
most shots were refused on every seed, became `needs_review: ["no take could be generated: …"]`,
the writer was asked to fix prompts with no number to aim at and wrote longer ones, and after
`MAX_PROMPT_FIX_ROUNDS=2` the video blocked. On 2026-10-06 two videos were blocked this way
(ai-term-temperature: 23 shots; cloudflare-workers: 7) and 600+ media jobs had failed.

## Definition of done

- [x] A shot whose prompt cannot fit the chosen image model's limit beside the look is not sent
      at all: its manifest entry says how many characters the prompt may have
      (`prompt_budget_chars`) and the problem line says so in words.
- [x] A retake whose corrections would push the request over the limit drops corrections (the
      last first) rather than be refused; the look's style, camera, cast and negative are never cut.
- [x] The writer's fix request carries the budget (`fix.prompt_budget_chars` and each target's),
      and the three writer prompts say a shorter prompt beats a fuller one.
- [x] The server reports the limits (`limits.image_prompt_chars`, `limits.image_prompt_chars_minimax`),
      and the tool falls back to a table, then 4000, on an older server.

## Steps

- [x] `tools/video/media/prompt-budget.mjs`: `imagePromptLimit`, `promptOverhead`,
      `shotPromptBudget` (throws `video_media_prompt_budget` for the owner when the look alone
      leaves under 40 characters), `composeShotPrompt`, `AVOID` equal to minimax.py's string.
- [x] `keyframes.mjs`: `shotPrompt`/`retakePrompt` keep their signatures with a `limit`; `run()`
      computes the limit from the chosen image choice, checks each shot's budget before the take
      loop, records `prompt_budget_chars` on every entry, reports trims; `--dry-run` prints each
      shot's budget and the over-budget shots; the style plate is composed under the limit too.
- [x] `flow.mjs`: `failedTargets` carries `prompt_budget_chars`; `fixPrompts` adds the minimum
      to `fix`.
- [x] `prompts.mjs`: one sentence in the slides, drama and explainer writers.
- [x] `admin_api.py`: the two limit keys; test asserts them.
- [x] Tests: `media.test.mjs` (budget math, drop order, word cut, overflow error, limit
      precedence, AVOID pinned to the server's source), `look-keyframes.test.mjs` (a MiniMax
      slides run: an over-budget shot is never sent, retakes stay under 1500 with the avoidance
      text, corrections dropped in order, the rewritten shot is drawn), `automation.test.mjs`
      (the slides walk hands `prompt_budget_chars: 420` to the writer).

## How to verify

```bash
node --test tools/video/media/media.test.mjs tools/video/media/look-keyframes.test.mjs tools/video/automation/automation.test.mjs tools/video/media/stages.test.mjs tools/video/media/clips.test.mjs
cd apps/api && PYTHONUTF8=1 uv run pytest tests/test_video_media_api.py tests/test_video_media_providers.py && uv run ruff check . && uv run mypy app
```

On the host, after the deploy: `node tools/video/cli.mjs keyframes --slug <blocked slug> --dry-run`
prints `prompt budget: <n> of <budget> characters` per shot and names the over-budget ones; a
run leaves `prompt_budget_chars` in `keyframes/manifest.json` and no `video_media_upstream_invalid`
job in the ledger. Then clear `prompt_fixes.keyframes` in the two blocked videos' `auto.json`
(or unblock them) so the writer gets a round with the number.

## Notes

- The budget for a riso look under MiniMax is 504 characters (camera "push in"): limit 1500 − 1
  − `. Style: ` + 576 − `. Camera: push in` − `. Avoid: ` + 384. The style plate prompt (418)
  fits under every preset; its corrections are dropped when they do not.
- The budget check is after the "kept" check, so a shot that already passed is not redrawn.
  The over-budget entry has no `fixes` field (there is nothing to put into a retake); the
  problem line carries the `→` clause so the writer reads it as the other problems.
- `retakePrompt(prompt, fixes, limit = 4000)` still serves `clips.mjs` and `look.mjs` with a
  composed prompt: under 4000 it now drops a correction that does not fit rather than slice
  through it, and cuts a prompt alone at a word boundary. `look-keyframes.test.mjs` pins both.
- `composeShotPrompt` throws through `shotPromptBudget` only when the scene has to be cut and
  the look alone leaves under 40 characters: a drama under the 4000 field limit never gets there.
- The cache key of a take is the composed prompt (`stage.imageKey`), so the same composer is
  used in `entryStands` and in the take loop; a different limit (another image model) gives
  other keys, as a model change already does through `sameImage`.
- `docs/videos/long-form/review.json` binds `flow.mjs`, `prompts.mjs`, `automation.test.mjs`
  and `look-keyframes.test.mjs`: the duration-review receipt is red after this change on
  purpose and is re-bound by an independent review agent.
- Windows-only red left alone: `media.test.mjs` "stock fetch stores the photo…" expects
  forward slashes in a `docs/videos/...` path and gets backslashes; not touched here.
