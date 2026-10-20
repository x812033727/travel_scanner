---
id: 2026-10-19-curio-s37-pliny-misenum
title: S37 Pliny at Misenum history episode
status: blocked
priority: P2
area: docs
owner: codex-s37
claimed_at: 2026-10-19T23:53:53Z
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
- [ ] Fresh independent 13 question blind read and final source/visual review of the exact script hash before any paid media.
- [ ] Owner reviews script and whole episode media budget, then continue approved production gates.

## Steps

- [x] Create research, brief, claims, `video.json`, generated `script.md`, and verification handoff under `docs/videos/curio-s37`.
- [x] Correct independent source and visual findings; remove unsupported exact date and firsthand Pompeii imagery.
- [ ] Run formal independent narrative panel and final source/visual review; update `verify-1.md` or add a new verify note.
- [ ] Complete audio, stills, music, cut and QA only after gates and budget review.

## How to verify

Run `node tools/video/cli.mjs lint --slug curio-s37 --json`, `npm run test:docs-videos`, and `npm run check:tasks`. The blind reader receives only `node tools/video/cli.mjs narrative --slug curio-s37` output, then submits answers from a fresh session. Source/visual reviewer compares every line and prompt to the fixed GITenberg letters. See `docs/videos/curio-s37/verify-1.md`.

## Notes

Blocked on a fresh independent 13-question blind read and final source/visual pass of the exact JSON hash; no paid media until those results and the owner budget review are recorded.

The 2026-10-20 preproduction JSON SHA-256 is `0a39ca65fd132a03b836597bdbd624f125ae79f2948812ab088323a75a8ce1bd`. Source text SHA-256 is `9f5fd6bc997d9386987a0d5ae184961f2c0f88f9a8912baa0cd7848687da4995`; commit `959ded9fab0f9d54768d2dbfad860b79c864c4c8`. The source is a Melmoth/Bosanquet English translation, not collated Latin. It prints 24 August but manuscript date variants are unresolved for this production, so the spoken script gives no exact date. Elder Pliny's Stabiae final moments are reports, not the nephew's eyewitness experience; cause of death is explicitly his conjecture. No paid media has been ordered.
