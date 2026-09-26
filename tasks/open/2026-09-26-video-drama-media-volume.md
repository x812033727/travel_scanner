---
id: 2026-09-26-video-drama-media-volume
title: Video drama: video_media volume in production compose and the disk figures
status: in-progress
priority: P2
area: ops
owner: claude-fable-5-1-video-drama
claimed_at: 2026-09-26T07:15:21Z
created_at: 2026-09-26T01:53:28Z
completed_at:
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
- [ ] 部署後 `GET /api/v1/video/media/status` 的 `store.writable` 為 true，重部署後檔案仍在。→ 等下一次部署（#791 的 0096、#797 的 0097 一起），部署時驗。
- [ ] 一支試作的磁碟用量（媒體庫與 `video_work`）記進 `docs/videos/DRAMA.md` 的成本節。→ 試作票 `2026-09-26-video-drama-pilot` 做完轉交。

## Steps

- [x] compose 改動；照 skill `deploy` 做主機預檢與部署。→ compose 已改；部署另排。
- [ ] 部署後量 `docker system df -v` 的 volume 大小。

## How to verify

```bash
docker compose -f docker-compose.prod.yml config | grep -A3 video_media
```

## Notes

設計全文在 `docs/videos/DRAMA.md`（跟 T1 一起合併）；供應商、價格、政策的研究依據也在那裡。
