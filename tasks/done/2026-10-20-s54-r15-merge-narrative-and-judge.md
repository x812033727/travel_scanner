---
id: 2026-10-20-s54-r15-merge-narrative-and-judge
title: S54 R15 merge narrative and judge policy
status: done
priority: P2
area: docs
owner: codex-s54-r15-merge-policy
claimed_at: 2026-10-20T22:49:42Z
created_at: 2026-10-20T22:49:39Z
completed_at: 2026-10-20T22:52:02Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s54/review/r15-merge-policy
---

# S54 R15 merge narrative and judge policy

## Why

The 15 R15 oral repairs changed the script after R14's narrative and policy PASS. Two fresh readers voted on the exact new script, and their answers need a formal fixed-rule merge and a new exact-version Jev policy result before new audio can be made.

## Definition of done

- [x] The two frozen independent ballots are checked against their official receipts, then merged without altering either ballot.
- [x] Official merged narrative and one Jev policy result are archived with the R15 creative hashes.
- [x] No creative edits, TTS, art, or music run during this review.

## Steps

- [x] Recompute the five creative file hashes and the two reader receipt bindings; apply `mergePanelVerdicts` OR.
- [x] Run official narrative CLI with merged answers, save its original receipt, then send one exact `policyRequest({doc, brief})` to Jev.
- [x] Preserve both reader dissent and the policy request/response hashes in a human-readable summary.

## How to verify

See `docs/videos/curio-s54/review/r15-merge-policy/summary.md`. The official narrative CLI exited 0 with 13/13 merged yes and no failures. The single Jev POST returned HTTP 200, `passed:true`; raw response and parsed receipt are archived. `npm run check:tasks` and a whitespace diff check are run before task closure.

## Notes

A voted 13/13 yes. B voted no on `payoffs` and `no_detour`; these remain in the raw ballot and merge audit. The fixed OR rule passes both because A supplied a cited yes. Policy scores were stance .66, demo N/A, advice .01, sponsored .22. `/workspace/.video-work/curio-s54/STOP` was present throughout this review; a subsequent audio worker may archive it to begin R15 TTS. New TTS and full check-audio are the next gate, not implied by this task.
