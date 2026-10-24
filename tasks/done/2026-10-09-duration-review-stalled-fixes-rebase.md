---
id: 2026-10-09-duration-review-stalled-fixes-rebase
title: Revalidate duration-only receipt after stalled video fixes rebase
status: done
priority: P2
area: docs
owner: codex-open-task-reconcile-510e
claimed_at: 2026-10-24T13:05:52Z
created_at: 2026-10-09T07:45:29Z
completed_at: 2026-10-24T13:06:14Z
branch: codex/open-tasks-reconcile-20261024
depends_on: []
scope:
  - tasks/open/2026-10-09-duration-review-stalled-fixes-rebase.md
---

# Revalidate duration-only receipt after stalled video fixes rebase

## Why

PR #1387 was rebased onto main 114aa2c95f8fa936cdaea649a6ed7a3b4476192b.
The exact main registry and report were preserved along with the earlier c645
review increment, leaving three actual changed registered bytes and the report
hash stale. A reviewer independent of the source authors must revalidate the
current baseline before the branch can claim a current duration-only receipt.

## Definition of done

- [x] All 108 main raw bindings agree with the exact main receipt and report;
  105 are unchanged and only the three actual registered deltas are rebound.
- [x] All main report text and the historical c645 review increment remain intact.
- [x] Current QA loss guards and duration/source rules are independently reviewed;
  focused tests and all 473 current plans pass with the fresh receipt.
- [x] Only these two receipt files and this narrow task record enter the commit;
  another agent's operational recovery document is left unstaged.

## Steps

- [x] Compare raw baseline Git blobs, all registry/table entries and current files.
- [x] Inspect the rebased source deltas and existing lost-Jev handling read-only.
- [x] Insert a genuine current-main incremental review and update only three hashes.
- [x] Verify preservation, focused tests, plan check and final receipt acceptance.

## How to verify

Use the compatible bundled Node v24.19.0 at
`<home>/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe`.

```text
node --test tools/video/qa/qa.test.mjs tools/video/qa/duration.test.mjs tools/video/core/duration.test.mjs tools/video/long-form/plans.test.mjs tools/video/long-form/integration.test.mjs tools/video/long-form/review.test.mjs
node --test --test-name-pattern "comparison ignores|same-sound characters|Taiwanese particles|closing particles at clause|outside Chinese|zh-CN keeps" tools/video/tts/check.test.mjs
node tools/video/long-form/cli.mjs check
node --test tools/video/long-form/review.test.mjs
node tools/tasks.mjs check
git diff --check
```

The focused suite passed 45/45 and matcher comparisons passed 6/6, zero skips.
The final report-text revision was rechecked with both receipt tests (2/2) and
all 473 plans. Raw baseline and preservation proofs plus command exit records
are retained under
`<home>/mokaair-work/stalled-video-audit-20261008/duration-rebase-20261009`.

## Notes

- Independent reviewer: `codex-local-video-audit-duration-review`; source authors
  are `codex-stalled-video-completion` and `codex-video-audio-matcher`.
- Reviewed source HEAD: 5121d025742b1c88444c61b0d3b7f48bb7796ff5. Actual registered
  deltas are QA CLI, QA tests and TTS check tests. No source file was changed by
  this reviewer; no provider, production or media action was performed.
- Before the review edit, the focused suite passed 44/45; only the expected stale
  receipt case failed. After rebinding, all 45 passed.
- A broader mocked TTS check suite aborted on a Windows speech-journal EPERM
  rename. It is recorded in focused-tests.log and not counted as a passing run;
  the narrower relevant matcher tests and QA/duration suite actually passed.
- This task completes the review and receipt refresh only. PR merge/deployment,
  movie owner playback, language choice and YouTube publication are distinct
  and are not asserted by this task.

2026-10-23 owner-directed narrow C-series handoff: the shared checkout's canonical
`docs/videos/long-form/review.md` and `review.json` were clean. The board steward released
only these two paths for an independent final duration review; the historical review,
remaining task status and checks are preserved. This task now scopes only its own record,
which keeps the still-open review ticket valid without reserving the canonical receipt.


### 2026-10-24 owner-directed reconciliation

站主要求處理全部open任務：不再需要或已有完成證據的項目結案。此為純任務紀錄接手；不接管其他live producer、不改產品scope檔、不發起付費、正式站寫入或YouTube操作。

Disposition: close_completed.

- Main scoped files exist: tasks/open/2026-10-09-duration-review-stalled-fixes-rebase.md
- DoD/Steps 全部勾選；範圍現已只剩此任務記錄。獨立 duration receipt、45/45 focused tests、6/6 matcher comparisons 已記錄；PR #1387 現場確認 2026-10-18 已合併。

以 review-only completed 結案，不聲稱媒體或正式站交付。
