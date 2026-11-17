---
id: 2026-11-17-second-youtube-channel-per-channel-connection
title: Second YouTube channel: per-channel connection, upload and reports
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-11-17T17:12:26Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_youtube
  - tools/video/youtube-reports
---

# Second YouTube channel: per-channel connection, upload and reports

## Why

站主 2026-11-17 決定開第二個 YouTube 頻道（B：AI 劇、AI 影片），@Mokaair（A）之後只放奇聞檔案局與原來如此事務所。站台目前只能連結一個頻道：`apps/api/app/models.py` 的 `VideoYoutubeConnection` 是單筆資料（`CHECK (id = 1)`），上傳、公開同步（`video_reviews/admin_service.py` 的 `_linked_youtube`）和 `tools/video/youtube-reports` 的報表都綁在那一筆。在這張票完成之前，B 只能從 Studio 手動上傳、手抄數據。計畫見 `docs/videos/channel-os-20261117/shared/05-ai-production.md` §4。

## Definition of done

- [ ] 後台可以連結兩個以上的 YouTube 頻道，每個頻道有自己的 OAuth 授權與狀態。
- [ ] 每支影片或系列記錄要上傳到哪個頻道；預設 `curio`、`sothatswhy` 上 A，`zhong-tian-qu-qi*`、漫劇與寵物短劇上 B。
- [ ] 公開同步與報表下載依頻道分開；`node tools/video/youtube-reports/cli.mjs` 可以用 `--channel` 指定頻道。
- [ ] 現有的 A 頻道連線不用重新授權，遷移後照常運作。

## Steps

- [ ] 讀 `backend-conventions`：migration 接在目前 head 之後、整合測試、後台頁登記。
- [ ] **認領時把 scope 擴大到** `apps/api/app/models.py`、新的 migration 檔、`apps/api/app/video_reviews/admin_service.py` 與對應的測試（建票時刻意不列，避免和進行中的票衝突）。
- [ ] 設計資料表：拿掉 `id = 1` 限制、加頻道欄位，影片或系列指到頻道。
- [ ] API、後台設定分頁、報表 CLI 依序改。

## How to verify

`cd apps/api && uv run pytest`、`npm run test:tools`；在後台連結第二個測試頻道，上傳一支私人影片，確認它出現在正確的頻道。

## Notes

從 `docs/videos/channel-os-20261117/` 開出（2026-11-17）。
