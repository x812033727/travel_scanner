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
---

# Follow up retained Codex C drive worktrees when their work finishes

## Why

The owner narrowed cleanup to Codex. After the deeper 22-dirty-root audit, four completed unused checkouts were removed and 32 of the original 36 Codex roots remain. Eighteen of the original dirty roots remain for specific integration, delivery, dependency or ownership reasons. The latest 22-root findings and concrete actions are in `tasks/worktree-dirty22-20261011.md`; the other original roots remain documented in `tasks/worktree-cleanup-20261011.md`. This task tracks later cleanup eligibility; it does not claim the underlying product tasks or authorize discarding changes.

## Definition of done

- [ ] Recheck only Codex paths after their existing owners have completed their work; record any eligible removals with before/after evidence.
- [ ] Preserve unfinished work, non-regenerable ignored files, the primary repository, and the ongoing Ou de Jianghu handoff.

## Steps

- [x] Deeply audit the 22 dirty roots: remove 54/56/57/58 after full backup and unused verification; retain eighteen.
- [ ] For the eighteen retained dirty roots, follow the per-root checklist in `tasks/worktree-dirty22-20261011.md`; five have completed source scope but still require dependency/ownership clearance, and thirteen require integration, delivery or material reconciliation.
- [ ] Finish or review the six existing open PRs without treating a clean checkout as delivery completion.
- [ ] Resolve the four clean ongoing delivery/workflow entries: news-held recovery, Embedding, localization batch003, and batch005.
- [ ] Recheck the two active audit worktrees and the protected 1b93 visual handoff only after their work ends; never remove the primary clone as a historical worktree.
- [ ] Immediately before a later removal, verify current HEAD, main/PR completion, status including all untracked files, ignored artifacts, running processes and chat ownership; keep recovery evidence and verify removal.

## How to verify

Read `C:/Users/x8120/.codex/scratch/worktree59-cleanup-20261011/codex-worktree-report.html` and the JSON/verification receipts alongside it. Recompute the evidence live before future cleanup; this is a dated inventory. Run `node tools/tasks.mjs check` for metadata edits.

## Notes

This task is open and unclaimed. Claude and all other projects are outside the final scope. Existing product ownership, production leases, STOP markers and source media remain untouched. This dated follow-up tracks the remaining 32 roots; four eligible local refs were removed in the deep audit, with recoverable archives.

## 下一輪建議優先順序（2026-10-11 容量快照）

這些是收尾後重新判定清理的候選，並未因列入清單而確認可以直接刪除；容量為較早排行的邏輯大小，不保證能釋放同等實體空間。前五項合計約 4.19 GiB，b136 的 0.66 GiB 另有實際凍結依賴。

| 優先 | 目錄／工作 | 原大小 GiB | 最後缺的步驟 |
| --- | --- | ---: | --- |
| 1 | `C:/Users/x8120/.codex/worktrees/article-locales-wave4/travel_scanㄐ` | 0.858 | #1401 exact-head CI/review與merge；對帳兩張原release票，保存ignored staging及外部raw receipts；原owner確認該checkout不再續用。 |
| 2 | `C:/Users/x8120/.codex/worktrees/fc2e/travel_scanㄐ` | 0.623 | 原聊天仍pinned，最後rollout缺失；確認仍否依賴32份研究／logs，再保全34untracked與ignored驗證日志。未確認用途不得刪。 |
| 3 | `C:/Users/x8120/.codex/worktrees/batch006-final-close/travel_scanㄐ` | 0.546 | 保全兩份local task後，核對仍pinned c5d9 managed attachment與真正owner用途；原rollout缺失未能證明釋出，本輪keep。 |
| 4 | `C:/Users/x8120/.codex/worktrees/4e16/travel_scanㄐ` | 1.263 | #1373 OPEN exact HEAD的CI/review/merge；保存ignored staging，將Decrypt分類原票的NanoBanana／TikTok兩候選scope明確對帳／交接共享隊列，確認原owner不再使用root。 |
| 5 | `C:/Users/x8120/.codex/worktrees/pr-merge-watch/travel_scanㄐ` | 0.897 | 沿單一restore-tidy-capped-list-retention-guard票，在fresh main整合最小guard及有意義回歸、CI/review/merge；完整封存舊staged17並確認checkout unused。 |
| 6 | `C:/Users/x8120/.codex/worktrees/b136/travel_scanㄐ` | 0.660 | e931 frozen manifest private_file_pins仍指向b136/tools/tasks.mjs，真executor每dispatch前驗pin。合法successor需在全新guard/manifest做same-bytes helper遷移與零provider驗證，證明不再依賴原absolute path。 |

- [ ] 先安排 wave4 已發布 13 篇收據 PR #1401、fc2e 研究封存與使用確認、Batch034 source-only 結案副本；不要重新發布已完成內容。
- [ ] 再收尾 4e16 的 32 篇發布收據 PR #1373 與 Decrypt 原票交接、PR921 missing-entry 保留 guard。
- [ ] b136 先沿 `2026-10-11-migrate-frozen-embedding-helper-dependency` 確認合法 successor 的新 guard，不改或重放旧 frozen manifest。

新聞審核 16.49 GiB（fe41 8.86、6f71 7.62）仍有 520／208 cohort 續作；整根不能視為可刪副本。翻譯發布 13.89 GiB 中，all-missing-20261007 約 9.68 GiB 仍承接未完工作，應先挑已發布子批次逐筆驗 release receipt、source/hash、owner、備份恢復。精確外部資料候選與限制見本機 `large-data-next-candidates.json`；本輪未刪除這些外部資料。

### 已發布翻譯材料的封存候選

容量為 2026-10-11 22:35–22:48 的父目錄快照；三組合計約 0.504 GiB，仍須排除共用／後續引用，不代表全部可回收。

- [ ] `C:/Users/x8120/.codex/article-localization-release/batch026-wordpress-operations`（約 0.166 GiB）：按已結案四篇的 source、final manifest、v5 terminal journal、public QA 與 hold 收尾重新核對檔案雜湊。 確認原 owner 與後續任務不再直接依賴此資料路徑；把失敗 v4 和成功 v5 一起封存、驗證還原後，再清本機副本。
- [ ] `C:/Users/x8120/.codex/article-localization-release/batch018-web-basics`（約 0.168 GiB）：重核四篇 exact source、manifest、terminal journal、final acceptance 和 post-clear 收據；不要只看內容票的早期 Notes。 保留舊 failed release 與 backup 的因果證據，確認 owner/path 無後續依賴，再封存並驗證還原。
- [ ] `C:/Users/x8120/.codex/article-localization-release/batch012-selection`（約 0.17 GiB）：先以 Otaru/Sapporo terminal release 子目錄為最小封存範圍，核對 source/review/journal/public QA 的 exact hashes。 確認新 Sapporo route 票與 Jeju handoff 是否引用舊原始 proof；有依賴先移交可還原證據，不直接刪整個 batch012-selection。

先核對既有 done 發布票、完整 source/review/release 原始證據與 owner，再做可還原備份。這次只列候選，沒有重跑正式站、發布或刪除外部材料。
