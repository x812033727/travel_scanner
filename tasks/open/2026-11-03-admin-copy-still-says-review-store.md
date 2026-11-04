---
id: 2026-11-03-admin-copy-still-says-review-store
title: Admin copy still says review-store mp4s go seven days after upload
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-11-03T05:47:38Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
---

# Admin copy still says review-store mp4s go seven days after upload

## Why

2026-11-03 起（PR #1997、#2000，docs/videos/BACKUP.md §跟 tidy 的關係）審核區的檔案不再是「上架滿 7 天刪 mp4」：
mp4 要等雲端備份完成；上架、備份完成、語言做好或略過（配音已上傳）三樣齊了，審核區那支的檔案**全部**刪掉。
後台文案 `previewsGone`（「成片 mp4 在上架滿 7 天後從審核區刪除，縮圖、字幕與說明欄留著」）與 `mp4Retired` 還照舊說法，
站主會誤以為縮圖、字幕還在審核區可以下載。

## Definition of done

- [ ] 五語 `admin.json` 的這兩句改成新規則（備份完成後才刪；全部刪除時說明可以從雲端硬碟 `AI/備份/<系列>/<集>/` 取回）。
- [ ] 若畫面需要區分「只刪 mp4」與「全部刪除」，看 `apps/web/components/admin-video-review-card.tsx` 用哪個欄位判斷，另開票改元件。

## Steps

- [ ] 改五語文案，`npm run check:i18n` 過。

## How to verify

`npm run check:i18n && npm run test:web`

## Notes
