---
id: 2026-09-26-auto-update-branches-workflow
title: Keep open PRs updated and merged when green from GitHub Actions, without a local watcher
status: done
priority: P2
area: tools
owner: claude-opus-ci-subscription
claimed_at: 2026-09-26T13:07:29Z
created_at: 2026-09-26T13:07:27Z
completed_at: 2026-09-26T13:28:29Z
branch: claude/auto-update-branches
depends_on: []
scope:
  - .github/workflows/auto-update-branches.yml
  - tools/ci/auto-update-branches.mjs
  - tools/ci-auto-update.test.mjs
  - .github/BRANCH_PROTECTION.md
  - .agents/skills/task-board/SKILL.md
  - .claude/skills/task-board/SKILL.md
  - .agents/skills/task-board/references/merge.md
---

# Keep open PRs updated and merged when green from GitHub Actions, without a local watcher

## Why

`main` has strict protection: four required checks and an up-to-date branch. Every merge makes the other open PRs `BEHIND`, and a person has to run "update branch" and wait for CI again before they can merge. Since 2026-09-23 the owner has kept a standing order, 「訂閱所有 CI 如果綠就合併」. Until now it was carried out by a watcher script that ran on the owner's Windows laptop in a Claude session. That had two problems:

- **It stopped whenever the laptop slept.** On 2026-09-26 the machine slept from 08:03 to 12:54 UTC, with brief wakes at 10:01 and 12:01, and no PR was updated in that window. The same thing had happened on 2026-09-24.
- **Its first version updated every BEHIND PR each time `main` moved.** With 16 open PRs that put 22 runs in the queue and kept 27 in progress, yet still only one PR can merge per commit on `main`.

The owner asked for merge queue. GitHub offers it only on public repositories owned by an organization, or on Enterprise Cloud (changelog 2023-07-12: "Merge queue is available on private and public repos on the GitHub Enterprise Cloud plan and all public repos owned by organizations"). This repository is owned by the user account `x812033727`. The owner chose the Actions-based alternative instead.

## Definition of done

- [x] One pass of `tools/ci/auto-update-branches.mjs` does four things:
  - merges the single up-to-date, all-green PR with `--match-head-commit`;
  - enables auto-merge through the GraphQL mutation, pinned to the head, on eligible PRs that cannot merge yet;
  - updates `BEHIND` PRs, green ones first, while at most 3 up-to-date PRs have required checks running;
  - turns auto-merge off again on labelled or draft PRs.
- [x] It never touches forks, stacked PRs, bots and Dependabot, other authors, drafts, the `no-auto-merge` label, or PRs whose auto-merge was switched off by hand.
- [x] `.github/workflows/auto-update-branches.yml` runs it on each push to `main`, each finished `CI` run, every 10 minutes, and on dispatch. It does nothing, and says so, while `AUTO_MERGE_TOKEN` is missing.
- [x] The docs describe the new merge rule: a non-draft PR from a repository branch merges when green. The places updated are `.github/BRANCH_PROTECTION.md`, task-board rule 6 and step 5 (both copies), and `references/merge.md`.
- [ ] Owner only: create the fine-grained token and the `AUTO_MERGE_TOKEN` secret, and create the `no-auto-merge` label.
- [ ] One real pass is seen in the Actions log that merges, and one that updates.

## Steps

- [x] Write the script as a pure `plan()` plus `commands()`, with `gh` injected into `main()`. Tests cover these without a network.
- [x] Get three independent reviews covering security, GitHub semantics, and tests/docs, then fix every finding (listed in Notes).
- [x] Run a read-only dry-run against the live PR list.
- [ ] After merge: the owner adds the secret. Dispatch the workflow once, then read its step summary.

## How to verify

```bash
node --test tools/ci-auto-update.test.mjs
GH_TOKEN=$(gh auth token) GH_REPO=x812033727/travel_scanner AUTO_MERGE_AUTHORS=x812033727 node tools/ci/auto-update-branches.mjs --dry-run
gh workflow run auto-update-branches.yml && gh run list --workflow auto-update-branches.yml --limit 1
```

The dry-run only reads. It prints `[dry-run] …` for each write it would make.

## Notes

- The review round (2026-09-26) found problems in the first version, all fixed before this PR:
  - The opt-out label came too late to matter: auto-merge was already on, and the script never turned it off. It also re-enabled auto-merge that had been turned off by hand; #807 was turned off manually at 13:02.
  - Stacked PRs were eligible. `gh pr merge --auto` merges a PR that is already mergeable (gh 2.97 `merge.go:530`, `763-766`), so a stacked PR would have been squashed into its parent while CI still ran.
  - Missing or cancelled checks held in-flight slots forever.
  - A red-but-running PR, or a `BEHIND` running PR, held a slot.
  - The pass right after a merge saw `UNKNOWN` and did nothing.
  - `SKIPPED`/`NEUTRAL` were counted as failures. Any "success" row won over a newer failure, and a `StatusContext` or another workflow's check with the same name could pass a check.
  - Tests never checked the actual `gh` arguments.
- GitHub facts checked:
  - `pull_request` runs from a `GITHUB_TOKEN` push need a maintainer's approval, so the script needs a PAT.
  - Auto-merge does not update a `BEHIND` branch. #808 was all green with auto-merge on and was not merged.
  - Auto-merge survives pushes by a writer: #711–#785 each had 1–5 commits after enabling it, with no disable event.
  - `allow_auto_merge` was on when checked on 2026-09-26.
- Removing the label, or leaving draft, does not turn auto-merge back on by itself, because the script's own switch-off counts as manual. Re-enable it once on the PR.
- The laptop watcher (`watch3.sh` in that session's scratchpad) keeps running until the secret exists.
