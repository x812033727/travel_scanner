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

## When main itself goes red

Protection stops a red pull request; it cannot stop a job that fails only on `main`
(a flaky end-to-end case, a registry outage). `.github/workflows/ci-red-main.yml` opens
an issue labelled `ci-red-main` when the CI run for a push to `main` fails, and comments
on the open one if there already is one.

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
change or every pull request will wait forever for a check that no longer exists.
