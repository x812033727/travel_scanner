---
id: 2026-10-20-uber-mobility-delivery-x19
title: Produce Uber mobility to delivery reversal X19 preproduction
status: open
priority: P2
area: docs
owner:
claimed_at:
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

- [x] A reproducible six-chapter Traditional Chinese X19 script, 30–60 second compressed opener, three final lines, 95 cute-mystery unbranded illustration slots, 12 native statistic cards, two different 9:16 Shorts, and per-line primary-source evidence are frozen for review.
- [ ] An independent fact audit and two blind narrative reviews PASS on the frozen files, with revisions and new hashes if needed.
- [ ] Formal worker validates actual audio runtime, full US$25 cap, approved media, official bumpers, and real upload links before delivery.

## Steps

- [x] Check duplicate and SEC source availability; keep Gross Bookings, revenue, segment Adjusted EBITDA, and GAAP net income distinct.
- [x] Compose main/Short JSON and handoff documents with exact live SEC URLs, bytes, SHA, shot and Short mappings, budget and link plan.
- [x] Independently audit v2 and obtain two fresh first-reader ballots on its frozen SHA; archive the factual PASS and narrative HOLD.
- [x] Revise and freeze v3 to address the shared Q8/Q13 and B's Q1/Q7 findings.
- [x] Obtain new same-SHA source and dual-blind reviews on v3; both gates returned HOLD.
- [x] Repair v3 source date and shared narrative failures in v4, rebuild all derived files and freeze author package.
- [x] Obtain new same-SHA source and dual-blind reviews of v4; source passed, shared Q8/Q13 narrative HOLD.
- [x] Revise, rebuild, validate and freeze v5 against both blind readers' exact blockers.
- [x] Obtain new same-SHA source and dual-blind reviews of v5; source passed, but both blind readers held Q7/Q8.
- [x] Revise and freeze v6, then obtain a new independent source audit and two new first-reader ballots on its exact SHA; source passed but both readers held Q8.
- [x] Repair v6's shared repetition in v7 and obtain new same-SHA source/two blind reviews; source passed but both readers held Q8/Q13.
- [ ] Repair v7's repeated accounting distinction and detached App/grocery aside in a new frozen version; repeat all independent gates before PR.
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

v4 [author response](../../docs/videos/story-everyday-uber-x19/reviews/v4-author-response.md) maps the exact date and Q4/Q8/Q13 repairs; it is not an independent vote. The 2020 Q3 S4 matrix and `x190419` now distinguish September's grocery Gross Bookings **annualized run rate** from the **2020-11-05 announcement-time** count of over ten countries including Taiwan. The repeated `x190516` sign and `x190606` ranking are removed; the unused `x190517–518` merchant/pickup metrics are removed. Opening Q4-style section cues are rewritten as events, and the driver/restaurant/site-order actions make the same illustrative phone more concrete. Six chapters, 114 lines, 98 stills, 12 native cards, 25 ordered loops, 187-character condensed opener and 2,581-character substantive body are frozen in `video.json` SHA-256 `5feac02ca62feb4625959c1bd8a48266d185e84ac3776783fdc3b3eddb628988`; unchanged `shorts.json` SHA-256 `bc2c17924498699adc6f8267ae820589ec7321c2e0f2e63e9931e10357f44c64` is revalidated against the new main-shot hash. Main lint 0 errors/0 warnings; both Short individual schemas and source hashes PASS; `episodeShortsProblems` empty; `test:docs-videos` 236/236 and `check:tasks` exit 0; `git diff --check` clean. All companion hashes are in README. **Next gate:** fresh independent SEC audit and two truly first-blind ballots on exact v4 JSON, then measured TTS and official media. No paid calls, MP4, true platform links or PR exist for X19.

v4 [independent SEC audit](../../docs/videos/story-everyday-uber-x19/reviews/script-source-audit-v4-independent.md) re-fetched the ten originals, matched bytes/SHA and passed the corrected S4 announcement date on frozen `video.json` SHA `5feac02c...`. Two genuinely fresh [blind A](../../docs/videos/story-everyday-uber-x19/reviews/blind-a-v4-independent.md) / [blind B](../../docs/videos/story-everyday-uber-x19/reviews/blind-b-v4-independent.md) both marked mandatory Q8 and Q13 **NO**. A found `x190416` immediately repeated Q3 rankings and `x190519–521` introduced a customer-overlap detour; B found `x190614`/`x190624` repeated the 2022 lead and `x190212–213` listed retail/package services without a payoff. Both Shorts stood alone on paper. Thus v4 narrative was **HOLD**, not PR-ready; its source PASS cannot transfer to later revisions. The earlier v4 author's “next gate” statement above is historical.

v5 [author response](../../docs/videos/story-everyday-uber-x19/reviews/v5-author-response.md) deletes the shared Q8/Q13 repetitions and detours, keeps the S1 restaurant/onboarding-versus-market-exit mechanism and the S5/S6 cost/retention boundary, and rebuilds all derived files. Candidate `video.json` SHA-256 `c6c442fdf02e65a86be1eaf7115a91a8962a1231a394956e9fca61187110768b`, `shorts.json` `b6b0212372d776c96572450baa8e9c4350499c72923d088ad0bd6833e8681d95`; source/narration/visual hashes in README. Six chapters, 110 lines, 95 stills, 12 native cards, 24 loops, 187-character compressed opener and 2,506-character written body. Lint 0/0; both Shorts standalone schema and shot hash PASS; docs-video tests 236/236; task check and diff check pass. Paper estimate is ~8:21 at 300 written characters/minute; **not measured TTS**. Next: independent SEC audit and two new first readers on exact v5 SHA; only then PR readiness. Formal worker access, real TTS ≥8:00, official 5s/21s bumpers, media, US$25 actual spend, MP4, true platform links remain outstanding. No paid calls or PR in this worktree.

