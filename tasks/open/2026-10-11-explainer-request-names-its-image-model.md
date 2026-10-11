---
id: 2026-10-11-explainer-request-names-its-image-model
title: Explainer request names its image model: cute presets default to image-01, a model with no key is refused at filing
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-11T04:01:35Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/series.py
  - apps/api/app/video_automation/admin_api.py
  - apps/api/app/video_media/jobs.py
  - apps/api/tests/test_video_drama_request_image_model.py
  - apps/api/tests/test_video_drama_requests.py
  - apps/api/tests/test_video_media_jobs.py
  - apps/web/lib/video-presets.ts
  - apps/web/components/admin-video-settings.tsx
  - apps/web/components/admin-video-series.tsx
  - apps/web/components/admin-video-request-image-model.test.tsx
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/automation/series.test.mjs
  - tools/video/media/look-keyframes.test.mjs
  - tools/video/media/stages.test.mjs
  - tools/video/core/explainer-family.test.mjs
  - docs/videos/DRAMA-FLOW.md
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
---

# Explainer request names its image model: cute presets default to image-01, a model with no key is refused at filing

## Why

Pull request 2 of the three that make up `2026-10-10-explainer-route-takes-a-series-look` (the design is
[`docs/videos/explainer-route/DESIGN.md`](../../docs/videos/explainer-route/DESIGN.md), section 4; the owner's decision 3 is in `DECISIONS.md` beside it).
Today a one-off drama request (`DramaRequestIn`) cannot name an image model: an explainer is
drawn with the drama settings' model (Gemini 3 Pro, US$0.134 a picture at 2K). The two cute
presets that pull request 1 adds have looks written for MiniMax `image-01` (positive text only,
US$0.0035 a picture), so a cute request must be stored with `image-01`, the worker must write
that model into the episode's `series.json` so the media stages ask for 1K pictures and count
MiniMax's 1,500-character prompt limit, and a request whose model's vendor has no key on the
site must be refused at filing, before any paid planning.

**Pull request 1 must have landed and been deployed first** (it adds the presets, the CHECK
constraints, `EXPLAINER_PRESETS` / `isExplainerPreset` on the three sides and
`apps/web/lib/video-presets.ts`, all of which this change builds on). Its ticket is filed by its
implementer on that pull request's branch; when it is on main, add its id to this ticket's
`depends_on`.

## Definition of done

- [ ] API (design 4.1 items 1 to 6): `PRESET_IMAGE_MODELS` in `schemas.py`;
      `DramaRequestIn.image_model` validated by `_known_image_model`, refused on a non-explainer
      preset, defaulted to `image-01` for the two cute presets and left `None` for
      `flat-explainer`; `create_one_off` stores it on the series row and in the audit entry;
      `series_image_vendor` in `video_media/jobs.py`; `create_drama_request` answers 409
      `video_drama_image_model_not_configured` when the named or defaulted model's vendor has no
      key, and looks nothing up when no model is named. No migration (the column exists since 0111).
- [ ] Tools (items 7 to 9): `draftEpisode` writes `image_model` into a one-off's `series.json`
      (never a long series'); `draftBudget` returns `prompt_budget_chars` for an explainer whose
      `series.json` names a model (1000 with today's looks). No change to `media/*`.
- [ ] Web (items 10 to 14): `PRESET_IMAGE_MODEL`, `imageModelOptions`, `requestImageModel`, the
      image-model select in `NewDramaForm` for explainer presets, the model on the one-off card
      and the series header, three strings in each of the five `admin.json`. `REQUEST_PRESETS`
      stays at five values: the cute presets join the form in pull request 3.
- [ ] `docs/videos/DRAMA-FLOW.md` section 二 carries the documentation.
      `.agents/skills/youtube-video/references/drama.md` is **not** edited: it is read into every
      drama payload, and one changed byte stops every unfinished drama stage.
- [ ] The tests of design 4.2, including the corrected `look-keyframes.test.mjs` case and the
      tests that must pass unedited.
- [ ] `flat-explainer` naming no model produces the same row, `series.json`, writer payload and
      cache keys as before (owner's decision 4).
- [ ] The duration receipt (`docs/videos/long-form/review.json`, `review.md`) is re-issued for the 13 bound files of
      design 4.3 by an agent that did not write the change (`DURATION_ONLY` increment), and
      `node tools/video/long-form/cli.mjs check` passes.
- [ ] Deployed as one release (web, API, tools) and the host checks of design 4.6 items 1 to 5 read.

## Steps

- [ ] Confirm pull request 1 is on main and on the host (`/admin/videos` settings list shows the
      two cute labels; the worker prints the three `EXPLAINER_PRESETS`).
- [ ] Read design sections 1, 2 and 4, and `orders/order-pr2.json` beside it for the wording the
      design refers to ("order 2 change 11", "order 2 test 1" and so on). Find every site by its
      quoted statement, not by line number.
- [ ] Before pushing, grep pull request 1's merged tests for an HTTP post of a cute preset: any
      such test must patch `admin_api.load_runtime_settings`.
- [ ] Run `npm run test:tools` whole once, without piping it through `tail`.
- [ ] Hand the receipt to an independent agent; then deploy (design 4.5: confirm the worker's
      checkout before the first request that names a model; never backfill the key into an
      existing video).

## How to verify

`cd apps/api && uv run pytest tests/test_video_drama_request_image_model.py tests/test_video_drama_requests.py tests/test_video_media_jobs.py tests/test_video_series.py`;
`node --test tools/video/automation/series.test.mjs tools/video/media/look-keyframes.test.mjs tools/video/media/stages.test.mjs tools/video/core/explainer-family.test.mjs`;
`npm run check:i18n && npm run typecheck:web && npm run test:web`;
`node tools/video/long-form/cli.mjs check`. On the host, design 4.6: the form shows the
image-model field for `flat-explainer` only, with "same as the drama settings" selected, and
every earlier one-off row has `image_model` NULL.

## Notes

- 2026-10-11 filed from the design. Known and accepted (design 4.7): naming a Gemini model draws
  at 1K, `flat-explainer` with `image-01` sends its negative as text, `POST /series` and
  `PATCH /series/{slug}` bypass the default and the key check, the dry run says
  `(provider key checked on submit)`. Each has its own follow-up ticket filed the same day.
- The pull request text must say the filing refusal covers named and defaulted models only.
