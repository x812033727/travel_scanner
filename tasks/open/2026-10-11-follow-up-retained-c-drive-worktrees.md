---
id: 2026-10-11-follow-up-retained-c-drive-worktrees
title: Follow up retained Codex C drive worktrees when their work finishes
status: open
priority: P3
area: meta
owner:
claimed_at:
created_at: 2026-10-11T14:40:49Z
completed_at:
branch: codex/historical-branches-cleanup-20261011
depends_on: []
scope:
  - tasks/open/2026-10-11-follow-up-retained-c-drive-worktrees.md
  - tasks/worktree-cleanup-20261011.md
  - tasks/worktree-closeout-20261011.md
---

# Follow up retained Codex C drive worktrees when their work finishes

## Why

The owner narrowed cleanup to Codex. After the deeper 22-dirty-root audit and follow-up closeout, seven completed unused checkouts were removed in total; 29 of the original 36 Codex roots remain. Sixteen of the original dirty roots remain for integration, delivery, dependency or ownership reasons. This is the original cohort, not a current global checkout count. The latest 22-root findings and concrete actions are in `tasks/worktree-dirty22-20261011.md`; the other original roots remain documented in `tasks/worktree-cleanup-20261011.md`. This task tracks later cleanup eligibility; it does not claim the underlying product tasks or authorize discarding changes.

## Definition of done

- [ ] Recheck only Codex paths after their existing owners have completed their work; record any eligible removals with before/after evidence.
- [ ] Preserve unfinished work, non-regenerable ignored files, the primary repository, and the ongoing Ou de Jianghu handoff.

## Steps

- [x] Deeply audit the 22 dirty roots: remove 54/56/57/58 after full backup and unused verification; retain eighteen.
- [ ] For the sixteen remaining dirty roots, follow the dated per-root checklist and latest closeout report in `tasks/worktree-dirty22-20261011.md`; the remaining dependency, ownership, integration and delivery requirements are recorded per root in the latest closeout report.
- [ ] Finish or review the remaining existing open PRs after excluding merged #1401 without treating a clean checkout as delivery completion.
- [ ] Resolve the four clean ongoing delivery/workflow entries: news-held recovery, Embedding, localization batch003, and batch005.
- [ ] Recheck the two active audit worktrees and the protected 1b93 visual handoff only after their work ends; never remove the primary clone as a historical worktree.
- [ ] Immediately before a later removal, verify current HEAD, main/PR completion, status including all untracked files, ignored artifacts, running processes and chat ownership; keep recovery evidence and verify removal.

## How to verify

Read `<home>/.codex/scratch/worktree59-cleanup-20261011/codex-worktree-report.html` and the JSON/verification receipts alongside it. Recompute the evidence live before future cleanup; this is a dated inventory. Run `node tools/tasks.mjs check` for metadata edits.

## Notes

This task is open and unclaimed. Claude and all other projects are outside the final scope. Existing product ownership, production leases, STOP markers and source media remain untouched. This follow-up tracks 29 remaining roots from the original cohort; seven eligible local refs were removed across the two cleanup stages, with recoverable archives.

## 最新收尾（2026-10-12）

實際收據、來源容量、備份位置及現存待辦以 [本輪收尾紀錄](../worktree-closeout-20261011.md) 為準，原始核對報告保持為歷史快照。

- [x] wave4 #1401 已合併；wave4、fc2e、Batch034 三個副本完整備份並確認未使用後移除，原 checkout 的 Gitdir binding／本機 ref／registry 均已移除；fc2e 的 metadata 槽已由新 a18a worktree 重用，保留新 owner 的 metadata。fc2e 與 Batch034 的使用者用途釋出紀錄保留。
- [x] batch026、batch018、batch012 的十二個 Otaru／Sapporo 子根清理；batch012 的 Jeju／共用 758 檔原 SHA 不變。
- [x] 使用者最新要求「幫我將新聞與翻譯的都刪除」，並指定「新聞與翻譯不用備份」：`<home>/.codex/news-review` 與 `<home>/.codex/article-localization-release/all-missing-20261007` 不新增完整備份，確認精確路徑、無 reparse 及未使用後整根刪除，包含未完來源。原先只清已結案子批次的建議在這兩根已被新指示取代。
- [x] #1373 的 32 篇收據、原 release done 票與全域 stale-claim 修正集中 #1450；Decrypt 原始分類票恢復共享 open／unclaimed。
- [x] PR921 missing-entry 保留 guard 與五個回歸集中 #1450，專項驗證通過，完整 suite 既有失敗如報告所列。
- [ ] #1450 合併後，重新核對 4e16 與 pr-merge-watch 的 dirty／index／ignored／使用状态，再處理兩個副本；目前保留。
- [ ] b136 須完成現任 owner 的實際依賴釋出，或經審查 successor adoption；四原件與 12 個離線驗證已保存，舊 collector 直接 import 依賴仍在。
- [ ] 兩個新增隔離暫存 checkout 因自動核准／pinned 保護留下，沿收尾紀錄處理，不用其他工具繞過。

## 整根刪除後的產品續作

刪除資料不代表新聞／翻譯已發布或結案。原任務與 claim 不變；依使用者指示，兩根沒有新增完整備份。續做須先從仍存 Git、既有局部備份、正式站與其他來源重新整理，不能承諾完整還原；重新檢查 source/hash、review 與目前使用狀態，不重放過時或未知付費結果的 helper。

- 新聞去重 589 個候選，最新唯讀對帳剩 66 個未完；原 520 cohort 剩 52 個是其子集，全部已映射既有票。保留 `2026-10-10-news-held-cohort-recovery` 與 `2026-10-07-resolve-current-news-review-and-redraft` 的原 owner；逐項 CP／Guide／hold 下一步見收尾紀錄和 `news/pending66-existing-task-map.json`。CFTC 需處理來源 403，Sanders／Glasses 需校正 claim 12／14，XRPL5186 需刷新 source/evidence/history seals；20 個 no-Guide 接原 ingestion 流程。
- 全域補語系票 `2026-10-07-article-missing-locales-completion` 保持 open／unclaimed；重新量實際缺口，舊 862／3448 不當現況。`2026-09-14-article-five-language-completion` 原 owner 保留。
- wave4／wave5 依仍存已提交收據核對；wave6 #1409 merged 只是內容包整合。`2026-10-09-localize-reviewed-web-design-wave6` 的原 owner 先依 merged 收據修正過時 checklist；17 篇正式發布沿 `2026-10-09-release-localized-web-design-wave6` 接續與 85 頁／170 views／255 媒體驗收，先從仍存內容包與收據重建來源／release state，再核正 merge-v1／merge-v2 綁定及未證實的背景結果。

所有尚未合併的收尾內容都放在既有 PR #1450。Claude、《偶的江湖》、正式站、原影片與 provider/HOLD 不變。
