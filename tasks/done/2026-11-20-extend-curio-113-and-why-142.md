---
id: 2026-11-20-extend-curio-113-and-why-142
title: Extend Curio wave 113 and So Thats Why wave 142 on PR 2177
status: done
priority: P1
area: docs
owner: codex-pr2177-pools
claimed_at: 2026-11-20T02:16:13Z
created_at: 2026-11-20T02:16:06Z
completed_at: 2026-11-20T02:42:32Z
branch: codex/curio86-why115
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - docs/videos/so-thats-why/pool
  - apps/api/app/video_pools/data
  - apps/api/app/video_backup/target.py
---

# Extend Curio wave 113 and So Thats Why wave 142 on PR 2177

## Why

接續 PR #2177 的奇聞第 112 批與原來如此第 141 批。以 #2182 的選題方式追問不同答案，把可以直接核對的原件、觀眾評分與退案理由留在各池。

## Definition of done

- [x] 逐題核對一手文件、來源限制與跨池近題，登錄入選及退案。
- [x] 完成獨立覆核與匿名評分，依素材厚度、需求和可拍性決定長題狀態。

## Steps

- [x] 重建兩池公開搜尋頁與後台，逐題驗證桌面、手機與長題篩選。
- [x] 執行兩池及後台資料檢查、相關測試與完整工具測試。

## How to verify

執行兩池 CLI 及後台資料包的 check、npm run test:docs-videos、npm run test:tools 與影片池、備份相關 API 測試。提交後比對 GitHub PR 與分支的 SHA。

## Notes

片長規則的舊票仍標示 review。對應 PR #2181 已合併，且其合併提交 c9ac6676e 已包含在本輪起點，故使用 --force 認領本票。

## 結果

奇聞有 3 題入選，池內由 1,918 增至 1,921 題。入選的是Sony 初代 Walkman 的通話鍵、菲律賓百事 349 瓶蓋案、美國自由女神郵票的權利金。另有 4 題後備：石英潛水錶的兩秒一跳、新可樂與經典配方並售、亞馬遜一鍵下單案、瑞士三角巧克力的產地標示。

原來如此增加 27 題，由 8,029 增至 8,056 題，包括7 張生活器物、6 張玻璃工藝、14 張馬拉松丈量研究卡。G785〈手錶報完全馬，拱門還在轉角後。把你跑的路攤開，哪一段多了？〉採用稿的模擬觀眾與需求併分為 6.55，列為可成題長片。六章共 8 分 30 秒，獨立覆核折算 11.5 條事實，可支撐約 8.6 分鐘。全池可成題長片共 119 組。

兩池共登錄 76 筆來源與 21 筆退案。兩池搜尋頁與後台資料已重建，桌機和手機各逐題查到 34 張新卡。用 G785 篩選可找到全部 14 張研究卡。相關測試 455 項通過，完整工具測試 3,102 項通過、6 項跳過、0 項失敗。
