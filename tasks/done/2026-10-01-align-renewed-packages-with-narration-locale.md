---
id: 2026-10-01-align-renewed-packages-with-narration-locale
title: Align renewed packages with narration locale selection
status: done
priority: P1
area: tools
owner: codex-renewal-narration-compat
claimed_at: 2026-10-01T10:18:07Z
created_at: 2026-10-01T10:17:38Z
completed_at: 2026-10-01T10:38:58Z
branch: codex/branding-cc-prompt-20261001
depends_on:
  - 2026-10-01-long-video-renewal-tools-and-ui
scope:
  - tools/video/review/renewal.mjs
  - tools/video/review/renewal.test.mjs
---

# Align renewed packages with narration locale selection

## Why

Main #1066 adds narration-aware automatic metadata/caption locales: an English video
always carries English and zh-TW while selected foreign languages remain optional.
The renewed-package guard composed metadata from selected locales only, so it rejected
valid English packages after rebase and did not validate their automatic zh-TW caption.
It also treated a selected original-language dub as a required duplicate audio track.

## Definition of done

- [x] The renewal guard uses the same metadata/caption/dub selection helpers as package.
- [x] English narration with only Japanese captions, no optional languages, or selected
      own-language metadata passes when automatic source-bound files are complete.
- [x] Missing or stale automatic captions, missing publish attachments, missing zh-TW
      metadata and a duplicate original-language dub are refused before submission.
- [x] An original-language dub choice remains in the choice pin and receives an explicit
      skip in the language proof, without generating or attaching a second audio track.
- [x] Focused/full tools and real emitted-byte consumer checks pass after the rebase.

## Steps

- [x] Claim only renewal.mjs and its tests after root completed the rebase onto b03e938e.
- [x] Add a reusable English-narration fixture with actual package files and source hashes.
- [x] Coordinate the separately claimed consumer narration fix and final fixture probe.

## How to verify

Run node --test tools/video/review/renewal.test.mjs tools/video/review/sync.test.mjs
tools/video/import/import.test.mjs, then npm run test:tools and task checks with the
documented bundled Node runtime. Pass real emitted English metadata/manifests/captions
to the API language_package consumer; do not mock its selection contract.

## Notes

- Root authorized this narrow compatibility task after rebase; no live operations or
  API edits are in scope. Consumer changes are separately owned and claimed.
- Focused tests: 93 passed. Existing nonrenewed output remains unchanged.
- Complete tools: 1046 passed, 2 existing skips, no failures. Actual English emitted
  files passed 5 positive cases (ja CC-only, none, own metadata/dub, all four, zh-CN),
  while 42 altered consumer proofs and 4 invalid producer cases were refused. The
  Traditional Chinese contract repeated its 85 scenarios with zero unexpected results.
- Independent producer/consumer review found no remaining major issue. The external
  `rollout/renewal-narration-validation.json` records exact hashes and report paths.
- Canonical adoption and imported/compilation handoff stay in the predecessor's open
  dependent task; this fix does not generate missing translations or paid narration.
