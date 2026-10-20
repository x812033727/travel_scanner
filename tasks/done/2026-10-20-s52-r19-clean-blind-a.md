---
id: 2026-10-20-s52-r19-clean-blind-a
title: S52 R19 clean blind narrative ballot A
status: done
priority: P2
area: docs
owner: codex-s52-r19-clean-a
claimed_at: 2026-10-20T21:44:41Z
created_at: 2026-10-20T21:44:38Z
completed_at: 2026-10-20T21:45:55Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s52/review/r19-clean-blind-a.json
  - docs/videos/curio-s52/review/r19-clean-blind-a.md
---

# S52 R19 clean blind narrative ballot A

## Why

S52 R19 needs an independent narrative verdict from a reader who has not seen episode briefs, sources, prior reviews, or another reader's ballot.

## Definition of done

- [x] A 13-question yes/no ballot with scene citations and stable script hash is saved in the narrow review scope.
- [x] The fixed narrative CLI accepts the ballot, and the task is closed.

## Steps

- [x] Read general rules, then only `script.md` and the fixed questionnaire before voting.
- [x] Freeze the vote, claim this task, write the JSON and Markdown ballots, and validate with the narrative CLI.

## How to verify

`VIDEO_WORKDIR=/tmp/s52-r19-clean-a node tools/video/cli.mjs narrative --slug curio-s52 --answers docs/videos/curio-s52/review/r19-clean-blind-a.json --json` returns `passed: true` with 13 yes answers. `sha256sum docs/videos/curio-s52/script.md` returns the hash below.

## Notes

All 13 answers are yes. Script SHA-256 before and after the blind read, and after validation: `5c51bcff8ed8540059f6a0c456562e04223fd591cbedec0349b72ad5a29fe067`. No S52 task, review, brief, source, or sibling ballot was opened before voting. CLI implementation details were opened only after the vote was frozen to validate the ballot format. The CLI receipt was written under `/tmp/s52-r19-clean-a`.
