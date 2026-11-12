---
id: 2026-11-12-curio-pool-wave47
title: 奇聞檔案局素材池第四十七批
status: in-progress
priority: P2
area: docs
owner: claude-cloud-pool-round20
claimed_at: 2026-11-12T14:17:34Z
created_at: 2026-11-12T14:17:33Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
---

# 奇聞檔案局素材池第四十七批

## Why

站主 2026-11-12：「持續擴充」。奇聞檔案局再補一批新題，去重、整理來源，太薄或無聊的合併或淘汰，不為片長硬湊。

## Definition of done

- [ ] batches/wave47-20261112.json 與 reviews/wave47-review-20261112.json 入庫，`cli.mjs check` PASS，pool.test.mjs 全過。

## Steps

- [ ] 七個研究代理（ZC1–ZC7：H 曆法換算的誤傳、G 大學與圖書館的鬼、M 動物最早的離譜描述、S 不存在的元素與射線、F 斯拉夫與東歐民間故事、L 名建築的誤傳由來、U 歷史流星雨與火球）先去重再實讀來源，候選號段 N5281–N5420。
- [ ] 七位非作者覆核（R471–R477）逐題重開關鍵來源，並逐筆讀工具紀錄。
- [ ] 組批、成題、更新 selection 與 README，跑語意近鄰。

## How to verify

`node tools/video/curio/pool/cli.mjs check` 與 `node --test tools/video/curio/pool/pool.test.mjs`。

## Notes

研究進行中（owner claude-cloud-pool-round20）。
