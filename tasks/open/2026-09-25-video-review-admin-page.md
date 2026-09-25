---
id: 2026-09-25-video-review-admin-page
title: 影片審核：後台 /admin/videos 頁面
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-25T05:12:46Z
completed_at:
branch:
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
  - apps/web/messages
  - apps/api/app/admin/operations_service.py
  - apps/api/tests/test_admin_operations.py
  - apps/web/e2e/admin-operations.spec.ts
---

# 影片審核：後台 /admin/videos 頁面

## Why

站主要在網站後台審核影片（見 `2026-09-25-video-review-api-storage-and-endpoints` 的 Why）。這張做頁面本身。

## Definition of done

- [ ] 後台導覽出現「影片審核」，有待審數字；沒有 `content.read` 的人看不到也進不去。
- [ ] 清單：每支影片的標題、目前在哪一步（checklist）、待審幾項、最後同步時間。
- [ ] 詳細頁：每一項審核依關卡顯示——大綱（企劃書全文、A／B／C 選一個、可寫補充意見）、旁白（播放器、Jev 檢查摘要、被標的句子）、成片（720p 播放器可拖曳、聯絡表、縮圖、五語系標題說明）、上架確認（上傳檢查表）；按鈕「核准」「退回（附原因）」。
- [ ] 預覽用專門的串流路由（帶 Range、Cookie 驗證），不走一般 BFF（它把回應當文字讀、上限 10 MiB）。
- [ ] 工具用的轉發路由 `/api/video/reviews/**`（Bearer 權杖，PUT 上限 4.5 MiB）。
- [ ] 五語系文案、元件測試。

## Steps

- [ ] `NAVIGATION_REGISTRY`（API）＋ web fallback navigation ＋ admin-nav 圖示 ＋ e2e 路徑清單。
- [ ] `apps/web/app/[locale]/admin/videos/page.tsx` ＋ `admin-video-reviews.tsx`。
- [ ] `apps/web/app/api/video/reviews/[...path]/route.ts`、`apps/web/app/api/admin-video-files/[slug]/[sha256]/route.ts`。

## How to verify

`npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web`；部署後以站主帳號打開 /zh-TW/admin/videos。

## Notes

- 依賴 API 那張先合併。
