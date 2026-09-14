---
id: 2026-09-14-gemini-advanced-curriculum
title: Gemini 深入教學第二階段課綱與任務拆分
status: done
priority: P2
area: docs
owner: codex-gemini-deep-plan
claimed_at: 2026-09-14T11:04:32Z
created_at: 2026-09-14T11:04:09Z
completed_at: 2026-09-14T11:15:48Z
branch: codex/gemini-advanced-curriculum
depends_on: []
scope:
  - docs/gemini-series/advanced
  - docs/gemini-series/README.md
  - docs/life-ai-series.md
---

# Gemini 深入教學第二階段課綱與任務拆分

## Why

使用者要求在現有 Gemini 50 篇之後繼續規劃深入教學。本次交付可執行的課綱和未來工作分工，先核對官方功能邊界與既有編輯批次，避免重複題目或提前建立未發布連結。

## Definition of done

- [x] 36 篇唯一 slug、系列 51–86、六個深入主題；保留既有 01–50 與唯一公開總目錄。
- [x] 每篇列出成果、先修、四階段操作、練習素材、通過條件、故障案例、官方依據及平台／版本條件。
- [x] 完整課綱有主題索引、六條閱讀路線、逐篇定位、前後卡片、延伸與返回目錄。
- [x] 記錄 NotebookLM／Gemini、Interactions／generateContent、MCP／Skills／MD 與第二階段可見性差異。
- [x] 更新 AI 編輯總表，拆成八張範圍明確的後續任務並記錄依賴。
- [x] 課綱資料、slug、引用、相對連結、先修 DAG 及任務檢查通過，結果留在 advanced/planning-validation.json。

## Steps

- [x] 讀取現行 catalogue、系列收據、編輯總表與相關未完成批次。
- [x] 查閱 34 個官方來源，按成果與失敗練習建立課綱。
- [x] 建立規劃用 JSON、可閱讀課綱、後續任務與總表入口。
- [x] 完成文件檢查並收尾本規劃任務；後續內容製作保持 open。

## How to verify

執行一次性 Python 文件完整性檢查，檢查 36 篇／34 來源、slug 不與既有內容重複、先修無循環、所有卡片及本機連結、八張製作任務 coverage。再執行 node tools/gemini-series.mjs check（確保現行 51 頁仍可通過）、npm run test:tools、npm run check:tasks 與 git diff --check。

## Notes

本次只規劃；沒有新增 36 篇正式內容、圖片、雲端操作或發布。現有 hub 已發布，新增 catalogue 不能只依 hub 發布旗標控制，需先完成伺服器端第二階段可見清單。第一階段的驗證收據維持原樣。新課綱與正式 runtime catalogue 明確分開。

## Outcome

2026-09-14：完成 advanced/README.md、curriculum.json、sources.json 與 planning-validation.json；AI 編輯總表新增 250–285，八張後續任務維持 open。

驗證：36 個唯一 slug；六主題、六路線覆蓋全部新篇；34 個官方來源；292 個課綱內部／相對連結；無先修循環及既有 slug 衝突。node tools/gemini-series.mjs check 通過現行 51 頁；npm run test:tools 48/48；npm run check:tasks 通過 423 張任務，只有既有其他任務的過期／範圍重疊警告；git diff --check 通過。沒有應用程式程式碼或 runtime catalogue 變更。
