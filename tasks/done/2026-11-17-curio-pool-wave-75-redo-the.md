---
id: 2026-11-17-curio-pool-wave-75-redo-the
title: Curio pool wave 75: redo the quarantined high scorers from real sources
status: done
priority: P2
area: docs
owner: claude-fable-heimao-topics
claimed_at: 2026-11-17T13:20:40Z
created_at: 2026-11-17T13:20:33Z
completed_at: 2026-11-17T13:47:55Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - apps/api/app/video_pools/data
---

# Curio pool wave 75: redo the quarantined high scorers from real sources

## Why

Wave 58–71 of the curio pool (238 single-episode cores) was quarantined because its sources do not
exist. The owner asked (2026-11-17) to score those cards for audience appeal first, check the high
scorers against the rest of the pool, and redo them from sources that are really read.

## Definition of done

- [x] The 238 quarantined cards have a calibrated audience score (kept out of `reviews/audience-*`, they are not selected topics).
- [x] The 67 cards at 7.15 or above are checked for collisions; the 46 that survive are researched again from real sources and reviewed by a non-author.
- [x] Adopted topics are in `batches/wave75-20261117.json` with a review receipt, selected or held, scored, and the pool and the admin bundle rebuild and pass their checks.

## Steps

- [x] Score the 238 cards (two reviewers per batch, six anchors plus eight controls).
- [x] Collision check, then ten research agents (ZT0–ZT9) and ten reviewers (R750–R759).
- [x] Merge, select, dedup decisions for the replaced cards, demand and audience scores, README section.

## How to verify

```bash
node tools/video/curio/pool/cli.mjs check
node tools/video/pool-admin/bundle.mjs check
npm run test:tools && npm run check:tasks
```

## Notes

- 46 directions: 37 adopted (33 selected, 4 held as chapters), 6 need more sources, 3 collided with existing topics (H01, G01, legacy S36) that a keyword check missed — a keyword pass is not enough, the research agents' own dedup caught two and a reviewer the third.
- 22 of the 33 selected topics pass 6.5. Demand is 1.0 for 31 of them, so the base score has to reach 7.6.
- The 43 replaced cards are `drop` in `dedup-decisions.json`; 15 old/new pairs are `distinct` on purpose, because a merge would pull the fabricated sources into the new topic.
- 195 cards are still quarantined: 171 scored below 7.15 (64 of them below 5), 24 collide with existing topics. Whether to remove them is the owner's call.
- The six `needs_check` topics list what is missing in their `notes`.
