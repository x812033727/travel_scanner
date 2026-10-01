---
id: 2026-10-01-setting-planner-writes-character-looks-and
title: Setting planner writes character looks and the ten plans use them
status: done
priority: P3
area: tools
owner: claude-opus-5-5-setting-looks
claimed_at: 2026-10-01T14:09:17Z
created_at: 2026-10-01T03:45:59Z
completed_at: 2026-10-01T14:29:30Z
branch: claude/setting-planner-looks
depends_on: []
scope:
  - tools/video/automation/prompts.mjs
  - tools/video/automation/prompts.test.mjs
  - .agents/skills/youtube-video/references/prompts/series-setting.md
  - docs/videos/series-plans/binge-five-20260928
  - docs/videos/series-plans/claude-binge-five-20260928
---

# Setting planner writes character looks and the ten plans use them

## Why

Since task `2026-09-29-let-a-drama-character-s-look`, a character in a setting book may carry
`looks: [{ id, from, to?, appearance, sheet_prompt?, voice_style? }]`, and an episode a look
covers is drawn and voiced with it (docs/videos/SERIES.md, 換裝與變化). Two places do not use it
yet:

- The setting-book planner is never told about `looks` (the character shape in
  `SERIES_INSTRUCTIONS["planner:setting"]` in tools/video/automation/prompts.mjs, and
  .agents/skills/youtube-video/references/prompts/series-setting.md), so a series the planner
  writes keeps every change in the shot prompts, which can add a coat but cannot take one off.
- The ten forty-episode plans under docs/videos/series-plans keep their clothing and prop states
  in `continuity_notes` (the fourth audit pass, 2026-09-29): a conductor's coat and badge off in
  episode 27, a red wrist cord cut in episode 35, a master in a wheelchair from episode 9, a
  wedding dress for episodes 1-3 only, hospital gowns in episode 38, and voice styles written
  for one stretch of the story (reviews/city-owes-a-light.json lists four). Their AUTHORING.md
  now says those belong in `looks`, and their validators accept them.

## Definition of done

- [x] The setting planner's instructions describe `looks` (when to write one, that its
  appearance is the whole look, one look per episode, a change inside one episode is a second
  character id) and its reference file says the same.
- [x] The changes each plan lists in `continuity_notes` that a shot prompt cannot add are
  moved into the characters' `looks`, with the generated files rebuilt (`node build.mjs`) and
  `node validate.mjs` clean for every work.
- [x] Voice styles written for part of a story move into a look's `voice_style`.

## Steps

- [x] Prompt text and its test in tools/video/automation/prompts.test.mjs.
- [x] One plan at a time; the authors' AUTHORING.md says where a look is written.

## How to verify

`node --test tools/video/automation/prompts.test.mjs`; in each plan directory
`node validate.mjs` and `node --test validate.test.mjs`.

## Notes

- The plans' content is the owner's approved story; moving a state into a look changes how it is
  drawn, not what happens. None of the ten works has started an episode (2026-09-28 snapshot).
- Claimed with `--force`: the overlap was with the stale claims `2026-09-28-drama-plan-continuity-handoff`
  and `2026-09-28-ten-drama-plan-audit-findings` (codex-ten-drama, PR #978 merged) and
  `2026-09-28-sothatswhy-shorts-from-episode` (PRs #904/#950/#962 merged).
- Prompt: `SERIES_INSTRUCTIONS["planner:setting"]` now lists `looks` in the character shape and
  says when to write one (a change lasting a run of episodes that a shot prompt cannot take off,
  or a changed voice), that its appearance is the whole look, one look per episode, and that a
  change inside one episode is a second character id. The reference file has the same as a
  "Looks" section. There is no copy of the reference under `.claude/skills/youtube-video/` (only
  SKILL.md is mirrored), so nothing else had to follow. The new test fails without the change.
- Rule used for the plans, from the Definition of done: a look where the base appearance would
  be wrong for whole episodes (something it draws has to go or be replaced) or the voice changes
  for a run of episodes, and only where the plan states the episodes and what to draw. Additions
  a shot prompt can make (crown, badges, lantern, backpack, bandages, the ghost's glow) stayed in
  `continuity_notes`. A look covers whole episodes; at a mid-episode boundary the episode uses
  whichever side the notes describe for most of it and the notes say so.
- Looks written (13): wedding-reckoning zhitang `wedding-gown` 1–3; seventh-passenger he-zhao
  `conductor-coat` 1–26 (with the unsteady voice; the base voice is now the steady one) and
  `patient` 38, and `patient` 38 for cheng-wang, lin-xiaoman, qiao-ning; before-the-hammer
  yanshan `wheelchair` 9–40 (limp right hand, post-stroke slurred voice from note 3);
  ghost-at-his-side luzheng `aged-61` 24–30 (with 「老去之後聲音變沙、變短」 moved out of the base
  style); reload-first-day xiaoshu `no-bag` 36, suxing `own-voice` 36– and duchengye `heard` 32–
  (the two voice changes note 聲音 was waiting for); taste-of-the-throne yuanji `bound-shoulder`
  40; three-needles huoqingshan `hospital-bed` 32–39. The notes that described each now point to
  the look. scapegoat-empress, city-owes-a-light and remembered-by-rival got none: their states are
  additions, or ambiguous (below). Qi Yan's red cord is never in his base appearance (hidden under
  the cuff), so cutting it takes nothing off; the wrist after the cut is left open (bandage or
  healed mark), so it stays a note.
- Both build.mjs files now show each look as a row under the character in setting.md.
- Verified: a scratch script (not committed) confirmed `castFrom` gives each
  look's appearance and voice style in every cast episode it covers; every look appearance is
  ASCII and under 800 characters (the validators check both).
- Left for the owner, filed as `2026-10-01-owner-settles-the-looks-the-ten`: changes inside one
  episode (wedding ep 1 cold open, He Zhao ep 27, Lu Zheng ep 30 and 16, Zong Dan ep 37, the
  reload panels, the first lines of Su Xing's and Du Chengye's new voices, Wei Cheng ep 32);
  ranges the notes do not give (周禾、徐浩「後段」, 沈知夏「敢說真話後」, 沈崇岳「敗局」, 老尤
  「後半段」); outfits nobody wrote (Lin Jiming ep 38–40, Zhiyuan in custody, the dowager, regent
  and Liu Gugu in prison).
- Not touched on purpose: the independent review receipts. wedding-reckoning and
  seventh-passenger now fail `node validate.mjs --require-reviews` with "review: stale source
  hash" (not a CI check; plain `node validate.mjs` is clean). Rewriting a receipt's hash would
  claim a review that did not happen. The shared `validation-report.json` and
  `local-revision-manifest.json` are refreshed by the lead reviewer (reviews/scapegoat-empress.json),
  so they were left as they were.
