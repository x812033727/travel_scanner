---
id: 2026-10-22-write-c13-victorinox-source-bound-script
title: Write C13 Victorinox source-bound script and visual plan
status: review
priority: P1
area: docs
owner: codex-c13-script
claimed_at: 2026-10-22T17:23:00Z
created_at: 2026-10-22T17:06:52Z
completed_at:
branch: codex/brand-story-victorinox-c13-treatment
depends_on: []
scope:
  - docs/videos/story-everyday-victorinox-c13/script.md
  - docs/videos/story-everyday-victorinox-c13/script-source-notes.md
  - docs/videos/story-everyday-victorinox-c13/visual-plan.md
  - docs/videos/story-everyday-victorinox-c13/visual-plan.json
  - docs/videos/story-everyday-victorinox-c13/reviews/author-script-receipt.md
---

# Write C13 Victorinox source-bound script and visual plan

## Why

The adopted C13 Treatment has the chronology and source boundaries, but no source-bound narration or executable illustration plan. A script must keep pre-2001 watches/travel gear, the Swiss/U.S. company distinction, and conflicting 2001 sales windows intelligible as one story.

## Definition of done

- [x] Six continuous zh-TW chapters with one sourced spoken sentence per line, a cold open, 5-second intro, and 21-second v4 endscreen/link placement.
- [x] One conceptual cute-mystery shot per line, with planned illustration time above 70% and at most three consecutive cards.
- [x] Preserve source-denominator and product-status limits in a source-note handoff and an author receipt; keep independent source/blind/owner/paid gates pending.
- [x] Independent source and blind-read gates are recorded as separate follow-up work; this author task does not award either PASS.

## Steps

- [x] Bind the already adopted Treatment/matrix hashes and reread primary original/company/reporting materials.
- [x] Draft `script.md`, `script-source-notes.md`, `visual-plan.md`, and `visual-plan.json` in this task's narrow scope.
- [x] Run line/shot/source-tag/hook/visual-duration mechanical checks and record exact limitations.
- [x] Prepare the exact five artifacts and task file for existing draft PR #1693; independent review remains a distinct gate.

## How to verify

Parse `visual-plan.json`; compare its 75 `shots[].line` values with all 75 script IDs; check each narration line has S/M tags, max planned hook gap, planned body seconds, illustration fraction, and consecutive cards. Run `git diff --cached --check` after staging only this task and the five authored artifacts. `npm run check:tasks` exit 1 on two pre-existing untracked duplicate open/done task IDs unrelated to C13 script; leave those files untouched. `npm run test:docs-videos` exit 1 (131 pass, 6 fail) because this worktree has no `node_modules` and existing TTS checks cannot load `pinyin-pro`; no dependency installation was attempted.

## Notes

Owner Treatment SHA-256 `A4A47F06F52490B4044267405445F31AC31EF7FB2C19575D59511D5BE0C57F20`; matrix SHA-256 `295A7793DE618FEF714FA530F78592527EF77E82BAA38EE5594745B8386641D1`. The adopted Treatment, matrix, and owner receipt are not edited. 1989 North American watches and 1999 licensed travel goods precede 2001; July 30 watch announcement precedes September, November operation follows. Swiss AG and U.S. SABI statistics stay separate. Jan 25 direct interview limits ~30% to October while Jan 29 report says near-third for Q4; neither is promoted to resolved global revenue. Four early-2002 product statuses and later CEO employee recollection remain attributed. Later 2005/2014/2017 portfolio dates are not all assigned to 9/11 causation. No paid media, import, upload, merge, or publication.
