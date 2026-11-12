---
id: 2026-11-11-curio-pool-wave25
title: 奇聞檔案局素材池第二十五批
status: done
priority: P2
area: docs
owner: claude-opus-cloud-channel-review
claimed_at: 2026-11-11T15:32:51Z
created_at: 2026-11-11T15:32:43Z
completed_at: 2026-11-11T16:24:28Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
---

# 奇聞檔案局素材池第二十五批

## Why

站主 2026-11-11 再次說「繼續擴充池」：奇聞檔案局再補一批新題，去重、整理來源，太薄或無聊的合併或淘汰，不為片長硬湊。

## Definition of done

- [x] batches/wave25-20261111.json 與 reviews/wave25-review-20261111.json 入庫，`cli.mjs check` PASS，pool.test.mjs 全過。

## Steps

- [x] 四個研究代理（H1–H4：亞非中東的 G、F 習俗源流、H 文物來歷、L／M 太平洋與極地）先去重再實讀來源。
- [x] 四位非作者覆核逐題重開關鍵來源，改動寫成完整欄位。
- [x] 組批、成題、更新 selection 與 README，跑語意近鄰。

## How to verify

`node tools/video/curio/pool/cli.mjs check`（PASS）與 `node --test tools/video/curio/pool/pool.test.mjs`（23 過）。

## Notes

入選 851→874（22 新題＋G11 從 Shorts 移回），新題案 T119（N2725＋G11）；退回 N2782 Pepys 島（福克蘭主權爭議）。素材池搜尋 "Flying Dutchman" 找不到 G11，用中文關鍵字才找到：去重要多種寫法並 grep。
