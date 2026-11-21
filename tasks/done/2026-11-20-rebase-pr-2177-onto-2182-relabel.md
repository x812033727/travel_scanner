---
id: 2026-11-20-rebase-pr-2177-onto-2182-relabel
title: Rebase PR 2177 onto #2182, relabel w-heimao waves, merge N8038 and enforce 6.5 threshold
status: done
priority: P2
area: docs
owner: antigravity-pr2177-review
claimed_at: 2026-11-20T11:25:42Z
created_at: 2026-11-20T11:25:34Z
completed_at: 2026-11-20T11:43:34Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - docs/videos/story-plans/brand-stories-100/README.md
  - apps/api/app/video_pools/data
---

# Rebase PR 2177 onto #2182, relabel w-heimao waves, merge N8038 and enforce 6.5 threshold

## Why

PR #2182 (W-axis heimao migration, 89 cores `N9001–N9091`) merged into `main` as `5bb92a2c` while draft PR #2177 (`codex/curio86-why115`, Curio waves 86–116 + So That's Why waves 115–145) was open. Merging them surfaced:
- 11 conflicting generated/selection files in `docs/videos/history-curiosity/pool` and `apps/api/app/video_pools/data/pools.json`;
- batch-name collision (`wave86-w-heimao` / `wave87-w-heimao` vs #2177's waves 86 & 87) and missing rejected N-IDs (`N9055`, `N9089`) in `not_added`;
- duplicate Akagi ice-bar topic (`wave111` `N8038` score 7.13 vs `w-heimao-02` `N9085` score 7.97);
- 65 selected non-W Curio cores in PR #2177 (waves 86–107) scoring below the unified 6.50 blended threshold;
- 5 double-question-mark questions (`N7948`, `N7976`, `N7978`, `N7998`, `N8006`).

## Definition of done

- [x] `codex/curio86-why115` merged cleanly with `origin/main` (including PR #2182) with zero conflict markers.
- [x] PR #2182 batches and batch reviews renamed to `w-heimao-01-20261119` / `w-heimao-02-20261119`, README headings and links updated, `N9055`/`N9089` recorded in `not_added` (55+1 = 56 in `w-heimao-01`).
- [x] `N8038` merged into canonical `N9085` in `dedup-decisions.json` with all 10 sources preserved on `N9085` and `N8038` scores archived in `merged_evaluations`.
- [x] All 65 sub-6.5 selected Curio cores from PR #2177 moved to `selection.json` `held` and archived in `held_evaluations` across `reviews/audience-*.json` and `reviews/demand-*.json`.
- [x] 5 double-question-mark questions rewritten to single `？` without changing factual scope.
- [x] Curio pool, admin `pools.json`, So That's Why pool, tools tests, and API pool/backup tests all pass.

## Steps

- [x] Merge `origin/main` into `codex/curio86-why115`.
- [x] Rename `wave86-w-heimao` / `wave87-w-heimao` batch & review files to `w-heimao-01` / `w-heimao-02` and add `N9055`/`N9089` IDs in `not_added`.
- [x] Merge `N8038` into `N9085` in `dedup-decisions.json` and relocate `N8038` scores to `merged_evaluations`.
- [x] Move 65 sub-6.5 cores (`N7912–N8018`, 4.57–6.47) to `held` and relocate their scores to `held_evaluations`.
- [x] Rewrite the 5 double-question-mark questions to single `？`.
- [x] Rebuild Curio pool (`2026-11-20-curio-1956`, 1,956 selected, 370 held) and `apps/api/app/video_pools/data/pools.json`, update READMEs, and run all checks.

## How to verify

- `NODE_OPTIONS=--max-old-space-size=4096 node tools/video/curio/pool/cli.mjs check`
- `NODE_OPTIONS=--max-old-space-size=4096 node tools/video/so-thats-why/pool/cli.mjs check`
- `node tools/video/pool-admin/bundle.mjs check`
- `node tools/video/long-form/cli.mjs check`
- `node --test tools/video/curio/pool/pool.test.mjs tools/video/so-thats-why/pool/pool.test.mjs tools/video/pool-admin/bundle.test.mjs`
- `npm run test:tools && npm run check:tasks`
- `cd apps/api && uv run pytest tests/test_video_pools.py tests/test_video_backup.py`

## Notes

- Owner decisions (2026-11-20): merge #2182 first, then update #2177; canonical `N9085` absorbs `N8038`; enforce 6.50 blended threshold across all axes in #2177; relabel #2182 waves to `w-heimao-01`/`w-heimao-02` while preserving `N9001–N9091` IDs; fix 5 double-question-mark questions.
- Post-build invariants verified: `selected_candidates=1956`, `held_candidates=370`, `high_similarity_pending=0`, `cross_series_pending=0`, `N9085` has alias `N8038` and 10 `source_refs` from both `w-heimao-02-20261119` and `wave111-20261120`, zero new selected candidates under 6.50, zero double-question-mark new candidates.
- Remaining minor notes (non-blocking): 96/166 #2177 Curio candidates have unsplit `source_locator` strings (cosmetic), 1 STW source (`R141-S06`) uses a Wikimedia Commons CC BY-SA photo reference, and #2177's 31 done task files used `--force` claims after #2181 merged.
