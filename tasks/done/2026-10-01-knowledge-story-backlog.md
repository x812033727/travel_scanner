---
id: 2026-10-01-knowledge-story-backlog
title: Restore knowledge explainer and short-story planning backlog
status: done
priority: P2
area: docs
owner: codex-knowledge-story
claimed_at: 2026-10-01T04:54:13Z
created_at: 2026-10-01T04:54:12Z
completed_at: 2026-10-01T04:59:56Z
branch: codex/knowledge-story-backlog
depends_on: []
scope:
  - docs/videos/KNOWLEDGE-STORIES.md
  - tasks/open/2026-10-01-sothatswhy-season1-launch-buffer.md
  - tasks/open/2026-10-01-sothatswhy-season2-production-packages.md
  - tasks/open/2026-10-01-sothatswhy-season3-production-packages.md
---

# Restore knowledge explainer and short-story planning backlog

## Why

站主要求「補上之前的知識科普跟小故事相關的票或是之前相關的企劃」。原來如此三季、100 品牌故事與直式小故事路線已存在，卻缺共用入口；第二／三季候選題轉完整包與第一季試片後庫存也沒有獨立承接票。

## Definition of done

- [x] `docs/videos/KNOWLEDGE-STORIES.md` 連回舊企劃、查核與既有票，分清題庫、文字包、試片及正式驗收。
- [x] 補三張窄 scope 接續票，寫明前置、驗收、批次交接與權限界線。
- [x] 未改其他持有者的 owner／狀態，未重開既有 pilot／rollout。

## Steps

- [x] 查 memory／近期聊天清單、main、tasks、worktree、遠端與 PR；確定主要證據在 repo 企劃與完成票。
- [x] 查四份題庫數量／狀態及逐列查核路徑，另連回 81 題 AI 名詞系列與既有試片。
- [x] 建總入口與三張接續票，檢查連結／任務格式。

## How to verify

`npm run check:tasks`；四份 JSON 數量與本地查核路徑檢查；新增 Markdown 的相對連結存在；`git diff --check`。

## Notes

- 2026-10-01 基準 `origin/main`：`2596ce7fb5cd832baab2c496fe0ae72962698a4c`。
- 原來如此第一季 100 列 `fact-checked`，第二／三季各 100 列 `checked`；100 品牌故事已有單篇與雜湊綁定查核。相關 AI 名詞系列 81 列另有試片與自動接續票。
- 本次只補入口與票務。未改正式站、生成、上傳或公開影片；舊 claim 與未勾驗收保留。
