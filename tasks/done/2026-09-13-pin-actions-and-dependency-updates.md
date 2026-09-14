---
id: 2026-09-13-pin-actions-and-dependency-updates
title: Pin GitHub Actions to commit SHAs and add automated dependency updates
status: done
priority: P2
area: ops
owner: claude-opus-5
claimed_at: 2026-09-14T00:38:04Z
created_at: 2026-09-13T23:37:46Z
completed_at: 2026-09-14T06:20:48Z
branch: claude/security-check-o5zaj1
depends_on: []
scope:
  - .github/workflows
  - .github/dependabot.yml
  - tools/workflow-pins.test.mjs
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

- [x] Every `uses:` in `.github/workflows/` names a 40-character commit SHA, with the
      human-readable version in a trailing comment.
- [x] Dependabot opens pull requests for npm, uv and GitHub Actions, and the actions
      ecosystem is included so the pins stay current rather than frozen.
- [x] CI is green on the pinned workflows: merged PR #472 at 24af149062dd99aad3f4c2bb16cea70f8edf164c;
      GitHub CI run 34808942136 completed successfully (verified 2026-09-14).

## Steps

- [x] Resolved each tag in use to the commit it points at today, via `git ls-remote`, and
      applied it per action rather than per occurrence. `astral-sh/setup-uv@v6` is an
      annotated tag, so it was peeled to the commit rather than pinned to the tag object.
- [x] Added `.github/dependabot.yml` with npm (workspace root), uv (`/apps/api`) and
      github-actions, weekly, with minor and patch grouped into one pull request each.
- [x] Wrote the review posture into the config comment: pinning without updates trades a
      supply-chain risk for a staleness one, which is why the two ship together.
- [x] Added `tools/workflow-pins.test.mjs` so the pins survive. An unpinned action is
      invisible in review, which is how this would come back.

## The pins

Each tag resolved on 2026-09-14. Nothing was upgraded — every pin is the commit the tag
already pointed at, so this change is a no-op at runtime.

| Action | Was | Now | Version |
| --- | --- | --- | --- |
| `actions/checkout` | `@v4` | `11d5960a326750d5838078e36cf38b85af677262` | v4.4.0 |
| `actions/setup-node` | `@v4` | `49933ea5288caeca8642d1e84afbd3f7d6820020` | v4.4.0 |
| `actions/upload-artifact` | `@v4` | `ea165f8d65b6e75b540449e92b4886f43607fa02` | v4.6.2 |
| `actions/github-script` | `@v7` | `f28e40c7f34bde8b3046d885e986cb6290c5673b` | v7.1.0 |
| `astral-sh/setup-uv` | `@v6` | `d0cc045d04ccac9d8b7881df0226f9e82c39688e` | v6.8.0 |

## How to verify

```bash
npm run test:tools
python3 -c "import yaml,glob; [yaml.safe_load(open(f)) for f in glob.glob('.github/workflows/*.yml')]"
python3 -c "import yaml; yaml.safe_load(open('.github/dependabot.yml'))"
```

Then push and confirm every job still starts: a mistyped SHA fails at `uses:` resolution,
immediately and loudly, before any step runs.

## Notes

- All five actions were already on their latest major except `actions/checkout`,
  `actions/setup-node`, `actions/upload-artifact` and `actions/github-script`, which have
  newer majors (v7, v7, v7, v9). Upgrading was deliberately left out: this change is meant to
  be behaviour-preserving, and Dependabot will now propose those majors one at a time with CI
  to judge them.
- Only `apps/api` gets a `uv` entry. The npm workspace has one lock file at the root that
  covers `apps/web`, so a second npm entry pointing there would find nothing to update.
- Filed by the 2026-09-13 security review (`docs/security-review-2026-09-13.md`).
- Closed the stale review state after verifying merged PR and exact-main green CI.
  A Windows-only file-URL parsing defect discovered during AI-series integration is
  tracked separately in 2026-09-14-workflow-pin-tests-use-file-url.
