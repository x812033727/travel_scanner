---
id: 2026-09-14-codex-depth-plan-alignment
title: Align Codex deep tutorials with Claude Code plan
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-14T02:23:07Z
completed_at:
branch:
depends_on: []
scope:
  - docs/codex-learning
  - tasks/open/2026-09-14-codex-learning-series.md
---

# Align Codex deep tutorials with Claude Code plan

## Why

使用者要求讀取另一個 Claude Code 教學任務的深入教學計畫，將本系列的深度、課程與驗收對齊，保留原來的五語及截圖要求。

## Definition of done

- [x] 讀取「規劃 Claude Code 教學目錄」已批准計畫及現有作者稿，記錄參考時間與狀態。
- [x] 完成 60 篇課程表、32 篇既有 ID／slug 對應、28 篇新增範圍與三批交付順序。
- [x] 完成作者模板、五篇代表篇、每十篇檢查與五語深入驗收標準。
- [x] 記錄兩邊共用元件和格式衝突，將整合工作放回原實作任務。
- [x] 更新 README 與原任務，明列 0/60 通過新標準，避免草稿完成被誤認為深入完成。

## Steps

- [x] 讀取對方任務 `01a09d8e-a18a-76a1-9952-b525f0210831` 與 `1cff` 工作目錄的相關檔案；沒有改動或送出任務訊息。
- [x] 對齐深度與網站體驗，保留 Codex 自身功能差異及五語範圍。
- [x] 驗證課程順序／ID／slug 唯一性、既有 32 篇映射、文件連結及任務格式。

## How to verify

解析 `docs/codex-learning/depth-plan.md` 的課程表：60 個閱讀位置、ID 1–60 各一次、32 深化＋28 新寫、十單元各六篇；ID 1–32 的 slug 必須與現有 catalog 完全一致。檢查三份文件的站內相對連結與 `npm run check:tasks`、`git diff --check`。這次只改計畫文件，不重跑無關的網站／API 建置。

## Notes

參考任務仍為 active；60 篇、1,800–3,000 字與五篇代表篇是其已批准計畫，不代表已完成。現有共用格式有實際差異：Codex spans 對 Claude inlines；對方 code 必填 label 且語言列舉未包含 Codex 既有 TOML／CSV／Shell。整合項目已記錄在 depth-plan.md 與原實作任務。本規劃完成後交還任務；文章擴充與發布仍未執行。
