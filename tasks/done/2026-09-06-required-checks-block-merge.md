---
id: 2026-09-06-required-checks-block-merge
title: A failing required check did not stop a merge, and main stayed red
status: done
priority: P1
area: meta
owner: claude-fable-5-1
claimed_at: 2026-09-06T02:29:37Z
created_at: 2026-09-06T00:52:19Z
completed_at: 2026-09-06T02:41:35Z
branch: claude/ci-guards
depends_on: []
scope:
  - .github
---

# A failing required check did not stop a merge, and main stayed red

## Why

On 2026-09-05 pull request #169 was merged while its `api` job was failing. `main` was red
from `76e0e74` and stayed red through two further merges — #170 and #164 — before anyone
noticed. Nothing in the repository stopped any of it: `gh pr merge` was accepted with a
failing check, and the three subsequent pull requests inherited a red base without being told.

The proximate cause was on the human/agent side: the check status was read through
`gh pr checks <n> --watch | tail -6`, which hides rows beyond the last six *and* discards the
command's exit status, because a shell pipeline returns the exit code of its last stage —
`tail`, which always succeeds. Both failing `api` rows were among the hidden ones.

That is a bad habit worth naming, but it is not the fix. The repository should not depend on
whoever presses merge reading the output correctly.

## Definition of done

- [x] A pull request whose `api`, `web`, `containers` or `full-stack-smoke` job is failing
      cannot be merged.
- [x] A pull request whose base is behind a red `main` is visibly distinguishable from one
      that is green.
- [x] The rule is written where it can be found — branch protection is invisible in the tree,
      so if it is configured in the GitHub UI, say so in a file.

## Steps

- [x] Turn the four CI jobs into required status checks on `main` (branch protection, or a
      ruleset). Note this is repository configuration, not a file, so it needs recording:
      a short note in `docs/` or `.github/` saying which checks are required and why.
- [x] Consider requiring branches to be up to date with `main` before merging, which is what
      would have surfaced the red base for #170 and #164.
- [x] Optional but cheap: a scheduled job that opens an issue when `main`'s own CI run fails,
      so a red default branch announces itself rather than waiting to be noticed.

## How to verify

Push a branch with a deliberately failing test, open a pull request, and confirm the merge
button refuses it. Then delete the branch.

## Notes

**Done 2026-09-06.** Branch protection on `main` is set through the REST API: required status
checks `api`, `web`, `containers`, `full-stack-smoke`, `strict: true` (branch must be up to date
with `main`, so a red base is re-checked on the merge result), `enforce_admins: true` (the one
account that merges is an administrator, so without this the rule would bind nobody — and
`gh pr merge --admin` is no longer a way past a red check), no review requirement.
`.github/BRANCH_PROTECTION.md` records the settings, the reason, the reliable way to read a
check, and the exact `gh api` call to change it. `.github/workflows/ci-red-main.yml` opens an
issue labelled `ci-red-main` (or comments on the open one) when the CI run for a push to `main`
fails, which is the scheduled-job idea in a cheaper shape (`workflow_run`, no cron).

Verified with throwaway pull request #185 (a deliberate double alembic head, so `api` was red):
`mergeStateStatus` was `BLOCKED`, `gh pr merge --squash` was refused ("the base branch policy
prohibits the merge") and `--admin` was refused too ("3 of 4 required status checks have not
succeeded"); the pull request was closed and the branch deleted. `strict` means every pull request opened after this must be rebased
onto the current `main` before it can merge, which re-runs CI once per rebase — the cost of
never merging onto a red base again.

The workflow itself is fine and was not the problem: `.github/workflows/ci.yml` runs on both
`push` and `pull_request` with identical steps, and `RUN_INTEGRATION_TESTS: "1"` is set for
both, so pull request checks do exercise the integration suite against Postgres. #169's `api`
job genuinely ran and genuinely failed.

The four assertions that broke are fixed in #172. The reliable way to read check state, for
whoever automates this next:

```bash
SHA=$(gh pr view <n> --json headRefOid -q .headRefOid)
gh api "repos/<owner>/<repo>/commits/$SHA/check-runs" \
  -q '.check_runs[] | "\(.name)\t\(.status)\t\(.conclusion)"'
```

Never pipe `gh pr checks --watch` into `tail` or `head`.
