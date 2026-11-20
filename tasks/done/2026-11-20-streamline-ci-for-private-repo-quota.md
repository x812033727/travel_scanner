---
id: 2026-11-20-streamline-ci-for-private-repo-quota
title: Streamline CI for private repo quota and add Google Drive multi-agent workspace capsule
status: done
priority: P1
area: ops
owner: antigravity
claimed_at: 2026-11-20T01:51:52Z
created_at: 2026-11-20T01:51:30Z
completed_at: 2026-11-20T01:59:26Z
branch: antigravity/private-ci-and-drive-workspace
depends_on: []
scope:
  - .github/BRANCH_PROTECTION.md
  - .github/workflows/auto-update-branches.yml
  - .github/workflows/ci.yml
  - .github/workflows/food-map-reservations.yml
  - .github/workflows/npm-audit.yml
  - .github/workflows/pip-audit.yml
  - .github/workflows/planner-premium.yml
  - .github/workflows/seo-audit.yml
  - .github/workflows/travel-discovery.yml
  - AGENTS.md
  - CLAUDE.md
  - GEMINI.md
  - ops/backup/README.md
  - ops/backup/manifest-paths.txt
  - package.json
  - tools/skills.test.mjs
  - tools/workspace-sync.mjs
  - tools/workspace-sync.test.mjs
---

# Streamline CI for private repo quota and add Google Drive multi-agent workspace capsule

## Why

The owner plans to switch `x812033727/travel_scanner` to a private repository on GitHub Pro (3,000 Actions minutes/month) without running CI on the production VPS, and wants deeper reliance on cloud accounts and Google Drive so Claude Code, Codex and Gemini (`agy` / Antigravity) can share workspaces and subscription accounts seamlessly.

Currently a single PR push bills ~140 Actions minutes (`ci.yml` 17 jobs = ~104 min plus 4 unconditional companion E2E/Lighthouse workflows = ~36 min), merging to `main` repeats the entire 140-minute run, `strict: true` forces every open PR to rebase and re-run CI whenever any topic-pool or task PR merges, and `auto-update-branches.yml` polls every 10 minutes (4,320 min/month). At ~150 PRs/month (~55,000 min/month), GitHub Pro's 3,000-minute monthly quota would be exhausted in 1–2 days.

For multi-agent collaboration, placing a live `.git` checkout and `node_modules`/`.venv` directly on a mounted Google Drive folder causes `.git/index.lock` `EPERM` races, 100k-file rate-limit stalls and split-brain corruption. Instead, we need a lightweight Google Drive workspace capsule (`npm run ws`, synced to `AI/工作區/<id>/`) carrying `wip.patch`, `untracked/`, `HANDOFF.md` and `meta.json`, unified root instructions (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`), and encrypted nightly backup of `/var/lib/mokaair-ai-accounts`.

## Definition of done

- [x] `ci.yml` detects changed paths in a lightweight `changes` job: `push` to `main` fast-passes in 1 billed minute (unless `[full-ci]` is in the commit message) so `ops/autodeploy` sees `CI` green without re-running 17 jobs; topic-pool / task-board / docs / skills PRs skip heavy Postgres/Chromium shards while still testing `test_video_pools.py` and `test_video_backup.py` when pool/backup metadata changes; `web-unit` runs inside `web-checks` and `api-tests`/`web-e2e` run in 2 shards instead of 4/3.
- [x] `seo-audit.yml`, `food-map-reservations.yml`, `planner-premium.yml` and `travel-discovery.yml` run on `workflow_dispatch` instead of every push/PR; `npm-audit.yml` and `pip-audit.yml` run weekly instead of daily; `auto-update-branches.yml` drops its 10-minute cron and lowers `MAX_INFLIGHT` to `"1"`; `.github/BRANCH_PROTECTION.md` documents `strict: false` and the private-repo CI budget.
- [x] `tools/workspace-sync.mjs` (`npm run ws`) supports `status`, `push`, `pull`, `list` and `delegate` against local Drive paths or `rclone` (`videobackup:工作區`), with unit tests in `tools/workspace-sync.test.mjs`.
- [x] `CLAUDE.md` and `GEMINI.md` mirror `AGENTS.md` at the repository root (enforced by `tools/skills.test.mjs`), and `ops/backup/manifest-paths.txt` includes `/var/lib/mokaair-ai-accounts` so all 20 subscription slots (Claude, Codex, Antigravity `agy`, Colab) are backed up in `config.tar.age` to Google Drive.

## Steps

- [x] Streamline `.github/workflows/ci.yml`, companion workflows, `auto-update-branches.yml` and `.github/BRANCH_PROTECTION.md`.
- [x] Implement `tools/workspace-sync.mjs`, `tools/workspace-sync.test.mjs` and wire `npm run ws` in `package.json`.
- [x] Update `AGENTS.md`, synchronize `CLAUDE.md` and `GEMINI.md`, and add the root agent-guide parity assertion to `tools/skills.test.mjs`.
- [x] Add `/var/lib/mokaair-ai-accounts` to `ops/backup/manifest-paths.txt` and document it in `ops/backup/README.md`.
- [x] Run `npm run test:tools`, `npm run check:tasks` and `python3 -m unittest discover -s ops/backup -v`.

## How to verify

```bash
npm run test:tools
npm run check:tasks
python3 -m unittest discover -s ops/backup -v
npm run ws -- status
```

## Notes

- Claimed with `--force` over `2026-10-14-curio-episodes-keep-the-series-look`, which is an 875-hour stale claim (`[not found anywhere]`) that listed `AGENTS.md` in its scope.
