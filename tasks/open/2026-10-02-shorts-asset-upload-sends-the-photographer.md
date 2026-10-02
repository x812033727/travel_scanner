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

- [x] 上傳素材的任何一個請求網址都不再帶 `author`、`rights_note`、`filename`、`taken_on`；這四項只在 JSON body 裡送一次。
- [x] 分段上傳照舊：原始位元組一段最多 4 MiB，網址只帶技術參數（`sha256`、`part`、`parts`、`size`、`need`）；API 不再從 query 收那四項（帶了也不會存）。
- [x] 錯誤代碼不變（`video_shorts_asset_need_unknown`、`video_shorts_asset_rights_missing`、`video_shorts_asset_type`…）；檔案還沒傳完就送資料時回一個新的後台代碼。
- [x] API 與網頁在同一個 PR 改，部署後不會有一邊新一邊舊。

## Steps

- [x] API：分段端點只存檔（最後一段照舊檢查是不是圖片）；新增 `POST /admin/video-shorts/topics/{slug}/assets/finish`，JSON body 帶 `sha256`、`need`、`filename`、`author`、`rights_note`、`taken_on`，檔案齊了才建素材那一列、寫稽核、重新判斷題目狀態。
- [x] 網頁：`admin-video-shorts-topics.tsx` 傳完各段後送一次 `finish`。
- [x] 測試：API 測 query 帶的 `author`／`rights_note` 不被收、body 的被存下、整趟來回；vitest 測每一個請求網址都沒有那四項、`finish` 的 body 有。
- [x] `docs/videos/SHORTS.md` 的端點表補上 `finish`。

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
- 做法：分段端點（`assets.upload_part`）只收位元組和技術參數，最後一段照舊檢查是不是圖片、不是就刪掉；新的 `assets.add_asset`（`POST …/assets/finish`，body 是 `AssetInfoIn`，`extra="forbid"`）在檔案齊了之後才建素材那一列、寫稽核、`resettle`。同一個檔案再送一次 `finish` 回原本那一列，不會多一列。回應沿用 `AssetPartOut`，網頁型別不用改。
- 分段網址如果還帶 `filename`／`author`／`rights_note`／`taken_on` 任何一項，回 422 `video_shorts_asset_info_in_url`（只列欄位名，不回值）：部署後還開著舊頁面的人會看到錯誤重新整理，而不是傳完檔案卻沒有素材。檔案還沒傳完就送 `finish` 回 409 `video_shorts_asset_not_uploaded`。這兩個新代碼都在 `admin` 檔案或用 `ShortsRefused` 丟，屬後台面，`tests/test_error_localization.py` 不要求四語翻譯（照樣通過）。
- `finish` 遇到不是圖片的檔案回 415 但不刪：分段上傳沒檢查過的檔案可能是同一個 slug 下工人的媒體。
- 只傳了位元組、沒送 `finish` 的檔案不是素材，媒體清理（`app.video_media.jobs.prune`）過了保留天數會刪掉。
- 沒有新增網頁字串（`apps/web/messages/*/admin.json` 沒動）；錯誤照舊顯示 API 的 detail。
- 搜尋過整個 repo：送 `author`／`rights_note` 進網址的只有這一個網頁元件；`tools/` 的工人不上傳素材。
- 驗過：`uv run ruff check .`、`uv run mypy app`、`uv run mypy tests`、`uv run pytest tests/test_video_shorts_automation.py tests/test_error_localization.py -q`（31 passed）；`npx vitest run components/admin-video-shorts-topics`（10 passed）、`npm run typecheck:web`、`npm run lint:web`。
