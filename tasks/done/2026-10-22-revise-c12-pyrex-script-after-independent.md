---
id: 2026-10-22-revise-c12-pyrex-script-after-independent
title: Revise C12 Pyrex script after independent HOLD
status: done
priority: P1
area: docs
owner: codex-c12-script-author
claimed_at: 2026-10-22T15:03:37Z
created_at: 2026-10-22T15:03:32Z
completed_at: 2026-10-22T15:05:48Z
branch: codex/brand-story-pyrex-c12-script
depends_on: []
scope:
  - docs/videos/story-everyday-pyrex-c12-script/script.md
  - docs/videos/story-everyday-pyrex-c12-script/visual-plan.md
---

# Revise C12 Pyrex script after independent HOLD

## Why

The independent review of C12 script SHA B5A9BC75... and visual SHA 1CA9F4BA... in draft PR #1692 found two source-boundary HOLD lines, one overstated evidence phrase, one visually understated broken dish, and several lines that read like audit or editing instructions. The original author must revise the same 80 IDs before a different agent can audit new bytes.

## Definition of done

- [x] H04, T03 and I07 no longer imply an unsupported year gap, invented ad wording, or an original household record.
- [x] O12 depicts a shattered ceramic dish; process-language lines become a continuous sourced story while preserving all 80 narration and visual IDs.
- [x] New script and visual hashes are pushed to the existing draft PR #1692 for fresh independent review, with no paid media or owner script approval claim.

## Steps

- [x] Read the independent review receipt and exact source/scene boundaries.
- [x] Revise H04, T03, I07, O12 and narration O07/I03/I13/E02/E03; align O11, I03, E03 and N14 scene descriptions.
- [x] Recheck 80/80 ordered IDs, image/card counts, prompt restrictions, hook gap and task formatting.

## How to verify

Compare the new lines against S1/S2/S4 and the prior review receipt. Read-only row check: 80 script IDs and 80 visual IDs in identical order, 67 illustrations and 13 cards, at most two cards in a row, no forbidden names/logos/text in illustration prompts. Recompute SHA-256 of both files, run `git diff --check` and `npm run check:tasks`, then inspect PR #1692 head and draft/no-auto-merge status.

## Notes

The original HOLD receipt stays at docs/videos/story-everyday-pyrex-c12-script/reviews/independent-script-source-review.md and is bound to the old hashes; it does not pass the revision. S1 says the lantern application was newly successful when Corning sought other markets, so H04 now says only “later.” S1 does not provide an original Bessie notebook, so I07 cites the museum's later recollection of one sponge cake. S1 says the dish shattered; O12 now shows fragments. S2 confirms department-store demonstrations but no Chinese “heat resistant” advertising quote. Process edits introduce Jesse at the market-search point, carry the dinner and battery-jar sequence forward, then move to the later patent and commercial ovenware. No exact patent date, formula switch year or universal product safety claim was added.

The independent reviewer task's left-behind untracked open file belongs to that reviewer; do not stage, move or remove it in this author task. Independent recheck, two blind readers, pronunciation review, owner script gate and actual TTS duration all remain pending.

Local `npm run check:tasks` reports a duplicate ID only because that reviewer-owned, untracked open ghost remains beside its tracked `tasks/done` copy. This author scope cannot remove it, and it must not be included in this PR. The 80/80 structure and `git diff --check` pass; CI will evaluate only the committed task files. The earlier broad docs-video test already has an unrelated Windows package-runtime child-process failure noted in the PR.
