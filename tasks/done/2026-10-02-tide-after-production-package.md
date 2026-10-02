---
id: 2026-10-02-tide-after-production-package
title: After the Tide production screenplay and department handoff
status: done
priority: P1
area: docs
owner: codex
claimed_at: 2026-10-02T15:17:43Z
created_at: 2026-10-02T15:17:43Z
completed_at: 2026-10-02T17:12:59Z
branch: codex/tide-after-third-review
depends_on: []
scope:
  - docs/videos/series-plans/tide-after-20260930
---

# After the Tide production screenplay and department handoff

## Why

《潮退之後》已有四十集細綱，但缺少可讀演的逐場對白與一致的製作拆表。使用者要求直接優化到可製作，因此延續 PR #1134，交付全季對白稿與前製交接，不把企劃或標註分鐘當作完成拍攝。

## Definition of done

- [x] 四十集均有完整 Fountain 分場對白稿，沿用人物、揭曉順序與結尾。
- [x] 故事日期、角色、場景及關鍵物件採共同編號，可由劇本重建製作表。
- [x] 導演、製片、演員、美術、攝影錄音及後製有具體交接文件與首集執行方案。
- [x] 自動核對及跨集人工審讀完成；讀本實測、實際報價與現場簽認誠實標示為前製工作。

## Steps

- [x] 建立共同製作規格、全季日曆及角色／場景／道具 registry。
- [x] 完成四十集分場對白，核對容量、節奏、角色知情與物件交付。
- [x] 產生逐場、角色、場景、道具與時長拆表及可列印讀本。
- [x] 補齊各組執行方案、成本橋接、首集方案與讀本鎖稿流程。
- [x] 通過檢查、任務結案並更新既有草稿 PR。

## How to verify

`python3 docs/videos/series-plans/tide-after-20260930/production/build_package.py --check`、`git diff --check`、`npm run check:tasks`。另以分篇審讀報告及 `production/reviews/final-review.md` 記錄非機械式檢查。

## Notes

- 持續使用 `codex/tide-after-third-review` 與草稿 PR #1134；認領前碰撞檢查無其他進行中同範圍任務。
- 維持真人四十集、每集約一小時；沒有切換為 AI 漫劇或縮為樣片。
- 劇本計畫秒數與容量是估算，讀本及實際演出時長尚未量測；未選角、未採購、未代為發布。

- 交付40集、969場、243,336可發聲漢字；逐集計畫56.33–61.67分鐘，時長均未實測。
- 已完成跨作者審读、28項後半季／製作交接問題與前半季／第二篇逐項回修；審稿明確區分自查與獨立審讀。
- 校驗器可重建13份索引／CSV／HTML／JSON，並驗證旁白集次、末集唯一口白、場號、故事日期及已登錄具詞角色出場資料。
- 製作報價表13類基準合計NT$340,000,000，供應商與報價欄空白；11景塊合計230工作日，夜班已包含。
- PDF在儲存庫外`/workspace/artifacts/tide-after-production-v1`輸出；全季及四個十集分冊附章節書籤，另有道具校樣。ZIP供離線交接，未將媒體二進位提交儲存庫。
- 末輪碰撞檢查：該scope只見本票與既有草稿PR1134，遠端主幹仍為較早企劃版。
- 實際讀本、勘景、顧問、選角及供應商回填另列2026-10-02-tide-after-table-read-lock，沒有把計畫資料寫成實測或採購承諾。
- 最終驗證：重建與`--check`通過、40集／969場CSV交叉核對通過、本地Markdown連結無缺檔、任務檢查通過（1302檔；僅既有其他scope警告）。暫存差異格式問題已移除多餘檔尾空行。
