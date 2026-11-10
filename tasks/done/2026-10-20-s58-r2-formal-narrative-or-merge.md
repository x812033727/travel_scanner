---
id: 2026-10-20-s58-r2-formal-narrative-or-merge
title: S58 R2 formal narrative OR merge diagnostic
status: done
priority: P1
area: docs
owner: codex-s58-source
claimed_at: 2026-10-20T23:29:27Z
created_at: 2026-10-20T23:29:24Z
completed_at: 2026-10-20T23:32:03Z
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s58/review/r2-merge
---

# S58 R2 formal narrative OR merge diagnostic

## Why

Two clean-room readers reviewed the exact R2 S58 script and disagree on some criteria. The official OR result and CLI record must be archived before R3 author edits make the R2 creative hashes stale.

## Definition of done

- [x] The exact R2 ballots, official OR merge, CLI result and pre/post five-file hashes are archived for later audit.

## Steps

- [x] Preserve both raw ballots and convert all 13 votes without changing the reader judgments.
- [x] Run `panelVerdict`, `mergePanelVerdicts` and the official narrative CLI in an isolated workdir.
- [x] Record exact 8/13 HOLD, five required failures and creative-file pre/post SHA; send R3 author edit clearance.

## How to verify

`node docs/videos/curio-s58/review/r2-merge/build-merge.mjs`; the exact CLI invocation and outputs are in `docs/videos/curio-s58/review/r2-merge/cli-status.json`; archived SHA and expected failed IDs were independently checked from `merge-audit.json`, `cli.stdout.json` and `official-narrative-record.json`. `npm run test:docs-videos`; `npm run check:tasks`; `git diff --check`.

## Notes

See `docs/videos/curio-s58/review/r2-merge/summary.md`. Raw ballot A is 6/13 YES, B 7/13 YES. Official OR is 8/13 YES with required `no_spoiler`, `one_line`, `payoffs`, `no_recap`, `no_detour` failing; CLI exit 1, `passed:false`, zero advisory failures. Five creative hashes matched the R2 freeze before and after CLI. Original ballot copies match original source hashes. The first wrapper's final assertion expected string IDs but CLI's `failed` entries are objects; all CLI artifacts had already been saved. Corrected the wrapper check, did not rerun CLI, and independently validated the archive. R3 author clearance was sent after the snapshot.
