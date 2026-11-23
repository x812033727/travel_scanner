---
id: 2026-11-12-curio-pool-wave34
title: 奇聞檔案局素材池第三十四批
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round14
claimed_at: 2026-11-12T08:18:00Z
created_at: 2026-11-12T08:17:59Z
completed_at: 2026-11-12T09:06:55Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
---

# 奇聞檔案局素材池第三十四批

## Why

站主 2026-11-12：「繼續擴充」「持續擴充」。奇聞檔案局再補一批新題，去重、整理來源，太薄或無聊的合併或淘汰，不為片長硬湊。

## Definition of done

- [x] batches/wave34-20261112.json 與 reviews/wave34-review-20261112.json 入庫，`cli.mjs check` PASS，pool.test.mjs 全過。

## Steps

- [x] 四個研究代理（A1–A4：U 1950 年前天上的不明物、G 東亞鬼故事原始紀錄、P 沒發生的末日、M 天降異物）先去重再實讀來源。
- [x] 四位非作者覆核（R341–R344）逐題重開關鍵來源，並逐筆讀工具紀錄查網址來源。
- [x] 組批、更新 selection 與 README，跑語意近鄰（本批沒有新題案）。

## How to verify

`node tools/video/curio/pool/cli.mjs check`（PASS）與 `node --test tools/video/curio/pool/pool.test.mjs`（23 過）。

## Notes

入選 1026→1038；暫緩 N3504；待查 N3441、N3444、N3445、N3465；退回 N3483、N3484、N3485（三題各有補進既有題的建議：P12 或 N3323 的一句、N2402 第三轉折、M17 的一句）。把研究代理的工具紀錄路徑交給覆核後，覆核能逐筆對網址，這一批抓到 A3 改 URL 參數與兩次拼 OCR 檔名。日本古典原文可走 NDL Lab 公開 API（R342 確認為公開文件記載）。可成題組合候選：N3443＋N2805（約 12.5 分鐘），要寫題案時再排章節。
