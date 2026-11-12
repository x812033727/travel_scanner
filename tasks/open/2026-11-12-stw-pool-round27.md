---
id: 2026-11-12-stw-pool-round27
title: 原來如此素材池第二十七輪：新領域從零研究新長題（先查合著網）
status: in-progress
priority: P2
area: docs
owner: claude-cloud-pool-round20
claimed_at: 2026-11-12T22:43:36Z
created_at: 2026-11-12T22:43:31Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/so-thats-why/pool
---

# 原來如此素材池第二十七輪：新領域從零研究新長題（先查合著網）

## Why

站主 2026-11-12：「再繼續跑原來如此再跑五輪」（第二十七到三十一輪），沿用「每跑完一輪推一次 PR」「期間你建議的決定就好」「品質為主」。PR #2080 已合併，這五輪推到一個新的 PR。第二十七輪從零研究新長題；第二十四輪新題全部後備的主因是作者漏查共同作者，所以這輪要求動筆前先用 Europe PMC 作者查詢確認至少四個互不合著的研究網。

## Definition of done

- [ ] 新核心批次與 `reviews/material-20261111-round27.{json,md}` 入庫，快照照前例，`cli.mjs check` PASS，pool 與 catalog 測試全過；推到新 PR。

## Steps

- [ ] 十六位作者（F120–F135）各在一個新領域從零研究一個新長題：動物建築、蜘蛛絲、寄生操控、植物溝通與菌根網、古生物、火山、海洋運動、球類物理、嗅覺、動物睡眠、生物時鐘、冰的物理、結構與橋、動物色覺、細菌集體行為、植物化學武器。
- [ ] 非作者覆核（V140 起，一位作者一位覆核）。
- [ ] 整合、更新 README 與報告。

## How to verify

`node tools/video/so-thats-why/pool/cli.mjs check`；`node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`。

## Notes

說明在工作階段暫存區 stw27/BRIEF.md、REVIEW-BRIEF.md。
