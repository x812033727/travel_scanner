---
id: 2026-10-23-c15-frixion-script-source-visual-review
title: Independently check C15 FriXion script facts and paired visuals
status: in-progress
priority: P1
area: docs
owner: codex-c15-independent-source
claimed_at: 2026-10-23T03:30:58Z
created_at: 2026-10-23T03:30:54Z
completed_at:
branch: codex/brand-story-frixion-c15-review
depends_on: []
scope:
  - docs/videos/story-everyday-frixion-c15/reviews/independent-script-source-visual-v1.md
---

# Independently check C15 FriXion script facts and paired visuals

## Why

The owner adopted C15's revised Treatment; the 87-line script and 87 paired visuals in draft PR #1701 were authored by another agent. They need an independent, exact-byte source and visual review before owner script approval.

## Definition of done

- [x] Reopen directly readable PILOT development histories, current FAQs and dated press release, and check each of the 87 lines against its source tags.
- [x] Check all 87 paired visuals for additional factual implications and the Curio illustration constraints.
- [x] Bind the review to the actual PR checkout file hashes and report precise HOLDs or PASS, without altering the author's script or visuals.
- [x] Resolve all HOLDs on revised author bytes and recheck the changed lines and corresponding visuals.

## Steps

- [x] Confirm PR #1701 exact head, draft state and no auto-merge.
- [x] Open sources S1–S5 and inspect S6's patent-publication metadata.
- [x] Compare script/visual Markdown/JSON IDs and narration strings; recompute sizes, card run, paper durations and SHA-256 on a fresh worktree from PR head.
- [x] Write independent HOLD receipt with source locators and narrowly proposed repairs.
- [x] Recheck author correction before moving this task to done.

## How to verify

`Get-FileHash -Algorithm SHA256` for script, notes, visual MD and JSON in a fresh checkout; `git ls-files --eol` to distinguish CRLF working bytes from committed LF bytes. Parse visual JSON and compare 87 IDs and narration strings with both Markdown tables. `npm run check:tasks`; `git diff --check`; read draft PR state.

## Notes

2026-10-23: Initial review found O13's “稍微變暖” exceeds the cited source's measured temperature claim; the 1976 Magic Cup is a paper cup, while O07–O09 prompts say only “plain cup”, risking ceramic/glass depiction. The author receipt's JSON SHA was measured on a CRLF working file, while the committed PR head checks out to LF bytes and a different SHA; author repaired only that receipt at head `842c28156`, so it is no longer a HOLD. Exact details are in `independent-script-source-visual-v1.md`; retain HOLD on O13/O07–O09 until corrected and rechecked. No paid media was made.

2026-10-23: Author head `665738706d90f7bddae20d1874cfb24dd878fe1d` repaired O13 and O07–O09. Recomputed four LF checkout hashes, read the exact diff, checked both primary PILOT pages again, and verified all 87 script/visual IDs and narration pairs. The same independent reviewer marked the updated source/visual text PASS in `independent-script-source-visual-v1.md`; the former HOLD is retained there as history. No paid media was made.
