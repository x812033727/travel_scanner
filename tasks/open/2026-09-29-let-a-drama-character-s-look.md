---
id: 2026-09-29-let-a-drama-character-s-look
title: Let a drama character's look change between episodes
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-29T00:34:04Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/media/look.mjs
  - tools/video/media/keyframes.mjs
  - tools/video/automation/series.mjs
  - tools/video/tts/requests.mjs
  - docs/videos/SERIES.md
---

# Let a drama character's look change between episodes

## Why

A character of a series has one `appearance` string and one approved character
sheet for the whole work (docs/videos/SERIES.md, 設定圖沿用). Both image prompts
take the string as it is, with no episode in it:

- `sheetPrompt` in tools/video/media/look.mjs: `Character: <name>, <appearance>`
- `shotPrompt` in tools/video/media/keyframes.mjs: `Characters: <name>: <appearance>; …`

The ten forty-episode plans under docs/videos/series-plans have characters who
change on purpose: a conductor's coat and staff badge taken off in episode 27,
a red wrist cord cut in episode 35, a master who sits in a wheelchair from
episode 9, a wedding dress worn for the first three episodes only, patients in
hospital gowns in episode 38, two characters who age decades in one scene.

The fourth audit pass (2026-09-29) found authors answering this inside the
string ("Episodes 1-26: … Episodes 28-37: never the coat"), which the image
model reads whole in every shot and cannot resolve. The plans now keep
`appearance` to what never changes and list what changes in `continuity_notes`
for the writer's shot prompts. That is additive only: a shot prompt can add a
coat, it cannot take the yellow raincoat out of a hospital scene, because the
fixed string still says raincoat. An aged face cannot be added at all.

A character's `voice.style` has the same problem. The worker copies it into
every episode (tools/video/automation/series.mjs) and the narration request
sends it with every line (tools/video/tts/requests.mjs), so a style written for
a master after his stroke ("字含在嘴裡、一次只說三四個字") also reaches the
lines he speaks before it.

## Definition of done

- [ ] An episode can carry a character's look for that episode (a replacement or
  a named variant of the setting book's appearance), and both the sheet prompt
  and the shot prompt use it.
- [ ] A variant has its own approved character sheet, kept in the series store
  beside the base one, so the owner approves a changed look once, not per episode.
- [ ] A variant can also carry its own voice style, used for the lines of the
  episodes it covers.
- [ ] A series without variants behaves exactly as now: same prompts, same
  sheet keys, no approval is lost.
- [ ] The authoring contract of the plans says where a variant is written, and
  the plans' validators accept it.

## Steps

- [ ] Decide the shape: variants on the character in the setting book (id,
  appearance, the episodes it covers) against a per-episode override in the
  chapter outline. The first keeps one place to read and one sheet per variant.
- [ ] `sheetKey` already hashes the appearance, so a variant gets its own key;
  check `reuseSheets` and `keepSheets` in tools/video/media/series-store.mjs.
- [ ] Carry the episode's variant into `series.json` when the worker drafts the
  episode (tools/video/automation/series.mjs), and into `settle()`, which
  replaces an episode's characters with the setting book's word for word.
- [ ] Tests with the drama fixture: two episodes of one series, one variant.

## How to verify

`npm run test:tools`, and with the fixture: the second episode's keyframe prompt
names the variant's appearance and the first episode's does not.

## Notes

- Found while repairing the ten plans on branch `codex/ten-drama-audit-fixes`;
  the plans' side of it is in
  docs/videos/series-plans/binge-five-20260928/AUDIT-REPAIR-20260929.md.
- Until this exists, the scenes it bites hardest are listed in each plan's
  `continuity_notes` under the prop and clothing states; a reviewer of keyframes
  should look at those shots first.
- None of the ten works has started an episode (production snapshot
  2026-09-28), so nothing is drawn wrong yet.
