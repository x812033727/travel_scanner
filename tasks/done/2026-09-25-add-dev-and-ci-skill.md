---
id: 2026-09-25-add-dev-and-ci-skill
title: Add the dev-and-ci skill
status: done
priority: P2
area: tools
owner: claude-opus-5-5-dev-and-ci
claimed_at: 2026-09-25T15:09:46Z
created_at: 2026-09-25T15:09:37Z
completed_at: 2026-09-25T15:19:40Z
branch: claude/skill-dev-and-ci
depends_on: []
scope:
  - .agents/skills/dev-and-ci
  - .claude/skills/dev-and-ci
---

# Add the dev-and-ci skill

## Why

How to run the checks on this Windows setup, how to read their exit codes, which CI failures
are known flakes and how to judge the weekly Dependabot pull requests all lived in one
person's session memory, spread over seven long notes. Every new session re-derived it, and
the same mistakes came back: a check piped through `| tail` read as passing, a worktree
without its own `npm ci` tested against a months-old `node_modules`, a load-only vitest flake
was "fixed" with a longer wait. Codex and Claude Code both need this, so it belongs in a
shared repository skill that loads on demand.

## Definition of done

- [x] `.agents/skills/dev-and-ci/SKILL.md` covers setup, the checks, reading exit codes, CI
      triage and Dependabot as numbered steps with commands, and points at references for detail.
- [x] `.claude/skills/dev-and-ci/SKILL.md` is a byte-identical copy.
- [x] Every command, path and flag in it was checked against the current tree, not copied
      from memory.
- [x] `node --test tools/skills.test.mjs` passes.

## Steps

- [x] Read the seven source notes, `AGENTS.md` and `.github/workflows/ci.yml`.
- [x] Verify each fact against the code (scripts, package versions, test files, helper paths).
- [x] Write `SKILL.md`, five references and `scripts/run-checks.sh`.
- [x] Run the skill test and the script's `tools` group.

## How to verify

```bash
node --test tools/skills.test.mjs
bash .agents/skills/dev-and-ci/scripts/run-checks.sh tools   # prints exit= per check and a summary
```

## Notes

- Stale facts found while verifying, and corrected in the skill:
  - The four API test files once ignored on Windows (`test_deployment_center.py`,
    `test_deployments_integration.py`, `test_integration_postgres_redis.py`,
    `test_warning_codes.py`) now collect and pass there: the deployment agent falls back to TCP
    when `socketserver.UnixStreamServer` is missing. No `--ignore` is needed.
  - CI no longer runs a `push` event for pull-request branches (only `main`), and a new push
    cancels the previous run of the same PR, so "two rows per job" no longer applies to PRs.
  - redis-py 8 and mypy 2 are no longer held majors (`redis>=8.1,<9`, `mypy>=2.3,<3`); only
    ESLint 10 and TypeScript 7 stay blocked, each with its own ticket.
  - `--allow-escape-sequences` is a `gh api` flag; `gh run view --log` does not have it.
  - The `server-only` sitemap example test lives at `apps/web/app/sitemaps/sitemap.test.ts`.
- Running `run-checks.sh tools` in a worktree without `npm ci` failed `test:tools` on missing
  `pinyin-pro` and fonts, which is the stale-`node_modules` rule the skill describes.
- Left out on purpose: i18n key parity and locale-redirect checks (the `web-i18n-e2e` skill),
  migration numbering and session-helper rules (`backend-conventions`), host `plink` surveys
  (`prod-host-ops`), the merge loop (`task-board`).
