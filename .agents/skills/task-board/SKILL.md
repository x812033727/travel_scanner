---
name: task-board
description: travel_scanner 的任務看板與 PR 循環：從 tasks/open 挑票、先查有沒有別的 session 在做（分支、worktree、遠端、開著的 PR）、claim 並開分支、在 PR 裡結案、在嚴格的分支保護下 rebase 與合併（四個必要檢查、squash、--match-head-commit）、讀 CI 失敗與已知 flake、整理卡在 review 的票與過期認領。要接下一張票、開票、認領或釋出票、開 PR、合併 PR、處理 BEHIND／DIRTY、判斷某張票或分支是否已經落地、做看板總整理時，先讀這個 skill。Take, claim, file and close tasks in tasks/, and open, rebase and merge their pull requests under branch protection.
metadata:
  short-description: 任務看板：挑票、認領、開 PR、合併
---

# 任務看板（task-board）

`tasks/open/` 是好幾個人與模型共用的佇列。這個 skill 只放指令、關卡、去哪裡讀；規則全文在 `tasks/README.md`，分支保護在 `.github/BRANCH_PROTECTION.md`。

## 不變的規矩

1. **claim 不是鎖。** `npm run tasks -- claim` 只寫你自己分支上的檔案；別的 session 在它的分支上認同一張票，你看不到。真正有效的檢查是分支：`git branch --list` 裡前面有 `+` 的分支是別的 worktree 正在用的（不管推沒推）；`git ls-remote --heads origin` 是別人推上去的；`gh pr list` 是開著的 PR。三個都查，而且要在**開 PR 前再查一次**，因為碰撞可以發生在你認領之後。
2. **scope 是對檔案的宣告，窄到只剩你會改的路徑。** scope 到 `apps/web` 會擋掉所有 web 的票。`--force` 可以蓋過重疊、活的持有者、未完成的相依，只在你確定的時候用，並把理由寫進票。
3. **在 PR 內結案。** `npm run tasks -- done <id>` 當 PR 的最後一個 commit，票的檔案跟工作一起搬到 `tasks/done/`；不要為了搬一個檔再開一個 PR。設成 `review` 卻從不 `done` 的票會在合併後繼續鎖住 scope。
4. **票的檔案就是交接。** 停手前打勾、寫 Notes、`release`；發現但不修的東西 `new` 一張票，不要留在對話裡。
5. **別人持有的票不要動**：對它 `done`／`release` 會被 auto 模式擋成 Interfere With Workloads，用有選項的提問列出票號與證據，站主同意後同一個指令就過。
6. **合併只能靠綠燈**：四個必要檢查 `api`、`web`、`containers`、`full-stack-smoke`，`strict` 表示分支要跟上 main，`enforce_admins` 表示 `--admin` 不是後門，repo 也不允許 `--auto`。用 `--match-head-commit <綠燈的 SHA>` 合併，別人推了新 commit 就會被拒而不是把沒測的東西合進去。背景的等綠再合併迴圈，只有站主下過點名條件的常設指令（例如「CI 綠就合併」）才能跑；否則每個 PR 各問一次。
7. **合併前先看票有沒有已經落地**：`git fetch` 後 `git log --oneline origin/main -- <scope 路徑>`，以及 `tasks/done/` 裡有沒有同一張票；另一個 session 做完的話，取 main 的版本，不要開競爭的 PR。
8. 中文的 PR 標題或內文在 Windows 的 Git Bash 要用 `--body-file` 或 `gh api --input`，不能當命令列參數。

## 主幹

