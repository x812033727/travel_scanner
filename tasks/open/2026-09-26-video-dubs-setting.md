---
id: 2026-09-26-video-dubs-setting
title: Video dubs: the dub_locales setting, off by default
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-26T17:59:10Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_automation/models.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/settings.py
  - apps/api/migrations
  - apps/api/tests/test_video_automation_settings.py
  - apps/web/components/admin-video-settings.tsx
  - apps/web/components/admin-video-settings.test.tsx
  - apps/web/messages
---

# Video dubs: the dub_locales setting, off by default

## Why

多語言音軌沒有 API：每支影片的四條配音都要站主在 YouTube Studio 手動上傳，和 `HANDS-OFF.md`「站主只決定上架時間」有衝突（`docs/videos/DUBS.md`）。所以要不要做配音、做哪幾個語系，是站主在設定分頁的決定，預設關。工人與 `qa` 只在這個設定不是空的時候才做配音。

## Definition of done

- [ ] `video_automation_settings` 多一欄 `dub_locales`（JSON 陣列，預設空），遷移接在當時 main 最新的 head 之後（開票時是 `0098`；`2026-09-26-video-hands-off-settings` 會動同一張表，先落地的那張排前面，後落地的接在它後面，實作前再查）。
- [ ] 驗證：只能是 `caption_locales` 的子集合、不重複；設定 API 讀寫來回一致；工人讀設定的端點（`client.mjs` 用的那個）帶出 `dub_locales`。
- [ ] 設定分頁在「字幕語系」下方多一組勾選「配音語系」，旁邊一行提示：每支影片要在 Studio「語言」手動上傳這些音軌，說明連到 DUBS.md 的站主步驟；五個語系的 `admin.json` 都有字串，`npm run check:i18n` 過。
- [ ] 兩側測試：預設空、子集合驗證、來回；元件的勾選與提示。

## Steps

- [ ] 遷移、model、schema、settings 讀寫。
- [ ] 設定分頁與訊息檔。
- [ ] 測試與檢查。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_video_automation_settings.py
npm run check:i18n && npm run typecheck:web && npm run test:web -- admin-video-settings
```

## Notes

- 遷移照 skill `backend-conventions`：revision id 不一定等於檔名、json 不是 jsonb、平行 session 會撞號。
- 配音一支約多 20,600 個 Gemini 字元；站主開這個設定時，同時在後台把 `video_speech_gemini_monthly_character_limit`（預設 300,000）調到 600,000 以上，提示文字可以提醒這件事。
