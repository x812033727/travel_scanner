---
id: 2026-09-25-video-auto-worker-image-node-chromium
title: Video auto worker image: Node, Chromium and ffmpeg in a compose service that runs the pipeline
status: done
priority: P1
area: ops
owner: claude-opus-5-5
claimed_at: 2026-09-25T08:22:20Z
created_at: 2026-09-25T07:38:50Z
completed_at: 2026-09-25T08:27:24Z
branch: claude/video-auto-worker-image
depends_on: []
scope:
  - ops/video
  - docker-compose.prod.yml
  - .github/workflows/video-worker-image.yml
---

# Video auto worker image: Node, Chromium and ffmpeg in a compose service that runs the pipeline

## Why

旁白、畫面、成片、字幕要在主機上跑，需要一個有 Node、Chromium、ffmpeg 與 Noto 字型的容器。設計全文在 `docs/videos/AUTOMATION.md`。站主 2026-09-25 的決定：在正式站主機上跑；設定放在「影片審核」頁；旁白 Jev 全數通過就自動核准，其他關卡等站主。

## Definition of done

- [x] `ops/video/Dockerfile`：
  - 以 `mcr.microsoft.com/playwright:v1.63.0-noble` 為底，瀏覽器版本和鎖檔的 `@playwright/test` 1.63.0 一致。
  - 另外裝 apt 的 ffmpeg（含 libx264）與 tools 用到的四個套件（`ops/video/package.json`，版本照鎖檔）。
  - 以 pwuser 執行。
- [x] `ops/video/Dockerfile.dockerignore`：只放 `tools/video`、`.agents/skills/youtube-video`、`docs/videos`、內容包和兩個 ops 檔，不可能帶進 `.env`。
- [x] `docker-compose.prod.yml` 的 `video-worker`（profile `video`）：
  - 三個具名 volume：工作區、權杖、`docs/videos`。
  - `read_only`、`/tmp` 用 tmpfs、`cap_drop: ALL`、`no-new-privileges`。
  - `shm_size` 1g，Chromium 在 64 MB 下渲染 1080p 會崩。
  - `mem_limit` 3g。
- [x] 工人迴圈 `ops/video/worker.sh`：
  - 沒有權杖就先 `login`，驗證碼印在 log，15 分鐘後重試。
  - 權杖存時對公開網址；執行時用 `MOKAAIR_SITE=http://web:3000` 走 compose 網路。
  - 每 5 分鐘跑一次 `auto`；沒開啟就什麼都不做，這由 `auto` 自己判斷。
- [ ] CI 建映像並在裡面跑煙霧測試（`.github/workflows/video-worker-image.yml`）：PR 上第一次跑時確認。

## Steps

- [x] 映像、dockerignore、套件清單、迴圈腳本。
- [x] compose 服務與 volume。
- [x] CI workflow。

## How to verify

- CI 的「Video worker image」會做這些事：
  - 照 compose 的方式建映像；
  - 再建 Dockerfile 的 `smoke` 階段：確認以 pwuser 執行、ffmpeg 有 libx264、skill 與頻道規格在映像裡、沒有 `.env` 或權杖，然後在映像裡跑 `assemble/smoke.mjs`，從 render 一路做到 package。
- 煙霧測試寫成建置階段，不用 `docker run`：`tools/ci-images.test.mjs` 規定每個 `docker run` 的映像都要先經 `pull-images.sh` 從 registry 拉，本機建的映像拉不到。
- 本機沒有 Docker，沒辦法在本機建映像。

## Notes

- **`auto` 的 CI 檢查放在 orchestrator 那張票**：這條分支沒有 `tools/video/automation`，沒辦法驗「沒權杖時結束碼 3」。
- **底層映像只釘標籤、沒有釘 digest**：Playwright 官方映像會隨標籤更新；CI 第一次建成功後，可以把 digest 釘進 Dockerfile。
- **`docs/videos` 的 volume**：第一次建立時從映像複製一份。之後映像更新（例如新的頻道規格）不會自動更新 volume 裡的副本；要更新就刪掉 volume 讓它重建，工人產生的影片資料夾要先備份。
- **部署**：這張票只放檔案。主機部署腳本加 `--profile video`、配對、開啟設定，在 `video-auto-rollout`。
