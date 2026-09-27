---
id: 2026-09-24-video-admin-limits
title: 後台可調 Gemini 旁白每月上限與 Jev 每日次數
status: done
priority: P2
area: web
owner: claude-opus-5-5
claimed_at: 2026-09-24T15:10:00Z
created_at: 2026-09-24T15:09:59Z
completed_at: 2026-09-24T15:24:33Z
branch: claude/video-admin-limits
depends_on: []
scope:
  - apps/api/app/admin/service.py
  - apps/api/tests/test_video_admin_limits.py
  - apps/web/components/admin-settings-panel.tsx
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
---

# 後台可調 Gemini 旁白每月上限與 Jev 每日次數

## Why

影片旁白改用 Gemini 聲音（#725）後有自己的每月字數上限
`video_speech_gemini_monthly_character_limit`（預設 300,000），旁白檢查（#732）又讓影片開始
花 Jev 的每日次數 `jev_daily_call_budget`（預設 200，新聞自動化、景點介紹的 Jev 影子評估也在用）。
兩個值都只能從主機的環境變數改，站主問「網頁在哪邊可以設定」時答不出來。

## Definition of done

- [x] 「Azure 語音（影片旁白）」卡片出現「Gemini 旁白每月字數上限」，存了就生效。
- [x] 「AI 供應商與金鑰」卡片出現「Jev 每日呼叫次數」，存了就生效。
- [x] 超出 Settings 範圍的值（Gemini 負數或超過一億、Jev 0 或超過 5,000）被 422 擋下。
- [x] 五個語系都有欄位名稱與說明。

## Steps

- [x] 兩個欄位加進 `PROVIDER_DEFINITIONS` 對應卡片的 `config_fields`，卡片說明補一句。
- [x] `admin-settings-panel.tsx` 的 `fieldMeta` 設成數字欄位；五個 `admin.json` 的 `providerFields`。
- [x] `tests/test_video_admin_limits.py`：欄位歸屬、範圍、後台值蓋過環境、Jev 用的是後台值。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_admin_limits.py tests/test_admin_provider_settings.py
npm run check:i18n && npm run lint:web && npm run typecheck:web
```

部署後在 `/zh-TW/admin/settings` 的兩張卡片看到欄位，改值、儲存、重新整理後值還在。

## Notes

- 範圍檢查不用另寫：`_validate_provider_values` 最後會拿合併後的值跑一次 `Settings.model_validate`，
  超出 `Field(ge=, le=)` 就回 422 `provider_setting_invalid`。
- Jev 的 0 刻意不接受（Settings 是 `ge=1`）：每個呼叫者把用完當成停手的理由，0 等於悄悄關掉 Jev。
- 設定欄位不看卡片開關：Azure 語音卡片停用時，Gemini 的上限照樣生效（測試有涵蓋）。
- fakeredis 沒有 Lua，`consume_jev_call` 的測試用一個自己算數的假 Redis，只證明送出去的上限是後台值。
- `ruff format --check app/admin/service.py` 在 main 上本來就不過（三處舊格式），CI 只跑 `ruff check`，這張沒動。
