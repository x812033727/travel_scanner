---
id: 2026-10-20-uber-mobility-delivery-x19
title: Produce Uber mobility to delivery reversal X19 preproduction
status: in-progress
priority: P2
area: docs
owner: codex-review
claimed_at: 2026-10-20T23:17:05Z
created_at: 2026-10-20T22:39:56Z
completed_at:
branch: codex/brand-story-uber-x19
depends_on: []
scope:
  - docs/videos/story-everyday-uber-x19
---

# Produce Uber mobility to delivery reversal X19 preproduction

## Why

The brand-story sequence needs a distinct, evidence-backed next topic after X18. Uber's 2020 Mobility/Delivery booking crossover is documented in short, accessible first-party SEC exhibits, but the common retelling confuses booking dollars with revenue or profit and credits a later Postmates acquisition for an earlier quarter.

## Definition of done

- [x] A reproducible six-chapter Traditional Chinese X19 script, 30–60 second compressed opener, three final lines, 102 cute-mystery unbranded illustration slots, 12 native statistic cards, two different 9:16 Shorts, and per-line primary-source evidence are frozen for review.
- [ ] An independent fact audit and two blind narrative reviews PASS on the frozen files, with revisions and new hashes if needed.
- [ ] Formal worker validates actual audio runtime, full US$25 cap, approved media, official bumpers, and real upload links before delivery.

## Steps

- [x] Check duplicate and SEC source availability; keep Gross Bookings, revenue, segment Adjusted EBITDA, and GAAP net income distinct.
- [x] Compose main/Short JSON and handoff documents with exact live SEC URLs, bytes, SHA, shot and Short mappings, budget and link plan.
- [x] Independently audit v2 and obtain two fresh first-reader ballots on its frozen SHA; archive the factual PASS and narrative HOLD.
- [x] Revise and freeze v3 to address the shared Q8/Q13 and B's Q1/Q7 findings.
- [x] Obtain new same-SHA source and dual-blind reviews on v3; both gates returned HOLD.
- [ ] Repair v3 source date and shared narrative failures in v4, then obtain new same-SHA source and dual-blind reviews before PR.
- [ ] Hand reviewed package to formal video worker, measure timing and audio QA, then create real YouTube IDs/links if the owner has supplied official assets and upload access.

## How to verify

From repo root:

```bash
node docs/videos/story-everyday-uber-x19/compose-video.mjs
node docs/videos/story-everyday-uber-x19/compose-shorts.mjs
node tools/video/cli.mjs lint --slug story-everyday-uber-x19
npm run test:docs-videos
npm run check:tasks
git diff --check
```

For Shorts, split `shorts.json` array into two temporary individual files and run `node tools/video/shorts/cli.mjs validate --file <file> --source-base docs/videos/story-everyday-uber-x19` on each. Composer also checks `episodeShortsProblems` against the freshly built main video.

## Notes

v1 source audit was HOLD. v2 source audit independently passed, but both fresh blind readers held Q8/Q13; blind B also held Q1/Q7. v3 rewrites the first line as an anonymous driver action, narrows the restaurant question and later shows Q3 partner growth, removes Q2/dispatch reprise and late whole-platform headcount, and reserves sourced 2022 Q4 segment Adjusted EBITDA as a new final answer. **v3 still needs its own independent SEC/source PASS and two new same-SHA blind passes.** No paid media, real TTS, approved official 5/21-second bumper files, production-worker import, upload or PR exists in this worktree. SEC S1–S8 and date-support 8-Ks S3a/S5a are the first-party material; see `source-matrix.md` and `publishing-handoff.md`. C03 Moleskine and C04 Bubble Wrap remain on source-access HOLD, so X19 follows X18 as a source-feasible topic. Author claim is released for independent reviewers; keep the task open until formal production.

v2 frozen `video.json` SHA-256 `3dca7d0e7701b763673c32e12fa6a371283cf2f829ebde188e5b0839e4fd12cc` and `shorts.json` `2f67f9983a8bb393d5fc71e735bc586f5f9821f864dcf2923a2b30ff98e038a3` passed author lint 0/0, Shorts schema/episode links and docs-video tests. Independent [source audit](../../docs/videos/story-everyday-uber-x19/reviews/script-source-audit-v2-independent.md) re-fetched S1–S8 plus S3a/S5a from SEC with identical bytes/SHA and passed v1's three corrected date/causal blockers. Truly fresh [blind A](../../docs/videos/story-everyday-uber-x19/reviews/blind-a-v2-independent.md) and [blind B](../../docs/videos/story-everyday-uber-x19/reviews/blind-b-v2-independent.md) both marked mandatory Q8/Q13 NO: June crossover and unquantified dispatch contribution recur without a new turn, while late all-platform consumer/earner figures distract after the car/bag payoff. B additionally marked Q1 NO for an abstract first action and Q7 NO for the unanswered restaurant-side capacity question. Thus v2 narrative remains **HOLD**; v3 now addresses those exact findings. Shorts already stand alone, subject to actual audio and portrait QA. No PR or completed media claimed.

v3 frozen author `video.json` SHA-256 `377d045d160e46ddd2ed3eaa08d30b5ecfd45f02e6a20dd7f6f6e1526604ca48`, `shorts.json` `bc2c17924498699adc6f8267ae820589ec7321c2e0f2e63e9931e10357f44c64`; other hashes and checks are in [`README.md`](../../docs/videos/story-everyday-uber-x19/README.md). Lint 0/0, `episodeShortsProblems` empty, both Shorts CLI validations passed, docs-video tests 236/236, tasks check exit 0 and `git diff --check` passed. The v2 review files above remain the record for the old hash only; no v3 independent PASS is claimed.

v3 independent [SEC audit](../../docs/videos/story-everyday-uber-x19/reviews/script-source-audit-v3-independent.md) re-fetched all ten S1–S8/S3a/S5a originals, matched bytes/SHA, and returned **HOLD** on `x190419`: S4 dates September only for grocery Gross Bookings' annualized run rate; the “over ten countries including Taiwan” statement is current at the 2020-11-05 third-quarter release, not explicitly September. The source matrix, narration and JSON need the same date repair. Fresh [blind A](../../docs/videos/story-everyday-uber-x19/reviews/blind-a-v3-independent.md) and [blind B](../../docs/videos/story-everyday-uber-x19/reviews/blind-b-v3-independent.md) both answered mandatory Q8 and Q13 **No**: a repeated 2021 Q4 ordering line and the merchant pickup/product-fact detour do not advance the driver-phone/bookings question. A additionally marked Q4 No. Both Shorts stand alone on paper. Thus v3 has a factual and narrative **HOLD**; v4 needs a new freeze, independent source audit and two fresh first-blind readers. No formal media worker import, measured TTS, official bumper assets, MP4, upload, true links or PR exists for X19.
