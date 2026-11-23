---
id: 2026-11-11-stw-pool-round6
title: 原來如此素材池第六輪：補後備長題缺的來源
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round6
claimed_at: 2026-11-11T23:16:11Z
created_at: 2026-11-11T23:16:09Z
completed_at: 2026-11-12T00:02:19Z
branch: claude/sleepy-rubin-3jpyl9
depends_on: []
scope:
  - docs/videos/so-thats-why/pool
---

# 原來如此素材池第六輪：補後備長題缺的來源

## Why

站主 2026-11-11：「繼續擴充奇聞跟原來如此素材池」。原來如此事務所替後備長題補缺的來源，夠成一集的才升為可成題，不為片長硬湊。

## Definition of done

- [x] wave56 批次、checkpoint-3733、reviews/material-20261111-round6.{json,md} 入庫，`cli.mjs check` PASS，pool.test.mjs 與 catalog.test.mjs 全過。

## Steps

- [x] 兩個研究代理（F7：G21、G20、G22、G26；F8：G12、G09、G11、G30）照各題 missing 補讀來源。
- [x] 兩位非作者覆核（V10、V11）重開來源、重算片長。
- [x] 組進素材池，夠 8.5 分鐘的升為可成題，其餘留後備並寫明缺什麼。

## How to verify

`node tools/video/so-thats-why/pool/cli.mjs check`、`node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`（32 過）。

## Notes

入選 3,733→3,784，可成題長題 54→61（G21、G20、G22、G26、G12、G09、G11）；G30 仍後備（約 8.3 分，塑化劑降到室溫以下那筆資料被退回）。覆核把作者估計每題下修 2–3 分鐘。五篇論文（Bshary & Grutter 2005 等）只經 WebFetch 讀取、本機沒有逐字快取：PMC 對 curl 回驗證頁、期刊站 403，沒有繞過；寫稿前要重讀。C2017 掛錯的 Deutsch 1970 來源與 E7006 同一種情形，併在票 2026-11-11-stw-pool-e7006-source-ref 處理。研究進行中若重建素材池，代理的 `cli.mjs search` 會回 Index is stale：重建後要立刻跑 `cli.mjs index`。還沒碰的後備長題：G01、G08、G35、G38、G42、G43、G52。
