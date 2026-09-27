---
id: 2026-09-25-patch-deploy-task-board-skills
title: Fill the deploy and task-board skills with what only memory knew
status: done
priority: P2
area: tools
owner: claude-opus-5-5-patch-deploy-task-board-skills
claimed_at: 2026-09-25T15:16:28Z
created_at: 2026-09-25T15:16:05Z
completed_at: 2026-09-25T15:18:30Z
branch: claude/patch-deploy-task-board-skills
depends_on: []
scope:
  - .agents/skills/deploy
  - .claude/skills/deploy
  - .agents/skills/task-board
  - .claude/skills/task-board
---

# Fill the deploy and task-board skills with what only memory knew

## Why

The shared `deploy` and `task-board` skills are what Codex and Claude read before a
deploy or a merge, but a coverage audit against the owner's personal memory notes found
about thirty lessons that only lived in those notes: how the permission classifier
treats merges, pushes to another session's branch, admin forms and even read-only
preflights; how to reach the Hostinger console and revive sshd; how to diagnose and
repair a umask-broken tree; why new seeded hotspots are listed but unusable; the
asynchronous `gh pr update-branch` and the cancelled-run exit 4/7 of
`merge-when-green.sh`; and a stacked-PR sync advice that resurrected done tickets.
Anyone without that memory repeats the mistakes.

## Definition of done

- [x] Every coverage-report item whose target is inside `deploy` or `task-board` is
  either written into the skill or listed below as skipped with a reason.
- [x] The two stale statements are corrected: "background watch-and-merge is always
  blocked" (merge.md) and "`git merge origin/main` for a stacked branch" (merge.md).
- [x] `.claude/skills/*/SKILL.md` stay byte-identical to `.agents/skills/*/SKILL.md`.

## Steps

- [x] deploy/SKILL.md stage 2: check whether a deploy is needed before asking (item 9).
- [x] deploy runbook: mode selector / Ctrl+Shift+M and back to Auto (1), read-only
  preflight also blocked (71), `--profile news`/`--profile video` (70).
- [x] deploy pitfalls: psql select blocked once (2), admin form routes (5), final publish
  button (6), SSH lockout / console / sshd (11–13), umask diagnosis and manual repair
  (15–16).
- [x] deploy post-deploy: unusable seeded hotspots (17), foods sheet check (18), #418
  softened (19), audit method (20).
- [x] task-board SKILL rule 6 and merge.md: standing-instruction merge rule (3), sweep
  grouping (26), async update-branch (27), cancelled run exit 4/7 (28), `--ours` (29),
  stacked PR via `checkout -B` + cherry-pick (67), migration number and 32-char id
  (68, 85).
- [x] collisions.md: push to another session's PR branch (4), count sessions and split
  by lane (21), land re-scopes fast (22), two-session handover (23), rebase-merge
  illusion (25).

## How to verify

```bash
node --test tools/skills.test.mjs
npm run check:tasks
git diff origin/main -- .agents/skills/deploy .agents/skills/task-board
```

## Notes

- Verified against origin/main: `merge-when-green.sh` exit codes 4 (failed incl.
  cancelled) and 7 (other mergeStateStatus such as BLOCKED); `ci.yml` concurrency
  `ci-pr-<n>` with cancel-in-progress on pull_request; `tests/test_schema.py` asserts
  the head revision is at most 32 chars; `seed_catalog`, `due_refresh_targets` (inner
  join), `refresh_due_map_place_ids` (verified only), `enrichment_targets` (outer
  join), `is_durable_coordinate_source` (type and https URL) and the foods sheet
  labels all exist as described. `docker-compose.prod.yml` has `news` and `video`
  profiles; the host script itself is not in git, so the runbook tells readers to grep it.
- Skipped: 7 (memory-file appends; generic, optional), 14 (already in merge.md
  §合併之後), 24 (optional; `--body-file`/`gh api --input` already covered), 8, 10
  (target content-pipeline only), 33 and 66 (primary target in content-pipeline and
  youtube-video; left there to avoid duplicating).
- The `description:` lines were not touched (PR #767 rewrites them).
