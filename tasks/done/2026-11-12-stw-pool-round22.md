---
id: 2026-11-12-stw-pool-round22
title: 原來如此素材池第二十二輪
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round20
claimed_at: 2026-11-12T15:14:42Z
created_at: 2026-11-12T15:14:41Z
completed_at: 2026-11-12T15:30:40Z
branch:
depends_on: []
scope:
  - docs/videos/so-thats-why/pool
---

# 原來如此素材池第二十二輪

## Why

站主 2026-11-12：「原來如此就一直持續審下去」。補讀第十六到十九輪留下、離門檻最近的八題後備組題。

## Definition of done

- [x] 第七十二批（wave72-physics／food／life／human）與 `reviews/material-20261111-round22.{json,md}` 入庫，checkpoint-4299 與 VALIDATION-4299 照前例，`cli.mjs check` PASS，pool 與 catalog 測試全過。

## Steps

- [x] 八位作者（F54–F61）：C10-01 冰為什麼滑、C12-01 冷凍肉、C13-01 鳥蛋、C13-02 蝸牛、C11-01 迷路繞圈、C9-01 浴室唱歌、C11-02 鴿子點頭、C12-02 冷藏蔬果。
- [x] 八位非作者覆核（V57–V64）。
- [x] 整合、更新 README 與報告。

## How to verify

`node tools/video/so-thats-why/pool/cli.mjs check`；`node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`。

## Notes

入選 4,299→4,321（23 個提案收 22、退回 1）；八題都仍後備，可成題長題維持 86 組。冰為什麼滑作者自判 8.56 分可成題，覆核 V57 重算 8.43 分改回後備（−0.5 °C 那格滑度是公式算回的）；冷凍肉 8.30 分。八位作者沒有違反網址規則。
