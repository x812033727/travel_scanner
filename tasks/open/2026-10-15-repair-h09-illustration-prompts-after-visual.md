---
id: 2026-10-15-repair-h09-illustration-prompts-after-visual
title: Repair H09 illustration prompts after visual QA
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-h09-art-fixes
claimed_at: 2026-10-15T03:38:42Z
created_at: 2026-10-15T03:38:34Z
completed_at:
branch: codex/curio-h09-earhart-20261015
depends_on: []
scope:
  - docs/videos/curio-h09/video.json
---

# Repair H09 illustration prompts after visual QA

## Why

H09's first full 92-shot MiniMax batch stopped cleanly after 28 manifest shots. Some selected images cannot enter the storyboard unchanged: two coral atolls were drawn as mountains, while `colorado-seaplane` passed at 7.18/10 despite an unrecognizable seaplane fused with a deckhand. Keep paid acceptable images and their valid cache keys; change only prompts with a concrete defect. The source review also corrected Colorado's ship type, so script and audio are being renewed before paid art resumes.

## Definition of done

- [ ] Every H09 shot has an accepted illustration or a documented owner-visible exception, with no factual contradiction or material style drift; only resume paid art after exact current script E9404ADD… and audio timeline 69E3FF3D… approvals are read back.
- [ ] Any new paid retakes fit the existing H09 US$3.80 image/judge hard cap and US$4.50 combined list-price stop ceiling.

## Steps

- [x] Wait for the current whole-batch `keyframes --takes 3` process to finish; collect judge failures and independent visual contradictions without changing `video.json` while it runs.
- [ ] Revise only evidence-backed failing shot prompts, lint, and make targeted retakes while preserving accepted caches.
- [ ] Inspect all selected images and record the resulting manifest, cost, and storyboard state in the H09 production task.

## How to verify

Run `node tools/video/cli.mjs lint --slug curio-h09`, targeted `keyframes --shot <ids> --takes 3 --dry-run` and then the paid rerun within the already authorized cap. Compare selected image hashes and judge verdicts in `<home>/mokaair-work/videos/curio-h09/keyframes/manifest.json`, inspect images, run `npm run check:tasks` and `git diff --check`.

## Notes

- Current full batch began only after current script D63D46A3… and audio timeline 4D9E93A6… were approved and H09's exact STOP was safely removed. It is still running as this task is filed; do not launch a second keyframes process or edit the visual source until it exits.
- The Curio skill accepts judge-passed illustrations unless they materially contradict narration/source or drift in style. Pseudo writing on a generic map does not alone justify a retake. Independent visual QA marked `captain-reads-line` content acceptable as an illustrative map despite the automatic text flag; `one-way-radio` has ~2 px black borders. `colorado-seaplane` has an actual fused aircraft/deckhand object error and merits correction.
- The running batch was stopped by the exact H09 `STOP` after 28 manifest shots and US$0.6480, with zero reservations. Independent review also found `search-from-howland` and `colorado-over-gardner` show mountainous islands instead of low coral atolls; `pilot-sees-empty` has only one failed take and a mountainous cliff. Current prompt edits replace the former's island view with open sea, require a flat coral ring for Gardner, separate deckhand from a complete floatplane, and constrain future visible atoll shores. Keep STOP until the corrected script and audio gates are reapproved.
- While fixing the Colorado picture, the source was checked against the U.S. Navy: Colorado was battleship BB-45, not a cruiser, and carried O3U Corsair floatplanes. The H09 spoken line and script draft were corrected; formal script SHA is now `E9404ADD9954E66AA6C26FC3725D7C0ABD09D91B9E571ED2631C152E4579633C`, which invalidates the prior script/audio approvals. Separate independent receipt tasks are reviewing the new script. Do not resume paid images before current script and audio readback.
- Owner approved exact E940 script and 69E3 audio timeline after a single B06 rerecording; both approvals were read back. The first 28 shot entries are now all selected, with zero `needs_review` after evidence-backed prompt revisions and targeted retakes. Current `video.json` SHA `2B84A62E17B47FA7B5BC8905CD9E01D148A619FF348610318E15E2AD87F39389`; media ledger 59 image plus 59 judge calls, US$0.7965, zero reservations. `pilot-sees-empty` was reduced to a cockpit close-up after two mountain-bearing attempts; `colorado-seaplane` now passes the judge as a generic floatplane but is not an exact O3U reconstruction, disclosed in `visual-qa.md`. The remaining 64 illustrations still need generation and inspection; no storyboard approval has been claimed.
