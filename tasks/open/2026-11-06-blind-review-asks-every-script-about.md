---
id: 2026-11-06-blind-review-asks-every-script-about
title: Blind review asks every script about 沒頭沒尾: no_orphans, with speaker names in dialogue transcripts
status: in-progress
priority: P2
area: tools
owner: claude-opus-5.5-focused-hopper
claimed_at: 2026-11-06T01:13:14Z
created_at: 2026-11-06T01:12:57Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/narrative.mjs
  - tools/video/core/narrative.test.mjs
  - docs/videos/so-thats-why/dialogue-pilot-20261103/SCORECARD.md
---

# Blind review asks every script about 沒頭沒尾: no_orphans, with speaker names in dialogue transcripts

## Why

站主 2026-11-06：「很多系列有遇到沒頭沒尾的對話的問題，記得也要補上這審核」. The blind `narrative` panel
had no question for a person, term or object that arrives unexplained, or a reply that does not meet the
line before it, and a dialogue transcript did not say who spoke, so a reader could not judge the second.

## Definition of done

- [x] `NARRATIVE_PANEL` has a required 14th question `no_orphans`, worded for story, tutorial and daily brief.
- [x] `narrationText` names the speaker on each line when a script has two or more characters.
- [x] `node --test tools/video/core/narrative.test.mjs` passes; the full `tools/video` suite passes.
- [ ] One existing dialogue episode run through `narrative` with the new question as a check that it reads right.

## Notes

- Story series (curio-, story-) get the base wording; PR #2027 rewrites their `chapters_link` toward the same
  continuity rule, and the two questions sit side by side.
- Adding a question changes the panel contract: a host episode whose panel ran before the deploy is asked
  again at its next panel stage (model tokens only).
- Claimed with --force over five stale claims on narrative.mjs (2026-10-14, 10-17, 10-20, 10-29, 11-03), none active for days.
