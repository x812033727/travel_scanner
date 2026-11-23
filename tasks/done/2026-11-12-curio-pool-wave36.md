---
id: 2026-11-12-curio-pool-wave36
title: 奇聞檔案局素材池第三十六批
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round16
claimed_at: 2026-11-12T10:04:04Z
created_at: 2026-11-12T10:04:03Z
completed_at: 2026-11-12T10:51:09Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
---

# 奇聞檔案局素材池第三十六批

## Why

站主 2026-11-12：「持續擴充」。奇聞檔案局再補一批新題，去重、整理來源，太薄或無聊的合併或淘汰，不為片長硬湊。

## Definition of done

- [x] batches/wave36-20261112.json 與 reviews/wave36-review-20261112.json 入庫，`cli.mjs check` PASS，pool.test.mjs 全過。

## Steps

- [x] 四個研究代理（C1–C4：U 博物館裡的未知生物、G 會移動的鬼、P 預知夢、L 考古騙局）先去重再實讀來源。
- [x] 四位非作者覆核（R361–R364）逐題重開關鍵來源，並逐筆讀工具紀錄。
- [x] 組批、更新 selection、T09 加一章（N3665）、README，跑語意近鄰。

## How to verify

`node tools/video/curio/pool/cli.mjs check`（PASS）與 `node --test tools/video/curio/pool/pool.test.mjs`（23 過）。

## Notes

入選 1050→1065；暫緩 N3644、N3645；待查 N3606、N3624、N3625、N3663。連續第二批四位研究代理都沒有違反網址規則。T09 從 11 分鐘改為 13 分鐘（加 Yarmouth 符文石章），已在上限，之後不能再加。N3645 補讀 Orderic Vitalis 後可能撐到 8 分鐘。
