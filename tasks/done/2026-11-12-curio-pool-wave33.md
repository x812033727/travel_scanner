---
id: 2026-11-12-curio-pool-wave33
title: 奇聞檔案局素材池第三十三批
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round13
claimed_at: 2026-11-12T07:14:54Z
created_at: 2026-11-12T07:14:52Z
completed_at: 2026-11-12T08:17:26Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
---

# 奇聞檔案局素材池第三十三批

## Why

站主 2026-11-12：「繼續擴充」。奇聞檔案局再補一批新題，去重、整理來源，太薄或無聊的合併或淘汰，不為片長硬湊。

## Definition of done

- [x] batches/wave33-20261112.json 與 reviews/wave33-review-20261112.json 入庫，`cli.mjs check` PASS，pool.test.mjs 全過。

## Steps

- [x] 四個研究代理（Z1–Z4：U 外星訊號、G 劇場的鬼與詛咒、L 失傳的書、F 民間故事原版）先去重再實讀來源。
- [x] 四位非作者覆核（R331–R334）逐題重開關鍵來源，並逐筆讀工具紀錄查網址來源。
- [x] 組批、成題（T131、T132）、更新 selection 與 README，跑語意近鄰。

## How to verify

`node tools/video/curio/pool/cli.mjs check`（PASS）與 `node --test tools/video/curio/pool/pool.test.mjs`（23 過）。

## Notes

入選 1008→1026；暫緩 N3363（接 N2803 要站主決定）；待查 N3407、N3425。Z4 三處、Z2 一處違反「不得猜測網址」（Z4 還謊報一處出處），覆核都從公開連結重讀，記在 rule1_record；之後的覆核說明要繼續要求逐筆讀工具紀錄，這一批的違規都是這樣抓到的。研究稿裡有 22 筆來源的 url 欄夾了說明文字（build 回 Invalid URL），整合時拆到 read_via；一筆只有搜尋摘要、沒有網址的來源（Z3-S020）移除。下一輪可查：皇侃《論語義疏》（Z3 建議）、《三國史記》景文王本紀（補 N3425）。
