---
id: 2026-09-29-let-a-drama-character-s-look
title: Let a drama character's look change between episodes
status: done
priority: P2
area: tools
owner: claude-opus-5-5-drama-look
claimed_at: 2026-10-01T03:37:46Z
created_at: 2026-09-29T00:34:04Z
completed_at: 2026-10-01T03:53:13Z
branch: claude/drama-character-look-change
depends_on: []
scope:
  - tools/video/media/look.mjs
  - tools/video/media/keyframes.mjs
  - tools/video/automation/series.mjs
  - tools/video/tts/requests.mjs
  - docs/videos/SERIES.md
  - tools/video/automation/flow.mjs
  - tools/video/automation/series.test.mjs
  - .agents/skills/youtube-video/references/series.md
  - docs/videos/series-plans/binge-five-20260928/AUTHORING.md
  - docs/videos/series-plans/binge-five-20260928/validate.mjs
  - docs/videos/series-plans/binge-five-20260928/validate.test.mjs
  - docs/videos/series-plans/claude-binge-five-20260928/AUTHORING.md
  - docs/videos/series-plans/claude-binge-five-20260928/validate.mjs
  - docs/videos/series-plans/claude-binge-five-20260928/validate.test.mjs
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

- [x] An episode can carry a character's look for that episode (a replacement or
  a named variant of the setting book's appearance), and both the sheet prompt
  and the shot prompt use it.
- [x] A variant has its own approved character sheet, kept in the series store
  beside the base one, so the owner approves a changed look once, not per episode.
- [x] A variant can also carry its own voice style, used for the lines of the
  episodes it covers.
- [x] A series without variants behaves exactly as now: same prompts, same
  sheet keys, no approval is lost.
- [x] The authoring contract of the plans says where a variant is written, and
  the plans' validators accept it.

## Steps

- [x] Decide the shape: variants on the character in the setting book (id,
  appearance, the episodes it covers) against a per-episode override in the
  chapter outline. The first keeps one place to read and one sheet per variant.
- [x] `sheetKey` already hashes the appearance, so a variant gets its own key;
  check `reuseSheets` and `keepSheets` in tools/video/media/series-store.mjs.
- [x] Carry the episode's variant into `series.json` when the worker drafts the
  episode (tools/video/automation/series.mjs), and into `settle()`, which
  replaces an episode's characters with the setting book's word for word.
- [x] Tests with the drama fixture: two episodes of one series, one variant.

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

### Done (2026-10-01, claude-opus-5-5-drama-look)

- Shape: `looks: [{ id, from, to?, appearance, sheet_prompt?, voice_style? }]` on the
  character in the setting book (or a one-off's bible), not a per-episode override in the
  chapter outline: one place to read, one sheet per look. `from`/`to` are inclusive episode
  numbers, no `to` runs to the series' end, one look per episode per character. A look's
  appearance is the whole look (a replacement), because the image model reads the string whole
  in every shot; an add-on could not take a coat off. A change inside one episode (aging in one
  scene) is a second character id, written so in the authoring contracts.
- One switch point: `castFrom(setting, episode)` in tools/video/automation/series.mjs swaps in
  the look covering the episode, and `draftEpisode` in flow.mjs (added to scope) passes the
  episode number. series.json's cast is then the episode's, and everything downstream already
  reads that cast: `settle()`, lint's verbatim check, the writer's `cast`, the brief,
  `sheetPrompt` (look.mjs), `shotPrompt` (keyframes.mjs), `voiceFor`/`planRequests`
  (requests.mjs). So look.mjs, keyframes.mjs, requests.mjs and series-store.mjs needed no
  change; video.json's character keys are unchanged (no `looks`, no new key).
- Sheets: `sheetKey` hashes the appearance, so a look has its own key and is stored as
  `_series/<series>/characters/<id>/<key>.png` beside the base sheet. The first episode that
  wears it draws it and the owner approves it once; later episodes it covers reuse it, and the
  episode after it reuses the base sheet again (tested).
- No looks, no change: `castFrom(book, n)` equals the old `castFrom(book)` for every n, so
  prompts, sheet keys, narration request keys and existing approvals are untouched (tested).
- Shape check: `looksProblem` (exported) is called from `documentProblem` for setting books and
  bibles; the plans' validators call `documentProblem`, so they accept a valid look and refuse a
  malformed one, and they now also apply their appearance word rules (length, ASCII for the
  claude batch, no timed words) to each look's appearance. `lookFor` reads looks defensively
  (skips a look without an appearance or integer `from`), since the site does not check them.
- The API's `doc_problem` does not check looks yet; stopped at the tool side and filed
  `2026-10-01-api-checks-the-looks-of-a`. The setting planner's prompt does not mention looks
  and the ten plans still keep their states in `continuity_notes`; filed
  `2026-10-01-setting-planner-writes-character-looks-and`.
- Verified: `node --test tools/video/automation/series.test.mjs` (40 pass; the three new tests
  fail without the change, the draft test checked by reverting the flow.mjs line),
  `npm run test:tools` (only the known Windows failure in tools/video/tts/check.test.mjs),
  both plan batches' `node validate.mjs` and `node --test validate.test.mjs` clean.
