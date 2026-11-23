---
id: 2026-11-12-stw-pool-round19
title: 原來如此素材池第十九輪：補讀其餘後備組題
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round19
claimed_at: 2026-11-12T11:22:55Z
created_at: 2026-11-12T11:22:38Z
completed_at: 2026-11-12T11:56:25Z
branch:
depends_on: []
scope:
  - docs/videos/so-thats-why/pool
---

# 原來如此素材池第十九輪：補讀其餘後備組題

## Why

站主 2026-11-12：「持續擴充」，並要求更多子代理並行。與第十八輪並行，三位作者各補一題其餘的後備組題；夠成一集的才成題，不為片長硬湊。

## Definition of done

- [x] wave69 批次、checkpoint-4103、reviews/material-20261111-round19.{json,md} 入庫，`cli.mjs check` PASS，pool.test.mjs 與 catalog.test.mjs 全過。

## Steps

- [x] 作者 F33 補 C11-01 迷路繞圈、F34 補 C11-02 鴿子點頭、F35 補 C9-01 浴室唱歌。
- [x] 三位非作者覆核（V36、V37、V38）重抓來源、逐筆讀工具紀錄、重算片長。
- [x] 組進素材池：三題都留後備。

## How to verify

`node tools/video/so-thats-why/pool/cli.mjs check`、`node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`（32 過）。

## Notes

入選 4,103→4,119，可成題長題維持 86。第十九輪與第十八輪並行研究，checkpoint-4103 是第十八輪併入後、第十九輪併入前的快照。三題離門檻都還遠（約 5.8–6.9 分），覆核都認為補齊被擋的來源也難到 8.5 分；鴿子點頭建議與其他鳥類視覺題合併再評。後備組題補讀的邊際效益已經很低，之後若要新長題，可能要改成在既有長題裡加章節，或請站主放寬「每題兩個不同研究群」的要求。
