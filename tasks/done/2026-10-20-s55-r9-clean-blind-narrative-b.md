---
id: 2026-10-20-s55-r9-clean-blind-narrative-b
title: S55 r9 clean blind narrative B ballot
status: done
priority: P2
area: docs
owner: codex-s55-r9-clean-b
claimed_at: 2026-10-20T21:33:46Z
created_at: 2026-10-20T21:33:44Z
completed_at: 2026-10-20T21:35:06Z
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s55/review/r9-clean-blind-b.json
  - docs/videos/curio-s55/review/r9-clean-blind-b.md
---

# S55 r9 clean blind narrative B ballot

## Why

S55 needs a second context-isolated reader's narrative ballot for round 9.

## Definition of done

- [x] Record all 13 yes/no answers with cited evidence and matching before/after script hashes in the two scoped ballot files.

## Steps

- [x] Read the fixed CLI questions and only `script.md` as episode material before voting.
- [x] Freeze the ballot, then validate its answer shape with the narrative CLI.

## How to verify

`VIDEO_WORKDIR=/tmp/s55-r9-clean-b node tools/video/cli.mjs narrative --slug curio-s55 --answers docs/videos/curio-s55/review/r9-clean-blind-b.json --json` returns exit 1 with only `no_recap` in `failed`, matching the 12 yes and 1 no ballot.

## Notes

Script SHA-256 before and after: `b72d5d03ef71f86673b68b59c616b06ec404ea40c8cb46e02a682ea6f716c45f`. The repeated twelve-foot measurement at [s55018] and [s55038] drives the no vote. The first CLI validation saw no answers because it requires `answers` as an array of `{id, yes, evidence}`; the ballot was reshaped without changing votes and validation then matched the frozen result.
