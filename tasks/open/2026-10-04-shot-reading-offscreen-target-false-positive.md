---
id: 2026-10-04-shot-reading-offscreen-target-false-positive
title: Avoid offscreen target co-mention false positives in shot reading
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5-shot-reading-offscreen
claimed_at: 2026-10-04T14:54:10Z
created_at: 2026-10-04T04:03:32Z
completed_at:
branch: claude/shot-reading-offscreen-target
depends_on: []
scope:
  - .agents/skills/animation-camera/scripts/shot_reading.mjs
  - tools/animation-camera.test.mjs
  - .agents/skills/animation-camera/SKILL.md
  - .claude/skills/animation-camera/SKILL.md
---

# Avoid offscreen target co-mention false positives in shot reading

## Why

The shot-reading offscreen heuristic treats every named character in a clause
containing `off screen` as the offscreen subject. For a correctly visible actor
whose action targets an offscreen opponent, this can tell the author to delete
the visible actor from `characters`, breaking the keyframe binding.

An independent forward-use review reproduced this with a medium close-up:
`One cyan arc leaves Yan's sword toward Wei off screen right.` Yan is visible and
must remain in `characters`; Wei is the offscreen target. Splitting the sentence
into a visible-actor clause and an explicit offscreen-target clause avoids the
current false positive, but the original sentence is semantically valid.

## Definition of done

- [x] A visible actor aiming at a named offscreen target does not receive `cast.offscreen` or advice to remove the visible actor.
- [x] Truly offscreen characters still receive the existing useful cast-binding diagnostic.
- [x] Regression coverage includes the co-mention example, an explicit offscreen subject and an ambiguous clause.

## Steps

- [x] Inspect the name/offscreen co-mention heuristic and distinguish actor from target where the wording supports it.
- [x] Keep ambiguous clauses reviewable; do not solve this by disabling offscreen checks.
- [x] Add regression cases and update any diagnostic guidance that could remove a correctly visible character.

## How to verify

Run `node --test tools/animation-camera.test.mjs` under Node 24.19. Run
`shot_reading.mjs --strict` on a temporary three-shot pilot using the example
above and confirm that the visible actor remains bound. Also exercise a true
offscreen speaker to show the guard still works.

## Notes

- Found on 2026-10-04 in the independent Budaimiao-style skill trial; the relevant heuristic is in `shot_reading.mjs` around lines 218-226.
- The current documentation warns against deleting a visible actor merely to clear this heuristic. Runtime behavior is unchanged by the skill-only task.
- No paid media, browser operations or runtime fix were performed for this discovery.
- 2026-10-04 fix (claude-opus-5-5-shot-reading-offscreen): `offScreenRoles` in `shot_reading.mjs` now reads
  whom each off-screen clause's words attach to, instead of treating every name in the clause as off screen.
  Three readings are definite: one name alone (`Wei speaks off screen`, `Wei off screen left at his eyeline`,
  `held by Wei off screen`, and the speaker fallback for `a voice from off screen`), which keeps the old
  message and fix; a name governed by toward/towards/at/to/on/onto/upon/into right before the off-screen words
  (`toward Wei off screen right`, `eyes on Chen off screen right`, `toward Old Wei off screen`), where that
  name is off screen and the other names in the clause are visible actors; and look/glance/stare/gaze/peer/
  point/aim/eyes right before them (`Yan looks off screen right`), where the words are a direction and a
  name after `at`/`toward` is the off-screen one. In `--file` mode the target need not be in the cast: an
  unlisted capitalised name (or him/her/them) after the preposition still counts as the target.
- What it cannot read stays a `cast.offscreen` trap (so `--strict` still stops) with a softer message,
  "讀不出是誰", and a fix that starts with "先確認" and says to keep a visible character: two or more names
  without one of the forms above (`Yan raises the sword as Wei shouts off screen`), a speech verb before the
  preposition (`Yan speaks to Wei off screen`, either could be the off-screen one), and an object that is a
  noun phrase (`swings toward the gate off screen`, target or location). A gaze verb before such a noun phrase
  (`looks toward the gate off screen`) is a direction and reports nothing.
- Deliberate trade-off: a clause the old code read definitely but that names two people (`Lin lifts the cup
  as Zhao speaks off screen` with both listed) now gets the softer message for both. Splitting it at a comma
  (`Lin lifts the cup, Zhao speaks off screen`) restores the definite one; the SKILL.md line says so.
- Limitation left: in `--file` mode only the listed characters are known, so a single listed name next to an
  unlisted one without a preposition (`Yan raises the sword as Wei shouts off screen` with only Yan listed)
  is still read as one name and reported definitely. A full `video.json` knows the whole cast and reports it
  as unsure.
- The coordinator's brief said the script also lives under `.claude/skills/animation-camera/scripts/`; it
  does not: only `SKILL.md` is mirrored (`tools/skills.test.mjs`), scripts and references live once under
  `.agents/`. Both SKILL.md copies were updated (line on aiming at someone off screen) and added to the scope.
- Measured: before the change a probe of the ticket's sentence with characters `[yan]` reported
  `cast.offscreen` for yan; after it, nothing, and with `[yan, wei]` only wei. `budaimiao-example.json` still
  reads eight shots, zero traps. A temporary three-shot pilot (s1 the ticket's sentence with Yan listed, s2
  `Yan off screen left at his eyeline` with Wei listed, s3 `Wei speaks off screen` with Yan and Wei listed)
  gave exactly one trap, `cast.offscreen` for wei on s3, exit 1 under `--strict`; with Wei removed from s3 it
  gave no traps, exit 0. Tests ran under Node 24.13.0 (this machine), not 24.19.
- Filed `2026-10-04-shot-reading-never-matches-o-s`: the `o.s.`/`v.o.` alternatives in `OFF_SCREEN` can never
  match because clauses are split on periods first.
