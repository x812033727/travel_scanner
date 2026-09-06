---
id: 2026-09-06-required-checks-block-merge
title: A failing required check did not stop a merge, and main stayed red
status: open
priority: P1
area: meta
owner:
claimed_at:
created_at: 2026-09-06T00:52:19Z
completed_at:
branch:
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

- [ ] A pull request whose `api`, `web`, `containers` or `full-stack-smoke` job is failing
      cannot be merged.
- [ ] A pull request whose base is behind a red `main` is visibly distinguishable from one
      that is green.
- [ ] The rule is written where it can be found — branch protection is invisible in the tree,
      so if it is configured in the GitHub UI, say so in a file.

## Steps

- [ ] Turn the four CI jobs into required status checks on `main` (branch protection, or a
      ruleset). Note this is repository configuration, not a file, so it needs recording:
      a short note in `docs/` or `.github/` saying which checks are required and why.
- [ ] Consider requiring branches to be up to date with `main` before merging, which is what
      would have surfaced the red base for #170 and #164.
- [ ] Optional but cheap: a scheduled job that opens an issue when `main`'s own CI run fails,
      so a red default branch announces itself rather than waiting to be noticed.

## How to verify

Push a branch with a deliberately failing test, open a pull request, and confirm the merge
button refuses it. Then delete the branch.

## Notes

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
