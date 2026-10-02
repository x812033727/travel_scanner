---
id: 2026-10-02-shorts-stage-models-the-api-saves
title: Shorts stage models: the API saves them and the AI settings page gets a Shorts stages block
status: done
priority: P2
area: api
owner: claude-opus-5-5-shorts-stage-models
claimed_at: 2026-10-02T08:29:15Z
created_at: 2026-10-02T06:31:32Z
completed_at: 2026-10-02T08:44:09Z
branch: claude/shorts-stage-models
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

- [x] `GET /admin/video-shorts/settings` 回 `stage_models`（`dict[Stage, StageModel] | None`，`None` 或空就是跟教學一樣），`PUT` 收得到並存進 `video_shorts_settings.stage_models`；送 `null` 就清掉（跟教學一樣），沒送就不動。
- [x] AI 設定頁的影片模型區多一塊「Shorts 各階段」：一個「跟教學一樣」勾選（勾了送 `null`），不勾就是六個階段各自的供應商與模型選單，跟漫劇那塊同一套（`stageFields`）。它自己存到 `PUT /admin/video-shorts/settings`，只送 `stage_models`，不碰其他 Shorts 設定。
- [x] 五個語系的字串；`npm run check:i18n` 過。
- [x] pytest：存、清、沒送不動、沒有供應商金鑰時的錯誤；vitest：勾選與送出的 body。

## Steps

- [x] API：schemas、`settings_values`、`update_settings` 的稽核紀錄（`changed` 會列出 `stage_models`）。
- [x] 網頁：`admin-video-model-settings.tsx` 多一塊，讀 `/admin/video-shorts/settings`。
- [x] 測試與五語字串。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_shorts.py -q
npm run lint:web && npm run check:i18n && npm run typecheck:web
cd apps/web && npx vitest run components/admin-video-model-settings
```

## Notes

- 階段名稱與 `StageModel` 沿用 `app/video_automation/schemas.py` 的 `Stage`、`StageModel`；`stage_choice` 已經會先看 Shorts 自己的選擇，再退回教學的，所以 API 只要讓它存得進去。
- `SettingsSave.merged_over` 會丟掉值是 `None` 的欄位：「送 `null` 就清掉」要另外處理（例如用 `model_fields_set` 判斷有沒有送），不然勾了「跟教學一樣」存不進去。
- 2026-10-02（claude-opus-5-5-shorts-stage-models）：claim 時被兩張舊認領擋住（`2026-09-27-video-drama-room-withdraw-a-one`，PR #870 已合併；`2026-09-28-drama-preloaded-document-approval-order`，codex-ten-drama，PR #978 已合併），兩張都是過期認領，用 `--force` 接手。
- 做法：
  - 不需要 migration：`video_shorts_settings.stage_models` 從 0109 起就在，NOT NULL、預設 `{}`。API 對外是 `dict[Stage, StageModel] | None`；存的時候「跟教學一樣」寫成 `{}`，讀回來空的就回 `None`。
  - `SettingsWrite.stage_models` 跟漫劇一樣要六個階段都選（少一個就 422 `video_shorts_settings_invalid`），空 dict 視同 `None`。`SettingsSave.merged_over` 用 `model_fields_set` 分辨「送了 null」（清掉）和「沒送」（不動）。
  - 檢查照漫劇（`app/video_automation/settings.py` 的 `drama_problems`）：模型不在 `model_options()` 裡一律擋；供應商沒有金鑰（`configured_providers`）只在 Shorts 自動製作開著（`enabled`）時擋，跟 Shorts 旁白聲音的 Gemini 金鑰檢查同一個條件。沒有新增錯誤代碼，沿用 `video_shorts_settings_invalid`，所以不用補四語錯誤訊息。
  - `ToolSettingsView` 繼承 `SettingsWrite`，所以 worker 讀的 `/video/automation/shorts/settings` 也會多一個 `stage_models`；`stage_choice` 讀的是資料列，不受影響。
  - 網頁：AI 設定頁影片模型區多一塊「Shorts 各階段」，沿用 `stageFields`，自己一個儲存鈕，只送 `{ stage_models }` 到 `PUT /admin/video-shorts/settings`；Shorts 設定讀不到時錯誤只顯示在這一塊，不擋教學與漫劇的模型。影片頁 Shorts 分頁的 `SETTINGS_KEYS` 不含 `stage_models`，所以那邊存設定不會蓋掉這裡的選擇。
- 驗證：`tests/test_video_shorts.py` 新增 `test_the_shorts_stage_models_save_clear_and_stay_when_not_sent`（存、沒送不動、缺階段、不存在的模型、開自動製作但沒有 anthropic 金鑰、送 null 清掉存成 `{}`、稽核紀錄的 `changed`）；新增 `apps/web/components/admin-video-model-settings.test.tsx`（勾選、送出的 body、清掉送 null、教學的儲存不帶 Shorts、422 顯示在這一塊）。要 API 與網頁都部署後才生效。
