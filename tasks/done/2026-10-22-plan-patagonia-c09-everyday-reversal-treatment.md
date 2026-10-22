---
id: 2026-10-22-plan-patagonia-c09-everyday-reversal-treatment
title: Plan Patagonia C09 everyday reversal treatment and source matrix
status: done
priority: P2
area: docs
owner: codex-c09-patagonia
claimed_at: 2026-10-22T12:50:55Z
created_at: 2026-10-22T12:49:22Z
completed_at: 2026-10-22T13:29:23Z
branch: codex/brand-story-patagonia-c09-treatment
depends_on: []
scope:
  - docs/videos/story-everyday-patagonia-c09
---

# Plan Patagonia C09 everyday reversal treatment and source matrix

## Why

The approved 20-episode everyday-reversal series assigns C09 to Patagonia and asks why a climbing-gear seller moved away from its popular pitons. The 1972 actor was Chouinard Equipment; the Patagonia clothing label followed in 1973. This distinction and the continued sale of pitons need to be visible before a script is written. C09 in the older 100-story index is an unrelated i-mode episode.

## Definition of done

- [x] Six-chapter, 8+ minute C09 Treatment and claim-level source matrix are independently checked and available for owner review.
- [x] Owner chooses whether to adopt the Treatment before anyone writes a full script.

## Steps

- [x] Check local/remote branches, PRs and task board for a C09 Patagonia owner; start an isolated managed worktree and claim this narrow scope.
- [x] Read the brand-story, youtube-video/story and curio-episode rules; consult contemporaneous and primary sources.
- [x] Draft `treatment.md` and `source-matrix.md`, including the distinction between the 1972 equipment company and later Patagonia label, the continued piton line, and the sales-evidence caveat.
- [x] Obtain a second agent's claim-by-claim review bound to the final SHA-256 of both files, resolve any revisions, and record the receipt.
- [x] Obtain owner Treatment decision before a full script or any paid media work.

## How to verify

Read S1–S4 and S6–S9 via the direct URLs in `source-matrix.md`; compare M01–M10 against passages and version notes. Run `npm run check:tasks` and `npm run test:docs-videos` on this PR branch. Review `git diff --check` and verify only this scope plus this task file changed. Independent reviewer must not reuse the author's PASS assertion.

## Notes

The 1967 Chouinard/Frost AAJ article still describes piton technique. Their 1972 catalog foreword asks climbers to favor chocks, yet preserves necessary piton exceptions; it does not tell customers to buy fewer pitons. Rowell's 1973 independent review records contemporary hypocrisy criticism. Bernstein's 1977 New Yorker interview still lists pitons among Great Pacific Iron Works products. The independent reviewer visually inspected the catalog scan: its inner cover says One Dollar and the p67 price list says Great Pacific Iron Works, while Karabin Museum documents altered 1972–74 reprints. Its piton pages cannot be treated as proof of the earliest 1972 edition. Patagonia's 2022 "best-selling" recollection is a company claim without a contemporaneous sales ledger. The company-history dynamic page does not expose body text to the automated reader; S1–S4 are directly readable HTML.

The first independent review is a historical HOLD bound to the original Treatment and matrix hashes; its receipt is `docs/videos/story-everyday-patagonia-c09-review/independent-source-review.md`. The author revised the headline, cold open, edition caveat, M04/M06/M08, and broken plan link. The later PASS below resolved that HOLD before the owner Treatment decision. No script or media production was part of the Treatment task.

The same receipt now begins with a second-agent PASS for the revised Treatment SHA-256 `0769134247D8D98407FDE2DCE3DD8026AF1681CB408A855C62F9708915991FDD` and matrix SHA-256 `EC8E598C9099EBE0FFD51CBF89807C96962C62618A41BE8BA3A66A48986EEA2C`. The owner explicitly adopted this revised C09 Treatment in the conversation on 2026-10-22. This ticket ends at the Treatment gate; script and visual planning are a separate narrow task. `npm run check:tasks` is locally blocked by an unrelated duplicate review ticket in this worktree; the policy-blocked open copy was left untouched.

No full script, TTS, image, music, import, upload, publish, or merge is authorized by this task. Do not inherit C05/C06 media approvals.
