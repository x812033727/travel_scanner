---
id: 2026-09-13-pin-actions-and-dependency-updates
title: Pin GitHub Actions to commit SHAs and add automated dependency updates
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-09-13T23:37:46Z
completed_at:
branch:
depends_on: []
scope:
  - .github/workflows
  - .github/dependabot.yml
---

# Pin GitHub Actions to commit SHAs and add automated dependency updates

## Why

Every workflow references third-party and first-party actions by a mutable tag:
`actions/checkout@v4`, `actions/setup-node@v4`, `actions/upload-artifact@v4`,
`actions/github-script@v7`, `astral-sh/setup-uv@v6`. A tag is a pointer the action's
owner can move, so whatever `v4` resolves to on the day a job runs is what executes —
with the repository checked out and, in `live-provider-validation.yml` and
`airline-crawler-validation.yml`, with provider API keys in the environment.

`deployment_agent/executor.py` gates deployment on CI being green, and
`.github/BRANCH_PROTECTION.md` records that `main` requires those same CI jobs. So the CI
runner is on the path to production: an action that changes under a tag runs inside the
thing that decides what gets deployed.

Nothing here has gone wrong. This is the supply-chain half of a posture that is otherwise
already careful — both lock files are hash-pinned and installed frozen, `npm audit` and
`pip-audit` run on every push, and secret-carrying workflows are `workflow_dispatch`-only
so a fork pull request cannot reach them. Actions are the one dependency class still
floating.

The same gap has a second half: there is no `dependabot.yml` and no Renovate config, so
nothing opens a pull request when a dependency ships a fix. Today both audits are clean,
which is the good time to automate it rather than the bad one.

`docs/security-audit-2026-09.md` filed this as INF-08 and recommendation #6.

## Definition of done

- [ ] Every `uses:` in `.github/workflows/` names a 40-character commit SHA, with the
      human-readable version in a trailing comment.
- [ ] Dependabot (or Renovate) opens pull requests for npm, uv/pip and GitHub Actions, and
      the actions ecosystem is included so the pins above stay current rather than frozen.
- [ ] CI is green on the pinned workflows.

## Steps

- [ ] For each action, resolve the tag to the SHA it points at today and record it as
      `uses: actions/checkout@<sha> # v4.2.2`. Do this per action, not per occurrence, so
      the same action is the same SHA everywhere.
- [ ] Add `.github/dependabot.yml` with three ecosystems: `npm` (root and `apps/web`),
      `uv` or `pip` for `apps/api`, and `github-actions`. Weekly is enough.
- [ ] Decide the review posture and write it in the Dependabot config comment: pinning
      without automated updates trades one risk for staleness, which is the failure mode
      this pairing exists to avoid.

## How to verify

```bash
python3 -c "import yaml,glob; [yaml.safe_load(open(f)) for f in glob.glob('.github/workflows/*.yml')]"
npm run check:tasks
```

Then push the branch and confirm every job still starts and passes — a mistyped SHA fails
at the `uses:` resolution step, immediately and loudly.

## Notes

- `actions/*` is GitHub's own namespace and lower risk than `astral-sh/setup-uv`, but
  pinning selectively invites the question of where the line is on every future addition.
  Pin all of them.
- Filed by the 2026-09-13 security review (`docs/security-review-2026-09-13.md`).
