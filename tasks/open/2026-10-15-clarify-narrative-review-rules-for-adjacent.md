---
id: 2026-10-15-clarify-narrative-review-rules-for-adjacent
title: Clarify narrative review rules for adjacent answers and product histories
status: in-progress
priority: P1
area: tools
owner: codex-a01-gate
claimed_at: 2026-10-16T00:07:46Z
created_at: 2026-10-15T19:57:31Z
completed_at:
branch: codex/clarify-narrative-adjacent-20261016
depends_on: []
scope:
  - tools/video/core/narrative.mjs
  - tools/video/core/narrative.test.mjs
  - tasks/open/2026-10-15-clarify-narrative-review-rules-for-adjacent.md
---

# Clarify narrative review rules for adjacent answers and product histories

## Why

A01's genuine narrative round 9 rejected `chapters_link`, `payoffs` and `one_thread` after all six chapter checks/listeners completed. The exact raw results and 80-step audit chain replay successfully; this is not a parser error. The `payoffs` evidence is an immediate question and its next-line answer (`eghq` -> `ys5y`), while the panel question requires every answer to explicitly name its hook. House writing guidance distinguishes an immediate answer from a callback after several minutes. The frozen story also follows the practical evolution of a product through several historical participants; the panel's singular-protagonist wording leaves its applicability unclear. Real opener and listener regressions remain separate issues and must not be excused by this task.

## Definition of done

- [x] Adjacent question/answer pairs and distant callbacks have clear, consistent review criteria; unanswered or ambiguous questions still fail.
- [x] Product-history storytelling has an explicit scope consistent with the approved format, while unrelated examples and unsupported historical causation still fail. Do not assume every product montage has one story line.
- [x] Tests bind the precise questions and representative valid/invalid examples without claiming that a deterministic fixture proves a live model's narrative judgment.
- [ ] Existing failures, counters and request/result hashes remain intact. Any changed question creates a fresh request and review; no receipt is silently reinterpreted as PASS.

## Steps

- [x] Read the complete actual script and round 9 evidence; check live task/worktree ownership before editing the shared narrative module.
- [x] Compare `payoffs`, `chapters_link` and `one_thread` with current writing guidance and the approved frozen story scope. Resolve semantics before requesting another unchanged panel.
- [x] Propose the narrowest wording change with independent review and focused positive/negative tests. If writing guidance also changes, expand scope to both mirrored skill references before editing them.
- [ ] Follow separate merge/deploy authority and actual per-script source/hash review. Do not start media or create a pilot receipt through this task.

## How to verify

Run focused narrative tests and inspect captured payloads/hash differences. Include immediate answered questions, distant explicitly recovered hooks, genuinely missing answers, a coherent product-use progression, unrelated same-category examples, and fabricated transmission between inventors. After any separately authorized deployment, judge the actual current full script normally; a prompt change alone is not a PASS.

## Notes

Observed snapshot `actual-20261016-035053`, archive SHA `b988ed8af18e650985f85d6085d243c71032b0885172405645a40c86dc1a341a`, source `cf39296d597d36db3cafedc1c2ca5ae730dd104a34b1d1868fb5b83fc089c56b`. Independent diagnosis SHA `9b9258810e6794c46409891f0e96e8e1bfa641c88e084dc2bce57ab2b88ca44e`; replay SHA `0c93450f0c6597cc2fd62e1290288afe790a9c83834f07dbfa61e31fa2eabd2d`. No tenth review was requested. `2026-10-15-preserve-story-listener-setup-and-payoff` separately covers listener context; the new observation is that preserving distant callback context alone does not preserve a chapter's explicit product-use transition. A01 remains blocked with its genuine round 9 FAIL and no canonical pilot receipt or media.

2026-10-16 branch handoff: this task originated in draft PR #1510 and was copied verbatim into a new managed worktree based on `origin/main` `9fe80417c07684305f1e710e027b2cc2f2b5c22d`. Claim required `--force` only because the older `2026-10-14-ai-and-tech-videos-tell-one` task still says in-progress and lists these paths. Its PR #1504 was already merged as `c4911a059`, its named branch is absent locally and remotely, and it has no active worktree or open PR; this branch did not edit or release that owner's task. The new wording remains within this ticket's two code/test paths. It distinguishes adjacent answers from distant callbacks, permits a cold-open return to the earlier source of the question, and requires a product history to advance one concrete use problem without fabricated lineage. It changes the questions sent to future reviews; it does not mutate the existing A01 round 9 result. Focused `node --test tools/video/core/narrative.test.mjs`: 13/13 pass.

Independent review by the parent Codex agent confirmed the three revised questions retain explicit negative cases (unanswered questions, same-category example montages, unsupported inventor-to-inventor causation). It also reviewed the separate A01 one-line candidate against the preserved Winnetka Historical Society source: a 1928 departure with the son's homemade suitcase made from baby-carriage wheels and a telescoping wooden handle. The candidate describes only that family's homemade case; it does not claim no wheeled case was sold anywhere. The candidate remains in the external A01 temp folder and has not been installed.

The offline A01 candidate changes only `origin-01`/`zc7k`: 「開場那一家人，其實早就不必一路提箱子：1928 年出發時，母親拉著兒子做的箱子。」→「1928 年，母親拉著兒子做的箱子出發；輪子有了，這卻還是一家人的自製品。」 Source chapter SHA `0c449e490e86cb1f505e6e72fb9747f31cc7396729d86cb41c810ec432285080`; one-field candidate SHA `750e8a98a86a4e51a9d63ea017c221be854a6110be43c2007efeda8e141ca0e7`. The before/after line SHA values are in the external manifest. Using the frozen actual video, host lexicon and series metadata, offline `lintVideo` had 0 errors and 36 warnings both before and after; its estimated timeline changed from 520.833 to 520.1 seconds. This is not measured TTS and did not call the narrative judge.

Using the unchanged actual `video.json` SHA `16b290c78ea72bcd723cc99812ddae73dc838c8c461c64c7b4777c3ea4037abe`, the old/new blind panel payloads have the same narration SHA `1950a1e1dd4423edddc266558ca697a079adbc9516094a04d7bed211f5f2af6b`, 13 questions in the same order, and differ only in `chapters_link`, `payoffs`, `one_thread`. SHA256 of serialized old payload: `9da05b5d74fefceced8cee30383a0253f6e2bf54839b2e6cea7adc7d14abbf7e`; new payload: `fa80cd3711d4c90d959fbf2922c47bccce82679b8182f310024ab50f685fa306`. These are offline payload hashes, not a new model verdict. The prior A01 no answers still fail; a fresh review would be required after a separately authorized deployment and text correction. Current A01 remains genuinely FAIL, with no pilot receipt or media.

Focused test `node --test tools/video/core/narrative.test.mjs` passed 13/13; `tools/tasks.mjs check` passed with pre-existing stale-owner and overlapping-scope warnings; `git diff --check` passed. The optional combined narrative/story test could not load `pinyin-pro` because this new managed worktree has no `node_modules`; it exited before the story tests ran. Hosted CI will provide that broader check after PR creation.
