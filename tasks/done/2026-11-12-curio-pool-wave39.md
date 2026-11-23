---
id: 2026-11-12-curio-pool-wave39
title: 奇聞檔案局素材池第三十九批
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round20
claimed_at: 2026-11-12T11:30:36Z
created_at: 2026-11-12T11:30:35Z
completed_at: 2026-11-12T12:35:21Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
---

# 奇聞檔案局素材池第三十九批

## Why

站主 2026-11-12：「持續擴充」。奇聞檔案局再補一批新題，去重、整理來源，太薄或無聊的合併或淘汰，不為片長硬湊。

## Definition of done

- [x] batches/wave39-20261112.json 與 reviews/wave39-review-20261112.json 入庫，`cli.mjs check` PASS，pool.test.mjs 全過。

## Steps

- [x] 十個研究代理（G1–G10）先去重再實讀來源。
- [x] 十位非作者覆核（R391–R400）逐題重開關鍵來源，並逐筆讀工具紀錄。
- [x] 組批、成題（T136）、更新 selection、README 與 dedup-decisions（N4101～N501 判不同），跑語意近鄰。

## How to verify

`node tools/video/curio/pool/cli.mjs check`（PASS）與 `node --test tools/video/curio/pool/pool.test.mjs`（23 過）。

## Notes

入選 1120→1156；暫緩 N3942（要改排 T43）、N4003（轉 Shorts）；待查 9 題，其中 N4044「讓中國睡吧」是排除線問題要站主決定。G10 自己輸入 NTRS API 網址（沒當來源）記在 rule1_record。
