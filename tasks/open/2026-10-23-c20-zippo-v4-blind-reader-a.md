---
id: 2026-10-23-c20-zippo-v4-blind-reader-a
title: C20 Zippo v4 blind reader A and parity receipt
status: review
priority: P2
area: docs
owner: codex-reader-a
claimed_at: 2026-10-23T07:02:50Z
created_at: 2026-10-23T07:02:44Z
completed_at:
branch: codex/c20-zippo-v4-blind-a
depends_on: []
scope:
  - docs/videos/story-everyday-zippo-c20/reviews/independent-blind-v4-reader-a.md
  - docs/videos/story-everyday-zippo-c20/reviews/independent-blind-v4-reader-a-parity.md
---

# C20 Zippo v4 blind reader A and parity receipt

## Why

C20 v4 needs an independent narration-only judgment locked before any author context, then proof that the judged projection is exactly the spoken text at author PR #1728's specified head. The review must remain separate from the author's script work.

## Definition of done

- [x] Read only the specified 64-ID projection, freeze all 12 narrative verdicts with its SHA-256 and a timestamp, and preserve a read-only local lock.
- [x] Verify ordered 64/64 narration parity against the exact author PR head after the lock.
- [x] Record the five HOLD items, line IDs, and actionable narrative issues in a separate receipt.
- [x] Open a stacked draft PR with only this review, receipt, and task record; attach the PR to this chat.

## Steps

- [x] Lock the projection-only review before inspecting author files or PR metadata.
- [x] Fetch 3b27a5af392acfe88a168850aa57d2f27cb2f84d into an isolated sparse worktree and compare script Markdown narration rows to the projection.
- [x] Add the immutable lock copy and parity receipt under C20 reviews without changing the author script.
- [x] Run narrow checks, push the branch, and create a draft PR targeting the author's script branch.

## How to verify

Compare SHA-256 of the projection to 0AB3EE39F253B19604618BDF70424DBEEDA51711561673B3120A06563697F761; parse the 64 `c20` script-table rows at exact head 3b27a5af392acfe88a168850aa57d2f27cb2f84d and compare each ordered ID and narration cell case-sensitively. Check `git diff --name-only` contains only the two review files and this task file. Run `npm run check:tasks`.

## Notes

Blind lock timestamp: 2026-10-23T15:00:12.3932917+08:00. Lock SHA-256: F7BBCAA2BC1410E4F226EB0D6488710B0FE60E77DA52BE163EC4C798A628219B. Exact-head parity: 64/64, zero differences. Overall HOLD: no_spoiler, payoffs, opening_hooks, no_detour, no_recap. Draft PR: https://github.com/x812033727/travel_scanner/pull/1755, stacked on codex/brand-story-zippo-c20-script. `npm run check:tasks` and `git diff --cached --check` passed; task checker reported pre-existing stale-task warnings. Source fact, TTS, audio, and playback gates were outside this review.
