---
id: 2026-11-19-extend-curio-wave-91-and-so
title: Extend Curio wave 91 and So Thats Why wave 120 on PR 2177
status: done
priority: P2
area: docs
owner: codex-pools
claimed_at: 2026-11-19T10:07:12Z
created_at: 2026-11-19T10:07:12Z
completed_at: 2026-11-19T10:38:55Z
branch: codex/curio86-why115
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - docs/videos/so-thats-why/pool
  - apps/api/app/video_pools/data
  - apps/api/app/video_backup/target.py
---

# Extend Curio wave 91 and So Thats Why wave 120 on PR 2177

## Why

在同一個 PR #2177 擴充奇聞與原來如此題庫。

## Definition of done

- [x] 新題通過雙池查重與來源覆核。
- [x] 單集及長題有獨立評分、改寫紀錄與採用依據。

## Steps

- [x] 核對分支及原 PR。
- [x] 整合兩批選題、更新對應的生成檔與後台資料。
- [x] 驗證新增內容並推到既有分支。

## Result

奇聞第 91 批新增 5 個單集，入選 1,820 題。《安妮日記》完成最後一輪版別查核與重新盲評。原來如此第 120 批新增 12 張日常物件、6 張地圖判讀及 18 張飲料容器素材，入選 7,288 張。G763 呈現新加坡 2026 年過渡期的押金算例，兩次改寫複評分別為 5.99、4.94，六章研究稿保留作後備，全池可成題長片 107 組。

## How to verify

兩池 build 與 check、後台資料比對、網頁搜尋和長題篩選、相關 Node 與 Python 測試。
