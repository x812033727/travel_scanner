---
id: 2026-11-12-curio-pool-wave37
title: 奇聞檔案局素材池第三十七批
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round17
claimed_at: 2026-11-12T10:52:16Z
created_at: 2026-11-12T10:52:15Z
completed_at: 2026-11-12T11:45:11Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
---

# 奇聞檔案局素材池第三十七批

## Why

站主 2026-11-12：「持續擴充」。奇聞檔案局再補一批新題，去重、整理來源，太薄或無聊的合併或淘汰，不為片長硬湊。

## Definition of done

- [x] batches/wave37-20261112.json 與 reviews/wave37-review-20261112.json 入庫，`cli.mjs check` PASS，pool.test.mjs 全過。

## Steps

- [x] 四個研究代理（D1–D4：U 太空來的生命證據、G 鬼屋調查原始報告、P 預知與讀心表演、M 天氣與冰的怪象）先去重再實讀來源。
- [x] 四位非作者覆核（R371–R374）逐題重開關鍵來源，並逐筆讀工具紀錄。
- [x] 組批、成題（T134）、更新 selection 與 README，跑語意近鄰。

## How to verify

`node tools/video/curio/pool/cli.mjs check`（PASS）與 `node --test tools/video/curio/pool/pool.test.mjs`（23 過）。

## Notes

入選 1065→1081；暫緩 N3684、N3725（都要站主決定接既有題案或轉 Shorts）；待查 N3683、N3705。連續第三批四位研究代理都沒有違反網址規則。
