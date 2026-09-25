---
id: 2026-09-25-video-auto-model-runner-the-server
title: Video auto model runner: the server runs each writing stage with its configured model, under a monthly budget
status: done
priority: P1
area: api
owner: claude-opus-5-5
claimed_at: 2026-09-25T07:57:09Z
created_at: 2026-09-25T07:38:48Z
completed_at: 2026-09-25T08:06:51Z
branch: claude/video-auto-model-runner
depends_on:
  - 2026-09-25-video-auto-settings-models-schedule-video
scope:
  - apps/api/app/video_automation/ai.py
  - apps/api/app/video_automation/topics.py
  - apps/api/app/video_automation/usage.py
  - apps/api/app/video_automation/admin_api.py
  - apps/api/app/video_automation/models.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/settings.py
  - apps/api/migrations/versions/0091_video_ai_runs.py
  - apps/api/tests/test_video_automation_ai.py
  - apps/web/app/api/video/automation
  - apps/web/app/api/video/speech/forward.ts
  - apps/web/components/admin-video-settings.tsx
  - apps/web/components/admin-video-settings.test.tsx
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
---

# Video auto model runner: the server runs each writing stage with its configured model, under a monthly budget

## Why

自動寫稿、查核、翻譯要用網站的 API 金鑰，而且金鑰不能離開 API 容器。設計全文在 `docs/videos/AUTOMATION.md`。站主 2026-09-25 的決定：
- 在正式站主機上跑。
- 設定放在「影片審核」頁。
- 旁白 Jev 全數通過就自動核准，其他關卡等站主。
- 寫稿用 API 金鑰，預設 Sonnet 寫、Opus 查。
- 題目先看站上新聞與文章，不夠再用 Brave 搜尋補。

## Definition of done

- [x] `POST /video/automation/run`（網頁 `/api/video/automation/run`）：
  - 工人送階段名稱、指示與輸入，伺服器用該階段設定的廠商與模型回整份檔案的文字。
  - 工人不能指定模型。
  - 一小時最多 120 次。
- [x] 每次呼叫在 `video_ai_runs` 記下階段、廠商、模型、token、耗時、權杖與影片代號，失敗的也記。
- [x] 兩個上限，超過回 429，並說明是哪一個上限：
  - 每月 token 上限；
  - 每月草稿數，以本月第一次企劃成功的影片代號計算。
- [x] 設定分頁顯示本月用量：token、草稿、呼叫次數與失敗次數。
- [x] `GET /video/automation/topics`（網頁 `/api/video/automation/topics`）：
  - 最近 14 天生活分類的 zh-TW 文章，也就是 AI、科技新聞與教學文章所在的分類。
  - Brave 搜尋，只取過去一週（`freshness=pw`）的結果，每個題材詞查一次，最多 5 次。
  - Brave 查詢算在景點介紹共用的每日額度裡（`consume_search_budget`）。
  - 設定關掉某個來源時，回應會附上說明。

## Steps

- [x] 遷移 0091：`video_ai_runs`。
- [x] 沿用 `app.hotspots.ai_search.research_provider` 的廠商轉接，輸出格式固定是 `{"text": …}`，由工人檢查內容，再把問題回饋給下一次呼叫。
- [x] 網頁 BFF：沿用 `speech/forward.ts`，只轉工具權杖，不轉 cookie。
  - `forwardToSpeech` 加了逾時參數，階段呼叫用 295 秒。
  - 請求上限 4 MiB，查核會附上讀過的網頁內容。

## How to verify

- `uv run pytest tests/test_video_automation_ai.py`：
  - 單元測試涵蓋設定的模型、預設模型、兩種預算、沒有金鑰、四種上游失敗都會記錄並說明、Brave 的一週範圍與額度。
  - 1 個 PostgreSQL 整合測試，驗本月用量與同一支影片的草稿只算一次。
- `npx vitest run app/api/video components/admin-video-settings.test.tsx`。
- 部署後用工人的權杖打一次 `/api/video/automation/run`，`video_ai_runs` 多一列，設定分頁的用量會跟著變。

## Notes

- **用量少算的地方**：廠商轉接內部會在格式不符時修一次，但只回報最後那一次的 token，所以修過的呼叫會少算前一次的輸入。要精確，得改 `app/hotspots/ai_search.py` 的轉接，這張票沒動。
- **生活分類文章的網址**是 `/zh-TW/guides/<slug>`；`/life` 只是列表頁。
- **工人連到 API 的方式**：工人在 compose 網路裡時，直接打 API（`http://api:8000/api/v1/video/...`），不經過 nginx 與網頁；網頁的 BFF 是給站主的電腦用的。這在 `video-auto-worker-image` 處理。
