---
id: 2026-09-26-video-series-pilot
title: Video series P1: the first series, three episodes end to end, and the numbers
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-26T17:36:33Z
completed_at:
branch:
depends_on:
  - 2026-09-26-video-series-episodes
  - 2026-09-26-video-series-admin-tab
scope:
  - docs/videos/SERIES.md
---

# Video series P1: the first series, three episodes end to end, and the numbers

## Why

規格是估的，數字要從第一部的前三集來：規劃的 token、劇本退回次數、每集媒體花費、設定圖是否真的沿用、旁白是否因詞彙表重錄。設計全文在 `docs/videos/SERIES.md`（站主 2026-09-27 的決定、名稱、流程、資料模型、提示詞規格都在那裡）；分票與順序在它的「分期與票」。

## Definition of done

- [ ] 站主在後台建第一部作品（原創仙俠、雙男主留白、約 100 集、每篇約 10 集、開放結局），設定集、總綱、第 1 篇細綱核准。
- [ ] 第 1–3 集做到上架：第 1 集生成設定圖並核准，第 2、3 集沿用；每集劇本經站主核准。
- [ ] `docs/videos/SERIES.md` 的成本與節奏改成實測數字；依數字調 `series_episodes_per_month`、月預算與 `series_max_in_flight`。

## Steps

- [ ] 部署後在後台建作品。
- [ ] 三集，逐集記錄。
- [ ] 改文件與設定。

## How to verify

看 `/admin/videos` 的漫劇分頁：三集都「已上架」，作品頁的花費與 `docs/videos/SERIES.md` 的數字一致。
