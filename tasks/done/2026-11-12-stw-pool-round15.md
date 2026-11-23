---
id: 2026-11-12-stw-pool-round15
title: 原來如此素材池第十五輪：補讀後備組題與從頭研究新長題
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round15
claimed_at: 2026-11-12T09:02:41Z
created_at: 2026-11-12T09:02:40Z
completed_at: 2026-11-12T09:39:39Z
branch:
depends_on: []
scope:
  - docs/videos/so-thats-why/pool
---

# 原來如此素材池第十五輪：補讀後備組題與從頭研究新長題

## Why

站主 2026-11-12：「持續擴充」。一邊替後備組題補讀，一邊從零研究全新長題；夠成一集的才成題，不為片長硬湊。

## Definition of done

- [x] wave65 批次、checkpoint-4006、reviews/material-20261111-round15.{json,md} 入庫，`cli.mjs check` PASS，pool.test.mjs 與 catalog.test.mjs 全過。

## Steps

- [x] 作者 F25 補讀 C9-02、C10-01；作者 F26 對八個候選去重（全部池中已有）後自提 C11-01 迷路繞圈、C11-02 鴿子點頭。
- [x] 兩位非作者覆核（V28、V29）重抓全部來源、逐筆讀工具紀錄、重算片長。
- [x] 組進素材池：四題都留後備，沒有新長題。

## How to verify

`node tools/video/so-thats-why/pool/cli.mjs check`、`node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`（32 過）。

## Notes

入選 4,006→4,032，可成題長題維持 84。後備：C9-02 約 8.43 分、差 0.25 條（Lu 2007 期刊版作者稿、Møller & Bonn 2007／Scheel 2008 合法全文）；C10-01 約 7.26 分、差 2.5 條，覆核估就算全補也只有約 11 條，建議不再追或併入其他摩擦題；C11-01 約 5.83 分、C11-02 約 5.44 分，關鍵原研究多在 cell.com、JEB 被 Cloudflare 擋。池中 P64-016、P64-017、P64-020 的字面改正（Canale 改期刊版、P64-016 計 1.0；P64-020 黏度倍數改為比值）因快照規則不能改寫舊批次，記在 round15 紀錄的 source_fixes，寫稿時照改。日常科學的直覺題池裡已很滿：F26 的八個候選全部已有，之後的新長題候選要先用 python 讀 pool.json 大範圍去重再列。
