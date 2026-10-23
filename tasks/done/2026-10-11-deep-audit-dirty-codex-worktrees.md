---
id: 2026-10-11-deep-audit-dirty-codex-worktrees
title: Deep audit dirty changes in 22 Codex worktrees
status: done
priority: P2
area: meta
owner: codex-dirty22-audit
claimed_at: 2026-10-11T14:48:35Z
created_at: 2026-10-11T14:48:34Z
completed_at: 2026-10-11T15:11:29Z
branch:
depends_on: []
scope:
  - tasks/open/2026-10-11-deep-audit-dirty-codex-worktrees.md
  - tasks/done/2026-10-11-deep-audit-dirty-codex-worktrees.md
  - tasks/worktree-dirty22-20261011.md
  - tasks/open/2026-10-10-resume-deterministic-video-production-blockers.md
  - tasks/open/2026-10-10-whisper-pyav19-second-opinion.md
  - tasks/open/2026-10-11-migrate-frozen-embedding-helper-dependency.md
  - tasks/evidence/worktree-cleanup/2026-10-10-production-resume.original.md
---

# Deep audit dirty changes in 22 Codex worktrees

## Why

The owner asked to distinguish already integrated edits, temporary files, incomplete work and active dependencies before retiring completed Codex checkouts. Claude and Ou de Jianghu are excluded.

## Definition of done

- [x] Classify every dirty path in the frozen 22-root cohort against main, replacement PRs and owner evidence.
- [x] Fully preserve and restore-check eligible roots, recheck current use and remove only completed unused checkouts.
- [x] Preserve unfinished work and record concrete next actions in the shared queue.

## Steps

- [x] Audit 4,454 paths across 22 roots; independently review destructive guards.
- [x] Remove four exact roots and local refs; retain eighteen.
- [x] Restore two missing original tasks and a byte-identical operational receipt; file a narrow frozen-helper dependency follow-up.

## How to verify

Read `tasks/worktree-dirty22-20261011.md` and the local scratch report / recovery / execution / retained-verification receipts. Run `node tools/tasks.mjs check` and `git diff --check`. Product tests do not apply to this metadata-only change.

## Notes

Source-complete roots are not automatically unused. b136 has a real absolute-path dependency enforced by the frozen Embedding executor. Foods/maps hit a OneDrive read-only directory error; exact residues were verified against the backup and separately cleared, with both failure and recovery receipts retained. No product, provider, production or Claude work was performed.
