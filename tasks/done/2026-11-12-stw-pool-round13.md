---
id: 2026-11-12-stw-pool-round13
title: 原來如此素材池第十三輪：補讀後備組題與從頭研究新長題
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round13
claimed_at: 2026-11-12T07:14:55Z
created_at: 2026-11-12T07:14:53Z
completed_at: 2026-11-12T07:56:32Z
branch:
depends_on: []
scope:
  - docs/videos/so-thats-why/pool
---

# 原來如此素材池第十三輪：補讀後備組題與從頭研究新長題

## Why

站主 2026-11-12：「繼續擴充」。一邊替後備組題補讀，一邊從零研究全新長題；夠成一集的才成題，不為片長硬湊。

## Definition of done

- [x] wave63 批次、checkpoint-3951、reviews/material-20261111-round13.{json,md} 入庫，`cli.mjs check` PASS，pool.test.mjs 與 catalog.test.mjs 全過。

## Steps

- [x] 作者 F21 補讀 C7-01、C8-01、C8-02；作者 F22 對八個候選去重後從零研究 C9-01 浴室唱歌、C9-02 濕沙堆沙堡。
- [x] 兩位非作者覆核（V24、V25）重抓全部來源、重算片長。
- [x] 組進素材池：新增 G624，其餘留後備。

## How to verify

`node tools/video/so-thats-why/pool/cli.mjs check`、`node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`（32 過）。

## Notes

入選 3,951→3,978，可成題長題 82→83。後備的補法：C7-01 約 8.2 分（G578 不先上片、保留 X37-008 則 8.69 分可成題）；C8-02 約 8.4 分，差約 0.15 條，需要一份不同研究群的輪胎水漂量測全文（Physics of Fluids 刊本未讀）；C9-02 約 7.7 分，差約 1.3 條，Scheel 2008（ANU 限制到 2037）或 Møller & Bonn 2007 的合法公開全文；C9-01 約 6.7 分，缺浴室本身的聲學量測與聽眾端研究，難補。F22 的候選去重：幽靈塞車（G592）、麵包回凝（LEG-S54）、打哈欠（LEG-S05）、梅納反應（F4001）、咖啡環（G606）已有；電梯關門鍵找不到開放原研究；冰箱結霜的原研究都被機器驗證或付費擋住。cli.mjs search 這一輪一直回 Index is stale，作者與覆核都改讀 pool.json。
