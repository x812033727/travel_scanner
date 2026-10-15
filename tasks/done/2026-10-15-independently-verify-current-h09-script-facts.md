---
id: 2026-10-15-independently-verify-current-h09-script-facts
title: Independently verify current H09 script facts
status: done
priority: P2
area: docs
owner: codex-h09-fact-auditor
claimed_at: 2026-10-15T02:44:28Z
created_at: 2026-10-15T02:44:19Z
completed_at: 2026-10-15T02:49:15Z
branch: codex/curio-h09-earhart-20261015
depends_on: []
scope:
  - docs/videos/curio-h09/verify-1.md
---

# Independently verify current H09 script facts

## Why

The prior fact receipt was bound to a 95-line editorial draft SHA. F03 and Z01 changed, and the current formal script has 100 narration segments, so the old PASS cannot certify the current script.

## Definition of done

- [x] Independent source receipt names the current formal script, editorial draft, and claims SHA-256 values.
- [x] The two revised lines and all unchanged narration are checked against the source boundaries, with the result limited to factual text.

## Steps

- [x] Compared the old 95-line draft to the new 95-line draft by ID; only F03 and Z01 changed.
- [x] Compared concatenated current draft narration to all 100 video.json and script.md narration segments.
- [x] Checked F03/Z01 against claims C05/C14/C16 and current Purdue/ALI primary releases; reread the unchanged sections.
- [x] Wrote docs/videos/curio-h09/verify-1.md, preserving limits for new audio and later expedition reports.

## How to verify

- Get-FileHash -Algorithm SHA256 on docs/videos/curio-h09/script.md, script-draft.md, and claims.md.
- git diff --check
- npm run check:tasks

## Notes

Limited factual PASS is bound to formal script SHA F2890AA3BE81026F846B9F76F9BA59A1C8B69FEBF7D3D7A7BFB8C0EF6DECC0A1. Z01's inline source labels omit the directly relevant C05, while claims.md contains and supports that boundary; note as advisory, not a fact error. The 1937 Navy PDF full-page review is inherited from the prior independent audit rather than freshly downloaded in this round. New F03/Z01 audio is not covered. npm run check:tasks and git diff --check passed. The broad npm run test:docs-videos suite was attempted, but many unrelated fixture tests failed in the managed sandbox with Temp EPERM rename and held speech-journal fixtures; this does not verify the receipt.
