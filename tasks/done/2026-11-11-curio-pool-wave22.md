---
id: 2026-11-11-curio-pool-wave22
title: 奇聞素材池第二十二批新題
status: done
priority: P2
area: docs
owner: claude-opus-cloud-channel-review
claimed_at: 2026-11-11T09:11:43Z
created_at: 2026-11-11T09:11:41Z
completed_at: 2026-11-11T09:58:37Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
---

# 奇聞素材池第二十二批新題

## Why

站主 2026-11-11 再次：「繼續擴充素材池，一樣做好去重和來源整理，太薄或無聊的題目就合併或淘汰，影片不要為了片長硬湊」。

## Definition of done

- [x] 新一批題目經研究、去重、非作者覆核後進素材池；太薄或重複的不收，不為片長硬湊。

## Steps

- [x] 4 個研究代理（約 66 個點子，收 25 題）。
- [x] 4 位非作者覆核（R221–R224），另補讀三筆來源。
- [x] 語意近鄰去重。
- [x] `batches/wave22-20261111.json`、`reviews/wave22-review-20261111.json`、selection（809）、題案 T114、README 第二十二批。

## How to verify

`node tools/video/curio/pool/cli.mjs check`（PASS，入選 809、題案 108）；`node --test tools/video/curio/pool/*.test.mjs`。

## Notes

- N2505 暫緩：要把 N1582 縮成約 7 分鐘才接得成一集，等站主決定。N2506 待查（Te Ara 403）。
- 素材池寫入後本機搜尋索引會過期，下一批開工前先跑 `cli.mjs index`。
