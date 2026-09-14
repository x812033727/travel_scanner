---
id: 2026-09-14-codex-upstream-integration
title: Integrate current main into the Codex learning branch
status: done
priority: P1
area: web
owner: codex-upstream-integration-fc2e
claimed_at: 2026-09-14T16:57:09Z
created_at: 2026-09-14T16:57:01Z
completed_at: 2026-09-14T17:18:28Z
branch: codex/codex-learning-complete
depends_on: []
scope:
  - apps/api/app/guides/content/codex-cli-getting-started.json
  - apps/api/app/guides/content/codex-cloud-tasks-github.json
  - apps/api/app/guides/schemas.py
  - apps/api/tests/test_guide_series.py
  - apps/api/tests/test_codex_learning.py
  - apps/web/components/planner-overlay.tsx
  - apps/web/components/planner-overlay.test.tsx
  - apps/web/components/route-mode-panel.tsx
  - apps/web/components/route-mode-panel.test.tsx
  - apps/web/lib/modal-sheet.ts
  - apps/web/lib/modal-sheet.test.tsx
  - apps/web/lib/content-blocks.ts
  - apps/web/public/guides/codex-cli-getting-started
  - apps/web/public/guides/codex-cloud-tasks-github
  - tasks/done/2026-09-11-modal-escape-flake-under-load.md
  - tasks/done/2026-09-13-life-ai-batch-04.md
  - docs/codex-learning
---

# Integrate current main into the Codex learning branch

## Why

The Codex branch was based before merged PR #493 and reproduced its already-fixed modal timing defects. Current main also contains the expanded Claude series and two older AI-batch Codex packs at the same stable CLI/cloud slugs. Integrate the current shared code and preserve the five-language Codex series without duplicate articles or duplicate modal fixes.

## Definition of done

- [x] Current main is merged locally, with no unresolved conflicts or duplicate task IDs.
- [x] Modal runtime/tests match the upstream fix; two comment labels use English for the i18n checker, and independent diagnostic history is retained as history.
- [x] Codex CLI/cloud retain the existing five-language lesson identities and reviewed assets.
- [x] Shared content schemas accept both Codex and Claude formats and affected checks pass.

## Steps

- [x] Inspect merge-tree conflicts and verify PR #493 is merged; stop the obsolete-baseline test repetition.
- [x] Resolve exact conflicts, validate and record the resulting integration commit.

## How to verify

Run affected frontend, API/series and Codex content checks, then one complete frontend suite. Check task consistency and conflict markers. Compare all 61 Codex pack hashes and reused slug/assets against the pre-merge source. No preview server, PR, publication or deployment is part of this integration task.

## Notes

The original series task remains blocked by prior article/preview auto-review denials. This bounded merge task does not retry those operations. The prior modal task is already done on main; its source and recorded CI should be reused, not reopened as an outstanding production defect. Local commit 00a513c5 preserves the independent four-case diagnosis, and its first full-suite attempt was deliberately interrupted before completion when the upstream fix was discovered.

Merged main 3d1df9cc locally as be815096. Preserved all 61 Codex pack hashes and the current exercise ZIP. The shared schema keeps all required code labels. The Claude catalogue test now selects its series among the Codex locales and verifies 96 entries/16 groups/12 paths. Existing upstream task completions were retained.

The first API integration run found incompatible CRLF expectations plus two expired fixtures based on the local date. The Codex test now follows the shared API's existing LF contract, with exact markup/indentation/trailing newline assertions; expiry fixtures use the same UTC clock as publication. Retest: 46 passed / 19 PostgreSQL skips (112.05s). Ruff, mypy (328 source files), web lint/typecheck, five-locale i18n, 52 tool tests, 60-lesson compilation, 300 localized lesson integrity and 451-task checks pass. The full frontend result is recorded below. Evidence: docs/codex-learning/evidence/upstream-integration-validation.json.

Final frontend validation on the unchanged be815096 source: 261 files / 2,829 tests passed in 735.38 seconds, exit 0. Complete output is retained as frontend-validation-20260915/post-main-full.log.gz with verified raw/compressed hashes and run timestamps. This completes the local integration task only. Original pending article/hub edits, final page acceptance and all PR/publication/deployment gates remain open in the Codex series tasks; no rejected action was retried.

The task completion command left both open and done files, matching the already-filed 2026-09-14-investigate-windows-task-archive-leftover-open task. After verifying identical task bodies, the exact obsolete open file was removed. The final task check again passes for 451 files; the underlying archival-tool issue remains in its existing task.
