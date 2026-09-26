---
id: 2026-09-26-video-hands-off-web
title: 影片交給 AI 決定：審核頁顯示 Jev 的理由與品管項目，加上「可以上架」清單
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-26T16:18:44Z
completed_at:
branch:
depends_on:
  - 2026-09-26-video-hands-off-judge
scope:
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - apps/api/app/video_reviews/schemas.py
  - apps/api/app/video_reviews/admin_api.py
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/tests/test_video_reviews_youtube.py
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
---

# 影片交給 AI 決定：審核頁顯示 Jev 的理由與品管項目，加上「可以上架」清單

## Why

站主不再逐關審核之後，`/admin/videos` 的用途變成三件事：看 AI 為什麼這樣決定、處理沒過的項目、拿到可以上架的影片（`docs/videos/HANDS-OFF.md` §上傳包與「可以上架」）。

## Definition of done

- [ ] 大綱審核卡片：Jev 自動選的，顯示「Jev 挑選」標記與理由表，列出每個選項的 pick 機率、符合立場、有示範，以及 advice。
- [ ] 成片審核卡片：列出品管項目，沒過的排在最上面並附細節；自動核准的顯示備註。
- [ ] `/admin/videos` 的排序：
  - 最上面是「需要你」：等站主的審核與卡住的影片；
  - 其次是「可以上架」：「確認上架」已核准、還沒有 `youtube_video_id` 的影片。每支列出標題、長度、章節數、下載連結（mp4、縮圖、字幕、說明欄）、中文標題與說明欄與標籤的複製鈕，以及揭露要怎麼勾。
- [ ] 「已上傳」表單：
  - 貼上 YouTube 網址，接受 youtu.be、`watch?v=` 與 Studio 的網址，解析出 11 字元的 id；上架時間選填；
  - 送到 `POST /admin/videos/{slug}/youtube`（ContentManager），存下 `youtube_video_id` 與 `youtube_publish_at`，寫稽核紀錄；
  - ProjectSummary、ProjectOut 與工具的 GET 都帶出這兩個欄位。
- [ ] 標成已上架滿 7 天後，審核檔案區刪掉這支影片的 mp4。
- [ ] 文案五種語言；加上 vitest 與 API 測試。

## Steps

- [ ] API：schemas、端點、服務、檔案保留規則，加上測試。
- [ ] 審核卡片：pick 表、品管清單。
- [ ] 清單排序與「可以上架」卡片。
- [ ] 表單與網址解析。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_reviews.py tests/test_video_reviews_youtube.py -q
cd apps/web && npx vitest run components/admin-video-reviews && npm run lint && npm run typecheck && cd ../.. && npm run check:i18n
```

## Notes

- 下載用既有的 `apps/web/app/api/admin-video-files/[slug]/[sha256]/route.ts`。
- T8（`2026-09-24-video-youtube-sync`）完成後，同一張卡片的上架時間會改成由網站用 API 排程。
