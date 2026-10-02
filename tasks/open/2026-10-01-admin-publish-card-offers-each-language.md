---
id: 2026-10-01-admin-publish-card-offers-each-language
title: Admin publish card offers each language thumbnail for download
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-10-01T15:22:58Z
completed_at:
branch:
depends_on:
  - 2026-09-28-video-localized-thumbnails
scope:
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - apps/web/messages
---

# Admin publish card offers each language thumbnail for download

## Why

`2026-09-28-video-localized-thumbnails` 讓上傳包多了 `thumbnails/<locale>.jpg`，`tools/video/package/check.mjs` 的 `packageFiles` 把它們用角色 `thumbnail_<locale>`（例如 `thumbnail_en`、`thumbnail_zh-CN`，`image/jpeg`）附在 publish 審核上送到網站。但 `/admin/videos` 的「可以上架」卡片（`apps/web/components/admin-video-review-card.tsx` 的 `downloads`）只認 `thumbnail`、`captions_*`、`description_*`、`metadata`，其他角色直接略過，所以站主在網站上拿不到語言縮圖，只能到工作區找檔案。

## Definition of done

- [ ] 「可以上架」卡片對每個 `thumbnail_<locale>` 檔案顯示一顆下載鈕（標籤含語言，檔名 `thumbnail.<locale>.jpg` 之類），五種語系的文字都有。
- [ ] 舊的審核（沒有這些角色）顯示不變。

## Steps

- [ ] 在 `downloads` 加 `thumbnail_` 前綴，沿用 `localeOf`。
- [ ] 訊息加進 `apps/web/messages` 五個語系，`npm run check:i18n`。
- [ ] `admin-video-reviews.test.tsx` 補一個有 `thumbnail_en` 的 publish 審核。

## How to verify

`cd apps/web && npx vitest run components/admin-video-reviews.test.tsx`，`npm run typecheck:web`，`npm run lint:web`，`npm run check:i18n`。

## Notes

- 伺服器端不用改：`ReviewFile.role` 的格式 `^[a-z][A-Za-z0-9_-]{0,39}$` 接受 `thumbnail_zh-CN`，`image/jpeg` 也是允許的類型；`video_youtube/sync.py` 只用完全等於 `thumbnail` 的角色，不會誤用語言縮圖。
