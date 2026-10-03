---
id: 2026-10-03-ai-terms-episode-calibration-plan
title: Plan the AI terms episode on calibration (Calibration), with Jev as the in-house example
status: done
priority: P2
area: docs
owner: claude-opus-5-5
claimed_at: 2026-10-03T14:57:59Z
created_at: 2026-10-03T14:57:59Z
completed_at: 2026-10-03T15:01:26Z
branch: claude/optimistic-hypatia-r2586e
depends_on: []
scope:
  - docs/videos/ai-term-calibration
---

# Plan the AI terms episode on calibration (Calibration), with Jev as the in-house example

## Why

The site owner asked for the Jev tutorial to become an episode of the AI terms series
(「AI 名詞十分鐘」). That series covers one general term per episode and keeps product and
model names out (`docs/videos/ai-terms/README.md` §查核規則), and Jev itself already has
its own P1 pilot, `2026-09-29-video-pilot-jev-decision-model`. The term behind Jev that
does not expire is calibration: whether an AI's stated confidence matches how often it
is right. The site's own use of Jev (three tiers, the non-English downgrade, shadow
measurement before thresholds) is the in-house example.

## Definition of done

- [x] `docs/videos/ai-term-calibration/brief.md` in the planner's eight sections plus the
      choice of term, three outline options (recipes A, B, C) with one recommended, the
      `terms.json` row to add, and the owner's decisions.
- [x] A demonstration that was actually run, with script and verbatim output in
      `docs/videos/ai-term-calibration/demo-log.md`.
- [x] The article and the production filed as their own tasks.

## Steps

- [x] Read the series spec, the planner prompt and the token pilot brief.
- [x] Open the first-party sources (scikit-learn calibration docs, arXiv 1706.04599,
      TypeSafe Confidence, Confidence-gated routing, Models, Jev 1.13 jaggedness).
- [x] Run the calibration demo on scikit-learn's bundled digits data.
- [x] Write the brief and the demo log.
- [x] File `2026-10-03-ai-term-calibration-article` and `2026-10-03-ai-term-calibration-video`.

## How to verify

Read `docs/videos/ai-term-calibration/brief.md` against
`.agents/skills/youtube-video/references/prompts/planner.md`; rerun the script in
`demo-log.md` with scikit-learn 1.9.1 and compare the JSON.

## Notes

- `terms.json` was deliberately not edited. Adding a row changes `CATALOG_COUNTS`
  (81) in `tools/video/long-form/plans.mjs`, the hash-bound `docs/videos/long-form/plans.json`,
  the duration review, and the admin catalog's hard-coded 473 entries. That belongs with
  the production task, after the article exists.
- TypeSafe's `confidence` is a summary of how concentrated the probability distribution
  is, not the probability of being right; a noul's value is the probability. This is
  the episode's second "你以為／其實" and the reason the brief never equates the two.
- The pilots used recipes A (token), B (context window) and C (RAG), so the recommended
  option uses A to avoid repeating C after RAG.
- `/claim-credit` was requested in the session; no such skill or command exists here.

- **Superseded 2026-10-03.** The owner meant TypeSafe's launch post itself; the episode is now planned in `2026-10-03-ai-terms-episode-system-one-plan`. Verification that day refuted three sentences in this brief about the site's own use of Jev (the non-English downgrade, the thresholds that decide, and the shadow measurement having produced numbers); they are corrected in the brief.
