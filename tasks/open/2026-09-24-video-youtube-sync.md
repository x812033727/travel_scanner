---
id: 2026-09-24-video-youtube-sync
title: 影片產線 T8：網站用 YouTube API 補齊勾了的語系的中繼資料、CC、縮圖，並在語言做好後依站主選的時間排程
status: review
priority: P2
area: api
owner: claude-fable-5-1-video-languages
claimed_at: 2026-09-27T09:14:37Z
created_at: 2026-09-24T00:41:17Z
completed_at:
branch:
depends_on:
  - 2026-09-26-video-hands-off-web
  - 2026-09-27-video-languages-web
scope:
  - apps/api/app/video_youtube
  - apps/api/tests/test_video_youtube.py
  - apps/api/tests/test_migration_0104_video_youtube.py
  - apps/api/tests/test_video_speech.py
  - apps/api/migrations/versions/0104_video_youtube.py
  - apps/api/app/models.py
  - apps/api/app/config.py
  - apps/api/app/i18n.py
  - apps/api/app/main.py
  - apps/api/app/worker.py
  - apps/api/app/admin/service.py
  - apps/api/app/video_reviews/admin_api.py
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/app/video_reviews/schemas.py
  - apps/web/components/admin-video-youtube.tsx
  - apps/web/components/admin-video-youtube.test.tsx
  - apps/web/components/admin-video-settings.tsx
  - apps/web/components/admin-video-settings.test.tsx
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-settings-panel.tsx
  - apps/web/messages
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
- [x] **2026-09-27 加（`docs/videos/LANGUAGES.md`）**：`localizations` 與 `captions.insert` 只送這支影片勾了的語系（`ProjectOut.locales`），zh-TW 一定送；`publishAt` 只在 `ready_to_upload` 為真（語言已決定、勾了的部件都做好或跳過）時送出，之前卡片寫「排程會在語言做好後送出」，做好的那一輪由網站送；上架後再勾的語系走同一支程式補送 `localizations` 與字幕（先 `captions.list`）。配音照舊只能站主在 Studio 上傳。
- [ ] 兩個實測結果寫進 `publish.md`：
  - 沒有稽核的專案，能不能對 Studio 上傳的影片呼叫 `captions.insert` 與設定 `publishAt`；
  - 中文字幕的語言碼要用 `zh-TW`／`zh-CN`，還是 `zh-Hant`／`zh-Hans`。做法是上傳一條測試軌，再用 `captions.list` 讀回。

## Steps

- [ ] 站主準備 Google Cloud 專案：
  - 啟用 YouTube Data API v3；
  - 建立「網頁應用程式」OAuth 用戶端，redirect URI 用網站的 callback；
  - 同意畫面的發布狀態設成「正式版」（留在「測試中」的話，refresh token 7 天就會過期）。沒有驗證的正式版應用程式會顯示警告畫面、最多 100 個使用者，只有站主一個人用不受影響。
  
  用戶端密鑰由站主自己在後台填，不經過代理或對話。
- [x] `app/video_youtube/`：OAuth、請求組裝（純函式加上測試）、送出與重試。
- [x] 設定分頁的連結按鈕；「可以上架」卡片的時間欄位改成送到這裡。
- [ ] 用一支私人影片實測，把結果寫進 `publish.md`。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_video_youtube.py -q
cd apps/web && npx vitest run components/admin-video-youtube && npm run lint && npm run typecheck
```

## Notes

- 2026-09-27 做完程式的部分（claude-fable-5-1-video-languages）。還沒打勾的兩條要站主：Google Cloud 專案與用戶端（用戶端 ID 與密鑰填在 `/admin/ai-accounts` 的「Azure 語音（影片旁白）」卡，redirect URI 照設定分頁「YouTube 頻道」卡上寫的），以及第一支影片的實測，結果回寫 `publish.md` §網站送到 YouTube 的東西的「待實測」。
- 做法：
  - 用戶端 ID／密鑰放在既有的 `azure_speech` 供應商卡（`youtube_oauth_client_id`、`youtube_oauth_client_secret`），和其他廠商金鑰一樣加密、`load_runtime_settings` 讀出。
  - refresh token 放新表 `video_youtube_channel`（遷移 `0104_video_youtube`，同一張遷移在 `video_projects` 加 `youtube_sync` JSON 欄記最後一次送出的結果）。用 `encrypt_secrets` 加密，任何路由都不回傳。
  - OAuth 在網站上跑：`POST /admin/video-youtube/connection/start` 產同意畫面網址（PKCE S256、`access_type=offline`、`prompt=consent`，state 與 verifier 放 Redis 十分鐘），Google 送回 `{站點}/api/travel/admin/video-youtube/connection/callback`（BFF 會把 302 轉給瀏覽器，帶站上的 cookie），callback 換 token、讀 `channels.list mine`、存 row、302 回設定分頁並帶 `youtube=connected` 或 Google 的錯誤碼。`DELETE` 撤銷。連結與撤銷只有 `roles.manage`。
  - 送出是 RQ 工作（佇列 `video-youtube`，`worker.py` 已加），三個入口：貼網址（`link_youtube`）、工人送到 `languages` 批次而影片已有 id（`enqueue_after_languages`）、影片頁「重送到 YouTube」（`POST /admin/video-youtube/{slug}/sync`，202）。`sync_project` 純邏輯在 `sync.py`（`update_body`、`caption_locales`、`schedule_problem`、`missing_captions`）。
  - 「語言還沒都做好」時 `publishAt` 不送但整批其他東西照送，排程那一步記為 ok；影片不是私人或時間已過才算失敗。
  - `CAPTION_LANGUAGE_CODES` 先留空（語系碼照站上的 zh-TW／zh-CN 送），實測 `captions.list` 讀回來對不上再填。
- 新增的錯誤碼 `video_youtube_*` 五個在 `app/i18n.py` 補了四語句子（`test_error_localization` 的掃描把 `video_youtube/oauth.py` 算成公開路徑）。
- 設計文件 `docs/videos/LANGUAGES.md` 還有幾處「T8 沒好之前站主手填」的字句，是設計時的說法；skill 的 `publish.md` 已改成現況。

- 如果要存權杖需要新的資料表，就要加遷移，檔名與號碼開工時再定，scope 跟著改。
- 通過稽核（票 `2026-09-26-video-hands-off-api-audit`）之後，下一步是網站自己用 `videos.insert` 上傳 mp4，這張的程式可以沿用。
- 原本依賴的 `2026-09-24-video-captions-i18n` 已經完成（#745、#788）。
- 2026-09-27：語言改成每支影片選（`docs/videos/LANGUAGES.md`），這張的 DoD 多一條；五語系不再是固定的，標題也照著改成「勾了的語系」。
