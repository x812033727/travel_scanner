---
id: 2026-09-24-video-youtube-sync
title: 影片產線 T8：網站用 YouTube API 補齊五語系中繼資料、CC、縮圖，並依站主選的時間排程
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-24T00:41:17Z
completed_at:
branch:
depends_on:
  - 2026-09-26-video-hands-off-web
scope:
  - apps/api/app/video_youtube
  - apps/api/tests/test_video_youtube.py
  - apps/web/components/admin-video-youtube.tsx
  - apps/web/components/admin-video-youtube.test.tsx
  - .agents/skills/youtube-video/references/publish.md
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

- [ ] 設定分頁新增「連結 YouTube 頻道」：
  - 網站跑 OAuth（網頁應用程式用戶端，callback 在網站上），scope 只有 `youtube.force-ssl`；
  - 站主在瀏覽器按同意，refresh token 存在 API 那一側，和其他廠商金鑰的存法一樣，永遠不回傳給瀏覽器；
  - 可以撤銷。
- [ ] 站主在「可以上架」送出網址與時間之後，API 容器依序送出：
  - `videos.update`：先讀現值、合併後整段送出；帶 `snippet.defaultLanguage`、五語系 `localizations`、標籤、分類、`status.containsSyntheticMedia`（依上傳包的揭露答案）、`selfDeclaredMadeForKids: false`、`privacyStatus: private` 與 `publishAt`；
  - `captions.insert`：每個語系一次；
  - `thumbnails.set`。
- [ ] 每一步的結果記在審核頁。失敗時可以重試，而且不會重複上傳字幕：先用 `captions.list` 看已經有哪些。
- [ ] 送出前的檢查：
  - 上傳包的雜湊，要等於核准的那一份；
  - 影片目前是私人、而且從來沒有公開過；
  - 上架時間在未來。
  
  任何一項不符就拒絕。
- [ ] 網站永遠不會直接把影片設成公開：一定要有站主選的時間，公開由 YouTube 在那個時間做。
- [ ] 兩個實測結果寫進 `publish.md`：
  - 沒有稽核的專案，能不能對 Studio 上傳的影片呼叫 `captions.insert` 與設定 `publishAt`；
  - 中文字幕的語言碼要用 `zh-TW`／`zh-CN`，還是 `zh-Hant`／`zh-Hans`。做法是上傳一條測試軌，再用 `captions.list` 讀回。

## Steps

- [ ] 站主準備 Google Cloud 專案：
  - 啟用 YouTube Data API v3；
  - 建立「網頁應用程式」OAuth 用戶端，redirect URI 用網站的 callback；
  - 同意畫面的發布狀態設成「正式版」（留在「測試中」的話，refresh token 7 天就會過期）。沒有驗證的正式版應用程式會顯示警告畫面、最多 100 個使用者，只有站主一個人用不受影響。
  
  用戶端密鑰由站主自己在後台填，不經過代理或對話。
- [ ] `app/video_youtube/`：OAuth、請求組裝（純函式加上測試）、送出與重試。
- [ ] 設定分頁的連結按鈕；「可以上架」卡片的時間欄位改成送到這裡。
- [ ] 用一支私人影片實測，把結果寫進 `publish.md`。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_video_youtube.py -q
cd apps/web && npx vitest run components/admin-video-youtube && npm run lint && npm run typecheck
```

## Notes

- 如果要存權杖需要新的資料表，就要加遷移，檔名與號碼開工時再定，scope 跟著改。
- 通過稽核（票 `2026-09-26-video-hands-off-api-audit`）之後，下一步是網站自己用 `videos.insert` 上傳 mp4，這張的程式可以沿用。
- 原本依賴的 `2026-09-24-video-captions-i18n` 已經完成（#745、#788）。
