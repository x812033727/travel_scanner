---
id: 2026-11-19-extend-curio-wave-95-and-so
title: Extend Curio wave 95 and So Thats Why wave 124 on PR 2177
status: done
priority: P2
area: docs
owner: codex-pools
claimed_at: 2026-11-19T12:37:56Z
created_at: 2026-11-19T12:37:55Z
completed_at: 2026-11-19T13:03:18Z
branch: codex/curio86-why115
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - docs/videos/so-thats-why/pool
  - apps/api/app/video_pools/data
  - apps/api/app/video_backup/target.py
---

# Extend Curio wave 95 and So Thats Why wave 124 on PR 2177

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

## 結果

奇聞新增 5 個單集，入選 1,840 題。原來如此新增 35 張素材，入選 7,433 題。G767〈成田機場寄同一個小包，晚上九點放、凌晨一點拿，為什麼會是300、400或800日圓？〉，採用稿併分 7.34，列為可成題長片。原來如此共有 111 組可成題長片。

兩池與管理後台資料包通過檢查，453 項相關測試通過。以桌面及手機視窗逐一搜尋 40 張新題卡，並確認 G767 篩選結果對應 16 張研究素材。
