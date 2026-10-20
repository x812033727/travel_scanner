---
id: 2026-10-20-s52-r17-official-merge
title: S52 R17 official isolated blind merge
status: done
priority: P2
area: docs
owner: codex-gpt6-root
claimed_at: 2026-10-20T21:17:40Z
created_at: 2026-10-20T21:17:40Z
completed_at: 2026-10-20T21:19:00Z
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s52/review/r17-isolated-merged-answers.json
  - docs/videos/curio-s52/review/r17-isolated-merge.md
  - docs/videos/curio-s52/review/r17-isolated-cli-receipt.json
---

# S52 R17 official isolated blind merge

## Why

Two independently frozen R17 ballots need an OR merge and an official narrative CLI verdict.

## Definition of done

- [x] Preserve original ballots, merge all 13 answers by the any-reader-Yes rule, and archive the CLI verdict.

## Steps

- [x] Confirm both readers reviewed the exact R17 script hash.
- [x] Run the official narrative CLI with the merged answers.

## How to verify

Check the frozen answer SHA values and the narrative CLI receipt.

## Notes

Formal R17 result: FAIL 12/13; shared no_recap No. See review/r17-isolated-merge.md.
