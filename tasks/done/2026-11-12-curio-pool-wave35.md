---
id: 2026-11-12-curio-pool-wave35
title: 奇聞檔案局素材池第三十五批
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round15
claimed_at: 2026-11-12T09:07:27Z
created_at: 2026-11-12T09:07:26Z
completed_at: 2026-11-12T10:03:33Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
---

# 奇聞檔案局素材池第三十五批

## Why

站主 2026-11-12：「持續擴充」。奇聞檔案局再補一批新題，去重、整理來源，太薄或無聊的合併或淘汰，不為片長硬湊。

## Definition of done

- [x] batches/wave35-20261112.json 與 reviews/wave35-review-20261112.json 入庫，`cli.mjs check` PASS，pool.test.mjs 全過。

## Steps

- [x] 四個研究代理（B1–B4：U 古畫裡的 UFO、P 被說成預言的舊書、F 中東與非洲故事原版、M 怪聲怪光）先去重再實讀來源。
- [x] 四位非作者覆核（R351–R354）逐題重開關鍵來源，並逐筆讀工具紀錄。
- [x] 組批、成題（T133）、更新 selection 與 README，跑語意近鄰。

## How to verify

`node tools/video/curio/pool/cli.mjs check`（PASS）與 `node --test tools/video/curio/pool/pool.test.mjs`（23 過）。

## Notes

入選 1038→1050；暫緩 N3524、N3542、N3545（N3545 接 N1103 要站主決定）；待查 N3523、N3525、N3526、N3544、N3584、N3585。這是第一批四位研究代理都沒有違反網址規則；說明檔列出前幾批的具體違規型態、覆核拿到工具紀錄逐筆查，看起來有效。古畫 UFO 這個方向的流傳說法大多只經 Cuoghi 一人轉引，之後同方向要先找第二個可讀出處再收。
