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
branch: codex/codex-learning-complete
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
- [x] 延續規劃 60 篇獨立補強規格：起點、操作、產物、正常／失敗、還原與圖片需求，集中到可點擊總目錄。
- [x] 連回現有四語作者檔及含簡中的內容包，補上六組十篇的共同驗收表，不更動發布狀態。

## Steps

- [x] 讀取對方任務 `01a09d8e-a18a-76a1-9952-b525f0210831` 與 `1cff` 工作目錄的相關檔案；沒有改動或送出任務訊息。
- [x] 對齊深度與網站體驗，保留 Codex 自身功能差異及五語範圍。
- [x] 驗證課程順序／ID／slug 唯一性、既有 32 篇映射、文件連結及任務格式。

## How to verify

解析 `docs/codex-learning/depth-plan.md` 的課程表與 `deepening/` 文件：60 個閱讀位置、ID 1–60 各一次、十單元各六篇；ID／slug／順序／單元須與現有 catalog 一致。逐一檢查總目錄、單元錨點、返回連結、作者檔及內容包的相對路徑。執行 `npm run check:tasks`、`git diff --check`。這次只改計畫文件，不重跑無關的網站／API 建置。

## Notes

先前已唯讀確認「規劃 Claude Code 教學目錄」60 篇繁中教學與總目錄完成、PR #485 合併；共用 inlines／article、code label 與 Shell／TOML／CSV 相容已整合至本分支。精確整合與驗證證據見 docs/codex-learning/progress.md；本輪沒有再次讀取或修改對方任務。

2026-09-14 本輪依使用者「繼續規劃深入教學」補上 deepening/README.md、unit-a.md 至 unit-j.md 及 review-checklist.md。60 篇規格與現有草稿逐篇連結，以五篇代表稿先行、六組各十篇核對。規格中的成功／失敗案例與圖片是下一輪要求，不代表新增實測結果。

驗證通過：十單元各六篇、60 個穩定 ID／slug／單元／次序、240 個作者稿連結、60 個五語內容包連結、1,101 個相對連結與必要錨點，以及六組十篇的完整覆蓋。npm run check:tasks 通過 412 個任務檔；其他任務既有警告保留。

目前 60 篇五語草稿已編譯；本輪只完成深入製作規劃，最終深入驗收仍 0/60。預覽啟動被自動核准審查拒絕（blocked by policy，未提供具體理由），產品操作與圖文終審仍待完成；原系列任務保留 blocked。本規劃保存後釋放持有，文章補強由對應內容任務接續，不提前開 PR、匯入、發布或部署。
