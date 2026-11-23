---
id: 2026-11-19-extend-curio-wave-108-and-so
title: Extend Curio wave 108 and So Thats Why wave 137 on PR 2177
status: done
priority: P2
area: docs
owner: codex-pools
claimed_at: 2026-11-19T23:04:57Z
created_at: 2026-11-19T23:04:33Z
completed_at: 2026-11-19T23:30:38Z
branch: codex/curio86-why115
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - docs/videos/so-thats-why/pool
  - apps/api/app/video_pools/data
  - apps/api/app/video_backup/target.py
---

# Extend Curio wave 108 and So Thats Why wave 137 on PR 2177

## Why

依站主新指示，從 PR #2182 的黑貓裂變法挑選種子，以新的一手證據擴充兩池。每題辨認新答案與既有素材、參考批次的差別。

## Definition of done

- [x] 兩池按核心答案查重，記錄種子、裂變方式、一手出處與退案。
- [x] 商業題經需求四問、覆核與盲評篩選，長題依素材厚度及改寫複評分類。

## Steps

- [x] 重建兩池、搜尋頁、後台資料與備份分類。
- [x] 核對桌面及手機逐題搜尋，執行相關測試與完整工具測試。

## How to verify

執行兩池及管理後台資料包的 build、check，執行 API、工具、影片文件測試，再核對本批提交與 PR #2177 的遠端 head。

## 認領說明

片長任務仍列為 review；對應的 PR #2181 已合併，提交 c9ac6676e 已在本分支，因此本批使用 --force 認領。

## 結果

奇聞新增 4 個單集，入選 1,902 題。原來如此新增 36 張素材，入選 7,909 題。G780〈鈔票只剩半張，還值一半的錢嗎？〉，採用稿併分 8.06，列為後備長片。原來如此共有 115 組可成題長片。

兩池與管理後台資料包通過檢查，455 項相關測試通過。完整工具測試另有 3,102 項通過，6 項跳過，沒有失敗。以桌面及手機視窗逐一搜尋 41 張新題卡，並確認 G780 篩選結果對應 18 張研究素材。
