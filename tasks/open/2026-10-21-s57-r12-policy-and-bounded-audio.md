---
id: 2026-10-21-s57-r12-policy-and-bounded-audio
title: S57 R12 policy and bounded audio readiness
status: in-progress
priority: P1
area: docs
owner: codex-s57-production-gate
claimed_at: 2026-10-21T01:27:18Z
created_at: 2026-10-21T01:27:14Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-s57/review/r12-media-readiness
  - docs/videos/curio-s57/review/r12-technical-audio
---

# S57 R12 policy and bounded audio readiness

## Why

S57 R12 has source, written visual, and formally bound narrative PASS. Before paid voice work, this exact version still needs a one-shot policy verdict, honest handling of the manual site's owner cards, and a bounded technical audio pass.

## Definition of done

- [x] Bind the current five SHA-256 values and R10 narrative record; run and retain the one-shot policy decision.
- [x] Submit and pull outline/script site cards; record any delegated local choice without claiming site owner review.
- [x] Finish one bounded original TTS pass and one full technical audio check; preserve its 43 flags. An audio card cannot be represented as approved while the check and listening remain HOLD.
- [x] Write first-pass receipts and verify hashes, lint, and task board. Follow-up human listening and any bounded corrections remain a separate gate.

## Steps

- [x] Read the curio/youtube workflow and current source gates.
- [x] Preflight the 159-line, 3,121-character Gemini Sulafat dry run and monthly quota.
- [x] Submit one policy POST, no retry; it passed as explainer.
- [x] Register and submit manual outline/script site cards; both await owner. Record locally delegated A and script continuation with an explicit note.
- [x] Observe and validate the bounded TTS and audio check; keep the audio card pending because 43 transcript flags need listening/conditional correction.

## How to verify

`sha256sum docs/videos/curio-s57/{research.md,brief.md,claims.md,video.json,script.md}`; `node tools/video/cli.mjs lint --slug curio-s57 --json`; inspect `docs/videos/curio-s57/review/r12-media-readiness/` and `r12-technical-audio/`, including the one-POST receipt, site card states, and TTS run plan; `npm run check:tasks`.

## Notes

Manual `review-push --gate outline` found 0 parseable options in the A/B table and sent an owner-choice card. The local A decision follows the user's delegated recommendation, not a Jev pick or owner personal review. Script card is also site-pending. The original 159/159 TTS run finished; the one full audio check exited 1 with 43 flags and no missing heard text. [The 2026-10-22 first-pass triage](../../docs/videos/curio-s57/review/r12-technical-audio/first-pass-triage-20261022.md) identifies numbers and meaning shifts to hear first. No `--redo` or new TTS run has occurred. A private STOP now prevents accidental paid art before the audio/storyboard gates.
