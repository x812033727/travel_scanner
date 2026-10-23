---
id: 2026-10-07-keep-renewed-final-evidence-notes-portable
title: Keep renewed-final evidence notes portable
status: review
priority: P2
area: tools
owner: codex-renewed-final-evidence-hygiene-20261007
claimed_at: 2026-10-07T04:06:31Z
created_at: 2026-10-07T04:05:55Z
completed_at:
branch: codex/renewed-finals-host-handoff-20261007
depends_on: []
scope:
  - tasks/open/2026-10-01-hand-off-owner-approved-renewed-finals.md
  - tasks/open/2026-10-07-continue-imported-language-units-before-requiring.md
  - tasks/open/2026-10-07-handle-a-no-cut-range-in.md
  - tasks/open/2026-10-07-imported-language-runner-hides-native-speech.md
  - tasks/open/2026-10-07-support-proven-thumbnail-encoding-in-renewal.md
---

# Keep renewed-final evidence notes portable

## Why

The renewed-final evidence notes include operator-specific home paths. The full
tools check correctly rejects those new tracked paths. Keep durable artifact
names and hashes while expressing the operator root as `<home>`.

## Definition of done

- [x] Tracked handoff notes pass the repository host-detail policy without
      changing their evidence names, hashes or operational meaning.

## Steps

- [x] Replace the five affected notes' local home roots with `<home>`.
- [x] Run the repository hygiene test and task validation.

## How to verify

`node --test tools/repo-hygiene.test.mjs` and `node tools/tasks.mjs check`.

## Notes

The full Windows tools run completed with exit 1: 1,948 passes, 11 failures and
13 platform skips. Its new host-detail failure is fixed here; the other failures
are Windows FFmpeg/filter-path, path-separator and speech-journal rename issues
outside this documentation scope. The successful focused native-unit tests and
exact production-image isolation are separate evidence from that full-suite exit.
The focused hygiene test passed 3/3, exit 0; task validation and diff checks
passed. Only portable note paths changed, with no production operation.
