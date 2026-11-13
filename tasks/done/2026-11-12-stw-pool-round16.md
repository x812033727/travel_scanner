---
id: 2026-11-12-stw-pool-round16
title: 原來如此素材池第十六輪：從頭研究新長題
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round16
claimed_at: 2026-11-12T09:44:29Z
created_at: 2026-11-12T09:44:28Z
completed_at: 2026-11-12T10:29:51Z
branch:
depends_on: []
scope:
  - docs/videos/so-thats-why/pool
---

# 原來如此素材池第十六輪：從頭研究新長題

## Why

站主 2026-11-12：「持續擴充」。上一輪八個直覺候選全部池中已有，這輪先在全池大範圍去重再選題；夠成一集的才成題，不為片長硬湊。

## Definition of done

- [x] wave66 批次、checkpoint-4032、reviews/material-20261111-round16.{json,md} 入庫，`cli.mjs check` PASS，pool.test.mjs 與 catalog.test.mjs 全過。

## Steps

- [x] 作者 F27（住家、廚房與日常科技，23 個候選）、F28（天空、地球與身邊的生物，28 個候選）先大範圍去重，各從零研究兩個新長題。
- [x] 兩位非作者覆核（V30、V31）重抓全部來源、逐筆讀工具紀錄、重算片長。
- [x] 組進素材池：四題都留後備，沒有新長題。

## How to verify

`node tools/video/so-thats-why/pool/cli.mjs check`、`node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`（32 過）。

## Notes

入選 4,032→4,074，可成題長題維持 84。連續三輪（第十四到十六輪）從零研究的新長題 8 題只成 0 題：日常科學直覺題大多池中已有，剩下的題開放原研究不夠兩個研究群、或關鍵研究被 Cloudflare 擋。覆核每題都把作者的事實數下修 15–35%。之後若要新長題，可能要改成以池中後備組題為主補讀，或接受只在既有長題裡加章節。食品題這輪用 K66 前綴（F 前綴容易跟作者代號 F27 混淆）。週期蟬（13／17 年）F28 讀了 10 篇、關鍵研究全被擋，快取在 scratchpad 的 stw16/f28src。
