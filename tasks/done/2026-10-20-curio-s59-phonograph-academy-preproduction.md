---
id: 2026-10-20-curio-s59-phonograph-academy-preproduction
title: Curio S59 phonograph Academy preproduction
status: done
priority: P2
area: docs
owner: codex-s59-author
claimed_at: 2026-10-20T23:20:59Z
created_at: 2026-10-20T23:20:56Z
completed_at: 2026-10-20T23:39:54Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s59
---

# Curio S59 phonograph Academy preproduction

## Why

Produce one distinct 奇聞檔案局 history episode with a checkable answer to the 1878 Paris Academy phonograph ventriloquist doubt. A short anecdote alone cannot support an eight-minute story; the mechanical cause, the failed operator change, and the requested retest must stay tied to contemporary evidence.

## Definition of done

- [x] A 30–60s condensed opening and six causal chapters with body ≥8 minutes even at 325 Han/min.
- [x] Two fixed, independently retrievable source texts, separated by evidence tier, and a line-linked citation for each historical sentence.
- [x] 70%+ original illustration shots, limited schematic cards, intro/outro/Short/link plan, and zero lint warnings.
- [x] Author checks and five-file hash receipt prepared for independent source and two blind-reader reviews; no media spend or author PASS.

## Steps

- [x] Verify du Moncel 1878 original and Edison 1910 direct retrospective with fixed commits and local SHA-256.
- [x] Draft recommended A/B brief, research boundaries, scene script, claims table, video JSON and per-scene citation audit.
- [x] Run lint, chapter timing, docs tests, task validation; freeze five deliverables for independent review.

## How to verify

`node tools/video/cli.mjs lint --slug curio-s59` (0 errors and warnings), `npm run test:docs-videos`, `npm run check:tasks`. The author also checked all 110 scene rows against the local D/E files and saved line-range results in `docs/videos/curio-s59/review/r1-source-citation-audit.md`; the temporary check script is not a repo deliverable. No tool calls for paid TTS, image or music generation were made.

## Notes

1878 du Moncel is a direct Academy participant but the ventriloquist quotes come from an unnamed attendee's letter that he reproduces. Edison in a 1910 biography recounts the machine origin, not the Paris audience; the 1892 English du Moncel translation is reading help, not another witness. Earlier P08 line range was wrong for pitch; corrected to D6955–6976 before freeze. The specified office test conditions are not itemized, and du Moncel's first failure is attributed by him to his mouth being too far from the recording opening. Review outcome remains pending independent workers.
