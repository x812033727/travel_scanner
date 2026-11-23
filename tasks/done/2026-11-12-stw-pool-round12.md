---
id: 2026-11-12-stw-pool-round12
title: 原來如此素材池第十二輪：補讀後備組題與從頭研究新長題
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round12
claimed_at: 2026-11-12T06:03:40Z
created_at: 2026-11-12T06:03:39Z
completed_at: 2026-11-12T06:42:28Z
branch: claude/sleepy-rubin-3jpyl9
depends_on: []
scope:
  - docs/videos/so-thats-why/pool
---

# 原來如此素材池第十二輪：補讀後備組題與從頭研究新長題

## Why

站主 2026-11-12：「繼續擴充」。池中既有核心已組不出新長題，這輪一邊補讀後備組題，一邊從零研究全新長題；夠成一集的才成題，不為片長硬湊。

## Definition of done

- [x] wave62 批次、checkpoint-3921、reviews/material-20261111-round12.{json,md} 入庫，`cli.mjs check` PASS，pool.test.mjs 與 catalog.test.mjs 全過。

## Steps

- [x] 作者 F19 補讀 C6-02、C7-01、C7-02；作者 F20 從零研究 C8-01 黃燈秒數、C8-02 雨天水漂。
- [x] 兩位非作者覆核（V22、V23）重抓全部來源、重算片長。
- [x] 組進素材池：新增 G622、G623，其餘留後備。

## How to verify

`node tools/video/so-thats-why/pool/cli.mjs check`、`node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`（32 過）。

## Notes

入選 3,921→3,951，可成題長題 80→82。後備的補法：C7-01 差 0.5 條（G578 先上片則差 1.5 條，須刪 X37-008），可讀 Begum Ali、Spence 與 Bremner 2015（Goldsmiths 典藏 PDF 在搜尋結果裡）；C8-01 行為與事故研究只讀到 FHWA 轉述，補 Chang 1985 或 Wortman & Fox 1986 原文，或台灣 3／4／5 秒表的官方依據；C8-02 約 8.0 分，FHWA-RD-79-31 與 NASA 1963 各被拆成多個核心，嚴格計分偏低，需再一份獨立的路面水漂研究。黃燈與水漂兩題都不得含駕駛或換胎建議，也不評價台灣法規。
