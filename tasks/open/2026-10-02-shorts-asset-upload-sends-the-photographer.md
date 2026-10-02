---
id: 2026-10-02-shorts-asset-upload-sends-the-photographer
title: Shorts asset upload sends the photographer and rights note in the body, not the URL
status: in-progress
priority: P2
area: api
owner: claude-opus-5-5-asset-privacy
claimed_at: 2026-10-02T08:33:04Z
created_at: 2026-10-02T08:32:07Z
completed_at:
branch: claude/shorts-asset-metadata-body
depends_on: []
scope:
  - apps/api/app/video_shorts/admin_automation_api.py
  - apps/api/app/video_shorts/assets.py
  - apps/api/tests/test_video_shorts_automation.py
  - apps/web/components/admin-video-shorts-topics.tsx
  - apps/web/components/admin-video-shorts-topics.test.tsx
  - docs/videos/SHORTS.md
---

# Shorts asset upload sends the photographer and rights note in the body, not the URL

## Why

Shorts 分頁的「站主素材」上傳（PR #1097 的 `POST /admin/video-shorts/topics/{slug}/assets`，PR #1118 的網頁）把拍攝者姓名（`author`）、授權說明（`rights_note`）、檔名和拍攝日期放在 query string，而且每一段（4 MiB 一段）都帶一次。網址會寫進 nginx 的 access log、Next.js 同源代理（`/api/travel`）的紀錄和瀏覽器歷史，所以一個人的名字和授權文字就留在各處的紀錄裡，刪資料庫那一列也刪不掉。

## Definition of done

- [ ] 上傳素材的任何一個請求網址都不再帶 `author`、`rights_note`、`filename`、`taken_on`；這四項只在 JSON body 裡送一次。
- [ ] 分段上傳照舊：原始位元組一段最多 4 MiB，網址只帶技術參數（`sha256`、`part`、`parts`、`size`、`need`）；API 不再從 query 收那四項（帶了也不會存）。
- [ ] 錯誤代碼不變（`video_shorts_asset_need_unknown`、`video_shorts_asset_rights_missing`、`video_shorts_asset_type`…）；檔案還沒傳完就送資料時回一個新的後台代碼。
- [ ] API 與網頁在同一個 PR 改，部署後不會有一邊新一邊舊。

## Steps

- [ ] API：分段端點只存檔（最後一段照舊檢查是不是圖片）；新增 `POST /admin/video-shorts/topics/{slug}/assets/finish`，JSON body 帶 `sha256`、`need`、`filename`、`author`、`rights_note`、`taken_on`，檔案齊了才建素材那一列、寫稽核、重新判斷題目狀態。
- [ ] 網頁：`admin-video-shorts-topics.tsx` 傳完各段後送一次 `finish`。
- [ ] 測試：API 測 query 帶的 `author`／`rights_note` 不被收、body 的被存下、整趟來回；vitest 測每一個請求網址都沒有那四項、`finish` 的 body 有。
- [ ] `docs/videos/SHORTS.md` 的端點表補上 `finish`。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_shorts_automation.py tests/test_error_localization.py -q
cd apps/web && npx vitest run components/admin-video-shorts-topics
npm run typecheck:web && npm run lint:web
```

## Notes

- 網頁送出上傳的是 `apps/web/components/admin-video-shorts-topics.tsx`（`NeedBox`），不是 `admin-video-shorts-data.ts`。
- 沒有改 `apps/api/app/video_shorts/schemas.py`（另一個代理在改），新的 request model 放在 `admin_automation_api.py`。
- 認領用了 `--force`：擋住的是 `2026-09-30-a-cut-short-is-not-asked`（claude-opus-5-5）的舊認領，它的 PR #998 已經合併。
