---
id: 2026-11-19-extend-curio-wave-92-and-so
title: Extend Curio wave 92 and So Thats Why wave 121 on PR 2177
status: done
priority: P2
area: docs
owner: codex-pools
claimed_at: 2026-11-19T10:43:27Z
created_at: 2026-11-19T10:43:27Z
completed_at: 2026-11-19T11:09:08Z
branch: codex/curio86-why115
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - docs/videos/so-thats-why/pool
  - apps/api/app/video_pools/data
  - apps/api/app/video_backup/target.py
---

# Extend Curio wave 92 and So Thats Why wave 121 on PR 2177

## Why

將奇聞與原來如此新一批題卡加進既有 PR #2177。

## Definition of done

- [x] 兩池比對核心答案與退案，逐題核對一手來源。
- [x] 完成獨立評分與改寫判定，記錄各題用途。

## Steps

- [x] 確認既有分支及上一批的題數。
- [x] 整合兩個新批次，重建題庫和管理後台。
- [x] 驗證手機、桌面搜尋及備份對應，更新原 PR。

## How to verify

兩池 build/check、後台資料包驗證、相關 Node 與 Python 測試，以及兩種視窗的搜尋與長題篩選。

## 結果

奇聞第 92 批新增五個 8–9 分鐘單集，入選 1,825 題。原來如此第 121 批新增 36 張素材，入選 7,324 題。G764 對照兩款日本 Panasonic 吹風機的電壓、功率與保證書，六章估 8 分 30 秒。採用稿併分 8.28，改寫複評 6.79，通過可成題門檻，全池共 108 組可成題長片。

兩池與管理後台資料包通過檢查。453 項相關測試通過，並在桌面及手機視窗逐一搜尋 41 張新題卡，確認 G764 可篩出 18 張研究素材。
