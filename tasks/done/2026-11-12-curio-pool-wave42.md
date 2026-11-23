---
id: 2026-11-12-curio-pool-wave42
title: 奇聞檔案局素材池第四十二批
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round20
claimed_at: 2026-11-12T12:44:18Z
created_at: 2026-11-12T12:44:17Z
completed_at: 2026-11-12T13:43:00Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
---

# 奇聞檔案局素材池第四十二批

## Why

站主 2026-11-12：「持續擴充」。奇聞檔案局再補一批新題，去重、整理來源，太薄或無聊的合併或淘汰，不為片長硬湊。

## Definition of done

- [x] batches/wave42-20261112.json 與 reviews/wave42-review-20261112.json 入庫，`cli.mjs check` PASS，pool.test.mjs 全過。

## Steps

- [x] 八個研究代理（I1–I8）先去重再實讀來源。
- [x] 八位非作者覆核（R421–R428）逐題重開關鍵來源，並逐筆讀工具紀錄。
- [x] 組批、成題（T141、T142）、更新 selection、README 與 dedup-decisions（3 組字面近鄰判不同）。

## How to verify

`node tools/video/curio/pool/cli.mjs check`（PASS）與 `node --test tools/video/curio/pool/pool.test.mjs`（23 過）。

## Notes

入選 1229→1265；暫緩 N4545、N4603；待查 4 題。I5 一筆網址規則違規（自加 www. 並換格式字尾，沒當來源）。本批中途子代理共用搜尋額度用完，後半段只重開已列網址，卒年補不到的人一律不入畫。
