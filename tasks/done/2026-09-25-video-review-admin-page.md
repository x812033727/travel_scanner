---
id: 2026-09-25-video-review-admin-page
title: 影片審核：後台 /admin/videos 頁面
status: done
priority: P2
area: web
owner: claude-opus-5-5
claimed_at: 2026-09-25T05:21:43Z
created_at: 2026-09-25T05:12:46Z
completed_at: 2026-09-25T05:32:35Z
branch: claude/video-review-page
depends_on:
  - 2026-09-25-video-review-api-storage-and-endpoints
scope:
  - apps/web/app/[locale]/admin/videos
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - apps/web/app/api/video/reviews
  - apps/web/app/api/admin-video-files
  - apps/web/lib/admin-operations.ts
  - apps/web/components/admin-nav.tsx
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/api/app/admin/operations_service.py
  - apps/api/tests/test_admin_operations.py
  - apps/web/e2e/admin-operations.spec.ts
---

# 影片審核：後台 /admin/videos 頁面

## Why

站主要在網站後台審核影片（見 `2026-09-25-video-review-api-storage-and-endpoints` 的 Why）。這張做頁面本身。

## Definition of done

- [x] 後台導覽出現「影片審核」，有待審數字（`video_reviews_pending`，也算進總待審）；沒有 `content.read` 的人看不到也進不去。
- [x] 清單：每支影片的標題、進度（checklist 完成幾項）、待審幾項、最後同步時間。
- [x] 詳細頁：每一項審核依關卡顯示——大綱（企劃書全文、A／B／C 選一個、可寫補充意見）、旁白（播放器、Jev 檢查摘要、被標的句子）、成片（720p 播放器可拖曳、聯絡表、縮圖、五語系標題說明）、上架確認（上傳檢查表）；按鈕「核准」「退回（附原因）」；過去的決定收在底下。
- [x] 預覽用專門的串流路由（帶 Range、Cookie 驗證），不走一般 BFF（它把回應當文字讀、上限 10 MiB）。
- [x] 工具用的轉發路由 `/api/video/reviews/**`（Bearer 權杖，只放行三個路徑，檔案分段上限 4 MiB）。
- [x] 五語系文案、元件與路由測試。

## Steps

- [x] `NAVIGATION_REGISTRY`（API）＋ web fallback navigation ＋ admin-nav 圖示（Clapperboard）；待審快取鍵升到 v3。
- [x] `apps/web/app/[locale]/admin/videos/page.tsx` ＋ `admin-video-reviews.tsx`。
- [x] `apps/web/app/api/video/reviews/[...path]/route.ts`、`apps/web/app/api/admin-video-files/[slug]/[sha256]/route.ts`。

## How to verify

`npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web`；部署後以站主帳號打開 /zh-TW/admin/videos。

## Notes

- 依賴 API 那張先合併。
- e2e 的 `admin-operations.spec.ts` 沒加 `/admin/videos`：那份清單逐頁載入並要 mock 各頁的 API，`/admin/news` 也沒在裡面；元件與路由測試涵蓋了這頁。
- 路由裡給工具看的錯誤訊息是英文：`check:i18n` 不准 web 的 .ts 新增中文字（只有 CLI 會讀到）。
- 日期用 `Intl.DateTimeFormat`，不用 next-intl 的 `useFormatter`：測試環境把它 mock 掉了，其他後台元件也都這樣做。
- 企劃書以純文字（保留換行）顯示，不渲染 Markdown：站內沒有共用的安全 Markdown 元件，審核只需要看得到內容。
