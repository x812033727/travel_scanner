---
id: 2026-10-26-finish-forty-s-es-pt-id
title: Finish ForTy's es, pt, id and th after the Codex handover
status: done
priority: P2
area: docs
owner: claude-opus-5-5
claimed_at: 2026-10-26T14:05:43Z
created_at: 2026-10-26T14:05:21Z
completed_at: 2026-10-26T14:05:44Z
branch: claude/forty-forest-map-finish
depends_on: []
scope:
  - docs/videos/forty-forest-map/i18n
  - docs/videos/forty-forest-map/finish-20261026.md
  - docs/videos/forty-forest-map/receipts/claude-finish-20261026
  - tasks/open/2026-10-25-ai-tech-forty-forest-map.md
---

# Finish ForTy's es, pt, id and th after the Codex handover

## Why

On 2026-10-26 the owner moved `forty-forest-map` from Codex (ticket
`2026-10-25-ai-tech-forty-forest-map`, PR #1851) to Claude. en, ja, ko and vi were delivered;
es and pt were stale, id and th not made, and Codex had stopped at two TTS requests whose billing
was unknown. Its work directory was on its own machine.

## Definition of done

- [x] es, pt, id and th dubbed against the approved narration's timing, checked by both
      transcribers, wrapped with the final's bookends, with captions and titles/descriptions.
- [x] An eight-language upload package and languages batch, bound to the approved final
      `564812bd…`, approved by the owner.
- [x] The changed translations, the method and the evidence committed next to Codex's work.

## Steps

- [x] Rebuild the zh-TW timeline from the delivered captions; prove it (line starts, total
      frames, speech hash).
- [x] Dub the four languages; shorten lines that do not fit, with an independent review.
- [x] Audio checks one language at a time; reword or re-take what both transcribers miss.
- [x] Captions and bookend-wrapped dubs; package and languages batch; owner approval.
- [x] Handover note `docs/videos/forty-forest-map/finish-20261026.md` and receipts.

## How to verify

`docs/videos/forty-forest-map/receipts/claude-finish-20261026/receipt.json` (hashes, review ids,
check summaries); rerun `rebuild-timeline.mjs` from a checkout of this branch with the final's
captions to get the same timeline.

## Notes

- Owner decision 2026-10-26: transcription requests that come back 502/504 are treated as possibly
  charged and sent again; checks run one language at a time.
- Language thumbnails rendered again (zh-TW byte-identical to Codex's) and sent in a second package `31467486…` and batch `5c2a4b2e…` for approval.
- Tooling idea, not done: `review-files` + a timeline rebuilt from captions could become a proper
  command for finishing a pipeline video whose work directory is gone.
