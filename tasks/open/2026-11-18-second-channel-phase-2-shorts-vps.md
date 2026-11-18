---
id: 2026-11-18-second-channel-phase-2-shorts-vps
title: Second channel phase 2: Shorts, VPS uploader and host CLIs
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-11-18T01:52:29Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_shorts
  - apps/api/app/video_youtube/vps.py
  - apps/api/app/video_youtube/vps_settings.py
  - apps/api/app/video_youtube/retitle.py
  - services/youtube-uploader
---

# Second channel phase 2: Shorts, VPS uploader and host CLIs

## Why

第一階段（看板票 `2026-11-17-second-youtube-channel-per-channel-connection`，migration 0147）讓站台可以連好幾個 YouTube 頻道，影片上傳、貼網址驗證、報表與觀眾續看都依影片的 `youtube_channel_key` 分頻道。以下幾塊還固定用 default 頻道（@Mokaair），摩卡劇場要用時得補：Shorts 的排程、授權範圍、數據讀取與上傳後的比對（`app/video_shorts/settings.py` 的 `channel_facts` 直接讀第 1 列；`publish.py`、`tick.py`、`claim.py` 呼叫 `connection.access_token` 沒帶 key）；VPS 上傳器只認一個 `UPLOADER_CHANNEL_ID`；主機指令 `video-youtube-caption-titles`（`retitle.py`）和 `video-youtube-backfill-publish-times` 只走 default。說明見 `docs/videos/YOUTUBE-REPORTS.md` §頻道。

## Definition of done

- [ ] 一個 Short 可以排到摩卡劇場：站主的授權範圍是依頻道給的，排程、讀數據、上傳後比對都用那個頻道的授權。
- [ ] VPS 上傳器可以依影片的頻道選 Studio 帳號，或明確說明只支援一個頻道、選了別的頻道時拒絕。
- [ ] 兩個主機指令加 `--channel`。

## Steps

- [ ] 讀 `backend-conventions` 和 `docs/videos/SHORTS.md`。
- [ ] Shorts 的同意範圍（`consent_scope`）改成每個頻道一份。

## How to verify

`cd apps/api && uv run pytest tests/test_video_shorts_*.py tests/test_video_youtube_vps*.py`。

## Notes

從第一階段開出（2026-11-18）。
