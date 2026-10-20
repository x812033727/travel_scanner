---
id: 2026-10-20-curio-s41-gate-readiness
title: Curio S41 gate readiness after audited preproduction
status: blocked
priority: P2
area: docs
owner: codex-s41-qin-feasibility
claimed_at: 2026-10-20T10:45:33Z
created_at: 2026-10-20T10:45:32Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s41
---

# Curio S41 gate readiness after audited preproduction

## Why

S41 R5h 書面前製在 `a3063691` 推送並經獨立 source/visual 與雙盲讀通過；站台影片流程只把 `verify-1.md` 視為已查核，原本的完整報告在 `reviews/source-visual.md`。大綱也須送真實 A/B 並記錄站台判定，不可把本機 Jev 挑選冒充站主核准。

## Definition of done

- [x] 站台收到現版 A/B 大綱，回覆的挑選與實際核准狀態被準確記錄。
- [x] `verify-1.md` 把獨立逐景查核接到流程，保留 R5h 的五個 frozen 審閱檔原樣。
- [ ] 待站台大綱確實核准後，才送現版劇本關卡；不生成付費媒體。

## Steps

- [x] 讀取站台 S41 狀態與企劃 A/B parser 輸出。
- [x] 送大綱並以 `review-pull` 查詢，不製造人工核准。
- [x] 將已有獨立報告對接 `verify-1.md`，重跑本機狀態與查核。
- [ ] 在站台大綱核准後送 script gate，更新交接紀錄。

## How to verify

`node tools/video/cli.mjs lint --slug curio-s41`；`node tools/video/cli.mjs status --slug curio-s41 --workdir /tmp/s41-review`；`NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node tools/video/cli.mjs review-pull --slug curio-s41 --gate outline --workdir /tmp/s41-review`。`review-pull` 的 `pending` 是等待站主，並非核准。

## Notes

2026-10-20: 站台原先沒有 S41 紀錄。`review-push --gate outline` 已把當前 `brief.md` SHA-256 `f1b37142edd09fc7a7d29e003f7be9e4f1a852525218211128a749a6f24db1ff` 的 A/B 送到站台；Jev 選 A（機率 1.00、立場 0.88、建議 0.01），但這是手動推送影片，沒有 worker `auto.json`，站台回 `pending`。立即 `review-pull` 回 `outline: waiting for the owner`。不得用本機 `approve` 或虛構 worker 檔把 pending 寫成核准。S41 工作目錄在 `/tmp/s41-review/curio-s41`，合併盲讀 `review/narrative.json` 是有效的現版；無付費媒體。
