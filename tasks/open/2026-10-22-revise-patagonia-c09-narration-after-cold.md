---
id: 2026-10-22-revise-patagonia-c09-narration-after-cold
title: Revise Patagonia C09 narration after cold read
status: review
priority: P2
area: docs
owner: codex-c09-patagonia
claimed_at: 2026-10-22T13:48:36Z
created_at: 2026-10-22T13:48:31Z
completed_at:
branch: codex/brand-story-patagonia-c09-treatment
depends_on: []
scope:
  - docs/videos/story-everyday-patagonia-c09/script.md
  - docs/videos/story-everyday-patagonia-c09/visual-plan.md
  - docs/videos/story-everyday-patagonia-c09/script-evidence.md
---

# Revise Patagonia C09 narration after cold read

## Why

PR #1685's first 101-ID script passed an independent line-by-line source audit at head `1cf0c222cb4db560f35e031c4580440561edfe5d`, but a genuinely cold narration-only reader placed the story on HOLD. The reader could not connect Patagonia to the 1972 equipment company until late in the film, found the original origin/idea chapters too dense with metallurgy, names and dates, and wanted the 1977 piton press beside the chock teaching board to remain the clear payoff. The owner authorized a focused revision of the script, matching shot plan and author source note. The source PASS applies only to the old script/visual/evidence SHA trio, so revised bytes need a delta source audit and two fresh cold reads.

## Definition of done

- [x] Patagonia's accurate relationship to Chouinard's 1972 equipment business and the rock-damage stake arrive in the opening three lines (estimated ~20 seconds, actual timing pending); the 1973 clothing-label timing is clear without calling the 1972 company Patagonia.
- [x] Compress the long origin/idea sections and spoken name/date inventory while retaining the 1972 necessary fixed-and-documented piton exception, 1973 skepticism, and 1977 continued piton sales/manufacture as the main reveal. Close on the rock/next-climber choice without a repetitive CTA.
- [x] Script, visual rows and source/hook note match by ID and SHA. This author records measured text/count checks without claiming the old source PASS or cold reader verdict applies to new bytes; delta review, two fresh readers, visual preflight, owner script approval and paid gates remain pending.

## Steps

- [x] Read the independent 101/101 source audit and parent-delivered cold-read HOLD; claim only the three author files.
- [x] Revise six-chapter narration and the one-to-one visual plan; remove early apparel hanger and narrow the accounting shorthand.
- [x] Update source trace, loops, counts and hashes; run mechanical checks, commit/push PR #1685 as draft with no-auto-merge, and hand off exact deltas for independent delta review.

## How to verify

Hash all three authored files. Compare `^| c09dddd |` ID sets between script and visual plan; count illustrated/body seconds planning and maximum card run; count body Hanzi without source columns; run `git diff --check` and `npm run check:tasks` while preserving unrelated policy-blocked duplicate review ticket open copies; read PR head, draft state and `no-auto-merge` after push. The body duration and 70% image time still require actual later media.

## Notes

Old input SHA-256 values: script `3AEDEFFF6019A6F85F5BD6207B1FED9C3BD0CEAF4B4BF357A56C221F896BDA09`, visual `60D56443D75C3BBAEA472AD1F4672CC8E8D7B03E85D497ACDA43C8BB79311214`, author evidence `27D286E2BE01EFBDD271B85EEE7900E47F065B6E9CC0EA2ADA80ADD40D345A6E`. The independent audit receipt is in `docs/videos/story-everyday-patagonia-c09-script-review/independent-source-review.md` and will remain untouched. It suggested also removing a clothes-hanger visual at c090211 and narrowing c090615 to the cited-source limitation. The untracked review-task open copies in this worktree are outside scope and remain untouched.

Author revision on 2026-10-22: script `BF90CE8B5892F086EAD7221C2870B9B4C709DDD82CA1BDA3615B50EED371D041`, visual `40BA457390853A87B95938C484E00122196ABA8F43CD835D43AFADF6E7984603`, source/hook note `98235CE7B7ABB0D4285CB672DD98A64F74C643549E139F785E49ED7459253521`. Six chapters contain 83 script rows and exactly 83 visual rows, no duplicate IDs, 70 `shot` / 13 `stats`, max consecutive cards 2. Narration is 2,111 Hanzi; 300/min estimates 7:02 and 270/min 7:49, so actual ≥480-second body is **unresolved** and cannot be padded with repeated facts. Illustrated share is 84.3% by rows and 79.4% under 5-second-shot/7-second-card planning assumptions, not actual time. `git diff --check` passed. `npm run check:tasks` currently fails on two unrelated policy-blocked duplicate open/done review ticket IDs; do not remove those open files via this task. The old 101/101 source PASS remains historical; no new independent signoff is claimed.
