---
id: 2026-11-12-stw-pool-round21
title: 原來如此素材池第二十一輪
status: in-progress
priority: P2
area: docs
owner: claude-cloud-pool-round20
claimed_at: 2026-11-12T14:44:56Z
created_at: 2026-11-12T14:44:55Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/so-thats-why/pool
---

# 原來如此素材池第二十一輪

## Why

站主 2026-11-12：「原來如此要繼續擴充」。從零研究的新長題連四輪都沒過覆核；這一輪改成只補讀第二十輪覆核在 `still_missing` 點名的原文，看第二十輪留下的十二題能不能過 8.5 分鐘與兩個轉折。

## Definition of done

- [ ] 新核心批次與 `reviews/material-20261111-round21.{json,md}` 入庫，快照 checkpoint 與 VALIDATION 照前例建立，`cli.mjs check` PASS，pool 與 catalog 測試全過。

## Steps

- [ ] 十二位作者（F42–F53）各補一題：C14-01 天空偏振、C17-02 鸚鵡對拍、C17-01 名琴、C14-02 夜光雲、C16-01 摩擦起電正負、C19-02 海中發光、C15-01 啄木鳥、C15-02 象鼻、C18-01 發光菇、C19-01 海色、C18-02 植物發熱、C16-02 撕膠帶。
- [ ] 十二位非作者覆核（V45–V56）重抓來源、逐筆讀工具紀錄、重算片長。
- [ ] 整合、更新 README 與報告。

## How to verify

`node tools/video/so-thats-why/pool/cli.mjs check`；`node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`。

## Notes

研究進行中（owner claude-cloud-pool-round20）。
