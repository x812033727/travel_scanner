---
id: 2026-11-12-curio-pool-wave45
title: 奇聞檔案局素材池第四十五批
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round20
claimed_at: 2026-11-12T13:43:30Z
created_at: 2026-11-12T13:43:29Z
completed_at: 2026-11-12T14:39:52Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
---

# 奇聞檔案局素材池第四十五批

## Why

站主 2026-11-12：「持續擴充」。奇聞檔案局再補一批新題，去重、整理來源，太薄或無聊的合併或淘汰，不為片長硬湊。

## Definition of done

- [x] batches/wave45-20261112.json 與 reviews/wave45-review-20261112.json 入庫，`cli.mjs check` PASS，pool.test.mjs 全過。

## Steps

- [x] 八個研究代理（ZA1–ZA8：H 名人遺言、G 旅店的鬼、S 誰第一個、F 東亞民間故事、L 失落寶藏、P 末日預言、M 騙局怪物、U 天上怪聲）先去重再實讀來源。
- [x] 八位非作者覆核（R451–R458）逐題重開關鍵來源，並逐筆讀工具紀錄。
- [x] 組批、成題（T151–T154）、更新 selection 與 README，跑語意近鄰（2 組字面近鄰判為不同題）。

## How to verify

`node tools/video/curio/pool/cli.mjs check`（PASS）與 `node --test tools/video/curio/pool/pool.test.mjs`（23 過）。

## Notes

入選 1329→1355；暫緩 N4964、N5044（兄弟題待查）；待查 12 題，其中 N5081 要站主同意 wave40 寫的重收條件；退回 N5025（台灣現存月老信仰）、N5103（前提不成立）。網址規則：ZA6 把 loc.gov 搜尋 id 欄的 http 改 https 讀了兩份報紙（覆核已合規重讀），遇驗證頁後又改抓同資料庫另一主機（被擋、沒取得內容）。
