---
id: 2026-10-05-slideshow-risk-craft-rows
title: Slideshow risk as craft rows: repeated setups, decorative shots, aimless motion, missing intent, text-first share, cinematic claims
status: done
priority: P2
area: tools
owner: claude-fable-5-1-craft
claimed_at: 2026-10-05T16:20:39Z
created_at: 2026-10-05T16:08:24Z
completed_at: 2026-10-05T16:41:23Z
branch: claude/slideshow-risk-craft-rows
depends_on: []
scope:
  - tools/video/core/craft.mjs
  - .agents/skills/youtube-video/scripts/drama_craft_check.mjs
  - tools/drama-craft-check.test.mjs
  - .agents/skills/youtube-video/references/drama-craft.md
  - docs/videos/DRAMA.md
---

# Slideshow risk as craft rows: repeated setups, decorative shots, aimless motion, missing intent, text-first share, cinematic claims

## Why

Owner feedback on the first drama takes was "it looks like a slideshow"; `visual-quality.md`
turns that into work after the fact. The craft check (`core/craft.mjs`) measures pace, hook,
lines, sizes and motion but nothing structural about sameness. OpenMontage (AGPL — idea only)
scores a plan on six dimensions before any asset is paid for; the same six fit our storyboard
as craft rows, warned by `lint` and gated for the worker.

## Definition of done

- [x] Six rows exist with targets in `TARGETS`, a `REFERENCE` note each and a table row in
      `drama-craft.md`: `risk.setup_repeat` (same camera family + location words in consecutive
      shots), `risk.decorative` (no action verb / no subject in `prompt`), `risk.motion_purpose`
      (`motion` names a move with no event), `risk.intent` (neither a line, an `action_seconds`
      beat nor a reveal), `risk.text_first` (card scenes over shot scenes), `risk.cinematic_claim`
      (cinematic words in `prompt` with no size or move structure).
- [x] Each row misses on a storyboard built to fail it and passes on the drama fixture;
      `tools/drama-craft-check.test.mjs` has a `cases` entry per row.
- [x] At least one row is in `CRAFT_GATE_ROWS` after being measured on the two pilots, or the
      ticket says with numbers why none is.

## Steps

- [x] Rows + readers in `core/craft.mjs`; `drama_craft_check.mjs` cases; the table in
      `drama-craft.md`; a paragraph in `DRAMA.md` §品質.
- [x] Measure on `docs/videos/jingwei-fills-the-sea` and the 偶的江湖 pilot; pick the gate rows.

## How to verify

```bash
node --test tools/drama-craft-check.test.mjs tools/video/core/lint.test.mjs
node .agents/skills/youtube-video/scripts/drama_craft_check.mjs --file docs/videos/<slug>/video.json --json
```

## Notes

- 2026-10-05, done. Six rows in `core/craft.mjs` (`TARGETS.sameFramingRun` 2, `decorativeShare`
  0.1, `cameraAsActor` 0, `emptyBeatShare` 0.05, `cards` 2 + `cardShare` 0.1, `claims` 0) with
  three new readers (`placeOf`, `nobodyIn`, `cameraInMotion`, plus `castWords`), exported through
  `drama_craft_check.mjs`; `--json` rows carry `place` and `nobody`.
- Measured before picking the gate (the 精衛 pilot folder does not exist yet, so the fixture
  stood in for it): the five 偶的江湖 storyboards (451–459 scenes each) pass all six rows
  (`risk.intent` 1–4%, `risk.decorative` 0–1%, `risk.setup_repeat` ≤ 2, the rest 0); the drama
  fixture passes all six; the wedding E1 measured edit (the take the owner sent back) misses
  `risk.setup_repeat` with five hand inserts in a row (S03–S07) and passes the rest; E2 passes
  all six; the 15-shot pilot edit has no storyboard data and reads as passing.
- Gate: `risk.setup_repeat`, `risk.decorative`, `risk.text_first` joined `CRAFT_GATE_ROWS`
  (structure, zero misses on every approved storyboard, the rejected take caught). The other
  three read one line's words (`motion` camera clauses, prompt claim words, a silent look) and
  stay warnings: `risk.intent` at a zero target would have flagged 4–18 designed silent holds
  per episode, so its target is a 5% share; a first `CAMERA_CLAUSE` draft misread "the crane
  feather" as a crane move, which is why articles were dropped from it.
- Reading decisions: an over-the-shoulder is its own setup family (CU → OTS reverse → CU is three
  setups, not a repeat); a prompt that names no place inherits the previous shot's; a shot whose
  data has neither prompt nor motion (a measured edit without its storyboard) is not read as
  empty; inserts are never "decorative".
- `.claude/skills/youtube-video/` mirrors only SKILL.md, so the script and the reference needed no
  copy (`npm run test:tools` passes, 1701).
- No bound file: `lint.mjs` prints craft rows generically (the `(…drama-craft.md)` suffix is
  asserted in `lint.test.mjs`), `series.mjs` reads `CRAFT_GATE_ROWS` from craft.mjs.
- `SHOT_KEYS` in `core/drama.mjs` is bound and contested, so no `intent` field here; see
  `2026-10-05-delivery-promise-and-continuity-locks`.
- `drama-craft.md` is also named by `2026-10-04-drama-montage-beats-flash-cuts` and
  `2026-10-05-re-run-yt-shot-probe-past` (both P3, unclaimed).
