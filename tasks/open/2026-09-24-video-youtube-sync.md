---
id: 2026-09-24-video-youtube-sync
title: 影片產線 T8：網站用 YouTube API 補齊五語系中繼資料、CC、縮圖，並依站主選的時間排程
status: in-progress
priority: P2
area: api
owner: claude-opus-5-5-youtube-link
claimed_at: 2026-09-27T09:35:33Z
created_at: 2026-09-24T00:41:17Z
completed_at:
branch: claude/youtube-account-linking-9c99d3
depends_on:
  - 2026-09-26-video-hands-off-web
scope:
  - apps/api/app/video_youtube
  - apps/api/app/models.py
  - apps/api/app/main.py
  - apps/api/app/video_reviews/schemas.py
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/migrations/versions/0102_video_youtube_sync.py
  - apps/api/tests/test_video_youtube.py
  - apps/api/tests/test_video_youtube_sync.py
  - apps/api/tests/test_migration_0102_video_youtube_sync.py
  - apps/web/app/api/admin-video-youtube
  - apps/web/components/admin-video-youtube.tsx
  - apps/web/components/admin-video-youtube.test.tsx
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
  - .agents/skills/youtube-video/references/publish.md
  - docs/videos/HANDS-OFF.md
  - docs/videos/YOUTUBE-API-AUDIT.md
---

# 影片產線 T8：網站用 YouTube API 補齊五語系中繼資料、CC、縮圖，並依站主選的時間排程

## Why

2026-09-27 改寫（原本的做法是在站主電腦上用桌面 OAuth，見 git 歷史）。工人已經搬到主機，金鑰只能放在 API 容器；站主也決定除了上架時間以外都不想管（`docs/videos/HANDS-OFF.md` §YouTube API 第一步）。

YouTube 只會把「未通過稽核的 API 專案用 `videos.insert` 上傳」的影片鎖成私人。站主在 Studio 上傳的私人影片，可以用 `videos.update` 設定 `status.publishAt`。官方規則是：影片必須是私人、而且從來沒有公開過；更新時 `privacyStatus` 也要送 `private`。

所以流程是：

1. 站主在 Studio 只上傳 mp4（私人）。
2. 在「可以上架」的卡片貼上網址、選上架時間。
3. 網站補齊其餘所有東西並排程，時間到了由 YouTube 自己公開。

一支約 2,100 配額單位，每日預設額度 10,000。

## Definition of done

- [x] 設定分頁新增「連結 YouTube 頻道」：
  - 網站跑 OAuth（網頁應用程式用戶端，callback 在網站上），scope 只有 `youtube.force-ssl`；
  - 站主在瀏覽器按同意，refresh token 存在 API 那一側，和其他廠商金鑰的存法一樣，永遠不回傳給瀏覽器；
  - 可以撤銷。
- [x] 站主在「可以上架」送出網址與時間之後，API 容器依序送出：
  - `videos.update`：先讀現值、合併後整段送出；帶 `snippet.defaultLanguage`、五語系 `localizations`、標籤、分類、`status.containsSyntheticMedia`（依上傳包的揭露答案）、`selfDeclaredMadeForKids: false`、`privacyStatus: private` 與 `publishAt`；
  - `captions.insert`：每個語系一次；
  - `thumbnails.set`。
- [x] 每一步的結果記在審核頁。失敗時可以重試，而且不會重複上傳字幕：先用 `captions.list` 看已經有哪些。
- [x] 送出前的檢查：
  - 上傳包的雜湊，要等於核准的那一份；
  - 影片目前是私人、而且從來沒有公開過；
  - 上架時間在未來。
  
  任何一項不符就拒絕。
- [x] 網站永遠不會直接把影片設成公開：一定要有站主選的時間，公開由 YouTube 在那個時間做。
- [ ] 兩個實測結果寫進 `publish.md`（要站主先連結頻道才測得到，移到票 `2026-09-27-video-youtube-sync-field-test`）：
  - 沒有稽核的專案，能不能對 Studio 上傳的影片呼叫 `captions.insert` 與設定 `publishAt`；
  - 中文字幕的語言碼要用 `zh-TW`／`zh-CN`，還是 `zh-Hant`／`zh-Hans`。做法是上傳一條測試軌，再用 `captions.list` 讀回。

## Steps

