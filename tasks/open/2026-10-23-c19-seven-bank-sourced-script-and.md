---
id: 2026-10-23-c19-seven-bank-sourced-script-and
title: C19 Seven Bank sourced script and paired visual plan
status: in-progress
priority: P2
area: docs
owner: codex-c19-script
claimed_at: 2026-10-23T05:58:37Z
created_at: 2026-10-23T05:58:25Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/story-everyday-seven-bank-c19/script.md
  - docs/videos/story-everyday-seven-bank-c19/script-source-notes.md
  - docs/videos/story-everyday-seven-bank-c19/visual-plan.md
  - docs/videos/story-everyday-seven-bank-c19/visual-plan.json
  - docs/videos/story-everyday-seven-bank-c19/reviews/author-script-receipt-20261023.md
---

# C19 Seven Bank sourced script and paired visual plan

## Why

The owner adopted C19's revised treatment at author PR #1716 head `eb34fb007`; the exact approval receipt was then committed at `f388a6cbc`. Write a single chronological, source-bound story about the retail group's licensed bank and shared ATM network. Give independent reviewers a line-paired visual plan while keeping paid work and publication separate.

## Definition of done

- [x] Six-chapter 79-line narrator script follows the adopted Treatment, with per-line source tags and an answerable opening question.
- [x] 79/79 paired visual text, 67 original concept illustrations and 12 postproduction cards, plus JSON author plan with exact content parity.
- [x] Author receipt records file hashes, paper timing, loop payoffs and specific source limits.
- [x] Independent source/visual and narrator-only review inputs are explicit and frozen; these later reviews remain separate gates for other agents, not an author's self-approval.

## Steps

- [x] Reopen issuer S1–S7; keep 2001, 2002, 2010 and 2024 claims in their own periods.
- [x] Draft an approximately 54-second paper hook and post-intro body plausibly over 480 seconds without treating paper timing as actual TTS.
- [x] Check 79/79 script, source-notes, visual MD and JSON ID/order/narration/source parity; no branded terms in image prompts.
- [ ] Publish draft no-auto-merge PR and hand exact hashes/projection to independent reviewers. No paid generation, import or upload.

## How to verify

Run `npm run check:tasks`, `git diff --check`, and author parity check for IDs, narration/source fields, shot/card count, maximum card streak, banned brand names in prompts and paper character count. Real TTS ≥480 seconds and visual time ≥70% remain later gates.

## Notes

- `script-source-notes.md` names S1–S7 and binds each line to claim IDs. `c190409` adds a narrow S3 p.14 cooperation value; independent reviewer must verify it directly.
- The 2001 announcement's July >1,000 machines is a retrospective achieved point. The 11/11 figure in that 11/09 document was still prospective and was not used.
- The 2010 fee figures are rounded from 85,294 and 9,003 million yen into approximately 853 and 90 hundred-million yen. They cannot be subtracted into per-machine profit.
- The title, script, dates, fees and all visuals remain author-draft text only; no voice, music, image, import or upload was requested.
