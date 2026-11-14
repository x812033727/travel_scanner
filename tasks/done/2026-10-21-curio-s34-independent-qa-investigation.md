---
id: 2026-10-21-curio-s34-independent-qa-investigation
title: Investigate S34 policy and channel-link QA failures
status: done
priority: P2
area: docs
owner: codex-s38-r8j-card-review
claimed_at: 2026-10-21T00:39:00Z
created_at: 2026-10-21T00:39:00Z
completed_at: 2026-10-21T00:41:00Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s34/qa-investigation-20261021.md
---

# Investigate S34 policy and channel-link QA failures

## Why

S34's final cut has two failed checks. A separate review needed to explain whether either failure comes from the video or from the judge and cloud network.

## Definition of done

- [x] Bind the read-only investigation to the actual final video and QA hashes.
- [x] Compare the sponsor score with sibling episodes and the exact S34 CTA without buying another judgment.
- [x] Reproduce the YouTube proxy failure and record an evidence-based [remedy](../../docs/videos/curio-s34/qa-investigation-20261021.md) that preserves the failed checks.

## How to verify

Read the receipt against the private `review/qa.json`, `final.mp4`, `video.json` and `tools/video/package/metadata.mjs`. No QA status or creative file was edited.
