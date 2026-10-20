---
id: 2026-10-20-uber-mobility-delivery-x19
title: Produce Uber mobility to delivery reversal X19 preproduction
status: in-progress
priority: P2
area: docs
owner: codex-uber-x19
claimed_at: 2026-10-20T22:39:59Z
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

- [x] A reproducible six-chapter Traditional Chinese X19 script, 30–60 second compressed opener, three final lines, 107 cute-mystery unbranded illustration slots, 12 native statistic cards, two different 9:16 Shorts, and per-line primary-source evidence are frozen for review.
- [ ] An independent fact audit and two blind narrative reviews PASS on the frozen files, with revisions and new hashes if needed.
- [ ] Formal worker validates actual audio runtime, full US$25 cap, approved media, official bumpers, and real upload links before delivery.

## Steps

- [x] Check duplicate and SEC source availability; keep Gross Bookings, revenue, segment Adjusted EBITDA, and GAAP net income distinct.
- [x] Compose main/Short JSON and handoff documents with exact live SEC URLs, bytes, SHA, shot and Short mappings, budget and link plan.
- [ ] Commission independent source and narrative reviews using README SHA; respond to findings.
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

No paid media, real TTS, approved official 5/21-second bumper files, production-worker import, upload or PR exists in this worktree. SEC S1–S8 and date-support 8-Ks S3a/S5a are the accepted first-party material; see `source-matrix.md` and `publishing-handoff.md`. C03 Moleskine and C04 Bubble Wrap remain on source-access HOLD, so X19 follows X18 as a source-feasible topic. Keep task in progress until audit/blinds and actual production, then update status.
