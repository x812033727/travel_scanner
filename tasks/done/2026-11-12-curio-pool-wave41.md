---
id: 2026-11-12-curio-pool-wave41
title: 奇聞檔案局素材池第四十一批
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round20
claimed_at: 2026-11-12T12:19:51Z
created_at: 2026-11-12T12:19:36Z
completed_at: 2026-11-12T13:28:24Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
---

# 奇聞檔案局素材池第四十一批

## Why

站主 2026-11-12：「持續擴充」。奇聞檔案局再補一批新題，去重、整理來源，太薄或無聊的合併或淘汰，不為片長硬湊。

## Definition of done

- [x] batches/wave41-20261112.json 與 reviews/wave41-review-20261112.json 入庫，`cli.mjs check` PASS，pool.test.mjs 全過。

## Steps

- [x] 八個研究代理（O1–O8）先去重再實讀來源。
- [x] 八位非作者覆核（R411–R418）逐題重開關鍵來源，並逐筆讀工具紀錄。
- [x] 組批、成題（T137–T140）、更新 selection 與 README，跑語意近鄰。

## How to verify

`node tools/video/curio/pool/cli.mjs check`（PASS）與 `node --test tools/video/curio/pool/pool.test.mjs`（23 過）。

## Notes

入選 1191→1229；暫緩 N4366；待查 4 題；N4385 與 wave40 的 N4265 同案退回，新讀的 1930 年來源記在 R414 merge_notes。O3、O8 兩筆網址規則違規都自報、覆核核實，沒有內容依賴違規抓取。
