---
id: 2026-11-20-extend-curio-111-and-why-140
title: Extend Curio wave 111 and So Thats Why wave 140 on PR 2177
status: done
priority: P1
area: docs
owner: codex-pr2177-pools
claimed_at: 2026-11-20T01:12:53Z
created_at: 2026-11-20T01:12:47Z
completed_at: 2026-11-20T01:37:23Z
branch: codex/curio86-why115
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - docs/videos/so-thats-why/pool
  - apps/api/app/video_pools/data
  - apps/api/app/video_backup/target.py
---

# Extend Curio wave 111 and So Thats Why wave 140 on PR 2177

## Why

接續 PR #2177 的奇聞第 110 批與原來如此第 139 批。以 #2182 的選題方式追問不同答案，把可以直接核對的原件、觀眾評分與退案理由留在各池。

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

奇聞 4 題入選、1 題後備。原來如此新增 28 張素材，長題 G783 採用稿併分 7.34，六章 8 分 35 秒，已列為可成題。兩池共登錄 71 筆來源與 16 筆退案。

桌面和手機各逐題查到 33 張新卡，G783 可篩出全部 15 張研究卡。相關測試 455 項通過；完整工具測試 3,102 項通過、6 項跳過、0 項失敗。
