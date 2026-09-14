---
id: 2026-09-14-codex-upstream-integration
title: Integrate current main into the Codex learning branch
status: in-progress
priority: P1
area: web
owner: codex-upstream-integration-fc2e
claimed_at: 2026-09-14T16:57:09Z
created_at: 2026-09-14T16:57:01Z
completed_at:
branch: codex/codex-learning-complete
depends_on: []
scope:
  - apps/api/app/guides/content/codex-cli-getting-started.json
  - apps/api/app/guides/content/codex-cloud-tasks-github.json
  - apps/api/app/guides/schemas.py
  - apps/api/tests/test_guide_series.py
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

- [ ] Current main is merged locally, with no unresolved conflicts or duplicate task IDs.
- [ ] Modal sources/tests match the upstream fix; independent diagnostic history is retained as history.
- [ ] Codex CLI/cloud retain the existing five-language lesson identities and reviewed assets.
- [ ] Shared content schemas accept both Codex and Claude formats and affected checks pass.

## Steps

- [x] Inspect merge-tree conflicts and verify PR #493 is merged; stop the obsolete-baseline test repetition.
- [ ] Resolve exact conflicts, validate and record the resulting integration commit.

## How to verify

Run affected frontend, API/series and Codex content checks, then one complete frontend suite. Check task consistency and conflict markers. Compare all 61 Codex pack hashes and reused slug/assets against the pre-merge source. No preview server, PR, publication or deployment is part of this integration task.

## Notes

The original series task remains blocked by prior article/preview auto-review denials. This bounded merge task does not retry those operations. The prior modal task is already done on main; its source and recorded CI should be reused, not reopened as an outstanding production defect. Local commit 00a513c5 preserves the independent four-case diagnosis, and its first full-suite attempt was deliberately interrupted before completion when the upstream fix was discovered.
