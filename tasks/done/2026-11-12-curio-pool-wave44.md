---
id: 2026-11-12-curio-pool-wave44
title: 奇聞檔案局素材池第四十四批
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round20
claimed_at: 2026-11-12T13:10:48Z
created_at: 2026-11-12T13:10:48Z
completed_at: 2026-11-12T14:32:46Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
---

# 奇聞檔案局素材池第四十四批

## Why

站主 2026-11-12：「持續擴充」。奇聞檔案局再補一批新題，去重、整理來源，太薄或無聊的合併或淘汰，不為片長硬湊。

## Definition of done

- [x] batches/wave44-20261112.json 與 reviews/wave44-review-20261112.json 入庫，`cli.mjs check` PASS，pool.test.mjs 全過。

## Steps

- [x] 八個研究代理（S1–S8：H 國王其實沒死、S 科學發現的意外、G 幽靈船、P 天氣預兆、L 美洲的失落殖民、F 太平洋民間故事、U 彗星與日月食凶兆、M 昆蟲奇災）先去重再實讀來源。
- [x] 八位非作者覆核（R441–R448）逐題重開關鍵來源，並逐筆讀工具紀錄。
- [x] 組批、成題（T146–T150）、更新 selection 與 README，跑語意近鄰（2 組字面近鄰判為不同題）。

## How to verify

`node tools/video/curio/pool/cli.mjs check`（PASS）與 `node --test tools/video/curio/pool/pool.test.mjs`（23 過）。

## Notes

入選 1297→1329；暫緩 N4842（兄弟題待查）、N4943（N2685 已在 T118）；待查 N4843、N4884、N4907、N4926；退回 N4906（今日族群認同）。網址規則：S3 夾了空 User-Agent 打向不存在網域的 curl 三次（沒取得內容）、S8 自加結尾斜線；S1 兩處出處不實已更正。編輯裁定：動物官司兩題照 R448 的界線收，總論題仍不收。
