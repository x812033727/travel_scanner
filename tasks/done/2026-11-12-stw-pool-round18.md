---
id: 2026-11-12-stw-pool-round18
title: 原來如此素材池第十八輪：補讀後備組題
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round18
claimed_at: 2026-11-12T11:07:17Z
created_at: 2026-11-12T11:07:17Z
completed_at: 2026-11-12T11:51:43Z
branch:
depends_on: []
scope:
  - docs/videos/so-thats-why/pool
---

# 原來如此素材池第十八輪：補讀後備組題

## Why

站主 2026-11-12：「持續擴充」。延續第十七輪，補讀其次接近門檻的後備組題；夠成一集的才成題，不為片長硬湊。

## Definition of done

- [x] wave68 批次、checkpoint-4089、reviews/material-20261111-round18.{json,md} 入庫，`cli.mjs check` PASS，pool.test.mjs 與 catalog.test.mjs 全過。

## Steps

- [x] 作者 F31 補 C10-01 冰、C12-01 冷凍肉；作者 F32 補 C13-01 鳥蛋、C13-02 蝸牛。
- [x] 兩位非作者覆核（V34、V35）重抓來源、逐筆讀工具紀錄、重算片長。
- [x] 組進素材池：四題都留後備。

## How to verify

`node tools/video/so-thats-why/pool/cli.mjs check`、`node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`（32 過）。

## Notes

入選 4,089→4,103，可成題長題維持 86。四題的覆核都認為補齊被擋的來源也只是勉強到線：C10-01、C12-01 各約 8.0 分差 1 條；C13-01 約 7.7 分；C13-02 約 7.0 分，建議與 B2128 合併成「殼的左右與螺旋」再評。之後的補讀優先順序：被 Cloudflare 擋的關鍵原研究（JEB、cell.com、PNAS）沒有合法替代就不再追。
