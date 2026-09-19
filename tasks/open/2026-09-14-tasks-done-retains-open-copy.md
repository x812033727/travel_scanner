---
id: 2026-09-14-tasks-done-retains-open-copy
title: tasks done 後仍保留 open 副本：調查 Windows 封存行為
status: review
priority: P2
area: tools
owner: claude-fable-5-1
claimed_at: 2026-09-19T11:05:39Z
created_at: 2026-09-14T11:16:14Z
completed_at:
branch: claude/travel-scanner-pr-552-rpq36m
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
- [x] done 成功回傳時，確認同 ID 只剩 done/ 一份；若刪除失敗或檔案被重新建立，給明確失敗診斷，不回報成功。
- [x] 對已完成檔案與其他任務做保存性檢查，不以清空目錄解決重複。
- [x] 必要回歸測試、npm run test:tools、npm run check:tasks 通過。

## Steps

- [x] 認領後查看 tools/tasks.mjs 的 done 流程（目前寫 done 再 rmSync open）。
- [x] 用新建的最小暫存 queue 測試，對照目前工具測試均通過但真實環境殘留的差異。
- [x] 依確認根因修復或記錄環境相容策略；不要因單次現象改寫整套任務協議。

## How to verify

在暫存 queue 完成一張任務後，同時用 Node existsSync、PowerShell Test-Path 與重讀目錄核對。模擬刪除錯誤時命令不得謊報完整成功；再次執行不破壞已完成紀錄。

## Notes

原事件在 2026-09-14T11:15:48Z。已確認 done 檔 ID/status 正確後，只手動移除該張 open 副本，保留完整已完成檔案。48 個工具測試先前全過，因此根因仍待查；本票不聲稱已重現一般 Node 或 Windows 的缺陷。

2026-09-14 約 15:34Z 再次觀察：使用者允許封存已合併 PR #485 的 `2026-09-14-claude-code-tutorial-center`。已核對 PR 狀態 MERGED、merge commit `35a2d258b51d2a1ac9aff91dc5f7ed5a8df823ec` 是目前 HEAD 的祖先；`tasks done` 回報完成後，原 open 檔仍在，導致下一張平台票 claim 拒絕。比對兩份 frontmatter 以下正文相同後，以 PowerShell `Remove-Item -LiteralPath` 只移除該確切 open 副本，`Test-Path` 回 false，隨後 claim 成功。沒有因此修改 tasks 工具或宣稱一般 Windows 都會重現；刪除成功後需重新讀取核對的調查留在本票，避免另建同題任務。

### 2026-09-19 done in repo (claude-fable-5-1)

這裡沒有 Windows，所以第一項（在 Windows 重現）沒做，留給站主（下面）。從 Linux 讀 `commandDone`
能確認的是：舊流程 `writeTask(done)` → `rmSync(open, { force: true })` → 回報「moved」**從不回頭看
open 副本是否真的不見了**，而 `force: true` 只吞 ENOENT。三種在 Windows 上會出現「命令成功、檔案還在」
的形狀，它都擋不住：

1. 另一個行程（編輯器、索引器、同步客戶端）用 share-delete 開著檔案：`unlink` 成功、目錄項目要等
   最後一個 handle 關掉才消失，`git status` 在那之前就看得到它。
2. 同步客戶端把剛刪掉的檔案放回來。
3. 刪除路徑是從 `id` 重組的（`open/<id>.md`），不是讀到的那個檔；名稱與 id 不一致時 rmSync 找不到
   檔案、`force` 把 ENOENT 吞掉，一樣回報成功。`check` 會抓名稱≠id，但 `done` 在它之前就說完成了。

改動（`tools/tasks.mjs`）：

- `done` 刪的是實際讀到的 `task.file`，刪完**驗證**檔案不在；還在就等 50→800 ms 重試五次，仍在就
  以非零結束並印出診斷（哪個檔還在、錯誤碼、done/ 已有完成檔、請關掉持有它的程式後手動刪除再跑 check）。
  done 副本保留，不動其他任何檔案。
- `check` 對「done/ 有 status: done、open/ 有同 id」這種重複，訊息多一句：這是被中斷的 done 留下的
  open 副本，比對後手動刪 open 那份。
- 測試（`tools/tasks.test.mjs`）：刪除一直 EBUSY／刪除「成功」但檔案仍在 → 回失敗訊息且重試節奏正確；
  第二次看不見 → 允許回 moved；正常 done 後只剩一份且 check 綠；人工放回 open 副本後 check 點名它。
  `npm run test:tools` 74 過，`npm run check:tasks` 588 檔通過。

**站主在 Windows 上確認（PowerShell，同一個 worktree）：**

```powershell
npm run tasks -- new --title "disposable windows archive check" --area tools --scope tools/tasks.mjs
npm run tasks -- claim <印出的 id> --owner <你的名字>
npm run tasks -- done <id>
Test-Path tasks/open/<id>.md   # 要是 False；若命令改回報失敗，照訊息關掉持有檔案的程式再刪
npm run check:tasks
git checkout -- tasks; Remove-Item tasks/done/<id>.md   # 用完把這張拋棄式的票清掉
```

`2026-09-14-investigate-windows-task-archive-leftover-open` 是同一件事的另一張票，已併進這裡。
