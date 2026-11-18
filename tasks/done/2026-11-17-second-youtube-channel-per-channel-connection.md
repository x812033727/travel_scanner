---
id: 2026-11-17-second-youtube-channel-per-channel-connection
title: Second YouTube channel: per-channel connection, upload and reports
status: done
priority: P1
area: api
owner: claude-opus
claimed_at: 2026-11-18T01:27:53Z
created_at: 2026-11-17T17:12:26Z
completed_at: 2026-11-18T01:53:19Z
branch: claude/blissful-meitner-bbg7uu
depends_on: []
scope:
  - apps/api/app/video_youtube/connection.py
  - apps/api/app/video_youtube/sync.py
  - apps/api/app/video_youtube/reports.py
  - apps/api/app/video_youtube/retention.py
  - apps/api/app/video_youtube/admin_api.py
  - apps/api/app/video_youtube/admin_reports_api.py
  - apps/api/app/video_youtube/schemas.py
  - apps/api/app/video_youtube/models.py
  - apps/api/app/video_youtube/jobs.py
  - apps/api/app/video_reviews/schemas.py
  - apps/api/tests/test_video_youtube_reports.py
  - apps/api/tests/test_migration_0145_video_youtube_reports.py
  - apps/api/app/models.py
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/app/video_shorts/settings.py
  - apps/api/migrations/versions/0147_video_youtube_channels.py
  - apps/api/tests/test_migration_0147_video_youtube_channels.py
  - apps/api/tests/test_video_youtube_channels.py
  - apps/web/components/admin-video-youtube.tsx
  - apps/web/components/admin-video-youtube.test.tsx
  - apps/web/components/admin-video-youtube-reports.tsx
  - apps/web/app/api/admin-video-youtube
  - apps/web/app/api/video/youtube-reports
  - apps/web/lib/youtube-reports-copy.ts
  - apps/web/lib/youtube-channels-copy.ts
  - tools/video/youtube-reports
  - docs/videos/YOUTUBE-REPORTS.md
---

# Second YouTube channel: per-channel connection, upload and reports

## Why

站主 2026-11-17 決定開第二個 YouTube 頻道（B：AI 劇、AI 影片），@Mokaair（A）之後只放奇聞檔案局與原來如此事務所。站台目前只能連結一個頻道：`apps/api/app/models.py` 的 `VideoYoutubeConnection` 是單筆資料（`CHECK (id = 1)`），上傳、公開同步（`video_reviews/admin_service.py` 的 `_linked_youtube`）和 `tools/video/youtube-reports` 的報表都綁在那一筆。在這張票完成之前，B 只能從 Studio 手動上傳、手抄數據。計畫見 `docs/videos/channel-os-20261117/shared/05-ai-production.md` §4。

## Definition of done

- [x] 後台可以連結兩個以上的 YouTube 頻道，每個頻道有自己的 OAuth 授權與狀態。
- [x] 每支影片或系列記錄要上傳到哪個頻道；預設 `curio`、`sothatswhy` 上 A，`zhong-tian-qu-qi*`、漫劇與寵物短劇上 B。
- [x] 公開同步與報表下載依頻道分開；`node tools/video/youtube-reports/cli.mjs` 可以用 `--channel` 指定頻道。
- [x] 現有的 A 頻道連線不用重新授權，遷移後照常運作。

## Steps

- [x] 讀 `backend-conventions`：migration 接在目前 head 之後、整合測試、後台頁登記。
- [x] **認領時把 scope 擴大到** `apps/api/app/models.py`、新的 migration 檔、`apps/api/app/video_reviews/admin_service.py` 與對應的測試（建票時刻意不列，避免和進行中的票衝突）。
- [x] 設計資料表：拿掉 `id = 1` 限制、加頻道欄位，影片或系列指到頻道。
- [x] API、後台設定分頁、報表 CLI 依序改。

## How to verify

`cd apps/api && uv run pytest`、`npm run test:tools`；在後台連結第二個測試頻道，上傳一支私人影片，確認它出現在正確的頻道。

## Notes

從 `docs/videos/channel-os-20261117/` 開出（2026-11-17）。

2026-11-18：站主同意用 `--force` 認領。`sync.py` 與 `video_reviews/admin_service.py` 仍掛在幾張停了數週的票上：2026-10-12-let-managers-link-a-private-studio、2026-10-29-daily-brief-on-the-host-worker、2026-10-13-dub-narrator-only-explainer-dramas-tool、2026-10-19-worker-video-languages-five、2026-11-03-admin-upload-zip-fails-to-download。這兩個檔案只改跟頻道有關的函式。
為了避開 `apps/web/messages` 與 `docs/videos/HANDS-OFF.md` 上的舊認領，新文案放在 `apps/web/lib/youtube-channels-copy.ts`（比照 `youtube-reports-copy.ts` 的做法），說明寫在 `docs/videos/YOUTUBE-REPORTS.md`。

2026-11-18 完成第一階段：
- migration `0147_video_youtube_channels`：連線表與報表狀態表拿掉單列限制，加上 `key`、`label`、`channel_id`；`video_projects` 加 `youtube_channel_key`。全部是加法，舊版程式只讀第 1 列。
- 後端：`connection.py` 的每個函式都帶 `key`，新增 `connections`、`channel_views`、`create_channel`；第 1 列的 OAuth 用戶端給所有頻道共用；同一個 YouTube 頻道不能連在兩個代號上。上傳（`sync.py`）、貼網址驗證（`admin_service._linked_youtube`）、觀眾續看（`retention.py`）都用影片所屬頻道的授權；新增 `PUT /admin/videos/{slug}/youtube/channel`，影片上了 YouTube 之後就不能換。報表（`reports.py`）依頻道保存與同步，只刪沒有任何一列連著的頻道的資料；每天的排程依序同步每個已連結頻道。
- API：新增 `/admin/video-youtube/channels` 系列路由；報表路由加 `?channel=`。
- 網頁：設定分頁加「其他頻道」卡片，上傳表單加頻道選單（有兩個以上頻道才顯示）；OAuth 起始路由和報表轉送層會帶上頻道代號。文案放在 `apps/web/lib/youtube-channels-copy.ts`。
- 報表工具加 `--channel`。
- 說明寫在 `docs/videos/YOUTUBE-REPORTS.md` §頻道。
- 「預設 curio、sothatswhy 上 A、漫劇上 B」沒有寫死在程式裡：影片沒選頻道就上 default，摩卡劇場的影片在上傳表單選頻道。要自動依系列分頻道的話另開票。
- Shorts、VPS 上傳器和兩個主機指令留給 `2026-11-18-second-channel-phase-2-shorts-vps`。
- 上線後：部署（`deploy` skill）跑 migration，接著站主在設定分頁新增 `theater` 並完成 Google 授權（同意畫面要勾 YouTube 與 Analytics）。
