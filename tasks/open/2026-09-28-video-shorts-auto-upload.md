---
id: 2026-09-28-video-shorts-auto-upload
title: Video shorts Y2: once the API audit has passed, the site uploads Shorts itself when a slot locks
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-28T04:15:00Z
completed_at:
branch:
depends_on:
  - 2026-09-28-video-shorts-youtube-auto
scope:
  - apps/api/app/video_shorts/upload.py
  - apps/api/app/video_shorts/tick.py
  - apps/api/app/video_shorts/publish.py
  - apps/api/tests/test_video_shorts_upload.py
---

# Video shorts Y2: once the API audit has passed, the site uploads Shorts itself when a slot locks

## Why

稽核通過前，全自動的最後一哩是站主每週把一批 mp4 拖進 Studio。稽核通過後，網站用 `videos.insert` 上傳的影片不再被鎖成私人，這一步就可以拿掉：時段鎖定時網站自己上傳、同時帶私人與 `publishAt`，站主只看每週報告。

續傳上傳、工作階段的保存與重試在 `app/video_youtube/sync.py` 已經有了（長片的「由網站上傳」）；缺的是「時間到了自己開始」與一天的上限。

設計全文在 `docs/videos/SHORTS.md`（§上架）。

## Definition of done

- [ ] 設定分頁的「YouTube API 稽核已通過」勾著、自動上架授權有效、沒有暫停時，`tick` 在時段鎖定的那一刻為那支 Shorts 建立 `mode: "upload"`、`visibility: "scheduled"` 的同步請求並啟動；沒勾時行為跟 Y1 一樣（等站主上傳）。
- [ ] 一天最多上傳 `max_per_day` 支，而且不超過 `videos.insert` 每天 100 次的配額桶；同一支 Shorts 絕不上傳第二份（已有影片 id 或有未完成的上傳工作階段時接續）。
- [ ] 上傳失敗：照既有的退避重試；當天仍失敗就把時段記成 `missed`、影片回片庫、原因寫在影片上並進每週報告。被 YouTube 以「頻道今天的上傳次數到上限」拒絕時當天不再試。
- [ ] Shorts 分頁的「等你上傳」區塊在勾了稽核之後不再出現（W1 已經照這個條件顯示）。
- [ ] pytest：自動開始的條件、每天上限、不重複上傳、失敗後的狀態。

## Steps

- [ ] 確認稽核已經通過、站主已經勾了那個開關；沒有的話這張票保持 open。
- [ ] `upload.py` 與 `tick.py` 的分支。
- [ ] 測試。
- [ ] 第一支先用一個隔天的時段試，確認 YouTube 端是私人加排程、到時間自己公開。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_video_shorts_upload.py tests/test_video_shorts_publish.py -q
```

## Notes

- 這張票要等站主送出稽核申請（`2026-09-28-video-shorts-audit-update`、`2026-09-26-video-hands-off-api-audit`）而且 YouTube 回覆通過；那是票外面的事，沒辦法寫成 `depends_on`。
- 網站永遠不把影片直接設成公開；`publishAt` 在過去會讓 YouTube 立刻公開，所以時間一定要在未來至少五分鐘（既有的 `MIN_LEAD`）。
