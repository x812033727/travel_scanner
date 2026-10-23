---
id: 2026-10-23-c20-zippo-script-source-and-visual
title: C20 Zippo script source and visual review
status: review
priority: P1
area: docs
owner: codex-c20-source-visual-review
claimed_at: 2026-10-23T05:23:44Z
created_at: 2026-10-23T05:23:32Z
completed_at:
branch: codex/brand-story-zippo-c20-script-source-review
depends_on: []
scope:
  - docs/videos/story-everyday-zippo-c20/reviews/independent-script-source-visual-review.md
---

# C20 Zippo script source and visual review

## Why

Treatment PR #1708 and its source audit PR #1710 cover the six-chapter plan, but the 68-line author script in PR #1728 adds exact voiced claims, a 1997 museum/Repair Clinic sentence, and one visual or card per line. A separate reviewer must compare the exact author blobs with primary sources and visuals before the owner is asked to approve a script or any media spend.

## Definition of done

- [x] A review receipt locks PR #1728's exact head and four Git blob SHA-256 values.
- [x] Every one of 68 narrated IDs and paired visuals/cards receives an explicit PASS or HOLD with primary-source boundaries and actionable repairs.
- [x] The receipt is in a separate draft, no-auto-merge PR targeting the author's branch; the author's files remain untouched.

## Steps

- [x] Inspect the adopted Treatment, source matrix, author script/source notes, visual Markdown and JSON.
- [x] Reopen official Zippo history, original US patent, US/UK current service pages, date codes, Arc FAQ and 600-millionth production page.
- [x] Independently compare 68/68 exact IDs and texts; document three narrow HOLDs.
- [x] Commit and push the independent receipt; open a draft review PR and read back its head, base, labels and merge mode.

## How to verify

Recompute SHA-256 from `git show 4b51defa16c8a8ca19f5504d67d1428c56227b4f:docs/videos/story-everyday-zippo-c20/<file>` for each of the four author files. Parse all four files to check 68 identical IDs, 58 `shot` and 10 `card` entries, exact narration/source/prompt agreement, and no adjacent cards. Read each primary URL linked in the receipt. Run `npm run check:tasks`, `git diff --check`, then inspect the review PR metadata on GitHub for the exact target and `no-auto-merge` label.

## Notes

2026-10-23: Author head `4b51defa16c8a8ca19f5504d67d1428c56227b4f` is still the exact head checked. Four blob hashes agree with the author's own receipt, but this reviewer re-read sources independently. 65 PASS / 3 HOLD: `c200207` should identify the 1933 price and first guarantee as a later corporate recollection in voice/card; `c200310` incorrectly implies a 1933 sales source and depicts a sales card; `c200410` dates the current Repair Clinic exhibit to the museum's 1997 opening without direct evidence. See the precise fixes and 68-row matrix in `docs/videos/story-everyday-zippo-c20/reviews/independent-script-source-visual-review.md`. No author files, paid media, import, upload, or publication were changed.

2026-10-23: [Draft review PR #1732](https://github.com/x812033727/travel_scanner/pull/1732) targets `codex/brand-story-zippo-c20-script`; initial pushed head `563029d850033e57421cd5b12088ae0857b852ff`. GitHub readback confirms `isDraft=true`, `autoMergeRequest=null`, `no-auto-merge` label present. `npm run check:tasks` passed (pre-existing unrelated warnings); staged diff whitespace check passed. `codex_app/attach_artifact` was attempted but the desktop tool reported unavailable; the PR URL remains in this durable ticket and review receipt.

Task closeout note: `npm run tasks -- done` wrote `tasks/done/2026-10-23-c20-zippo-script-source-and-visual.md` but reported that Windows still held the source file open. One exact `Remove-Item -LiteralPath` attempt against the verified open-file path was **blocked by policy**. No alternate deletion route was attempted. The task is left in `review` in this PR; the locally untracked done copy is not staged or pushed. Finish the move only after the policy or file-handle condition is resolved through an approved route.
