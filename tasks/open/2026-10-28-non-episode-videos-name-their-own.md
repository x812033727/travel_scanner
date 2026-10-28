---
id: 2026-10-28-non-episode-videos-name-their-own
title: Non-episode videos name their own image model in series.json
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-10-28T02:02:38Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_media/jobs.py
  - apps/api/app/video_media/schemas.py
  - apps/api/tests/test_video_media_jobs.py
  - apps/api/tests/test_video_media_api.py
  - tools/video/media/stages.mjs
  - tools/video/media/stages.test.mjs
  - tools/video/media/client.mjs
  - docs/videos/SERIES.md
---

# Non-episode videos name their own image model in series.json

## Why

站主 2026-10-28：《我的修仙獎勵是不是發錯了？》第 1 集在本機寫分鏡、在站上跑 `look`，image-01 三輪設定圖都被 judge 退（黏土玩偶、小孩比例）。想改用 Gemini 3 Pro Image，但站上只認兩種來源：設定分頁的全站圖片模型（一改其他影片都跟著變）與站上作品列的 `image_model`（只對工人做的集生效，本機寫的集查不到）。站主要「漫劇可以用另外的選擇」：一部漫劇自己選圖片模型，不動其他影片。

## Definition of done

- [x] `ImageJobIn.image_model`（選填，照目錄驗證）；`submit_job` 對站上沒有作品的影片用它（`_project_image_model`，退役或不存在以 422 拒絕）；站上作品的集仍以作品列為準
- [x] `Stage.image` 在 `series.json` 有 `image_model`（imageVersion 1）時送 `image_model`
- [x] 測試：API 三條（自己的模型、站上作品優先、目錄外被 schema 拒）；tools 一條（有／沒有 series 模型的請求內容）
- [x] `docs/videos/SERIES.md` 工具端一條
- [ ] 部署後在 `xiuxian-jiangli-e001` 放 `series.json`（`image_model` 設 `gemini-3-pro-image`）重跑 `look`，確認伺服器回的 provider/model 是 gemini

## How to verify

`cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest tests/test_video_media_jobs.py tests/test_video_media_api.py`；`node --test tools/video/media/*.test.mjs`。

## Notes for the next person

claim 被 `2026-10-25-fixprompts-look-blocked-sheet-prompt`（review 狀態、超過 24 小時）的 scope 擋住，`--force` 在這個 session 被拒，所以票沒有正式 claim 就做了；兩邊改的檔不同。伺服器刻意不讓請求指定「站上作品的集」的模型，這條只開給站上沒有作品的影片，價錢照目錄算，預算仍走原本的每月與每支上限。
