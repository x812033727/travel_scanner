---
id: 2026-11-12-stw-pool-round26
title: 原來如此素材池第二十六輪：最後一輪補讀最接近門檻的後備題
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round20
claimed_at: 2026-11-12T17:48:26Z
created_at: 2026-11-12T17:48:26Z
completed_at: 2026-11-12T18:17:57Z
branch:
depends_on: []
scope:
  - docs/videos/so-thats-why/pool
---

# 原來如此素材池第二十六輪：最後一輪補讀最接近門檻的後備題

## Why

站主 2026-11-12：「原來如此還可以跑個兩輪」「每跑完一輪推一次 PR，推同一個就好」「期間你建議的決定就好」。第二十六輪是追加的最後一輪，補讀第二十四、二十五輪最接近門檻、點名原文仍有機會讀到的後備題。

## Definition of done

- [x] 新核心批次與 `reviews/material-20261111-round26.{json,md}` 入庫，快照照前例，`cli.mjs check` PASS，pool 與 catalog 測試全過；推到 PR #2080，重開自動合併。

## Steps

- [x] 五位作者（F113–F117）：F89-T1 費氏葉序、F94-T1 動物數數、F92-T1 人類回聲定位、F83-T1 洋裝顏色、M3-T1 無骨肢體。
- [x] 非作者覆核 V121、V124、V125（F114、F115 無提案，沿用上一輪結論）。
- [x] 整合、更新 README 與報告。

## How to verify

`node tools/video/so-thats-why/pool/cli.mjs check`；`node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`。

## Notes

說明在工作階段暫存區 stw26/BRIEF.md、REVIEW-BRIEF.md。結果：第七十六批 12 個核心（4,653 → 4,665）；G629 費氏葉序可成題（11.75 條、8.69 分，任何一條核心都不能刪）；洋裝、動物數數、無骨肢體留後備，人類回聲定位建議收題。站主追加的兩輪做完，之後不再派補讀輪。