v5 [independent SEC audit](../../docs/videos/story-everyday-uber-x19/reviews/script-source-audit-v5-independent.md) passed the frozen claims after re-fetching all ten first-party originals; the 2026-10-21 raw SEC responses gained a nine-byte rotating script URL, and normalizing only that tag restored the earlier source-matrix bytes exactly. Two genuinely fresh [blind A](../../docs/videos/story-everyday-uber-x19/reviews/blind-a-v5-independent.md) and [blind B](../../docs/videos/story-everyday-uber-x19/reviews/blind-b-v5-independent.md) both marked mandatory **Q7 and Q8 NO**: `x190505` promises an answer to whether integrating Postmates *changed* losses, while later segment figures cannot establish that cause; `x190218` repeats the eight-market fact from `x190215`. A also marked Q5/Q13 NO, while B marked those YES. Both Shorts stand alone on paper. Under the two-reader rule, v5 narrative is **HOLD**. Revise v6, freeze all derived files, and require a new exact-SHA source audit plus two genuinely new blind readers. No measured media, MP4 or real YouTube links are claimed.

v6 [author response](../../docs/videos/story-everyday-uber-x19/reviews/v6-author-response.md) repairs the v5 shared blockers and A's additional Q5/Q13 issues. `x190505` now leads to the sourced user migration; `x190516` explicitly says the department total cannot identify Postmates' separate earnings effect. `x190218` advances from restaurant onboarding to a customer order without repeating eight markets. `x190601` answers the prior chapter's positive-indicator question in its first sentence. The late grocery branch is replaced with the S2/S6 same-quarter Delivery adjusted EBITDA loss narrowing of US$71m, with no acquisition attribution. Rebuilt v6 `video.json` SHA-256 `a3149c4904182bf473a7d452c3e5a80de790402c4b240e10da4b2610e1dfbaf8`; regenerated but content-identical `shorts.json` SHA-256 `b6b0212372d776c96572450baa8e9c4350499c72923d088ad0bd6833e8681d95`. Six chapters, 110 lines, 95 stills, 12 native cards, 24 loops, 187 opening chars and 2,507 substantive body chars (~8:21 at 300/min) remain. Main lint 0/0, both standalone Short schema/shot-hash checks passed, docs-video tests 236/236, tasks check exit 0 and diff check clean. The source matrix identifies its 10/20 SEC bytes/raw hashes as historical and the 10/21 rotating script-tag comparison; v6 requires a **new** independent source audit and two **new** same-SHA blind ballots before PR. No real TTS timing, image generation, official bumper media, MP4, upload or true links are claimed. Author claim is released for those reviewers; leave this task open for formal media work.

v6 [independent SEC audit](../../docs/videos/story-everyday-uber-x19/reviews/script-source-audit-v6-independent.md) passed the same-SHA source facts after re-fetching all ten originals. Fresh [blind A](../../docs/videos/story-everyday-uber-x19/reviews/blind-a-v6-independent.md) and [blind B](../../docs/videos/story-everyday-uber-x19/reviews/blind-b-v6-independent.md) both marked required Q8 No on `x190421` repeating the still-unclosed Postmates agreement from `x190412`. v6 narrative was HOLD. The [v7 author response](../../docs/videos/story-everyday-uber-x19/reviews/v7-author-response.md) removed that repeated clause; v7 video SHA `f4e373a53a3424f29f9c3e511f13c2489ac9c7e93c4500413038060d8d08a385`, unchanged Shorts SHA `b6b0212372d776c96572450baa8e9c4350499c72923d088ad0bd6833e8681d95`. Six chapters, 110 lines, 95 stills, 12 cards, 24 loops and 2,496 substantive written characters (~8:19 at 300/min on paper) pass author lint 0/0, both Short validators, docs-video 236/236, task check and diff check. Actual TTS remains unmeasured.

v7 [independent SEC audit](../../docs/videos/story-everyday-uber-x19/reviews/script-source-audit-v7-independent.md) re-fetched S1–S8/S3a/S5a at the current raw hashes and passed facts; the shortened `x190421` did not add an acquisition claim. Two new first readers [A](../../docs/videos/story-everyday-uber-x19/reviews/blind-a-v7-independent.md) and [B](../../docs/videos/story-everyday-uber-x19/reviews/blind-b-v7-independent.md) both marked required **Q8 and Q13 No**. A finds `x190603` repeats the segment-versus-GAAP caveat from `x190321` without a callback and the `x190417–419` App/grocery/Taiwan aside detaches from the booking/profit question. B separately finds `x190617` repeats the prior two-route growth/payoff distinction and `x190210`'s Mobility-app illustration sidesteps the driver-destination question; B also marks Q7 No. Both Shorts stand alone. Thus v7 narrative is **HOLD**: do not open a PR or start paid generation from this SHA. Next editor should narrow these App/grocery/accounting passages to story movement, answer the driver question with a supported observation or reframe the question, then freeze and repeat source/two genuinely fresh narrative audits. Formal media, official animation files, measured body audio, actual US$25 ledger, MP4 and platform IDs remain unavailable. This task is released for handoff.
