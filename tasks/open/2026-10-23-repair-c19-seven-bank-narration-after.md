---
id: 2026-10-23-repair-c19-seven-bank-narration-after
title: Repair C19 Seven Bank narration after blind review
status: in-progress
priority: P2
area: docs
owner: codex-c19-v5-narrative
claimed_at: 2026-10-23T07:39:35Z
created_at: 2026-10-23T07:02:20Z
completed_at:
branch: codex/brand-story-seven-bank-c19-script
depends_on: []
scope:
  - docs/videos/story-everyday-seven-bank-c19/script.md
  - docs/videos/story-everyday-seven-bank-c19/script-source-notes.md
  - docs/videos/story-everyday-seven-bank-c19/visual-plan.md
  - docs/videos/story-everyday-seven-bank-c19/visual-plan.json
  - docs/videos/story-everyday-seven-bank-c19/reviews/author-script-receipt-20261023.md
---

# Repair C19 Seven Bank narration after blind review

## Why

The owner approved the C19 Treatment direction, not the script. Independent full source and paired visual review passed the preceding v4 head in #1758 and #1760. Two fresh, context-free narrator-only blinds on that exact v4 projection held the story: #1763 found six of twelve criteria HOLD and #1764 found seven. Both identified an answer disclosed early, dropped night-shopper viewpoint, date and product inventory, and a final answer that did not join the partner's cost benefit, usage fee, and ATM cash operations. Their old-head findings are routing evidence, not a verdict on v5.

## Definition of done

- [x] Rewrite the 79-line narrator script around one night-store customer's question and carry it through the final causal answer.
- [x] Pair all 79 author source notes and MD/JSON visuals with the revised narration; limit the 2023–24 service to a short, accurately scoped coda.
- [x] Preserve 1987→1999→2001→2002→2005→2007→2010 chronology and the separate customer fee and partner ATM usage fee in the 2010 report.
- [x] Generate a new narration-only projection for two fresh, independent, context-free blind readers.
- [x] Obtain independent full source and paired visual re-review on the exact v5 head: #1769 found narration/source 79/79 PASS and seven visual HOLDs.
- [ ] Obtain independent seven-shot visual delta recheck on the new author head.
- [ ] Obtain two fresh, independent narrator-only blind verdicts on the exact v5 projection.
- [ ] Present the independently reviewed script and visual direction to the owner for the separate script gate.

## Steps

- [x] Inspect exact-head blind HOLD receipts #1763 and #1764, the approved Treatment, and the source matrix.
- [x] Revise script, source notes, and paired MD/JSON visuals; document the narrative-order refinement.
- [x] Regenerate the narrator-only projection and run mechanical parity checks.
- [x] Commit and push the v5 author draft to original draft PR #1742.
- [x] Read #1769's seven precise visual HOLDs and revise only those paired MD/JSON prompts for one visible person doing one action.
- [x] Commit and push the seven-shot visual delta to the same draft PR #1742.

## How to verify

From clean v5 checkout `C:\Users\x8120\.codex\worktrees\brand-story-seven-bank-c19-v5\travel_scanㄐ`, run `python C:\Users\x8120\.codex\worktrees\brand-story-seven-bank-c19-v5\verify_v5.py`, `git diff --check`, and `npm run check:tasks`. The scratch verifier checks 79 IDs/order, narration and source parity, JSON visual type and text, card streak, exact image model/look, prompt exclusions, and the new narrator-only projection bytes. It is mechanical author QA, not independent source or story approval. Confirm PR #1742 remains draft and points to the committed author head. Actual voice duration, paid quote, media, import, upload, and publication remain separate.

## Notes

The approved Treatment's paper sequence put the fee mechanism before expansion; the v5 narrator script puts 2005–07 expansion first to keep the chronology continuous. This is a narration-order refinement under the same approved factual direction, explicitly documented for owner review. The full source/visual PASS at the preceding `c1fe8f9` head and blind HOLD receipts #1763/#1764 do not validate v5. The original author checkout has a policy-blocked untracked `tasks/done` duplicate; leave it intact. This clean detached checkout keeps this tracked `tasks/open` task pending independent review. No paid media or product publishing was attempted. Exact v5 author hashes and projection are in `reviews/author-script-receipt-20261023.md`.

## Seven-shot visual delta after #1769

Independent full review #1769 is bound to author head `8849fe98ee08b9741c67d715fbd781938799fa94`: narration/source 79/79 PASS, visual 72/79 PASS, seven HOLDs for `c190204`, `c190309`, `c190403`, `c190504`, `c190516`, `c190517`, and `c190610`. The author changed only those seven `visual-plan.md` and `visual-plan.json` prompts to a single person and action with static context. `script.md` and `script-source-notes.md` retain the exact #1769 audited bytes, and the narrator-only projection remains the same. This is an author repair, not an independent visual PASS; ask another reviewer for a seven-shot hash-bound delta before owner script/visual approval. The exact new visual hashes are in the adjacent author receipt. The old policy-blocked duplicate is untouched.