| # | 階段 | 指令 | 關卡 |
| --- | --- | --- | --- |
| 1 | 挑票 | `npm run tasks -- next [--area A]` 或 `list`；`node .agents/skills/task-board/scripts/who-is-on-it.mjs [--scope <path>]` | 沒有 `+` 分支、遠端分支、開著的 PR 在做同一件事；main 上沒有已落地的痕跡 |
| 2 | 認領 | `git fetch origin && git checkout -b claude/<slug> origin/main`；`npm run tasks -- claim <id> --owner <你的名字> --branch claude/<slug>` | 工具沒有拒絕（scope 重疊會拒；過期 24 小時的認領可直接接手） |
| 3 | 做事 | 在 worktree 裡改 scope 內的檔案；票的 Steps 隨手打勾；AGENTS.md 列的檢查跑你動到的那幾項 | `npm run check:tasks` 過 |
| 4 | 結案 | `npm run tasks -- done <id>`，commit（訊息附 `Task: <id>`），push | 檔案在 `tasks/done/`、未勾的項目在 Notes 交代 |
| 5 | PR | `gh pr create --base main --head <branch> --title "<type>(<area>): …" --body-file <file>` | 內文寫為什麼、做了什麼、怎麼驗 |
| 6 | 等綠、合併 | `bash .agents/skills/task-board/scripts/merge-when-green.sh <pr>`（rebase → push → 等檢查 → squash 合併 → main 又動了就重來，最多三輪） | 四個必要檢查 `completed success`；`mergeStateStatus` 是 CLEAN |
| 7 | 之後 | 部署走 skill `deploy`；同一組票要批次合併時一次跑一條 chain | 票在 done、分支已刪、記憶或交接有寫 |

## 指令

```bash
npm run tasks                                   # 指令清單
npm run tasks -- list [--status S] [--area A] [--owner NAME]
npm run tasks -- new --title "..." --area <api|web|ops|tools|docs|meta> --scope a,b [--priority P2] [--depends-on id,id]
npm run tasks -- claim <id> --owner <name> --branch <branch> [--force]
npm run tasks -- status <id> <open|in-progress|blocked|review>
npm run tasks -- release <id>        # 停手
npm run tasks -- done <id>           # 合併前、PR 的最後一個 commit
npm run check:tasks                  # CI 也跑：格式、狀態對資料夾、scope 非空、相依存在
# 可靠地讀檢查（永遠不要 gh pr checks --watch | tail）
SHA=$(gh pr view <n> --json headRefOid -q .headRefOid)
gh api "repos/{owner}/{repo}/commits/$SHA/check-runs" -q '.check_runs[] | "\(.name)\t\(.status)\t\(.conclusion)"'
gh pr view <n> --json mergeStateStatus,mergeable
gh pr merge <n> --squash --match-head-commit "$SHA"
```

`tasks new` 寫出的範本帶佔位段落（`## Why` 等），把佔位文字換掉，不要在下面再加一份同名段落。`--depends-on` 在檔案裡是縮排清單，寫成 `[id]` 會被 check 擋。

## 規則在哪裡（不重抄）

| 問題 | 讀 |
| --- | --- |
| 五條規則、欄位表、狀態的意思、`check` 抓什麼 | `tasks/README.md`、`tools/tasks.mjs` 的 `helpText` |
| 分支保護設了什麼、為什麼、怎麼讀檢查 | `.github/BRANCH_PROTECTION.md` |
| 推 PR 前要跑的檢查 | `AGENTS.md` §Checks before you push |
| 怎麼查誰在做、怎麼證明已落地、過期認領怎麼處理 | `.agents/skills/task-board/references/collisions.md` |
| BEHIND／DIRTY、rebase 的坑、讀 CI 失敗、已知 flake | `.agents/skills/task-board/references/merge.md` |
| 一張好票長什麼樣 | `.agents/skills/task-board/references/ticket-template.md`；範例 `tasks/done/2026-09-14-release-drivers-own-deploy-hold.md` |
| 看板總整理的做法與紀錄 | `docs/work-status-2026-09-19.md` |

## 這個 skill 的檔案

- `scripts/who-is-on-it.mjs`：唯讀。列出持有中的票（年齡、是否過期）、它們鎖住哪些票、`+` 分支與遠端分支、開著的 PR，以及 `--scope <path>` 時誰碰到那條路徑。
- `scripts/merge-when-green.sh`：在有 PR 分支的 worktree 裡跑，rebase 到 origin/main、push、等檢查、以綠燈的 SHA squash 合併；衝突就停下來交給人。
- `.claude/skills/task-board/SKILL.md` 是這一份的逐字複本，`npm run test:tools` 會比對。
