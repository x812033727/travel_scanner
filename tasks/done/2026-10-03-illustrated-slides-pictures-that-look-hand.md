---
id: 2026-10-03-illustrated-slides-pictures-that-look-hand
title: Illustrated slides pictures that look hand-made, varied and sharp
status: done
priority: P1
area: tools
owner: claude-fable-5-1-illustration-polish
claimed_at: 2026-10-03T01:41:31Z
created_at: 2026-10-03T01:38:33Z
completed_at: 2026-10-03T02:16:52Z
branch: claude/video-series-illustration-polish-c26975
depends_on: []
scope:
  - tools/video/core/drama.mjs
  - tools/video/core/drama.test.mjs
  - tools/video/core/fixtures/illustrated
  - tools/video/automation/prompts.mjs
  - tools/video/automation/prompts.test.mjs
  - tools/video/assemble/drama.mjs
  - tools/video/assemble/drama.test.mjs
  - tools/video/media/keyframes.mjs
  - tools/video/media/stages.mjs
  - tools/video/media/look-keyframes.test.mjs
  - tools/video/media/stages.test.mjs
  - apps/api/app/video_media/schemas.py
  - apps/api/app/video_media/jobs.py
  - apps/api/app/video_media/catalog.py
  - apps/api/app/video_media/meter.py
  - apps/api/app/video_media/admin_api.py
  - apps/api/app/video_media/providers/gemini_images.py
  - apps/api/tests/test_video_media_jobs.py
  - apps/api/tests/test_video_media_providers.py
  - apps/api/tests/test_video_media_catalog.py
  - apps/api/tests/test_video_media_api.py
  - docs/videos/ILLUSTRATED.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Illustrated slides pictures that look hand-made, varied and sharp

## Why

The owner looked at the illustrated slides pictures (docs/videos/ILLUSTRATED.md) and said they
are rough, monotonous, visually dull and too obviously AI-made; they want them to look drawn by a
person. Measured on the three AI-terms pilot scripts: every one of 97 prompts of
`ai-term-context-window` opens with "flat editorial illustration" and copies the palette, "desk" is
in 51 of them, "lamp" in 24 of `ai-term-token`'s 62, 65 prompts name no shot size, and one run of
three push-ins in a row. The `tech-story` preset asked for "anonymous figures" on a teal ground, every
scene dissolved into the next under the same tiny linear zoom, the judge never scored craft, and
every picture came at 1K and was upscaled 1.25×. The sameness is made by the prompts and rules,
not by the model.

## Definition of done

- [x] The `tech-story` look reads as a printmaker's brief (uneven ink, misregistered flat colour,
      paper grain, off-centre focal point, small simple people with faces or backs) and its negative
      refuses the machine look (glossy, glow, stock vector, faceless mannequin, centred symmetry).
- [x] The slides writer is told a picture recipe (shot size → place and time → one person doing one
      thing → focal object and material → light), no style or colour words, a camera chosen for the
      picture and never the previous shot's, cuts by default, each chapter in its own place, no
      tech-world props.
- [x] Lint refuses three stills in a row under one camera move and warns, once per video, about
      prompts with no shot size, prompts restating the look, and a place or object in more than a
      third of the pictures (illustrated slides only).
- [x] Narrator-only keyframes are judged on `craft` as well.
- [x] Stills ease their camera move (smoothstep), scale the travel to the shot, drift left or right
      by shot id; scene changes cut unless the line before ends on a pause beat (≥ 600 ms), a chapter
      card, or the writer says otherwise.
- [x] Illustrated slides and explainer keyframes are asked at 2K when the server's image choice has
      a 2K price (`usd_per_image_2k` on the status choices; `ImageJobIn.size`; Gemini `imageSize`),
      priced accordingly; a 1K-only model refuses 2K with 422.
- [x] `docs/videos/ILLUSTRATED.md` records the decisions, the cost at 2K and what is left.
- [x] The duration-review receipt (`docs/videos/long-form/review.*`) is rebound by an independent
      reviewer for the bound files this touches (prompts.mjs, drama.mjs, look-keyframes.test.mjs):
      `claude-pr-review-illustration-polish`, commit 68e1efd17.

## Steps

- [x] core/drama.mjs: preset, `cameraMove`, `pictureVarietyProblems` through `shotProblems`.
- [x] automation/prompts.mjs: the shot bullet and the "Pictures travel" paragraph of TEMPLATE_GUIDE.
- [x] core/fixtures/illustrated/video.json: prompts rewritten in the recipe; a 600 ms beat before the
      clock picture shows the dissolve rule.
- [x] assemble/drama.mjs: `zoompanExpr(move, frames, { eased, travel })`, `motionTravel`,
      `driftDirection`, `illustratedTransition(source, index, previous)`, `DISSOLVE_BEAT_MS`,
      MOTION_ENCODER_VERSION v3.
- [x] media/stages.mjs + keyframes.mjs: `IMAGE_SIZES`, `imageSizeFor`, `imagePrice(status, format,
      size)`, `craft` rubric item.
- [x] apps/api video_media: `ImageJobIn.size`, `ChoiceView.usd_per_image_2k`,
      `MediaModel.usd_per_image_2k`, `meter.usd_for(..., size)`, Gemini `imageSize`.
- [x] Tests on both sides; docs.
- [x] Independent duration review of the bound files; commit, PR #1166.

## How to verify

```bash
node --test tools/video/core/drama.test.mjs tools/video/assemble/drama.test.mjs tools/video/media/look-keyframes.test.mjs tools/video/media/stages.test.mjs tools/video/automation/prompts.test.mjs
cd apps/api && uv run pytest tests/test_video_media_jobs.py tests/test_video_media_providers.py tests/test_video_media_catalog.py tests/test_video_media_api.py -q
node tools/video/cli.mjs lint --slug ai-term-context-window   # 3 variety warnings, no error
node tools/video/cli.mjs lint --slug ai-term-retrieval-augmented-generation   # 1 error: three push-ins in a row
```

After deployment, on the first illustrated video: `keyframes --dry-run` prints `pictures at 2K`, the
first picture is about 2048×1152, and `keyframes/manifest.json` carries `craft` scores.

## Notes

- The three AI-terms scripts (another task's scope, in review) now carry warnings and, for RAG, one
  lint error (three push-ins); the worker's lint-fix loop will rewrite that camera word. Their
  prompts still copy the palette and lean on desks; only a prompt rewrite changes the pictures.
- `tools/video/shorts/motion.mjs` keeps the linear expressions (held by
  2026-09-28-sothatswhy-shorts-from-episode); `zoompanExpr` stays backward compatible for it.
- `prompts.mjs` was in that task's scope too (claim from 2026-09-28, stale); claimed with --force,
  touching only the slides TEMPLATE_GUIDE.
- The `flat-explainer` preset and the explainer writer rules are unchanged; the explainer gets the
  `craft` rubric and 2K only. Its fixture prompts start with "flat illustration", which is why the
  variety rules apply to illustrated slides alone.
- Gemini's REST field for the size is `generationConfig.imageConfig.imageSize` ("1K"/"2K"/"4K");
  the first real 2K picture after deployment is the check that the field is accepted.
