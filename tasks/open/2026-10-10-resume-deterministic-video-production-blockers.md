---
id: 2026-10-10-resume-deterministic-video-production-blockers
title: Resume deterministic video production blockers
status: in-progress
priority: P1
area: ops
owner: codex-3603
claimed_at: 2026-10-10T11:21:36Z
created_at: 2026-10-10T11:20:59Z
completed_at:
branch: codex/stalled-production-resume-20261010
depends_on: []
scope:
  - docs/videos/recovery/2026-10-10-production-resume.md
---

# Resume deterministic video production blockers

## Why

The owner asked to continue stalled production and explicitly reserved the active
published-dub campaign to its existing chat. Seven other worker projects have
deterministic blockers: four unvoiced drafts and two captions tails reject the
shared dictionary's numeric-leading aliases; ICANN also fails the final AAC peak.

## Definition of done

- [ ] Complete the existing ICANN assembly and retain normal final-quality gates.
- [ ] Finish the two already-approved movies' captions/package tails where their selected parts permit it.
- [ ] Resume the four drafts through normal fact/listener verification and media stages, or record the exact remaining owner/service gate without replaying uncertain requests.
- [ ] Preserve other chat's sources, shared dictionary, campaign and provider receipts.

## Steps

- [x] Audit current worker state, backend reviews and saved source/media hashes.
- [x] Confirm actual `8B` and `6abc` values, affected speech hashes and the shared-dictionary collision.
- [ ] Run source-bound private helpers with ordinary project leases and checks.
- [ ] Read back resulting files, reviews and persisted stage state.

## How to verify

Private audit namespace: `stalled-video-resume-20261010-3603`. The initial
read-only preflight binds current source and media hashes, real lint errors and
the normal validator's result after removing only the two invalid aliases from
an in-memory copy. Every producer must persist actual command exits, read back
checks and approvals, and retain the original dictionary bytes. Do not equate a
successful render, pending review or automatic QA with owner playback or upload.

## Notes

- Live snapshot: 2026-10-10 19:24 Taipei, host `1bd1d47c`; worker and AI worker running.
- The original six-film batch has newer completed delivery evidence and is outside this task.
- `8B` and `6abc` are string aliases, not null. Removing them changes the planned speech hash for two drafts without audio; the other five target hashes remain identical. No existing audio may inherit a changed speech hash.
- Shared dictionary is pinned by another active campaign. This task must use private input shelves, with unchanged source/media evidence for the three already-voiced movies.
- PR #1423 contains the proposer fix but is not yet merged; no competing source fix is needed. PR #1387 contains the tested narrow AAC join limiter; only a private source-bound implementation may be reused here.
- All unknown writer/verifier and Meta caption jobs, Mods STOP, dropped projects, Shorts and airport-series drafts stay outside the selected seven-film cohort.

## Recovery provenance (2026-10-11)

- 原文與原 front matter 完整保留；本次僅追加此復原出處。created_at、claimed_at、owner、status、branch、scope 及原 checklist 均未改動；沒有重新認領、釋放或結案。
- 原檔：`<home>/.codex/worktrees/3603/travel_scanㄐ/tasks/open/2026-10-10-resume-deterministic-video-production-blockers.md`；分支 `codex/stalled-production-resume-20261010`；HEAD `1bd1d47ceab109b1425af01f1571173e95004c8e`。此檔在該 checkout 是未追蹤原稿。
- 原檔 SHA-256：`7cc25767a4ac843cffac524ecbacefacbbf50dc3de276888de8e28225f3fa870`；原始大小 3052 bytes；原文字節副本保存在清理備份及 scratch `prepared-tasks/originals/2026-10-10-resume-deterministic-video-production-blockers.md`。
- 比對基準：main `9c46c14ed5c22388be68dec8301695667a226bee`；此 ID 未見於 main、清理工作區的既有任務及 PR #1450 的 `8a8b64782c5ef9e5ab5a3bc17fd1c3e28ffaae69` 快照。整合前再核對最新 main / PR，若已有同 ID 只合併本段出處，不另開票。
- 完整 operational receipt 原始 archive：`tasks/evidence/worktree-cleanup/2026-10-10-production-resume.original.md`；SHA-256 `f1f278888a2a763a3fc5d4455c721baaa533b1ba41896616a1cf776e6edd8a8a`（14616 bytes）。本輪只保全原始收據，不寫入原 owner scope `docs/videos/recovery/2026-10-10-production-resume.md`。原收據的最後更新記錄至 2026-10-10 21:14 Taipei，不代表此刻程序或製作仍在執行。
- 原票中的「目前」、PR 狀態、claim 衝突及主機狀態都是當時快照。續作前應唯讀核對現有 owner、相同 scope、已知 job / source / review hashes、STOP 與 lease，沿用收據而非重買或重跑未知請求。恢復票不構成 provider / 正式站 / 發布的新授權。
- 21:05 的私人 PyAV 19 四段相容性 pilot 為 exit 0，SHA-256 `ae10fbf530d91f0e0059feb318f2ca4a7b2c23f032ddbb43e7047b38c95637b3`；此證據僅適用原輸入與私有 per-process shim，沒有證明 installed worker 或其他 campaign 已完成修補。21:14 的 V5 JA/EN 啟動記錄尚不等於正常音訊 QA、owner playback、上傳或公開。
