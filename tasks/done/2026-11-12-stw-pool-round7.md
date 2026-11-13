---
id: 2026-11-12-stw-pool-round7
title: 原來如此素材池第七輪：補其餘後備長題的來源
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round7
claimed_at: 2026-11-12T00:34:46Z
created_at: 2026-11-12T00:34:44Z
completed_at: 2026-11-12T01:29:00Z
branch: claude/sleepy-rubin-3jpyl9
depends_on: []
scope:
  - docs/videos/so-thats-why/pool
---

# 原來如此素材池第七輪：補其餘後備長題的來源

## Why

站主 2026-11-12：「繼續擴充」。原來如此事務所替其餘後備長題補缺的來源，夠成一集的才升為可成題，不為片長硬湊。

## Definition of done

- [x] wave57 批次、checkpoint-3784、reviews/material-20261111-round7.{json,md} 入庫，`cli.mjs check` PASS，pool.test.mjs 與 catalog.test.mjs 全過。

## Steps

- [x] 兩個研究代理（F9：G52、G43、G42、G30；F10：G08、G35、G01、G38）照各題 missing 補讀來源。
- [x] 兩位非作者覆核（V12、V13）重抓來源、重算片長。
- [x] 組進素材池，夠 8.5 分鐘且有兩個轉折的升為可成題，其餘留後備並寫明缺什麼。

## How to verify

`node tools/video/so-thats-why/pool/cli.mjs check`、`node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`（32 過）。

## Notes

入選 3,784→3,838，可成題長題 61→65（G52、G43、G30、G08）。G42、G35、G01、G38 仍後備：G42 要一份與 Lstiburek 無關的濕熱氣候實測或模擬；G01 要一份有濃度的糖鹽導電量測；G38 改題後還差約 1.5 條、要來自 Signal 以外的來源；G35 約 8.3 分、企劃自己說不是長片候選。素材審視點名的後備長題都補過一輪了，下一輪要擴充得另找方向（新組長題或新核心）。P164、P024 掛錯的舊來源併在票 2026-11-11-stw-pool-e7006-source-ref。
