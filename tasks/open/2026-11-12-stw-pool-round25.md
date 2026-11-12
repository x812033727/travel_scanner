---
id: 2026-11-12-stw-pool-round25
title: 原來如此素材池第二十五輪：補讀第二十四輪最接近門檻的後備題
status: in-progress
priority: P2
area: docs
owner: claude-cloud-pool-round20
claimed_at: 2026-11-12T17:00:35Z
created_at: 2026-11-12T17:00:34Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/so-thats-why/pool
---

# 原來如此素材池第二十五輪：補讀第二十四輪最接近門檻的後備題

## Why

站主 2026-11-12：「原來如此還可以跑個兩輪」「每跑完一輪推一次 PR，推同一個就好」「期間你建議的決定就好」。第二十五輪補讀第二十四輪差距最小、點名原文有開放全文的後備題。

## Definition of done

- [ ] 新核心批次與 `reviews/material-20261111-round25.{json,md}` 入庫，快照照前例，`cli.mjs check` PASS，pool 與 catalog 測試全過；推到 PR #2080。

## Steps

- [ ] 八位作者（F105–F112）各補一題：M2-T1 生物發光、F100-T1 走跑轉換、F95-T1 酸種、F99-T1 地磁、F89-T1 費氏葉序、F94-T1 動物數數、F92-T1 人類回聲定位、F97-T1 暴雨溪水。
- [ ] 非作者覆核（V113–V120）。
- [ ] 整合、更新 README 與報告。

## How to verify

`node tools/video/so-thats-why/pool/cli.mjs check`；`node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`。

## Notes

說明在工作階段暫存區 stw25/BRIEF.md、REVIEW-BRIEF.md。PR #2080 的自動合併先關閉，第二十六輪推完再開。
