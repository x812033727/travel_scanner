---
id: 2026-09-14-tasks-done-retains-open-copy
title: tasks done 後仍保留 open 副本：調查 Windows 封存行為
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-14T11:16:14Z
completed_at:
branch:
depends_on: []
scope:
  - tools/tasks.mjs
  - tools/tasks.test.mjs
---

# tasks done 後仍保留 open 副本：調查 Windows 封存行為

## Why

2026-09-14 在 Windows worktree 執行 npm run tasks -- done 2026-09-14-gemini-advanced-curriculum，命令回報已移至 done，但隨後 git status 與 Get-Content 同時看到 done/status:done 與 open/status:in-progress 兩份同 ID 檔案。需要釐清是檔案系統、執行環境或工具封存流程造成；尚未確認根因。

## Definition of done

- [ ] 在不影響真實 task queue 的暫存目錄重現或確認環境限制，記錄 Windows、Node、檔案系統與最小操作。
- [ ] done 成功回傳時，確認同 ID 只剩 done/ 一份；若刪除失敗或檔案被重新建立，給明確失敗診斷，不回報成功。
- [ ] 對已完成檔案與其他任務做保存性檢查，不以清空目錄解決重複。
- [ ] 必要回歸測試、npm run test:tools、npm run check:tasks 通過。

## Steps

- [ ] 認領後查看 tools/tasks.mjs 的 done 流程（目前寫 done 再 rmSync open）。
- [ ] 用新建的最小暫存 queue 測試，對照目前工具測試均通過但真實環境殘留的差異。
- [ ] 依確認根因修復或記錄環境相容策略；不要因單次現象改寫整套任務協議。

## How to verify

在暫存 queue 完成一張任務後，同時用 Node existsSync、PowerShell Test-Path 與重讀目錄核對。模擬刪除錯誤時命令不得謊報完整成功；再次執行不破壞已完成紀錄。

## Notes

原事件在 2026-09-14T11:15:48Z。已確認 done 檔 ID/status 正確後，只手動移除該張 open 副本，保留完整已完成檔案。48 個工具測試先前全過，因此根因仍待查；本票不聲稱已重現一般 Node 或 Windows 的缺陷。

2026-09-14 約 15:34Z 再次觀察：使用者允許封存已合併 PR #485 的 `2026-09-14-claude-code-tutorial-center`。已核對 PR 狀態 MERGED、merge commit `35a2d258b51d2a1ac9aff91dc5f7ed5a8df823ec` 是目前 HEAD 的祖先；`tasks done` 回報完成後，原 open 檔仍在，導致下一張平台票 claim 拒絕。比對兩份 frontmatter 以下正文相同後，以 PowerShell `Remove-Item -LiteralPath` 只移除該確切 open 副本，`Test-Path` 回 false，隨後 claim 成功。沒有因此修改 tasks 工具或宣稱一般 Windows 都會重現；刪除成功後需重新讀取核對的調查留在本票，避免另建同題任務。
