---
id: 2026-10-05-slideshow-risk-craft-rows
title: Slideshow risk as craft rows: repeated setups, decorative shots, aimless motion, missing intent, text-first share, cinematic claims
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-05T16:08:24Z
completed_at:
branch:
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

- [ ] Six rows exist with targets in `TARGETS`, a `REFERENCE` note each and a table row in
      `drama-craft.md`: `risk.setup_repeat` (same camera family + location words in consecutive
      shots), `risk.decorative` (no action verb / no subject in `prompt`), `risk.motion_purpose`
      (`motion` names a move with no event), `risk.intent` (neither a line, an `action_seconds`
      beat nor a reveal), `risk.text_first` (card scenes over shot scenes), `risk.cinematic_claim`
      (cinematic words in `prompt` with no size or move structure).
- [ ] Each row misses on a storyboard built to fail it and passes on the drama fixture;
      `tools/drama-craft-check.test.mjs` has a `cases` entry per row.
- [ ] At least one row is in `CRAFT_GATE_ROWS` after being measured on the two pilots, or the
      ticket says with numbers why none is.

## Steps

- [ ] Rows + readers in `core/craft.mjs`; `drama_craft_check.mjs` cases; the table in
      `drama-craft.md`; a paragraph in `DRAMA.md` §品質.
- [ ] Measure on `docs/videos/jingwei-fills-the-sea` and the 偶的江湖 pilot; pick the gate rows.

## How to verify

```bash
node --test tools/drama-craft-check.test.mjs tools/video/core/lint.test.mjs
node .agents/skills/youtube-video/scripts/drama_craft_check.mjs --file docs/videos/<slug>/video.json --json
```

## Notes

- No bound file: `lint.mjs` prints craft rows generically (the `(…drama-craft.md)` suffix is
  asserted in `lint.test.mjs`), `series.mjs` reads `CRAFT_GATE_ROWS` from craft.mjs.
- `SHOT_KEYS` in `core/drama.mjs` is bound and contested, so no `intent` field here; see
  `2026-10-05-delivery-promise-and-continuity-locks`.
- `drama-craft.md` is also named by `2026-10-04-drama-montage-beats-flash-cuts` and
  `2026-10-05-re-run-yt-shot-probe-past` (both P3, unclaimed).
