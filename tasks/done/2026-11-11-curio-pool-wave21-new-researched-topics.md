---
id: 2026-11-11-curio-pool-wave21-new-researched-topics
title: Curio pool wave21: new researched topics, dedup and sources; thin or dull ones merged or dropped, no padding
status: done
priority: P1
area: docs
owner: claude-opus-cloud-channel-review
claimed_at: 2026-11-11T05:41:09Z
created_at: 2026-11-11T05:41:08Z
completed_at: 2026-11-11T06:43:20Z
branch: claude/youthful-albattani-m1ih5z
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
---

# Curio pool wave21: new researched topics, dedup and sources; thin or dull ones merged or dropped, no padding

## Why

站主 2026-11-11：「繼續擴充素材池，一樣做好去重和來源整理，太薄或無聊的題目就合併或淘汰，影片不要為了片長硬湊」。

## Definition of done

- [x] 新一批題目經過研究、去重、非作者覆核後進素材池，太薄或重複的不收，不為片長硬湊。

## Steps

- [x] 6 個研究代理（約 90 個點子，收 28 題）。
- [x] 3 位非作者覆核逐題重開關鍵來源（`reviews/wave21-review-20261111.json`）。
- [x] 語意近鄰去重（釘版 MiniLM）與素材池搜尋。
- [x] `batches/wave21-20261111.json`、`selection.json`（786）、題案 T113、README 第二十一批。

## How to verify

`node tools/video/curio/pool/cli.mjs check`（PASS，入選 786、題案 107）；`node --test tools/video/curio/pool/*.test.mjs`。

## Notes

- 退回 N2441（=M11 對照章）、N2461（併入 N2443）；N2445 待查。
- 覆核建議的系列排序（N2422＋N2423 等）要站主決定，沒有排成題案。
- 素材池搜尋若回 `Index is stale`，先跑 `cli.mjs index`（只寫本機 .cache）。
