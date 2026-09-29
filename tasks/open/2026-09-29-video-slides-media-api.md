---
id: 2026-09-29-video-slides-media-api
title: Slides media on the server: switch, Flash image model, per-video cap, auto-approved storyboard, music and sfx names
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-29T09:14:23Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_automation/models.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/settings.py
  - apps/api/app/video_media/jobs.py
  - apps/api/app/video_media/admin_api.py
  - apps/api/migrations
  - apps/api/tests/test_video_media_jobs.py
  - apps/api/tests/test_video_automation_settings.py
  - apps/web/components/admin-video-settings-drama.tsx
  - apps/web/components/admin-video-settings-drama.test.tsx
  - apps/web/messages
---

# Slides media on the server: switch, Flash image model, per-video cap, auto-approved storyboard, music and sfx names

## Why

生圖與配樂在伺服器只看 `drama_enabled`（`apps/api/app/video_media/jobs.py:268-273`），影像模型只有全站一個或每系列一個。插圖投影片要落在 US$8–15 必須用 gemini-3.1-flash-image，而漫劇繼續用 Pro；站主決定分鏡一開始就自動核准、配樂與音效用授權檔。

## Definition of done

- [ ] 設定列加 `slides_media_enabled`（預設 false）、`slides_image_model`（nullable，預設 gemini-3.1-flash-image，用 `_known_image_model` 驗證）、`slides_max_usd_per_video`（20）、`slides_auto_approve_storyboard`（預設 true）、`music_track`、`sfx_set`；`DEFAULT_VOICE.style` 換成說書式。
- [ ] `submit_job` 查 `VideoProject.format`（`apps/api/app/models.py:2178`）：slides 專案在 `slides_media_enabled` 時放行 image／music，影像模型 `series_image ?? slides_image_model`；漫劇不受影響。
- [ ] `settings.py` `auto_approves_storyboard` 對 slides 專案看 `slides_auto_approve_storyboard`。
- [ ] `media_status` 回 `slides_enabled`、`slides_image`、`slides_max_usd_per_video`。
- [ ] 後台設定分頁「投影片影片的插畫」區塊，五語 i18n。
- [ ] migration 接在當時的 head 後、整合測試（`backend-conventions` skill）。

## Steps

- [ ] models／schemas／settings／migration。
- [ ] jobs.py、admin_api.py。
- [ ] web 元件、messages、測試。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_video_media_jobs.py tests/test_video_automation_settings.py -q
npm run check:i18n && npm run test:web -- admin-video-settings
```

## Notes

過渡期：`drama_enabled` 打開加上把試片登記成一集的系列並設 `image_model`（`jobs.py:151-192`），或全站切 Flash。