- [ ] 站主準備 Google Cloud 專案（站主的事，卡片上有五步；移到票 `2026-09-27-video-youtube-sync-field-test`）：
  - 啟用 YouTube Data API v3；
  - 建立「網頁應用程式」OAuth 用戶端，redirect URI 用網站的 callback；
  - 同意畫面的發布狀態設成「正式版」（留在「測試中」的話，refresh token 7 天就會過期）。沒有驗證的正式版應用程式會顯示警告畫面、最多 100 個使用者，只有站主一個人用不受影響。
  
  用戶端密鑰由站主自己在後台填，不經過代理或對話。
- [x] `app/video_youtube/`：OAuth、請求組裝（純函式加上測試）、送出與重試。
- [x] 設定分頁的連結按鈕；「可以上架」卡片的時間欄位改成送到這裡。
- [ ] 用一支私人影片實測，把結果寫進 `publish.md`（同上）。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_video_youtube.py -q
cd apps/web && npx vitest run components/admin-video-youtube && npm run lint && npm run typecheck
```

## Notes

- 如果要存權杖需要新的資料表，就要加遷移，檔名與號碼開工時再定，scope 跟著改。
- 通過稽核（票 `2026-09-26-video-hands-off-api-audit`）之後，下一步是網站自己用 `videos.insert` 上傳 mp4，這張的程式可以沿用。
- 原本依賴的 `2026-09-24-video-captions-i18n` 已經完成（#745、#788）。

### 做法與決定（2026-09-27，claude-opus-5-5-youtube-link）

- **兩條來源都做了**：「我已經在 Studio 上傳（私人），貼網址」（第一步，不用稽核），以及「由網站上傳 mp4」（`videos.insert` 續傳上傳，第二步）。稽核沒過時上傳要站主勾「我知道會被鎖成私人」，API 端也擋（`video_youtube_private_lock`）；這讓稽核附件 8 截得到真正的上傳畫面。設定卡片有「YouTube API 稽核已通過」，勾了之後不再多問、預設來源改成由網站上傳。
- **用戶端 ID 與密鑰放在設定分頁的卡片**（`video_youtube_connections` 單列表，遷移 0102），不是 `/admin/settings` 的供應商卡：連結按鈕、重新導向 URI 與五步說明在同一張卡，站主一個地方做完。密鑰與 refresh token 用 `app.admin.service.encrypt_secrets` 一起加密，和供應商金鑰同一把鑰匙。
- **OAuth**：`access_type=offline`、`prompt=select_account consent`（品牌帳號的頻道要能選）、PKCE、state＋瀏覽器綁定（HttpOnly cookie，只在 `/api/admin-video-youtube`），流程記錄在 Redis 10 分鐘、用一次就刪。沒勾 YouTube 權限（Google 的細部同意可以取消）或帳號沒有頻道都會拒絕，後者把剛拿到的授權還給 Google。換用戶端 ID 前要先解除連結。
- **執行位置**：審核檔案區只掛在 `api` 容器（`docker-compose.prod.yml`），所以同步是 API 行程裡的 asyncio 工作，不是 rq。用 `youtube_sync.lease_until` 當租約、每分鐘續；API 重啟時租約過期，面板顯示「中斷了」，按重試接著做。續傳工作階段存在 `video_projects.youtube_upload_session`（「sha256 空格 URI」，只對同一支 mp4 有效，永遠不回傳瀏覽器）。
- **標題與說明**：表單預填上傳包的 zh-TW（`payload.zh`），站主可以改（RMF 要求）；沒送就用 metadata.json 的。瀏覽權限：在選定時間公開／不公開／私人。RMF 的原文是「public, private, or unlisted」，這裡的「公開」只以排程的形式存在（本票「網站永遠不直接設成公開」）；稽核審查若要求能直接選公開，要站主決定要不要加。
- **錯誤訊息**：服務丟 `video_youtube.errors.Refused`，`admin_api` 換成 `AppError`（和 `StorageRefused` 同一個做法），所以 `test_error_localization` 把它們當後台代碼。前端 zh-TW 顯示 API 的原句，其他語系用 `admin.videoYoutube.errors.<code>`。
- **失敗的同步算「需要你」**：`needsOwner` 多看 `youtube_sync` 失敗或中斷；清單列會顯示「正在送 YouTube」「YouTube 同步失敗」。
- **沒做的**：`captions.update`／`delete`（稽核草稿列了，但現在的重試只補缺的語系，不替換舊字幕）；配音音軌（Data API 沒有方法，仍在 Studio）。
