---
id: 2026-11-20-extend-curio-112-and-why-141
title: Extend Curio wave 112 and So Thats Why wave 141 on PR 2177
status: done
priority: P1
area: docs
owner: codex-pr2177-pools
claimed_at: 2026-11-20T01:51:39Z
created_at: 2026-11-20T01:51:25Z
completed_at: 2026-11-20T02:12:15Z
branch: codex/curio86-why115
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - docs/videos/so-thats-why/pool
  - apps/api/app/video_pools/data
  - apps/api/app/video_backup/target.py
---

# Extend Curio wave 112 and So Thats Why wave 141 on PR 2177

## Why

接續 PR #2177 的奇聞第 111 批與原來如此第 140 批。以 #2182 的選題方式追問不同答案，把可以直接核對的原件、觀眾評分與退案理由留在各池。

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

奇聞 3 題入選、4 題後備。原來如此新增 27 張素材，長題 G784 採用稿併分 5.91，規劃 8 分 30 秒，列為後備長片。兩池共登錄 73 筆來源與 21 筆退案。

桌面和手機各逐題查到 34 張新卡，G784 可篩出全部 16 張研究卡。相關測試 455 項通過，完整工具測試有 3,102 項通過、6 項跳過、0 項失敗。
