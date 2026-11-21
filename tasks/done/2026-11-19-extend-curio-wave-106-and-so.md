---
id: 2026-11-19-extend-curio-wave-106-and-so
title: Extend Curio wave 106 and So Thats Why wave 135 on PR 2177
status: done
priority: P2
area: docs
owner: codex-pools
claimed_at: 2026-11-19T21:34:05Z
created_at: 2026-11-19T21:34:04Z
completed_at: 2026-11-19T22:03:00Z
branch: codex/curio86-why115
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - docs/videos/so-thats-why/pool
  - apps/api/app/video_pools/data
  - apps/api/app/video_backup/target.py
---

# Extend Curio wave 106 and So Thats Why wave 135 on PR 2177

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

## 認領說明

片長規則的任務仍標為 review，但其 PR #2181 已合併，提交 c9ac6676e 也已進入本分支。因此使用 --force 認領本次素材擴充。

## 結果

奇聞新增 4 個單集，入選 1,893 題。原來如此新增 36 張素材，入選 7,837 題。G778〈你買的一磅冷凍蝦，沖到哪一秒該關水，才知道那一磅有沒有少？〉，採用稿併分 7.18，列為後備長片。原來如此共有 115 組可成題長片。

兩池與管理後台資料包通過檢查，455 項相關測試通過。完整工具測試另有 3,102 項通過，6 項跳過，沒有失敗。以桌面及手機視窗逐一搜尋 40 張新題卡，並確認 G778 篩選結果對應 17 張研究素材。
