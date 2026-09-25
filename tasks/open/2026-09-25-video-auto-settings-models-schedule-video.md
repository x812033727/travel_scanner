---
id: 2026-09-25-video-auto-settings-models-schedule-video
title: Video auto settings: models, schedule, video parameters and budgets on the review page
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-25T07:38:37Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_automation/__init__.py
  - apps/api/app/video_automation/settings.py
  - apps/api/app/video_automation/settings_api.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/migrations/versions/0090_video_automation_settings.py
  - apps/api/tests/test_video_automation_settings.py
  - apps/web/components/admin-video-settings.tsx
  - apps/web/components/admin-video-settings.test.tsx
---

# Video auto settings: models, schedule, video parameters and budgets on the review page

## Why

站主要在 /admin/videos 選製作影片的 AI 模型、多久產生一次草稿、成片參數與預算。設計全文在 `docs/videos/AUTOMATION.md`。站主 2026-09-25 的決定：在正式站主機上跑；設定放在「影片審核」頁；旁白 Jev 全數通過就自動核准，其他關卡等站主；寫稿用 API 金鑰（預設 Sonnet 寫、Opus 查）；題目先看站上新聞與文章，不夠再用 Brave 搜尋補。

## Definition of done

- [ ] /admin/videos 有「設定」分頁，存得下 AUTOMATION.md「設定」表的每一欄，存檔寫稽核紀錄。
- [ ] 模型下拉只列有金鑰、且能做結構化輸出的廠商與模型（沿用 `app/ai/catalog.py`）。
- [ ] 工具用影片工具權杖讀得到設定（`GET /video/automation/settings`）。
- [ ] 旁白送審時帶的檢查結果全數通過、設定開著，審核紀錄直接成為「已核准（Jev 全數通過）」。

## Steps

- [ ] 遷移 0090：一列的 `video_automation_settings`（照 `news_automation_settings` 的做法）。
- [ ] API：admin GET／PUT、工具 GET、驗證。
- [ ] 網頁：設定分頁與五語系文字。
- [ ] 旁白自動核准的規則放在 `video_reviews` 的送審流程。

## How to verify

API 與網頁測試；部署後在 /admin/videos 改一個設定，工具讀回同一個值。

## Notes

- 預算只存上限與開關；用量計數在 `video-auto-model-runner`。
