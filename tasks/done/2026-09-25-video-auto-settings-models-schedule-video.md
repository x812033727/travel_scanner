---
id: 2026-09-25-video-auto-settings-models-schedule-video
title: Video auto settings: models, schedule, video parameters and budgets on the review page
status: done
priority: P1
area: api
owner: claude-opus-5-5
claimed_at: 2026-09-25T07:40:16Z
created_at: 2026-09-25T07:38:37Z
completed_at: 2026-09-25T07:54:25Z
branch: claude/video-auto-settings
depends_on: []
scope:
  - apps/api/app/video_automation/__init__.py
  - apps/api/app/video_automation/models.py
  - apps/api/app/video_automation/settings.py
  - apps/api/app/video_automation/admin_api.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/app/main.py
  - apps/api/migrations/versions/0090_video_automation_settings.py
  - apps/api/tests/test_video_automation_settings.py
  - apps/web/components/admin-video-settings.tsx
  - apps/web/components/admin-video-settings.test.tsx
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/app/api/video/automation/settings
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
---

# Video auto settings: models, schedule, video parameters and budgets on the review page

## Why

站主要在 /admin/videos 選製作影片的 AI 模型、多久產生一次草稿、成片參數與預算。設計全文在 `docs/videos/AUTOMATION.md`。站主 2026-09-25 的決定：
- 在正式站主機上跑；設定放在「影片審核」頁。
- 旁白 Jev 全數通過就自動核准，其他關卡等站主。
- 寫稿用 API 金鑰，預設 Sonnet 寫、Opus 查。
- 題目先看站上新聞與文章，不夠再用 Brave 搜尋補。

## Definition of done

- [x] /admin/videos 有「影片／設定」兩個分頁（`?tab=settings`）。設定分頁存得下 AUTOMATION.md「設定」表的每一欄，存檔時寫稽核紀錄 `video_automation_settings_updated`，紀錄裡列出改了哪些欄位。
- [x] 模型下拉列出每個廠商能做結構化輸出、而且還沒下線的 catalog 模型，沒有金鑰的廠商標「沒有金鑰」。存檔時伺服器再驗一次模型與聲音，驗不過就回 422，並說明是哪一項。
- [x] 工具用影片工具權杖讀得到設定：`GET /video/automation/settings`，經網頁的 `/api/video/automation/settings`。
- [x] 旁白送審時，如果每一句都檢查過、沒有被標、設定也開著，審核紀錄送到就是「已核准」。這時寫稽核紀錄 `video_review_auto_approved`，備註寫明是 Jev 判斷後依設定自動核准。

## Steps

- [x] 遷移 0090：只有一列的 `video_automation_settings`，第一次讀取時照預設值建立。
- [x] API：
  - 讀取要 `content.read`；修改要 `settings.manage`，因為設定決定付費模型與預算。
  - 路徑用 `/admin/video-automation/settings`。不用 `/admin/videos/settings`，因為審核頁已經有 `/admin/videos/{slug}`，兩條路徑會撞。
- [x] 網頁：設定分頁與五語系文字。
- [x] 旁白自動核准的規則放在 `video_reviews` 的送審流程裡。

## How to verify

- `uv run pytest tests/test_video_automation_settings.py`：
  - 14 個單元測試，涵蓋預設值、10 種存不進去的值、伺服器跑不了的模型與聲音、權限。
  - 2 個 PostgreSQL 整合測試（CI 會跑），涵蓋存檔寫稽核紀錄、旁白自動核准，以及關掉設定後改等站主。
- `npx vitest run components/admin-video-settings.test.tsx components/admin-video-reviews.test.tsx app/api/video`：20 個測試通過。
- 部署後在 /admin/videos 的設定分頁改一個值，工具讀回同一個值。

## Notes

- 預算只存上限與開關，用量計數在 `video-auto-model-runner`。
- 審核頁已知的缺口：自動核准的旁白在頁面上顯示為一般的「已核准」加上備註，沒有另外的標籤。
