---
id: 2026-11-12-curio-n2443-lemuria-year
title: 奇聞素材池 N2443 把 Lemuria 寫成 1879 年提出，與 Sclater 1864 原文不合
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-11-12T02:25:03Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
---

# 奇聞素材池 N2443 把 Lemuria 寫成 1879 年提出，與 Sclater 1864 原文不合

## Why

第二十八批覆核 R284 讀 N3022（Lemuria）時發現：素材池的 N2443 寫「1879 年才提出的雷姆利亞大陸」，而 Sclater 取這個名字的文章刊在 1864 年 4 月號（來源見 batches/wave28-20261112.json 的 N3022）。N2443 是第二十二批的題，受快照保護，改動要走重查。

## Definition of done

- [ ] N2443 的年份照原文改正，或確認「1879」指的是別的文獻並寫明出處。

## Steps

- [ ] `node tools/video/curio/pool/cli.mjs show N2443` 看那句的上下文與它引的來源。
- [ ] 改動寫成該批的 recheck（`batches/<wave>.json` 的重查欄位），並在 `selection.json` 的 `raw_changes` 寫理由，重建。

## How to verify

`node tools/video/curio/pool/cli.mjs build && node tools/video/curio/pool/cli.mjs check`。

## Notes

不影響 N3022；N3022 的 scope 另有六條硬性界線，最後一段旁白稿上稿前要請站主看過。
