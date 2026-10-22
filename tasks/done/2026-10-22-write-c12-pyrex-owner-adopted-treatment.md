---
id: 2026-10-22-write-c12-pyrex-owner-adopted-treatment
title: Write C12 Pyrex owner-adopted Treatment script and visual plan
status: done
priority: P2
area: docs
owner: codex-c12-script-author
claimed_at: 2026-10-22T14:39:03Z
created_at: 2026-10-22T14:38:54Z
completed_at: 2026-10-22T14:45:13Z
branch: codex/brand-story-pyrex-c12-script
depends_on: []
scope:
  - docs/videos/story-everyday-pyrex-c12-script
---

# Write C12 Pyrex owner-adopted Treatment script and visual plan

## Why

The owner adopted the SHA-bound C12 Pyrex Treatment on 2026-10-22. It needs an independently authored narration and visual plan before a different agent can review every line and before the owner considers the script gate. This ticket owns only the new C12 script folder; the Treatment and its independent source review stay as approved inputs.

## Definition of done

- [x] Six chronological chapters tell one story from Nonex railway lanterns to Bessie's battery-jar trial, the 1915 consumer launch, the home-economist demonstrations, and today's separate product/material scopes.
- [x] Every narration ID has a source note and one corresponding visual ID; the illustration/card design has a conservative ≥70% illustration-time target and no more than three consecutive cards.
- [x] Draft package is committed and sent to a draft stacked PR without media generation, merge, owner script approval, or publication.

## Steps

- [x] Recheck adopted Treatment/matrix hashes and directly read the publisher sources.
- [x] Draft script and source notes; keep historical anecdotes attributed and material scopes separate.
- [x] Draft one-to-one scene prompts/cards, intro/outro placements, and media stop rules.
- [x] Run focused structure, prompt, task and whitespace checks.

## How to verify

Use a read-only row check on script.md and visual-plan.md: 80 IDs in each, identical order; 67 illustrations, 13 cards, longest card run two. Inspect illustration prompts for brand/person names or generated text. Run `npm run check:tasks` and `git diff --check`. Treatment/matrix hashes must match the owner-adopted bytes recorded in script.md. Script still requires independent per-line review, two blind reads, owner script approval and actual TTS ≥480 seconds before images.

## Notes

The source set is principally later Corning Museum narratives S1/S2/S3/S6, current Corning lab FAQ S5, and European brand claims S4/S7. S4 alone supplies the cold-rain detail; S1 says cold air. The trial used two sawed-off Nonex battery-jar bottoms, not a railway globe. The single current French product page cannot generalize to all Pyrex, and Corning laboratory limits do not govern consumer bakeware. No precise U.S. formula-change year or material safety advice appears in the draft.

The approximately 2,750-character narration is a writing estimate, not proof of 480 seconds. Gate order: independent script audit, two blind reads, owner script decision, separately authorized paid TTS and real duration receipt, then a priced illustration batch only if duration passes. No prior C03–C06 US$25 approval carries over.
