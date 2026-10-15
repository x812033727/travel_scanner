---
id: 2026-10-15-rebind-h09-source-verification-to-approved
title: Rebind H09 source verification to approved formal script
status: done
priority: P2
area: docs
owner: codex-gpt6-h09-source-bind
claimed_at: 2026-10-15T03:06:23Z
created_at: 2026-10-15T03:06:09Z
completed_at: 2026-10-15T03:09:45Z
branch: codex/curio-h09-earhart-20261015
depends_on: []
scope:
  - docs/videos/curio-h09/verify-1.md
---

# Rebind H09 source verification to approved formal script

## Why

The independent H09 fact receipt named a pre-submission `script.md` SHA-256 of F2890AA3…. The script gate submitted a regenerated formal file with SHA-256 D63D46A3…, so the byte-bound receipt no longer identified the exact file the owner approved. Keep the existing source review but independently check whether the formal narration text changed before rebinding it.

## Definition of done

- [x] `verify-1.md` binds the actual D63D46A3… formal script, with a clearly limited factual PASS and an explicit explanation of what can and cannot be inferred from the changed hash.
- [x] All 100 formal lines are reconciled with `video.json`, the 95-line editorial draft, H09-C01–C17 and the current Purdue cutoff.

## Steps

- [x] Recomputed the formal script, draft and claims SHA-256 values and compared every formal narration line to the current source JSON.
- [x] Checked that the editorial draft joins to the same narration text, rechecked Purdue's latest reported expedition status, and updated only `verify-1.md`.
- [x] Ran the task checker and diff whitespace check.

## How to verify

`Get-FileHash -Algorithm SHA256` on `script.md`, `script-draft.md`, `claims.md`; `node -e` comparison of 100 script and JSON lines, 95 joined draft lines and deterministic `screenplay(video.json)` output; `npm run check:tasks`; `git diff --check`.

## Notes

Current formal script SHA-256 D63D46A3E93F7469B9A610CDBD83FB599A1A313D9AAA0A0233EF02C1951C9F82; draft CF579A778769BCE9905B2C5C477C075FF3D140D9EE7433F48373732644D4D881 and claims 16C3E21AF7F7C3564C5672FEF07FF0911B55B82FD85372D197ED9C7BACB191B7 are unchanged. Formal line comparison was 100/100 with zero mismatches, draft joined text matched exactly, and current file bytes equal the generator output. The old F2890… file bytes are not retained in this worktree, so the exact byte difference cannot be attributed. Purdue's currently located latest update is dated October 14 and does not identify the Taraia Object; check again before final film and upload. This ticket does not attest the audio or backend approval state.
