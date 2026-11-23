---
id: 2026-11-11-stw-pool-round4
title: 原來如此素材池第四輪：補後備長題來源
status: done
priority: P2
area: docs
owner: claude-opus-cloud-channel-review
claimed_at: 2026-11-11T13:40:29Z
created_at: 2026-11-11T13:40:27Z
completed_at: 2026-11-11T14:42:21Z
branch:
depends_on: []
scope:
  - tools/video/so-thats-why/pool
---

# 原來如此素材池第四輪：補後備長題來源

## Why

站主 2026-11-11 再次要求「繼續擴充素材池」：原來如此事務所補齊後備長題與後備組題缺的核心，夠成一集的才升為可成題，不為片長硬湊。

## Definition of done

- [x] wave54 批次、checkpoint-3615、reviews/material-20261111-round4.{json,md} 入庫，`cli.mjs check` PASS，pool.test.mjs 與 catalog.test.mjs 全過。

## Steps

- [x] 兩個研究代理（F3、F4）補讀來源寫核心。
- [x] 兩位非作者覆核（V7、V6）逐題重開關鍵來源、重算片長。
- [x] 組進素材池：G19、G05、G14、G06、G16 升為可成題，新增 G605–G609；G01、C1-12、C1-13、C3-12 留在後備。

## How to verify

`node tools/video/so-thats-why/pool/cli.mjs check`、`node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`。

## Notes

覆核抓到兩個實質錯誤：Datasaurus 的恐龍與星星是兩個例子、統計值也不同；Hagen 1852 本人說更早有人量過，不能問「誰最先量到」。入選 3,615→3,661，可成題長題 36→46。G01 還差一章，est 7.9 分鐘。
