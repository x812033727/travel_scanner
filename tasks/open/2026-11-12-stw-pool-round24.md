---
id: 2026-11-12-stw-pool-round24
title: 原來如此素材池第二十四輪：十七個新領域從零研究新長題
status: in-progress
priority: P2
area: docs
owner: claude-cloud-pool-round20
claimed_at: 2026-11-12T15:51:12Z
created_at: 2026-11-12T15:51:06Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/so-thats-why/pool
---

# 原來如此素材池第二十四輪：十七個新領域從零研究新長題

## Why

站主 2026-11-12：「原來如此要繼續擴充」「可以開20個子代理」。第二十一到二十三輪三次補讀後備題都沒過線，覆核多建議不再單獨補讀；改回從零研究新長題。第二十輪的新題全部後備，原因多是只有一、兩個研究群有開放全文，所以這輪要求作者動筆前先確認至少三個不同研究群。

## Definition of done

- [ ] 新核心批次與 `reviews/material-20261111-round24.{json,md}` 入庫，快照照前例，`cli.mjs check` PASS，pool 與 catalog 測試全過；可成題的新長題寫進 themes.json。

## Steps

- [ ] 十七位作者（F82–F98）各在一個領域從零研究一個新長題：廚房、感官、雲雨雪、岩石、昆蟲、鳥類、水生動物、植物、材料、流體、聲音、天象、動物認知、微生物、哺乳類、河湖冰川、爬蟲兩棲。
- [ ] 非作者覆核（V85 起，一位作者一位覆核）。
- [ ] 整合、更新 README 與報告。

## How to verify

`node tools/video/so-thats-why/pool/cli.mjs check`；`node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`。

## Notes

作者與覆核說明在工作階段暫存區 stw24/BRIEF.md、REVIEW-BRIEF.md（不進 repo）。研究進行中（owner claude-cloud-pool-round20）。
