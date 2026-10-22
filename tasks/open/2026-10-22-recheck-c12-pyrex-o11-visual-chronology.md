---
id: 2026-10-22-recheck-c12-pyrex-o11-visual-chronology
title: Recheck C12 Pyrex O11 visual chronology
status: review
priority: P1
area: docs
owner: codex-c12-source-review
claimed_at: 2026-10-22T15:18:35Z
created_at: 2026-10-22T15:18:23Z
completed_at:
branch: codex/brand-story-pyrex-c12-script
depends_on: []
scope:
  - docs/videos/story-everyday-pyrex-c12-script/reviews/independent-visual-sequence-recheck.md
---

# Recheck C12 Pyrex O11 visual chronology

## Why

C12 前一份獨立差異審查只在 O11 畫面時序留下 HOLD；作者已修 O11 與 N14 註記。須對新視覺雜湊和未變劇本留下獨立重核收據，避免把舊 HOLD 或舊 PASS 直接套到新稿。

## Definition of done

- [x] 新視覺 SHA 專用收據核 O11、N14 並判 PASS／HOLD。
- [x] 確認劇本 80 列未改、分鏡只改兩列，67 插圖／13 卡和最多兩張連卡未變。

## Steps

- [x] 直接重開館方 S1 的晚餐／破皿順序。
- [x] 用 Git diff、ID 列及 hash 對位作者修訂。
- [x] 寫收據、推送草稿 PR 並更新 PR 狀態，不進付費。

## How to verify

比較 `git diff b64ded4035ac238f805455c8e3fa6bec932074bf..6a5bdcc569905f41b7bbb15db7a338fa703c2c55`；逐 ID 列比較劇本與逐鏡；`Get-FileHash` 核 script／visual SHA。收據在 `docs/videos/story-everyday-pyrex-c12-script/reviews/independent-visual-sequence-recheck.md`。

## Notes

O11 已去完整陶皿並明列 O12 為較早破裂的回想，N14 改為插圖上短字疊加，兩列 PASS。已知上一個任務的未追蹤 open ghost 刪除遭 `blocked by policy`；未碰該檔，本票隨草稿 PR 標 review。畫面實物、配音、兩位盲讀、站主稿件核准尚未完成。
