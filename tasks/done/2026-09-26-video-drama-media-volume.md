---
id: 2026-09-26-video-drama-media-volume
title: Video drama: video_media volume in production compose and the disk figures
status: done
priority: P2
area: ops
owner: claude-fable-5-1-video-drama
claimed_at: 2026-09-26T07:15:21Z
created_at: 2026-09-26T01:53:28Z
completed_at: 2026-09-26T16:39:11Z
branch:
depends_on:
  - 2026-09-26-video-drama-media-api
  - 2026-09-25-run-the-site-s-claude-features
scope:
  - docker-compose.prod.yml
---

# Video drama: video_media volume in production compose and the disk figures

## Why

媒體庫 `/var/lib/mokaair/video-media` 沒掛 volume 之前，生成結果寫在 api 容器層，重部署就掉。`docker-compose.prod.yml` 正被 `2026-09-25-run-the-site-s-claude-features` 鎖住，所以拆成這張票排在它之後。

## Definition of done

- [x] `api.volumes` 有 `video_media:/var/lib/mokaair/video-media`，頂層 `volumes:` 有 `video_media`（本機 js-yaml 解析過）。
- [x] 部署後 `GET /api/v1/video/media/status` 的 `store.writable` 為 true。→ 2026-09-26 16:36Z 部署 c5ed650a 後從工人容器查：`writable: true`、`used_bytes: 0`、單檔 200 MB、總量 30 GB；`travel_scanner_video_media` 是具名 volume，重部署不會掉（還沒有檔案可拿來證明，第一集做完再看）。
- [ ] 一支試作的磁碟用量（媒體庫與 `video_work`）記進 `docs/videos/DRAMA.md` 的成本節。→ 試作票 `2026-09-26-video-drama-pilot` 做完轉交。

## Steps

- [x] compose 改動；照 skill `deploy` 做主機預檢與部署。→ compose 已改；部署另排。
- [x] 部署後量 volume 大小。→ 媒體庫還是空的（used_bytes 0），數字等試作票量。

## How to verify

```bash
docker compose -f docker-compose.prod.yml config | grep -A3 video_media
```

## Notes

設計全文在 `docs/videos/DRAMA.md`（跟 T1 一起合併）；供應商、價格、政策的研究依據也在那裡。

2026-09-26（claude-fable-5-1-video-drama）：#804 合併後 14:45Z 的部署已把 volume 掛上（`docker volume ls` 有 `travel_scanner_video_media`，api 內 `/var/lib/mokaair/video-media` 為 app:app 755）；16:36Z 再部署 c5ed650a（#808、#814，alembic 到 0098）後驗證如上。磁碟數字交給 `2026-09-26-video-drama-pilot`。
