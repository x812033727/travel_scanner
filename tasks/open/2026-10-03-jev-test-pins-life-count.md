---
id: 2026-10-03-jev-test-pins-life-count
title: JEV catalogue test pins the life article count, so every content batch past 960 breaks it
status: in-progress
priority: P1
area: api
owner: claude-opus-5-5-ai-terms-03
claimed_at: 2026-10-03T11:33:00Z
created_at: 2026-10-03T11:32:41Z
completed_at:
branch: claude/sweet-ramanujan-1v06fx
depends_on: []
scope:
  - apps/api/tests/test_guides_jev_review.py
---

# JEV catalogue test pins the life article count, so every content batch past 960 breaks it

## Why

`test_the_shipped_catalogue_costs_what_the_plan_measured` asserted that the lifestyle corpus
splits into exactly 12 chunks at `--chunk-size 80` and 17 under the token ceiling. Those are
functions of how many life articles exist: 12 holds up to 960. The AI-terms batches on this
branch (2026-10-03) took the corpus from 955 to 979, and the test failed with
`assert -(-979 // 80) == 12`. Any content batch would have tripped it the same way.

## Definition of done

- [x] The test still pins what the plan measured: the mean option cost (186 travel, 158 life,
      within 6) and that the token ceiling binds before `--chunk-size 80` (more chunks than
      80-per-chunk would give), and that no candidate is dropped.
- [x] It no longer pins the corpus size.
- [x] `pytest tests/test_guides_jev_review.py`, `ruff check`, `mypy` pass.

## Steps

- [x] Replace the pinned `chunk_size_only` / `real` counts with the ceiling-binds relation.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_jev_review.py -q && uv run ruff check tests && uv run mypy tests
```

## Notes

- Claimed with `--force`: the file is in the scope of `2026-09-22-jev-review-advisory-tool`,
  which is still `in-progress` under claude-fable-5-1 but was claimed 11 days ago, its branch
  `claude/jev-review-tool` is gone from origin, and the tool it built is on main. That ticket
  was not touched; its owner or the site owner should close it.
- Measured on 2026-10-03: travel 174 candidates, mean option 186.7, 3 chunks by size, 4 by
  tokens; life 979 candidates, mean option 159.3, 13 by size, 18 by tokens.
