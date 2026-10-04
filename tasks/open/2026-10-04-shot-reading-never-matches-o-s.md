---
id: 2026-10-04-shot-reading-never-matches-o-s
title: shot_reading never matches o.s. or v.o. because clauses are split on periods
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-04T15:09:53Z
completed_at:
branch:
depends_on: []
scope:
  - .agents/skills/animation-camera/scripts/shot_reading.mjs
  - tools/animation-camera.test.mjs
---

# shot_reading never matches o.s. or v.o. because clauses are split on periods

## Why

`OFF_SCREEN` in `.agents/skills/animation-camera/scripts/shot_reading.mjs` lists the
screenplay abbreviations `o.s.` and `v.o.` as ways to say a character is not in the picture,
but `shotTraps` first splits `prompt` and `motion` into clauses on `.`, `;` and `,`. A prompt
such as `Close-up of Lin, Zhao (o.s.)` therefore reaches the regex as `Zhao (o`, `s` and `)`,
and neither abbreviation ever matches. The result is silent: no `cast.offscreen` when Zhao is
also listed in `characters`, and a `cast.speaker` trap that tells the author to write
`speaks off screen` although they already said it another way. The two alternatives look
supported in the code and are not.

## Definition of done

- [ ] `o.s.` and `v.o.` (any case, with or without parentheses) are read as off-screen words, or are removed from `OFF_SCREEN` with the skill saying to write `off screen`.
- [ ] A regression case in `tools/animation-camera.test.mjs` pins whichever choice is made.

## Steps

- [ ] Decide between protecting the abbreviations from the clause split (for example, split on a period only when it is followed by whitespace or the end, and not inside `o.s.`/`v.o.`) and dropping them.
- [ ] Check that a name like `Mr. Chen` is not newly glued to the previous clause by the change.
- [ ] Add the regression case and run `node --test tools/animation-camera.test.mjs tools/skills.test.mjs`.

## How to verify

`node --test tools/animation-camera.test.mjs`, plus `shot_reading.mjs --file` on a one-shot JSON
whose prompt is `Close-up of Lin, Zhao (o.s.)`, with `characters` `["lin", "zhao"]` and a line
spoken by `zhao`: it should report `cast.offscreen` for zhao (or, if the abbreviations are
dropped, the skill should say so).

## Notes

- Noticed on 2026-10-04 while fixing `2026-10-04-shot-reading-offscreen-target-false-positive`;
  left alone there because it changes which clauses count as off screen at all, which is a
  separate behaviour change from who in a clause is off screen.
- No repository `video.json` uses `o.s.` or `v.o.` today (a `git grep` over `docs/videos` found
  only `off screen` wordings), so this is latent, not a live false negative.
