---
id: 2026-10-02-shorts-stage-models-the-api-saves
title: Shorts stage models: the API saves them and the AI settings page gets a Shorts stages block
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-02T06:31:32Z
completed_at:
branch:
depends_on:
  - 2026-09-28-video-shorts-admin-automation
scope:
  - apps/api/app/video_shorts/schemas.py
  - apps/api/app/video_shorts/settings.py
  - apps/api/app/video_shorts/admin_api.py
  - apps/api/tests/test_video_shorts.py
  - apps/web/components/admin-video-model-settings.tsx
  - apps/web/components/admin-video-model-settings.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
---

# Shorts stage models: the API saves them and the AI settings page gets a Shorts stages block

## Why

W2（`2026-09-28-video-shorts-admin-automation`）的完成條件之一是「各階段模型的『跟教學一樣』勾選放在 AI 設定頁（`admin-video-model-settings.tsx`）多一塊『Shorts 各階段』」。做 W2 時發現 API 沒有可以寫的地方：`video_shorts_settings.stage_models` 欄位存在，`app/video_automation/ai.py` 的 `stage_choice` 在 `format == "shorts"` 時也會讀它，但 `SettingsWrite`、`SettingsSave`、`SettingsView`（`apps/api/app/video_shorts/schemas.py`）都沒有這個欄位，`settings_values` 也不讀它。`SettingsSave` 是 `extra="forbid"`，網頁送了只會 422。所以 W2 只做了受測模型（`subject_models`），這一塊留到這張票。

## Definition of done

- [ ] `GET /admin/video-shorts/settings` 回 `stage_models`（`dict[Stage, StageModel] | None`，`None` 或空就是跟教學一樣），`PUT` 收得到並存進 `video_shorts_settings.stage_models`；送 `null` 就清掉（跟教學一樣），沒送就不動。
- [ ] AI 設定頁的影片模型區多一塊「Shorts 各階段」：一個「跟教學一樣」勾選（勾了送 `null`），不勾就是六個階段各自的供應商與模型選單，跟漫劇那塊同一套（`stageFields`）。它自己存到 `PUT /admin/video-shorts/settings`，只送 `stage_models`，不碰其他 Shorts 設定。
- [ ] 五個語系的字串；`npm run check:i18n` 過。
- [ ] pytest：存、清、沒送不動、沒有供應商金鑰時的錯誤；vitest：勾選與送出的 body。

## Steps

- [ ] API：schemas、`settings_values`、`update_settings` 的稽核紀錄（`changed` 會列出 `stage_models`）。
- [ ] 網頁：`admin-video-model-settings.tsx` 多一塊，讀 `/admin/video-shorts/settings`。
- [ ] 測試與五語字串。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_shorts.py -q
npm run lint:web && npm run check:i18n && npm run typecheck:web
cd apps/web && npx vitest run components/admin-video-model-settings
```

## Notes

- 階段名稱與 `StageModel` 沿用 `app/video_automation/schemas.py` 的 `Stage`、`StageModel`；`stage_choice` 已經會先看 Shorts 自己的選擇，再退回教學的，所以 API 只要讓它存得進去。
- `SettingsSave.merged_over` 會丟掉值是 `None` 的欄位：「送 `null` 就清掉」要另外處理（例如用 `model_fields_set` 判斷有沒有送），不然勾了「跟教學一樣」存不進去。
