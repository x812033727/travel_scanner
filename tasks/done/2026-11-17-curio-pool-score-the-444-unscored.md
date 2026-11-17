---
id: 2026-11-17-curio-pool-score-the-444-unscored
title: Curio pool: score the 444 unscored single-episode cores and repack the near misses
status: done
priority: P2
area: docs
owner: claude-heimao-topics
claimed_at: 2026-11-17T16:15:21Z
created_at: 2026-11-17T16:15:19Z
completed_at: 2026-11-17T16:35:14Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - apps/api/app/video_pools/data
  - apps/api/tests/test_video_pools.py
---

# Curio pool: score the 444 unscored single-episode cores and repack the near misses

## Why

444 selected single-episode cores in the curio pool had never been scored, so nobody could tell which of them
pass the 6.5 gate. They are already sourced and reviewed; scoring them is the cheapest way to find more passing
topics. The owner chose (2026-11-17) to score them all and repackage the near misses.

## Definition of done

- [x] Every selected single-episode core has an audience score (71 first answer the demand questions).
- [x] Cores at 6.0–6.5 get one round of repackaging; only rewrites that rescore 0.5 higher are adopted.
- [x] Pool and admin bundle rebuild and pass; README records the method and the result.

## Steps

- [x] Demand for 71 cores, two reviewers.
- [x] Nine scoring batches with anchors and controls, two reviewers each.
- [x] Repack rounds 10–13 (75 cores), rescored with controls, 30 adopted.

## How to verify

```bash
node tools/video/curio/pool/cli.mjs check
node tools/video/pool-admin/bundle.mjs check
npm run check:tasks
```

## Notes

- 35 pass straight away, 24 more after repackaging: cores at 6.5 or above go from 321 to 380, and all 1,335 selected cores are now scored.
- Pass rate is low (59 of 444) because these are older cards with long research-style questions and almost all have demand 1.0, so the base has to reach 7.6.
- The rewriters added two dates that were not in the verified content (N303, N2983); the editor removed them before rescoring. `cards.py` flags such numbers, keep running it.
- H36 is a legacy topic outside the batch files and cannot be repackaged by `apply.py`.
- `test_cores_filter_by_category_status_score_and_text` assumed some curio cores were still unscored; with every core scored the unscored page is empty, so the test now only checks that whatever it returns is unscored (the status partition is still checked by the total).
