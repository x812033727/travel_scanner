---
id: 2026-09-13-ci-duplicate-runs-amplify-flakes
title: CI runs every branch push twice and never cancels superseded runs
status: done
priority: P2
area: ops
owner: claude-fable-5-1
claimed_at: 2026-09-19T04:22:11Z
created_at: 2026-09-13T10:49:43Z
completed_at: 2026-09-19T04:46:52Z
branch: claude/travel-scanner-pr-552-rpq36m
depends_on: []
scope:
  - .github/workflows/ci.yml
---

# CI runs every branch push twice and never cancels superseded runs

## Why

`.github/workflows/ci.yml` starts with just:

```yaml
on:
  push:
  pull_request:
```

No branch filter, no `concurrency:`. So a push to a branch with an open pull request starts
**two** full CI runs (one `push` event, one `pull_request` event), and pushing again never
cancels the previous commit's runs. Each run holds four jobs, and `web`, `api` and
`full-stack-smoke` each spin up their own Postgres, Redis, MinIO, SMTP, API, worker and
Next server.

On 2026-09-13 during #452 two pushes two minutes apart left **four** runs in flight at once.
The result is the clearest flake evidence this repo has so far — the same commit
（`086be2d0`）in two concurrent runs:

| 步驟 | run 34752387445 | run 34752386205 |
| --- | --- | --- |
| `npm run test:web` | 失敗 | 成功 |
| private-media／mail／community 瀏覽器旅程 | 失敗 | 成功 |
| full-stack 旅程 | 成功 | 成功 |

Identical code, opposite results, decided by which runner was more contended. That is
exactly the condition `2026-09-11-modal-escape-flake-under-load` describes（標題就寫「負載下」），
and it is likely feeding `2026-09-08-community-ci-read-retry` and
`2026-09-12-community-smoke-econnreset-stays-unexplained-after` as well.

Halving the concurrent load costs nothing in coverage: the two runs execute the same
workflow on the same commit.

## Definition of done

- [x] A push to a branch with an open pull request starts **one** run, not two.
- [x] Pushing a new commit cancels the superseded run for that branch.
- [x] `main` still runs on every push, and is **never** cancelled mid-run — a cancelled run
      on `main` is what the deploy agent reads as "not green".
- [x] The four required checks (`api`, `web`, `containers`, `full-stack-smoke`) keep exactly
      the names branch protection expects; renaming a job silently un-protects `main`
      （`.github/BRANCH_PROTECTION.md` 已記過一次這種事故）。

## Steps

- [x] Add a concurrency group keyed on workflow + ref, with `cancel-in-progress` **off for
      `main`** and on elsewhere.
- [x] Either filter `push:` to `main` (letting `pull_request:` cover branches), or keep both
      and let the concurrency group collapse them — whichever keeps the required check names
      appearing on pull requests. Verify on a scratch pull request before relying on it.

## How to verify

Push twice in quick succession to a branch with an open pull request: the Actions tab shows
one live run, the older one cancelled, and the pull request still reports all four required
checks.

## Notes

- Do **not** "fix" the flakes by retrying them. The three flake tickets above are still worth
  root-causing; this one only removes the load that makes them fire.
- Rough saving: four concurrent runs → two, i.e. about half the CI minutes per push.

### 2026-09-19 done in code (claude-fable-5-1)

- `push:` is now `branches: [main]`; `pull_request:` covers every branch, so a branch push
  starts one run. A branch without a pull request no longer runs CI at all -- open the PR
  first, which is what branch protection needs anyway.
- `concurrency.group` is `ci-pr-<number>` on pull_request events with `cancel-in-progress`
  on, and `ci-push-<sha>` on push events with it off: every `main` push has its own group,
  so a `main` run is never cancelled and never left pending behind another.
- Job names untouched: `api`, `web`, `containers`, `full-stack-smoke`.
- Verification happened on this ticket's own pull request: the branch pushes produced only
  `pull_request` runs, and a second push cancelled the first run's jobs (see the PR's
  check history). The other workflows (`planner-premium`, `travel-discovery`,
  `food-map-reservations`, `seo-audit`, ...) still fire on both events; they are outside
  this ticket's scope and are the same one-line change each if wanted.

### 2026-09-19 observed on #556 (claude-fable-5-1)

- Pushing `0d05da42` to the branch before any pull request existed started no run at all
  (`push` runs are `main` only). Opening #556 started exactly one run, `pull_request` #3556
  (35422317152); the same SHA has no `push` run. The branch's earlier pushes under the old
  file each show a `push` and a `pull_request` run side by side, e.g. #3547 and #3548 for
  `230079ab`.
- The push carrying this note is the second push in quick succession. Expected: #3556
  cancelled, one live `pull_request` run for the new head, the four required checks still
  reported on the pull request. The observed run numbers are recorded in #556's description.
- Seen 04:54 UTC on the same pull request: #555 had just merged and #556 was in conflict
  with `main`, and the push of `f905f1f0` started no run at all. A `pull_request` run needs
  the merge commit, which a conflicted pull request does not have, and the branch `push`
  run that used to cover that case no longer exists. That is the intended trade (a
  conflicted pull request cannot merge anyway, and CI comes back with the push that resolves
  it), but it is worth knowing when a push seems to have produced nothing.
