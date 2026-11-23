---
id: 2026-11-12-curio-pool-wave46
title: 奇聞檔案局素材池第四十六批
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round20
claimed_at: 2026-11-12T13:57:00Z
created_at: 2026-11-12T13:56:52Z
completed_at: 2026-11-12T14:59:48Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
---

# 奇聞檔案局素材池第四十六批

## Why

站主 2026-11-12：「持續擴充」。奇聞檔案局再補一批新題，去重、整理來源，太薄或無聊的合併或淘汰，不為片長硬湊。

## Definition of done

- [x] batches/wave46-20261112.json 與 reviews/wave46-review-20261112.json 入庫，`cli.mjs check` PASS，pool.test.mjs 全過。

## Steps

- [x] 八個研究代理（ZB1–ZB8：H 翻譯與抄寫錯誤、G 燈塔的鬼、M 植物怪聞、S 自動機騙局、F 南亞民間故事、P 手相與算命「說中」、L 秘密地道、U 地震前後的怪光怪聲）先去重再實讀來源，候選號段 N5121–N5280。
- [x] 八位非作者覆核（R461–R468）逐題重開關鍵來源，並逐筆讀工具紀錄。
- [x] 組批、成題（T155–T159）、更新 selection 與 README，跑語意近鄰。

## How to verify

`node tools/video/curio/pool/cli.mjs check` 與 `node --test tools/video/curio/pool/pool.test.mjs`。

## Notes

入選 1355→1384；暫緩 N5164、N5204、N5225；待查 7 題；沒有退回。網址規則：ZB2 從一頁的 301 得知新主機後自己把另一頁換主機抓、read_via 不實（覆核已循合法路徑重取）；ZB5 兩筆 read_via 被建置腳本誤套。wave42 以「與 N703 重複」退回 Helike 動物的判斷解除。
