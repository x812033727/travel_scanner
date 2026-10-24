---
id: 2026-10-11-explainer-named-gemini-model-draws-at
title: An explainer that names a Gemini image model is drawn at 1K while 'same as the settings' draws at 2K
status: done
priority: P3
area: api
owner: codex-open-tasks-price
claimed_at: 2026-10-24T13:53:17Z
created_at: 2026-10-11T04:03:23Z
completed_at: 2026-10-24T14:46:13Z
branch: codex/open-tasks-reconcile-20261024
depends_on:
  - 2026-10-11-explainer-request-names-its-image-model
scope:
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/settings.py
  - apps/api/tests/test_video_automation_settings.py
  - tools/video/media/stages.mjs
  - tools/video/media/stages.test.mjs
  - tools/video/media/look-keyframes.test.mjs
---

# An explainer that names a Gemini image model is drawn at 1K while 'same as the settings' draws at 2K

## Why

After `2026-10-11-explainer-request-names-its-image-model` an explainer request may name its image model. `imageStatus` in
`tools/video/media/stages.mjs` nulls the 2K price for any overridden model, because the
catalogue rows the worker receives (`MediaOptionView`) carry no `usd_per_image_2k`; with no 2K
price the picture is asked for at 1K. So choosing "Gemini 3 Pro Image" by name gives a softer
picture under a camera move than leaving the field on "same as the drama settings", at the same
US$0.134, and a cute video on Gemini is always 1K because the cute presets have no "same as the
settings" entry ([`docs/videos/explainer-route/DESIGN.md`](../../docs/videos/explainer-route/DESIGN.md) section 4.7 and section 7 item 6; `orders/order-pr2.json` risks).

## Definition of done

- [x] `MediaOptionView` carries `usd_per_image_2k` where the catalogue has one (`schemas.py`,
      `settings.py`), and `imageStatus` keeps the named model's own 2K price.
- [x] An explainer naming a Gemini model is drawn at the same size as one following the
      settings; `image-01` (no 2K price) is still drawn at 1K with no `size` in the request.
- [x] Image cache keys of videos that name no model do not move. Tests on both sides; the
      receipt re-issued (`schemas.py` and `settings.py` are bound).

## Steps

- [x] Check what a changed size does to `keyframeKey` for an explainer already drawn at 1K
      under a named Gemini model (it should redraw only if the owner asks).

## How to verify

`node --test tools/video/media/stages.test.mjs tools/video/media/look-keyframes.test.mjs`;
`cd apps/api && uv run pytest tests/test_video_automation_settings.py`; `keyframes --dry-run`
on such a video prints `pictures at 2K`.

## Notes

- 2026-10-11 filed from the design's section 7, item 6.


### 2026-10-24 narrow owner-requested execution

Parent coordinated only the exact listed source/test paths after fresh branch/worktree/open-PR checks found no active exact-file implementation. Historical broader stale scope is not taken over; its remaining producer/media/acceptance work stays untouched. The preceding related fixes on this parent branch are retained. Scope is narrowed before product editing. No provider calls, paid regeneration, production settings change or deployment is part of this code task.

Parent explicitly adds the existing look-keyframes regression suite to verify paid1K cache reuse with zero new vendor POSTs; fresh named Gemini requests must use2K. Independent duration receipts remain delegated under the reconciliation task. Existing catalog price values are unchanged.


### 2026-10-24 coordinator acceptance

Existing catalogue2K price forwarded by MediaOptionView/settings and used by named Gemini model. No price values changed. Default model keys/MiniMax no-size/legacy omission preserved. Regression proves existing paid1K manifest/cache reused with zero POSTs until explicit --force; fresh named Gemini2K uses own price. Independent review refreshed exactly4 duration-bound files,104 others unchanged, prior report byte-prefix retained. Actual checks all exit0: media74/74;API settings50passed/3existing PostgreSQL integration skips;Ruff;mypy3files;duration27/27;473plans. Post-check frozen6 hashes reverified. Independent reviewer codex-independent-gemini2k-review-20261024. ReportSHA5b93c175cc2cc138e3b1247e74d0e4dded56d711d2861fbc01073795a17298b0;receiptSHA75b4de9f53680e3c6a2f937dbc136e281502b951a94516c5656c7984fbd88e2b.

Implementation is local on `codex/open-tasks-reconcile-20261024`; merge/deployment and any paid media actions remain separate. No vendor POST, media deletion, upload or approval was performed by this fix.
