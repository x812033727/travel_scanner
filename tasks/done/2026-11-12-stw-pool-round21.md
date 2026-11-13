---
id: 2026-11-12-stw-pool-round21
title: 原來如此素材池第二十一輪
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round20
claimed_at: 2026-11-12T14:44:56Z
created_at: 2026-11-12T14:44:55Z
completed_at: 2026-11-12T15:14:40Z
branch:
depends_on: []
scope:
  - docs/videos/so-thats-why/pool
---

# 原來如此素材池第二十一輪

## Why

站主 2026-11-12：「原來如此要繼續擴充」「原來如此就一直持續審下去」。從零研究的新長題連四輪都沒過覆核；這一輪改成只補讀第二十輪覆核在 `still_missing` 點名的原文。

## Definition of done

- [x] 第七十一批（wave71-physics／earth／life）與 `reviews/material-20261111-round21.{json,md}` 入庫，checkpoint-4257 與 VALIDATION-4257 照前例建立，`cli.mjs check` PASS，pool 與 catalog 測試 32 過。

## Steps

- [x] 十二位作者（F42–F53）各補第二十輪的一題後備長題。
- [x] 十二位非作者覆核（V45–V56）重抓來源、逐筆讀工具紀錄、照守研究群封頂、重算片長。
- [x] 整合、更新 README 與報告。

## How to verify

`node tools/video/so-thats-why/pool/cli.mjs check`；`node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`。

## Notes

入選 4,257→4,299（46 個提案收 42、退回 4）；十二題都仍後備（4.5–7.5 分），可成題長題維持 86 組。F47 遇 403 後改抓同資料庫另一主機（沒取得內容），其餘無違規。第二批八題（F54–F61）移到 `2026-11-12-stw-pool-round22`。
