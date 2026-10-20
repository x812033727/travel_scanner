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

- [x] A reproducible six-chapter Traditional Chinese X19 script, 30–60 second compressed opener, three final lines, 106 cute-mystery unbranded illustration slots, 12 native statistic cards, two different 9:16 Shorts, and per-line primary-source evidence are frozen for review.
- [ ] An independent fact audit and two blind narrative reviews PASS on the frozen files, with revisions and new hashes if needed.
- [ ] Formal worker validates actual audio runtime, full US$25 cap, approved media, official bumpers, and real upload links before delivery.

## Steps

- [x] Check duplicate and SEC source availability; keep Gross Bookings, revenue, segment Adjusted EBITDA, and GAAP net income distinct.
- [x] Compose main/Short JSON and handoff documents with exact live SEC URLs, bytes, SHA, shot and Short mappings, budget and link plan.
- [x] Independently audit v2 and obtain two fresh first-reader ballots on its frozen SHA; archive the factual PASS and narrative HOLD.
- [ ] Revise v3 to resolve the shared Q8/Q13 findings, then obtain new same-SHA source and dual-blind reviews before PR.
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

v1 source audit was HOLD and both independent blind readers requested changes; v2 fixes the dated-app/market-exit and causal issues, removes opener spoilers and late recaps, and awaits independent v2 re-review. No paid media, real TTS, approved official 5/21-second bumper files, production-worker import, upload or PR exists in this worktree. SEC S1–S8 and date-support 8-Ks S3a/S5a are the accepted first-party material; see `source-matrix.md` and `publishing-handoff.md`. C03 Moleskine and C04 Bubble Wrap remain on source-access HOLD, so X19 follows X18 as a source-feasible topic. Keep task in progress until audit/blinds and actual production, then update status.

v2 frozen `video.json` SHA-256 `3dca7d0e7701b763673c32e12fa6a371283cf2f829ebde188e5b0839e4fd12cc` and `shorts.json` `2f67f9983a8bb393d5fc71e735bc586f5f9821f864dcf2923a2b30ff98e038a3` passed author lint 0/0, Shorts schema/episode links and docs-video tests. Independent [source audit](../../docs/videos/story-everyday-uber-x19/reviews/script-source-audit-v2-independent.md) re-fetched S1–S8 plus S3a/S5a from SEC with identical bytes/SHA and passed v1's three corrected date/causal blockers. Truly fresh [blind A](../../docs/videos/story-everyday-uber-x19/reviews/blind-a-v2-independent.md) and [blind B](../../docs/videos/story-everyday-uber-x19/reviews/blind-b-v2-independent.md) both marked mandatory Q8/Q13 NO: June crossover and unquantified dispatch contribution recur without a new turn, while late all-platform consumer/earner figures distract after the car/bag payoff. B additionally marked Q1 NO for an abstract first action and Q7 NO for the unanswered restaurant-side capacity question. Thus v2 narrative remains **HOLD**; v3 should open on a physical driver action, pay the restaurant question precisely or stop asking it, remove the 2022 all-platform-headcount coda, and make the ending a new sourced result or clean synthesis rather than repeating Q2. Shorts already stand alone, subject to actual audio and portrait QA. No PR or completed media claimed.
