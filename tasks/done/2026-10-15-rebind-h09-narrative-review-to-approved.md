---
id: 2026-10-15-rebind-h09-narrative-review-to-approved
title: Rebind H09 narrative review to approved formal script
status: done
priority: P1
area: docs
owner: codex-h09-current-narrative-bind
claimed_at: 2026-10-15T03:06:29Z
created_at: 2026-10-15T03:06:22Z
completed_at: 2026-10-15T03:08:25Z
branch: codex/curio-h09-earhart-20261015
depends_on: []
scope:
  - docs/videos/curio-h09/narrative-blind.md
---

# Rebind H09 narrative review to approved formal script

## Why

The independent 13-question narrative receipt names an earlier `script.md` file SHA (F2890AA3…), while the owner's newly approved, regenerated formal script is D63D46A3…. A receipt bound to the wrong file cannot serve as current review evidence.

## Definition of done

- [x] The receipt names the exact SHA-256 of the current approved formal script and clearly states the unchanged narrative/tool binding and audio limitation.

## Steps

- [x] Compare the current file with deterministic `screenplay(video.json)`, all 100 scene/line IDs, and the persisted narrative record.
- [x] Recompute the 13-question panel verdict and quoted evidence against the current `video.json`.
- [x] Rebind only `narrative-blind.md` and run the task and diff checks.

## How to verify

`Get-FileHash docs/videos/curio-h09/script.md -Algorithm SHA256`; a read-only Node comparison using `screenplay`, `scriptCheckBinding`, `scriptCheckMatches`, `NARRATIVE_PANEL`, and `panelVerdict`; `npm run check:tasks`; `git diff --check`.

## Notes

Current file SHA and deterministic generated SHA both equal D63D46A3E93F7469B9A610CDBD83FB599A1A313D9AAA0A0233EF02C1951C9F82. The current 100-scene/100-line document retains narrative_hash 1617913c723b78bd, speech_hash f126475d033c526e, and script_hash a29a9e618b6485c254ab2e2a6446e69b30bcfc8955bb0450e7d542accd83858e; the stored narrative record matches all bindings. Its 13 question IDs and all 13 quoted line IDs/texts match current `video.json`, and a fresh local `panelVerdict` passes with no failed/advisory entries. F2890AA3… was a stale file-level fingerprint; its old bytes are not retained here to attribute the precise byte difference. This task does not renew audio or timeline approval.
