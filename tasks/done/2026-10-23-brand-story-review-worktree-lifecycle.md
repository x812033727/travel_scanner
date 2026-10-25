---
id: 2026-10-23-brand-story-review-worktree-lifecycle
title: Reuse brand-story review checkout and clean finished review worktrees
status: done
priority: P1
area: docs
owner: codex-gpt6-brand-story-lifecycle
claimed_at: 2026-10-23T08:39:01Z
created_at: 2026-10-23T08:38:56Z
completed_at: 2026-10-23T08:41:35Z
branch: codex/brand-story-review-workspace-lifecycle-20261023
depends_on: []
scope:
  - .agents/skills/brand-story/SKILL.md
  - .claude/skills/brand-story/SKILL.md
  - tasks/open/2026-10-23-brand-story-review-worktree-lifecycle.md
  - tasks/done/2026-10-23-brand-story-review-worktree-lifecycle.md
---

# Reuse brand-story review checkout and clean finished review worktrees

## Why

Brand-story reviews repeatedly created complete Git worktrees for read-only source checks,
blind reads and visual deltas. The owner observed 85 new copies consuming about 55.6 GB
in two hours on 2026-10-23. Independent judgments require isolated inputs and locked
verdicts, not separate copies of the repository.

## Definition of done

- [x] Brand-story skill tells reviewers to read an immutable commit through one shared
  checkout, without creating a worktree for each review.
- [x] The skill states a closeout check for any exceptional temporary worktree and
  requires its safe removal when the review is finished.

## Steps

- [x] Add the shared workspace and cleanup rule to both byte-identical skill copies.
- [x] Check both skill hashes, task metadata and diff; submit a narrow draft PR.

## How to verify

Compare the two skill file hashes; run `npm run test:tools` and
`npm run check:tasks`; review the PR diff for only these two skills and this ticket.

## Notes

This ticket changes future review procedure. It does not authorize deleting any
specific old worktree without a fresh clean/pushed/idle and ignored-file audit.
The current Codex subagents have finished; the app thread list showed this brand-story
chat as the only active local thread at the time of filing. AGENTS.md is held by another
active task, so this rule belongs in the brand-story skill.

Verification: both skill copies SHA-256 `1214E4F7044A09916BFF2263D40F6745E01B9807912CD0C7810D05D4B47A4E11`;
`npm run check:tasks` validated 2103 task files; `git diff --check` passed.
`npm run test:tools` and its focused `tools/skills.test.mjs` could not load
dependencies (`@playwright/test`, `pinyin-pro`, `js-yaml`) in this sparse checkout.
No dependency installation was done because that would add disk use during this fix.
