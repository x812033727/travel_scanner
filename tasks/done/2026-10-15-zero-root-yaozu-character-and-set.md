---
id: 2026-10-15-zero-root-yaozu-character-and-set
title: Zero-root Yaozu: character and set reference images for episodes 1-10 on Hailuo
status: done
priority: P2
area: docs
owner: claude-opus-5-5-yaozu-refs
claimed_at: 2026-10-15T05:33:54Z
created_at: 2026-10-15T05:33:43Z
completed_at: 2026-10-15T06:28:09Z
branch:
depends_on: []
scope:
  - docs/videos/series-plans/zero-root-yaozu/production
---

# Zero-root Yaozu: character and set reference images for episodes 1-10 on Hailuo

## Why

站主 2026-10-15 同意先拍第一季第一篇章 10 集，並說「好，開始做參考圖」。600 集真人漫劇最大的技術風險是換臉，所以每個首格都要帶同一組參考圖。

## Definition of done

- [x] 第 1–10 集出場的 10 位角色各有定妝照與三視圖，孫二、山魈各一張，四個場景各一張，無水印原檔在影片工作區。
- [x] `production/refs.json` 記下每張的提示詞、作品編號、檔名與 SHA256。

## How to verify

影片工作區 `_series/zero-root-yaozu/refs/index.json` 的 27 個檔案 SHA256 與 `refs.json` 的 results 相同；`ledger.jsonl` 27 列合計 550 點，海螺餘額 24,804 → 24,254。

## Notes

- 定妝照 3:4（20 點）；三視圖 16:9、以定妝照為參考圖（21 點）；場景 16:9。
- 送出時序坑：填完提示詞立刻按「創建」，網站送出的是上一則提示詞；要等 1.5 秒再按，並比對新卡片文字。第一批因此錯位一格，多出一張胡奶奶（20 點），孫二出成 16:9。
- 比例晶片要呼叫選項 DIV 的 React onClick 才會切換；頁面重載會回 21:9、參考圖清空。
- 無水印網址在詳情頁的 React props：`targetDetailItem.videoAsset.videoURLs.downloadURLWithoutWatermark`，同步讀取即可，同一分頁連續換頁沒卡（用 setTimeout 輪詢就會卡）。檔案所在的小時資料夾可能跳到下一小時。
- 之後要補：胡奶奶本相（約第 41 集）、五位妖祖真身（約第 51 集）、第 11 集以後的新角色與場景；山魈若要正面打鬥再重畫。
