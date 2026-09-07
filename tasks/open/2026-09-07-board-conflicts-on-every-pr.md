---
id: 2026-09-07-board-conflicts-on-every-pr
title: tasks/BOARD.md 是產生檔，卻讓每個 PR 互相衝突
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-09-07T01:23:52Z
completed_at:
branch:
depends_on: []
scope:
  - .gitattributes
  - tools/tasks.mjs
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

- [ ] 兩個各自新增一張任務的分支，可以在不手動處理 BOARD.md 的情況下合併。

## Steps

- [ ] 評估三個方向：(a) `.gitattributes` 給 `tasks/BOARD.md` 一個 `merge=` driver，衝突時
      直接重跑產生器；(b) 把 BOARD.md 從版本控制拿掉，改成 `npm run tasks -- list` 就好，
      `check:tasks` 只驗任務檔；(c) 讓 BOARD.md 的排版對 append 友善（每張任務一行、依 id
      排序），把衝突縮小到真正同一行的情況。
- [ ] 選定之後同步更新 `tasks/README.md` 與 `AGENTS.md` 的說法。

## How to verify

開兩個分支各自 `npm run tasks -- new`，把其中一個合進 main，另一個 rebase／merge 過來，
確認不需要人工處理 BOARD.md。

## Notes

- (a) 的 merge driver 在 CI 與別人的機器上都要裝，`.gitattributes` 的 `merge=` 只是名字，
  真正的指令在各自的 git config 裡——這是這個方向最大的成本。
- 現況的暫時解法：衝突時不要手動改，`git checkout --ours`／`--theirs` 都不對，直接
  `npm run tasks:board` 重新產生再 `git add`。
