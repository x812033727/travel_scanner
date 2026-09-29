---
id: 2026-09-29-video-slides-media-api
title: Slides media on the server: switch, Flash image model, per-video cap, auto-approved storyboard, music and sfx names
status: done
priority: P1
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-29T10:09:35Z
created_at: 2026-09-29T09:14:23Z
completed_at: 2026-09-29T10:44:58Z
branch: claude/sharp-brown-dh2x95
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
  - apps/api/app/video_media/schemas.py
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/tests/test_video_media_api.py
  - apps/api/tests/test_migration_0114_video_slides_media.py
  - apps/web/components/admin-video-settings.tsx
  - apps/web/components/admin-video-settings-tutorial.tsx
  - apps/web/components/admin-video-settings.test.tsx
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - docs/videos/ILLUSTRATED.md
---

# Slides media on the server: switch, Flash image model, per-video cap, auto-approved storyboard, music and sfx names

## Why

生圖與配樂在伺服器只看 `drama_enabled`（`apps/api/app/video_media/jobs.py:268-273`），影像模型只有全站一個或每系列一個。插圖投影片要落在 US$8–15 必須用 gemini-3.1-flash-image，而漫劇繼續用 Pro；站主決定分鏡一開始就自動核准、配樂與音效用授權檔。

## Definition of done

- [x] 設定列加 `slides_media_enabled`（預設 false）、`slides_image_model`（nullable，預設 gemini-3.1-flash-image，用 `_known_image_model` 驗證）、`slides_max_usd_per_video`（20）、`slides_auto_approve_storyboard`（預設 true）、`slides_music_track`、`slides_sfx_set`（欄位名都帶 `slides_` 前綴，放在設定的 `slides` 物件裡，像 `drama`）；`DEFAULT_VOICE.style` 換成說書式。
- [x] `submit_job` 查 `VideoProject.format`：slides 專案在 `slides_media_enabled` 時放行 image／music，影像模型 `series_image ?? slides_image_model ?? 漫劇的`；漫劇不受影響；投影片專案不接 clip。
- [x] `settings.py` `auto_approves_storyboard` 多收 `video_format`，slides 專案看 `slides_auto_approve_storyboard`（`admin_service` 傳專案的 format）。
- [x] `media_status` 回 `slides_enabled`、`slides_image`、`slides_max_usd_per_video`（加 `slides_auto_approve_storyboard`、`slides_music_track`、`slides_sfx_set`）。
- [x] 後台教學分頁「投影片影片的插畫」區塊（跟教學設定一起存，`tutorialBody` 帶 `slides`），五語 i18n。
- [x] migration 0114 接在 0113 後、整合測試 `test_migration_0114_video_slides_media.py`（要 PostgreSQL，`RUN_INTEGRATION_TESTS=1`）。

## Steps

- [x] models／schemas／settings／migration。
- [x] jobs.py、admin_api.py。
- [x] web 元件、messages、測試。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_video_media_jobs.py tests/test_video_automation_settings.py -q
npm run check:i18n && npm run test:web -- admin-video-settings
```

## Notes

過渡期：`drama_enabled` 打開加上把試片登記成一集的系列並設 `image_model`（`jobs.py:151-192`），或全站切 Flash。

做完學到的：

- 設定放成巢狀 `slides` 物件（`SettingsSave.merged_over` 逐欄位合併，舊頁面送不出來的欄位不會被清掉），欄位名帶 `slides_` 前綴才能像 `DRAMA_FIELDS` 一樣 `getattr(row, field)`；工人在 `settle()` 讀 `settings.slides.slides_music_track`（worker 票原本讀頂層，這張票一併改）。
- 測試裡的 `VideoAutomationSettings(id=1, **values)` 是還沒 flush 的物件，Python 端 `default=` 不會生效，沒給的欄位是 None：`slides_values()`／`_slides_image_model()` 都用 `getattr(row, …, None)` 退回預設，測試的 `_row()` 也要展開 `DEFAULT_SLIDES`。
- `test_video_media_jobs` 的 `FakeSession.scalar` 對任何查詢都回同一個 job：`project_format()` 只認 `str`，查不到就當「不知道格式」走漫劇開關，所以既有測試不變；投影片的案例用 monkeypatch 換掉 `project_format`。
- 站主的 `voice.style` 是存在資料列上的值，`DEFAULT_VOICE` 換成說書式只影響新安裝；正式站要在後台貼（`register.mjs` 的 `STORY_VOICE_STYLE`）。
- scope 加了 `video_media/schemas.py`（MediaStatus）、`admin_service.py`（傳 format）、`test_video_media_api.py`、新 migration 測試、web 共用型別／教學元件／測試、`flow.mjs`＋`automation.test.mjs`、`ILLUSTRATED.md` 階段表。claim 時 `--force` 蓋過的是過期的 review 票（drama-room、languages、兩張 2026-09 舊票），都超過 24 小時沒動。
