---
id: 2026-10-24-prepare-c15-frixion-canonical-video-project
title: Prepare C15 FriXion canonical video project without paid calls
status: done
priority: P1
area: docs
owner: codex-c-series-integration
claimed_at: 2026-10-24T03:27:36Z
created_at: 2026-10-24T03:27:29Z
completed_at: 2026-10-24T06:51:49Z
branch: codex/c15-frixion-canonical-preflight-20261024
depends_on: []
scope:
  - docs/videos/story-everyday-frixion-c15
---

# Prepare C15 FriXion canonical video project without paid calls

## Why

The owner-approved C15 script and visual plan are Markdown/JSON preproduction evidence. A canonical machine-readable video project is needed for later nonpaid QA and, only after separate gates, a local pilot. Preserve the approved source bytes and the per-episode USD 25 stop.

## Definition of done

- [x] Preserve the six approved source blobs unchanged and map 87 sentences to six chapters, 72 stills and 15 postproduction cards.
- [x] Add video.json, series.json, brief.md, claims.md, verify-1.md and a conversion receipt without paid calls.
- [x] Verify 87/87 narration parity, exact shot/card counts, factsChecks and check:tasks.
- [x] Obtain independent read-only conversion review and resolve the T07 lint false positive in its own claimed core scope; document exact accepted head before PR completion.
- [x] Keep actual narration, visual time, cost routing, import, upload and publication as later separate gates.

## Steps

- [x] Compare all six original Git blob SHA-256 values against owner approvals before writing derived files.
- [x] Generate one machine scene per original line without sentence pre-split; mark the voice pronunciations as provisional.
- [x] Run focused lint, facts checks and task validation; preserve the sole lint error and six warnings as evidence. Targeted schema/lint/facts tests pass; drama.test.mjs exits 1 without case-level diagnostics on this Windows checkout.
- [x] Independent reviewer reads approved original and derived video/claim/card pairs against the locked bytes.

## How to verify

- node tools/video/cli.mjs lint --slug story-everyday-frixion-c15  (exit 0: 0 errors, 6 warnings after narrow lint fix)
- node tools/video/qa/facts.mjs via factsChecks: verify-1.md marks no claim NOT FOUND
- npm run check:tasks  (exit 0; unrelated old-task warnings)
- Recompute Git blob SHA-256 of six protected files and compare reviews/owner-script-approval.md; verify 87/87 video lines exactly reproduce visual-plan.json narration and script.md.
- git diff --cached --check after staging.

## Notes

Canonical receipt: docs/videos/story-everyday-frixion-c15/reviews/canonical-video-preflight-20261024.md. Approved full draft is 87 sentences/72 shots/15 cards. Paper postintro body is 513.12 seconds and body still share 79.28%, both unmeasured proxies. Paid calls remain HOLD until a deployed/read-back attributable USD 25 route, old charges/pending requests, provider prices and TTS/ASR/Jev costs are reconciled; actual postintro voice must reach 480 seconds before image purchase.

The T07 false positive has been removed in the separately claimed core lint task without changing approved text. Focused lint is 0 errors, 6 warnings; the independent conversion receipt is reviews/independent-canonical-conversion-20261024.md. No paid media, import, upload or publication occurred. The exact accepted PR head will be recorded in the PR and checked before merge.
