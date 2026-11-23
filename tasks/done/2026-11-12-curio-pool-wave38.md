---
id: 2026-11-12-curio-pool-wave38
title: 奇聞檔案局素材池第三十八批
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round19
claimed_at: 2026-11-12T11:22:54Z
created_at: 2026-11-12T11:22:37Z
completed_at: 2026-11-12T12:17:15Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
---

# 奇聞檔案局素材池第三十八批

## Why

站主 2026-11-12：「持續擴充」。奇聞檔案局再補一批新題，去重、整理來源，太薄或無聊的合併或淘汰，不為片長硬湊。

## Definition of done

- [x] batches/wave38-20261112.json 與 reviews/wave38-review-20261112.json 入庫，`cli.mjs check` PASS，pool.test.mjs 全過。

## Steps

- [x] 八個研究代理（E1–E8：未解讀文字、名人鬼故事、通靈板與降靈調查、動物觀察紀錄、日韓民間故事原版、冒名者、小東西引起的戰爭、科學發現軼事）先去重再實讀來源。
- [x] 八位非作者覆核（R381–R388）逐題重開關鍵來源，並逐筆讀工具紀錄。
- [x] 組批、成題（T135）、改排 T20、更新 selection 與 README，跑語意近鄰。

## How to verify

`node tools/video/curio/pool/cli.mjs check`（PASS）與 `node --test tools/video/curio/pool/pool.test.mjs`（23 過）。

## Notes

入選 1081→1120；暫緩 N3826、N3904、N3905（都要站主決定接既有題或轉 Shorts）；待查 N3764、N3806。兩位研究代理違反網址規則（E5 自填 NDL 相鄰コマ號、E6 自換主機名），都沒有內容依賴違規抓取，記在覆核的 rule1_record；下一批 BRIEF 要把「換主機名」與「自填相鄰頁碼」寫進硬性規定（wave39、wave40 的派工訊息已寫）。
