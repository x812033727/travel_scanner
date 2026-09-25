---
id: 2026-09-25-video-auto-model-runner-the-server
title: Video auto model runner: the server runs each writing stage with its configured model, under a monthly budget
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-25T07:38:48Z
completed_at:
branch:
depends_on:
  - 2026-09-25-video-auto-settings-models-schedule-video
scope:
  - apps/api/app/video_automation/ai.py
  - apps/api/app/video_automation/topics.py
  - apps/api/app/video_automation/usage.py
  - apps/api/app/video_automation/tool_api.py
  - apps/api/migrations/versions/0091_video_ai_runs.py
  - apps/api/tests/test_video_automation_ai.py
  - apps/web/app/api/video/automation
---

# Video auto model runner: the server runs each writing stage with its configured model, under a monthly budget

## Why

自動寫稿、查核、翻譯要用網站的 API 金鑰，而且金鑰不能離開 API 容器。設計全文在 `docs/videos/AUTOMATION.md`。站主 2026-09-25 的決定：在正式站主機上跑；設定放在「影片審核」頁；旁白 Jev 全數通過就自動核准，其他關卡等站主；寫稿用 API 金鑰（預設 Sonnet 寫、Opus 查）；題目先看站上新聞與文章，不夠再用 Brave 搜尋補。

## Definition of done

- [ ] `POST /video/ai/run`：工人給階段名稱、提示與輸入，伺服器用該階段設定的模型回結構化結果；工人不能指定模型。
- [ ] 每次呼叫記下階段、廠商、模型、token 與影片代號；每月 token 上限與每月草稿數上限，超過回 429。
- [ ] `GET /video/automation/topics`：最近 14 天站上已發布的 AI／科技新聞與文章，加上 Brave 搜尋結果（金鑰在伺服器），排除已做過的題目與要避開的題材。
- [ ] 設定分頁顯示本月用量。

## Steps

- [ ] 遷移 0091：`video_ai_runs`。
- [ ] 沿用新聞自動化的廠商轉接（`news_automation/ai.py` 的 `research_provider`）。
- [ ] 網頁 BFF 路由，照 `apps/web/app/api/video/speech` 的做法。

## How to verify

API 測試（假廠商）；部署後用工人權杖打一次 `/video/ai/run`，用量表多一列。
