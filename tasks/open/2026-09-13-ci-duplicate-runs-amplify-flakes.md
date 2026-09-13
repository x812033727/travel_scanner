---
id: 2026-09-13-ci-duplicate-runs-amplify-flakes
title: CI runs every branch push twice and never cancels superseded runs
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-09-13T10:49:43Z
completed_at:
branch:
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

- [ ] A push to a branch with an open pull request starts **one** run, not two.
- [ ] Pushing a new commit cancels the superseded run for that branch.
- [ ] `main` still runs on every push, and is **never** cancelled mid-run — a cancelled run
      on `main` is what the deploy agent reads as "not green".
- [ ] The four required checks (`api`, `web`, `containers`, `full-stack-smoke`) keep exactly
      the names branch protection expects; renaming a job silently un-protects `main`
      （`.github/BRANCH_PROTECTION.md` 已記過一次這種事故）。

## Steps

- [ ] Add a concurrency group keyed on workflow + ref, with `cancel-in-progress` **off for
      `main`** and on elsewhere.
- [ ] Either filter `push:` to `main` (letting `pull_request:` cover branches), or keep both
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
