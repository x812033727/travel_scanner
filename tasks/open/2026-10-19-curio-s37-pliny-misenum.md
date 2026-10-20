---
id: 2026-10-19-curio-s37-pliny-misenum
title: S37 Pliny at Misenum history episode
status: blocked
priority: P2
area: docs
owner: codex-s37-r4
claimed_at: 2026-10-20T00:36:17Z
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
- [ ] Fresh independent 13 question blind read and final source/visual review of the **R4 exact hash** before any paid media; R3 blind read reached 11/13 with `one_line` and `no_recap` blocked.
- [ ] Owner reviews script and whole episode media budget, then continue approved production gates.

## Steps

- [x] Create research, brief, claims, `video.json`, generated `script.md`, and verification handoff under `docs/videos/curio-s37`.
- [x] Correct R1 independent source and visual findings; remove unsupported exact date and firsthand Pompeii imagery.
- [x] Rebuild the story in chronological intercuts after R1 found a long rewind, repeated leave-behind line, and non-event chapters; correct `pl002` cloud position, `pl037` pillow placement, `pl026` bag, and remove the premature `pl066` held hand.
- [x] Run an independent R2 13 question panel and full pinned-source/visual pass; preserve the 12/13 narrative failure and source/pass notes in `verify-3.md`.
- [x] Revise the R3 first sentence after `[pl033]` to answer the boy's sleep question, remove the stale `[pl053] -> [pl054]` loop, and apply the independent precision notes.
- [x] Run independent R3 script-only 13 question panel and full pinned-source/91-prompt audit; preserve the 11/13 narrative failure and four daylight contradictions in `verify-4.md`.
- [x] Rebuild R4 as the nephew's continuous Misenum route, then reveal the uncle's end as a short reported outcome after the return; correct all four afternoon prompts and source chronology notes.
- [ ] Run a **new R4** script-only 13 question panel and full pinned-source/91-prompt pass against the exact new hashes.
- [ ] Complete audio, stills, music, cut and QA only after gates and budget review.

## How to verify

Run `node tools/video/cli.mjs lint --slug curio-s37 --json`, `npm run test:docs-videos`, and `npm run check:tasks`. The blind reader receives only `node tools/video/cli.mjs narrative --slug curio-s37` output, then submits answers from a fresh session. Source/visual reviewer compares every line and prompt to the fixed GITenberg letters. See `docs/videos/curio-s37/verify-1.md`.

## Notes

Blocked on a fresh independent 13-question blind read and full source/visual pass of the **R4** exact hashes; no paid media until those results and the whole episode budget gate are recorded. `verify-2.md` records failed R1, `verify-3.md` records R2 12/13, and `verify-4.md` records the independent R3 11/13 and R4 handoff. None is R4 approval.

R4 narrows the on-screen timeline to one path: after the uncle's ship leaves, the plot stays with the nephew and mother from the Misenum earthquake through their return. When Tacitus later asks about the uncle, a short letter-bound report resolves the opening ship/body questions. The repeated witness-location assertions at old `[pl042]`, `[pl044]`, `[pl090]` are gone; only `[pl089]` attributes the beach discovery to near-time hearsay. All four afternoon `pl007/pl009/pl015/pl018` prompts now say afternoon; the old cross-bay instant chronology is no longer implied. The uncle's wake-up actor is omitted, sulfur smell explicitly precedes flames, and third-day body timing is tied to the uncle's fall. R4 has 94 aligned lines/claims, 91 still prompts and 21 ordered loops; estimate total 9:30.2 and story body 8:32.3. Lint 0 errors/0 warnings. Keyframes dry-run still quotes US$1.23 for one MiniMax take and US$3.69 at most for three; no generation occurred.

R4 exact SHA-256: script `1827212ba8c33a67df660ab6b8f9b20f86ddada9e4c1aba963cb5cb4deeb2836`; video JSON `3119b930da51bacf85002a8268af301bd66c237ac5659d8fabbbf6a59d752e16`; claims `80436b3cebc71c08eff7b1717302ae73caf2e5534fbabe5de35fc83ce91e88bb`. The pinned English translation remains `9f5fd6bc997d9386987a0d5ae184961f2c0f88f9a8912baa0cd7848687da4995` at GITenberg commit `959ded9fab0f9d54768d2dbfad860b79c864c4c8`. No TTS or paid imagery/music ordered.

R3 corrects the only remaining R2 narrative blocker: the new chapter's first line `[pl047]` now directly answers `[pl033]` before asking about the stronger quake, which `[pl048]` resolves. The loop table now has 21 valid entries; the stale `[pl053] -> [pl054]` entry is gone. The R2 source/prompt auditor found no historical blocker among 94 lines or 91 images, only five line-precision and three illustration-precision notes; R3 addresses all eight without changing the story outcome. `lint` is 0 errors/0 warnings; estimated story body is 513.7 seconds (8:33.7). R3 script SHA-256 `91697aaab93400a16b226308a3b45aee35e14bacadec53ca20f3711a5d956cc5`; video JSON SHA-256 `fd2e427bee1caff84dfe005cf4485bcedbbb38352db11244a30b7de1f2d4730c`; claims SHA-256 `21541e383cdbdc6249aac6b4c78c17701ddc4920342c8851820529a3eba0e68f`. No paid media has been ordered for this version.

R2 reorganized the 94 lines in two-bank night and morning order, with 91 still prompts and 22 declared open loops; it no longer finishes the uncle's death and then rewinds to the nephew's departure. `pl047`, `pl046`, `pl020`, and `pl092` add only details present in the pinned LXV/LXVI letters (earlier tremors, his own doubt about reading Livy, the cloud's changing colour, and his own fear). The current `keyframes --dry-run --takes 3` quote is 91 stills, US$1.23 for one pass, US$3.69 at three takes; **no image generation or other paid media was run**. Music quote is unavailable before TTS timeline creation. Lint is 0 errors/0 warnings; local docs-video tests passed 236/236 and task check exited 0 with pre-existing and temporarily overlapping S37-review task warnings. Estimated body excluding opener/outro is over eight minutes, subject to real TTS measurement.

R2 SHA-256: `script.md` `06b5ed9b368b0d9fed3f22bd1fbb88897fb6e1f44b87a092fd1002bb6b91b71c`; `video.json` `c8e03ce56afa489a4669dd47573f9ce79556cdad46bbb38dc46431ba9c12bd19`; `claims.md` `4ceafd1a13008d46d6bba3624b1943e83540a83208c2d10559cf3d49cf072286`. The 94 claim rows exactly match the 94 spoken lines and line IDs in JSON, in playback order. Pinned English translation text remains `9f5fd6bc997d9386987a0d5ae184961f2c0f88f9a8912baa0cd7848687da4995` from commit `959ded9fab0f9d54768d2dbfad860b79c864c4c8`.

The 2026-10-20 preproduction JSON SHA-256 is `0a39ca65fd132a03b836597bdbd624f125ae79f2948812ab088323a75a8ce1bd`. Source text SHA-256 is `9f5fd6bc997d9386987a0d5ae184961f2c0f88f9a8912baa0cd7848687da4995`; commit `959ded9fab0f9d54768d2dbfad860b79c864c4c8`. The source is a Melmoth/Bosanquet English translation, not collated Latin. It prints 24 August but manuscript date variants are unresolved for this production, so the spoken script gives no exact date. Elder Pliny's Stabiae final moments are reports, not the nephew's eyewitness experience; cause of death is explicitly his conjecture. No paid media has been ordered.
