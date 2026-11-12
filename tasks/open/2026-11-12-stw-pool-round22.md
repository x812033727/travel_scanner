---
id: 2026-11-12-stw-pool-round22
title: 原來如此素材池第二十二輪
status: in-progress
priority: P2
area: docs
owner: claude-cloud-pool-round20
claimed_at: 2026-11-12T15:14:42Z
created_at: 2026-11-12T15:14:41Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/so-thats-why/pool
---

# 原來如此素材池第二十二輪

## Why

站主 2026-11-12：「原來如此就一直持續審下去」。補讀第十六到十九輪留下、離門檻最近的八題後備組題。

## Definition of done

- [ ] 第七十二批與 `reviews/material-20261111-round22.{json,md}` 入庫，快照照前例，`cli.mjs check` PASS，pool 與 catalog 測試全過。

## Steps

- [ ] 八位作者（F54–F61）：C10-01 冰為什麼滑、C12-01 冷凍肉、C13-01 鳥蛋、C13-02 蝸牛、C11-01 迷路繞圈、C9-01 浴室唱歌、C11-02 鴿子點頭、C12-02 冷藏蔬果。
- [ ] 八位非作者覆核（V57–V64）。
- [ ] 整合、更新 README 與報告。

## How to verify

`node tools/video/so-thats-why/pool/cli.mjs check`；`node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`。

## Notes

研究與覆核進行中（owner claude-cloud-pool-round20）；作者 F54 自判冰為什麼滑剛好過線（8.56 分），待覆核。
