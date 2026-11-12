---
id: 2026-11-12-curio-pool-wave47
title: 奇聞檔案局素材池第四十七批
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round20
claimed_at: 2026-11-12T14:17:34Z
created_at: 2026-11-12T14:17:33Z
completed_at: 2026-11-12T15:21:00Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
---

# 奇聞檔案局素材池第四十七批

## Why

站主 2026-11-12：「持續擴充」。奇聞檔案局再補一批新題，去重、整理來源，太薄或無聊的合併或淘汰，不為片長硬湊。

## Definition of done

- [x] batches/wave47-20261112.json 與 reviews/wave47-review-20261112.json 入庫，`cli.mjs check` PASS，pool.test.mjs 全過。

## Steps

- [x] 七個研究代理（ZC1–ZC7：H 曆法換算的誤傳、G 大學與圖書館的鬼、M 動物最早的離譜描述、S 不存在的元素與射線、F 斯拉夫與東歐民間故事、L 名建築的誤傳由來、U 歷史流星雨與火球）先去重再實讀來源，候選號段 N5281–N5420。
- [x] 七位非作者覆核（R471–R477）逐題重開關鍵來源，並逐筆讀工具紀錄。
- [x] 組批、成題（T160–T161）、更新 selection 與 README，跑語意近鄰。

## How to verify

`node tools/video/curio/pool/cli.mjs check` 與 `node --test tools/video/curio/pool/pool.test.mjs`。

## Notes

奇聞檔案局素材池擴充的最後一批（站主：「奇聞到 wave47 結束就收尾」；已開工的 wave48 研究代理停掉、任務檔已移除）。入選 1384→1411；待查 7 題；退回 2 題（N5382 與 N345 重複、N5403 1833 審判日仍屬 wave40 的不收理由）。N5364 克拉科夫號聲要站主決定是否短期內不做。網址規則只有 ZC5 一筆輕微換主機（沒當來源）。
