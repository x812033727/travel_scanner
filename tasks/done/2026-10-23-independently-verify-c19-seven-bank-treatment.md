---
id: 2026-10-23-independently-verify-c19-seven-bank-treatment
title: Independently verify C19 Seven Bank treatment sources
status: done
priority: P1
area: docs
owner: codex-c19-independent-review
claimed_at: 2026-10-23T05:41:10Z
created_at: 2026-10-23T05:41:05Z
completed_at: 2026-10-23T05:42:31Z
branch: codex/seven-bank-c19-independent-review-20261023
depends_on: []
scope:
  - docs/videos/story-everyday-seven-bank-c19/reviews/independent-source-review-20261023.md
---

# Independently verify C19 Seven Bank treatment sources

## Why

The author's C19 six-chapter Treatment and M01–M16 matrix need a separate reading of their issuer originals before the owner can decide whether to adopt the Treatment. A reviewer must not edit the author's files or let fact confirmation stand in for owner adoption.

## Definition of done

- [x] Directly reopen all S1–S7 and record an individual M01–M16 verdict with source boundaries.
- [x] Bind the verdict to PR #1716 head and SHA-256 of the exact Git blobs for both author files.
- [x] Record any treatment-level holds and visual/thumbnail finding in an independent receipt.

## Steps

- [x] Check source chronology, ATM access versus own deposit/account service and later loans, 2010 versus 2024 business models, fees versus placement costs, geographic reach, and actual versus planned service.
- [x] Check whether the narrative infers a comparative founding motive or ATM-caused customer growth beyond its sources.
- [x] Keep the author worktree read only and prepare the receipt on an isolated sparse branch.

## How to verify

Open `docs/videos/story-everyday-seven-bank-c19/reviews/independent-source-review-20261023.md` and check its head, two Git blob OIDs and SHA-256 values against PR #1716 exact head. Run `npm run check:tasks` and `git diff --check` on this review branch. The review PR targets the author branch and stays draft with `no-auto-merge`.

## Notes

M01–M16 pass as written with their caveats. Two Treatment lines are held: the promised reason for choosing a licensed bank over partnership is not documented by S1–S7, and the causal-arrow sentence improperly implies later ATM fee income drove the early rollout. Receipt gives precise repair wording. Owner adoption and script/media work remain separate gates.

- Local `npm run check:tasks` is blocked by the untracked open source copy left after `done`; exact-path deletion was rejected as `blocked by policy`. The PR stages only this completed task and the receipt; no workaround deletion was attempted.
