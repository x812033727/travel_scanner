---
id: 2026-11-12-curio-n2443-lemuria-year
title: 奇聞素材池 N2443 把 Lemuria 寫成 1879 年提出，與 Sclater 1864 原文不合
status: done
priority: P3
area: docs
owner: claude-sonnet-3-8
claimed_at: 2026-11-13T01:40:52Z
created_at: 2026-11-12T02:25:03Z
completed_at: 2026-11-13T03:01:52Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
---

# 奇聞素材池 N2443 把 Lemuria 寫成 1879 年提出，與 Sclater 1864 原文不合

## Why

第二十八批覆核 R284 讀 N3022（Lemuria）時發現：素材池的 N2443 寫「1879 年才提出的雷姆利亞大陸」，而 Sclater 取這個名字的文章刊在 1864 年 4 月號（來源見 batches/wave28-20261112.json 的 N3022）。N2443 是第二十二批的題，受快照保護，改動要走重查。

## Definition of done

- [x] N2443 的年份照原文改正，或確認「1879」指的是別的文獻並寫明出處。

## Steps

- [x] `node tools/video/curio/pool/cli.mjs show N2443` 看那句的上下文與它引的來源。
- [x] 改動寫成該批的 recheck（`batches/<wave>.json` 的重查欄位），並在 `selection.json` 的 `raw_changes` 寫理由，重建。

## How to verify

`node tools/video/curio/pool/cli.mjs build && node tools/video/curio/pool/cli.mjs check`。

## Notes

- 在 `batches/wave47-decisions-20261112.json` 新增 `DEC-S002`（Sclater 1864 年 4 月《The Quarterly Journal of Science》pp. 218–219 原文，與 `wave28` 的 `Q4-S005` 相同）與 `N2443` 的 `rechecks` 紀錄，將 `answer_target` 改為「1864 年 Sclater 才命名的『雷姆利亞大陸』（A5-S009 轉述為 1879 年，不論 1864 或 1879 皆晚於手稿自稱的 1838–39 年）」。
- `N2443` 為 `wave21` 新題，不在 `baseline.json`（涵蓋至 `wave20`）的快照原始紀錄內，故無須於 `selection.json` 宣告 `raw_changes`（若宣告會被 `validateBaseline` 判為 Stale raw change declaration）。
- 不影響 N3022；N3022 的 scope 另有六條硬性界線，最後一段旁白稿上稿前要請站主看過。
