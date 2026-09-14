---
id: 2026-09-14-claude-tutorial-ci-validation
title: Claude tutorial GitHub Actions validation workflow
status: in-progress
priority: P2
area: tools
owner: codex-claude-completion
claimed_at: 2026-09-14T13:54:40Z
created_at: 2026-09-14T13:29:33Z
completed_at:
branch: codex/claude-code-advanced-tutorials
depends_on: []
scope:
  - .github/workflows/claude-tutorial-validation.yml
---

# Claude tutorial GitHub Actions validation workflow

## Why

使用者指定 x812033727/travel_scanner 作為 Claude 網頁與 GitHub Actions 實測儲存庫。原教材僅有獨立練習包的 workflow，需提供符合 monorepo 路徑、可審查的實際手動驗證入口。

## Definition of done

- [x] 提供手動入口，預設只測合成資料；模型審查需另選 run_model。
- [x] 鎖定預設分支的 dispatch SHA、contents:read、claude-lab 與固定 action SHA；輸出只保存驗證後 JSON artifact。
- [x] 本機 workflow 解析與防護測試通過。
- [ ] 合併後取得 GitHub Actions baseline 與實際模型執行紀錄；沒有憑證時保持待辦。

## Steps

- [x] 核對官方 Action 固定提交的輸入、輸出。
- [x] 改用 monorepo 內的測試、diff、模型與 artifact 路徑。
- [x] 記錄執行結果與尚缺前提。

## How to verify

`node --test tools/claude-code-series.test.mjs`；在 lab 執行 `node --test tests/model.test.mjs tests/automation.test.mjs tests/sdk-state.test.mjs`。合併後在 Actions → Claude tutorial validation → Run workflow 先保持 run_model=false；claude-lab 加入 ANTHROPIC_API_KEY 後再選 true，核對 review artifact。

## Notes

2026-09-14：GitHub 唯讀盤點顯示 repository secrets=0、environments=0、registered Claude workflows=[]。本機 CLI OAuth 重新授權成功不等於 GitHub CI 有憑證，沒有複製帳號憑證到 GitHub。此 workflow 尚未合併、安裝或 dispatch；不含部署、資料庫匯入與公開發布。

本機系列工具 12 項通過；實際 workflow baseline 指令 8 項通過。原始範圍與 SHA：docs/claude-code-series/advanced/evidence/live/ci-workflow-validation.json；操作手冊：docs/claude-code-series/advanced/github-actions-validation.md。workflow 已包含在審查包，等待與本批內容一併審查及遠端前提建立。
