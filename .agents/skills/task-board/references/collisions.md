# 誰在做這件事：碰撞、過期認領、證明已落地

## 為什麼看板擋不住重工

- `claim` 只寫你分支上的檔案。2026-09-06 兩個 session 各自做完同一張票（#216 先合併，#217 關掉），白做一小時。
- 同一天再一次：看板顯示未認領，遠端分支與開著的 PR 都乾淨，但兄弟 worktree 在一條**沒推過**的本地分支上做同一個功能。`git branch --list` 裡帶 `+` 的分支就是它，`git branch -r` 與 `gh pr list` 看不到。
- 2026-09-12：認領前、推 PR 前都查過，對方在 37 分鐘後認同一張票、做完、先合併；我的 PR 綠著等審。碰撞的窗口是 PR 的整個壽命，不是認領那一刻。
- 2026-09-20：站主在兩個 session 下了同一句指令。長清單裡排後面的項目開工前先 `ListAgents`、看別的 worktree 的分支名。

## 開工前的四個檢查（一條指令跑完）

```bash
node .agents/skills/task-board/scripts/who-is-on-it.mjs --scope apps/web/lib
```

它做的事，手動版：

```bash
git fetch -q origin
git branch --list                                   # 前面 + 的分支：別的 worktree 正在用
git worktree list                                   # 本機的其他 session
git ls-remote --heads origin | grep -v refs/heads/main
gh pr list --state open --limit 100 --json number,title,headRefName,files   # 用你會碰的「路徑」過濾，不是票號
git log --oneline origin/main -- <scope 路徑>       # 空的才算真的沒開始
ls tasks/done | grep <slug>                         # 別人做完的票
```

分支只告訴你「這張票有人拿了」，不告訴你是誰：四條分支曾屬於至少兩個 session。要給持有者的訊息寫進票的 Notes，不要對著猜出來的 session 講。

## 過期認領與被鎖住的票

- 持有超過 24 小時（`isStale`）的認領可以直接接手，`claim` 會印 `Taking over a stale claim from <owner>` 並清掉 branch 欄位。
- 但 `claim` 的重疊檢查**不排除過期的認領**：只要持有者不改狀態，重疊的票要 `--force` 或先把那張改成 `blocked`。
- 2026-09-13 與 09-19 兩次總整理：主要工作早就合併、票卻停在 `review` 的認領，各鎖住 10 到 23 張票。算被鎖清單用唯讀腳本匯入 `tools/tasks.mjs` 的 `loadTasks`、`sharedScope`、`isStale`（`who-is-on-it.mjs` 就是這個）。
- 由非持有者結案要留紀錄：標題「標記完成（由站主授權，非原持有者）」、PR 與證據、每個沒勾的項目去了哪裡；站主同意後再做，否則被擋。
- main 上看不到的工作要另外查三處：兄弟 worktree 未 commit 的 `tasks/open/*`（`git -C <wt> status --short -- tasks/open`）、沒開 PR 的分支、開著的 PR 帶的新票。36 個 worktree 逐一跑 git 在 Windows 會超過兩分鐘，用背景執行。

## 證明一張票或一條分支已經落地

repo 用 **squash merge**，所以合併過的分支的 commit 永遠不在 main 上：`git cherry`、`--not --remotes`、subject 比對都會把落地的分支說成沒推（231 條裡誤報 69 條，真的只有 1 條）。

1. 有 PR 的：`gh pr list --state all --head <branch>` 拿 state 與 mergeCommit；`git diff --stat <PR head> <squash commit>` 是空的就是完整落地（`strict` 逼 head 跟上 main，所以樹會一模一樣）。head 物件本機沒有就 `git fetch origin pull/<n>/head`。
2. 沒 PR 的：先兩個便宜的過濾，`git merge-base --is-ancestor <branch> origin/main` 與 `git cherry origin/main <branch>` 零個 `+`；殘餘的用**內容標記**測：挑 2 到 4 個這條分支引入的東西（新檔路徑、符號、i18n key、migration 檔名）對 `origin/main` 查（`git ls-tree -r --name-only origin/main | grep …`）。有就是落地了，不管 git 怎麼說。
3. 推送狀態用 `git ls-remote --heads origin <branch>` 核實，本機有沒有 `origin/<branch>` 不算。
4. 刪分支前看 `git worktree list --porcelain` 有沒有 `detached`：掛在 detached HEAD 上的 commit 不在任何分支上，刪 worktree 就沒了。`git branch -d` 對已落地但 upstream 是 `[gone]` 的分支會拒絕，確認 `--is-ancestor` 後用 `-D`。

## 碰撞已經發生時

- 對方先合併：取 main 的版本（`git checkout origin/main -- <paths>`），拿掉你多加而沒人用的 message key；讀對方的做法，它可能比你的好。
- 只有一部分重疊：留下不重疊的那部分，開成一張疊在對方分支上的票。
- 兩份實作都完整：用多視角的代理比較（loader、route、單元測試、e2e、文件，加一個專門找合併版缺陷的），每個發現交給獨立代理反駁；存活的才值得帶進小的後續 PR。關掉被取代的 PR 時留言說明原因、分支保留。
