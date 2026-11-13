---
id: 2026-11-12-stw-pool-round10
title: 原來如此素材池第十輪：補讀後備組題缺的來源
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round10
claimed_at: 2026-11-12T03:29:43Z
created_at: 2026-11-12T03:29:41Z
completed_at: 2026-11-12T04:26:54Z
branch: claude/sleepy-rubin-3jpyl9
depends_on: []
scope:
  - docs/videos/so-thats-why/pool
---

# 原來如此素材池第十輪：補讀後備組題缺的來源

## Why

站主 2026-11-12：「繼續擴充」。這一輪只補讀新來源，不再派新組長題；夠成一集的才成題，不為片長硬湊。

## Definition of done

- [x] wave60 批次、checkpoint-3885、reviews/material-20261111-round10.{json,md} 入庫，`cli.mjs check` PASS，pool.test.mjs 與 catalog.test.mjs 全過。

## Steps

- [x] 作者 F15 補 C5-01、C5-02、C5-03；作者 F16 補 C4-02、C6-01、C6-02。
- [x] 兩位非作者覆核（V18、V19）重抓來源、重算片長。
- [x] 組進素材池：新增 G617–G620，C5-02、C6-02 留後備。

## How to verify

`node tools/video/so-thats-why/pool/cli.mjs check`、`node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`（32 過）。

## Notes

入選 3,885→3,907，可成題長題 75→79。行人那組改用于利希實驗，不再需要站主對 2006 年事故案例的裁示。C5-02 雨滴差至少 0.5 條（要一份田間自然降雨下雨濺傳病的原研究），C6-02 雲滴變雨差約 2.5 條。說明檔加了「不得猜測網址」後，仍有一位研究代理與一位覆核者各試過一個推出來的網址（都 404、未當來源）：下一輪把這條放到說明檔開頭。
