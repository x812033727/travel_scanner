---
id: 2026-11-19-extend-curio-wave-96-and-so
title: Extend Curio wave 96 and So Thats Why wave 125 on PR 2177
status: done
priority: P2
area: docs
owner: codex-pools
claimed_at: 2026-11-19T13:10:45Z
created_at: 2026-11-19T13:10:44Z
completed_at: 2026-11-19T13:37:47Z
branch: codex/curio86-why115
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - docs/videos/so-thats-why/pool
  - apps/api/app/video_pools/data
  - apps/api/app/video_backup/target.py
---

# Extend Curio wave 96 and So Thats Why wave 125 on PR 2177

## Why

持續擴充奇聞和原來如此素材池，讓新選題和來源能在既有 PR #2177 一起審閱。

## Definition of done

- [x] 兩池以核心答案查重，留有可回查的來源與退案紀錄。
- [x] 各題依素材厚度分類，長題完成獨立覆核與觀眾複評。

## Steps

- [x] 確認 PR、分支和上一批的入選數。
- [x] 重建兩池、搜尋頁、後台資料與備份分類。
- [x] 驗證桌面和手機搜尋，將本批推到同一個 PR。

## How to verify

執行兩池 build 與 check、後台資料包檢查及相關 Node 與 Python 測試。以兩種視窗尺寸查詢新增題卡和長題，再比對遠端 PR 的最新提交。

## 本批查核

已將主分支 #2181 的奇聞片長規則併入本 PR。史料覆核為五個新選題各估 8–10 分鐘。沖印題使用北村公開網路價目與紙張尺寸試算，並核對しまうま選北村門市取件時的裁切限制。

## 結果

奇聞新增 5 個單集，入選 1,845 題。原來如此新增 36 張素材，入選 7,469 題。G768〈同一張手機合照，各花59日圓印成DSC和L，為什麼一張預覽留得住帽尖，一張卻削掉？〉，採用稿併分 7.91，列為可成題長片。原來如此共有 112 組可成題長片。

兩池與管理後台資料包通過檢查，453 項相關測試通過。以桌面及手機視窗逐一搜尋 41 張新題卡，並確認 G768 篩選結果對應 17 張研究素材。
