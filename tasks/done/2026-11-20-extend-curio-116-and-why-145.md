---
id: 2026-11-20-extend-curio-116-and-why-145
title: Extend Curio wave 116 and So Thats Why wave 145 on PR 2177
status: done
priority: P1
area: docs
owner: codex-pr2177-pools
claimed_at: 2026-11-20T03:58:51Z
created_at: 2026-11-20T03:58:44Z
completed_at: 2026-11-20T04:24:45Z
branch: codex/curio86-why115
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - docs/videos/so-thats-why/pool
  - apps/api/app/video_pools/data
  - apps/api/app/video_backup/target.py
---

# Extend Curio wave 116 and So Thats Why wave 145 on PR 2177

## Why

接續 PR #2177 的奇聞第 115 批與原來如此第 144 批。以 #2182 的選題方式追問不同答案，把可以直接核對的原件、觀眾評分與退案理由留在各池。

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

奇聞有 3 題入選，池內由 1,930 增至 1,933 題。入選的是麥旋風換匙後如何攪拌、嬌生急救產品與美國紅十字會的標誌授權、愛迪達為何用菁英賽不能穿來介紹新跑鞋。另有 4 題留作後備，包括迪士尼手環沒電仍能入園卻可能收不到設施照片、蒲公英黃回歸後兩種 Crayola 盒裝的換色差異、珍妮郵票為何從倒印變成正印稀有、馬內酒瓶上的紅三角與英國一號商標。

原來如此新增 28 題，包括 6 張生活器物與規則、7 張染織與織物工藝、15 張棒球出局與得分研究卡。另將第 144 批 K144-0002 併入第 142 批 K142-0005，兩題都解釋 Apple Watch 結束水中鎖定時播音排出揚聲器積水。保留兩批原件與題號對照後，池內淨增 27 題，由 8,110 增至 8,137 題。G788〈雙殺結束、國民隊都往場下走了，為什麼海盜的比分才從三變成四？〉採用稿的模擬觀眾與需求合併評分為 7.85，列為可成題長片。六章共 8 分 10 秒，獨立覆核折算 11.5 條事實，可支撐約 8.6 分鐘。全池可成題長片共 120 組。

兩池共登錄 76 筆來源與 24 筆退案。逐題比對兩池舊案及 #2182 的 89 個候選與 57 筆退案，並將原件覆核、盲評和改稿取捨寫入本批紀錄。兩池搜尋頁與後台資料已重建，桌機和手機各逐題查到 35 張新卡。用 G788 篩選可找到全部 15 張研究卡。相關測試 455 項通過，完整工具測試 3,102 項通過、6 項跳過、0 項失敗。
