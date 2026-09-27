# Branch protection on `main`

Branch protection is repository configuration, not a file, so this note is the only
place in the tree that says what is set and why. If the settings and this file ever
disagree, the settings are what actually happens; fix whichever one is wrong.

## What is set

Configured on 2026-09-06 through the REST API
(`PUT /repos/x812033727/travel_scanner/branches/main/protection`):

| Setting | Value | Why |
| --- | --- | --- |
| Required status checks | `api`, `web`, `containers`, `full-stack-smoke` | The four jobs of `.github/workflows/ci.yml`. A pull request with any of them failing cannot be merged. |
| Require branches to be up to date (`strict`) | on | A pull request opened against a base that later turned red is re-checked on the merged result, and a branch that is behind must rebase before it can merge. This is what would have shown #170 and #164 that their base was already red. |
| Enforce for administrators | on | The one account that merges here is an administrator; without this the rule would apply to nobody. `gh pr merge --admin` is therefore not a way around a red check. |
| Required reviews | none | One person works on this repository; a review requirement would only ever be self-approved. |
| Force pushes / deletions | off | Default. |

## Why

On 2026-09-05 pull request #169 was merged while its `api` job was failing. `main` was
red from `76e0e74` through two further merges (#170, #164) before anyone noticed, and the
four broken assertions were only repaired in #172. Nothing in the repository stopped any
of it: `gh pr merge` accepted a failing check, and the next pull requests inherited a red
base without being told.

The habit that hid it is worth naming: check state was read through
`gh pr checks <n> --watch | tail -6`, which hides rows past the last six *and* discards
the exit status, because a pipeline returns the exit code of its last stage. Both failing
`api` rows were among the hidden ones.

## How to read a check reliably

```bash
SHA=$(gh pr view <n> --json headRefOid -q .headRefOid)
gh api "repos/x812033727/travel_scanner/commits/$SHA/check-runs" \
  -q '.check_runs[] | "\(.name)\t\(.status)\t\(.conclusion)"'
```

Every row should read `completed  success` before merging. Never pipe
`gh pr checks --watch` into `tail` or `head`.

## Dependency audits are advisory inside CI

`npm audit` and `pip-audit` both need a registry at request time. Either one failing
on a network hiccup would now block a merge whose code was never run, so inside `ci.yml`
both are `continue-on-error: true`. The enforcing runs are `npm-audit.yml` and
`pip-audit.yml`, daily and retryable from the Actions tab.

## When main itself goes red

Protection stops a red pull request; it cannot stop a job that fails only on `main`
(a flaky end-to-end case, a registry outage). `.github/workflows/ci-red-main.yml` opens
an issue labelled `ci-red-main` when the CI run for a push to `main` fails, and comments
on the open one if there already is one.

## Automatic updates and merges

`strict` means a green pull request stops being mergeable whenever `main` moves: it has to be
updated from `main` and pass CI again. On a busy day that is most pull requests, many times.
GitHub's merge queue exists for this, but it is offered only to repositories owned by an
organization (or on Enterprise Cloud); this repository belongs to a user account, so it is not
available here (checked 2026-09-26).

`.github/workflows/auto-update-branches.yml` runs `tools/ci/auto-update-branches.mjs` on every
push to `main`, on every finished `CI` run, every ten minutes and on demand. Each pass:

- merges the one pull request that is up to date with all four required checks green, with
  `--match-head-commit`, so a commit pushed meanwhile is refused instead of merged untested;
- turns on auto-merge (squash, pinned to the current head) for every other eligible pull request
  that cannot merge yet, so GitHub merges it as soon as its checks pass on an up-to-date head.
  It uses the GraphQL mutation, never `gh pr merge --auto`, which merges a pull request that
  happens to be mergeable at that moment;
- runs "update branch" on BEHIND pull requests, green ones first, then by number, while at most
  three up-to-date pull requests have required checks running. A BEHIND pull request's own run
  cannot lead to a merge, so it holds no slot, and neither does a red one;
- re-reads the list for a few seconds while mergeability is still UNKNOWN, which is normal right
  after `main` moved.

A check counts the way branch protection counts it: only the `CI` workflow's check run, the most
recent one per name; success, skipped and neutral pass. A head whose required checks were
cancelled or never started gets a note in the run summary and no slot.

Eligible means all of these:

- the base is `main` (stacked pull requests into a feature branch are never touched);
- a branch of this repository, never a fork: this repository is public, and a stranger's pull
  request must not merge because its CI passed;
- opened by the repository owner, and not by a bot (Dependabot upgrades need a person:
  `.agents/skills/dev-and-ci/references/dependabot.md`);
- not a draft, and no `no-auto-merge` label;
- auto-merge was not switched off by hand on the pull request.

Opening a non-draft pull request from a branch here therefore means it will merge once it is
green. To hold one: open it as a draft, add the `no-auto-merge` label, or turn auto-merge off on
the pull request. The next pass also turns auto-merge off on a labelled or draft pull request.
Since that counts as a manual switch-off too, after removing the label or leaving draft, turn
auto-merge back on once on the pull request (or merge it yourself). Create the label once with
`gh label create no-auto-merge --color B60205 --description "Auto-update workflow leaves this pull request alone"`.

It relies on the repository setting "Allow auto-merge" (`allow_auto_merge`, on when
checked on 2026-09-26) and on a repository secret `AUTO_MERGE_TOKEN`. It cannot use `GITHUB_TOKEN`:
pull_request runs started by a `GITHUB_TOKEN` push wait for a maintainer to approve them, so an
updated branch would sit without CI. Without the secret, each pass prints a notice and exits 0.
To create it, the owner makes a fine-grained personal access token (GitHub → Settings →
Developer settings → Fine-grained tokens):

- resource owner `x812033727`, repository access "Only select repositories" →
  `travel_scanner`;
- repository permissions: Contents: read and write (update branch creates a merge commit),
  Pull requests: read and write (merge and auto-merge), Workflows: read and write (updating a
  branch after `main` changed a workflow file needs it); Metadata: read is added by GitHub;
- an expiry of 30 to 90 days. When it expires, passes fail at `gh pr list` and the token has to
  be renewed.

Then store it under Settings → Secrets and variables → Actions → New repository secret, name
`AUTO_MERGE_TOKEN`. A repository secret can be read by any workflow run on a branch of this
repository, which only people with write access can push; forks never see it. Whoever holds the
token can push and merge to `main` without review, which is also what write access allows. To
narrow it to `main`, make it an environment secret of an environment whose deployment branches
are limited to `main`, and add `environment:` to the job (each pass then records a deployment).

While the workflow runs, do not drive an eligible pull request with
`.agents/skills/task-board/scripts/merge-when-green.sh`: both would update the same branch.

To stop it: disable the workflow in the Actions tab, or delete the secret.

## Changing it

```bash
gh api -X PUT repos/x812033727/travel_scanner/branches/main/protection --input - <<'JSON'
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["api", "web", "containers", "full-stack-smoke"]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": null,
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
JSON
```

Renaming a job in `ci.yml` renames its check; update the `contexts` list in the same
change or every pull request will wait forever for a check that no longer exists. Update
`REQUIRED` in `tools/ci/auto-update-branches.mjs` too, and if the workflow itself is renamed,
`REQUIRED_WORKFLOW` there and `workflows: [CI]` in `.github/workflows/auto-update-branches.yml`.
