---
id: 2026-09-25-video-auto-worker-image-node-chromium
title: Video auto worker image: Node, Chromium and ffmpeg in a compose service that runs the pipeline
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-09-25T07:38:50Z
completed_at:
branch:
depends_on: []
scope:
  - ops/video
  - docker-compose.prod.yml
---

# Video auto worker image: Node, Chromium and ffmpeg in a compose service that runs the pipeline

## Why

旁白、畫面、成片、字幕要在主機上跑，需要一個有 Node、Chromium、ffmpeg 與 Noto 字型的容器。設計全文在 `docs/videos/AUTOMATION.md`。站主 2026-09-25 的決定：在正式站主機上跑；設定放在「影片審核」頁；旁白 Jev 全數通過就自動核准，其他關卡等站主；寫稿用 API 金鑰（預設 Sonnet 寫、Opus 查）；題目先看站上新聞與文章，不夠再用 Brave 搜尋補。

## Definition of done

- [ ] `ops/video/Dockerfile`：非 root、字型齊全、`tools/video` 的煙霧測試（`assemble/smoke.mjs`）在映像裡通過。
- [ ] `docker-compose.prod.yml`：`video-worker` 服務（profile `video`）、具名 volume `video_work` 與權杖 volume，加固方式同其他服務。
- [ ] 工人迴圈：每 5 分鐘 `auto --once`，沒設定、沒開啟就什麼都不做。

## Steps

- [ ] 映像與 CI（路徑過濾的 workflow 建一次映像並跑煙霧測試）。
- [ ] compose 服務與 volume。
- [ ] 第一次啟動時跑配對，把驗證碼印在 log。

## How to verify

CI 建映像並跑煙霧測試；本機 `docker compose --profile video up video-worker` 看到配對碼。
