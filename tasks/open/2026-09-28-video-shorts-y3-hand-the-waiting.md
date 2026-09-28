---
id: 2026-09-28-video-shorts-y3-hand-the-waiting
title: Video shorts Y3: hand the waiting files to the Studio uploader instead of asking the owner to drag them
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-28T11:13:40Z
completed_at:
branch:
depends_on:
  - 2026-09-28-video-shorts-youtube-auto
  - 2026-09-28-vps-youtube-studio-deployment-and-live
scope:
  - apps/api/app/video_shorts/upload_bridge.py
  - apps/api/tests/test_video_shorts_upload_bridge.py
---

# Video shorts Y3: hand the waiting files to the Studio uploader instead of asking the owner to drag them

## Why

Shorts 區的「全自動」在 YouTube API 稽核通過之前還差一步：未稽核的專案用 API 上傳的影片會被鎖成私人，所以第一期的做法是站主每週把一批 mp4 拖進 YouTube Studio，網站再依檔名認領（`docs/videos/SHORTS.md` §稽核通過前，`app/video_shorts/claim.py`）。

2026-09-28 另一條線合併了「VPS 獨立 YouTube Studio 上傳服務」（PR #890、#893，`docs/videos/VPS-UPLOADER.md`，`app/video_youtube/vps.py`）：一個獨立的服務用瀏覽器操作 Studio，把核准的 mp4 上傳成私人影片並填好詳細資料，完成後把影片 id 記回網站。它不呼叫 Data API，也不公開或排程影片。

兩者接起來的話，稽核通過前站主連拖檔案都不用做：鎖定的時段由那個服務上傳成私人，拿到影片 id 之後，Shorts 原本的排程（`publish.send_due`，走 `videos.update` 加 `publishAt`）照舊把它排在時段的時間。

這張票先回答「能不能、該不該」，再決定要不要做。

## Definition of done

- [ ] 先確認三件事，結果寫進 `docs/videos/SHORTS.md`：
  - VPS 上傳服務已經在真的頻道上驗收過（`2026-09-28-vps-youtube-studio-deployment-and-live`）。沒有驗收過就不接。
  - 未稽核的專案對「Studio 上傳的私人影片」送 `videos.update` 加 `publishAt` 會成功（`2026-09-28-video-shorts-pilot-launch` 要實測的五項之一）。不成功的話，這條路到不了排程，這張票關掉並寫明原因。
  - 站主讀過 `VPS-UPLOADER.md` 開頭關於 YouTube 條款對自動存取的那一段，並明確決定要不要讓 Shorts 用這個服務。這是站主的決定，不是實作者的。
- [ ] 三件都成立才往下做：鎖定的時段、影片還沒有 YouTube id、服務已設定而且沒有工作在等人接手時，由伺服器替那支 Shorts 開一筆上傳工作；一次只開一筆（那個服務一個頻道只有一個瀏覽器 worker）。
- [ ] 服務回報影片 id 之後，那支 Shorts 跟「依檔名認領」對到的一樣：下一次 `tick` 由 `send_due` 排程。
- [ ] 服務停在「需要你接手」（登入、驗證、Studio 畫面變了）時，Shorts 分頁的「需要你」多一項，說明要到哪裡接手；那一格照舊在時間到了記成錯過，不晚發。
- [ ] 自動上架授權的條文第五項現在寫的是「檔案由我自己上傳到 YouTube Studio」。要用這個服務，條文要改、授權要重新同意：改 `rules.consent_text` 會讓既有的授權雜湊對不上，這是要的結果。
- [ ] 「等你上傳」與依檔名認領保留：服務沒設定、停住、或站主不想用的時候，原本的做法照舊可用。
- [ ] pytest：用假的上傳服務涵蓋開工作、一次一筆、拿到 id 之後排程、停住時的「需要你」、服務沒設定時什麼都不做。

## Steps

- [ ] 讀 `docs/videos/VPS-UPLOADER.md`、`app/video_youtube/vps.py`、`app/video_shorts/publish.py`、`claim.py`、`tick.py`。
- [ ] 等兩張相依的票的結果；把上面三件事的答案寫進文件。
- [ ] 站主決定之後才寫程式。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_video_shorts_upload_bridge.py tests/test_video_shorts_publish.py -q
```

對真的頻道：先用一支私人的測試影片走完「服務上傳 → 網站排程 → 撤回」，確認不會動到頻道上其他影片。

## Notes

- 發現的時間：2026-09-28 做 `2026-09-28-video-shorts-youtube-auto` 時，main 合併了 #890。Shorts 的設計（同一天稍早寫的）不知道有這個服務。
- `sync.request_sync` 與 `retry_sync` 現在會先問那個服務這支影片有沒有工作在跑（`vps.assert_idle`）；服務有設定但連不上時會回 503，Shorts 的 `send_due` 會把原因寫在那一格上、下一輪再試。這一段不用改。
- 那個服務不排程、不公開影片；排程仍然是 Data API 的事，配額照 `app/video_shorts/quota.py` 算。
- 不要為了省這一步去繞過 YouTube 的登入或驗證：那個服務遇到這些會停下來等人，這是對的。
