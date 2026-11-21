---
id: 2026-11-20-extend-curio-115-and-why-144
title: Extend Curio wave 115 and So Thats Why wave 144 on PR 2177
status: done
priority: P1
area: docs
owner: codex-pr2177-pools
claimed_at: 2026-11-20T03:26:14Z
created_at: 2026-11-20T03:26:02Z
completed_at: 2026-11-20T03:48:37Z
branch: codex/curio86-why115
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - docs/videos/so-thats-why/pool
  - apps/api/app/video_pools/data
  - apps/api/app/video_backup/target.py
---

# Extend Curio wave 115 and So Thats Why wave 144 on PR 2177

## Why

接續 PR #2177 的奇聞第 114 批與原來如此第 143 批。以 #2182 的選題方式追問不同答案，把可以直接核對的原件、觀眾評分與退案理由留在各池。

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

奇聞有 5 題入選，池內由 1,925 增至 1,930 題。入選的是老寶麗來拍完八張卻顯示還剩兩張、山葉樂器與機車黑白商標上的音叉和字母 M、培樂多如何在商標證書登記氣味、好市多賣的歐米茄錶背小地球與教科書轉售案、Pyrex 量杯上的產地與商品頁承諾。另有 2 題留作後備，包括英國宜家回購書櫃為何要求組好交回、陸戰隊同一個奧斯卡獎的石膏牌與戰後收到的金屬獎像。

原來如此增加 26 題，由 8,084 增至 8,110 題，包括 7 張生活器物與規則、7 張裝飾工藝與器物、12 張莎士比亞《第一對開本》研究卡。G787〈翻開 1623 年《理查二世》第 45 頁，為什麼一本裡國王說了兩行，另一本直接換人進場？〉採用稿的模擬觀眾與需求合併評分為 6.38，列為後備長片。六章共 8 分 20 秒，獨立覆核折算 8 條事實，可支撐約 6 分鐘。全池可成題長片共 119 組。

兩池共登錄 70 筆來源與 23 筆退案。逐題比對兩池舊案及 #2182 的 89 個候選與 57 筆退案，並將原件覆核、盲評和改稿取捨寫入本批紀錄。兩池搜尋頁與後台資料已重建，桌機和手機各逐題查到 33 張新卡。用 G787 篩選可找到全部 12 張研究卡。相關測試 455 項通過，完整工具測試 3,102 項通過、6 項跳過、0 項失敗。
