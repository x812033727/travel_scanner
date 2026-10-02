---
id: 2026-10-01-admin-publish-card-offers-each-language
title: Admin publish card offers each language thumbnail for download
status: in-progress
priority: P2
area: web
owner: claude-opus-5-5-card-thumbs
claimed_at: 2026-10-02T00:20:30Z
created_at: 2026-10-01T15:22:58Z
completed_at:
branch: claude/publish-card-locale-thumbs
depends_on:
  - 2026-09-28-video-localized-thumbnails
scope:
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
---

# Admin publish card offers each language thumbnail for download

## Why

`2026-09-28-video-localized-thumbnails` 讓上傳包多了 `thumbnails/<locale>.jpg`，`tools/video/package/check.mjs` 的 `packageFiles` 把它們用角色 `thumbnail_<locale>`（例如 `thumbnail_en`、`thumbnail_zh-CN`，`image/jpeg`）附在 publish 審核上送到網站。但 `/admin/videos` 的「可以上架」卡片（`apps/web/components/admin-video-review-card.tsx` 的 `downloads`）只認 `thumbnail`、`captions_*`、`description_*`、`metadata`，其他角色直接略過，所以站主在網站上拿不到語言縮圖，只能到工作區找檔案。

## Definition of done

- [x] 「可以上架」卡片對每個 `thumbnail_<locale>` 檔案顯示一顆下載鈕（標籤含語言，檔名 `thumbnail.<locale>.jpg` 之類），五種語系的文字都有。
- [x] 舊的審核（沒有這些角色）顯示不變。

## Steps

- [x] 在 `downloads` 加 `thumbnail_` 前綴，沿用 `localeOf`。
- [x] 訊息加進 `apps/web/messages` 五個語系，`npm run check:i18n`。
- [x] `admin-video-reviews.test.tsx` 補一個有 `thumbnail_en` 的 publish 審核。

## How to verify

`cd apps/web && npx vitest run components/admin-video-reviews.test.tsx`，`npm run typecheck:web`，`npm run lint:web`，`npm run check:i18n`。

## Notes

- 伺服器端不用改：`ReviewFile.role` 的格式 `^[a-z][A-Za-z0-9_-]{0,39}$` 接受 `thumbnail_zh-CN`，`image/jpeg` 也是允許的類型；`video_youtube/sync.py` 只用完全等於 `thumbnail` 的角色，不會誤用語言縮圖。
- 2026-10-02 claude-opus-5-5-card-thumbs：再確認一次伺服器端不用改。`admin_service.py` 把審核的 `files` 整份交給卡片（`ReviewFile.model_validate`），下載走 `/api/admin-video-files/<slug>/<sha256>`，`file_for_admin` 只比 sha256，不看角色。
- 認領時 scope 原本是整個 `apps/web/messages`，和 `2026-09-06-ask-origin-airport-at-trip-creation`、`2026-09-13-display-card-promises-language` 的 messages 檔重疊；這張票只動 `admin.videoReviews`，所以把 scope 縮成五個 `admin.json`。剩下擋住的 `2026-09-27-video-drama-room-withdraw-a-one`（PR #870）與 `2026-09-28-drama-preloaded-document-approval-order`（codex-ten-drama，PR #978）的 PR 都已合併，是過期認領，用 `--force` 認領。
- 做法：`downloads` 在完全等於 `thumbnail` 之後加 `thumbnail_` 前綴，沿用 `localeOf`（舊拼法 `thumbnail_zh_cn` 也對回 `zh-CN`），標籤是新鍵 `downloadLocaleThumbnail`（「縮圖 {locale}」，五個語系），下載檔名 `thumbnail.<locale>.jpg`。順手在 `UploadPackage` 的註解角色表補上這一行。
- 測試：新增一個直接畫 `UploadPackage` 的測試（`thumbnail`、`thumbnail_en`、`thumbnail_zh_cn`、`captions_en`），斷言檔名、標籤與連結；把元件改回 main 的版本時這個測試紅（只拿到 `thumbnail.jpg`、`en.srt`）。既有的「可以上架」測試沒有語言縮圖，下載清單的完整斷言不變，證明舊審核顯示不變。
