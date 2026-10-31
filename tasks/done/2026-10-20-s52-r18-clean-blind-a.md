---
id: 2026-10-20-s52-r18-clean-blind-a
title: S52 R18 clean isolated narrative blind reader A
status: done
priority: P2
area: docs
owner: codex-s52-r18-clean-a
claimed_at: 2026-10-20T21:25:39Z
created_at: 2026-10-20T21:25:37Z
completed_at: 2026-10-20T21:28:28Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s52/review/r18-clean-blind-a.json
  - docs/videos/curio-s52/review/r18-clean-blind-a.md
---

# S52 R18 clean isolated narrative blind reader A

## Why

S52 R18 needs a fresh, independent answer to the fixed 13-question narrative panel before any merged verdict or author revision. This reader must see only the panel questions and the current script before voting.

## Definition of done

- [x] A cited, SHA-bound 13-question blind ballot is saved in `docs/videos/curio-s52/review/r18-clean-blind-a.json` and `.md`.
- [x] The CLI accepts the ballot and reports its exact yes/no result.

## Steps

- [x] Read repository rules; claim the two ballot paths.
- [x] Fetch fixed questions, read only the script and questions, verify script SHA before and after, and freeze 13 independent answers.
- [x] Check the frozen answers with the narrative CLI; record and close the task.

## How to verify

`sha256sum docs/videos/curio-s52/script.md` returned `1a5d07020b2f15555f3359d31ecf6d90c6f8cb4780c8d3159e4c7cc2544d6857` before and after the read and again after the ballot. `VIDEO_WORKDIR=/tmp/s52-r18-clean-a node tools/video/cli.mjs narrative --slug curio-s52 --answers docs/videos/curio-s52/review/r18-clean-blind-a.json --json` accepted all 13 cited entries and returned the expected exit code 1 for four required no answers.

## Notes

Result: 9 yes, 4 no. Failed IDs: `chapters_link`, `payoffs`, `no_recap`, `no_detour`. The ballot contains script-line citations and rationale for every vote. The CLI requires `answers` as an array of `{id, yes, evidence}`; the saved JSON uses that form. No sibling ballot, prior episode review, brief, or source file was read before voting. This task changed only its own task record and two ballot files.
