---
id: 2026-09-22-document-batch-010-and-011-localization
title: Document batch 010 and 011 localization release evidence
status: done
priority: P1
area: docs
owner: codex-p1-audit
claimed_at: 2026-09-29T02:10:12Z
created_at: 2026-09-22T03:20:02Z
completed_at: 2026-09-29T02:10:27Z
branch: codex/p1-task-audit
depends_on: []
scope:
  - docs/article-localization/releases/2026-09-22
  - tasks/open/2026-09-22-document-batch-010-and-011-localization.md
  - tasks/done/2026-09-22-document-batch-010-and-011-localization.md
---

# Document batch 010 and 011 localization release evidence

## Why

Batch 010 Singapore and batch 011 Jeju were independently reviewed, merged,
deployed, published and browser-verified, but their release evidence existed only
in local hash-bound artifacts. Later task-only PRs repeated intermediate Singapore
HOLD findings as if they were still current. Commit a small, shareable evidence
record without production snapshots, logs, credentials or screenshots.

## Definition of done

- [x] Singapore and Jeju release phases, exact Git and artifact hashes, QA counts
      and all public locale URLs are recorded in the repository.
- [x] Small independent editorial, source-correction, numeric/structural and SVG
      JSON receipts are preserved byte-for-byte with their original SHA-256.
- [x] The record distinguishes zero GitHub review objects from independent
      hash-bound editorial review and resolves the stale #639/#647 assertions.

## Steps

- [x] Reconcile final batch010 v6 and batch011 v2 release receipts and journals.
- [x] Copy only the required small review receipts and add structured evidence.
- [x] Validate JSON, receipt hashes, operation counts, task metadata and diff.

## How to verify

`Get-ChildItem docs/article-localization/releases/2026-09-22 -Recurse -Filter *.json`
parsed through `ConvertFrom-Json`; copied receipt SHA-256 values were checked
against their source artifacts. `npm run check:tasks` and `git diff --check` pass.

## Notes

The requested P: worktree could not be checked out because device writes returned
“A device attached to the system is not functioning.” Its path and registration
were preserved. Work continued in a C: sparse worktree under 15 MB with no package
installation. PR #639's task file and PR #647 were not edited or closed.


## 2026-09-29 標記完成（由站主授權，非原持有者）

站主要求逐張核對原 64 張 P1 並處理已無剩餘工作的票，並明確確認本次 30 張封存、2 張刪除。本次只結案，不重做已合併實作。
原持有者：codex-batch012-release-evidence；原分支：codex/localization-release-evidence-010-011。

- PR #648 merged 2026-09-22; README and 15 small evidence/review JSON files are present in docs/article-localization/releases/2026-09-22.
- Record distinguishes zero GitHub reviews from independent hash-bound editorial review and resolves stale #639/#647 claims.

上述後續證據補足舊清單仍未勾選的項目，已同步勾選。歷史限制保留供追溯；這是既有完成紀錄的核對，不宣稱本日重新部署、重新發布或重新跑過歷史測試。



`--force` 僅用於本次授權的任務結案記帳，未修改或接管原分支實作；已核對 main 與開啟 PR，完成判定依上列證據。Windows 的 tasks done 搬移曾留下 open 副本，本次用 Git 原子搬移保留完整任務紀錄。
