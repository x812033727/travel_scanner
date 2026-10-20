---
id: 2026-10-19-curio-s37-pliny-misenum
title: S37 Pliny at Misenum history episode
status: blocked
priority: P2
area: docs
owner: codex-s37-r2
claimed_at: 2026-10-20T00:10:22Z
created_at: 2026-10-19T23:53:49Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-s37
---

# S37 Pliny at Misenum history episode

## Why

The next Curio history episode asks whether Pliny the Younger witnessed the Vesuvian disaster from Pompeii. The pinned letters show a different position and distinguish his escape from his report of his uncle's last hours.

## Definition of done

- [x] Reopen and hash pinned LXV/LXVI, record claims and source limitations.
- [x] Draft options, chosen brief, 8+ minute screenplay, 75–120 still shots and loop map.
- [x] Pass video lint and relevant documentation checks.
- [ ] Fresh independent 13 question blind read and final source/visual review of the **R2 exact hash** before any paid media; R1 independently found four required narrative failures and a source/prompt mismatch.
- [ ] Owner reviews script and whole episode media budget, then continue approved production gates.

## Steps

- [x] Create research, brief, claims, `video.json`, generated `script.md`, and verification handoff under `docs/videos/curio-s37`.
- [x] Correct R1 independent source and visual findings; remove unsupported exact date and firsthand Pompeii imagery.
- [x] Rebuild the story in chronological intercuts after R1 found a long rewind, repeated leave-behind line, and non-event chapters; correct `pl002` cloud position, `pl037` pillow placement, `pl026` bag, and remove the premature `pl066` held hand.
- [ ] Run a **new R2** independent 13 question narrative panel and full pinned-source/visual pass; preserve the R1 failure in `verify-2.md`.
- [ ] Complete audio, stills, music, cut and QA only after gates and budget review.

## How to verify

Run `node tools/video/cli.mjs lint --slug curio-s37 --json`, `npm run test:docs-videos`, and `npm run check:tasks`. The blind reader receives only `node tools/video/cli.mjs narrative --slug curio-s37` output, then submits answers from a fresh session. Source/visual reviewer compares every line and prompt to the fixed GITenberg letters. See `docs/videos/curio-s37/verify-1.md`.

## Notes

Blocked on a fresh independent 13-question blind read and full source/visual pass of the **R2** exact hashes; no paid media until those results and the whole episode budget gate are recorded. The prior `verify-2.md` is a transparent failed R1 review, not R2 approval.

R2 reorganized the 94 lines in two-bank night and morning order, with 91 still prompts and 22 declared open loops; it no longer finishes the uncle's death and then rewinds to the nephew's departure. `pl047`, `pl046`, `pl020`, and `pl092` add only details present in the pinned LXV/LXVI letters (earlier tremors, his own doubt about reading Livy, the cloud's changing colour, and his own fear). The current `keyframes --dry-run --takes 3` quote is 91 stills, US$1.23 for one pass, US$3.69 at three takes; **no image generation or other paid media was run**. Music quote is unavailable before TTS timeline creation. Lint is 0 errors/0 warnings; local docs-video tests passed 236/236 and task check exited 0 with pre-existing and temporarily overlapping S37-review task warnings. Estimated body excluding opener/outro is over eight minutes, subject to real TTS measurement.

R2 SHA-256: `script.md` `06b5ed9b368b0d9fed3f22bd1fbb88897fb6e1f44b87a092fd1002bb6b91b71c`; `video.json` `c8e03ce56afa489a4669dd47573f9ce79556cdad46bbb38dc46431ba9c12bd19`; `claims.md` `4ceafd1a13008d46d6bba3624b1943e83540a83208c2d10559cf3d49cf072286`. The 94 claim rows exactly match the 94 spoken lines and line IDs in JSON, in playback order. Pinned English translation text remains `9f5fd6bc997d9386987a0d5ae184961f2c0f88f9a8912baa0cd7848687da4995` from commit `959ded9fab0f9d54768d2dbfad860b79c864c4c8`.

The 2026-10-20 preproduction JSON SHA-256 is `0a39ca65fd132a03b836597bdbd624f125ae79f2948812ab088323a75a8ce1bd`. Source text SHA-256 is `9f5fd6bc997d9386987a0d5ae184961f2c0f88f9a8912baa0cd7848687da4995`; commit `959ded9fab0f9d54768d2dbfad860b79c864c4c8`. The source is a Melmoth/Bosanquet English translation, not collated Latin. It prints 24 August but manuscript date variants are unresolved for this production, so the spoken script gives no exact date. Elder Pliny's Stabiae final moments are reports, not the nephew's eyewitness experience; cause of death is explicitly his conjecture. No paid media has been ordered.
