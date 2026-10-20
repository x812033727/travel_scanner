---
id: 2026-10-20-s54-r14-merge-narrative-and-judge
title: S54 R14 merge narrative and judge policy
status: done
priority: P2
area: docs
owner: codex-s54-r14-merge-policy
claimed_at: 2026-10-20T21:56:40Z
created_at: 2026-10-20T21:56:37Z
completed_at: 2026-10-20T21:58:44Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s54/review/r14-merge-policy
---

# S54 R14 merge narrative and judge policy

## Why

S54 R14 had two independent clean-blind narrative votes. Production needs their fixed-panel OR merge bound to the current script, plus exactly one Jev policy judgment on the current video and brief before audio resumes.

## Definition of done

- [x] Both reader ballots and official receipts are checked against the same script and panel hashes, and their answers are merged by the fixed OR rule.
- [x] The official narrative CLI records a passing merged verdict for the current production work directory.
- [x] One exact R14 Jev policy request is recorded with its raw reply, hashes, and parsed verdict.
- [x] STOP remains present; no paid TTS or creative edit occurs in this task.

## Steps

- [x] Validate A and B frozen ballots and run `mergePanelVerdicts`.
- [x] Run official narrative CLI with the merged answers and archive its receipt.
- [x] Build `policyRequest({doc, brief})` from exact R14 files, send once, and archive raw and parsed outputs.

## How to verify

See `docs/videos/curio-s54/review/r14-merge-policy/summary.md` for all input and output SHA-256 values. `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs narrative --slug curio-s54 --answers docs/videos/curio-s54/review/r14-merge-policy/merged-answers.json --json` exited 0. The resulting `/workspace/.video-work/curio-s54/review/narrative.json` matches the archived receipt byte for byte. The Jev request returned HTTP 200 and `passed:true`; raw response SHA-256 matches the parsed receipt. A final local check confirmed STOP remained present.

## Notes

Merged narrative: 13/13 yes, 0 required failures, 0 advisory failures. Jev policy: PASS, stance 0.69, demo not applicable, advice 0.01, sponsored 0.26. Exactly one policy POST was sent, without retry. Reader B was sent exact receipt paths and hashes for verification before taking over audio. This policy pass is a pre-audio gate, not a final QA or owner approval.
