---
id: 2026-09-07-board-conflicts-on-every-pr
title: tasks/BOARD.md 是產生檔，卻讓每個 PR 互相衝突
status: review
priority: P3
area: tools
owner: claude-opus-5
claimed_at: 2026-09-12T03:26:18Z
created_at: 2026-09-07T01:23:52Z
completed_at:
branch: claude/great-torvalds-c39666
depends_on: []
scope:
  - .gitignore
  - tasks/BOARD.md
  - tasks/README.md
  - tools/tasks.mjs
  - tools/tasks.test.mjs
  - AGENTS.md
  - README.md
---

# tasks/BOARD.md 是產生檔，卻讓每個 PR 互相衝突

## Why

看板規定「每張任務都要進 `tasks/open/`」，而 `npm run check:tasks` 會擋下沒有跟著更新的
`tasks/BOARD.md`。結果是：任何一個開了新任務的 PR 都會改到 BOARD.md 的同一段，兩個這樣的
PR 一定衝突。

2026-09-07 的實測：PR #249 在 90 分鐘內兩次變成 `mergeable_state: dirty`，兩次的唯一衝突
檔案都是 `tasks/BOARD.md`，兩次都是重跑 `npm run tasks:board` 就好——但每次都要 rebase、
force-push、等一輪完整 CI。main 的合併頻率比一輪 CI 還快的時候，這會變成跑不完的跑步機。

## Definition of done

- [x] 兩個各自新增一張任務的分支，可以在不手動處理 BOARD.md 的情況下合併。

## Steps

- [x] 評估三個方向：(a) `.gitattributes` 給 `tasks/BOARD.md` 一個 `merge=` driver，衝突時
      直接重跑產生器；(b) 把 BOARD.md 從版本控制拿掉，改成 `npm run tasks -- list` 就好，
      `check:tasks` 只驗任務檔；(c) 讓 BOARD.md 的排版對 append 友善（每張任務一行、依 id
      排序），把衝突縮小到真正同一行的情況。
- [x] 選定之後同步更新 `tasks/README.md` 與 `AGENTS.md` 的說法。

## How to verify

開兩個分支各自 `npm run tasks -- new`，把其中一個合進 main，另一個 rebase／merge 過來，
確認不需要人工處理 BOARD.md。

## Notes

2026-09-12 決定：走方向 (b)，把 `tasks/BOARD.md` 從版控移除、加進 `.gitignore`，改由
`npm run tasks:board` 隨時產生。(a) 與 (c) 都實測過，兩個都不行：

**(a) merge driver 做不出正確的看板。** 在小型複製品上掛一個探針 driver 實測，driver 被呼叫
的當下：工作目錄裡沒有對方分支新增的任務檔（`worktree_has_alpha=false`）、index 裡也沒有、
`MERGE_HEAD` 與 `REBASE_HEAD` 都解不出來。也就是說 driver 拿得到的只有 BOARD.md 自己的三個
版本，看不到合併後的任務集合，因此「重跑產生器」重跑出來的是**少一張任務**的看板。實測結果：
合併確實不再衝突，但合併完 `check:tasks` 直接報 out of date，看板裡找不到對方那張任務。等於
把一個看得見的衝突換成一個安靜的錯誤答案，CI 照樣紅、照樣要再補一個 commit 跑一輪。

另外兩個成本仍然存在：driver 的指令要每台機器自己 `git config`（`.gitattributes` 只寫得了
名字），而 GitHub 算 mergeable 時不會執行自訂 driver，所以 PR 在網頁上還是會變 dirty——
#404／#409／#410 的實際痛點（rebase、force-push、等一輪完整 CI）一個都沒省到。

**(b) merge=union 同樣產出 check 不接受的檔案。** 實測合併不衝突，但 `check:tasks` 一樣報
out of date：union 是把兩邊的行都留下，本來就不會等於產生器的輸出。

**(c) 一行一張、依 id 排序也救不了。** 兩張同一天建立的任務 id 相鄰，插入點是同一個位置，
git 需要中間至少隔一行沒動過的內容才併得起來——而「同一天各開一張任務」正是這裡最常見的情況。
開頭那行統計數字（`**N open · ...**`）也是每張任務都會動。

**做法與保證。** `check:tasks` 的看板新鮮度檢查沒有拿掉，只是跟著檔案走：`BOARD.md` 只要
還在版控裡（`git ls-files` 查得到）就必須與任務檔一致，否則 exit 1；被 git ignore 的時候就
跳過，這樣別人 `git pull` 之後本機那份舊看板不會害 pre-push 檢查紅掉。實測三種狀態的結束碼：
tracked+stale=1、tracked+fresh=0、untracked=0。

**驗證。** 用真的 `tools/tasks.mjs` 與真的 309 個任務檔建小型複製品，兩個分支各 `tasks new`
一張任務：改之前 `git merge` 必衝突且唯一衝突檔就是 `tasks/BOARD.md`；改之後 `git merge` 與
`git rebase` 都乾淨通過。

**遷移成本。** 當下有 4 個 open PR（#411／#414／#417／#419）仍把 BOARD.md 當成追蹤檔。這個
PR 合併後，它們各自會遇到一次 modify/delete 衝突，用 `git rm tasks/BOARD.md` 解掉即可，之後
就不會再有。

**如果之後還是想在 GitHub 上直接讀到看板**：唯一不會重新引入衝突的做法是讓 CI 在 main 上
產生並提交它（PR 分支永遠不碰這個檔）。這需要一個能推上受保護 main 的 bot，本次沒有動。

- (a) 的 merge driver 在 CI 與別人的機器上都要裝，`.gitattributes` 的 `merge=` 只是名字，
  真正的指令在各自的 git config 裡——這是這個方向最大的成本。
- 現況的暫時解法：衝突時不要手動改，`git checkout --ours`／`--theirs` 都不對，直接
  `npm run tasks:board` 重新產生再 `git add`。
