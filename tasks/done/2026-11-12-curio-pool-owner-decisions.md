---
id: 2026-11-12-curio-pool-owner-decisions
title: 奇聞素材池：站主決定 N5081 收、N5364 退
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round20
claimed_at: 2026-11-12T16:33:20Z
created_at: 2026-11-12T16:33:19Z
completed_at: 2026-11-12T16:41:07Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
---

# 奇聞素材池：站主決定 N5081 收、N5364 退

## Why

站主 2026-11-12：「你建議決定」。wave45、wave47 留下兩題要站主決定：N5081 1874 年中央公園猛獸騙局（覆核 R457 判待查的唯一理由是需站主同意 wave40 的條件），N5364 克拉科夫號聲（市集廣場 2026-11-07／08 剛發生致命攻擊）。

## Definition of done

- [x] N5081 依條件收（重查紀錄 `batches/wave47-decisions-20261112.json`），N5364 以 drop 退件（`dedup-decisions.json`），README 更新，`cli.mjs check` PASS，pool 測試全過。

## Steps

- [x] N5081：重查紀錄改 screened，scope 寫明只講報社收尾、別家怎麼罵與 Connery 的自述，猛獸咬人段落不唸不畫；不做新研究，只重列 R457 已重開的 Connery 1893。
- [x] N5364：drop，寫明重提條件。
- [x] 入選 1,411 → 1,412。

## How to verify

`node tools/video/curio/pool/cli.mjs check`；`node --test tools/video/curio/pool/pool.test.mjs`。

## Notes

其餘 42 題暫緩維持暫緩；奇聞素材池擴充已在 wave47 收尾。
