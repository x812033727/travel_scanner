---
id: 2026-11-11-curio-pool-wave24
title: 奇聞素材池第二十四批新題
status: done
priority: P2
area: docs
owner: claude-opus-cloud-channel-review
claimed_at: 2026-11-11T13:40:28Z
created_at: 2026-11-11T13:40:25Z
completed_at: 2026-11-11T14:25:21Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
---

# 奇聞素材池第二十四批新題

## Why

站主 2026-11-11 再次要求「繼續擴充素材池」：奇聞檔案局再補一批新題，去重、整理來源，太薄或無聊的合併或淘汰，不為片長硬湊。

## Definition of done

- [x] batches/wave24-20261111.json 與 reviews/wave24-review-20261111.json 入庫，`cli.mjs check` 為 PASS，pool.test.mjs 全過。

## Steps

- [x] 四個研究代理（E1–E4）先去重再實讀來源。
- [x] 四位非作者覆核（R241–R244）逐題重開關鍵來源，改動寫成完整欄位。
- [x] 組批、成題（T118）、更新 selection 與 README，跑語意近鄰。

## How to verify

`node tools/video/curio/pool/cli.mjs check`（PASS）與 `node --test tools/video/curio/pool/pool.test.mjs`（23 過）。

## Notes

素材池搜尋找不到 "Cock Lane"，N2647 是用 case_key 比對才發現與 N201 同案：去重時兩種都要做。ejournals.eu（Wojtucki 2020）與 etymonline 讀不到，沒有繞過。

## 結果（2026-11-11）

入選 832→851，新題案 T118（N2685＋N2686）；退回 N2647（與 N201 同案，素材池搜尋找不到，要用 case_key 比對）；待查 N2645、N2664、N2665，原因寫在批次備註。ejournals.eu 與 etymonline 讀不到。
